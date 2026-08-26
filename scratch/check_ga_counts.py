import urllib.request
import json

base_url = "https://services.ga.gov.au/gis/rest/services/Electricity_Infrastructure/MapServer"

# Test query count
for layer_id in [0, 1, 2]:
    url = f"{base_url}/{layer_id}/query?where=1%3D1&returnCountOnly=true&f=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"Layer {layer_id} count: {data.get('count')}")
    except Exception as e:
        print(f"Error count {layer_id}: {e}")

# Check distinct voltages in Power Lines
url_v = f"{base_url}/2/query?where=1%3D1&outFields=CAPACITY_KV&returnDistinctValues=true&f=json"
req = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        data = json.loads(r.read().decode('utf-8'))
        voltages = [f['attributes']['CAPACITY_KV'] for f in data.get('features', []) if f['attributes']['CAPACITY_KV']]
        print("Voltages in Power Lines:", sorted(set(voltages)))
except Exception as e:
    print("Error voltages:", e)
