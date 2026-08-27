# Strategic Positioning & Implementation Plan: AuraSiting Crafter

**Project Name:** AuraSiting Crafter (*The Australian Regional & AI Infrastructure Siting Engine*)  
**Repository:** [`hunter_spatial_crafter`](file:///c:/Projects/hunter_spatial_crafter)  
**Author:** George Chandeep Corea  
**The Story Arc:** What started as a personal curiosity to test cloud spatial tools on a local council precinct proposal (in Lake Macquarie / Hunter) expanded across NSW and scaled nationally across all 8 jurisdictions. It demonstrates how data-driven spatial analysis can provide practical answers to the questions raised by the Prime Minister and National Cabinet regarding data centre energy, water, and community impacts.

---

## 🧭 Multi-Perspective Architecture ("I am a...")

To ensure the framework serves both state and federal stakeholders without dilution, the documentation and interactive tools adopt an audience-driven lens:

1. **"I am a State Spatial Planner / Cadastral Lead" (e.g. NSW DPHI / Spatial Services)**:
   - Focus on automated Net Developable Area (NDA) calculations, GDA2020 cadastral parcel joins (3.5M+ parcels), and zero conflict with state housing targets.
2. **"I am a Federal AI & Energy Policy Lead" (e.g. PM&C Office of AI / AEMO)**:
   - Focus on verifiable "net-zero-load" power connections ($\ge 132\text{kV}$), potable water preservation, and transparent national 8-jurisdiction screening.
3. **"I am a Hyperscale Developer / Infrastructure Investor"**:
   - Focus on derisked site selection, grandfathered brownfield grid connections, and instant `Lot/Plan` due diligence.
4. **"I am a Regional Council / Community Leader" (e.g. Hunter Valley)**:
   - Focus on acoustic buffers ($300\text{m}-1,000\text{m}$), community amenity preservation, and repurposing post-mining assets for high-tech jobs.

---

## 🎛️ Policy Sandbox Presets (Neutral Siting Modes)

The interactive runner UI and What-If sandbox incorporate neutral policy presets:

* **Balanced National Baseline**: Power (40%), Community Protection (25%), Recycled Water (20%), Net Developable Area (15%).
* **Net-Zero Grid Optimization**: Prioritizes direct high-voltage ($\ge 132\text{kV}$) substation proximity and Renewable Energy Zone (REZ) co-location.
* **Maximum Community & Water Protection**: Heightens residential acoustic buffers ($1,000\text{m}$) and mandates non-potable recycled water loops.
* **Regional Brownfield Priority**: Strongly rewards retired coal power stations, former mining infrastructure, and regional employment corridors.

---

## 📄 Published Documentation & Deliverables

| Deliverable | Location | Purpose |
| :--- | :--- | :--- |
| **README Overview** | [`README.md`](file:///c:/Projects/hunter_spatial_crafter/README.md) | Official project documentation, story arc, and capability matrix. |
| **Wherobots Partner Blog** | [`docs/wherobots_ai_data_center_suitability_blog.html`](file:///c:/Projects/hunter_spatial_crafter/docs/wherobots_ai_data_center_suitability_blog.html) | Technical deep-dive on scaling from local precinct to 4.92M geometries nationally. |
| **LinkedIn Thought Leadership** | [`docs/linkedin_article_draft.md`](file:///c:/Projects/hunter_spatial_crafter/docs/linkedin_article_draft.md) | High-impact article connecting the project to the National Cabinet AI standards debate. |
| **Multi-Perspective Briefing** | [`docs/strategic_briefing_multi_persona.md`](file:///c:/Projects/hunter_spatial_crafter/docs/strategic_briefing_multi_persona.md) | Interactive "I am a..." strategic briefing for state and federal stakeholders. |
| **Interactive National Siting Report** | [`runner/national_suitability_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html) | Self-contained "Map in a Box" with live Kepler.gl map and DuckDB-WASM sandbox. |
| **Data Verification Audit** | [`runner/data_verification_technical_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/data_verification_technical_report.html) | Authoritative dataset provenance, CRS parameters, and spatial lineage audit. |
