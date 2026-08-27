# Implementation Plan: Wherobots Guest Blog Editor Review & Simulated Baselines Alignment

This implementation plan addresses the editor's review feedback for the Wherobots guest blog post and interactive report. It ensures all modeled interstate regional benchmarks (Latrobe Valley, Collie, Gladstone) are explicitly labeled as **simulated regional baselines**, clarifies runtime benchmarks, verifies licensing, structures the WordPress iframe embed, and aligns roadmap and visual assets.

## User Review Required

> [!IMPORTANT]
> **Simulated Regional Baselines vs. Measured Ground-Truth**:
> The Latrobe Valley (VIC), Collie (WA), and Gladstone (QLD) candidates represent modeled regional baselines rather than fully measured site-level ground truths (unlike the NSW Hunter precinct where multi-tier riparian, pipeline, DEM slope, and cadastral constraints are measured in detail). The word **"simulated"** must explicitly appear across all published text, callouts, footnotes, and candidate tables to ensure policy-makers and readers do not mistake modeled benchmarks for measured figures during the ongoing National Cabinet AI data center debate.

> [!NOTE]
> **Licensing Status**:
> The root repository already includes the standard MIT License ([`LICENSE`](file:///c:/Projects/hunter_spatial_crafter/LICENSE)) under George Chandeep Corea (GetBack2Basics). No additional license file creation is needed.

## Proposed Changes

---

### 1. Blog Post HTML Enhancement & Editorial Refinement
#### [MODIFY] [`docs/wherobots_ai_data_center_suitability_blog.html`](file:///c:/Projects/hunter_spatial_crafter/docs/wherobots_ai_data_center_suitability_blog.html)

- **Explicit "Simulated" Regional Baseline Labeling**:
  - Audit all prose in the blog post where interstate comparisons are mentioned (Latrobe Valley in VIC, Collie in WA, Gladstone in QLD).
  - Ensure the term **"simulated regional baselines"** appears in:
    1. The 6-stage workflow description (Stage 5).
    2. The dedicated callout box on Regional Baselines.
    3. The KPI strip metric footnote / tooltip (`#fn-candidates`).
    4. Any candidate comparison summaries.
- **WordPress Iframe Embed Integration & Configuration**:
  - Add standard iframe embed markup snippet and instructions for the Wherobots WordPress deployment:
    - Same-origin `/wp-content/uploads/national-suitability-report.html` path.
    - Responsive wrapper (`height: 80vh; min-height: 640px; border-radius: 12px`).
    - Dedicated "Open full report in a new tab →" link.
    - Note on WordPress SFTP / MIME upload for the 9 MB standalone HTML report.
- **Query Runtime Callout Precision**:
  - Retain the structured breakdown distinguishing:
    - **2.4s**: Spatial SQL join across 1.75M+ features on Wherobots Cloud.
    - **3.2s** (down from 18.4s): Hilbert curve partitioned scan across 15.91M national geometries.
    - **200.6s**: Cold end-to-end multi-table batch ETL pipeline (uncached ingestion, GDA2020 CRS reproject, `ST_MakeValid`, Iceberg write).
    - **< 1ms**: Client-side slider re-scoring in browser.
- **Prose De-personification & Tone Review**:
  - Confirm active author voice ("I built", "I evaluated", "the engine computes") rather than personifying the platform ("the platform lets you").
- **Author Roadmap & GeoLibre Disclaimers**:
  - Maintain the explicit callout that GeoLibre and future natural-language query tools are author roadmap concepts, not current Wherobots platform features.

---

### 2. Interactive Report App Baseline Consistency
#### [MODIFY] [`runner/national_suitability_report.html`](file:///c:/Projects/hunter_spatial_crafter/runner/national_suitability_report.html)

- Ensure the leaderboard and candidate audit cards for interstate sites (Latrobe, Collie, Gladstone) carry prominent visual badges (`badge-simulated` / "Simulated Regional Baseline") and corresponding tooltip text explaining the distinction between measured Hunter sites and modeled regional reference baselines.

---

### 3. Documentation & Review Artifact Persistence
#### [NEW] [`docs/implementation_plan_editor_review.md`](file:///c:/Projects/hunter_spatial_crafter/docs/implementation_plan_editor_review.md)
#### [MODIFY] [`docs/scratchpad.md`](file:///c:/Projects/hunter_spatial_crafter/docs/scratchpad.md)

- Persist the complete editorial notes, blocker resolution trail, and WordPress hosting guidelines in the `docs/` directory per repository governance rules.

---

## Verification Plan

### Automated Checks
- HTML validation check on `docs/wherobots_ai_data_center_suitability_blog.html` and `runner/national_suitability_report.html` to ensure no broken tags, valid anchor IDs, and functional CSS tooltip/callout styling.
- Grep audit across `docs/` to confirm that all instances of "Latrobe", "Collie", and "Gladstone" are accompanied by "simulated" or "simulated regional baseline".

### Manual / Browser Verification
- Open `docs/wherobots_ai_data_center_suitability_blog.html` in browser to verify layout, KPI strip, callouts, code blocks, and iframe embed responsiveness.
- Inspect `runner/national_suitability_report.html` to confirm candidate badges and attribution banner remain intact.
