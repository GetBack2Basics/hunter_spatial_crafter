#!/usr/bin/env python3
"""
Macquarie Coal Complex Transformation Precinct — Spatial ETL Module.

This module ingests Lake Mac Open Data, NSW SEED, ABS Meshblocks and
TfNSW openspace layers, builds constraint masks (water, biodiversity,
pipelines, TSF inundation), computes net developable zones by
sub-precinct, and persists outputs under org_catalog.fgsdb.macquarie_*
via Havasu/Iceberg.

Data root: wherobots://fgsdb/macquarie         (see config/macquarie.json)
Target CRS: EPSG:7856  GDA2020 / MGA Zone 56  — metric-safe for buffering
Source CRS: EPSG:4326  WGS84                   — GeoJSON / SEED native
"""

import os
import sys

if __package__ is None or __package__ == "":
    import subprocess
    for pkg in ["requests", "pandas", "geopandas", "pyproj"]:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

import json
import requests
import pandas as pd
import geopandas as gpd

from sedona.spark import SedonaContext
from pyspark.sql.functions import col, to_json, expr, lit, when, concat_ws

try:
    import pyproj
except ImportError:
    import subprocess, sys as _sys
    subprocess.check_call([_sys.executable, "-m", "pip", "install", "--quiet", "pyproj"])
    import pyproj

# =============================================================================
# Utilities
# =============================================================================

def _cfg() -> dict:
    env = os.getenv("WHEROBOTS_ENV", "dev")
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, f"config/{env}.json"),
        os.path.join(here, "config/macquarie.json"),
        os.path.join(here, f"{env}.json"),
        os.path.join(here, "macquarie.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
            if cfg.get("environment", env) in ("macquarie", env):
                return cfg
    raise FileNotFoundError("Missing config for precinct ingest. Expected config/macquarie.json or macquarie.json alongside module.")


def _sedona() -> SedonaContext:
    return SedonaContext.create(SedonaContext.builder().getOrCreate())


def _fetch_featureserver_geojson(base_url: str, layer_id: int, max_features: int = 5000) -> list:
    query_url = f"{base_url}/{layer_id}/query"
    out = []
    offset = 0
    page = 1000
    while len(out) < max_features:
        params = {
            "where": "1=1",
            "outFields": "*",
            "f": "geojson",
            "outSR": "4326",
            "resultOffset": offset,
            "resultRecordCount": page,
        }
        resp = requests.get(query_url, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"[macquarie] FeatureServer partial or complete stop at HTTP {resp.status_code}: {query_url}")
            break
        features = resp.json().get("features", [])
        if not features:
            break
        out.extend(features)
        if len(features) < page or len(out) >= max_features:
            break
        offset += page
    print(f"[macquarie] Retrieved {len(out)} features from {query_url}")
    return out


def _to_sedona(sedona: SedonaContext, gdf: gpd.GeoDataFrame, srid: int = 4326) -> "pyspark.sql.DataFrame":
    gdf = gdf.copy()
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    if getattr(gdf.crs, "to_epsg", None)() != srid:
        gdf.to_crs(epsg=srid, inplace=True)
    gdf["wkt_geometry"] = gdf.geometry.apply(lambda g: g.wkt if g is not None else None)
    pdf = pd.DataFrame(gdf.drop(columns=["geometry"]))
    for col_name in pdf.columns:
        if pd.api.types.is_numeric_dtype(pdf[col_name]):
            pdf[col_name] = pdf[col_name].astype(float)
        else:
            pdf[col_name] = pdf[col_name].astype(str).replace({"nan": None, "<NA>": None, "None": None})
    sdf = sedona.createDataFrame(pdf)
    return sdf.withColumn("geometry", expr(f"ST_GeomFromWKT(wkt_geometry)")).drop("wkt_geometry")


def save_table(sedona: SedonaContext, sdf, table_name: str, storage_root: str, partition_col: str = "precinct_key"):
    is_wherobots = os.getenv("WHEROBOTS_ENV") in ("stg", "prod") or storage_root.startswith("wherobots://")
    full_name = f"org_catalog.fgsdb.{table_name}"
    if is_wherobots:
        try:
            sedona.sql("CREATE DATABASE IF NOT EXISTS org_catalog.fgsdb")
            writer = sdf.write.format("havasu.iceberg").mode("overwrite")
            if partition_col:
                writer = writer.partitionBy(partition_col)
            writer.saveAsTable(full_name)
            print(f"[macquarie] Saved Havasu table: {full_name}")
            return
        except Exception as exc:
            print(f"[macquarie] Havasu save failed ({exc}); falling back to GeoParquet")
    clean_root = storage_root
    if clean_root.startswith("wherobots://"):
        clean_root = "file:///tmp/macquarie"
    path = f"{clean_root}/{table_name}.parquet"
    writer = sdf.write.format("geoparquet").mode("overwrite")
    if partition_col:
        writer = writer.partitionBy(partition_col)
    writer.save(path)
    print(f"[macquarie] Saved GeoParquet: {path}")


# =============================================================================
# 1. Precinct boundary and sub-precincts
# =============================================================================

def load_precinct_boundary(sedona: SedonaContext, storage_root: str) -> None:
    """
    Loads/creates precinct boundary and sub-precinct metadata.
    Replace the placeholder geometry with an actual precinct boundary when available.
    """
    placeholder = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"precinct": "MacquarieCoalComplex", "precinct_key": "mcc"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [151.65, -32.93], [151.72, -32.93],
                        [151.72, -32.88], [151.65, -32.88], [151.65, -32.93]
                    ]],
                },
            }
        ],
    }
    import pyproj
    tgt = _cfg().get("target_crs", "EPSG:7856")
    tgt_epsg = int(tgt.split(":")[1]) if ":" in tgt else 7856
    gdf = gpd.GeoDataFrame.from_features(placeholder, crs="EPSG:4326")
    gdf = gdf.to_crs(tgt)
    boundary_sdf = _to_sedona(sedona, gdf, srid=tgt_epsg).withColumn("precinct_key", lit("mcc"))
    save_table(sedona, boundary_sdf, "macquarie_precinct_boundary", storage_root, partition_col=None)

    sub_precincts = pd.DataFrame([
        {"sub_precinct": "Killingworth",  "precinct_key": "mcc", "use_case": "AdvancedMfg_DataHub"},
        {"sub_precinct": "WestLake",      "precinct_key": "mcc", "use_case": "NatureTourism_Recreation"},
        {"sub_precinct": "CockleCreek",   "precinct_key": "mcc", "use_case": "IndustrialGateway_TSF"},
        {"sub_precinct": "Teralba",       "precinct_key": "mcc", "use_case": "TransitOriented_Residential"},
    ])
    sub_sdf = sedona.createDataFrame(sub_precincts)
    save_table(sedona, sub_sdf, "macquarie_sub_precincts", storage_root, partition_col=None)
    print("[macquarie] Loaded precinct boundary + sub-precinct registry")


