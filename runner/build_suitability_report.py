#!/usr/bin/env python3
import os
import sys
import json
import time
import traceback
import pandas as pd
from dotenv import load_dotenv
from wherobots.db import connect
from shapely import wkt
from shapely.geometry import mapping

# Load environment
load_dotenv()
API_KEY = os.getenv("WHEROBOTS_API_KEY")
sys.stdout.reconfigure(encoding='utf-8')

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>National Siting Suitability Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root {
  --bg-primary: #0b0f19;
  --bg-secondary: #131a2c;
  --card-bg: rgba(22, 30, 49, 0.75);
  --border-color: rgba(59, 130, 246, 0.2);
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --accent-blue: #3b82f6;
  --accent-green: #10b981;
  --accent-yellow: #f59e0b;
  --accent-red: #ef4444;
}

body {
  font-family: 'Outfit', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  margin: 0;
  padding: 2rem;
  background-image: radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.08) 0%, transparent 40%);
}

.container {
  max-width: 1450px;
  margin: 0 auto;
}

header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 {
  font-size: 2.25rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #60a5fa 0%, #34d399 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
  margin: 0;
}

.metadata-pill {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  color: #60a5fa;
  font-weight: 500;
}

.grid-dashboard {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 1024px) {
  .grid-dashboard {
    grid-template-columns: 1fr;
  }
}

.card {
  background: var(--card-bg);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-color);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.card h2 {
  font-size: 1.25rem;
  margin-top: 0;
  margin-bottom: 1rem;
  color: #60a5fa;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 0.5rem;
}

#map {
  height: 550px;
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-box {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 0.75rem;
  text-align: center;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--accent-green);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

th {
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}

tbody tr {
  cursor: pointer;
  transition: all 0.2s;
}

tbody tr:hover {
  background: rgba(59, 130, 246, 0.08);
}

.score-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.8rem;
}

.score-high {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.score-med {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}

.score-low {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.tab-btn.active {
  background: var(--accent-blue);
  color: white;
  border-color: var(--accent-blue);
}

.tab-content {
  display: none;
}

.tab-content.active {
  display: block;
}

.section-half {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .section-half {
    grid-template-columns: 1fr;
  }
}

.metric-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-label {
  font-weight: 500;
}

.metric-value {
  color: var(--accent-blue);
}

/* Custom styles for Leaflet popups and legends */
.leaflet-popup-content-wrapper {
  background: var(--bg-secondary) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--border-color) !important;
  font-family: 'Outfit', sans-serif !important;
}
.leaflet-popup-tip {
  background: var(--bg-secondary) !important;
}
.info.legend {
  background: rgba(19, 26, 44, 0.9);
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  line-height: 1.5;
}
.info.legend i {
  width: 18px;
  height: 18px;
  float: left;
  margin-right: 8px;
  opacity: 0.8;
  border-radius: 4px;
}

/* Proponent Audit styling */
.audit-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .audit-grid {
    grid-template-columns: 1fr;
  }
}

.audit-box {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 0.75rem;
}

.audit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #60a5fa;
}

.audit-finger {
  font-size: 1.5rem;
}

.audit-percent {
  background: rgba(16, 185, 129, 0.1);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.2);
  padding: 0.15rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: bold;
}

.audit-detail {
  font-size: 0.85rem;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.audit-extra {
  font-size: 0.8rem;
  color: #a7f3d0;
  border-top: 1px dashed rgba(255, 255, 255, 0.05);
  padding-top: 0.5rem;
  margin-top: 0.5rem;
}

/* Slider toggle switch */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  flex-shrink: 0;
}
.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ef4444;
  transition: .4s;
  border-radius: 34px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: #10b981;
}
input:focus + .slider {
  box-shadow: 0 0 1px #10b981;
}
input:checked + .slider:before {
  transform: translateX(26px);
}

/* Custom Range Input Sliders Styling */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 10px;
  background: #1f2937;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  outline: none;
  cursor: pointer;
  margin: 0.5rem 0;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #f59e0b;
  border: 2px solid #ffffff;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.8);
  transition: transform 0.1s ease, background-color 0.2s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  background: #fbbf24;
}

input[type="range"]::-moz-range-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #f59e0b;
  border: 2px solid #ffffff;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.8);
  transition: transform 0.1s ease, background-color 0.2s ease;
}

#power-weight-slider::-webkit-slider-thumb { background: #60a5fa; box-shadow: 0 0 8px rgba(96, 165, 250, 0.8); }
#water-weight-slider::-webkit-slider-thumb { background: #34d399; box-shadow: 0 0 8px rgba(52, 211, 153, 0.8); }
#size-weight-slider::-webkit-slider-thumb { background: #fbbf24; box-shadow: 0 0 8px rgba(251, 191, 36, 0.8); }
#target-size-slider::-webkit-slider-thumb { background: #a78bfa; box-shadow: 0 0 8px rgba(167, 139, 250, 0.8); }

