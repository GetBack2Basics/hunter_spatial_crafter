# Next Steps: Sensitive Receptor Spatial Scoring & GeoLibre AI Integration Architecture

## Executive Summary

This specification outlines the next development phase for the **National Data Center Siting Suitability Model** (`hunter_spatial_crafter`). It details two core enhancements:
1. Incorporating **social & community sensitive receptors** (schools, child care centers, hospitals) and **residential proximity** into the Multi-Criteria Decision Analysis (MCDA) ranking engine.
2. Connecting the spatial outputs to an open-source **GeoLibre** ([opengeos/GeoLibre](https://github.com/opengeos/GeoLibre)) platform hosted on **Google Cloud Platform (GCP)** to enable free public AI-driven spatial analysis ("Ask AI").

---

## 1. Social & Sensitive Receptor Spatial Scoring Framework

### A. Core Sensitive Receptors & Land Use Categories

| Receptor Category | Target Facilities / Datasets | Primary Exclusion/Buffer Rationale |
| :--- | :--- | :--- |
| **Education & Child Care** | Schools, Preschools, Early Childhood Centers, Universities | Acoustic protection, EMF safety compliance, traffic safety |
| **Healthcare Facilities** | Public/Private Hospitals, Emergency Care, Aged Care Homes | Sensitive equipment interference, 24/7 low-frequency noise limits |
| **Residential Areas** | ABS Meshblock (Residential), SA1 High-Density Residential Zones | Community amenity, acoustic setback under EPA guidelines, heat island mitigation |
| **Residential Workforce** | ABS Urban Center / Locality Boundaries | Workforce availability balance (proximity needed for staff commute) |

### B. Mathematical Multi-Criteria Spatial Scoring Formula

To prevent land-use conflicts while ensuring operational viability, sensitive receptor scoring uses a continuous **Sigmoidal Buffer Decay Model**:

$$S_{\text{sensitive}}(d) = \frac{1}{1 + e^{-k (d - d_0)}}$$

Where:
- $d$: Minimum Euclidean or network distance from site boundary to nearest sensitive receptor (meters).
- $d_0$: Critical threshold distance (e.g., $500\text{m}$ for acoustic compliance).
- $k$: Steepness factor ($k = 0.01\text{m}^{-1}$).

#### Integrated Receptor Score Matrix:

```
Distance to Sensitive Receptor (d)    Score (S_sensitive)     Constraint Classification
-----------------------------------------------------------------------------------
d < 300m                              0.00                    HARD EXCLUSION (Unsuitable)
300m <= d < 500m                      0.20 - 0.50             HIGH PENALTY (Requires Acoustic Wall)
500m <= d < 1,500m                    0.80 - 1.00             OPTIMAL BUFFER (Ideal Siting)
1,500m <= d < 5,000m                  1.00                    OPTIMAL WORKFORCE DISTANCE
d >= 5,000m                           0.70 (Linear Decay)     DISTANT (Workforce Commute Penalty)
```

---

## 2. GeoLibre AI Spatial Integration on Google Cloud Platform (GCP)

### A. High-Level GCP Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                GOOGLE CLOUD PLATFORM (GCP)                              │
│                                                                                         │
│   ┌────────────────────────────────┐                 ┌──────────────────────────────┐   │
│   │ Google Cloud Storage (GCS)     │                 │ GCP Cloud Run (Serverless)   │   │
│   │                                │                 │                              │   │
│   │ • GeoParquet Siting Datasets   │◄────────────────┤ • FastAPI Spatial AI Proxy   │   │
│   │ • PMTiles Basemaps & Vector    │ (Direct HTTP)   │ • Scale-to-Zero Container    │   │
│   │ • Static GeoLibre Web App UI   │                 │ • Gemini & OpenRouter Client │   │
│   └───────────────▲────────────────┘                 └──────────────▲───────────────┘   │
└───────────────────┼─────────────────────────────────────────────────┼───────────────────┘
                    │                                                 │
                    │ static assets & parquet                         │ NL Prompts & SQL
                    ▼                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                END-USER WEB BROWSER                                     │
│                                                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ GeoLibre Web Application (Hosted for Free)                                      │   │
│   │                                                                                 │   │
│   │  ┌─────────────────────────────┐           ┌─────────────────────────────────┐  │   │
│   │  │ Client-Side DuckDB-WASM     │           │ Conversational AI Assistant     │  │   │
│   │  │ (Zero-Cost In-Browser SQL)  │           │ ("Ask AI" Prompt Drawer)        │  │   │
│   │  └─────────────────────────────┘           └─────────────────────────────────┘  │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### B. Shared Cloud Data Storage Architecture (Wherobots & GeoLibre Integration)

Rather than copying data onto local web server disk storage or maintaining separate file servers, GeoLibre and Wherobots share the exact same cloud-native dataset repository:

1. **Zero-Duplication Central Data Layer**:
   - Wherobots Cloud (Apache Sedona Spark) outputs suitability modeling layers directly into a central Google Cloud Storage (GCS) / S3 bucket as **GeoParquet** and **PMTiles**.
   - GeoLibre queries these exact same files in GCS without dataset conversion or server data duplication.
2. **HTTP Range-Request Querying**:
   - GeoLibre’s in-browser DuckDB-WASM engine fetches only required byte ranges and spatial row groups via HTTP range requests (`read_parquet('https://storage.googleapis.com/.../datacenter_candidates.parquet')`).
   - Eliminates downloading full datasets to the client or maintaining expensive local web server NVMe storage drives.

### C. Free Public Conversational AI Workflow

1. **User Ask**: The user types a natural language question in GeoLibre:  
   *"Show me all candidate sites in VIC larger than 10 hectares that are within 2km of high-voltage transmission lines and at least 1km away from any school or hospital."*
2. **AI Translation**: GeoLibre sends the user prompt + active dataset schemas to the FastAPI gateway on GCP Cloud Run. Cloud Run queries Gemini LLM to generate DuckDB Spatial SQL:
   ```sql
   SELECT site_name, area_ha, power_dist_km, sensitive_dist_km, suitability_score
   FROM read_parquet('https://storage.googleapis.com/hunter-spatial-data/datacenter_candidates.parquet')
   WHERE state = 'VIC' 
     AND area_ha > 10.0 
     AND power_dist_km <= 2.0 
     AND school_dist_km >= 1.0 
     AND hospital_dist_km >= 1.0;
   ```
3. **In-Browser Compute**: The SQL query is executed directly inside the user's browser using DuckDB-WASM, fetching only required byte ranges from GCS using HTTP range requests.
4. **Instant Visualisation**: GeoLibre renders matching candidates on an interactive Mapbox/Leaflet map with dynamic stats.