# =============================================================================
# 2. Water / Hydrology
# =============================================================================

def load_water_infrastructure(sedona: SedonaContext, storage_root: str, cfg: dict) -> None:
    tgt = cfg.get("target_crs", "EPSG:7856")
    tgt_epsg = int(tgt.split(":")[1]) if ":" in tgt else 7856

    hydro_url = f"{cfg['data_sources']['nsw_seed']}/Hydrography_Watercourses/MapServer/0/query?where=1%3D1&outFields=*&f=geojson"
    print("[macquarie] Fetching NSW SEED Hydrography …")
    resp = requests.get(hydro_url, timeout=30)
    resp.raise_for_status()
    tbl = gpd.GeoDataFrame.from_features(resp.json(), crs="EPSG:4326")
    if tbl.empty:
        print("[macquarie] WARNING: hydrography returned empty; skipping.")
        return
    gdf = tbl.to_crs(tgt)
    hydro_sdf = _to_sedona(sedona, gdf, srid=tgt_epsg).withColumn("layer", lit("seed_hydrography"))
    save_table(sedona, hydro_sdf, "macquarie_water_hydrography", storage_root, partition_col=None)
    print("[macquarie] Water infrastructure loaded.")


# =============================================================================
# 3. Biodiversity / constraints
# =============================================================================

