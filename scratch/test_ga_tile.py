import urllib.request

test_urls = [
    # WMS with layers='0,1,2'
    'https://services.ga.gov.au/gis/services/Electricity_Infrastructure/MapServer/WMSServer?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=-45,110,-10,155&CRS=EPSG:4326&WIDTH=800&HEIGHT=600&LAYERS=0,1,2&STYLES=&FORMAT=image/png&TRANSPARENT=TRUE',
    # ArcGIS REST export
    'https://services.ga.gov.au/gis/rest/services/Electricity_Infrastructure/MapServer/export?bbox=110,-45,155,-10&bboxSR=4326&imageSR=4326&size=800,600&f=image&transparent=true&layers=show:0,1,2'
]

for idx, u in enumerate(test_urls, 1):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
            ct = r.headers.get("Content-Type", "")
            print(f"Test #{idx}: Code {r.status}, Content-Type: {ct}, Size: {len(data)} bytes")
            if len(data) > 1000 and 'image' in ct:
                print(f"SUCCESS! Valid map image rendered ({len(data)} bytes)")
            else:
                print(f"Response snippet: {data[:200]}")
    except Exception as e:
        print(f"Error Test #{idx}: {e}")
