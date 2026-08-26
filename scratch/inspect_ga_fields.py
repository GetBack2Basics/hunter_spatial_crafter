import urllib.request
import json

base_url = "https://services.ga.gov.au/gis/rest/services/Electricity_Infrastructure/MapServer"

# Check layer definitions
for layer_id in [0, 1, 2]:
    url = f"{base_url}/{layer_id}?f=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"Layer {layer_id}: {data.get('name')} | Geometry: {data.get('geometryType')}")
            fields = [f['name'] for f in data.get('fields', [])]
            print(f"   Fields: {fields[:10]}")
    except Exception as e:
        print(f"Error layer {layer_id}: {e}")