def load_biodiversity_constraints(sedona: SedonaContext, storage_root: str, cfg: dict) -> None:
    tgt = cfg.get("target_crs", "EPSG:7856")
    tgt_epsg = int(tgt.split(":")[1]) if ":" in tgt else 7856

    bio_url = f"{cfg['data_sources']['nsw_seed']}/High_Biodiversity_Values/MapServer/0/query?where=1%3D1&outFields=*&f=geojson"
    print("[macquarie] Fetching NSW SEED High Biodiversity Values …")
    resp = requests.get(bio_url, timeout=30)
    if resp.status_code != 200:
        print(f"[macquarie] Biodiversity layer skipped: HTTP {resp.status_code}")
        return
    tbl = gpd.GeoDataFrame.from_features(resp.json(), crs="EPSG:4326")
    if tbl.empty:
        print("[macquarie] WARNING: biodiversity layer empty.")
        return
    gdf = tbl.to_crs(tgt)
    bio_sdf = _to_sedona(sedona, gdf, srid=tgt_epsg).withColumn("layer", lit("seed_biodiversity"))
    save_table(sedona, bio_sdf, "macquarie_biodiversity_constraints", storage_root, partition_col=None)
    print("[macquarie] Biodiversity constraints loaded.")


# =============================================================================
# 4. Energy infrastructure
# =============================================================================

def load_energy_infrastructure(sedona: SedonaContext, storage_root: str, cfg: dict) -> None:
    tgt = cfg.get("target_crs", "EPSG:7856")
    tgt_epsg = int(tgt.split(":")[1]) if ":" in tgt else 7856
    nsw_base = cfg["data_sources"]["nsw_spatial_services"]
    candidate_themes = [
        f"{nsw_base}/Electricity_Infrastructure/FeatureServer",
        f"{nsw_base}/Electricity_Transmission_Network/FeatureServer",
    ]
    frames = []
    for theme in candidate_themes:
        for layer_id in (0, 1, 2):
            try:
                feats = _fetch_featureserver_geojson(theme, layer_id, max_features=2000)
                if feats:
                    gdf = gpd.GeoDataFrame.from_features(feats, crs="EPSG:4326")
                    if not gdf.empty:
                        frames.append(gdf)
                        break
            except Exception as exc:
                print(f"[macquarie] Skipping electricity theme layer {theme} {layer_id}: {exc}")
    if not frames:
        print("[macquarie] No electricity features retrieved; skipping energy infrastructure.")
        return
    combined = pd.concat(frames, ignore_index=True)
    gdf_all = gpd.GeoDataFrame(combined, crs="EPSG:4326").to_crs(tgt)
    energy_sdf = _to_sedona(sedona, gdf_all, srid=tgt_epsg).withColumn("layer", lit("energy_infrastructure"))
    save_table(sedona, energy_sdf, "macquarie_energy_infrastructure", storage_root, partition_col="layer")
    print("[macquarie] Energy infrastructure loaded.")


# =============================================================================
# 5. Pipeline corridors
# =============================================================================

def load_pipeline_corridors(sedona: SedonaContext, storage_root: str, cfg: dict) -> None:
    tgt = cfg.get("target_crs", "EPSG:7856")
    tgt_epsg = int(tgt.split(":")[1]) if ":" in tgt else 7856
    nsw_base = cfg["data_sources"]["nsw_spatial_services"]
    candidate_themes = [
        f"{nsw_base}/Pipeline_Corridors/FeatureServer",
        f"{nsw_base}/Gas_Pipelines/FeatureServer",
        f"{nsw_base}/Petroleum_Pipelines/FeatureServer",
    ]
    frames = []
    for theme in candidate_themes:
        for layer_id in (0, 1):
            try:
                feats = _fetch_featureserver_geojson(theme, layer_id, max_features=2000)
                if feats:
                    gdf = gpd.GeoDataFrame.from_features(feats, crs="EPSG:4326")
                    if not gdf.empty:
                        frames.append(gdf)
                        break
            except Exception as exc:
                print(f"[macquarie] Skipping pipeline theme layer {theme} {layer_id}: {exc}")
    if not frames:
        print("[macquarie] No pipeline features retrieved; using placeholder for safety buffer modeling.")
        return
    combined = pd.concat(frames, ignore_index=True)
    gdf_all = gpd.GeoDataFrame(combined, crs="EPSG:4326").to_crs(tgt)
    pipe_sdf = _to_sedona(sedona, gdf_all, srid=tgt_epsg).withColumn("layer", lit("pipeline_corridor"))
    save_table(sedona, pipe_sdf, "macquarie_pipeline_corridors", storage_root, partition_col="layer")
    print("[macquarie] Pipeline corridors loaded.")


# =============================================================================
# 6. Rail + Active transport networks
# =============================================================================

