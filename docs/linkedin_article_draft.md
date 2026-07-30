# LinkedIn Technical Article Draft

**Title:** Building a Cloud-Native Regional Spatial Siting Engine with Apache Sedona & Wherobots Cloud  
**Author:** Corey (GetBack2Basics / Hunter Spatial Crafter)  
**Target Audience:** GIS Engineers, Spatial Data Engineers, Cloud Architects, Urban Planners, Data Center Developers  

---

## 🚀 Building a Cloud-Native Regional Spatial Siting Engine with Apache Sedona & Wherobots Cloud

Energy transition and digital infrastructure demand rapid, data-driven spatial siting. Whether evaluating former industrial precincts for hyperscale data centers, renewable microgrids, or clean technology hubs, traditional desktop GIS desktop workflows struggle when merging multi-layer environmental, infrastructure, and cadastral constraints at scale.

In our open benchmark project—**Hunter Spatial Crafter**—we set out to answer a key question:  
*How quickly and cost-effectively can we build an end-to-end, automated spatial siting engine for regional NSW (Macquarie Coal Complex Transformation Precinct) using cloud-native spatial technologies?*

Here is how we built it using **Wherobots Cloud**, **Apache Sedona**, **Havasu (Iceberg)**, and **GeoPandas**, along with key spatial engineering insights and cost-optimization learnings.

---

### 💡 1. The Challenge: Multi-Constraint Siting Analysis

The Macquarie Precinct (covering Killingworth, West Lake, Cockle Creek, and Teralba) presents a classic complex spatial siting scenario:

1. **Infrastructure Proximity**: High-voltage electrical transmission lines, freight rail corridors, and major arterial roads.
2. **Environmental & Safety Constraints**: Riparian buffer zones (30m), pipeline safety corridors (20m), high biodiversity conservation areas, and mine tailings dam (TSF) inundation zones.
3. **Net Developable Area Calculations**: Subtracting cumulative constraint masks from sub-precinct boundaries to isolate true buildable envelopes.

Doing this manually across gigabytes of ABS Meshblocks, NSW SEED biodiversity layers, and council open datasets in desktop GIS is tedious and non-reproducible.

---

### ⚡ 2. The Cloud-Native Architecture

We designed a two-stage spatial pipeline running on **Wherobots Cloud**:

```
[ NSW SEED / ABS / Lake Mac Open Data ]
                  │
                  ▼ (Wherobots Spatial Ingest - EPSG:7856)
  [ Apache Sedona + Spatial SQL Transformations ]
                  │
                  ▼ (Havasu / Iceberg Storage)
    [ org_catalog.fgsdb.macquarie_* ]
                  │
                  ▼ (Suitability Scoring & Rendering)
 [ Interactive Siting Dashboard & HTML Reports ]
```

#### Key Technical Highlights:
* **Metric-Safe Coordinate System**: All spatial calculations (buffers, areas, distances) are reprojected from WGS84 (`EPSG:4326`) to projected MGA Zone 56 (`EPSG:7856`) using Sedona’s `ST_Transform()`.
* **Spatial Iceberg Tables**: Standardized datasets are stored in Wherobots Havasu spatial tables (`org_catalog.fgsdb.macquarie_*`), allowing column projection pushdowns and fast spatial indexing.
* **Automated Batch Execution**: Pipelines execute via `WherobotsJob` Python scripts, decoupling compute execution from local machine limits.

---

### 🛠️ 3. Spatial SQL Snippet: Generating Net Developable Zones

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

### 💰 4. Key Learnings: Performance & Cost Optimization on Wherobots

One of our biggest takeaways from building **Hunter Spatial Crafter** was managing cloud spatial compute costs:

1. **Headless Batch Execution is Exceptionally Cost-Efficient**: Running batch jobs (`WherobotsJob(runtime="tiny")`) cost under **$24 total** across dozens of full regional ingest and analysis runs. Runtimes automatically shut down the moment execution finishes.
2. **Interactive Session Discipline**: Interactive sessions (notebooks, SQL consoles, MCP server connections) bill continuously by the hour ($1.50+/SU-hour). Configuring strict 5-minute auto-shutdown idle timeouts prevents accidental background runtime charges.
3. **Session Teardown**: Always wrapping Spark/Sedona sessions in `try...finally: spark.stop()` guarantees clean compute release.

---

### 🎯 Results & What's Next

The automated pipeline outputs high-resolution suitability rankings, metric site evaluations (power proximity, contiguous site area), and interactive HTML dashboards for stakeholder reviews.

By combining **Apache Sedona** and **Wherobots Cloud**, we reduced precinct site evaluation times from days to seconds while establishing a fully reproducible spatial ETL template for future infrastructure planning across Australia.

---

📌 *Project Repository:* [`GetBack2Basics / hunter_spatial_crafter`](file:///c:/Projects/hunter_spatial_crafter)  
💬 *What tools are you using for large-scale spatial ETL and infrastructure siting? Let's connect in the comments!*  

#GIS #SpatialData #ApacheSedona #Wherobots #DataEngineering #Geospatial #DataCenter #EnergyTransition #Python #SpatialSQL
