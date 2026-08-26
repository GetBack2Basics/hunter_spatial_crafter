#!/usr/bin/env python3
"""
Fixes indentation in main() in runner/build_suitability_report.py
"""

with open("runner/build_suitability_report.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

out_lines = []
in_main_api_block = False

for idx, line in enumerate(lines):
    if line.startswith("def main():"):
        in_main_api_block = True
        out_lines.append(line)
        out_lines.append("    start_time = time.time()\n")
        out_lines.append("    is_offline = '--offline' in sys.argv or '--local' in sys.argv or os.getenv('OFFLINE_MODE') == '1'\n")
        out_lines.append("    if is_offline or not API_KEY:\n")
        out_lines.append("        print('[1/8] Running in fast Local Authoritative Data Mode (offline/local)...')\n")
        out_lines.append("        candidates, state_list, region_list, precinct_geojson, net_developable_geojson, pipelines_geojson, rail_geojson, biodiversity_geojson = load_cached_report_data()\n")
        out_lines.append("        total_local = 1187334\n")
        out_lines.append("        total_state = 3737248\n")
        out_lines.append("        tbody_html = '<!-- Authoritative Multi-Jurisdiction Data Sources Indexed -->'\n")
        out_lines.append("    else:\n")
        out_lines.append("        print('[1/8] Connecting to Wherobots Spatial SQL API...')\n")
        out_lines.append("        try:\n")
        out_lines.append("            conn = connect(api_key=API_KEY)\n")
        out_lines.append("            cursor = conn.cursor()\n")
        continue

    # Skip the old initialization lines
    if in_main_api_block and (
        line.strip().startswith("start_time = time.time()") or
        line.strip().startswith("is_offline =") or
        line.strip().startswith("if is_offline or not API_KEY:") or
        line.strip().startswith("print('[1/8] Running in fast") or
        line.strip().startswith("candidates, state_list, region_list") or
        line.strip().startswith("total_local =") or
        line.strip().startswith("total_state =") or
        line.strip().startswith("tbody_html =") or
        line.strip().startswith("else:") or
        line.strip().startswith("print('[1/8] Connecting to Wherobots") or
        line.strip().startswith("try:") or
        line.strip().startswith("conn = connect(") or
        line.strip().startswith("cursor = conn.cursor()")
    ):
        continue

    # Once we reach # 1. Fetching local Macquarie Precinct... indent the lines inside try
    if in_main_api_block and "# 1. Fetching local Macquarie Precinct" in line:
        # From here up to except Exception as api_err, indent by 4 spaces
        pass

    if in_main_api_block and line.strip().startswith("except Exception as api_err:"):
        out_lines.append("        except Exception as api_err:\n")
        continue
    
    if in_main_api_block and ("# Generate HTML content by injecting JSON" in line):
        in_main_api_block = False

    if in_main_api_block:
        # Check if line should be indented inside try block (lines 1595 to 2187)
        if line.startswith("    "):
            out_lines.append("        " + line)
        else:
            out_lines.append(line)
    else:
        out_lines.append(line)

with open("runner/build_suitability_report.py", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Fixed main() structure in runner/build_suitability_report.py.")
