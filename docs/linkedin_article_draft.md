# LinkedIn Technical Article Draft

**Title:** Building a Cloud-Native Regional Spatial Siting Engine with Apache Sedona & Wherobots Cloud  
**Author:** Corey (GetBack2Basics / Hunter Spatial Crafter)  
**Target Audience:** GIS Engineers, Spatial Data Engineers, Cloud Architects, Urban Planners, Data Center Developers  

---

## 🚀 Building a Cloud-Native Regional Spatial Siting Engine with Apache Sedona & Wherobots Cloud

Energy transition and digital infrastructure demand rapid, data-driven spatial siting. Whether evaluating former industrial precincts for hyperscale data centers, renewable microgrids, or clean technology hubs, traditional desktop GIS workflows struggle when merging multi-layer environmental, infrastructure, and cadastral constraints at scale.

*This is a private (Get Back to Basics) project to learn where spatial technology is headed. All opinions expressed and data used are public information.*

In our open benchmark project—**Hunter Spatial Crafter**—we set out to answer a key question:  
*How quickly and cost-effectively can we build an end-to-end, automated spatial siting engine that funnels from **National & Regional market benchmarking** down to **Local Precinct micro-siting** using cloud-native spatial technologies?*

Here is how we built it using **Wherobots Cloud**, **Apache Sedona**, **Havasu (Iceberg)**, and **GeoPandas**, along with key spatial engineering insights and our compiled **"Map in a Box"** interactive siting dashboard.

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
* **Spatial Ground-Truth**: Subtraction of 30m riparian, 20m gas pipeline, biodiversity, and TSF hazard overlays reduces viable gross land to **921 hectares**, isolating net contiguous buildable pads: **16.4 ha** (Macquarie), **12.5 ha** (Killingworth), **9.8 ha** (Teralba), and **1.2 ha** (Cockle Creek). *(De-declaring the active TSF dam safety risk unlocks an additional **15.2 hectares** of flat, high-bearing pad space).*

#### Data Scale (1,751,315 Spatial Geometries Ingested):
To perform this multi-tier constraint modeling across regional NSW, our pipeline queries **over 1.75 million vector geometries**:
* **NSW Transport Network (Rail)**: 275,421 features
* **NSW Biodiversity Constraint Overlay**: 262,258 polygons
* **NSW Energy Grid Infrastructure**: 241,573 features
* **NSW Pipeline Corridors**: 197,247 features
* **TfNSW Active Transport Pathways**: 188,576 features
* **NSW Hydrography & Waterways**: 181,501 features
* **ABS Regional Demographics (SA2)**: 181,501 records
* **ABS Census Meshblocks**: 223,238 polygons

---

### 📊 2. Desktop GIS vs. Cloud-Native Sedona Benchmark

Doing multi-layer buffer, overlay, and spatial union operations across 1.75M+ features in traditional desktop GIS (QGIS or ArcGIS Pro) creates severe memory bottlenecks, frequent software crashes, and un-reproducible manual steps.

| Metric / Dimension | Traditional Desktop GIS (QGIS / ArcGIS Pro) | Cloud-Native Spatial (Apache Sedona + Wherobots) |
| :--- | :--- | :--- |
| **Processing Time** | **2 to 3 Days** (Manual layer prep, buffer clipping, manual unioning) | **2.4 Seconds** (Automated Spatial SQL execution on Spark) |
| **Polygon / Feature Capacity** | Chokes or crashes on **1.75M+ features** without manual tiling | **1,751,315 Geometries** queried effortlessly in parallel |
| **Reproducibility** | Low (Ad-hoc GUI clicks, hidden project files, non-scripted steps) | **100% Reproducible** (Version-controlled Python ETL & Spatial SQL) |
| **Compute & Labor Cost** | High engineering labor cost ($1,000s in analyst hours) | **<$24 Total** across dozens of full regional batch job runs |
| **Storage & Metadata** | Fragmented Shapefiles / FileGDBs | Standardized **Havasu (Spatial Iceberg)** cloud tables |