def load_transport_networks(sedona: SedonaContext, storage_root: str, cfg: dict) -> None:
    tgt = cfg.get("target_crs", "EPSG:7856")
    tgt_epsg = int(tgt.split(":")[1]) if ":" in tgt else 7856
    src = cfg.get("source_crs", "EPSG:4326")

    try:
        existing = sedona.table("org_catalog.fgsdb.nsw_train_lines")
        existing_df = existing.withColumn("layer", lit("main_northern_rail"))
        existing_df = existing_df.withColumn(
            "geometry",
            expr(f"ST_Transform(ST_SetSRID(geometry, 4326), 'EPSG:4326', '{tgt}')")
        )
        save_table(sedona, existing_df, "macquarie_rail_network", storage_root, partition_col="layer")
        print("[macquarie] Reused cached NSW train lines (reprojected to target CRS) for precinct rail network.")
    except Exception:
        print("[macquarie] No cached NSW train lines; fetching NSW Spatial Services")
        theme = cfg["data_sources"]["nsw_spatial_services"] + "/NSW_Transport_Theme/FeatureServer"
        feats = _fetch_featureserver_geojson(theme, 7, max_features=4000)
        if not feats:
            print("[macquarie] Could not fetch rail lines; leaving rail network empty.")
        else:
            gdf = gpd.GeoDataFrame.from_features(feats, crs=src)
            if gdf.crs is None:
                gdf = gdf.set_crs(src)
            gdf = gdf.to_crs(tgt)
            rail_sdf = _to_sedona(sedona, gdf, srid=tgt_epsg).withColumn("layer", lit("main_northern_rail"))
            save_table(sedona, rail_sdf, "macquarie_rail_network", storage_root, partition_col="layer")
            print("[macquarie] Rail network loaded and reprojected to target CRS.")

    active_urls = [
        cfg["data_sources"]["lakemac_open_data"] + "/cycling-routes-way-finding-map/exports/geojson",
        cfg["data_sources"]["lakemac_open_data"] + "/walking-pedestrian-routes/exports/geojson",
    ]
    active_frames = []
    for url in active_urls:
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                gdf = gpd.GeoDataFrame.from_features(r.json(), crs=src)
                if not gdf.empty:
                    active_frames.append(gdf)
        except Exception as exc:
            print(f"[macquarie] Active transport dataset skip: {exc}")
    if active_frames:
        gdf_all = pd.concat(active_frames, ignore_index=True)
        gdf_all = gpd.GeoDataFrame(gdf_all, crs=src).to_crs(tgt)
        active_sdf = _to_sedona(sedona, gdf_all, srid=tgt_epsg).withColumn("layer", lit("active_transport"))
        save_table(sedona, active_sdf, "macquarie_active_transport", storage_root, partition_col="layer")
        print("[macquarie] Active transport loaded and reprojected to target CRS.")
    else:
        print("[macquarie] No active transport datasets retrieved.")


# =============================================================================
# 7. ABS Meshblocks clipped to precinct
# =============================================================================

def load_abs_meshblocks(sedona: SedonaContext, storage_root: str, cfg: dict) -> None:
    tgt = cfg.get("target_crs", "EPSG:7856")
    tgt_epsg = int(tgt.split(":")[1]) if ":" in tgt else 7856
    abs_fs = cfg["data_sources"]["abs_digital_atlas"]
    params = {
        "where": "LGA_NAME21='Lake Macquarie' OR LGA_NAME21='Lake Macquarie City'",
        "outFields": "*",
        "f": "geojson",
        "outSR": "4326",
        "returnGeometry": "true",
    }
    print("[macquarie] Fetching ABS Meshblocks for Lake Macquarie …")
    r = requests.get(f"{abs_fs}/query", params=params, timeout=60, allow_redirects=True)
    if r.status_code != 200:
        print(f"[macquarie] ABS Meshblocks HTTP {r.status_code}; try broader filter later.")
        return
    tbl = gpd.GeoDataFrame.from_features(r.json(), crs="EPSG:4326")
    if tbl.empty:
        print("[macquarie] WARNING: ABS Meshblock response empty.")
        return
    gdf = tbl.to_crs(tgt)
    mb_sdf = _to_sedona(sedona, gdf, srid=tgt_epsg).withColumn("layer", lit("abs_meshblocks"))
    save_table(sedona, mb_sdf, "macquarie_abs_meshblocks", storage_root, partition_col="layer")
    print("[macquarie] ABS Meshblocks loaded.")


# =============================================================================
# 8. Spatial processing: constraints overlay → net developable zones
# =============================================================================

