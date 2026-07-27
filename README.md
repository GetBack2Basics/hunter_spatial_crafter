# Hunter Spatial Crafter

Spatial ETL and analytics pipelines for precinct planning, starting with the Macquarie Coal Complex Transformation Precinct.

## Overview

This project provides tools to ingest and process spatial datasets for the Macquarie Coal Complex precinct. It integrates:
- Lake Macquarie City Council Open Data
- NSW SEED Portal (Hydrography and Biodiversity)
- ABS Meshblocks
- Transport for NSW (TfNSW) Spatial Networks

The ETL pipeline builds constraint masks (water, biodiversity, pipelines, active rail corridors), computes net developable zones, and prepares clean spatial layers for precinct planning.

## Project Structure

- `src/Ingestion/macquarie_spatial_ingest.py`: Core python script implementing the Sedona Spark spatial ETL.
- `src/Analysis/national_suitability_analysis.py`: 5-Tier Spatial Constraint Model (Terrain Slope, Mine Subsidence, Flood Outfalls, Power Grid, and Water) to benchmark candidate sites nationally.
- `config/macquarie.json`: Configuration settings, coordinate reference system (CRS) parameters, buffer thresholds, and data source endpoints.
- `runner/macquarie_etl_runner.html`: A premium HTML runner UI with a vertical timeline, step status indicators, and millisecond-accurate execution timers.
- `notebooks/Macquarie_Coal_Complex_Spatial_ETL.ipynb`: Interactive Jupyter Notebook outlining the local spatial ETL steps and visualization.
- `notebooks/National_Siting_Dashboard.ipynb`: Interactive dashboard containing Kepler.gl suitability maps and multi-state/regional benchmarking matrices.
