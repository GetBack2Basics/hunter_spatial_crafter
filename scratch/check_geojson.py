import re

path = "runner/national_suitability_report.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Search for the variables
vars_to_check = [
    "precinctBoundaryGeoJSON",
    "netDevelopableZonesGeoJSON",
    "pipelineCorridorsGeoJSON",
    "railNetworkGeoJSON",
    "biodiversityConstraintsGeoJSON"
]

for var in vars_to_check:
    match = re.search(r'const ' + var + r' = (.*?);', content)
    if match:
        val = match.group(1)
        print(f"{var} length: {len(val)}")
        if len(val) < 200:
            print(f"Content: {val}")
    else:
        print(f"{var} NOT found!")
