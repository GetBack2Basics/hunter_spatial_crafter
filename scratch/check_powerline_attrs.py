import urllib.request
import json

base_url = "https://services.ga.gov.au/gis/rest/services/Electricity_Infrastructure/MapServer/2/query?where=1%3D1&outFields=*&resultRecordCount=10&f=json"
req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=5) as r:
    data = json.loads(r.read().decode('utf-8'))
    for f in data.get('features', []):
        print(f.get('attributes'))