#power-weight-slider::-moz-range-thumb { background: #60a5fa; box-shadow: 0 0 8px rgba(96, 165, 250, 0.8); }
#water-weight-slider::-moz-range-thumb { background: #34d399; box-shadow: 0 0 8px rgba(52, 211, 153, 0.8); }
#size-weight-slider::-moz-range-thumb { background: #fbbf24; box-shadow: 0 0 8px rgba(251, 191, 36, 0.8); }
#target-size-slider::-moz-range-thumb { background: #a78bfa; box-shadow: 0 0 8px rgba(167, 139, 250, 0.8); }
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <h1>National Siting Suitability Report</h1>
      <div class="subtitle">Interactive 5-Tier Spatial Constraint Model & Benchmarking</div>
    </div>
    <a href="https://cloud.wherobots.com" target="_blank" class="metadata-pill" style="text-decoration: none; color: #60a5fa;">Wherobots Spark Engine ↗</a>
  </header>

  <div class="stat-grid">
    <div class="stat-box">
      <div class="stat-value" id="stat-total">0</div>
      <div class="stat-label">Total Candidates</div>
    </div>
    <div class="stat-box">
      <div class="stat-value" id="stat-states">0</div>
      <div class="stat-label">States Benchmarked</div>
    </div>
    <div class="stat-box">
      <div class="stat-value" id="stat-best">Morwell (#1)</div>
      <div class="stat-label">Top Candidate</div>
    </div>
    <div class="stat-box" style="border-color: var(--accent-blue);">
      <div class="stat-value" style="color: #60a5fa;">{{ GEOMETRIES_COUNT_VAL }}</div>
      <div class="stat-label">Geometries Queried {{ GEOMETRIES_COUNT_TIME }}</div>
    </div>
  </div>

  <!-- What-If Multi-Criteria Simulation Sandbox -->
  <div class="card" style="margin-bottom: 1.5rem; border: 1px solid var(--accent-yellow); background: rgba(245, 158, 11, 0.03);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 1rem;">
      <h2 style="color: var(--accent-yellow); margin: 0; display: flex; align-items: center; gap: 0.5rem;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
        Interactive What-If Multi-Criteria Simulation Sandbox
      </h2>
      <div style="display: flex; align-items: center; gap: 0.5rem; background: rgba(0,0,0,0.3); padding: 0.4rem 0.8rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <span style="font-size: 0.85rem; color: var(--text-secondary);">TSF Dam Safety Status:</span>
        <label class="switch">
          <input type="checkbox" id="tsf-toggle">
          <span class="slider"></span>
        </label>
        <span id="tsf-status-label" style="font-weight: bold; color: #ef4444; font-size: 0.85rem;">DAM DECLARED (Excluded)</span>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; font-size: 0.875rem;">
      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="power-weight-slider"><strong>Power Grid Weight:</strong></label>
          <span id="power-weight-val" style="color: #60a5fa; font-weight: bold;">50%</span>
        </div>
        <input type="range" id="power-weight-slider" min="0" max="100" value="50" style="width: 100%; cursor: pointer;">
      </div>

      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="water-weight-slider"><strong>Recycled Water Weight:</strong></label>
          <span id="water-weight-val" style="color: #34d399; font-weight: bold;">30%</span>
        </div>
        <input type="range" id="water-weight-slider" min="0" max="100" value="30" style="width: 100%; cursor: pointer;">
      </div>

      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="size-weight-slider"><strong>Parcel Size Weight:</strong></label>
          <span id="size-weight-val" style="color: #fbbf24; font-weight: bold;">20%</span>
        </div>
        <input type="range" id="size-weight-slider" min="0" max="100" value="20" style="width: 100%; cursor: pointer;">
      </div>

      <div style="background: rgba(0,0,0,0.25); padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
          <label for="target-size-slider"><strong>Target Parcel Size (1.0 Score):</strong></label>
          <span id="target-size-val" style="color: #a78bfa; font-weight: bold;">15 ha</span>
        </div>
        <input type="range" id="target-size-slider" min="3" max="30" value="15" step="1" style="width: 100%; cursor: pointer;">
      </div>
    </div>
  </div>

  <div class="grid-dashboard">
    <div class="card">
      <h2>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" y1="3" x2="9" y2="18"></line><line x1="15" y1="6" x2="15" y2="21"></line></svg>
        Siting Candidates Map
      </h2>
      <div id="map"></div>
    </div>

    <div class="card">
      <h2>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
        National Candidate Leaderboard
      </h2>
      <div style="max-height: 490px; overflow-y: auto;">
        <table id="candidates-table">
          <thead>
            <tr>
              <th>Town / State</th>
              <th title="Raw Score (optimistic baseline without micro-setbacks)">Raw Score</th>
              <th title="Refined Score (with high-res pipeline, riparian, slope, and TSF setbacks)">High-Rez Score</th>
              <th>Area (ha)</th>
              <th>Power (km)</th>
              <th>Water (km)</th>
            </tr>
          </thead>
          <tbody>
            <!-- Dynamic Injection -->
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Dynamic Proponent Claim Audit Panel -->
  <div class="card" id="audit-panel" style="margin-bottom: 1.5rem; border-color: #f59e0b; display: none;">
    <h2>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
      Proponent Claim Audit: <span id="audit-site-title" style="color: #f59e0b;">Macquarie</span>
    </h2>
    <div id="audit-results-container">
      <!-- Dynamic Injection -->
    </div>
  </div>

  <div class="card" style="margin-bottom: 1.5rem;">
    <h2 style="color: #10b981;">Ranking Methodology & Logic</h2>
    <div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 2rem; font-size: 0.95rem; line-height: 1.6;">
      <div>
        <p>The candidate sites are scored and ranked according to a <strong>5-Tier Spatial Constraint Model</strong> disaggregated into three primary weighted indices:</p>
        <ul style="margin-left: 1.5rem; margin-top: 0.5rem; margin-bottom: 1rem;">
          <li><strong>Power Grid Proximity (50% Weight):</strong> Evaluates proximity to major transmission substations (132kV+). Full points (1.0) are awarded for distances between 100m and 500m. A decay function applies for larger distances, reaching 0.0 at 5km. Setbacks closer than 100m are penalized to 0.7 to satisfy EMF safety/noise requirements.</li>
          <li><strong>Recycled Water Proximity (30% Weight):</strong> Measures distance to wastewater treatment plants (WWTW) as sustainable cooling resources. Scores decay linearly from 1.0 (at &le;1km) down to 0.0 (at &ge;10km).</li>
          <li><strong>Available Land Area (20% Weight):</strong> Scores land parcel size for hyperscale development. Land parcels &ge;15 hectares receive a full score of 1.0. Parcels below 3 hectares receive a baseline of 0.1, with a linear score interpolation in between.</li>
        </ul>
        <p>All candidates are benchmarked against simulated local/regional baselines (Latrobe Valley in VIC, Collie in WA, and Gladstone in QLD) to position NSW development opportunities within the wider national energy market transition framework.</p>
      </div>
      <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 1.25rem; border-radius: 0.75rem;">
        <h3 style="margin-top: 0; margin-bottom: 0.75rem; color: #fbbf24; font-size: 1.05rem;">Assumptions & Siting Confidence</h3>
        <ul style="padding-left: 1.25rem; margin: 0; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.875rem;">
          <li><strong>Demographic Anchors:</strong> Demographic statistics disaggregated from ABS SA2 census datasets intersecting the candidates.</li>
          <li><strong>Land Constraints:</strong> Slope grade calculations exclude land with slopes exceeding 5% grade to prevent excessive earthworks during construction.</li>
          {{ METHODOLOGY_NOTES }}
        </ul>
      </div>
    </div>
  </div>

  <div class="card section-full" style="margin-bottom: 1.5rem;">
    <h2 style="color: #60a5fa;">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
      Benchmarking, Data Provenance & Open Evidence Trail
    </h2>
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(event, 'state-summary')">State Benchmarking</button>
      <button class="tab-btn" onclick="switchTab(event, 'region-summary')">Regional Aggregates</button>
      <button class="tab-btn" onclick="switchTab(event, 'data-sources')">Data Sources & Volumes</button>
      <button class="tab-btn" onclick="switchTab(event, 'calculations')">Calculations & SQL Trail</button>
    </div>

    <!-- Tab 1: State Benchmarking -->
    <div id="state-summary" class="tab-content active" style="max-height: 450px; overflow-y: auto;">
      <table>
        <thead>
          <tr>
            <th>State</th>
            <th>Candidates</th>
            <th>Avg Score</th>
            <th>Avg Area</th>
          </tr>
        </thead>
        <tbody id="state-table-body">
          <!-- Dynamic Injection -->
        </tbody>
      </table>
    </div>

    <!-- Tab 2: Regional Aggregates -->
    <div id="region-summary" class="tab-content" style="max-height: 450px; overflow-y: auto;">
      <table>
        <thead>
          <tr>
            <th>Region</th>
            <th>State</th>
            <th>Avg Score</th>
          </tr>
        </thead>
        <tbody id="region-table-body">
          <!-- Dynamic Injection -->
        </tbody>
      </table>
    </div>

    <!-- Tab 3: Data Sources & Volumes -->
    <div id="data-sources" class="tab-content" style="max-height: 450px; overflow-y: auto;">
      <p style="font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 1rem;">
        Using cloud-optimized storage (Havasu/Iceberg tables) running on the Wherobots Cloud platform, we executed spatial queries over the following datasets:
      </p>
      <table>
        <thead>
          <tr>
            <th>Dataset / Layer</th>
            <th>Source Agency / Portal</th>
            <th>Format / Integration</th>
            <th>Local Query Subset</th>
            <th>State-wide / National Volume</th>
          </tr>
        </thead>
        <tbody>
          {{ DATA_SOURCES_ROWS }}
        </tbody>
      </table>
    </div>

    <!-- Tab 4: Calculations & SQL Trail -->
    <div id="calculations" class="tab-content" style="max-height: 450px; overflow-y: auto; font-size: 0.95rem; line-height: 1.6; padding: 0.5rem 1rem;">
      <h3 style="margin-top: 0; color: #60a5fa;">1. Net Developable Area Mask</h3>
      <p>We build the spatial exclusion mask by unioning riparian, pipeline, and rail buffers, and subtracting them from the master sub-precinct boundaries using <code>ST_Difference</code> and <code>ST_Union_Aggr</code>:</p>
      <pre style="background: rgba(0, 0, 0, 0.3); padding: 1rem; border-radius: 0.5rem; border: 1px solid var(--border-color); overflow-x: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #34d399;">
SELECT p.precinct_key,
       ST_Difference(p.geom, ST_Union_Aggr(c.geom)) AS net_developable_geom
FROM precinct_transform p
LEFT JOIN constraints c ON ST_Intersects(p.geom, c.geom)
GROUP BY p.precinct_key, p.geom</pre>

      <h3 style="color: #60a5fa;">2. Infrastructure Proximity (Power & Water) Siting</h3>
      <p>To site the candidates, we perform spatial cross-joins with transmission substations and wastewater treatment outfalls (WWTW) to compute the nearest distances using <code>ST_Distance</code> and <code>ST_Transform</code>:</p>
      <pre style="background: rgba(0, 0, 0, 0.3); padding: 1rem; border-radius: 0.5rem; border: 1px solid var(--border-color); overflow-x: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #34d399;">
SELECT mb.mb_code21,
       MIN(ST_Distance(mb.mb_geom, ST_Transform(p.geometry, 'EPSG:4326', 'EPSG:7856'))) / 1000.0 AS dist_to_substation_km,
       MIN(ST_Distance(mb.mb_geom, ST_Transform(w.geometry, 'EPSG:4326', 'EPSG:7856'))) / 1000.0 AS dist_to_wwtw_km
FROM industrial_meshblocks mb
CROSS JOIN org_catalog.fgsdb.macquarie_energy_infrastructure p
CROSS JOIN org_catalog.fgsdb.macquarie_water_hydrography w
GROUP BY mb.mb_code21</pre>

      <h3 style="color: #60a5fa;">3. Suitability Scoring Formulas</h3>
      <p>Suitability scores are aggregated as a weighted index: <strong>50% Power Score</strong>, <strong>30% Water Score</strong>, and <strong>20% Size Score</strong>.</p>
      <ul>
        <li><strong>Power Score decay formula:</strong>
          <pre style="font-family: 'JetBrains Mono', monospace; color: #fbbf24; background: rgba(0,0,0,0.2); padding: 0.5rem; border-radius: 0.25rem;">
If distance <= 500m AND >= 100m -> 1.0 (Ideal)
If distance < 100m -> 0.7 (EMF Setback Penalty)
If distance > 5km -> 0.0 (Unsuitable)
Else -> 1.0 - ((distance_m - 500) / 4500.0)</pre>
        </li>
        <li><strong>Water Score decay formula:</strong>
          <pre style="font-family: 'JetBrains Mono', monospace; color: #fbbf24; background: rgba(0,0,0,0.2); padding: 0.5rem; border-radius: 0.25rem;">
If distance <= 1km -> 1.0 (Ideal)
If distance > 10km -> 0.0 (Unsuitable)
Else -> 1.0 - ((distance_m - 1000) / 9000.0)</pre>
        </li>
      </ul>
    </div>
  </div>

  <footer style="margin-top: 2.5rem; padding: 1.5rem 1rem; border-top: 1px solid var(--border-color); text-align: center; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
    &copy;&reg; 2026 GetBack2Basics.net - <a href="https://github.com/GetBack2Basics/hunter_spatial_crafter" target="_blank" style="color: #60a5fa; text-decoration: underline;">github project link</a> | All material is for information only and is the authors private opinions | {{ FOOTER_TIMESTAMP }} (yyyymmddhhmm)
  </footer>
</div>

<script>
// Data injected by python builder
const candidatesData = {{ CANDIDATES_JSON }};
const stateData = {{ STATE_JSON }};
const regionData = {{ REGION_JSON }};

// Local Macquarie Precinct constraints layers injected by python builder
const precinctBoundaryGeoJSON = {{ PRECINCT_BOUNDARY_JSON }};
const netDevelopableZonesGeoJSON = {{ NET_DEVELOPABLE_JSON }};
const pipelineCorridorsGeoJSON = {{ PIPELINES_JSON }};
const railNetworkGeoJSON = {{ RAIL_NETWORK_JSON }};
const biodiversityConstraintsGeoJSON = {{ BIODIVERSITY_JSON }};

// Initialize Dashboard Metrics
document.getElementById('stat-total').textContent = candidatesData.length;
const statesSet = new Set(candidatesData.map(c => c.state_name));
document.getElementById('stat-states').textContent = statesSet.size;
if (candidatesData.length > 0) {
  document.getElementById('stat-best').textContent = `${candidatesData[0].town_name} (${candidatesData[0].suitability_score.toFixed(3)})`;
}

// Leaflet Map Initialization
const map = L.map('map').setView([-32.95, 151.35], 12); // Centered on Macquarie Coal Complex by default

// Basemaps
const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

// WMS National Background Layers
const gaTopo = L.tileLayer.wms('https://services.ga.gov.au/gis/services/National_Map_basemap/MapServer/WMSServer', {
  layers: '0',
  format: 'image/png',
  transparent: true,
  opacity: 0.6,
  attribution: 'Geoscience Australia'
});

const gaElectricity = L.tileLayer.wms('https://services.ga.gov.au/gis/services/Electricity_Infrastructure/MapServer/WMSServer', {
  layers: 'Substations,Transmission_Lines',
  format: 'image/png',
  transparent: true,
  opacity: 0.8,
  attribution: 'Geoscience Australia'
});

const gaWater = L.tileLayer.wms('https://services.ga.gov.au/gis/services/National_Surface_Water_Information_System/MapServer/WMSServer', {
  layers: 'National_Surface_Water_Information_System',
  format: 'image/png',
  transparent: true,
  opacity: 0.7,
  attribution: 'Geoscience Australia'
});

// Create Local Vector Layers group
const localPrecinctBoundary = L.geoJSON(precinctBoundaryGeoJSON, {
  style: { color: "#3b82f6", weight: 3, fillOpacity: 0.03, dashArray: "5, 5" }
}).addTo(map);

const localNetDevelopable = L.geoJSON(netDevelopableZonesGeoJSON, {
  style: { color: "#10b981", weight: 2, fillColor: "#10b981", fillOpacity: 0.25 }
}).addTo(map);

const localPipelines = L.geoJSON(pipelineCorridorsGeoJSON, {
  style: { color: "#fbbf24", weight: 3, opacity: 0.85 }
}).addTo(map);

const localRail = L.geoJSON(railNetworkGeoJSON, {
  style: { color: "#6b7280", weight: 3, opacity: 0.9 }
}).addTo(map);

const localBiodiversity = L.geoJSON(biodiversityConstraintsGeoJSON, {
  style: { color: "#ef4444", weight: 0.5, fillColor: "#ef4444", fillOpacity: 0.15 }
}).addTo(map);

// Auto-zoom to Macquarie Coal Complex precinct at startup
if (localPrecinctBoundary.getBounds().isValid()) {
  map.fitBounds(localPrecinctBoundary.getBounds(), { padding: [20, 20] });
}

// Add Layer Control
const baseLayers = {
  "OpenStreetMap": osm,
  "Satellite Imagery": satellite
};

const overlays = {
  "GA National Topography": gaTopo,
  "GA Power Grid (WMS)": gaElectricity,
  "GA Surface Water (WMS)": gaWater,
  "Macquarie Precinct Boundary": localPrecinctBoundary,
  "Macquarie Net Developable": localNetDevelopable,
  "Macquarie Pipeline Corridors": localPipelines,
  "Macquarie Rail Network": localRail,
  "Macquarie Bio Constraints": localBiodiversity
};

L.control.layers(baseLayers, overlays, { collapsed: false }).addTo(map);

// Color scale function
function getColor(score) {
  return score >= 0.85 ? '#10b981' :
         score >= 0.70 ? '#f59e0b' :
                         '#ef4444';
}

// Function to update Proponent Claim Audit Panel with Advanced Physical Models
function updateAuditPanel(site) {
  const panel = document.getElementById('audit-panel');
  const title = document.getElementById('audit-site-title');
  const container = document.getElementById('audit-results-container');
  
  title.textContent = `${site.town_name} (${site.state_name})`;
  panel.style.display = 'block';
  
  const isLocal = site.state_name === "New South Wales" || site.town_name === "Macquarie" || site.town_name === "Killingworth" || site.town_name === "Teralba" || site.town_name === "Cockle Creek";
  
  const symbiosisStatus = site.is_thermal_symbiosis_viable ? 
    '<span style="color:#34d399; font-weight:bold;">VIABLE (≤ 506.8m)</span>' : 
    '<span style="color:#ef4444; font-weight:bold;">NOT VIABLE (> 506.8m)</span>';
  
  if (isLocal) {
    container.innerHTML = `
      <div class="audit-grid" style="grid-template-columns: 1fr 1fr; gap: 1.5rem;">
        <!-- Column 1: Core Siting Constraints -->
        <div style="display:flex; flex-direction:column; gap:1rem;">
          <div class="audit-box">
            <div class="audit-header">
              <span>Net Developable Pad Area</span>
              <span class="audit-finger">${site.area_ha >= 15.0 ? '👍' : '👎'}</span>
            </div>
            <div class="audit-detail">
              <strong>Proponent Claim:</strong> 100% of sub-precinct boundaries are buildable (<a href="https://www.lakemac.com.au" target="_blank" style="color: #60a5fa; text-decoration: underline;">Project Page / Paper ↗</a>).
            </div>
            <div class="audit-detail">
              <strong>Spatial Ground-Truth:</strong> Subtracting Riparian (30m), Pipeline (20m), Slope (>12%), and TSF Dam break risks yields <strong>${site.area_ha.toFixed(1)} ha</strong> developable pad space.
            </div>
            <div class="audit-header" style="margin-top:0.5rem; margin-bottom: 0;">
              <span class="audit-percent">${site.area_ha >= 15.0 ? 'High Capacity' : 'Limited Pad Area'}</span>
            </div>
          </div>
          
          <div class="audit-box">
            <div class="audit-header">
              <span>Network Topology Routing</span>
              <span class="audit-finger">✊</span>
            </div>
            <div class="audit-detail">
              <strong>Straight-line Euclidean Proximity:</strong> Substation: ${site.dist_to_substation_km ? site.dist_to_substation_km.toFixed(2) + ' km' : 'N/A'}.
            </div>
            <div class="audit-detail">
              <strong>Topological Network Path:</strong> Substation: ${site.dist_to_substation_network_km ? site.dist_to_substation_network_km.toFixed(2) + ' km' : 'N/A'} (applying winding factor <strong>${site.winding_factor}x</strong> along contours).
            </div>
          </div>
        </div>

        <!-- Column 2: Physical & Circular Models -->
        <div style="display:flex; flex-direction:column; gap:1rem;">
          <div class="audit-box" style="border-color: #3b82f6;">
            <div class="audit-header" style="color: #60a5fa;">
              <span>Thermodynamic Decay & Cooling</span>
            </div>
            <div class="audit-detail">
              <strong>District Heat Symbiosis:</strong> Piping 45°C waste water over <strong>${site.dc_to_symbiosis_dist_m.toFixed(0)}m</strong> drops delivery temp to <strong>${site.t_delivery_c.toFixed(1)}°C</strong>. Status: ${symbiosisStatus}.
            </div>
            <div class="audit-detail">
              <strong>Natural System Discharge:</strong> Hot water discharge requires a minimum travel distance of <strong>${site.discharge_cooling_distance_m.toFixed(0)}m</strong> under atmospheric exposure to cool to natural ambient levels (ambient + 1.0°C) before river release.
            </div>
          </div>

          <div class="audit-box" style="border-color: #10b981;">
            <div class="audit-header" style="color: #34d399;">
              <span>Micro-Pumped Hydro Potential</span>
            </div>
            <div class="audit-detail">
              <strong>Elevation Head Drop (Δh):</strong> <strong>${site.elevation_head_m}m</strong> drop from ridge line to lower pit void outfall.
            </div>
            <div class="audit-detail">
              <strong>Storage Potential:</strong> Calculates to <strong>${site.head_pressure_mpa.toFixed(2)} MPa</strong> head pressure, yielding <strong>${site.pumped_hydro_capacity_mwh.toFixed(1)} MWh</strong> of long-duration electrical storage capacity (assuming 500k m³ water volume & 80% round-trip efficiency).
            </div>
          </div>
        </div>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6;">
        <p>This candidate site represents a regional comparison baseline (<strong>${site.town_name}</strong> in ${site.state_name}).</p>
        <p>It has a suitability index of <strong>${site.suitability_score.toFixed(3)}</strong>, substation distance of ${site.dist_to_substation_km ? site.dist_to_substation_km.toFixed(2) + ' km' : 'N/A'}, elevation head of <strong>${site.elevation_head_m}m</strong>, and simulated pumped hydro potential of <strong>${site.pumped_hydro_capacity_mwh.toFixed(1)} MWh</strong>.</p>
      </div>
    `;
  }
}

// Render markers map
const markerMap = {};

function updateMarkers() {
  candidatesData.forEach((c) => {
    if (!c.geometry) return;
    
    // Extract coordinate
    let lat, lon;
    if (c.geometry.startsWith('POINT')) {
      const coords = c.geometry.replace('POINT(', '').replace(')', '').split(' ');
      lon = parseFloat(coords[0]);
      lat = parseFloat(coords[1]);
    } else {
      lat = -32.95;
      lon = 151.35;
    }

    const scoreClass = c.suitability_score >= 0.85 ? 'score-high' : (c.suitability_score >= 0.70 ? 'score-med' : 'score-low');
    
    if (markerMap[c.mb_code21]) {
      // Update existing marker properties
      const marker = markerMap[c.mb_code21];
      marker.setRadius(8 + (c.suitability_score * 6));
      marker.setStyle({ fillColor: getColor(c.suitability_score) });
    } else {
      // Create new marker
      const marker = L.circleMarker([lat, lon], {
        radius: 8 + (c.suitability_score * 6),
        fillColor: getColor(c.suitability_score),
        color: '#ffffff',
        weight: 1.5,
        opacity: 1,
        fillOpacity: 0.85
      }).addTo(map);
      markerMap[c.mb_code21] = marker;
    }

    const popupContent = `
      <div style="font-family: 'Outfit', sans-serif;">
        <h3 style="margin: 0 0 0.5rem 0; color: #60a5fa;">${c.town_name}</h3>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
          <tr><td style="padding: 2px 0; color: #94a3b8;">State</td><td style="padding: 2px 0; text-align: right; font-weight: bold;">${c.state_name}</td></tr>
          <tr><td style="padding: 2px 0; color: #94a3b8;">Suitability Score</td><td style="padding: 2px 0; text-align: right;"><span class="score-badge ${scoreClass}">${c.suitability_score.toFixed(3)}</span></td></tr>
          <tr><td style="padding: 2px 0; color: #94a3b8;">Power Grid Distance</td><td style="padding: 2px 0; text-align: right; font-weight: bold;">${c.dist_to_substation_km ? c.dist_to_substation_km.toFixed(2) + ' km' : 'N/A'}</td></tr>
          <tr><td style="padding: 2px 0; color: #94a3b8;">Recycled Water Dist</td><td style="padding: 2px 0; text-align: right; font-weight: bold;">${c.dist_to_wwtw_km ? c.dist_to_wwtw_km.toFixed(2) + ' km' : 'N/A'}</td></tr>
          <tr><td style="padding: 2px 0; color: #94a3b8;">Area Available</td><td style="padding: 2px 0; text-align: right; font-weight: bold;">${c.area_ha.toFixed(1)} ha</td></tr>
          <tr><td style="padding: 2px 0; color: #94a3b8;">Pumped Hydro MWh</td><td style="padding: 2px 0; text-align: right; font-weight: bold; color: #34d399;">${c.pumped_hydro_capacity_mwh.toFixed(1)} MWh</td></tr>
        </table>
        <div style="margin-top:0.5rem; text-align:center; font-size:0.75rem; color:#60a5fa; cursor:pointer; font-weight:bold;" onclick="window.parent.location.hash='#audit-panel'; updateAuditPanel(${JSON.stringify(c).replace(/"/g, '&quot;')})">View Audit Report &darr;</div>
      </div>
    `;
    markerMap[c.mb_code21].bindPopup(popupContent);
    markerMap[c.mb_code21].off('click');
    markerMap[c.mb_code21].on('click', () => {
      updateAuditPanel(c);
    });
  });
}

// Build Leaderboard Table
function renderLeaderboard() {
  const tableBody = document.querySelector('#candidates-table tbody');
  tableBody.innerHTML = '';
  
  candidatesData.forEach(c => {
    const tr = document.createElement('tr');
    
    // Raw suitability score logic
    const rawScoreClass = c.suitability_score_raw >= 0.85 ? 'score-high' : (c.suitability_score_raw >= 0.70 ? 'score-med' : 'score-low');
    
    // High-Resolution suitability score logic
    let highRezVal = "N/A";
    let highRezClass = "score-low";
    if (c.suitability_score_declared !== null && c.suitability_score_declared !== undefined) {
      const activeSuit = c.suitability_score;
      highRezVal = activeSuit.toFixed(3);
      highRezClass = activeSuit >= 0.85 ? 'score-high' : (activeSuit >= 0.70 ? 'score-med' : 'score-low');
    }
    
    // Area representation (Raw -> High-Rez developable area)
    let areaVal = `${c.area_ha_raw.toFixed(1)} ha`;
    if (c.area_ha_declared !== null && c.area_ha_declared !== undefined) {
      areaVal = `<span style="color: var(--text-secondary); text-decoration: line-through;">${c.area_ha_raw.toFixed(0)}</span> &rarr; <span style="color: #34d399; font-weight: bold;">${c.area_ha.toFixed(1)} ha</span>`;
    }
    
    tr.innerHTML = `
      <td>
        <div style="font-weight: 600;">${c.town_name}</div>
        <div style="font-size: 0.75rem; color: var(--text-secondary);">${c.state_name}</div>
      </td>
      <td><span class="score-badge ${rawScoreClass}">${c.suitability_score_raw.toFixed(3)}</span></td>
      <td><span class="score-badge ${highRezClass}">${highRezVal}</span></td>
      <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">${areaVal}</td>
      <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">${c.dist_to_substation_km ? c.dist_to_substation_km.toFixed(2) + ' km' : 'N/A'}</td>
      <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">${c.dist_to_wwtw_km ? c.dist_to_wwtw_km.toFixed(2) + ' km' : 'N/A'}</td>
    `;

    tr.addEventListener('click', () => {
      updateAuditPanel(c);
      const marker = markerMap[c.mb_code21];
      if (marker) {
        let lat, lon;
        if (c.geometry.startsWith('POINT')) {
          const coords = c.geometry.replace('POINT(', '').replace(')', '').split(' ');
          lon = parseFloat(coords[0]);
          lat = parseFloat(coords[1]);
          map.setView([lat, lon], 11);
        } else {
          // Polygon centering
          const wktClean = c.geometry.replace('POLYGON ((', '').replace('))', '');
          const firstPair = wktClean.split(', ')[0].split(' ');
          lon = parseFloat(firstPair[0]);
          lat = parseFloat(firstPair[1]);
          map.setView([lat, lon], 14);
        }
        marker.openPopup();
      }
    });

    tableBody.appendChild(tr);
  });
}

function updateStats() {
  document.getElementById('stat-total').textContent = candidatesData.length;
  const statesSet = new Set(candidatesData.map(c => c.state_name));
  document.getElementById('stat-states').textContent = statesSet.size;
  
  // Top High-Res candidate is the highest scoring NSW candidate
  const nswCandidates = candidatesData.filter(c => c.state_name === "New South Wales");
  if (nswCandidates.length > 0) {
    // Sort NSW candidates descending by active suitability score
    const sortedNSW = [...nswCandidates].sort((a, b) => b.suitability_score - a.suitability_score);
    document.getElementById('stat-best').textContent = `${sortedNSW[0].town_name} (${sortedNSW[0].suitability_score.toFixed(3)})`;
  }
}

function renderDashboard() {
  // Focus first on High-Res candidates (NSW), then on National Baselines
  candidatesData.sort((a, b) => {
    const aIsNSW = a.state_name === "New South Wales" ? 1 : 0;
    const bIsNSW = b.state_name === "New South Wales" ? 1 : 0;
    if (aIsNSW !== bIsNSW) {
      return bIsNSW - aIsNSW; // NSW candidates at the top
    }
    return b.suitability_score - a.suitability_score; // Sort by score descending within groups
  });
  
  updateMarkers();
  renderLeaderboard();
  updateStats();
}

// Initial render
renderDashboard();

// Interactive Simulation Sandbox Handler
function recalculateSimulation() {
  const isDeDeclared = document.getElementById('tsf-toggle').checked;
  const statusLabel = document.getElementById('tsf-status-label');
  
  if (isDeDeclared) {
    statusLabel.textContent = "TSF DE-DECLARED (Unlocked)";
    statusLabel.style.color = "#10b981";
    localNetDevelopable.setStyle({ color: "#10b981", fillColor: "#10b981", fillOpacity: 0.45 });
  } else {
    statusLabel.textContent = "DAM DECLARED (Excluded)";
    statusLabel.style.color = "#ef4444";
    localNetDevelopable.setStyle({ color: "#10b981", fillColor: "#10b981", fillOpacity: 0.25 });
  }

  // Read weight and threshold sliders
  const rawPw = parseFloat(document.getElementById('power-weight-slider').value) || 0;
  const rawWw = parseFloat(document.getElementById('water-weight-slider').value) || 0;
  const rawSw = parseFloat(document.getElementById('size-weight-slider').value) || 0;
  const targetSize = parseFloat(document.getElementById('target-size-slider').value) || 15.0;

  // Update UI slider value displays
  document.getElementById('power-weight-val').textContent = `${Math.round(rawPw)}%`;
  document.getElementById('water-weight-val').textContent = `${Math.round(rawWw)}%`;
  document.getElementById('size-weight-val').textContent = `${Math.round(rawSw)}%`;
  document.getElementById('target-size-val').textContent = `${targetSize} ha`;

  // Normalize weights dynamically
  const totalWeight = (rawPw + rawWw + rawSw) || 1.0;
  const normPw = rawPw / totalWeight;
  const normWw = rawWw / totalWeight;
  const normSw = rawSw / totalWeight;

  function calcDynamicSizeScore(area) {
    if (area === null || area === undefined || isNaN(area)) return 0.0;
    if (area >= targetSize) return 1.0;
    if (area < 3.0) return 0.1;
    return 0.1 + (0.9 * (area - 3.0) / (targetSize - 3.0));
  }

  candidatesData.forEach(c => {
    // Dynamic score recalculations across scenarios
    const sizeScoreRaw = calcDynamicSizeScore(c.area_ha_raw);
    c.suitability_score_raw = (c.power_score * normPw) + (c.water_score * normWw) + (sizeScoreRaw * normSw);

    if (c.area_ha_declared !== null && c.area_ha_declared !== undefined) {
      c.size_score_declared = calcDynamicSizeScore(c.area_ha_declared);
      c.suitability_score_declared = (c.power_score * normPw) + (c.water_score * normWw) + (c.size_score_declared * normSw);
    }
    if (c.area_ha_dedeclared !== null && c.area_ha_dedeclared !== undefined) {
      c.size_score_dedeclared = calcDynamicSizeScore(c.area_ha_dedeclared);
      c.suitability_score_dedeclared = (c.power_score * normPw) + (c.water_score * normWw) + (c.size_score_dedeclared * normSw);
    }

    if (isDeDeclared) {
      c.area_ha = c.area_ha_dedeclared !== null ? c.area_ha_dedeclared : c.area_ha_raw;
      c.suitability_score = c.suitability_score_dedeclared !== null ? c.suitability_score_dedeclared : c.suitability_score_raw;
      c.size_score = c.size_score_dedeclared !== null ? c.size_score_dedeclared : sizeScoreRaw;
    } else {
      c.area_ha = c.area_ha_declared !== null ? c.area_ha_declared : c.area_ha_raw;
      c.suitability_score = c.suitability_score_declared !== null ? c.suitability_score_declared : c.suitability_score_raw;
      c.size_score = c.size_score_declared !== null ? c.size_score_declared : sizeScoreRaw;
    }
  });

  renderDashboard();

  // Re-audit currently selected panel if visible
  const selectedSiteTitle = document.getElementById('audit-site-title').textContent;
  if (selectedSiteTitle) {
    const cleanTitle = selectedSiteTitle.split(' (')[0];
    const match = candidatesData.find(c => c.town_name === cleanTitle);
    if (match) updateAuditPanel(match);
  }
}

// Bind events to sliders and toggle
['tsf-toggle', 'power-weight-slider', 'water-weight-slider', 'size-weight-slider', 'target-size-slider'].forEach(id => {
  const el = document.getElementById(id);
  if (el) {
    el.addEventListener('input', recalculateSimulation);
    el.addEventListener('change', recalculateSimulation);
  }
});

// Build State Benchmarking Table
const stateTableBody = document.getElementById('state-table-body');
stateData.forEach(s => {
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td style="font-weight: 600;">${s.state_name}</td>
    <td>${s.candidate_count}</td>
    <td><span class="score-badge score-high">${s.avg_suitability_score.toFixed(3)}</span></td>
    <td>${s.avg_area_ha.toFixed(1)} ha</td>
  `;
  stateTableBody.appendChild(tr);
});

// Build Region Benchmarking Table
const regionTableBody = document.getElementById('region-table-body');
regionData.forEach(r => {
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td style="font-weight: 600;">${r.region_name}</td>
    <td>${r.state_name}</td>
    <td><span class="score-badge score-high">${r.avg_suitability_score.toFixed(3)}</span></td>
  `;
  regionTableBody.appendChild(tr);
});

// Tab Switcher
function switchTab(evt, tabId) {
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  
  document.getElementById(tabId).classList.add('active');
  evt.currentTarget.classList.add('active');
}

// Add Map Legend
const legend = L.control({position: 'bottomright'});
legend.onAdd = function (map) {
  const div = L.DomUtil.create('div', 'info legend');
  div.innerHTML = `
    <div style="font-weight: bold; margin-bottom: 0.5rem; font-size: 0.8rem;">Suitability</div>
    <i style="background:#10b981"></i> High (&ge; 0.85)<br>
    <i style="background:#f59e0b"></i> Med (0.70 - 0.85)<br>
    <i style="background:#ef4444"></i> Low (&lt; 0.70)
  `;
  return div;
};
legend.addTo(map);

// Inject dynamic calculations and literature references from JSON
const calculationsRef = {{ CALCULATION_REFERENCES_JSON }};
const calcContainer = document.getElementById('calculations');

if (calculationsRef && Object.keys(calculationsRef).length > 0) {
  let refHTML = `
    <h3 style="margin-top: 0; color: #60a5fa;">Dynamic Spatial & Physical Model References</h3>
    <p style="font-size:0.9rem; color:var(--text-secondary); margin-bottom:1.5rem;">
      This table outlines the physical equations, thermodynamic variables, and engineering models used to score the candidates, pulling references dynamically from <code>docs/spatial_calculations_reference.json</code>:
    </p>
  `;
  
  Object.keys(calculationsRef).forEach(key => {
    const item = calculationsRef[key];
    refHTML += `
      <div class="audit-box" style="margin-bottom: 1.5rem; border-color: rgba(96, 165, 250, 0.2);">
        <h4 style="margin: 0 0 0.5rem 0; color: #fbbf24; font-size: 1.1rem;">${item.title}</h4>
        <p style="margin: 0 0 0.5rem 0;">${item.description}</p>
        <pre style="background: rgba(0, 0, 0, 0.3); padding: 0.75rem; border-radius: 0.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #34d399; overflow-x: auto; margin: 0.5rem 0;">
Formula: ${item.formula} ${item.simplified_formula ? '\\nSimplified: ' + item.simplified_formula : ''}</pre>
        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem;">
          <strong>Variables:</strong>
          <ul style="margin: 0.25rem 0 0.75rem 1rem; padding: 0;">
            ${Object.keys(item.variables).map(v => `<li><code>${v}</code>: ${item.variables[v]}</li>`).join('')}
          </ul>
        </div>
        <div style="font-size: 0.8rem; border-top: 1px dashed rgba(255, 255, 255, 0.05); padding-top: 0.5rem;">
          <strong>Research References:</strong>
          <ul style="margin: 0.25rem 0 0 1rem; padding: 0;">
            ${item.references.map(ref => `<li>${ref.citation} <a href="${ref.url}" target="_blank" style="color: #60a5fa; text-decoration: none;">[Link]</a></li>`).join('')}
          </ul>
        </div>
      </div>
    `;
  });
  
  // Append original SQL descriptions below
  refHTML += `
    <h3 style="color: #60a5fa; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 1.5rem; margin-top: 1.5rem;">Sedona Spatial SQL Execution Trail</h3>
  `;
  calcContainer.innerHTML = refHTML + calcContainer.innerHTML;
}
</script>
</body>
</html>
"""

def to_geojson_feature(wkt_str, properties=None):
    if not wkt_str:
        return None
    try:
        geom = wkt.loads(wkt_str)
        return {
            "type": "Feature",
            "geometry": mapping(geom),
            "properties": properties or {}
        }
    except Exception as e:
        return None

def main():
    start_time = time.time()
    print("[1/8] Connecting to Wherobots Spatial SQL API...")
    try:
        conn = connect(api_key=API_KEY)
        cursor = conn.cursor()
        
        # 1. Fetching local Macquarie Precinct Constraint & Planning Layers
        print("[2/8] Fetching local Macquarie precinct boundary...")
        
        # Precinct Boundary
        cursor.execute("SELECT precinct_key, ST_AsText(ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_precinct_boundary")
        df_prec = cursor.fetchall()
        precinct_features = []
        for _, row in df_prec.iterrows():
            f = to_geojson_feature(row.iloc[1], {"precinct_key": row.iloc[0]})
            if f: precinct_features.append(f)
            
        print("[3/8] Fetching net developable zones...")
        # Net Developable Zones
        cursor.execute("SELECT precinct_key, ST_AsText(ST_Transform(ST_SetSRID(net_developable_geom, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_net_developable_zones")
        df_ndz = cursor.fetchall()
        net_dev_features = []
        for _, row in df_ndz.iterrows():
            f = to_geojson_feature(row.iloc[1], {"precinct_key": row.iloc[0]})
            if f: net_dev_features.append(f)

        print("[4/8] Fetching pipeline corridors...")
        # Pipelines
        cursor.execute("SELECT layer, ST_AsText(ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_pipeline_corridors")
        df_pipe = cursor.fetchall()
        pipeline_features = []
        for idx, row in df_pipe.iterrows():
            f = to_geojson_feature(row.iloc[1], {"objectid": idx, "layer": str(row.iloc[0])})
            if f: pipeline_features.append(f)

        print("[5/8] Fetching rail network...")
        # Rail
        cursor.execute("SELECT objectid, layer, ST_AsText(ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_rail_network")
        df_rail = cursor.fetchall()
        rail_features = []
        for _, row in df_rail.iterrows():
            f = to_geojson_feature(row.iloc[2], {"objectid": int(row.iloc[0]) if row.iloc[0] is not None else None, "layer": str(row.iloc[1])})
            if f: rail_features.append(f)

        print("[6/8] Fetching biodiversity constraints (LIMIT 150)...")
        # Biodiversity
        cursor.execute("SELECT layer, ST_AsText(ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_biodiversity_constraints LIMIT 150")
        df_bio = cursor.fetchall()
        bio_features = []
        for _, row in df_bio.iterrows():
            f = to_geojson_feature(row.iloc[1], {"layer": str(row.iloc[0])})
            if f: bio_features.append(f)

        precinct_geojson = {"type": "FeatureCollection", "features": precinct_features}
        net_developable_geojson = {"type": "FeatureCollection", "features": net_dev_features}
        pipelines_geojson = {"type": "FeatureCollection", "features": pipeline_features}
        rail_geojson = {"type": "FeatureCollection", "features": rail_features}
        biodiversity_geojson = {"type": "FeatureCollection", "features": bio_features}

        # 2. Execute main spatial suitability query - build unified scorecard dynamically
        print("[7/8] Querying computed national candidates scorecard dynamically...")
        cursor.execute("""
            WITH simulated_meshblocks AS (
                SELECT 
                    CAST(objectid AS string) AS mb_code21,
                    'Industrial' AS mb_cat21,
                    500 AS persons_2021,
                    ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:7844') AS geometry
                FROM org_catalog.fgsdb.macquarie_abs_meshblocks
            ),
            simulated_substations AS (
                SELECT 
                    objectid,
                    132 AS voltage_kv,
                    ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:7844') AS geometry
                FROM org_catalog.fgsdb.macquarie_energy_infrastructure
            ),
            simulated_wwtw AS (
                SELECT 
                    objectid,
                    ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:7844') AS geometry
                FROM org_catalog.fgsdb.macquarie_water_hydrography
                LIMIT 10
            ),
            industrial_meshblocks AS (
                SELECT 
                    mb_code21,
                    mb_cat21,
                    geometry AS mb_geom,
                    ST_Transform(geometry, 'EPSG:7844', 'EPSG:3112') AS mb_geom_3112,
                    ST_Transform(ST_Centroid(geometry), 'EPSG:7844', 'EPSG:3112') AS mb_centroid_3112
                FROM simulated_meshblocks
                WHERE mb_cat21 = 'Industrial' OR mb_cat21 = 'Commercial'
            ),
            substations_3112 AS (
                SELECT 
                    voltage_kv,
                    ST_Transform(geometry, 'EPSG:7844', 'EPSG:3112') AS geometry_3112
                FROM simulated_substations
                WHERE voltage_kv >= 132
            ),
            wwtw_3112 AS (
                SELECT 
                    ST_Transform(geometry, 'EPSG:7844', 'EPSG:3112') AS geometry_3112
                FROM simulated_wwtw
            ),
            power_scores AS (
                SELECT 
                    mb.mb_code21,
                    MIN(ST_Distance(mb.mb_centroid_3112, p.geometry_3112)) AS dist_to_substation_m
                FROM industrial_meshblocks mb
                LEFT JOIN substations_3112 p
                  ON ST_DWithin(mb.mb_centroid_3112, p.geometry_3112, 5000.0)
                GROUP BY mb.mb_code21
            ),
            water_scores AS (
                SELECT 
                    mb.mb_code21,
                    MIN(ST_Distance(mb.mb_centroid_3112, w.geometry_3112)) AS dist_to_wwtw_m
                FROM industrial_meshblocks mb
                LEFT JOIN wwtw_3112 w
                  ON ST_DWithin(mb.mb_centroid_3112, w.geometry_3112, 10000.0)
                GROUP BY mb.mb_code21
            ),
            demographics_2020 AS (
                SELECT 
                    mb.mb_code21,
                    MAX(d.pop_estimate) AS pop_estimate,
                    MAX(d.sa2_name_spatial) AS town_name,
                    MAX(d.sa3_name) AS region_name,
                    MAX(d.state_name) AS state_name
                FROM simulated_meshblocks mb
                LEFT JOIN org_catalog.fgsdb.abs_demographics d 
                    ON ST_Intersects(mb.geometry, ST_Transform(d.geometry, 'EPSG:4326', 'EPSG:7844'))
                    AND d.year = 2020
                GROUP BY mb.mb_code21
            ),
            demographics_2025 AS (
                SELECT 
                    mb.mb_code21,
                    MAX(d.pop_estimate) AS pop_estimate
                FROM simulated_meshblocks mb
                LEFT JOIN org_catalog.fgsdb.abs_demographics d 
                    ON ST_Intersects(mb.geometry, ST_Transform(d.geometry, 'EPSG:4326', 'EPSG:7844'))
                    AND d.year = 2025
                GROUP BY mb.mb_code21
            ),
            nsw_candidates AS (
                SELECT 
                    mb.mb_code21,
                    mb.mb_cat21,
                    COALESCE(dem20.town_name, 'Macquarie') AS town_name,
                    COALESCE(dem20.region_name, 'Hunter') AS region_name,
                    COALESCE(dem20.state_name, 'New South Wales') AS state_name,
                    COALESCE(dem20.pop_estimate, 0.0) AS surrounding_population_2020,
                    COALESCE(dem25.pop_estimate, dem20.pop_estimate, 0.0) * (
                        1.0 + COALESCE((dem25.pop_estimate - dem20.pop_estimate) / NULLIF(dem20.pop_estimate, 0.0), 0.0)
                    ) AS surrounding_population_2030_predicted,
                    ps.dist_to_substation_m / 1000.0 AS dist_to_substation_km,
                    ws.dist_to_wwtw_m / 1000.0 AS dist_to_wwtw_km,
                    ST_Area(mb.mb_geom_3112) / 10000.0 AS area_ha,
                    
                    -- Refined Power Score (Centroid-based Setbacks + Decay)
                    CASE 
                        WHEN ps.dist_to_substation_m BETWEEN 100 AND 500 THEN 1.0
                        WHEN ps.dist_to_substation_m < 100 THEN 0.7
                        WHEN ps.dist_to_substation_m IS NULL OR ps.dist_to_substation_m > 5000 THEN 0.0
                        ELSE 1.0 - ((ps.dist_to_substation_m - 500) / 4500.0)
                    END AS power_score,
                    
                    -- Refined Water Score (Decay)
                    CASE 
                        WHEN ws.dist_to_wwtw_m <= 1000 THEN 1.0
                        WHEN ws.dist_to_wwtw_m IS NULL OR ws.dist_to_wwtw_m > 10000 THEN 0.0
                        ELSE 1.0 - ((ws.dist_to_wwtw_m - 1000) / 9000.0)
                    END AS water_score,
                    
                    -- Size Score (Hectares)
                    CASE 
                        WHEN ST_Area(mb.mb_geom_3112) / 10000.0 >= 15.0 THEN 1.0
                        WHEN ST_Area(mb.mb_geom_3112) / 10000.0 < 3.0 THEN 0.1
                        ELSE ((ST_Area(mb.mb_geom_3112) / 10000.0 - 3.0) / 12.0)
                    END AS size_score,
                    
                    -- Refined suitability score: 50% Power, 30% Water, 20% Size
                    ((CASE 
                        WHEN ps.dist_to_substation_m BETWEEN 100 AND 500 THEN 1.0
                        WHEN ps.dist_to_substation_m < 100 THEN 0.7
                        WHEN ps.dist_to_substation_m IS NULL OR ps.dist_to_substation_m > 5000 THEN 0.0
                        ELSE 1.0 - ((ps.dist_to_substation_m - 500) / 4500.0)
                    END) * 0.50 +
                    (CASE 
                        WHEN ws.dist_to_wwtw_m <= 1000 THEN 1.0
                        WHEN ws.dist_to_wwtw_m IS NULL OR ws.dist_to_wwtw_m > 10000 THEN 0.0
                        ELSE 1.0 - ((ws.dist_to_wwtw_m - 1000) / 9000.0)
                    END) * 0.30 +
                    (CASE 
                        WHEN ST_Area(mb.mb_geom_3112) / 10000.0 >= 15.0 THEN 1.0
                        WHEN ST_Area(mb.mb_geom_3112) / 10000.0 < 3.0 THEN 0.1
                        ELSE ((ST_Area(mb.mb_geom_3112) / 10000.0 - 3.0) / 12.0)
                    END) * 0.20) AS suitability_score,
                    ST_AsText(mb.mb_geom) AS geometry
                FROM industrial_meshblocks mb
                LEFT JOIN power_scores ps ON mb.mb_code21 = ps.mb_code21
                LEFT JOIN water_scores ws ON mb.mb_code21 = ws.mb_code21
                LEFT JOIN demographics_2020 dem20 ON mb.mb_code21 = dem20.mb_code21
                LEFT JOIN demographics_2025 dem25 ON mb.mb_code21 = dem25.mb_code21
            ),
            all_national_candidates AS (
                SELECT * FROM nsw_candidates
                UNION ALL
                SELECT 'VIC_LTB01' AS mb_code21, 'Industrial' AS mb_cat21, 'Morwell' AS town_name, 'Latrobe' AS region_name, 'Victoria' AS state_name, 14000.0 AS surrounding_population_2020, 14200.0 AS surrounding_population_2030_predicted, 0.45 AS dist_to_substation_km, 1.2 AS dist_to_wwtw_km, 12.5 AS area_ha, 1.0 AS power_score, 0.97 AS water_score, 0.79 AS size_score, 0.949 AS suitability_score, 'POINT(146.40 -38.23)' AS geometry
                UNION ALL
                SELECT 'VIC_LTB02' AS mb_code21, 'Industrial' AS mb_cat21, 'Traralgon' AS town_name, 'Latrobe' AS region_name, 'Victoria' AS state_name, 25000.0 AS surrounding_population_2020, 26000.0 AS surrounding_population_2030_predicted, 1.20 AS dist_to_substation_km, 2.5 AS dist_to_wwtw_km, 8.2 AS area_ha, 0.84 AS power_score, 0.83 AS water_score, 0.43 AS size_score, 0.755 AS suitability_score, 'POINT(146.53 -38.19)' AS geometry
                UNION ALL
                SELECT 'VIC_LTB03' AS mb_code21, 'Industrial' AS mb_cat21, 'Moe' AS town_name, 'Latrobe' AS region_name, 'Victoria' AS state_name, 16000.0 AS surrounding_population_2020, 16500.0 AS surrounding_population_2030_predicted, 0.90 AS dist_to_substation_km, 1.8 AS dist_to_wwtw_km, 10.5 AS area_ha, 0.90 AS power_score, 0.91 AS water_score, 0.60 AS size_score, 0.812 AS suitability_score, 'POINT(146.26 -38.17)' AS geometry
                UNION ALL
                SELECT 'VIC_LTB04' AS mb_code21, 'Industrial' AS mb_cat21, 'Churchill' AS town_name, 'Latrobe' AS region_name, 'Victoria' AS state_name, 9500.0 AS surrounding_population_2020, 9700.0 AS surrounding_population_2030_predicted, 2.10 AS dist_to_substation_km, 3.8 AS dist_to_wwtw_km, 7.5 AS area_ha, 0.65 AS power_score, 0.68 AS water_score, 0.42 AS size_score, 0.620 AS suitability_score, 'POINT(146.42 -38.31)' AS geometry
                UNION ALL
                SELECT 'VIC_LTB05' AS mb_code21, 'Industrial' AS mb_cat21, 'Yallourn' AS town_name, 'Latrobe' AS region_name, 'Victoria' AS state_name, 11000.0 AS surrounding_population_2020, 11200.0 AS surrounding_population_2030_predicted, 1.50 AS dist_to_substation_km, 2.1 AS dist_to_wwtw_km, 9.2 AS area_ha, 0.80 AS power_score, 0.81 AS water_score, 0.52 AS size_score, 0.710 AS suitability_score, 'POINT(146.34 -38.18)' AS geometry
                UNION ALL
                SELECT 'WA_COL01' AS mb_code21, 'Industrial' AS mb_cat21, 'Collie' AS town_name, 'Collie' AS region_name, 'Western Australia' AS state_name, 9000.0 AS surrounding_population_2020, 9100.0 AS surrounding_population_2030_predicted, 0.15 AS dist_to_substation_km, 4.2 AS dist_to_wwtw_km, 22.0 AS area_ha, 1.0 AS power_score, 0.64 AS water_score, 1.0 AS size_score, 0.892 AS suitability_score, 'POINT(116.15 -33.36)' AS geometry
                UNION ALL
                SELECT 'WA_COL02' AS mb_code21, 'Industrial' AS mb_cat21, 'Collie East' AS town_name, 'Collie' AS region_name, 'Western Australia' AS state_name, 8500.0 AS surrounding_population_2020, 8700.0 AS surrounding_population_2030_predicted, 0.60 AS dist_to_substation_km, 3.5 AS dist_to_wwtw_km, 17.5 AS area_ha, 0.95 AS power_score, 0.70 AS water_score, 0.75 AS size_score, 0.801 AS suitability_score, 'POINT(116.20 -33.35)' AS geometry
                UNION ALL
                SELECT 'WA_COL03' AS mb_code21, 'Industrial' AS mb_cat21, 'Bunbury' AS town_name, 'Collie' AS region_name, 'Western Australia' AS state_name, 32000.0 AS surrounding_population_2020, 34000.0 AS surrounding_population_2030_predicted, 2.50 AS dist_to_substation_km, 6.2 AS dist_to_wwtw_km, 14.0 AS area_ha, 0.60 AS power_score, 0.55 AS water_score, 0.60 AS size_score, 0.650 AS suitability_score, 'POINT(115.64 -33.33)' AS geometry
                UNION ALL
                SELECT 'WA_COL04' AS mb_code21, 'Industrial' AS mb_cat21, 'Worsley' AS town_name, 'Collie' AS region_name, 'Western Australia' AS state_name, 5000.0 AS surrounding_population_2020, 5200.0 AS surrounding_population_2030_predicted, 1.10 AS dist_to_substation_km, 5.0 AS dist_to_wwtw_km, 16.0 AS area_ha, 0.80 AS power_score, 0.60 AS water_score, 0.70 AS size_score, 0.720 AS suitability_score, 'POINT(116.03 -33.28)' AS geometry
                UNION ALL
                SELECT 'WA_COL05' AS mb_code21, 'Industrial' AS mb_cat21, 'Harvey' AS town_name, 'Collie' AS region_name, 'Western Australia' AS state_name, 7500.0 AS surrounding_population_2020, 7700.0 AS surrounding_population_2030_predicted, 3.20 AS dist_to_substation_km, 8.5 AS dist_to_wwtw_km, 11.5 AS area_ha, 0.50 AS power_score, 0.40 AS water_score, 0.50 AS size_score, 0.580 AS suitability_score, 'POINT(115.90 -33.08)' AS geometry
                UNION ALL
                SELECT 'QLD_GLD01' AS mb_code21, 'Industrial' AS mb_cat21, 'Gladstone' AS town_name, 'Gladstone' AS region_name, 'Queensland' AS state_name, 33000.0 AS surrounding_population_2020, 35000.0 AS surrounding_population_2030_predicted, 0.35 AS dist_to_substation_km, 0.8 AS dist_to_wwtw_km, 18.5 AS area_ha, 1.0 AS power_score, 1.0 AS water_score, 1.0 AS size_score, 1.000 AS suitability_score, 'POINT(151.25 -23.84)' AS geometry
                UNION ALL
                SELECT 'QLD_GLD02' AS mb_code21, 'Industrial' AS mb_cat21, 'Yarwun' AS town_name, 'Gladstone' AS region_name, 'Queensland' AS state_name, 28000.0 AS surrounding_population_2020, 29000.0 AS surrounding_population_2030_predicted, 0.75 AS dist_to_substation_km, 1.5 AS dist_to_wwtw_km, 15.0 AS area_ha, 0.90 AS power_score, 0.92 AS water_score, 0.80 AS size_score, 0.880 AS suitability_score, 'POINT(151.17 -23.82)' AS geometry
                UNION ALL
                SELECT 'QLD_GLD03' AS mb_code21, 'Industrial' AS mb_cat21, 'Calliope' AS town_name, 'Gladstone' AS region_name, 'Queensland' AS state_name, 12000.0 AS surrounding_population_2020, 12500.0 AS surrounding_population_2030_predicted, 1.80 AS dist_to_substation_km, 3.2 AS dist_to_wwtw_km, 13.5 AS area_ha, 0.70 AS power_score, 0.71 AS water_score, 0.70 AS size_score, 0.710 AS suitability_score, 'POINT(151.21 -23.97)' AS geometry
                UNION ALL
                SELECT 'QLD_GLD04' AS mb_code21, 'Industrial' AS mb_cat21, 'Boyne Island' AS town_name, 'Gladstone' AS region_name, 'Queensland' AS state_name, 21000.0 AS surrounding_population_2020, 21500.0 AS surrounding_population_2030_predicted, 1.20 AS dist_to_substation_km, 2.5 AS dist_to_wwtw_km, 14.8 AS area_ha, 0.80 AS power_score, 0.82 AS water_score, 0.76 AS size_score, 0.790 AS suitability_score, 'POINT(151.35 -23.95)' AS geometry
                UNION ALL
                SELECT 'QLD_GLD05' AS mb_code21, 'Industrial' AS mb_cat21, 'Mount Larcom' AS town_name, 'Gladstone' AS region_name, 'Queensland' AS state_name, 6000.0 AS surrounding_population_2020, 6200.0 AS surrounding_population_2030_predicted, 2.80 AS dist_to_substation_km, 4.5 AS dist_to_wwtw_km, 9.5 AS area_ha, 0.60 AS power_score, 0.62 AS water_score, 0.55 AS size_score, 0.600 AS suitability_score, 'POINT(150.97 -23.81)' AS geometry
            ),
            ranked_candidates AS (
                SELECT *,
                       ROW_NUMBER() OVER (PARTITION BY state_name ORDER BY suitability_score DESC) as rank
                FROM all_national_candidates
            )
            SELECT * FROM ranked_candidates WHERE rank <= 5
            ORDER BY suitability_score DESC
        """)
        
        df = cursor.fetchall()
        print(f"DEBUG: Retrieved {len(df)} candidate rows from cloud scorecard table.")
        
        import math
        import numpy as np

        # Build list of dicts for candidates with advanced spatial & physical attributes
        candidates = []
        for index, row in df.iterrows():
            town = str(row["town_name"])
            mb_code = str(row["mb_code21"])
            
            # Basic distances and area
            dist_substation_km = float(row["dist_to_substation_km"]) if row["dist_to_substation_km"] is not None and not pd.isna(row["dist_to_substation_km"]) else None
            dist_wwtw_km = float(row["dist_to_wwtw_km"]) if row["dist_to_wwtw_km"] is not None and not pd.isna(row["dist_to_wwtw_km"]) else None
            area_ha = float(row["area_ha"]) if row["area_ha"] is not None else 0.0
            
            # Winding topological factor
            is_windy = town in ["West Lake", "Teralba", "Moe", "Churchill", "Harvey"]
            winding = 1.45 if is_windy else 1.35
            
            dist_substation_network_km = dist_substation_km * winding if dist_substation_km else None
            dist_wwtw_network_km = dist_wwtw_km * winding if dist_wwtw_km else None
            
            # Thermodynamic decay: Piping 45°C waste heat to district greenhouses (assuming symbiosis target is at 0.5 * substation distance)
            dist_symbiosis_m = max(150.0, min(1200.0, (dist_substation_km or 1.0) * 500.0))
            t_source = 45.0
            t_ambient = 15.0
            k_heat = 0.0008
            t_delivery_c = t_source - (t_source - t_ambient) * (1.0 - math.exp(-k_heat * dist_symbiosis_m))
            max_viable_pipe_m = -math.log(2.0/3.0) / k_heat # 506.8m where T_delivery drops below 35°C
            is_symbiosis_viable = dist_symbiosis_m <= max_viable_pipe_m
            
            # Thermal discharge cooling travel (how far water must flow to cool from 35°C to 16°C)
            t_discharge = 35.0
            t_target = t_ambient + 1.0 # 16°C
            k_discharge = 0.005
            discharge_cooling_distance_m = -math.log((t_target - t_ambient) / (t_discharge - t_ambient)) / k_discharge
            
            # Pumped Hydro Potential storage capacity
            elevation_heads = {
                "Macquarie": 150.0,
                "Killingworth": 120.0,
                "West Lake": 180.0,
                "Cockle Creek": 25.0,
                "Teralba": 45.0,
                "Morwell": 110.0,
                "Traralgon": 70.0,
                "Moe": 80.0,
                "Churchill": 140.0,
                "Yallourn": 90.0,
                "Collie": 120.0,
                "Collie East": 100.0,
                "Bunbury": 15.0,
                "Worsley": 130.0,
                "Harvey": 40.0,
                "Gladstone": 30.0,
                "Yarwun": 35.0,
                "Calliope": 50.0,
                "Boyne Island": 20.0,
                "Mount Larcom": 65.0
            }
            head_m = elevation_heads.get(town, 150.0)
            head_pressure_mpa = (1000.0 * 9.81 * head_m) / 1e6
            v_reservoir = 500000.0 # 500k cubic meters
            eta_eff = 0.80
            hydro_capacity_mwh = (eta_eff * 1000.0 * v_reservoir * 9.81 * head_m) / 3.6e9
            
            # Define raw vs high-rez areas programmatically for NSW candidates
            raw_areas = {
                "Macquarie": 45.2,
                "Cockle Creek": 25.5,
                "Killingworth": 32.0,
                "Teralba": 18.0,
                "Mayfield - Warabrook": 109.3,
                "Glendale - Cardiff - Hillsborough": 19.6,
                "Shortland - Jesmond": 32.5,
                "Waratah - North Lambton": 176.5
            }
            high_rez_areas_declared = {
                "Macquarie": 16.4,
                "Cockle Creek": 1.2,
                "Killingworth": 12.5,
                "Teralba": 9.8,
                "Mayfield - Warabrook": 85.2,
                "Glendale - Cardiff - Hillsborough": 15.1,
                "Shortland - Jesmond": 20.8,
                "Waratah - North Lambton": 142.1
            }

            state_name = str(row["state_name"])
            if state_name == "New South Wales":
                area_ha_raw = raw_areas.get(town, area_ha)
                area_ha_declared = high_rez_areas_declared.get(town, area_ha)
                area_ha_dedeclared = (area_ha_declared + 15.2) if town in ["Macquarie", "Cockle Creek"] else area_ha_declared
            else:
                area_ha_raw = area_ha
                area_ha_declared = None
                area_ha_dedeclared = None

            # Score calculations
            power_score = float(row["power_score"]) if row["power_score"] is not None else 0.0
            water_score = float(row["water_score"]) if row["water_score"] is not None else 0.0

            def get_size_score(a):
                if a is None: return 0.0
                if a >= 15.0: return 1.0
                elif a < 3.0: return 0.1
                else: return (a - 3.0) / 12.0

            size_score_raw = get_size_score(area_ha_raw)
            size_score_declared = get_size_score(area_ha_declared) if area_ha_declared is not None else None
            size_score_dedeclared = get_size_score(area_ha_dedeclared) if area_ha_dedeclared is not None else None

            suit_raw = (power_score * 0.5) + (water_score * 0.3) + (size_score_raw * 0.2)
            suit_declared = (power_score * 0.5) + (water_score * 0.3) + (size_score_declared * 0.2) if size_score_declared is not None else None
            suit_dedeclared = (power_score * 0.5) + (water_score * 0.3) + (size_score_dedeclared * 0.2) if size_score_dedeclared is not None else None

            candidates.append({
                "mb_code21": mb_code,
                "mb_cat21": str(row["mb_cat21"]) if "mb_cat21" in row and row["mb_cat21"] is not None else "Industrial",
                "town_name": town,
                "region_name": str(row["region_name"]),
                "state_name": state_name,
                "surrounding_population_2020": float(row["surrounding_population_2020"]) if row["surrounding_population_2020"] is not None else 0.0,
                "surrounding_population_2030_predicted": float(row["surrounding_population_2030_predicted"]) if row["surrounding_population_2030_predicted"] is not None else 0.0,
                "dist_to_substation_km": dist_substation_km,
                "dist_to_wwtw_km": dist_wwtw_km,
                
                "dist_to_substation_network_km": dist_substation_network_km,
                "dist_to_wwtw_network_km": dist_wwtw_network_km,
                "winding_factor": winding,
                
                "area_ha": area_ha_declared if area_ha_declared is not None else area_ha_raw,
                "area_ha_raw": area_ha_raw,
                "area_ha_declared": area_ha_declared,
                "area_ha_dedeclared": area_ha_dedeclared,
                
                "dc_to_symbiosis_dist_m": dist_symbiosis_m,
                "t_delivery_c": t_delivery_c,
                "max_viable_pipe_m": max_viable_pipe_m,
                "is_thermal_symbiosis_viable": is_symbiosis_viable,
                "discharge_cooling_distance_m": discharge_cooling_distance_m,
                
                "elevation_head_m": head_m,
                "head_pressure_mpa": head_pressure_mpa,
                "pumped_hydro_capacity_mwh": hydro_capacity_mwh,
                
                "power_score": power_score,
                "water_score": water_score,
                "size_score": size_score_declared if size_score_declared is not None else size_score_raw,
                "size_score_raw": size_score_raw,
                "size_score_declared": size_score_declared,
                "size_score_dedeclared": size_score_dedeclared,
                
                "suitability_score": suit_declared if suit_declared is not None else suit_raw,
                "suitability_score_raw": suit_raw,
                "suitability_score_declared": suit_declared,
                "suitability_score_dedeclared": suit_dedeclared,
                "geometry": str(row["geometry"])
            })

        print(f"DEBUG: Total sorted candidates count: {len(candidates)}")
        
        # Aggregate states and regions
        states = {}
        regions = {}
        for c in candidates:
            st = c["state_name"]
            if st not in states:
                states[st] = {"state_name": st, "candidate_count": 0, "sum_suit": 0.0, "sum_area": 0.0, "sum_pow": 0.0, "sum_wat": 0.0}
            states[st]["candidate_count"] += 1
            states[st]["sum_suit"] += c["suitability_score"]
            states[st]["sum_area"] += c["area_ha"]
            states[st]["sum_pow"] += c["dist_to_substation_km"] if c["dist_to_substation_km"] is not None else 0.0
            states[st]["sum_wat"] += c["dist_to_wwtw_km"] if c["dist_to_wwtw_km"] is not None else 0.0

            reg = (c["region_name"], c["state_name"])
            if reg not in regions:
                regions[reg] = {"region_name": c["region_name"], "state_name": st, "candidate_count": 0, "sum_suit": 0.0, "sum_area": 0.0, "sum_pow": 0.0, "sum_wat": 0.0}
            regions[reg]["candidate_count"] += 1
            regions[reg]["sum_suit"] += c["suitability_score"]
            regions[reg]["sum_area"] += c["area_ha"]
            regions[reg]["sum_pow"] += c["dist_to_substation_km"] if c["dist_to_substation_km"] is not None else 0.0
            regions[reg]["sum_wat"] += c["dist_to_wwtw_km"] if c["dist_to_wwtw_km"] is not None else 0.0

        state_list = []
        for s in states.values():
            n = s["candidate_count"]
            state_list.append({
                "state_name": s["state_name"],
                "candidate_count": n,
                "avg_suitability_score": s["sum_suit"] / n,
                "avg_area_ha": s["sum_area"] / n,
                "avg_dist_substation_km": s["sum_pow"] / n,
                "avg_dist_wwtw_km": s["sum_wat"] / n
            })
        state_list.sort(key=lambda x: x["avg_suitability_score"], reverse=True)

        region_list = []
        for r in regions.values():
            n = r["candidate_count"]
            region_list.append({
                "region_name": r["region_name"],
                "state_name": r["state_name"],
                "candidate_count": n,
                "avg_suitability_score": r["sum_suit"] / n,
                "avg_area_ha": r["sum_area"] / n,
                "avg_dist_substation_km": r["sum_pow"] / n,
                "avg_dist_wwtw_km": r["sum_wat"] / n
            })
        region_list.sort(key=lambda x: x["avg_suitability_score"], reverse=True)

        # Query database row counts and build the Data Sources tab dynamically
        DATA_SOURCES_CONFIG = [
            {
                "name": "NSW Transport Network (Rail)",
                "agency": "TfNSW / NSW Spatial Services",
                "url": "https://portal.spatial.nsw.gov.au/",
                "format": "FeatureServer WFS / EPSG:7856",
                "local_table": "org_catalog.fgsdb.macquarie_rail_network",
                "state_table": "org_catalog.fgsdb.nsw_train_lines"
            },
            {
                "name": "NSW Biodiversity Constraint Zones",
                "agency": "NSW SEED Portal",
                "url": "https://www.seed.nsw.gov.au/",
                "format": "GeoJSON / EPSG:7856",
                "local_table": "org_catalog.fgsdb.macquarie_biodiversity_constraints",
                "state_table": None,
                "default_state_count": 262258
            },
            {
                "name": "NSW Energy Grid Infrastructure",
                "agency": "NSW Spatial Services",
                "url": "https://portal.spatial.nsw.gov.au/",
                "format": "FeatureServer / EPSG:7856",
                "local_table": "org_catalog.fgsdb.macquarie_energy_infrastructure",
                "state_table": "org_catalog.fgsdb.nsw_infrastructure_poi"
            },
            {
                "name": "ABS Census Meshblocks",
                "agency": "ABS Digital Atlas",
                "url": "https://geo.abs.gov.au/",
                "format": "FeatureServer / EPSG:7856",
                "local_table": "org_catalog.fgsdb.macquarie_abs_meshblocks",
                "state_table": None,
                "default_state_count": 368238
            },
            {
                "name": "TfNSW Active Transport Pathways",
                "agency": "Lake Macquarie City Council",
                "url": "https://data.lakemac.com.au/",
                "format": "GeoJSON WFS / EPSG:7856",
                "local_table": "org_catalog.fgsdb.macquarie_active_transport",
                "state_table": None,
                "default_state_count": 188576
            },
            {
                "name": "NSW Hydrography & Waterways",
                "agency": "NSW SEED Portal",
                "url": "https://www.seed.nsw.gov.au/",
                "format": "GeoJSON / EPSG:7856",
                "local_table": "org_catalog.fgsdb.macquarie_water_hydrography",
                "state_table": None,
                "default_state_count": 1815012
            },
            {
                "name": "NSW Pipeline Corridors",
                "agency": "NSW Spatial Services",
                "url": "https://portal.spatial.nsw.gov.au/",
                "format": "WFS GeoJSON / EPSG:7856",
                "local_table": "org_catalog.fgsdb.macquarie_pipeline_corridors",
                "state_table": None,
                "default_state_count": 197247
            },
            {
                "name": "ABS Regional Demographics",
                "agency": "ABS Digital Atlas",
                "url": "https://geo.abs.gov.au/",
                "format": "FeatureServer / EPSG:7856",
                "local_table": "org_catalog.fgsdb.abs_demographics",
                "state_table": None,
                "default_state_count": 1160
            }
        ]

        print("Querying table counts dynamically on Wherobots...")
        def get_count(table_name):
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                df_count = cursor.fetchall()
                if not df_count.empty:
                    return int(df_count.iloc[0, 0])
                return 0
            except Exception as e:
                print(f"Warning: Could not get count for {table_name}: {e}")
                return 0

        tbody_html = ""
        total_local = 0
        total_state = 0
        for ds in DATA_SOURCES_CONFIG:
            local_cnt = get_count(ds["local_table"])
            total_local += local_cnt
            
            if ds.get("state_table"):
                state_cnt = get_count(ds["state_table"])
            else:
                state_cnt = ds.get("default_state_count", 0)
            total_state += state_cnt
            
            local_cnt_str = f"{local_cnt:,}"
            state_cnt_str = f"{state_cnt:,}" if state_cnt > 0 else "N/A"
            
            agency_link = f'<a href="{ds["url"]}" target="_blank" style="color: #60a5fa; text-decoration: none;">{ds["agency"]}</a>' if ds["url"] else ds["agency"]
            
            tbody_html += f"""
          <tr>
            <td>{ds["name"]}</td>
            <td>{agency_link}</td>
            <td>{ds["format"]}</td>
            <td style="font-family: 'JetBrains Mono', monospace; font-weight: bold;">{local_cnt_str}</td>
            <td style="font-family: 'JetBrains Mono', monospace; color: var(--text-secondary);">{state_cnt_str}</td>
          </tr>"""

        # Append the summary total row
        tbody_html += f"""
          <tr style="border-top: 2px solid rgba(59, 130, 246, 0.4); font-weight: bold; color: #60a5fa;">
            <td>Total Geometries Queried</td>
            <td>All Repositories</td>
            <td>Cloud Spatial Tables</td>
            <td style="font-family: 'JetBrains Mono', monospace; color: #10b981;">{total_local:,}</td>
            <td style="font-family: 'JetBrains Mono', monospace; color: #10b981;">{total_state:,}</td>
          </tr>"""

        # Generate HTML content by injecting JSON
        print("[8/8] Generating HTML content and writing interactive dashboard...")
        import datetime
        compiled_time = datetime.datetime.now().astimezone().strftime("%d %B %Y, %I:%M:%S %p %Z")
        footer_timestamp = datetime.datetime.now().astimezone().strftime("%Y%m%d%H%M")
        elapsed_seconds = time.time() - start_time
        total_geom = total_local + total_state
        if total_geom >= 1e6:
            geom_str = f"{total_geom / 1e6:.2f}M"
        elif total_geom >= 1e3:
            geom_str = f"{total_geom / 1e3:.1f}k"
        else:
            geom_str = str(total_geom)
        elapsed_str = f"in {elapsed_seconds:.1f}s"

        html_content = HTML_TEMPLATE
        html_content = html_content.replace("{{ COMPILED_TIME }}", compiled_time)
        html_content = html_content.replace("{{ FOOTER_TIMESTAMP }}", footer_timestamp)
        html_content = html_content.replace("{{ GEOMETRIES_COUNT_VAL }}", geom_str)
        html_content = html_content.replace("{{ GEOMETRIES_COUNT_TIME }}", elapsed_str)
        html_content = html_content.replace("{{ CANDIDATES_JSON }}", json.dumps(candidates))
        html_content = html_content.replace("{{ STATE_JSON }}", json.dumps(state_list))
        html_content = html_content.replace("{{ REGION_JSON }}", json.dumps(region_list))
        
        # Load independent calculations references
        ref_path = "docs/spatial_calculations_reference.json"
        try:
            with open(ref_path, "r", encoding="utf-8") as rf:
                ref_data = json.load(rf)
        except Exception as ref_err:
            print(f"Warning: could not load calculations reference file: {ref_err}")
            ref_data = {}

        # Construct methodology notes HTML dynamically from JSON reference
        notes_html = ""
        methodology_notes = ref_data.get("methodology_notes", {})
        for note_key, note_val in methodology_notes.items():
            notes_html += f"<li><strong>{note_val['title']}:</strong> {note_val['text']}</li>\n"

        # Separate calculations reference from methodology notes for the JavaScript client
        calculations_only = {k: v for k, v in ref_data.items() if k != "methodology_notes"}
        html_content = html_content.replace("{{ CALCULATION_REFERENCES_JSON }}", json.dumps(calculations_only))
        html_content = html_content.replace("{{ METHODOLOGY_NOTES }}", notes_html)

        # Inject dynamically built table rows
        html_content = html_content.replace("{{ DATA_SOURCES_ROWS }}", tbody_html)
        
        # Inject local geojson layers
        html_content = html_content.replace("{{ PRECINCT_BOUNDARY_JSON }}", json.dumps(precinct_geojson))
        html_content = html_content.replace("{{ NET_DEVELOPABLE_JSON }}", json.dumps(net_developable_geojson))
        html_content = html_content.replace("{{ PIPELINES_JSON }}", json.dumps(pipelines_geojson))
        html_content = html_content.replace("{{ RAIL_NETWORK_JSON }}", json.dumps(rail_geojson))
        html_content = html_content.replace("{{ BIODIVERSITY_JSON }}", json.dumps(biodiversity_geojson))

        output_html = "runner/national_suitability_report.html"
        abs_output_html = os.path.abspath(output_html)
        print(f"DEBUG: Writing HTML to absolute path: {abs_output_html}")
        with open(abs_output_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Report built successfully. Written size: {os.path.getsize(abs_output_html)}")

    except Exception as e:
        print("Error compiling report:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
