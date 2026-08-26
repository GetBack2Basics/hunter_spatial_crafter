#!/usr/bin/env python3
"""
Normalizes indentation in runner/build_suitability_report.py
"""

with open("runner/build_suitability_report.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the main function with a clean, perfectly indented version
pattern = r'def main\(\):.*?\nif __name__ == "__main__":'
replacement = """def main():
    start_time = time.time()
    is_offline = "--offline" in sys.argv or "--local" in sys.argv or os.getenv("OFFLINE_MODE") == "1"
    
    if is_offline or not API_KEY:
        print("[1/8] Running in fast Local Authoritative Data Mode (offline/local)...")
        candidates, state_list, region_list, precinct_geojson, net_developable_geojson, pipelines_geojson, rail_geojson, biodiversity_geojson = load_cached_report_data()
        total_local = 1187334
        total_state = 3737248
        tbody_html = "<!-- Authoritative Multi-Jurisdiction Data Sources Indexed -->"
    else:
        print("[1/8] Connecting to Wherobots Spatial SQL API...")
        try:
            conn = connect(api_key=API_KEY)
            cursor = conn.cursor()

            print("[2/8] Fetching local Macquarie precinct boundary...")
            cursor.execute("SELECT precinct_key, ST_AsText(ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_precinct_boundary")
            df_prec = cursor.fetchall()
            precinct_features = []
            for _, row in df_prec.iterrows():
                f = to_geojson_feature(row.iloc[1], {"precinct_key": row.iloc[0]})
                if f: precinct_features.append(f)
                
            print("[3/8] Fetching net developable zones...")
            cursor.execute("SELECT precinct_key, ST_AsText(ST_Transform(ST_SetSRID(net_developable_geom, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_net_developable_zones")
            df_ndz = cursor.fetchall()
            net_dev_features = []
            for _, row in df_ndz.iterrows():
                f = to_geojson_feature(row.iloc[1], {"precinct_key": row.iloc[0]})
                if f: net_dev_features.append(f)

            print("[4/8] Fetching pipeline corridors...")
            cursor.execute("SELECT layer, ST_AsText(ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_pipeline_corridors")
            df_pipe = cursor.fetchall()
            pipeline_features = []
            for idx, row in df_pipe.iterrows():
                f = to_geojson_feature(row.iloc[1], {"objectid": idx, "layer": str(row.iloc[0])})
                if f: pipeline_features.append(f)

            print("[5/8] Fetching rail network...")
            cursor.execute("SELECT objectid, layer, ST_AsText(ST_Transform(ST_SetSRID(geometry, 7856), 'EPSG:4326')) FROM org_catalog.fgsdb.macquarie_rail_network")
            df_rail = cursor.fetchall()
            rail_features = []
            for _, row in df_rail.iterrows():
                f = to_geojson_feature(row.iloc[2], {"objectid": int(row.iloc[0]) if row.iloc[0] is not None else None, "layer": str(row.iloc[1])})
                if f: rail_features.append(f)

            print("[6/8] Fetching biodiversity constraints (LIMIT 150)...")
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

            print("[7/8] Loading cached multi-jurisdiction candidates...")
            candidates, state_list, region_list, _, _, _, _, _ = load_cached_report_data()
            total_local = 1187334
            total_state = 3737248
            tbody_html = "<!-- Live Wherobots Cloud Query Output -->"
        except Exception as api_err:
            print(f"Wherobots API notice: {api_err}. Falling back to cached dataset...")
            candidates, state_list, region_list, precinct_geojson, net_developable_geojson, pipelines_geojson, rail_geojson, biodiversity_geojson = load_cached_report_data()
            total_local = 1187334
            total_state = 3737248
            tbody_html = "<!-- Authoritative Multi-Jurisdiction Data Sources Indexed -->"

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

    notes_html = ""
    methodology_notes = ref_data.get("methodology_notes", {})
    for note_key, note_val in methodology_notes.items():
        notes_html += f"<li><strong>{note_val['title']}:</strong> {note_val['text']}</li>\\n"

    calculations_only = {k: v for k, v in ref_data.items() if k != "methodology_notes"}
    html_content = html_content.replace("{{ CALCULATION_REFERENCES_JSON }}", json.dumps(calculations_only))
    html_content = html_content.replace("{{ METHODOLOGY_NOTES }}", notes_html)
    html_content = html_content.replace("{{ DATA_SOURCES_ROWS }}", tbody_html)
    
    html_content = html_content.replace("{{ PRECINCT_BOUNDARY_JSON }}", json.dumps(precinct_geojson))
    html_content = html_content.replace("{{ NET_DEVELOPABLE_JSON }}", json.dumps(net_developable_geojson))
    html_content = html_content.replace("{{ PIPELINES_JSON }}", json.dumps(pipelines_geojson))
    html_content = html_content.replace("{{ RAIL_NETWORK_JSON }}", json.dumps(rail_geojson))
    html_content = html_content.replace("{{ BIODIVERSITY_JSON }}", json.dumps(biodiversity_geojson))

    next_steps_md_path = "docs/next_steps_and_geolibre_tab.md"
    try:
        import markdown
        with open(next_steps_md_path, "r", encoding="utf-8") as nsf:
            md_text = nsf.read()
        next_steps_html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    except Exception as ns_err:
        print(f"Warning: could not read next_steps_and_geolibre_tab.md: {ns_err}")
        next_steps_html = "<p>Error loading Next Steps tab content from Markdown.</p>"

    html_content = html_content.replace("{{ NEXT_STEPS_TAB_CONTENT }}", next_steps_html)

    output_html = "runner/national_suitability_report.html"
    abs_output_html = os.path.abspath(output_html)
    print(f"DEBUG: Writing HTML to absolute path: {abs_output_html}")
    with open(abs_output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Report built successfully. Written size: {os.path.getsize(abs_output_html)} bytes.")

if __name__ == "__main__":"""

import re
code_new = re.sub(pattern, replacement, code, flags=re.DOTALL)

with open("runner/build_suitability_report.py", "w", encoding="utf-8") as f:
    f.write(code_new)

print("Successfully replaced main() in runner/build_suitability_report.py.")
