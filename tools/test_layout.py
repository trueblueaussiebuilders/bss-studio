"""Tests for the layout guard (engine/layout.py). Offline, no voice.

  python3 tools/test_layout.py
"""
import os, sys, types
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import build, layout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = {"type": "hook", "kicker": "ASX:TST", "title": "A *test* video", "chips": [{"label": "Price", "text": "5c"}],
        "say": "A short hook line for the test."}
VERSUS = {"type": "versus", "title": "Both *sides*", "for": {"points": ["One", "Two", "Three"]},
          "against": {"points": ["One", "Two", "Three"]}, "say": "The catch is short."}


def spec(*scenes, **meta):
    m = types.SimpleNamespace()
    m.META = {"kind": "stock", "date": "2026-11-23", "ticker": "TST", "company": "Test", "commodity": "copper", **meta}
    m.SCENES = [HOOK, *scenes, VERSUS]
    m.CAPTION = ""
    return m


def issues(*scenes):
    s = spec(*scenes)
    return layout.check(s, build._guess_timeline(s))


def expect(name, got, needle):
    hit = [g for g in got if needle in g]
    print(("ok   " if hit else "FAIL ") + name + (f"  -> {hit[0]}" if hit else f"  (got {got})"))
    return bool(hit)


def main():
    ok = True
    say = "Some narration that runs for a few seconds so the scene settles."
    # 1. two drill holes whose intercepts sit at similar depths: the callout cards stack on each other
    ok &= expect("intercept callouts overlap", issues(
        {"type": "intercept", "title": "Holes", "say": say,
         "holes": [{"id": "A", "from": 191, "width": 12, "depth": 260, "headline": "12m @ 2.83% Cu"},
                   {"id": "B", "from": 170, "width": 20, "depth": 260, "headline": "20m @ 0.45% Cu"}]}), "cards overlap")
    # 2. a pin label that lands on the locator inset
    ok &= expect("map label under the inset", issues(
        {"type": "map", "title": "Map", "say": say, "region": [149.95, -24.0, 151.55, -22.75], "inset": True,
         "pins": [{"name": "Mt Chalmers", "sub": "Project", "lat": -23.29, "lon": 150.64, "kind": "project"},
                  {"name": "Gladstone", "sub": "Port", "lat": -23.84, "lon": 151.26, "kind": "town", "side": "left"}]}),
        "cards overlap")
    # 3. off-screen detection, and a long big-number sub line now wraps instead of running off both edges
    ok &= expect("off-screen box flagged", layout.problems([("text", -40, 900, 1100, 930, "wide")], layout.SUB_LIMIT),
                 "runs off screen")
    long_sub = issues(
        {"type": "big", "title": "Big", "say": say, "text": "16x", "caption": "A caption",
         "sub": "A very long source line that keeps on going well past the edge of a phone screen, about ninety characters"})
    print(("ok   " if not long_sub else "FAIL ") + "big sub wraps" + ("" if not long_sub else f"  (got {long_sub})"))
    ok &= not long_sub
    # 4. a catalysts scene with too much in it reaches the subtitles
    long_why = "A long explanation of why this matters that wraps onto a second line"
    ok &= expect("catalysts into subtitle zone", issues(
        {"type": "catalysts", "title": "What could *move* it", "say": say,
         "items": [{"when": f"Q{i} 2027", "title": f"A fairly long catalyst title number {i}", "why": long_why} for i in range(1, 6)]}),
        "subtitle zone")
    # 5. a clean scene has no issues
    clean = issues({"type": "stats", "title": "Numbers", "say": say,
                    "items": [{"label": "Cash", "value": 10.7, "prefix": "A$", "suffix": "m", "dp": 1},
                              {"label": "Price", "text": "5.2c"}]})
    print(("ok   " if not clean else "FAIL ") + "clean scene passes" + ("" if not clean else f"  (got {clean})"))
    ok &= not clean
    # 6. every video in videos/ is clean (older specs too: the engine fixes must not break them)
    for f in sorted(os.listdir(os.path.join(ROOT, "videos"))):
        s = build.load_spec(os.path.join(ROOT, "videos", f))
        got = layout.check(s, build._guess_timeline(s))
        print(("ok   " if not got else "FAIL ") + f"videos/{f}" + ("" if not got else f"  {got}"))
        ok &= not got
    print("ALL OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
