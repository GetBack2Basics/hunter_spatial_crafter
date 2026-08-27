# AuraSiting Crafter

**Tagline:** *The Australian Regional & AI Infrastructure Siting Engine*  
**Repository:** `hunter_spatial_crafter`  
**Author:** George Chandeep Corea  

---

## 🌟 The Story Arc

What began as personal curiosity to test cloud-native spatial data engineering tools against a local council transformation proposal in the Hunter region (the Macquarie Coal Complex in Lake Macquarie) quickly expanded into a state-wide and ultimately **national-scale AI infrastructure siting engine across all 8 Australian jurisdictions**.

AuraSiting Crafter demonstrates how high-performance, transparent spatial analytics provides practical, evidence-based answers to the critical policy questions raised by the Prime Minister, National Cabinet, and state planning agencies regarding data centre energy, water security, and community amenity.

---

## 🚀 Key Capabilities

1. **5-Tier Multi-Criteria Siting & Suitability Engine**:
   - **Power & Former Industrial Assets (40%)**: Proximity to $\ge 132\text{kV}$ transmission lines, terminal substations, and retired coal-fired power station grid injection points.
   - **Sensitive Community Protection (25%)**: Sigmoidal acoustic buffer modeling excluding parcels within $300\text{m}-1,000\text{m}$ of residential zones, schools, and hospitals while preserving regional workforce commute corridors ($1.5\text{km}-15\text{km}$).
   - **Recycled Water & Catchment Safeguards (20%)**: Hard topological masks protecting potable water catchments and rivers; prioritizing industrial effluent and wastewater treatment plant loops.
   - **True Net Developable Space (15%)**: Automated geometric clipping of riparian corridors, easements, steep terrain ($>5\%$), and hazard overlays.

2. **Cloud-Native Scale & Open Standards**:
   - Built on **Apache Sedona (PySpark)**, **Wherobots Cloud**, and **GeoParquet/Havasu** spatial tables.
   - Processed **4.92 million geometries in 200.6 seconds** while compressing spatial layers from ~2.9 GB down to ~430.7 MB.

3. **Zero-Cost Interactive "Map in a Box" Delivery**:
   - Self-contained HTML report with live Kepler.gl map, cadastral search by `Lot/Plan` & street address, and a client-side **What-If Sandbox** powered by DuckDB-WASM for real-time scenario modeling with zero server costs.

---

## 📂 Repository Structure

- `src/Ingestion/macquarie_spatial_ingest.py`: Sedona PySpark pipeline for local precinct constraint extraction and Net Developable Area (NDA) calculations.
- `src/Analysis/national_suitability_analysis.py`: National 5-tier multi-criteria spatial scoring engine across all 8 Australian states & territories.
- `runner/build_suitability_report.py`: Automated builder generating the zero-dependency interactive national report.
- `runner/national_suitability_report.html`: The compiled, self-contained interactive siting dashboard and What-If sandbox.
- `runner/data_verification_technical_report.html`: Technical provenance, coordinate reference systems, and audit verification report.
- `docs/wherobots_ai_data_center_suitability_blog.html`: Wherobots partner technical blog post.
- `docs/linkedin_article_1_submitted.md`: Article 1: *Building a Cloud-Native Regional Spatial Siting Engine* (Submitted).
- `docs/linkedin_article_2_national_siting_puzzle.md`: Article 2: *From a Local Council Proposal to a National Evidence Base* (Draft).
- `docs/strategic_briefing_multi_persona.md`: Multi-persona executive briefing ("I am a...").
- `config/macquarie.json`: Precinct boundaries, buffer thresholds, and CRS parameters.

---

## 🔗 Live Artifacts & Links

- 🌐 **Interactive National Siting Dashboard**: [`runner/national_suitability_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html)
- 📄 **Data Verification & Audit Report**: [`runner/data_verification_technical_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/data_verification_technical_report.html)
- 📝 **LinkedIn Article 2 Draft**: [`docs/linkedin_article_2_national_siting_puzzle.md`](file:///c:/Projects/hunter_spatial_crafter/docs/linkedin_article_2_national_siting_puzzle.md)
- 📚 **Strategic Multi-Persona Briefing**: [`docs/strategic_briefing_multi_persona.md`](file:///c:/Projects/hunter_spatial_crafter/docs/strategic_briefing_multi_persona.md)