def build_net_developable_zones(sedona: SedonaContext, storage_root: str, cfg: dict) -> None:
    target_crs = cfg.get("target_crs", "EPSG:7856")
    src = cfg.get("source_crs", "EPSG:4326")
    buffers = cfg.get("buffers_m", {})

    sedona.sql(f"""
        CREATE OR REPLACE TEMP VIEW precinct_transform AS
        SELECT precinct_key,
               ST_Transform(geometry, '{src}', '{target_crs}') AS geom
        FROM org_catalog.fgsdb.macquarie_precinct_boundary
    """)

    # Assemble constraints with metric buffers where specified
    constraints = []

    hydro = f"SELECT 'hydro_30m' AS constraint_type, ST_Buffer(ST_Transform(geometry, '{src}','{target_crs}'), 30.0) AS geom FROM org_catalog.fgsdb.macquarie_water_hydrography"
    constraints.append(hydro)

    bio = f"SELECT 'biodiversity' AS constraint_type, ST_Transform(geometry, '{src}','{target_crs}') AS geom FROM org_catalog.fgsdb.macquarie_biodiversity_constraints"
    constraints.append(bio)

    try:
        pipe_q = f"SELECT 'pipeline_20m' AS constraint_type, ST_Buffer(ST_Transform(geometry, '{src}','{target_crs}'), 20.0) AS geom FROM org_catalog.fgsdb.macquarie_pipeline_corridors"
        constraints.append(pipe_q)
    except Exception:
        print("[macquarie] Pipeline constraints table missing; buffer step skipped.")

    rail_q = f"SELECT 'rail_10m' AS constraint_type, ST_Buffer(ST_Transform(geometry, '{src}','{target_crs}'), 10.0) AS geom FROM org_catalog.fgsdb.macquarie_rail_network"
    constraints.append(rail_q)

    unioned = " UNION ALL ".join(constraints)
    sedona.sql(f"CREATE OR REPLACE TEMP VIEW constraints AS {unioned}")

    net = sedona.sql(f"""
        SELECT
            p.precinct_key,
            ST_Difference(p.geom, ST_Union_Aggregate(c.geom)) AS net_developable_geom
        FROM precinct_transform p
        LEFT JOIN constraints c ON ST_Intersects(p.geom, c.geom)
        GROUP BY p.precinct_key, p.geom
    """)
    if "precinct" in net.columns:
        net = net.drop("precinct")

    save_table(sedona, net, "macquarie_net_developable_zones", storage_root, partition_col="precinct_key")
    print("[macquarie] Computed net developable zones.")


# =============================================================================
# 9. Verification
# =============================================================================

def run_verification(sedona: SedonaContext) -> None:
    print("\n[demo] Tables now available under org_catalog.fgsdb:")
    for row in sedona.sql("SHOW TABLES IN org_catalog.fgsdb").collect():
        print("  -", row["tableName"])

    for tbl in [
        "macquarie_precinct_boundary",
        "macquarie_water_hydrography",
        "macquarie_biodiversity_constraints",
        "macquarie_energy_infrastructure",
        "macquarie_pipeline_corridors",
        "macquarie_rail_network",
        "macquarie_active_transport",
        "macquarie_abs_meshblocks",
        "macquarie_net_developable_zones",
    ]:
        try:
            cnt = sedona.table(f"org_catalog.fgsdb.{tbl}").count()
            print(f"[demo] {tbl}: {cnt} rows")
        except Exception as exc:
            print(f"[demo] {tbl} unavailable: {exc}")


# =============================================================================
# Main
# =============================================================================

def main():
    storage_root = _cfg().get("storage_root", "wherobots://fgsdb/macquarie")
    print(f"[macquarie] Storage root: {storage_root}")
    sedona = _sedona()
    sedona.sql("CREATE DATABASE IF NOT EXISTS org_catalog.fgsdb")

    load_precinct_boundary(sedona, storage_root)
    load_water_infrastructure(sedona, storage_root, _cfg())
    load_biodiversity_constraints(sedona, storage_root, _cfg())
    load_energy_infrastructure(sedona, storage_root, _cfg())
    load_pipeline_corridors(sedona, storage_root, _cfg())
    load_transport_networks(sedona, storage_root, _cfg())
    load_abs_meshblocks(sedona, storage_root, _cfg())
    build_net_developable_zones(sedona, storage_root, _cfg())
    run_verification(sedona)
    print("\n[macquarie] Macquarie ETL complete.")


if __name__ == "__main__":
    main()
