"""Layout guard: render each scene's rest frame with a recorder on and flag what a viewer would see as broken.

  - content running into the subtitle zone (or, on the last scene, into the disclaimer card)
  - text or cards running off the edge of the screen
  - cards overlapping each other (map labels, drill-hole callouts, the locator inset)
  - text crossing a card's edge, or text sitting on top of other text

Used by `python -m engine.build ... --sheet` (prints LAYOUT lines) and `python3 tools/check.py --layout` (fails on them).
Pure rendering, no voice: it uses the saved timings if a full build has run, else the same word-count estimate as --sheet.
"""
import cairo
from engine import render, scenes, style
from engine.style import W, H, SUB_Y, SAFE_BOTTOM, SANS, X0, X1, SLOW, END_HOLD, wrap

SUB_LIMIT = SUB_Y - 15      # subtitle text tops out here when it runs to 3 lines
EDGE = 20                   # px from the screen edge that counts as off screen
MIN_OVERLAP = 6             # px; touching or anti-aliased edges don't count


def _record(spec, tl, idx, lt):
    """Draw scene idx at local time lt (seconds) and return the recorded boxes."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    env = render.env_for(spec)
    sc = dict(spec.SCENES[idx]); sc["_n"] = sum(1 for s in spec.SCENES[:idx + 1] if s["type"] not in ("hook", "outro"))
    style.LAYOUT = []
    try:
        scenes.RENDER[sc["type"]](ctx, sc, lt * SLOW, tl.durs[idx] * SLOW, env)
        return list(style.LAYOUT)
    finally:
        style.LAYOUT = None


def end_card_top(spec):
    ctx = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8))
    lines = wrap(ctx, render.env_for(spec)["disclaimer"], SANS, 27, X1 - X0 - 120)
    return SAFE_BOTTOM - (74 + len(lines) * 36)


def _inter(a, b):
    return max(0.0, min(a[3], b[3]) - max(a[1], b[1])), max(0.0, min(a[4], b[4]) - max(a[2], b[2]))


def _inside(a, b, tol=4):
    """a sits inside b (with a little tolerance)."""
    return a[1] >= b[1] - tol and a[2] >= b[2] - tol and a[3] <= b[3] + tol and a[4] <= b[4] + tol


def _name(b):
    lab = (b[5] or "").strip()
    return f"{b[0]} '{lab[:32]}'" if lab else b[0]


def problems(boxes, bottom, where=""):
    out = []
    for b in boxes:
        if b[4] > bottom + 2:
            out.append(f"{_name(b)} reaches y={b[4]:.0f}, into the {where or 'subtitle zone'} (limit {bottom:.0f})")
        if b[1] < EDGE or b[3] > W - EDGE:
            out.append(f"{_name(b)} runs off screen (x {b[1]:.0f} to {b[3]:.0f})")
    cards = [b for b in boxes if b[0] == "card"]
    texts = [b for b in boxes if b[0] == "text"]
    for i, a in enumerate(cards):
        for b in cards[i + 1:]:
            ix, iy = _inter(a, b)
            if ix > MIN_OVERLAP and iy > MIN_OVERLAP and not (_inside(a, b) or _inside(b, a)):
                out.append(f"cards overlap: {_name(a)} at ({a[1]:.0f},{a[2]:.0f}) and {_name(b)} at ({b[1]:.0f},{b[2]:.0f})")
    for t in texts:
        for c in cards:
            ix, iy = _inter(t, c)
            if ix > MIN_OVERLAP and iy > MIN_OVERLAP and not _inside(t, c):
                out.append(f"{_name(t)} crosses the edge of {_name(c)}")
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            ix, iy = _inter(a, b)
            if ix > 4 and iy > max(4, 0.25 * min(a[4] - a[2], b[4] - b[2])):
                out.append(f"text overlaps: {_name(a)} and {_name(b)}")
    seen, uniq = set(), []
    for p in out:
        if p not in seen: seen.add(p); uniq.append(p)
    return uniq


def check(spec, tl):
    """List of 'scene N (type): problem' strings; empty when the layout is clean."""
    issues = []
    last = len(spec.SCENES) - 1
    for i, (s, e) in enumerate(tl.scenes):
        D = e - s
        kind = spec.SCENES[i]["type"]
        if kind == "outro": continue
        for p in problems(_record(spec, tl, i, 0.85 * D), SUB_LIMIT):
            issues.append(f"scene {i} ({kind}): {p}")
        if i == last:
            spoken_end = tl.subs[i][-1][1] if tl.subs[i] else D - END_HOLD
            if D - spoken_end > 0.4:   # the disclaimer card is up by the final frame
                for p in problems(_record(spec, tl, i, D - 0.05), end_card_top(spec) - 12, "disclaimer card"):
                    msg = f"scene {i} ({kind}), final frame: {p}"
                    if msg.replace(", final frame", "") not in issues: issues.append(msg)
    return issues
