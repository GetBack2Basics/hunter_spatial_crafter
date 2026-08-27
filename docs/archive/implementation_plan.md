# Implementation Plan: Social & Sensitive Receptor Spatial Scoring Framework (Part 1)

This plan details the implementation of **Part 1: Social & Sensitive Receptor Spatial Scoring Framework** for the National Data Center Siting Suitability Model (`hunter_spatial_crafter`), as specified in [`docs/next_steps_and_geolibre_tab.md`](file:///c:/Projects/hunter_spatial_crafter/docs/next_steps_and_geolibre_tab.md).

All spatial datasets will be harvested from **live official national and state/territory WFS/REST services and authoritative open datasets (including OpenStreetMap Australia for harmonized national POIs)**—**no simulated datasets will be used**. The ingestion engine will also incorporate **national elevation models (ELVIS DEM)** for slope filtering and **cadastral layers (Lot/Plan & Address)** to enable granular site querying.

---

## User Review Required

> [!IMPORTANT]
> **National Coverage & Cadastre Querying**:
> - **Full National Footprint**: Ingests all 8 Australian States & Territories (**NSW, QLD, VIC, WA, SA, TAS, ACT, NT**).
> - **National Seamless POIs + State WFS**: Uses National Registers (ACARA, NHSD, Geoscape G-NAF) and OSM Australia extracts, cross-checked with State WFS/REST portals and ABS 2021 Meshblocks.
> - **Cadastre & Address Lookups**: Includes National/State Cadastre to allow filtering and querying by `Lot/Plan` (e.g. `Lot 1 DP123456`, `Lot 12 RP89012`) and physical street addresses.
> - **Terrain & Elevation**: Incorporates Geoscience Australia ELVIS Digital Elevation Models (DEM) to enforce $< 5\%$ slope suitability criteria.

---

## Data Sources & Provenance Architecture

Data sources are structured with a strict separation between **National Authoritative Layers** (seamless baseline) and **State/Territory Live WFS & REST Services** (local enrichment and micro-siting).

### 1. National Authoritative Baseline Datasets & Services (All States & Territories)

| Category | Dataset / Service Name | Source Agency / Portal | Live Endpoint / Format | Geometry Type | Data Currency / Cadence | Spatial Operations & Processing Lineage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cadastre & Lot/Plan** | Geoscape National Cadastre & G-NAF | [Geoscape / Data.gov.au](https://data.gov.au/data/dataset/geocoded-national-address-file-g-naf) | WFS / Geopackage / REST | Polygon / Point | 2025–2026 (Quarterly) | Schema normalization for `lot_plan`, `street_address`, `locality`, `state`. Cleaned for multipart polygons. |
| **Elevation & Terrain** | National 1-sec SRTM & 5m/1m LiDAR DEM | [Geoscience Australia (ELVIS)](https://elevation.fsdf.org.au/) | WCS / GeoTIFF / REST API | 32-bit Float Raster | Authoritative National DEM | Sedona `RS_Slope` computation. Flags parcels with slope grade $>5\%$. |
| **Land Use & Meshblocks** | ASGS 2021 Meshblocks | [Australian Bureau of Statistics (ABS)](https://geo.abs.gov.au/arcgis/rest/services/ASGS2021) | ArcGIS REST FeatureServer | Polygon | 2021 Census (Official) | Filtered for `mb_cat21` (`Residential`, `Education`, `Commercial`, `Industrial`). Used as POI ground-truth cross-check. |
| **Workforce & Urban Centers** | ASGS 2021 Urban Centres and Localities (UCL) | [Australian Bureau of Statistics (ABS)](https://geo.abs.gov.au/arcgis/rest/services/ASGS2021) | ArcGIS REST FeatureServer | Polygon | 2021 Census (Official) | Dissolved metropolitan & regional urban boundaries. Used for $1.5\text{km}-15\text{km}$ workforce decay modeling. |
| **Education POIs** | National Schools Dataset | [ACARA / National Map](https://data.gov.au/dataset/ds-dga-19597793-be34-406a-939e-d1b4a5598687) | WFS / GeoJSON / CSV REST | Point | 2024–2025 (Annual) | Normalized `school_name`, `education_type`, reprojected to `EPSG:7844` and metric `EPSG:3112`. |
| **Healthcare POIs** | National Health Services Directory (NHSD) | [Healthdirect Australia](https://about.healthdirect.gov.au/national-health-services-directory) / [National Map](https://nationalmap.gov.au) | WFS / REST GeoJSON | Point | 2025 (Monthly API) | Filtered for inpatient hospitals, emergency departments, and residential aged care facilities. |
| **Harmonized National POIs** | OpenStreetMap (OSM) Australia Extract | [OpenStreetMap Foundation / Geofabrik](https://download.geofabrik.de/australia-oceania/australia.html) | Overpass API / Parquet | Point / Polygon | Live Rolling | Filtered on `amenity IN ('school', 'kindergarten', 'hospital', 'clinic', 'university')`. Validated against ABS. |
| **Power Infrastructure** | National Transmission Grid ($\ge 132\text{kV}$) | [Geoscience Australia / AEMO](https://nationalmap.gov.au) | ArcGIS REST / GeoJSON | Line / Point | 2024–2025 | Filtered for transmission voltages $\ge 132\text{kV}$ and terminal substations. |
| **Water Infrastructure** | National Recycled Water & Wastewater Plants | [Bureau of Meteorology (BoM) / GA](https://www.bom.gov.au/water) | WFS / ArcGIS REST | Point / Polygon | 2024 | Industrial water cooling availability flags. |

---

### 2. State & Territory Live WFS / REST Services

| Jurisdiction | Category | Source Agency / Portal | Live Endpoint / Service Details | Data Currency |
| :--- | :--- | :--- | :--- | :--- |
| **NSW** | Cadastre, Schools, Health, Rail, Energy | [NSW Spatial Services](https://portal.spatial.nsw.gov.au/server/rest/services) & [NSW SEED](https://www.seed.nsw.gov.au) | `https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Cadastre/MapServer`<br>`https://www.seed.nsw.gov.au/arcgis/rest/services` | 2025–2026 Live |
| **QLD** | Cadastre (DCDB), Health, Education | [data.qld.gov.au](https://data.qld.gov.au) & [Queensland Spatial Information (QSpatial)](https://qspatial.information.qld.gov.au) | `https://spatial-gis.information.qld.gov.au/arcgis/rest/services/PlanningCadastre/LandParcelPropertyFramework/MapServer` | 2025–2026 Live |
| **VIC** | Vicmap Property, Features POI | [Data.vic.gov.au](https://discover.data.vic.gov.au) / Vicmap | `https://services.land.vic.gov.au/arcgis/rest/services/` | 2025 Quarterly |
| **WA** | Cadastre & Education/Health POIs | [Data.wa.gov.au](https://data.wa.gov.au) / Landgate SLIP | `https://slip.landgate.wa.gov.au/arcgis/rest/services/` | 2025 Live |
| **ACT (Canberra)** | Cadastre & Community Facilities | [ACTmapi](https://actmapi-actgov.opendata.arcgis.com/) / ACT Open Data | `https://services1.arcgis.com/E5n4f19nThNVBumn/arcgis/rest/services/` | 2025 Live |
| **NT** | Cadastre & Community POIs | [NT Atlas & Spatial Data Directory](https://data.nt.gov.au/) / Data NT | `https://ntg-spatial.nt.gov.au/arcgis/rest/services/` | 2024–2025 Live |
| **SA** | LocationSA Cadastre & Infrastructure | [Data.sa.gov.au](https://data.sa.gov.au) / LocationSA | `https://location.sa.gov.au/arcgis/rest/services/` | 2025 Live |
| **TAS** | LISTas Cadastre & Infrastructure | [thelist.tas.gov.au](https://www.thelist.tas.gov.au) / Land Information System Tasmania | `https://services.thelist.tas.gov.au/arcgis/rest/services/` | 2025 Live |

---

## Proposed Changes

### 1. Ingestion, Meshing & Data Verification Engine

#### [NEW] [`src/Ingestion/data_injest.py`](file:///c:/Projects/hunter_spatial_crafter/src/Ingestion/data_injest.py)
- Connects to national repositories and live state WFS/REST endpoints.
- Meshes datasets into unified spatial Havasu tables in Sedona Spark:
  - `org_catalog.fgsdb.national_cadastre`: Standardized lot/plan (`lot_plan`, `cadastre_id`), address, and geometry.
  - `org_catalog.fgsdb.national_education_receptors`: Schools, Preschools, Universities (ACARA + OSM + State POIs).
  - `org_catalog.fgsdb.national_healthcare_receptors`: Hospitals, Emergency Care, Aged Care (NHSD + OSM + State POIs).
  - `org_catalog.fgsdb.national_residential_meshblocks`: ABS 2021 Residential Meshblocks.
  - `org_catalog.fgsdb.national_urban_centres`: ABS 2021 Urban Centres & Localities.
  - `org_catalog.fgsdb.national_elevation_slope`: ELVIS DEM slope analysis raster layer.
- **QA & Ground-Truth Cross-Check**:
  - Validates POI points against ABS Meshblock classifications (calculates % of education/health points within congruent land-use zones).
  - Tracks **Data Currency** (publication and API fetch timestamps).
  - Tracks **Transformation Lineage** (records whether layer is *Raw Unchanged* or underwent *CRS Reprojection*, *Deduplication*, *Geometry Repair*, or *Attribute Normalization*).
  - Exports audit metrics to `docs/data_verification_audit.json`.

---

### 2. Multi-Criteria Analysis & Scoring Engine

#### [MODIFY] [`src/Analysis/datacenter_suitability.py`](file:///c:/Projects/hunter_spatial_crafter/src/Analysis/datacenter_suitability.py)
- Integrates the meshed sensitive receptor layers and lot/plan identifiers.
- Implements the continuous Sigmoidal Buffer Decay formula:
  $$S_{\text{sensitive}}(d) = \frac{1}{1 + e^{-k (d - d_0)}}$$
  where $d_0 = 500\text{m}$ and steepness $k = 0.01\text{m}^{-1}$.
- Applies zoning rules:
  - $d < 300\text{m} \rightarrow 0.00$ (`HARD EXCLUSION` - acoustic & safety barrier).
  - $300\text{m} \le d < 500\text{m} \rightarrow [0.20, 0.50]$ (`HIGH PENALTY` - acoustic wall required).
  - $500\text{m} \le d < 1,500\text{m} \rightarrow [0.80, 1.00]$ (`OPTIMAL BUFFER`).
  - $1,500\text{m} \le d < 5,000\text{m} \rightarrow 1.00$ (`OPTIMAL WORKFORCE DISTANCE`).
  - $d \ge 5,000\text{m} \rightarrow$ Linear decay to $0.70$ at $15,000\text{m}$ (`WORKFORCE COMMUTE PENALTY`).
- Integrates slope grade thresholding from DEM ($>5\%$ slope excluded).

#### [MODIFY] [`src/Analysis/national_suitability_analysis.py`](file:///c:/Projects/hunter_spatial_crafter/src/Analysis/national_suitability_analysis.py)
- Replaces mock views with distributed Sedona Spark queries against the unified Havasu tables across all states and territories (NSW, QLD, VIC, WA, ACT, NT, SA, TAS).
- Computes minimum Euclidean metric distance $d$ to nearest sensitive receptor.
- Evaluates composite MCDA score:
  $$\text{Suitability} = 0.40 \cdot S_{\text{power}} + 0.25 \cdot S_{\text{sensitive}} + 0.20 \cdot S_{\text{water}} + 0.15 \cdot S_{\text{size}}$$
- Persists candidates with `lot_plan`, `street_address`, `slope_pct`, `dist_to_sensitive_km`, and `suitability_score` to `org_catalog.fgsdb.all_national_candidates`.

---

### 3. Documentation & Reference Calculations

#### [MODIFY] [`docs/spatial_calculations_reference.json`](file:///c:/Projects/hunter_spatial_crafter/docs/spatial_calculations_reference.json)
- Documents `sigmoidal_sensitive_receptor_decay`, `dem_slope_filtering`, and `lotplan_cadastral_querying` with variable definitions, formulas, EPA environmental noise policies, and Australian Standard AS 1055 citations.

---

### 4. Technical Verification Report & Dashboard

#### [NEW] [`runner/build_data_verification_report.py`](file:///c:/Projects/hunter_spatial_crafter/runner/build_data_verification_report.py)
- Generates [`runner/data_verification_technical_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/data_verification_technical_report.html):
  - Live data currency timestamps across all National & State/Territory endpoints (NSW, QLD, VIC, WA, ACT, NT, SA, TAS).
  - Transformation Lineage audit (Raw Unchanged vs. Reprojected / Cleaned).
  - Cross-validation results (% POI alignment with ABS Meshblocks).
  - Raster DEM elevation & slope metadata summary.

#### [MODIFY] [`runner/build_suitability_report.py`](file:///c:/Projects/hunter_spatial_crafter/runner/build_suitability_report.py)
- Updates report dashboard:
  - Adds a **Lot/Plan & Address Search Bar** to query candidate parcels by Lot/Plan or address.
  - Adds interactive Leaflet layer toggles for Sensitive Receptor Buffers (300m exclusion, 500m acoustic setback) and Elevation Contours/Slope.
  - Adds an interactive Chart.js Sigmoidal Buffer Decay curve with formula callout.
  - Links to the Data Verification Technical Report.

---

## Verification Plan

### Automated Tests & Pipeline Execution
1. Run `python src/Ingestion/data_injest.py` to ingest national & state endpoints and produce `docs/data_verification_audit.json`.
2. Run `python runner/build_data_verification_report.py` to build `runner/data_verification_technical_report.html`.
3. Run `python src/Analysis/datacenter_suitability.py` and `python src/Analysis/national_suitability_analysis.py` to verify national multi-state MCDA scoring.
4. Run `python runner/build_suitability_report.py` to produce `runner/national_suitability_report.html`.

### Manual & Report Verification
- Inspect `runner/data_verification_technical_report.html`: verify data currency, raw vs. cleaned lineage, and cross-validation stats across all 8 jurisdictions.
- Inspect `runner/national_suitability_report.html`: test Lot/Plan & Address search, verify hard exclusions ($<300\text{m}$), and verify the sigmoidal buffer decay curve.
