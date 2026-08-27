# LinkedIn Technical Article (Part 1 - Submitted)

**Title:** Building a Cloud-Native Regional Spatial Siting Engine with Apache Sedona & Wherobots Cloud  
**Author:** Corey (GetBack2Basics / Hunter Spatial Crafter)  
**Target Audience:** GIS Engineers, Spatial Data Engineers, Cloud Architects, Urban Planners, Data Center Developers  
**Status:** Submitted / Published  

---

## 🚀 Building a Cloud-Native Regional Spatial Siting Engine with Apache Sedona & Wherobots Cloud

Energy transition and digital infrastructure demand rapid, data-driven spatial siting. Whether evaluating former industrial precincts for hyperscale data centers, renewable microgrids, or clean technology hubs, traditional desktop GIS workflows struggle when merging multi-layer environmental, infrastructure, and cadastral constraints at scale.

*This is a private (Get Back to Basics) project to learn where spatial technology is headed. All opinions expressed and data used are public information.*

In our open benchmark project—**Hunter Spatial Crafter**—we set out to answer a key question:  
*How quickly and cost-effectively can we build an end-to-end, automated spatial siting engine that funnels from **National & Regional market benchmarking** down to **Local Precinct micro-siting** using cloud-native spatial technologies?*

Here is how we built it using **Wherobots Cloud**, **Apache Sedona**, **Havasu (Spatial Iceberg)**, and **GeoParquet**, along with key spatial engineering insights and our compiled **"Map in a Box"** interactive siting dashboard.

---

### 💡 1. The Multi-Scale Siting Challenge (National ➔ Regional ➔ Local)

Rather than evaluating a single isolated property, modern site selection requires a top-down, multi-scale spatial funnel:

```
                  ┌────────────────────────────────────────┐
                  │ 1. NATIONAL SCALE: Market Baselines   │
                  │ (Hunter NSW, Latrobe VIC, Collie WA,  │
                  │  Gladstone QLD)                        │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │ 2. REGIONAL SCALE: Infrastructure      │
                  │ (HV Grid Proximity, SA2 Demographics, │
                  │  Recycled Water Outfalls)              │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │ 3. LOCAL PRECINCT SCALE: Micro-Siting │
                  │ (Riparian 30m, Pipeline 20m, Slope,   │
                  │  TSF Tailings Dam Hazards)             │
                  └────────────────────────────────────────┘
```

#### Detailed Precinct Ground-Truth (Macquarie Transformation Precinct):
Focusing down to the Macquarie Precinct (Killingworth, West Lake, Cockle Creek, Teralba):
* **Proponent Claim**: 100% of the site boundary (**1,160 hectares**) is fully developable.
* **Spatial Reality**: When running rigorous 5-tier overlays (slope $>5\%$, flood inundation, mine subsidence, high-value biodiversity, riparian setbacks, pipeline easements, and active rail corridors), the actual **Net Developable Area (NDA) is ~482 hectares (41.6% of gross area)**.

---

### ⚡ 2. The 5-Tier Spatial Constraint Model

To benchmark sites nationally, our pipeline evaluates 5 spatial constraint tiers:

1. **Elevation & Terrain Slope**: Digital Elevation Models (DEM) filtered via `RS_Slope` to eliminate unbuildable terrain ($>5\%$).
2. **Mine Subsidence & Geotechnical Hazards**: Overlaying legacy mining shafts, grout zones, and historical workings.
3. **Flood Risk & Hydrological Outfalls**: Riparian buffers ($30\text{m}-100\text{m}$) and 1-in-100-year flood extent layers.
4. **Power Grid & Substation Interconnection**: Euclidean and network proximity to $\ge 132\text{kV}$ transmission corridors and terminal substations.
5. **Protected Habitat & Social Buffers**: Biodiversity corridors and sensitive receptor setbacks (schools, hospitals, residential meshblocks).

---

### 🌐 3. Data Ingestion Architecture & Provenance

The pipeline harvests data directly from official, authoritative REST and WFS endpoints:
* **NSW SEED Portal**: Biodiversity Values Map (BVM) and Hydrography.
* **Geoscience Australia & AEMO**: National Electricity Market (NEM) transmission infrastructure.
* **Australian Bureau of Statistics (ABS)**: ASGS 2021 Meshblocks & Urban Centres.
* **Lake Macquarie City Council Open Data**: Precinct Master Plan zoning and cadastral boundaries.

---

### 📊 4. Benchmark: Desktop GIS vs. Cloud Spatial Lakehouse

| Metric | Traditional Desktop GIS | Wherobots Cloud + Sedona |
| :--- | :--- | :--- |
| **Ingestion & Joins** | 2–3 days manual processing | **2.4 seconds (1.75M rows)** |
| **Storage & Metadata** | Fragmented Shapefiles / FileGDBs | Standardized **Havasu (Spatial Iceberg)** cloud tables |
| **Reproducibility** | Manual point-and-click GUI | **100% Version-Controlled Python & Spatial SQL** |
| **Client Delivery** | Heavy GIS desktop installation | **Self-contained "Map in a Box" HTML report** |

