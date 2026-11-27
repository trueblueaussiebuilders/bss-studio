"""Rebuild assets/geo/lakes.json from Natural Earth (public domain) 10m lakes + the 10m Australia lakes supplement.

    curl -LO https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_lakes.geojson
    curl -LO https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_lakes_australia.geojson
    python3 tools/build_lakes.py ne_10m_lakes.geojson ne_10m_lakes_australia.geojson

Output: [{"n": name or "", "s": 1 if a salt lake else 0, "b": [lon0, lat0, lon1, lat1], "r": [[[lon, lat], ...], ...]}]
Only outer rings, rounded to 0.01 degrees (~1 km, finer than a close-up map can show), small lakes dropped.
"""
import json, sys


def rings(g):
    if g["type"] == "Polygon": return [g["coordinates"][0]]
    return [poly[0] for poly in g["coordinates"]]


def area(r):   # rough area in square degrees (shoelace)
    return abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r)))) / 2


def simplify(r, q=100):
    out = []
    for lo, la in r:
        p = [round(lo * q) / q, round(la * q) / q]
        if not out or p != out[-1]: out.append(p)
    return out if len(out) >= 4 else None


def main(world, au):
    out = []
    au_names = {f["properties"].get("name") for f in json.load(open(au))["features"]}
    for path, min_area in ((au, 0.002), (world, 0.03)):
        for f in json.load(open(path))["features"]:
            p = f["properties"]
            lo, la = rings(f["geometry"])[0][0]
            if path == world and 112 < lo < 155 and -45 < la < -9 and (not p.get("name") or p.get("name") in au_names):
                continue   # Australia comes from the more detailed supplement where it has the lake
            rs = [s for s in (simplify(r) for r in rings(f["geometry"]) if area(r) >= min_area) if s]
            if not rs: continue
            xs = [c[0] for r in rs for c in r]; ys = [c[1] for r in rs for c in r]
            out.append({"n": p.get("name") or "", "s": 1 if "Alkaline" in (p.get("featurecla") or "") else 0,
                        "b": [min(xs), min(ys), max(xs), max(ys)], "r": rs})
    json.dump(out, open("assets/geo/lakes.json", "w"), separators=(",", ":"))
    print(f"{len(out)} lakes, {sum(len(r) for l in out for r in l['r'])} points")


if __name__ == "__main__":
    main(*sys.argv[1:3])
