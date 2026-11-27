"""Lakes on maps: data loads, the right lakes show for close-up regions, labels clear pins and the inset, opt-out works.

    python3 tools/test_lakes.py
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cairo
from engine import geo, scenes, style, render, build

ok = True
def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg); ok = ok and cond

names = lambda bbox, md=0.0: {l["n"] for l in geo.lakes_in(bbox, md)}
check("Lake Lefroy" in names([120.7, -31.75, 122.25, -30.45]), "Lake Lefroy shows on a Kambalda close-up")
check("Lago Buenos Aires" in names([-75.6, -48.6, -69.0, -44.6]), "Lago Buenos Aires shows on the Cerro Bayo map")
check("Great Salt Lake" in names(geo.REGIONS["USA_WEST"]), "Great Salt Lake shows on USA_WEST")
check(len(geo.lakes_in(geo.REGIONS["AU"], (155 - 111.5) / 120)) < len(geo.lakes_in(geo.REGIONS["AU"])) / 2, "small lakes drop out on an Australia-wide view")
salt = {l["n"]: l["s"] for l in geo.lakes_in([120.7, -31.75, 122.25, -30.45])}
check(salt.get("Lake Lefroy") == 1, "Lake Lefroy is drawn as a salt lake")


def record(sc, t=9.0):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, style.W, style.H)
    ctx = cairo.Context(surf)
    env = render.env_for(build.load_spec("videos/2026-11-27-aar"))
    style.LAYOUT = []
    try:
        scenes.map_scene(ctx, dict(sc, _n=1), t, 12.0, env)
        return list(style.LAYOUT)
    finally:
        style.LAYOUT = None

base = {"type": "map", "label": "The project", "title": "Test", "region": [120.7, -31.75, 122.25, -30.45], "inset": True,
        "pins": [{"name": "Kambalda", "sub": "Town", "lat": -31.20, "lon": 121.66, "kind": "town", "side": "right"}], "say": "x"}
boxes = record(base)
texts = [b for b in boxes if b[0] == "text"]
lake_txt = [b for b in texts if "Lake" in str(b[-1])]
check(bool(lake_txt), "a lake name is drawn on the Goldfields close-up")
cards = [b for b in boxes if b[0] == "card"]
def hit(a, b): return a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]
check(not any(hit(t_, c) for t_ in lake_txt for c in cards), "lake names never sit on a pin card or the inset")
boxes = record(dict(base, lakes=False))
check(not any("Lake" in str(b[-1]) for b in boxes if b[0] == "text"), "lakes: False turns lakes and their names off")

# speed: the zoom from Australia must not slow rendering noticeably
spec = build.load_spec("videos/2026-11-27-aar")
tl = build._guess_timeline(spec)
t0 = tl.scenes[1][0]
s = time.time()
for k in range(10): render.draw_frame(spec, tl, t0 + 0.05 * k)
dt = (time.time() - s) / 10
check(dt < 0.5, f"map frames mid-zoom render in {dt * 1000:.0f} ms")

print("ALL PASS" if ok else "FAILED"); sys.exit(0 if ok else 1)
