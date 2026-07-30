import sys
import io
import os
import base64
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely import wkt

from sedona.spark import *
from pyspark.sql import SparkSession

def df_to_gdf(df, geom_col="geometry"):
    pdf = df.toPandas()
    if pdf.empty:
        return gpd.GeoDataFrame()
    if geom_col in pdf.columns:
        geoms = pdf[geom_col].apply(lambda g: wkt.loads(g) if g else None)
        if geom_col != "geometry":
            pdf = pdf.drop(columns=[geom_col])
        pdf["geometry"] = geoms
    gdf = gpd.GeoDataFrame(pdf, geometry="geometry", crs="EPSG:7856")
    return gdf

def score_power(dist):
    if dist is None or pd.isna(dist):
        return 0.0
    # Closer to high-voltage lines is better (ideal < 250m)
    if dist <= 250:
        return 100.0
    elif dist >= 2000:
        return 0.0
    else:
        return 100.0 - ((dist - 250) / 1750) * 100.0

def score_size(area):
    # Larger parcels are better for data centers (ideal > 15 ha)
    if area >= 15.0:
        return 100.0
    elif area < 3.0:
        return 0.0
    else:
        return ((area - 3.0) / 12.0) * 100.0

def main():
    print("[analysis] Initializing SedonaContext...")
    spark = SedonaContext.create(SedonaContext.builder().getOrCreate())
    spark.sparkContext.setLogLevel("WARN")
    
    print("[analysis] Loading zones and computing spatial metrics...")
    
    # 1. Load boundaries and infrastructure
    precinct_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_precinct_boundary"))
    study_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_study_area_boundary"))
    net_developable_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(net_developable_geom) as geometry, precinct_key FROM org_catalog.fgsdb.macquarie_net_developable_zones"))
    energy_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_energy_infrastructure"))
    rail_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry, layer FROM org_catalog.fgsdb.macquarie_rail_network"))
    water_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_water_hydrography LIMIT 1000"))
    biodiversity_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_biodiversity_constraints LIMIT 1000"))
    
    # 2. Compute spatial join metrics on Sedona Spark
    # Minimum distance from developable zones to energy transmission line
    power_dist_df = spark.sql("""
        SELECT 
            z.precinct_key,
            MIN(ST_Distance(z.net_developable_geom, e.geometry)) AS dist_to_power_m
        FROM org_catalog.fgsdb.macquarie_net_developable_zones z
        LEFT JOIN org_catalog.fgsdb.macquarie_energy_infrastructure e
          ON ST_DWithin(z.net_developable_geom, e.geometry, 2000.0)
        GROUP BY z.precinct_key
    """).toPandas()
    
    # Minimum distance from developable zones to rail network
    rail_dist_df = spark.sql("""
        SELECT 
            z.precinct_key,
            MIN(ST_Distance(z.net_developable_geom, r.geometry)) AS dist_to_rail_m
        FROM org_catalog.fgsdb.macquarie_net_developable_zones z
        LEFT JOIN org_catalog.fgsdb.macquarie_rail_network r
          ON ST_DWithin(z.net_developable_geom, r.geometry, 20000.0)
        GROUP BY z.precinct_key
    """).toPandas()

    import numpy as np

    # Calculate developable zones area
    zones_df = spark.sql("""
        SELECT 
            precinct_key,
            ST_Area(net_developable_geom) / 1e4 AS area_ha
        FROM org_catalog.fgsdb.macquarie_net_developable_zones
    """).toPandas()
    
    # Merge metrics
    metrics_df = zones_df.merge(power_dist_df, on="precinct_key").merge(rail_dist_df, on="precinct_key")
    
    # Thermodynamic decay & heat symbiosis routing
    metrics_df["dc_to_symbiosis_dist_m"] = metrics_df["dist_to_power_m"].fillna(1000.0).apply(lambda d: float(max(150.0, min(1200.0, d * 0.5))))
    
    t_source = 45.0
    t_ambient = 15.0
    k_heat = 0.0008
    metrics_df["t_delivery_c"] = t_source - (t_source - t_ambient) * (1.0 - np.exp(-k_heat * metrics_df["dc_to_symbiosis_dist_m"]))
    
    metrics_df["max_viable_pipe_m"] = -np.log(2.0/3.0) / k_heat
    metrics_df["is_thermal_symbiosis_viable"] = metrics_df["dc_to_symbiosis_dist_m"] <= metrics_df["max_viable_pipe_m"]

    # Thermal discharge naturalization cooling distance
    t_discharge = 35.0
    t_target = t_ambient + 1.0 # 16°C
    k_discharge = 0.005
    metrics_df["discharge_cooling_distance_m"] = -np.log((t_target - t_ambient) / (t_discharge - t_ambient)) / k_discharge

    # Pumped Hydro Potential storage capacity
    elevation_heads = {
        "mcc": 150.0,
        "Killingworth": 120.0,
        "West Lake": 180.0,
        "Cockle Creek": 25.0,
        "Teralba": 45.0
    }
    metrics_df["elevation_head_m"] = metrics_df["precinct_key"].map(elevation_heads).fillna(150.0)
    metrics_df["head_pressure_mpa"] = (1000.0 * 9.81 * metrics_df["elevation_head_m"]) / 1e6
    
    v_reservoir = 500000.0
    eta_eff = 0.80
    metrics_df["pumped_hydro_capacity_mwh"] = (eta_eff * 1000.0 * v_reservoir * 9.81 * metrics_df["elevation_head_m"]) / 3.6e9

    # Network routing distance vs straight line
    metrics_df["winding_factor"] = metrics_df["precinct_key"].apply(lambda k: 1.45 if k in ["West Lake", "Teralba"] else 1.35)
    metrics_df["dist_to_power_network_m"] = metrics_df["dist_to_power_m"] * metrics_df["winding_factor"]
    metrics_df["dist_to_rail_network_m"] = metrics_df["dist_to_rail_m"] * metrics_df["winding_factor"]

    # Compute scores
    metrics_df["power_score"] = metrics_df["dist_to_power_m"].apply(score_power)
    metrics_df["size_score"] = metrics_df["area_ha"].apply(score_size)
    metrics_df["suitability_score"] = (metrics_df["power_score"] * 0.6) + (metrics_df["size_score"] * 0.4)
    metrics_df = metrics_df.sort_values(by="suitability_score", ascending=False)
    
    print("===START_SUITABILITY_TABLE===")
    print(metrics_df.to_json(orient="records"))
    print("===END_SUITABILITY_TABLE===")

    # 3. Generating Plot
    print("[analysis] Generating suitability plot...")
    fig, ax = plt.subplots(figsize=(8, 7))
    
    if not study_gdf.empty:
        study_gdf.plot(ax=ax, facecolor="none", edgecolor="#7f8c8d", linestyle="--", linewidth=1.5, label="Study Area Boundary")
    if not precinct_gdf.empty:
        precinct_gdf.plot(ax=ax, facecolor="none", edgecolor="#2c3e50", linewidth=2.5, label="Precinct Boundary")
        
    # Constraints
    if not biodiversity_gdf.empty:
        biodiversity_gdf.plot(ax=ax, facecolor="#2ecc71", alpha=0.3, edgecolor="none", label="Biodiversity Constraints")
    if not water_gdf.empty:
        water_gdf.plot(ax=ax, facecolor="#3498db", edgecolor="#2980b9", alpha=0.3, label="Riparian Streams")
        
    # Infrastructure
    if not energy_gdf.empty:
    try:
        print("[analysis] Loading zones and computing spatial metrics...")
        
        # 1. Load boundaries and infrastructure
        precinct_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_precinct_boundary"))
        study_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_study_area_boundary"))
        net_developable_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(net_developable_geom) as geometry, precinct_key FROM org_catalog.fgsdb.macquarie_net_developable_zones"))
        energy_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_energy_infrastructure"))
        rail_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry, layer FROM org_catalog.fgsdb.macquarie_rail_network"))
        water_gdf = df_to_gdf(spark.sql("SELECT ST_AsText(geometry) as geometry FROM org_catalog.fgsdb.macquarie_water_hydrography LIMIT 1000"))
        
        metrics = []
        for idx, row in net_developable_gdf.iterrows():
            geom = row.geometry
            if geom is None:
                continue
            
            # Area in Hectares (EPSG:7856 is in meters)
            area_ha = geom.area / 10000.0
            
            # Distance to Energy Infrastructure
            dist_energy = energy_gdf.distance(geom).min() if len(energy_gdf) > 0 else 99999.0
            
            # Distance to Water
            dist_water = water_gdf.distance(geom).min() if len(water_gdf) > 0 else 99999.0
            
            # Distance to Rail
            dist_rail = rail_gdf.distance(geom).min() if len(rail_gdf) > 0 else 99999.0
            
            # Sub-scores
            s_power = score_power(dist_energy)
            s_size = score_size(area_ha)
            
            # Overall Suitability Score (0 - 100)
            overall_score = round((s_power * 0.6) + (s_size * 0.4), 1)
            
            metrics.append({
                "precinct_key": row["precinct_key"],
                "area_ha": round(area_ha, 2),
                "dist_energy_m": round(dist_energy, 1),
                "dist_water_m": round(dist_water, 1),
                "dist_rail_m": round(dist_rail, 1),
                "suitability_score": overall_score
            })
            
        metrics_df = pd.DataFrame(metrics)
        print("\n[analysis] Data Center Suitability Analysis Metrics:")
        print(metrics_df.to_string(index=False))
        
        # 2. Render plot
        fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
        
        # Plot study area and precinct boundary
        if len(study_gdf) > 0:
            study_gdf.plot(ax=ax, color="#f8f9fa", edgecolor="#bdc3c7", linestyle="--", label="Study Area (5km)")
        if len(precinct_gdf) > 0:
            precinct_gdf.plot(ax=ax, color="none", edgecolor="#2c3e50", linewidth=2, label="Precinct Boundary")
        if len(energy_gdf) > 0:
            energy_gdf.plot(ax=ax, color="#e74c3c", linewidth=1.5, label="High-Voltage Transmission")
        if len(rail_gdf) > 0:
            rail_gdf.plot(ax=ax, color="#34495e", linewidth=1.2, linestyle=":", label="Rail Infrastructure")
            
        if len(net_developable_gdf) > 0:
            net_developable_gdf = net_developable_gdf.merge(metrics_df, on="precinct_key")
            net_developable_gdf.plot(
                ax=ax, 
                column="suitability_score", 
                cmap="Oranges", 
                edgecolor="#e67e22", 
                linewidth=3.0, 
                legend=True, 
                legend_kwds={'label': "Data Center Suitability Score"},
                label="Developable Zones"
            )
            
        plt.title("Macquarie Precinct Data Center Suitability Analysis", fontsize=14, fontweight="bold")
        plt.xlabel("Easting (m) - EPSG:7856", fontsize=10)
        plt.ylabel("Northing (m) - EPSG:7856", fontsize=10)
        plt.grid(True, which='both', color='#ecf0f1', linestyle='-', linewidth=0.5)
        
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc="upper right")
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=60, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        print("===START_B64_IMAGE===")
        chunk_size = 80
        for i in range(0, len(img_str), chunk_size):
            print(img_str[i:i+chunk_size])
        print("===END_B64_IMAGE===")
        print("[analysis] Analysis job finished successfully.")
    finally:
        print("[analysis] Stopping SedonaContext session...")
        spark.stop()

if __name__ == "__main__":
    main()
