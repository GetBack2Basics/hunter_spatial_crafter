# AuraSiting Crafter: Multi-Perspective Strategic Briefing

**Project:** AuraSiting Crafter (*The Australian Regional & AI Infrastructure Siting Engine*)  
**Repository:** [`hunter_spatial_crafter`](file:///c:/Projects/hunter_spatial_crafter)  
**Author:** George Chandeep Corea  
**Core Framework:** Apache Sedona (PySpark), Wherobots Cloud, GeoParquet, DuckDB-WASM  

---

## 🧭 Multi-Perspective Strategic Navigator ("I am a...")

Select your stakeholder perspective below to see how **AuraSiting Crafter** directly addresses your regulatory, infrastructure, or operational priorities:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   "I AM A..."                                          │
├─────────────────────────┬─────────────────────────┬────────────────────────────────────┤
│ [1] NSW / State Planner │ [2] Federal AI & Energy │ [3] Hyperscale Developer / Infratech│
│     or Cadastral Lead   │     Regulator (PM&C)    │     Investor / Site Selection Team │
├─────────────────────────┴─────────────────────────┴────────────────────────────────────┤
│                         [4] Regional Council / Community Leader                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 🏛️ [Perspective 1]: "I am a State Spatial Planner or Cadastral Lead (e.g., NSW DPHI / Spatial Services)"

* **Your Mandate**: Accelerate precinct master planning, achieve state housing targets, protect biodiversity corridors, and modernize the Spatial Digital Twin.
* **How AuraSiting Crafter Helps**:
  * **Zero Housing Cannibalism**: Cross-references ASGS 2021 Meshblocks and G-NAF cadastre to automatically disqualify residential zones and Transport Oriented Development (TOD) corridors.
  * **Automated Net Developable Area (NDA)**: Replaces weeks of manual desktop GIS buffering with distributed Spatial SQL, stripping out riparian corridors, mine subsidence, and easements in seconds.
  * **Digital Twin Interoperability**: Built entirely on open GeoParquet and GDA2020 (EPSG:7844 / EPSG:3112), integrating seamlessly with the NSW Spatial Digital Twin and state web services.

---

### ⚡ [Perspective 2]: "I am a Federal AI & Energy Policy Lead (e.g., PM&C Office of AI, DCCEEW, AEMO)"

* **Your Mandate**: Enforce mandatory national standards for AI data centres by early 2027 (power net-zero-load, water conservation, sovereign capability) without discouraging frontier AI investment.
* **How AuraSiting Crafter Helps**:
  * **Empirical Net-Zero Siting**: Identifies parcels adjacent to $\ge 132\text{kV}$ transmission substations and declared Renewable Energy Zones (REZs) that can underwrite clean power without stressing household grids.
  * **Potable Water Protection**: Maps drinking catchments and prioritizes proximity ($<5\text{km}$) to recycled wastewater treatment plants for closed-loop cooling.
  * **Sovereign Scenario Simulator**: Zero-cloud-cost DuckDB-WASM web dashboard allows regulators to test and adjust policy weightings dynamically in real time.

---

### 💼 [Perspective 3]: "I am a Hyperscale Developer or Infrastructure Investor"

* **Your Mandate**: Rapidly identify bankable, low-risk, power-ready land parcels across Australia with secure water access and minimal planning approval delays.
* **How AuraSiting Crafter Helps**:
  * **National 8-Jurisdiction Screening**: Scans candidate parcels across NSW, QLD, VIC, WA, SA, TAS, ACT, and NT under a unified, consistent 5-tier multi-criteria scoring matrix.
  * **Brownfield Prioritization**: Highlights retired coal-fired power station sites and heavy industrial land with grandfathered grid connections and pre-approved industrial zoning.
  * **Interactive Due Diligence**: Search by exact `Lot/Plan` (e.g. `Lot 1 DP123456`) or street address, with instant access to terrain slope, flood risk, and easement setbacks.

---

### 🏘️ [Perspective 4]: "I am a Regional Council or Community Leader (e.g., Hunter Region)"

* **Your Mandate**: Attract high-paying clean-tech and digital economy jobs through a "just transition" from legacy mining while fiercely protecting local water security, noise amenity, and property values.
* **How AuraSiting Crafter Helps**:
  * **Acoustic & Sensitive Receptor Protection**: Applies strict sigmoidal buffer decay curves ($300\text{m}-1,000\text{m}$) safeguarding schools, hospitals, and homes from industrial cooling and transformer noise.
  * **Brownfield Activation**: Repurposes former coal washeries and industrial rail corridors (e.g. the Macquarie Coal Complex in Lake Macquarie) into high-value digital infrastructure assets.
  * **Open Public Transparency**: Eliminates "black-box" planning proposals by making every constraint layer, buffer calculation, and scoring weight publicly auditable.

---

## 🎛️ Policy Sandbox Presets (What-If Siting Simulator)

When running the interactive dashboard, stakeholders can select from balanced preset profiles:

1. **Balanced National Baseline**: Power (40%), Community Protection (25%), Recycled Water (20%), Net Developable Area (15%).
2. **Net-Zero Grid Optimization**: Prioritizes direct high-voltage substation ties and Renewable Energy Zone co-location.
3. **Maximum Community & Water Protection**: Maximizes acoustic setbacks and enforces zero potable water usage.
4. **Regional Brownfield Priority**: Emphasizes post-industrial land, retired mining assets, and regional economic transition.
