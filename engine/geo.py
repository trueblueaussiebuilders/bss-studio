"""Country outlines (Natural Earth via world-atlas) and approximate Australian state borders."""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache = {}

REGIONS = {
    "AU": (111.5, -44.5, 155.0, -9.5),
    "WA": (112.0, -36.0, 130.0, -13.0),
    "WA_SOUTH": (113.0, -35.5, 127.0, -24.0),
    "GOLDFIELDS": (117.5, -33.5, 125.0, -26.0),
    "PILBARA": (114.0, -24.5, 123.5, -19.5),
    "QLD": (137.5, -29.5, 154.0, -10.0),
    "NSW_VIC": (140.5, -39.5, 154.0, -28.0),
    "SA_NT": (128.5, -38.5, 141.5, -10.5),
    "WORLD": (-170.0, -58.0, 190.0, 80.0),
    "CANADA": (-142.0, 41.0, -52.0, 72.0),
    "USA": (-126.0, 24.0, -66.0, 50.0),
    "USA_WEST": (-125.5, 30.5, -103.0, 49.5),
    "NEVADA": (-121.0, 34.5, -113.0, 42.5),
    "AFRICA": (-20.0, -36.0, 52.0, 38.0),
    "WEST_AFRICA": (-18.0, 3.0, 10.0, 18.0),
    "SOUTH_AMERICA": (-82.0, -56.0, -34.0, 13.0),
    "EUROPE": (-12.0, 35.0, 35.0, 71.0),
}

# State borders (lon, lat), straight-line approximations; good enough as faint context lines
AU_BORDERS = [
    [(129.0, -14.9), (129.0, -31.7)],                                   # WA | NT, SA
    [(129.0, -26.0), (138.0, -26.0)],                                   # NT | SA
    [(138.0, -16.6), (138.0, -26.0)],                                   # NT | QLD
    [(138.0, -26.0), (141.0, -26.0), (141.0, -29.0)],                   # SA | QLD, down to NSW
    [(141.0, -29.0), (148.9, -29.0), (150.3, -28.6), (151.4, -28.9), (152.0, -28.3), (153.55, -28.17)],  # QLD | NSW
    [(141.0, -29.0), (141.0, -38.06)],                                  # SA | NSW, VIC
    [(141.0, -34.0), (142.4, -34.7), (144.0, -35.6), (146.0, -35.9), (147.6, -36.0), (148.2, -36.8), (149.98, -37.5)],  # NSW | VIC
]


# Handy sub-national outlines (lon, lat) for the usual mining jurisdictions. Straight-line approximations.
AREAS = {
    "Nevada": [(-120.0, 42.0), (-114.04, 42.0), (-114.04, 36.2), (-114.63, 35.0), (-120.0, 39.0)],
    "Utah": [(-114.05, 42.0), (-111.05, 42.0), (-111.05, 41.0), (-109.05, 41.0), (-109.05, 37.0), (-114.05, 37.0)],
    "Idaho": [(-117.03, 49.0), (-116.05, 49.0), (-116.05, 47.98), (-114.3, 46.6), (-111.05, 44.5), (-111.05, 42.0),
              (-117.03, 42.0), (-117.03, 43.8), (-116.5, 45.6), (-117.03, 46.4)],
    "Arizona": [(-114.82, 37.0), (-109.05, 37.0), (-109.05, 31.33), (-111.07, 31.33), (-114.82, 32.5), (-114.6, 35.0), (-114.04, 36.2), (-114.05, 37.0)],
    "Quebec": [(-79.5, 47.0), (-79.5, 51.5), (-79.0, 54.5), (-77.0, 62.5), (-69.0, 59.0), (-64.5, 60.3), (-63.0, 52.0),
               (-57.1, 51.4), (-64.0, 50.2), (-66.5, 50.0), (-71.0, 46.8), (-70.0, 45.6), (-71.5, 45.0), (-74.7, 45.0)],
}


# Reference towns drawn faintly for context (name, lon, lat)
TOWNS = [
    ("Perth", 115.86, -31.95), ("Kalgoorlie", 121.47, -30.75), ("Leonora", 121.33, -28.88), ("Laverton", 122.40, -28.63),
    ("Meekatharra", 118.49, -26.59), ("Newman", 119.73, -23.36), ("Port Hedland", 118.60, -20.31),
    ("Karratha", 116.85, -20.74), ("Geraldton", 114.61, -28.78), ("Esperance", 121.89, -33.86), ("Norseman", 121.78, -32.20),
    ("Southern Cross", 119.33, -31.23), ("Mount Magnet", 117.85, -28.06), ("Broome", 122.24, -17.96), ("Kununurra", 128.74, -15.77),
    ("Darwin", 130.84, -12.46), ("Alice Springs", 133.88, -23.70), ("Tennant Creek", 134.19, -19.65), ("Mount Isa", 139.49, -20.73),
    ("Townsville", 146.82, -19.26), ("Cairns", 145.77, -16.92), ("Brisbane", 153.03, -27.47), ("Rockhampton", 150.51, -23.38),
    ("Charters Towers", 146.26, -20.08), ("Sydney", 151.21, -33.87), ("Orange", 149.10, -33.28), ("Broken Hill", 141.47, -31.95),
    ("Cobar", 145.83, -31.50), ("Melbourne", 144.96, -37.81), ("Bendigo", 144.28, -36.76), ("Ballarat", 143.85, -37.56),
    ("Adelaide", 138.60, -34.93), ("Roxby Downs", 136.89, -30.56), ("Port Augusta", 137.77, -32.49), ("Hobart", 147.33, -42.88),
    ("Reno", -119.81, 39.53), ("Elko", -115.76, 40.83), ("Las Vegas", -115.14, 36.17), ("Salt Lake City", -111.89, 40.76),
    ("Phoenix", -112.07, 33.45), ("Boise", -116.20, 43.62), ("Vancouver", -123.12, 49.28), ("Toronto", -79.38, 43.65),
    ("Timmins", -81.33, 48.48), ("Val-d'Or", -77.78, 48.10), ("Yellowknife", -114.37, 62.45), ("Accra", -0.19, 5.60),
    ("Bamako", -8.00, 12.64), ("Ouagadougou", -1.52, 12.37), ("Abidjan", -4.02, 5.35), ("Windhoek", 17.08, -22.56),
    ("Johannesburg", 28.05, -26.20), ("Dar es Salaam", 39.28, -6.79), ("Lima", -77.04, -12.05), ("Santiago", -70.67, -33.45),
    ("Antofagasta", -70.40, -23.65), ("Buenos Aires", -58.38, -34.60), ("Sao Paulo", -46.63, -23.55),
]


