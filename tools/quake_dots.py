import json,urllib.request,sys
u="https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&orderby=time&limit=200&minmagnitude=4"
d=json.load(urllib.request.urlopen(u,timeout=30))
W,H=1000,500
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="background:#0e1116">']
for lon in range(-180,181,30): o.append(f'<line x1="{(lon+180)/360*W}" y1="0" x2="{(lon+180)/360*W}" y2="{H}" stroke="#222a35"/>')
for lat in range(-90,91,30): o.append(f'<line x1="0" y1="{(90-lat)/180*H}" x2="{W}" y2="{(90-lat)/180*H}" stroke="#222a35"/>')
for f in d['features']:
    lon,lat,dep=f['geometry']['coordinates'];m=f['properties']['mag'] or 0
    c="#f2c14e" if dep<=70 else "#e4572e" if dep<=300 else "#9b5de5"
    o.append(f'<circle cx="{(lon+180)/360*W:.1f}" cy="{(90-lat)/180*H:.1f}" r="{(m-3)**1.6*2.2:.1f}" fill="{c}" fill-opacity=".55"><title>M{m} {f["properties"]["place"]}, {dep} km</title></circle>')
o.append('</svg>')
open(sys.argv[1],'w').write("\n".join(o));print(len(d['features']),"events")
