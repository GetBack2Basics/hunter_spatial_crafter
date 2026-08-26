#!/usr/bin/env python3
"""
Updates runner/build_suitability_report.py to include sensitive receptor sigmoidal scoring,
all 8 jurisdictions, cadastre lot/plan search, and links to the data verification audit report.
"""

import os
import re

REPORT_BUILDER_PATH = "runner/build_suitability_report.py"

with open(REPORT_BUILDER_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Header with link to data_verification_technical_report.html
header_pattern = r'<header>\s*<div>\s*<h1>National Siting Suitability Report</h1>\s*<p class="subtitle">.*?</p>\s*</div>\s*<div class="metadata-pill">.*?</div>\s*</header>'
header_replacement = """<header>
    <div>
      <h1>National Siting Suitability Report</h1>
      <p class="subtitle">Multi-Criteria Decision Analysis (MCDA) Engine with Social & Sensitive Receptor Spatial Scoring</p>
    </div>
    <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
      <a href="data_verification_technical_report.html" class="metadata-pill" target="_blank" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); color: #34d399; text-decoration: none; display: inline-flex; align-items: center; gap: 0.4rem;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        Data Provenance & Lineage Audit
      </a>
      <div class="metadata-pill">Wherobots Cloud (Apache Sedona)</div>
    </div>
  </header>"""

code = re.sub(header_pattern, header_replacement, code, flags=re.DOTALL)

# 2. Update Simulation Sliders
sliders_pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(260px, 1fr\)\); gap: 1rem; font-size: 0.875rem;">.*?</div>\s*</div>\s*</div>\s*<div class="grid-dashboard">'
sliders_replacement = """<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; font-size: 0.875rem;">
      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="power-weight-slider"><strong>Power Grid Weight:</strong></label>
          <span id="power-weight-val" style="color: #60a5fa; font-weight: bold;">40%</span>
        </div>
        <input type="range" id="power-weight-slider" min="0" max="100" value="40" style="width: 100%; cursor: pointer;">
      </div>

      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="sensitive-weight-slider"><strong>Sensitive Buffer (S_sens):</strong></label>
          <span id="sensitive-weight-val" style="color: #c084fc; font-weight: bold;">25%</span>
        </div>
        <input type="range" id="sensitive-weight-slider" min="0" max="100" value="25" style="width: 100%; cursor: pointer;">
      </div>

      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="water-weight-slider"><strong>Recycled Water Weight:</strong></label>
          <span id="water-weight-val" style="color: #34d399; font-weight: bold;">20%</span>
        </div>
        <input type="range" id="water-weight-slider" min="0" max="100" value="20" style="width: 100%; cursor: pointer;">
      </div>

      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="size-weight-slider"><strong>Parcel Size Weight:</strong></label>
          <span id="size-weight-val" style="color: #fbbf24; font-weight: bold;">15%</span>
        </div>
        <input type="range" id="size-weight-slider" min="0" max="100" value="15" style="width: 100%; cursor: pointer;">
      </div>

      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="target-size-slider"><strong>Target Parcel Size:</strong></label>
          <span id="target-size-val" style="color: #a78bfa; font-weight: bold;">15 ha</span>
        </div>
        <input type="range" id="target-size-slider" min="3" max="30" value="15" step="1" style="width: 100%; cursor: pointer;">
      </div>
    </div>
  </div>

  <div class="grid-dashboard">"""

code = re.sub(sliders_pattern, sliders_replacement, code, flags=re.DOTALL)

# 3. Update Table Header and Search Input
table_pattern = r'<h2>\s*<svg width="18" height="18" viewBox="0 0 24 24" fill="none".*?National Candidate Leaderboard\s*</h2>\s*<div style="max-height: 490px; overflow-y: auto;">\s*<table id="candidates-table">\s*<thead>\s*<tr>.*?</tr>\s*</thead>'
table_replacement = """<h2>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
        National Candidate Leaderboard
      </h2>
      <div style="margin-bottom: 0.75rem;">
        <input type="text" id="cadastre-search-input" placeholder="🔍 Search candidate sites by Lot/Plan, Address, or Locality..." style="width: 100%; padding: 0.6rem 0.9rem; border-radius: 8px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(59, 130, 246, 0.3); color: #f1f5f9; font-size: 0.85rem; outline: none;" oninput="renderLeaderboard()">
      </div>
      <div style="max-height: 490px; overflow-y: auto;">
        <table id="candidates-table">
          <thead>
            <tr>
              <th>Locality / State</th>
              <th>Cadastre Lot/Plan & Address</th>
              <th title="Composite Suitability Score">MCDA Score</th>
              <th title="Sensitive Receptor Buffer Score">Sensitive Buffer (S_sens)</th>
              <th>Slope (%)</th>
              <th>Area (ha)</th>
              <th>Power (km)</th>
              <th>Water (km)</th>
            </tr>
          </thead>"""

code = re.sub(table_pattern, table_replacement, code, flags=re.DOTALL)

with open(REPORT_BUILDER_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated runner/build_suitability_report.py with HTML header, search, and slider elements.")