---

### 🛠️ 5. Spatial SQL Snippet: Generating Net Developable Zones

With Apache Sedona on Wherobots, combining multi-layer constraint masks into a net developable polygon requires concise Spatial SQL:

```sql
-- Union environmental and infrastructure constraint buffers
WITH combined_constraints AS (
  SELECT ST_Union_Aggr(geometry) AS constraint_geom
  FROM (
    SELECT ST_Buffer(geometry, 30.0) AS geometry FROM org_catalog.fgsdb.macquarie_water_hydrography
    UNION ALL
    SELECT ST_Buffer(geometry, 20.0) AS geometry FROM org_catalog.fgsdb.macquarie_pipeline_corridors
    UNION ALL
    SELECT geometry FROM org_catalog.fgsdb.macquarie_biodiversity_constraints
    UNION ALL
    SELECT geometry FROM org_catalog.fgsdb.macquarie_tsf_risk_zones
  )
)
-- Subtract constraints from precinct boundary to yield buildable zones
SELECT 
  p.precinct_key,
  ST_Difference(p.geometry, c.constraint_geom) AS net_developable_geom,
  ST_Area(ST_Difference(p.geometry, c.constraint_geom)) / 10000.0 AS developable_area_ha
FROM org_catalog.fgsdb.macquarie_precinct_boundary p
CROSS JOIN combined_constraints c;
```

---

### 📦 6. The "Map in a Box" Report & Open Evidence Trail

Our python builder compiles the full cloud analytics run into a zero-dependency, self-contained **"Map in a Box"** HTML report ([`national_suitability_report.html`](https://github.com/GetBack2Basics/hunter_spatial_crafter/blob/main/runner/national_suitability_report.html)) featuring **9 integrated tabs** in the *Benchmarking, Data Provenance & Open Evidence Trail* section:

1. **State Benchmarking**: Statewide candidate score & area averages across NSW, VIC, WA, QLD.
2. **Regional Aggregates**: Regional sub-market performance comparisons.
3. **Data Sources & Volumes**: Direct agency links (SEED NSW, ABS Digital Atlas, TfNSW, Lake Mac Open Data).
4. **Lakehouse Storage & Directory Tree**: Visual S3 directory tree (`metadata/` vs `data/`) and CRS specs.
5. **Table Footprint & Compression**: Complete inventory of feature counts, raw sizes, and GeoParquet sizes.
6. **Whitepapers & Specifications**: Direct links to open standards (Havasu, Iceberg, GeoParquet, Sedona).
7. **Speed Mechanics**: Detailed breakdown of envelope pruning, Hilbert clustering, and vectorized joins.
8. **What-If Sandbox Mechanics**: Explains how the interactive multi-criteria sandbox runs **100% in-browser** with zero server calls, zero network latency, and **$0.00 cloud compute charges** during interactive slider sessions.
9. **Calculations & SQL Trail**: Mathematical equations for thermodynamic pipe heat loss, head pressure, and Spatial SQL snippets.

---

### 💰 7. Key Learnings: Performance & Cost Optimization on Wherobots

One of our biggest takeaways from building **Hunter Spatial Crafter** was managing cloud spatial compute costs:

1. **Headless Batch Execution is Exceptionally Cost-Efficient**: Running batch jobs (`WherobotsJob(runtime="tiny")`) cost under **$24 total** across dozens of full regional ingest and analysis runs, executing 1.75M feature queries in **2.4 seconds**. Runtimes automatically shut down the moment execution finishes.
2. **Interactive Session Discipline**: Interactive sessions (notebooks, SQL consoles, MCP server connections) bill continuously by the hour ($1.50+/SU-hour). Configuring strict 5-minute auto-shutdown idle timeouts prevents accidental background runtime charges.
3. **Session Teardown**: Always wrapping Spark/Sedona sessions in `try...finally: spark.stop()` guarantees clean compute release.

---

### 🎯 Results & What's Next

By combining **Apache Sedona** and **Wherobots Cloud**, we reduced multi-scale site evaluation times from **days (in desktop GIS) down to 2.4 seconds**, querying **1,751,315 spatial geometries** and compiling the entire national-to-local analysis into a portable **"Map in a Box"** report.

Check out the interactive report and open-source project repository to explore cloud-native spatial siting for your next infrastructure benchmark!

---

📌 *Project Repository:* [github.com/getback2basics / hunter_spatial_crafter](https://github.com/GetBack2Basics/hunter_spatial_crafter)  
🌐 *Interactive Report:* [national_suitability_report.html](https://github.com/GetBack2Basics/hunter_spatial_crafter/blob/main/runner/national_suitability_report.html)  
💬 *What tools are you using for large-scale spatial ETL and infrastructure siting? Let's connect in the comments!*  

©® 2026 GetBack2Basics - [github.com/getback2basics](https://github.com/GetBack2Basics) | All material is for information only and is the authors private opinion

#GIS #SpatialData #ApacheSedona #Wherobots #DataEngineering #Geospatial #DataCenter #EnergyTransition #Python #SpatialSQL #Iceberg #GeoParquet