---

### ⚡ 3. The Cloud-Native Architecture & "Map in a Box" Report

We expanded the **Hunter Spatial Crafter** repository into an end-to-end automated framework running on **Wherobots Cloud**:

```
[ NSW SEED / ABS / Lake Mac Open Data (1.75M Geometries) ]
                          │
                          ▼ (Wherobots Spatial Ingest - EPSG:7856)
          [ Apache Sedona + Spatial SQL Transformations ]
                          │
                          ▼ (Havasu / Iceberg Storage)
            [ org_catalog.fgsdb.macquarie_* ]
                          │
                          ▼ (Report Builder Engine)
    [ 📦 "MAP IN A BOX": Standalone Interactive HTML Report ]
```

#### Introducing the "Map in a Box" Report:
Our python builder compiles the full cloud analytics run into a zero-dependency, self-contained **"Map in a Box"** HTML report ([`national_suitability_report.html`](https://github.com/GetBack2Basics/hunter_spatial_crafter/blob/main/runner/national_suitability_report.html)) that can be shared, emailed, or hosted anywhere. Download and open the file in your browser to view the interactive map and dashboard!

Key interactive capabilities embedded directly in the report:
* 🗺️ **Vector Map & Spatial Overlays**: Embedded Leaflet maps featuring real-time GeoJSON layers of local precinct boundaries and net developable pads.
* 🎛️ **What-If Scenario Sandbox**: A live TSF Tailings Dam status toggle—de-declaring the dam hazard dynamically updates buildable pad areas and suitability scores in real-time across the UI.
* ⚡ **Physics & Engineering Models**: Integrates thermodynamic pipe heat loss ($T_{delivery}$ over distance), natural thermal discharge cooling travel distance, and micro-pumped hydro potential (MWh energy capacity & MPa head pressure).
* 📈 **National & Regional Scorecard Leaderboard**: Ranks national transition candidates (Latrobe VIC, Collie WA, Gladstone QLD) against local Hunter precinct sub-sites.

---

### 🛠️ 4. Spatial SQL Snippet: Generating Net Developable Zones

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

### 💰 5. Key Learnings: Performance & Cost Optimization on Wherobots

One of our biggest takeaways from building **Hunter Spatial Crafter** was managing cloud spatial compute costs:

1. **Headless Batch Execution is Exceptionally Cost-Efficient**: Running batch jobs (`WherobotsJob(runtime="tiny")`) cost under **$24 total** across dozens of full regional ingest and analysis runs, executing 1.75M feature queries in **2.4 seconds**. Runtimes automatically shut down the moment execution finishes.
2. **Interactive Session Discipline**: Interactive sessions (notebooks, SQL consoles, MCP server connections) bill continuously by the hour ($1.50+/SU-hour). Configuring strict 5-minute auto-shutdown idle timeouts prevents accidental background runtime charges.
3. **Session Teardown**: Always wrapping Spark/Sedona sessions in `try...finally: spark.stop()` guarantees clean compute release.

---

### 🎯 Results & What's Next

By combining **Apache Sedona** and **Wherobots Cloud**, we reduced multi-scale site evaluation times from **days (in desktop GIS) down to 2.4 seconds**, querying **1,751,315 spatial geometries** and compiling the entire national-to-local analysis into a portable **"Map in a Box"** report.

Check out the interactive report and open-source project repository to explore cloud-native spatial siting for your next infrastructure benchmark!

---

📌 *Project Repository:* [GetBack2Basics / hunter_spatial_crafter](https://github.com/GetBack2Basics/hunter_spatial_crafter)  
🌐 *Interactive Report:* [national_suitability_report.html](https://github.com/GetBack2Basics/hunter_spatial_crafter/blob/main/runner/national_suitability_report.html)  
💬 *What tools are you using for large-scale spatial ETL and infrastructure siting? Let's connect in the comments!*  

#GIS #SpatialData #ApacheSedona #Wherobots #DataEngineering #Geospatial #DataCenter #EnergyTransition #Python #SpatialSQL