def _load(name):
    if name not in _cache:
        _cache[name] = json.load(open(os.path.join(ROOT, "assets", "geo", name)))
    return _cache[name]


def rings_in(bbox):
    """All country outer rings that intersect bbox, using the detailed set where we have it."""
    lo0, la0, lo1, la1 = bbox
    detail, coarse = _load("detail50.json"), _load("world110.json")
    world = bbox[2] - bbox[0] > 150
    out = []
    names = set(coarse) | set(detail)
    for n in names:
        rings = coarse.get(n) if world or n not in detail else detail[n]
        if rings is None: rings = detail[n]
        for r in rings:
            xs = [p[0] for p in r]; ys = [p[1] for p in r]
            if max(xs) < lo0 or min(xs) > lo1 or max(ys) < la0 or min(ys) > la1: continue
            if max(xs) - min(xs) > 300: continue   # slivers split at the antimeridian (e.g. Fiji) draw as a line across the map
            out.append((n, r))
    return out


class Projection:
    """Equirectangular with cos(lat) correction, fitted (centred) into a pixel rect."""
    def __init__(self, bbox, rect, pad=0.0):
        lo0, la0, lo1, la1 = bbox
        x, y, w, h = rect
        self.k = math.cos(math.radians((la0 + la1) / 2))
        bw, bh = (lo1 - lo0) * self.k, (la1 - la0)
        self.s = min((w - 2 * pad) / bw, (h - 2 * pad) / bh)
        self.cx, self.cy = x + w / 2, y + h / 2
        self.lo, self.la = (lo0 + lo1) / 2, (la0 + la1) / 2

    def __call__(self, lon, lat):
        return self.cx + (lon - self.lo) * self.k * self.s, self.cy - (lat - self.la) * self.s

    def km(self):
        """pixels per km"""
        return self.s / 111.0


def camera(a, b, e):
    """A Projection part-way (e in 0..1) on a smooth zoom from projection a to projection b.
    Scale moves geometrically; the centre moves so the destination stays steady in view (no swing)."""
    c = object.__new__(Projection)
    c.cx, c.cy = b.cx, b.cy
    c.k = a.k + (b.k - a.k) * e
    c.s = math.exp(math.log(a.s) + (math.log(b.s) - math.log(a.s)) * e)
    w = 1.0 if a.s == b.s else (1 / a.s - 1 / c.s) / (1 / a.s - 1 / b.s)
    c.lo, c.la = a.lo + (b.lo - a.lo) * w, a.la + (b.la - a.la) * w
    return c


def view_bbox(proj, rect):
    """The lon/lat box a projection shows inside a pixel rect."""
    x, y, w, h = rect
    lo0 = proj.lo + (x - proj.cx) / (proj.k * proj.s); lo1 = proj.lo + (x + w - proj.cx) / (proj.k * proj.s)
    la1 = proj.la + (proj.cy - y) / proj.s; la0 = proj.la + (proj.cy - y - h) / proj.s
    return (lo0, la0, lo1, la1)


ZOOM_PARENTS = ["USA", "CANADA", "AFRICA", "SOUTH_AMERICA", "EUROPE"]


def zoom_context(bbox, override=None):
    """Where a map scene's opening zoom starts: Australia for Australian regions, else the smallest
    continent-scale region around it. None when the region is already that wide (no zoom)."""
    if override is not None:
        ctx = resolve_region(override)
    else:
        lo0, la0, lo1, la1 = bbox
        cx, cy = (lo0 + lo1) / 2, (la0 + la1) / 2
        au = REGIONS["AU"]
        if au[0] <= cx <= au[2] and au[1] <= cy <= au[3]:
            ctx = au
        else:
            cands = [REGIONS[n] for n in ZOOM_PARENTS
                     if REGIONS[n][0] <= cx <= REGIONS[n][2] and REGIONS[n][1] <= cy <= REGIONS[n][3]]
            cands = [c for c in cands if (c[2] - c[0]) >= 2.5 * (lo1 - lo0)]
            if cands:
                ctx = min(cands, key=lambda c: (c[2] - c[0]) * (c[3] - c[1]))
            elif lo1 - lo0 > 15:
                return None                      # already continent-scale (USA, WORLD...): nothing to zoom from
            else:
                hw, hh = (lo1 - lo0) * 3, (la1 - la0) * 3
                ctx = (cx - hw, max(-85, cy - hh), cx + hw, min(85, cy + hh))
    if (ctx[2] - ctx[0]) < 2.0 * (bbox[2] - bbox[0]) and (ctx[3] - ctx[1]) < 2.0 * (bbox[3] - bbox[1]):
        return None
    return tuple(ctx)


def resolve_region(region):
    if isinstance(region, str): return REGIONS[region.upper()]
    return tuple(region)


def km_between(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    d = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(d))
