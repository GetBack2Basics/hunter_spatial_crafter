import urllib.request
import json

urls = [
    'https://services.ga.gov.au/gis/rest/services/National_Surface_Water_Information_System/MapServer?f=json',
    'https://services.ga.gov.au/gis/rest/services/Australian_Water_Resource_Assessment/MapServer?f=json',
    'https://services.ga.gov.au/gis/rest/services/National_Map_basemap/MapServer?f=json'
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"SUCCESS: {u}")
            for l in data.get('layers', []):
                print(f"   Layer ID {l.get('id')}: {l.get('name')}")
    except Exception as e:
        print(f"FAILED: {u} -> {e}")
