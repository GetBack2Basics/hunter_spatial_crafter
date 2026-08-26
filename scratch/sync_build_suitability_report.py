#!/usr/bin/env python3
"""
Updates runner/build_suitability_report.py to contain the full HTML_TEMPLATE,
the robust load_cached_report_data() function, and the seamless offline/online execution flow.
"""

with open("scratch/assemble_complete_report.py", "r", encoding="utf-8") as f:
    assemble_code = f.read()

with open("runner/build_suitability_report.py", "r", encoding="utf-8") as f:
    original_code = f.read()

# Replace HTML_TEMPLATE in build_suitability_report.py with the updated template
import sys
sys.path.insert(0, ".")
from scratch.assemble_complete_report import template

# Escape any backslashes properly if needed, but in multiline string raw template is clean
start_marker = 'HTML_TEMPLATE = """'
end_marker = '"""\n\ndef to_geojson_feature'
start_pos = original_code.find(start_marker)
end_pos = original_code.find(end_marker)

new_builder_code = (
    original_code[:start_pos + len(start_marker)] +
    template +
    original_code[end_pos:]
)

# Update load_cached_report_data in new_builder_code
cached_func_code = """def load_cached_report_data():
    \"\"\"
    Returns authoritative multi-jurisdiction candidates and cached GeoJSON layers.
    \"\"\"
    html_path = "runner/national_suitability_report.html"
    if not os.path.exists(html_path):
        return None
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        def extract_json(var_name):
            prefix = f"const {var_name} = "
            idx = content.find(prefix)
            if idx == -1:
                return None
            start = idx + len(prefix)
            end = content.find(";\\n", start)
            if end == -1:
                end = content.find(";\\r\\n", start)
            if end == -1:
                return None
            return json.loads(content[start:end].strip())

        candidates = extract_json("candidatesData") or []
        state_list = extract_json("stateData") or []
        region_list = extract_json("regionData") or []
        precinct_geojson = extract_json("precinctBoundaryGeoJSON") or {"type": "FeatureCollection", "features": []}
        net_developable_geojson = extract_json("netDevelopableZonesGeoJSON") or {"type": "FeatureCollection", "features": []}
        pipelines_geojson = extract_json("pipelineCorridorsGeoJSON") or {"type": "FeatureCollection", "features": []}
        rail_geojson = extract_json("railNetworkGeoJSON") or {"type": "FeatureCollection", "features": []}
        biodiversity_geojson = extract_json("biodiversityConstraintsGeoJSON") or {"type": "FeatureCollection", "features": []}

        return (candidates, state_list, region_list, precinct_geojson, net_developable_geojson, pipelines_geojson, rail_geojson, biodiversity_geojson)
    except Exception as e:
        print(f"Warning: could not parse cached dataset: {e}")
        return None"""

import re
new_builder_code = re.sub(r'def load_cached_report_data\(\):.*?\n(?=def main\(\):)', cached_func_code + "\n\n", new_builder_code, flags=re.DOTALL)

with open("runner/build_suitability_report.py", "w", encoding="utf-8") as f:
    f.write(new_builder_code)

print("Updated runner/build_suitability_report.py successfully.")
