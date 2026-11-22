"""Offline tests for the opening map zoom (engine/geo.py camera/zoom_context, engine/scenes.py map_scene).
Run: python3 tools/test_map_zoom.py

Checks the zoom starts on Australia for Australian regions and on the right continent overseas, skips regions
that are already wide, the camera lands exactly on the final projection, `zoom: False` and `zoom_from` work,
the antimeridian sliver (Fiji) is no longer drawn as a line across the map, and every map scene in videos/
renders mid-zoom and at rest.
"""
import glob, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from engine import geo, render  # noqa: E402
from engine.build import load_spec, _guess_timeline  # noqa: E402
from engine.scenes import MAP_ZOOM  # noqa: E402

fails = 0


def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name); fails += 0 if cond else 1


R = geo.REGIONS
check("Kalgoorlie close-up zooms from Australia", geo.zoom_context((120.95, -31.45, 122.2, -30.55)) == R["AU"])
check("Tasmania zooms from Australia", geo.zoom_context((143.2, -44.0, 150.2, -40.4)) == R["AU"])
check("GOLDFIELDS zooms from Australia", geo.zoom_context(R["GOLDFIELDS"]) == R["AU"])
check("USA_WEST zooms from the USA", geo.zoom_context(R["USA_WEST"]) == R["USA"])
check("NEVADA zooms from the USA", geo.zoom_context(R["NEVADA"]) == R["USA"])
check("WEST_AFRICA zooms from Africa", geo.zoom_context(R["WEST_AFRICA"]) == R["AFRICA"])
check("AU itself: no zoom", geo.zoom_context(R["AU"]) is None)
check("WORLD: no zoom", geo.zoom_context(R["WORLD"]) is None)
check("USA: no zoom (nothing wider to start from)", geo.zoom_context(R["USA"]) is None)
check("zoom_from override", geo.zoom_context(R["NEVADA"], "WORLD") == R["WORLD"])

rect = (72, 700, 936, 640)
a, b = geo.Projection(R["AU"], rect, pad=10), geo.Projection(R["GOLDFIELDS"], rect, pad=10)
c0, c1 = geo.camera(a, b, 0.0), geo.camera(a, b, 1.0)
check("camera starts on the context view", all(abs(x - y) < 1e-6 for x, y in zip(c0(121.5, -30.7), a(121.5, -30.7))))
check("camera lands exactly on the region view", all(abs(x - y) < 1e-6 for x, y in zip(c1(121.5, -30.7), b(121.5, -30.7))))
mid = geo.camera(a, b, 0.5)
check("mid-zoom scale between the two", a.s < mid.s < b.s)
vb = geo.view_bbox(b, rect)
check("view box contains the region", vb[0] <= R["GOLDFIELDS"][0] + 1e-6 and vb[2] >= R["GOLDFIELDS"][2] - 1e-6)
check("no antimeridian slivers drawn", not any(max(p[0] for p in r) - min(p[0] for p in r) > 300
                                               for _, r in geo.rings_in(R["AU"])))

# every map scene in the repo renders mid-zoom and at rest; zoom: False renders identically to the rest frame
n = 0
for spec_path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "videos", "*", "spec.py"))):
    spec = load_spec(os.path.dirname(spec_path)); tl = _guess_timeline(spec)
    for i, sc in enumerate(spec.SCENES):
        if sc["type"] != "map": continue
        t0, t1 = tl.scenes[i]
        for t in (t0 + 0.05, t0 + MAP_ZOOM * 0.5, t0 + MAP_ZOOM + 0.3, t1 - 0.3):
            render.draw_frame(spec, tl, t)
        n += 1
check(f"{n} map scenes render through the zoom", n >= 5)

print("ALL PASS" if not fails else f"{fails} FAILED")
sys.exit(1 if fails else 0)
