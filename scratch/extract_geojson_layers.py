#!/usr/bin/env python3
"""Extract GeoJSON layers from the built HTML into runner/attachments/layers/"""
import json
import os

html_path = "runner/national_suitability_report.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

def extract_json(var_name):
    prefix = f"const {var_name} = "
    idx = content.find(prefix)
    if idx == -1:
        return None
    start = idx + len(prefix)
    end = content.find(";\n", start)
    if end == -1:
        end = content.find(";\r\n", start)
    if end == -1:
        return None
    return json.loads(content[start:end].strip())

os.makedirs("runner/attachments/layers", exist_ok=True)

layers = {
    "precinct_boundary": "precinctBoundaryGeoJSON",
    "net_developable": "netDevelopableZonesGeoJSON",
    "pipeline_corridors": "pipelineCorridorsGeoJSON",
    "rail_network": "railNetworkGeoJSON",
    "biodiversity_constraints": "biodiversityConstraintsGeoJSON",
}

for fname, var in layers.items():
    data = extract_json(var) or {"type": "FeatureCollection", "features": []}
    out = "runner/attachments/layers/" + fname + ".json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f)
    count = len(data.get("features", []))
    print(f"{fname}: {count} features -> {out}")

print("Done.")
