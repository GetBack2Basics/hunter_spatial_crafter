import re
import json

with open("runner/national_suitability_report.html", "r", encoding="utf-8") as f:
    text = f.read()

match = re.search(r'const candidatesData = (\[.*?\]);', text, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    print(f"Loaded {len(data)} candidates.")
    first = data[0]
    print("Keys of candidate #1:", list(first.keys()))
    for field in ['dist_to_substation_network_km', 'winding_factor', 'dc_to_symbiosis_dist_m', 't_delivery_c', 'discharge_cooling_distance_m', 'is_thermal_symbiosis_viable']:
        has_field = [c['town_name'] for c in data if field in c and c[field] is not None]
        print(f"Field '{field}': present in {len(has_field)}/{len(data)}")
else:
    print("Could not find const candidatesData regex match")
