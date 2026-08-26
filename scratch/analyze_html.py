import re

with open("runner/national_suitability_report.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

# Check Leaflet CDN tags
has_leaflet_css = "leaflet.css" in html
has_leaflet_js = "leaflet.js" in html
print("Has Leaflet CSS:", has_leaflet_css)
print("Has Leaflet JS:", has_leaflet_js)

# Check map container
has_map_div = 'id="map"' in html
print("Has #map div:", has_map_div)

# Check CSS for #map
map_css_match = re.search(r'#map\s*\{([^}]+)\}', html)
if map_css_match:
    print("Map CSS:", map_css_match.group(0))
else:
    print("Map CSS: NOT FOUND")

# Check tabs
tabs = re.findall(r'class="[^"]*nav-tab[^"]*"[^>]*>([^<]+)<', html)
print("Nav Tabs found:", tabs)

tab_panes = re.findall(r'id="(tab-[^"]+)"', html)
print("Tab Panes found:", tab_panes)

# Check if tab switching JS exists
has_tab_switch = "switchTab" in html or "showTab" in html or "nav-tab" in html
print("Has tab navigation JS:", has_tab_switch)
