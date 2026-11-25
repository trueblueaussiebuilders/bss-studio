"""Tests for the fast hook: the optional `stat` count-up, the quicker first cut and the overseas locator inset.
Offline, no voice.

  python3 tools/test_hook.py
"""
import os, sys, types
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cairo
from engine import build, layout, scenes, geo, voice, render
from engine.style import W, H, SLOW, SUB_Y, fmt

TITLES = ["A *test* hook", "A shut *silver* mine keeps finding new veins",
          "A much longer *hook* title that will wrap onto three whole lines here"]
STAT = {"value": 1269, "suffix": " g/t", "caption": "silver equiv. over 1.7m"}
CHIPS = [{"label": "Resource", "value": 136, "suffix": " Moz AgEq"}, {"label": "Cash", "value": 70.5, "prefix": "~A$",
         "suffix": "m", "dp": 1}, {"label": "Plant", "text": "On site, idle"}]
VERSUS = {"type": "versus", "title": "Both *sides*", "for": {"points": ["One", "Two"]},
          "against": {"points": ["One", "Two"]}, "say": "The catch is short."}


def spec(hook):
    m = types.SimpleNamespace()
    m.META = {"kind": "stock", "date": "2026-11-25", "ticker": "TST", "company": "Test", "commodity": "silver"}
    m.SCENES = [hook, VERSUS]; m.CAPTION = ""
    return m


def check(name, cond, extra=""):
    print(("ok   " if cond else "FAIL ") + name + (f"  ({extra})" if extra and not cond else ""))
    return bool(cond)


def drawn_stat(hook, real_t):
    """The text the stat shows at real time real_t (records text boxes and reads the value back)."""
    from engine import style
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(surf)
    env = render.env_for(spec(hook))
    style.LAYOUT = []
    try:
        scenes.hook(ctx, dict(hook), real_t * SLOW, 4 * SLOW, env)
        return [b for b in style.LAYOUT if b[0] == "text" and b[-1].endswith(" g/t")]
    finally:
        style.LAYOUT = None


def main():
    ok = True
    for title in TITLES:
        for stat in (None, STAT):
            hook = {"type": "hook", "kicker": "ASX:TST  ·  Silver", "title": title, "chips": CHIPS,
                    "say": "A shut silver mine in Patagonia keeps finding new veins."}
            if stat: hook["stat"] = stat
            s = spec(hook)
            got = layout.check(s, build._guess_timeline(s))
            ok &= check(f"layout clean: {len(title)}-char title, stat={'yes' if stat else 'no'}", not got, got)
    hook = {"type": "hook", "kicker": "K", "title": TITLES[1], "chips": CHIPS, "stat": STAT, "say": "Hook."}
    early, landed = drawn_stat(hook, 0.5), drawn_stat(hook, 1.5)
    ok &= check("stat is counting up at 0.5s", early and early[0][-1] != fmt(1269, STAT), early)
    ok &= check("stat has landed on its value by 1.5s", landed and landed[0][-1] == fmt(1269, STAT), landed)
    # quicker first cut: guessed timings give the hook a short tail
    s = spec({"type": "hook", "title": "x", "say": "A shut silver mine in Patagonia keeps finding new veins."})
    tl = build._guess_timeline(s)
    ok &= check("hook ends ~0.45s after its line (guess)", tl.durs[0] < tl.subs[0][-1][1] + 0.5, tl.durs)
    ok &= check("voice.HOOK_GAP is short", 0.2 <= voice.HOOK_GAP <= 0.5)
    # locator inset: continent around overseas regions, Australia at home
    ok &= check("inset: Chile -> South America", geo.inset_region((-75.6, -48.6, -69.0, -44.6)) == geo.REGIONS["SOUTH_AMERICA"])
    ok &= check("inset: Nevada -> USA", geo.inset_region(geo.REGIONS["NEVADA"]) == geo.REGIONS["USA"])
    ok &= check("inset: Goldfields -> Australia", geo.inset_region(geo.REGIONS["GOLDFIELDS"]) == geo.REGIONS["AU"])
    # every video in videos/ still lays out cleanly
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos")
    for v in sorted(os.listdir(root)):
        sp = build.load_spec(os.path.join(root, v))
        got = layout.check(sp, build._guess_timeline(sp))
        ok &= check(f"{v} layout clean", not got, got)
    print("all passed" if ok else "FAILURES")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
