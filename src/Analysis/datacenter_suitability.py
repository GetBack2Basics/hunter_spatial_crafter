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
            MIN(ST_Distance(z.net_developable_geom, ST_Transform(e.geometry, 'EPSG:4326', 'EPSG:7856'))) AS dist_to_power_m
        FROM org_catalog.fgsdb.macquarie_net_developable_zones z
        CROSS JOIN org_catalog.fgsdb.macquarie_energy_infrastructure e
        GROUP BY z.precinct_key
    """).toPandas()
    
    # Minimum distance from developable zones to rail network
    rail_dist_df = spark.sql("""
        SELECT 
            z.precinct_key,
            MIN(ST_Distance(z.net_developable_geom, r.geometry)) AS dist_to_rail_m
        FROM org_catalog.fgsdb.macquarie_net_developable_zones z
        CROSS JOIN org_catalog.fgsdb.macquarie_rail_network r
        GROUP BY z.precinct_key
    """).toPandas()
    
    # Calculate developable zones area
    zones_df = spark.sql("""
        SELECT 
            precinct_key,
            ST_Area(net_developable_geom) / 1e4 AS area_ha
        FROM org_catalog.fgsdb.macquarie_net_developable_zones
    """).toPandas()
    
    # Merge metrics
    metrics_df = zones_df.merge(power_dist_df, on="precinct_key").merge(rail_dist_df, on="precinct_key")
    
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
        energy_gdf.plot(ax=ax, color="#f1c40f", linewidth=1.8, alpha=0.8, label="Electricity lines (HV)")
    if not rail_gdf.empty:
        rail_gdf.plot(ax=ax, color="#e74c3c", linewidth=2.5, label="Active Railway network")
        
    # Developable Zones (suitability ranking colored)
    if not net_developable_gdf.empty:
        # Merge suitability scores to spatial dataframe
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

if __name__ == "__main__":
    main()
