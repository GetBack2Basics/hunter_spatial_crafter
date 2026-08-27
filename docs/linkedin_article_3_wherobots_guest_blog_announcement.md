# LinkedIn Article Draft 3: Honored to Contribute a Technical Guest Post for Wherobots

**Target Platform:** LinkedIn Post & Article  
**Author:** George Chandeep Corea  
**Focus:** Announcement & Technical Reflection on Authoring the Wherobots Official Guest Post  
**Live Project:** [AuraSiting Crafter (hunter_spatial_crafter)](https://github.com/GetBack2Basics/hunter_spatial_crafter) | [Interactive National Report](https://national-suitability-report.vercel.app)  

---

### Headline
**Honored to share our cloud spatial engineering journey on the official Wherobots technical blog: Scaling AI Data Center Siting from a Local NSW Precinct to 15.91 Million National Geometries**

---

### Post Body

I am truly honored and grateful to have been invited by **Wherobots** to write a technical guest post sharing the architectural journey behind **AuraSiting Crafter**.

What began as my personal curiosity to test cloud spatial tools against a local industrial proposal in New South Wales (the Lake Macquarie / Hunter coal transition precinct) quickly evolved into a nationwide spatial engine spanning **17 candidate brownfield hubs across all 8 Australian States and Territories** (evaluating 4 detailed micro-sited sites in NSW alongside 13 simulated regional reference baselines).

---

### 🌐 Answering the National AI Infrastructure Challenge with Spatial Evidence

Australia is currently engaged in a vital national discourse. Following recent Prime Ministerial statements, National Cabinet meetings, and regulatory debates, the core question is clear:

> *How do we scale energy-hungry AI data centers and hyperscale infrastructure without overloading regional electricity grids, draining precious drinking water catchments, or imposing noise burdens on communities?*

The answer lies in **auditable spatial evidence**. Rather than evaluating sites through speculative developer marketing or static spreadsheets, we built an engine that directly interrogates the ground truth across **16 authoritative national and state portals**.

---

### ⚡ 4 Technical Takeaways from the Wherobots Guest Post

In the blog post, I dive deep into how Apache Sedona and Wherobots Cloud transformed an engineering workflow that typically takes 2–3 days on desktop GIS into an automated cloud pipeline running in seconds:

1. **Massive Cloud Spatial Scale (15.91M Features):**
   Indexing 15.4M Geoscape cadastre parcels, 368k ABS meshblocks, 275k rail corridors, and 241k power transmission vectors across Australia's NEM and SWIS grids—with 1.75M+ regional geometries in the Hunter deep-dive and 17 candidate sites audited against 33 localized sensitive receptors (19 schools, 14 hospitals) for 100% ABS land-use ground truth.

2. **85.2% Storage Compression via Havasu (Spatial Iceberg):**
   Compressed raw vector datasets from **~2.9 GB down to ~430.7 MB** using cloud-native GeoParquet and Hilbert-curve spatial partitioning, accelerating full continental query scans from 18.4s down to **3.2s**.

3. **Sub-3-Second Distributed Joins:**
   Executing complex topological repairs (`ST_MakeValid`), 30m riparian buffers, and `ST_Difference` Net Developable Area (NDA) overlays across 1.75M regional geometries in **2.4 seconds**.

4. **Decoupled Architecture & ~$36 AUD Total Batch Spend:**
   By separating heavy geometric calculations from lightweight scoring decay curves ($S_{\text{power}}, S_{\text{water}}, S_{\text{sensitive}}$), our entire multi-week batch ETL, benchmarking, and QA pipeline consumed just **~$36 AUD (US$24.13)** across **~35 automated batch runs (~$1.03/run)**. 
   
   Furthermore, by compiling precomputed distance matrices into a standalone report, interactive What-If scenario simulations and multi-stakeholder persona re-weightings run 100% in-browser via **DuckDB-WASM at $0.00 cloud compute cost**.

---

### 🛡️ A Note on Cloud Cost Management & Lifecycle Best Practices

In the spirit of open engineering, we also discuss practical cloud cost optimization: during initial exploratory testing and iterative tuning, multi-session interactive compute accumulated unexpected development charges.

A joint utilization analysis with Wherobots engineering highlighted key operational takeaways:
* **80% of incurred compute was active execution** during experimentation, with **20% idle before timeout shutdown**.
* Wherobots provides built-in automated guardrails by default (including default idle auto-shutdown within 8 hours and 24-hour runtime limits), which users can further tune with tighter timeout settings.
* As Wherobots' cost guide highlights, idle timeouts serve as a safety backstop—proactive teardowns and programmatic `try...finally: sedona.stop()` blocks are the gold standard.
* Production headless batch ETL across 15.91M national geometries cost just **~$36 AUD (US$24.13)** across ~35 full runs (~$1.03 AUD/run), highlighting the immense efficiency of right-sized headless batch execution.

---

### 🚀 Explore the Links & Live Artifacts

A huge thank you to the Wherobots team for the platform, the invitation, and the opportunity to share this work with the global geospatial community!

* 📖 **Read the Full Wherobots Technical Guest Post:**  
  [Wherobots Official Blog: Scaling AI Data Center Siting](https://wherobots.com/blog/) | [`wherobots_ai_data_center_suitability_blog.html`](https://github.com/GetBack2Basics/hunter_spatial_crafter)  
* ⚡ **Launch the Standalone Interactive National Report (Zero Cloud Cost):**  
  https://national-suitability-report.vercel.app
* 📁 **Explore the Open-Source Repository:**  
  https://github.com/GetBack2Basics/hunter_spatial_crafter
* 📖 **Wherobots & Antigravity Engineering Playbook:**  
  https://github.com/GetBack2Basics/CheatSheets/blob/main/wherobots_antigravity_playbook.md

I welcome thoughts, feedback, and discussion from planners, grid engineers, and spatial practitioners!

---

#Geospatial #SpatialSQL #ApacheSedona #Wherobots #DataCenters #AIInfrastructure #EnergyTransition #RenewableEnergy #DuckDB #OpenData #DigitalTwin #CloudEngineering
