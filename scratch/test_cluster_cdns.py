import urllib.request

urls = [
    "https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js",
    "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css",
    "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css",
    "https://unpkg.com/esri-leaflet-cluster@3.0.1/dist/esri-leaflet-cluster.js"
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"SUCCESS: {u} -> Status {r.status}, Size {len(r.read())} bytes")
    except Exception as e:
        print(f"FAILED: {u} -> {e}")
