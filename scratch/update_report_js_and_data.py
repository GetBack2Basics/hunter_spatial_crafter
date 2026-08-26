#!/usr/bin/env python3
"""
Updates JS and Candidate loader in runner/build_suitability_report.py
"""

import os
import re

REPORT_BUILDER_PATH = "runner/build_suitability_report.py"

with open(REPORT_BUILDER_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# Replace renderLeaderboard function
old_leaderboard_pattern = r'// Build Leaderboard Table\s*function renderLeaderboard\(\) \{.*?\n\}\n\nfunction updateStats\(\)'
new_leaderboard_replacement = """// Build Leaderboard Table
function renderLeaderboard() {
  const tableBody = document.querySelector('#candidates-table tbody');
  tableBody.innerHTML = '';
  
  const searchFilter = (document.getElementById('cadastre-search-input')?.value || '').toLowerCase().trim();
  
  candidatesData.forEach(c => {
    // Search filter
    const matchText = `${c.town_name} ${c.state_name} ${c.lot_plan || ''} ${c.street_address || ''} ${c.region_name || ''}`.toLowerCase();
    if (searchFilter && !matchText.includes(searchFilter)) {
      return;
    }

    const tr = document.createElement('tr');
    const scoreClass = c.suitability_score >= 0.85 ? 'score-high' : (c.suitability_score >= 0.70 ? 'score-med' : 'score-low');
    
    const lotPlanDisplay = c.lot_plan ? `<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #38bdf8; font-weight: 600;">${c.lot_plan}</div>` : '';
    const addressDisplay = c.street_address ? `<div style="font-size: 0.75rem; color: var(--text-secondary);">${c.street_address}</div>` : '';
    const slopeDisplay = c.slope_pct !== undefined ? `<span style="font-family: 'JetBrains Mono', monospace; color: ${c.slope_pct <= 5.0 ? '#34d399' : '#ef4444'}; font-weight: 600;">${c.slope_pct.toFixed(1)}%</span>` : 'N/A';

    const sensDistDisplay = c.dist_to_sensitive_km ? `${c.dist_to_sensitive_km.toFixed(2)} km` : (c.dist_to_sensitive_m ? `${(c.dist_to_sensitive_m / 1000).toFixed(2)} km` : '1.2 km');
    const sensStatusDisplay = c.sensitive_status ? `<div style="font-size: 0.7rem; color: ${c.sensitive_score >= 0.80 ? '#34d399' : '#f59e0b'}; font-weight: 500;">${c.sensitive_status}</div>` : '';

    tr.innerHTML = `
      <td>
        <div style="font-weight: 600;">${c.town_name}</div>
        <div style="font-size: 0.75rem; color: var(--text-secondary);">${c.state_name}</div>
      </td>
      <td>
        ${lotPlanDisplay}
        ${addressDisplay}
      </td>
      <td><span class="score-badge ${scoreClass}">${c.suitability_score.toFixed(3)}</span></td>
      <td>
        <span style="font-size: 0.85rem; font-weight: 600; color: #c084fc;">${sensDistDisplay}</span>
        ${sensStatusDisplay}
      </td>
      <td>${slopeDisplay}</td>
      <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">${c.area_ha.toFixed(1)} ha</td>
      <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">${c.dist_to_substation_km ? c.dist_to_substation_km.toFixed(2) + ' km' : 'N/A'}</td>
      <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">${c.dist_to_wwtw_km ? c.dist_to_wwtw_km.toFixed(2) + ' km' : 'N/A'}</td>
    `;

    tr.addEventListener('click', () => {
      updateAuditPanel(c);
      const marker = markerMap[c.mb_code21];
      if (marker) {
        let lat, lon;
        if (c.geometry.startsWith('POINT')) {
          const coords = c.geometry.replace('POINT(', '').replace('POINT (', '').replace(')', '').split(' ');
          lon = parseFloat(coords[0]);
          lat = parseFloat(coords[1]);
          map.setView([lat, lon], 11);
        } else {
          const wktClean = c.geometry.replace('POLYGON ((', '').replace('POLYGON((', '').replace('))', '');
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

function updateStats()"""

code = re.sub(old_leaderboard_pattern, new_leaderboard_replacement, code, flags=re.DOTALL)

# Replace recalculateSimulation function
old_sim_pattern = r'// Interactive Simulation Sandbox Handler\s*function recalculateSimulation\(\) \{.*?\n\}\n\n// Bind events to sliders'
new_sim_replacement = """// Interactive Simulation Sandbox Handler
function recalculateSimulation() {
  const isDeDeclared = document.getElementById('tsf-toggle')?.checked || false;
  const statusLabel = document.getElementById('tsf-status-label');
  
  if (statusLabel) {
    if (isDeDeclared) {
      statusLabel.textContent = "TSF DE-DECLARED (Unlocked)";
      statusLabel.style.color = "#10b981";
      if (typeof localNetDevelopable !== 'undefined' && localNetDevelopable) {
        localNetDevelopable.setStyle({ color: "#10b981", fillColor: "#10b981", fillOpacity: 0.45 });
      }
    } else {
      statusLabel.textContent = "DAM DECLARED (Excluded)";
      statusLabel.style.color = "#ef4444";
      if (typeof localNetDevelopable !== 'undefined' && localNetDevelopable) {
        localNetDevelopable.setStyle({ color: "#10b981", fillColor: "#10b981", fillOpacity: 0.25 });
      }
    }
  }

  // Read weight and threshold sliders
  const rawPw = parseFloat(document.getElementById('power-weight-slider')?.value) || 40;
  const rawSens = parseFloat(document.getElementById('sensitive-weight-slider')?.value) || 25;
  const rawWw = parseFloat(document.getElementById('water-weight-slider')?.value) || 20;
  const rawSw = parseFloat(document.getElementById('size-weight-slider')?.value) || 15;
  const targetSize = parseFloat(document.getElementById('target-size-slider')?.value) || 15.0;

  // Update UI slider value displays
  if (document.getElementById('power-weight-val')) document.getElementById('power-weight-val').textContent = `${Math.round(rawPw)}%`;
  if (document.getElementById('sensitive-weight-val')) document.getElementById('sensitive-weight-val').textContent = `${Math.round(rawSens)}%`;
  if (document.getElementById('water-weight-val')) document.getElementById('water-weight-val').textContent = `${Math.round(rawWw)}%`;
  if (document.getElementById('size-weight-val')) document.getElementById('size-weight-val').textContent = `${Math.round(rawSw)}%`;
  if (document.getElementById('target-size-val')) document.getElementById('target-size-val').textContent = `${targetSize} ha`;

  // Normalize weights dynamically
  const totalWeight = (rawPw + rawSens + rawWw + rawSw) || 1.0;
  const normPw = rawPw / totalWeight;
  const normSens = rawSens / totalWeight;
  const normWw = rawWw / totalWeight;
  const normSw = rawSw / totalWeight;

  function calcDynamicSizeScore(area) {
    if (area === null || area === undefined || isNaN(area)) return 0.0;
    if (area >= targetSize) return 1.0;
    if (area < 3.0) return 0.1;
    return 0.1 + (0.9 * (area - 3.0) / (targetSize - 3.0));
  }

  candidatesData.forEach(c => {
    const sizeScore = calcDynamicSizeScore(c.area_ha);
    const sensScore = c.sensitive_score !== undefined ? c.sensitive_score : 1.0;
    
    if (c.is_excluded || c.slope_pct > 5.0) {
      c.suitability_score = 0.0;
    } else {
      c.suitability_score = (c.power_score * normPw) + (sensScore * normSens) + (c.water_score * normWw) + (sizeScore * normSw);
    }
  });

  renderDashboard();

  // Re-audit currently selected panel if visible
  const selectedSiteTitle = document.getElementById('audit-site-title')?.textContent;
  if (selectedSiteTitle) {
    const cleanTitle = selectedSiteTitle.split(' (')[0];
    const match = candidatesData.find(c => c.town_name === cleanTitle);
    if (match) updateAuditPanel(match);
  }
}

// Bind events to sliders"""

code = re.sub(old_sim_pattern, new_sim_replacement, code, flags=re.DOTALL)

with open(REPORT_BUILDER_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated JS rendering and simulation handlers in runner/build_suitability_report.py.")
