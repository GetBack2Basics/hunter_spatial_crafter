# Walkthrough: Next Steps & GeoLibre AI Integration for National Suitability Report

We have implemented a dedicated **Next Steps & GeoLibre AI Platform** tab in [`runner/national_suitability_report.html`](file:///C:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html), driven by a modular Markdown source file [`docs/next_steps_and_geolibre_tab.md`](file:///C:/Projects/hunter_spatial_crafter/docs/next_steps_and_geolibre_tab.md).

---

## Key Achievements

### 1. Modular Markdown Source Architecture
- **Markdown File**: Created [`docs/next_steps_and_geolibre_tab.md`](file:///C:/Projects/hunter_spatial_crafter/docs/next_steps_and_geolibre_tab.md). Content is kept decoupled from code for simple non-code editing.
- **Generator Script**: Updated [`runner/build_suitability_report.py`](file:///C:/Projects/hunter_spatial_crafter/runner/build_suitability_report.py) to read and parse the Markdown file into styled HTML, embedding it dynamically into the report.
- **Resilient Fallback**: Added offline/cached dataset parsing to `build_suitability_report.py` so the report compiles cleanly even when the Wherobots Cloud API requires payment configuration or is offline.

### 2. Social & Community Sensitive Receptor Scoring Framework
- **Receptor Classes**: Schools, Child Care Centers, Hospitals & Healthcare Facilities, Residential Meshblocks, and Workforce Commute Hubs.
- **Mathematical Sigmoidal Decay Model**:
  $$S_{\text{sensitive}}(d) = \frac{1}{1 + e^{-k (d - d_0)}} \times \psi_{\text{workforce}}(d)$$
- **Setback Controls**: $d < 300\text{m}$ Hard Exclusion, $300\text{m} \le d < 500\text{m}$ Acoustic Penalty Buffer, $500\text{m} \le d < 1.5\text{km}$ Compliant Buffer, $> 5.0\text{km}$ Workforce Commute Decay.

### 3. National Cabinet & Prime Minister Speech AI Energy Analysis
- **Grid Security & Headroom**: Evaluates co-location with retiring thermal power stations (Latrobe, Collie, Gladstone) to utilize existing 330kV+ transmission infrastructure.
- **Water Sustainability**: Mandates WWTW recycled water outfall cooling; penalizes potable drinking water consumption.
- **Regulatory Tiers**: Classifies candidates into *Tier 1: Grid-Ready*, *Tier 2: Conditional*, and *Tier 3: Constrained*.

### 4. GeoLibre Open-Source AI Spatial Platform Integration
- **Cloud Architecture**: Google Cloud Platform (Cloud Run + GCS GeoParquet/PMTiles + client-side DuckDB-WASM).
- **Dual-Model LLM Access**: Free default Gemini API + OpenRouter BYOK (Bring Your Own Key) for non-free models (Claude 3.5 Sonnet, GPT-4o, DeepSeek-R1, Llama 3) inspired by [`GetBack2Basics/LivePersonaCrafter`](https://github.com/GetBack2Basics/LivePersonaCrafter).

---

## Verification Results

### Build Verification
- Executed `.venv\Scripts\python.exe runner/build_suitability_report.py`.
- **Result**: Successfully outputted [`runner/national_suitability_report.html`](file:///C:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html) (9.18 MB) with zero errors.

### UI & Tab Verification
- Confirmed that `<button class="tab-btn" onclick="switchTab(event, 'next-steps-ai')">` renders in the tab bar.
- Confirmed that `<div id="next-steps-ai" class="tab-content">` contains all rendered cards, tables, math equations, and code blocks from Markdown.
