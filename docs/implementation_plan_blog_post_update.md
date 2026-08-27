# Implementation Plan: Update & Fact-Check Wherobots Guest Blog Post

Review and update the Wherobots guest blog post at [`docs/wherobots_ai_data_center_suitability_blog.html`](file:///c:/Projects/hunter_spatial_crafter/docs/wherobots_ai_data_center_suitability_blog.html) to incorporate Ben Pruden's structural enhancements from the Notion draft, resolve runtime and metric discrepancies, explicitly label simulated baselines, clarify the **GeoLibre** (not MapLibre) cloud architecture, and align all statistics with the latest project analysis.

---

## User Review Required

> [!IMPORTANT]
> **Runtime Discrepancy Reconciliation**:
> We will resolve Ben's primary blocker ("conflicting runtime numbers: 200.6s vs 2.4s vs 1.2s") by establishing precise technical definitions:
> 1. **2.4 Seconds**: Wherobots Cloud **Spatial SQL query execution** over 1.75M+ features (Havasu metadata envelope pruning, Hilbert clustering, vectorized Apache Sedona joins). This is the reproducible benchmark query.
> 2. **200.6 Seconds**: End-to-end **batch ETL pipeline duration** (uncached multi-table ingestion, GDA2020 CRS transformation, `ST_MakeValid` geometry repair, and writing 8 Havasu tables covering 4.92M spatial join combinations).
> 3. **< 1 Millisecond**: Client-side **MCDA sandbox re-scoring** executed in the browser via JavaScript.
> 4. **18.4s ➔ 3.2s**: Query acceleration on the national 15.91M geometry dataset via Hilbert space-filling curve partitioning.

> [!NOTE]
> **GeoLibre & Google Cloud Architecture Clarification**:
> - **GeoLibre (not MapLibre)**: Reference [`opengeos/GeoLibre`](https://github.com/opengeos/GeoLibre), utilizing in-browser **DuckDB-WASM** to query cloud-native **GeoParquet** and **PMTiles** via HTTP range requests.
> - **Cloud Architecture Rationale**: Data is stored centrally in cloud object storage (S3/GCS); the client/web tier and Gemini API gateway run serverless on Google Cloud (leveraging George's developer stack and high free tier); Wherobots Cloud handles the heavy distributed spatial SQL computations.

---

## Key Numbers & Statistics Alignment Table

| Dimension / Metric | Verified Number | Context & Definition |
| :--- | :--- | :--- |
| **Spatial Tables Ingested** | **8 Cloud Spatial Tables** | Cataloged under `org_catalog.fgsdb.*` in AWS `us-west-2` |
| **Ingested Geometries** | **1,751,315 Geometries** | Full NSW regional layer stack (Rail, Grid, Pipelines, Hydro, Meshblocks, Biodiversity, Demographics) |
| **Spatial Join Combination Space** | **4,920,000 Geometries** | Cross-join & spatial intersection evaluation space |
| **National Pipeline Total** | **15.91 Million Geometries** | Multi-state national authoritative dataset pipeline |
| **Raw Equivalent Footprint** | **~2.9 GB** | Uncompressed GeoJSON / Shapefile / WFS equivalent |
| **Optimized Footprint** | **~430.7 MB** | Compressed GeoParquet files inside Havasu tables |
| **Storage Reduction** | **85.2% Footprint Reduction** | Enabled by columnar Parquet encoding & spatial indexing |
| **Reproducible Spatial SQL Query** | **2.4 Seconds** | Distributed spatial join & net developable overlay execution |
| **Full Batch ETL Ingestion Run** | **200.6 Seconds** | Cold multi-layer ingestion, validation, and table creation |
| **Interactive Sandbox Recalibration** | **< 1 Millisecond** | In-browser slider weight updates & leaderboard re-sorting |
| **Macquarie Gross Claim** | **1,160 ha** (100% Proponent Envelope) | Proponent masterplan total site area claim |
| **Ground-Truth Net Developable Area** | **44.5 ha** | Deducting 20.5 ha for 30m riparian, 20m pipelines, >5% slope, TSF |
| **TSF Dam Hazard Unlock** | **+15.2 ha** | Contiguous flat high-bearing pad space unlocked if de-declared |
| **Topological Winding Factor** | **1.32x** | Real network terrain distance vs straight-line Euclidean distance |
| **Regional Baselines Status** | **Simulated Regional Baselines** | Explicitly labeled for Latrobe Valley (VIC), Collie (WA), Gladstone (QLD) |

---

## Proposed Changes to `docs/wherobots_ai_data_center_suitability_blog.html`

### 1. Structure & Layout Overhaul (Adopting Ben's Notion Redesign)
- **Interactive Report Lead-In**: Place the Siting Explorer app prompt and embed link (`https://national-suitability-report.vercel.app`) right after the intro paragraph so readers can immediately explore the interactive sandbox.
- **Exposing High-Value Technical Content**:
  - Insert actual **Spatial SQL snippets**:
    - Net developable area mask (`ST_Difference` + `ST_Union_Aggr` over riparian, pipeline, biodiversity, and TSF buffers).
    - Proximity joins (`ST_Distance` + `ST_Transform` to 132kV+ transmission substations and wastewater outfalls).
  - Insert the **Scoring Formulas & Sigmoidal Decay Equations**:
    - Continuous sigmoidal acoustic buffer penalty: $S_{\text{sensitive}}(d) = \frac{1}{1 + e^{-k(d - d_0)}}$ ($d_0 = 500\text{m}$, $k = 0.01\text{m}^{-1}$).
    - Linear wastewater decay ($\le 1\text{km}$ to $\ge 10\text{km}$) and parcel thresholding.
  - Insert the **4-Part Query Speed Mechanics**:
    1. Zero-Scan Metadata Envelope Pruning (Havasu 2D bounding boxes in Iceberg AVRO manifests).
    2. Hilbert Curve Spatial Clustering (geographically adjacent row groups).
    3. Vectorized Memory Execution (Apache Sedona operating on columnar WKB buffers).
    4. Parallel Distributed Spatial Joins (R-tree / Quad-tree partitioning converting $O(N \times M)$ to $O(N \log M)$).

### 2. Fact-Checking & Blocker Resolutions
- **Resolve Runtime Numbers**:
  - Replace the ambiguous "4.92 million geometries in 200.6 seconds" phrasing with clear separation: **2.4s Spatial SQL query execution** vs. **200.6s full cold batch ETL ingestion** vs. **<1ms in-browser sandbox recalculation**.
- **Explicit "Simulated" Baseline Labeling**:
  - Update all references to Latrobe Valley, Collie, and Gladstone to explicitly read **"simulated regional baselines"** (or modeled reference baselines).
- **Correct Technical Names & Ecosystem Clarifications**:
  - Replace any generic "MapLibre" references with **GeoLibre** (`opengeos/GeoLibre`).
  - Clarify the role of Google Cloud (Gemini API serverless host, Antigravity AI pair programming) and Wherobots (cloud spatial compute & Apache Sedona engine) with shared zero-duplication cloud storage (S3/GCS GeoParquet & PMTiles).
- **Future Roadmap Scoping**:
  - Clearly mark the sensitive receptor expansion, National Cabinet energy/water policy tiers, and GeoLibre integration as **Author's Future Roadmap / Next Steps**, not current shipped Wherobots product features.
- **Repository, Asset & Author Links**:
  - Ensure links point to `national-suitability-report.vercel.app`, GitHub repos (`GetBack2Basics/hunter_spatial_crafter`, `GetBack2Basics/Spatial_Report_Crafter`), and LinkedIn.
  - Reference local figures (`images/figure1.png`, `images/figure2.png`, `images/figure3.png`).

---

## Verification Plan

### Automated & Consistency Validation
- Validate HTML structure, markup validity, and responsive styles for `docs/wherobots_ai_data_center_suitability_blog.html`.
- Cross-check all numbers in the HTML against [`docs/walkthrough.md`](file:///c:/Projects/hunter_spatial_crafter/docs/walkthrough.md), [`docs/linkedin_article_draft.md`](file:///c:/Projects/hunter_spatial_crafter/docs/linkedin_article_draft.md), and [`runner/national_suitability_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html).

### Review Artifact
- Confirm all changes are ready for Ben Pruden to copy directly into WordPress/Notion.
