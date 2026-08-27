# Walkthrough: Editor Review Alignment & Simulated Baselines Implementation

We have updated the guest blog post ([`docs/wherobots_ai_data_center_suitability_blog.html`](file:///c:/Projects/hunter_spatial_crafter/docs/wherobots_ai_data_center_suitability_blog.html)) and interactive report app ([`runner/national_suitability_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html)) to address the editor's notes and the user's feedback regarding simulated regional baselines, portal available vs. ingested counts, and embedding configuration.

## Key Changes Made

### 1. Explicit Simulated Baseline Designation
- **Interstate Candidates**: Latrobe Valley (VIC), Collie (WA), Gladstone (QLD), and other interstate sites are explicitly marked with `<span class="badge badge-simulated">Simulated Baselines</span>` and `(Simulated Regional Baselines)`.
- **Policy Context**: Added clear disclaimers that interstate sites represent modeled regional reference benchmarks, contrasting with the NSW Hunter precinct where multi-tier riparian, pipeline, DEM slope, and cadastral constraints are measured in detail.

### 2. Available Portal Scale vs. Ingested Pilot Scope Distinction
- Explicitly separated the **Published National Registry Universe** (15.91M total geometries across 16 government portals, including 15.4M Geoscape parcels and 47,510 national POIs) from the **Ingested Pilot & Audited QA Scope** (1.75M+ regional geometries in the Hunter deep dive, 17 indexed industrial sites, and 33 audited sensitive receptors in candidate zones across 8 states).

### 3. WordPress Iframe Embed Architecture
- Integrated responsive iframe embed container (`height: 75vh; min-height: 600px; border-radius: 12px`) with the "Open full report in a new tab" link.
- Provided note for WordPress production hosting via `/wp-content/uploads/national-suitability-report.html`.

### 4. Interactive Report App Updates
- Added `SIMULATED REGIONAL BASELINE` badge and copy to the candidate audit panel and leaderboard table for all non-NSW candidate parcels in [`runner/national_suitability_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html).

## Verification Results
- Verified that all mentions of Latrobe, Collie, and Gladstone in the blog post and report app are accompanied by simulated baseline labels.
- Verified that the data verification audit metrics in [`docs/data_verification_audit.json`](file:///c:/Projects/hunter_spatial_crafter/docs/data_verification_audit.json) perfectly match the ingested vs. available definitions in the blog post.
- Compute/Instance Teardown status: All computational jobs are complete and no remote clusters or active spark sessions are running.
