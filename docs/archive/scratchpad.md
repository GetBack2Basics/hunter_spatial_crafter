# Technical Scratchpad: Wherobots Resource, Editorial & Baselines Alignment

## Summary of Editorial Review & Plan Execution (28 Aug 2026)

### 1. Simulated Regional Baselines vs. Measured Ground-Truth
- **Policy Sensitivity**: During the active National Cabinet debate on AI data center grid load and regional transition hubs, modeled benchmark numbers must never be quoted or published as measured engineering site figures.
- **Explicit Designation**:
  - Interstate candidates (**Latrobe Valley in VIC, Collie in WA, Gladstone in QLD, etc.**) are explicitly labeled **"Simulated Regional Baseline"** across all text, callout boxes, footnotes, and candidate tables in [`docs/wherobots_ai_data_center_suitability_blog.html`](file:///c:/Projects/hunter_spatial_crafter/docs/wherobots_ai_data_center_suitability_blog.html) and [`runner/national_suitability_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html).
  - Contrasting baseline: The **NSW Hunter precinct** sites have fully measured ground-truth spatial constraints (riparian 30m, high-pressure pipeline 20m, DEM slope >5%, tailings hazards, and cadastral lot/plan boundaries).

### 2. Available Portal Scale vs. Ingested Pilot Scope Distinction
- **Portal Available Universe**: 15.91M total geometries across 16 Australian national & state portals (including 15.4M Geoscape parcels, 368k ABS meshblocks, and 47,510 national sensitive receptor POIs via ACARA, NHSD, and OSM).
- **Ingested Pilot & QA Scope**:
  - 1.75M+ regional geometries processed for the Hunter Net Developable Area pipeline.
  - 17 high-priority candidate industrial sites indexed across 8 states/territories.
  - 33 sensitive receptors (19 schools via ACARA, 14 hospitals via NHSD) directly in candidate zones audited for 100% ABS land-use ground truth.

### 3. Runtime Benchmark Precision
- **200.6s**: Cold, multi-table batch ETL pipeline execution (uncached ingestion, GDA2020 CRS reproject, `ST_MakeValid`, Iceberg table write).
- **2.4s**: Wherobots Cloud Spatial SQL query execution for complex distributed joins across 1.75M+ regional features.
- **3.2s**: National dataset scan duration across 15.91M geometries using Hilbert space-filling curve partitioning (down from 18.4s).
- **< 1ms**: Client-side What-If sandbox recalculation in browser JavaScript with zero server calls.

### 4. Interactive Report Hosting & WordPress Iframe Embed
- Standalone HTML document (9.2 MB) configured with standard responsive iframe embed markup (`height: 75vh; min-height: 600px; border-radius: 12px`).
- Retained visible attribution banner, disclaimer notes, and "Open in new tab" link.
