import urllib.request
import json
import xml.etree.ElementTree as ET

# 1. Inspect REST service
rest_url = 'https://services.ga.gov.au/gis/rest/services/Electricity_Infrastructure/MapServer?f=json'
req = urllib.request.Request(rest_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("--- ArcGIS REST Layers ---")
    for l in data.get('layers', []):
        print(f"ID: {l.get('id')}, Name: '{l.get('name')}', minScale: {l.get('minScale')}, maxScale: {l.get('maxScale')}")

# 2. Inspect WMS Capabilities
wms_url = 'https://services.ga.gov.au/gis/services/Electricity_Infrastructure/MapServer/WMSServer?request=GetCapabilities&service=WMS'
req2 = urllib.request.Request(wms_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req2, timeout=10) as resp2:
    xml_data = resp2.read()
    root = ET.fromstring(xml_data)
    print("\n--- WMS Layers in GetCapabilities ---")
    # Search for Layer elements
    for layer in root.iter('{http://www.opengis.net/wms}Layer'):
        name = layer.find('{http://www.opengis.net/wms}Name')
        title = layer.find('{http://www.opengis.net/wms}Title')
        crs = layer.findall('{http://www.opengis.net/wms}CRS')
        name_str = name.text if name is not None else "N/A"
        title_str = title.text if title is not None else "N/A"
        print(f"Name: '{name_str}', Title: '{title_str}'")

