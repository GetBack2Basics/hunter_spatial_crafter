import re

with open("runner/national_suitability_report.html", "r", encoding="utf-8") as f:
    html = f.read()

tab_btns = re.findall(r'class="tab-btn[^"]*"[^>]*>([^<]+)<', html)
tab_contents = re.findall(r'id="([^"]+)"\s+class="tab-content', html)
print("Tab buttons:", tab_btns)
print("Tab contents:", tab_contents)
print("Has Leaflet L.map:", "L.map(" in html)
print("Has #map element:", 'id="map"' in html)
print("Has candidates-table:", 'id="candidates-table"' in html)
