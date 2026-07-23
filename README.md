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
- `config/macquarie.json`: Configuration settings, coordinate reference system (CRS) parameters, buffer thresholds, and data source endpoints.
- `notebooks/Macquarie_Coal_Complex_Spatial_ETL.ipynb`: Interactive Jupyter Notebook outlining the spatial ETL steps and visualization.
