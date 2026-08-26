import urllib.request
import json

req = urllib.request.Request('https://services.ga.gov.au/gis/rest/services?f=json', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Root GA Services:")
        for s in data.get('services', []):
            print(f" - {s.get('name')} ({s.get('type')})")
        print("Folders:", data.get('folders', []))
except Exception as e:
    print("Error:", e)
