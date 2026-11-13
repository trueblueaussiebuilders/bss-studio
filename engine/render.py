"""Frame composition: background, persistent header, the current scene, subtitles. Plus the Reel cover."""
import math
import cairo
from engine.style import *          # noqa: F401,F403
from engine import scenes, swan

DEFAULT_DISCLAIMER = ("General information only, not financial advice. It doesn't consider your objectives or "
                      "situation. Speculative stocks are high risk and can lose most or all of their value. "
                      "We hold no position in this company. Do your own research.")


class Timeline:
    """Scene start/end times from the voice durations. subs[i] = [(start, end, sentence), ...] within scene i."""
    def __init__(self, durations, subs=None):
        self.durs = durations
        self.starts = [sum(durations[:i]) for i in range(len(durations))]
        self.scenes = [(s, s + d) for s, d in zip(self.starts, durations)]
        self.duration = sum(durations)
        self.subs = subs or [[] for _ in durations]

    def at(self, t):
        for i, (s, e) in enumerate(self.scenes):
            if t < e: return i, t - s
        return len(self.scenes) - 1, t - self.scenes[-1][0]


def env_for(spec):
    m = spec.META
    com = commodity(m.get("commodity"))
    return {"commodity": com, "accent": ACCENT, "meta": m,
            "disclaimer": m.get("disclaimer", DEFAULT_DISCLAIMER)}


def header(ctx, spec, tl, t, idx):
    m = spec.META
    swan.draw(ctx, X0 - 4, 112, 58, body=INK, beak=ACCENT, eye=BG)
    text(ctx, "BLACK SWAN STOCKS", X0 + 66, 154, SANS_SEMI, 25, INK, 1, tracking=0.16)
    chip = f"ASX:{m['ticker']}" if m.get("ticker") else m.get("chip", "SUNDAY BRIEF")
    w_ = width(ctx, chip, MONO_BOLD, 24) + 36
    rrect(ctx, X1 - w_, 120, w_, 48, 24); rgba(ctx, INK, 0.9); ctx.set_line_width(2); ctx.stroke()
    text(ctx, chip, X1 - w_ / 2, 152, MONO_BOLD, 24, INK, 1, align="center")
    # story-style progress segments
    n = len(tl.scenes); gap = 8; seg = (X1 - X0 - gap * (n - 1)) / n
    for i, (s, e) in enumerate(tl.scenes):
        x = X0 + i * (seg + gap)
        rrect(ctx, x, 196, seg, 4, 2); rgba(ctx, INK, 0.16); ctx.fill()
        f = clamp((t - s) / (e - s))
        if f > 0:
            rrect(ctx, x, 196, seg * f, 4, 2); rgba(ctx, INK, 0.85); ctx.fill()
    text(ctx, m.get("strap", "General information only · Not financial advice"), X0, 244, MONO, 20, MUTED, 1)
    asof = m.get("asof")
    if asof: text(ctx, asof, X1, 244, MONO, 20, MUTED, 1, align="right")


def subtitles(ctx, tl, idx, lt):
    for s, e, sent in tl.subs[idx]:
        if s - 0.05 <= lt < e + 0.25:
            break
    else:
        return
    a = ease_out(prog(lt, s - 0.05, 0.2)) * (1 - prog(lt, e + 0.1, 0.15))
    words = sent.split()
    f = clamp((lt - s) / max(0.3, e - s))
    lines = wrap(ctx, sent, SANS_MED, 40, 900)[:3]
    said = int(round(f * len(words) + 0.5))
    k = 0
    y0 = SUB_Y + 40 if len(lines) < 3 else SUB_Y + 10
    for li, ln in enumerate(lines):
        lw = width(ctx, ln, SANS_MED, 40)
        x = W / 2 - lw / 2
        for w_ in ln.split():
            text(ctx, w_, x, y0 + li * 52, SANS_MED, 40, INK, a * (1.0 if k < said else 0.34))
            x += width(ctx, w_ + " ", SANS_MED, 40); k += 1


def draw_frame(spec, tl, t):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    background(ctx, t)
    idx, lt = tl.at(t)
    env = env_for(spec)
    sc = dict(spec.SCENES[idx]); sc["_n"] = sum(1 for s in spec.SCENES[:idx + 1] if s["type"] not in ("hook", "outro"))
    D = tl.durs[idx]
    out = prog(lt, D - 0.26, 0.26) if idx < len(tl.scenes) - 1 else 0.0
    ctx.push_group()
    if out: ctx.translate(0, -28 * ease_in_out(out))
    scenes.RENDER[sc["type"]](ctx, sc, lt, D, env)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(1 - ease_in_out(out))
    header(ctx, spec, tl, t, idx)
    if spec.META.get("subtitles", True) and sc["type"] != "outro":
        subtitles(ctx, tl, idx, lt)
    return surf


def draw_cover(spec, tl=None):
    """Static Reel cover. The profile grid crops to the middle 3:4, so everything sits in y 260-1660."""
    m = spec.META
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    background(ctx, 0.0)
    env = env_for(spec)
    sym, num, name, col = env["commodity"]
    swan.draw(ctx, X0 - 4, 300, 64, body=INK, beak=ACCENT, eye=BG)
    text(ctx, "BLACK SWAN STOCKS", X0 + 72, 346, SANS_SEMI, 27, INK, 1, tracking=0.16)
    big_txt = m.get("ticker") or m.get("cover_word", "SUNDAY")
    size = 330 if len(big_txt) <= 3 else 250
    while width(ctx, big_txt, SERIF, size) > X1 - X0 and size > 120: size -= 10
    kick = f"ASX:{m['ticker']}  ·  {name.upper()}" if m.get("ticker") else name.upper()
    text(ctx, kick, X0, 520, MONO, 34, col, 1, tracking=0.08)
    text(ctx, big_txt, X0 - 6, 520 + size * 0.86, SERIF, size, INK, 1)
    y = 520 + size * 0.86 + 150
    lines = rich_lines(ctx, " ".join(m.get("cover", [])), 96, X1 - X0)
    for ln in lines[:3]:
        rich_draw_line(ctx, ln, X0, y, 96, INK, ACCENT)
        y += 104
    ty = max(y + 20, 1290)
    scenes.element_tile(ctx, X0, ty, 300, 99, env, start=0)
    if m.get("company"):
        text(ctx, m["company"], X0 + 340, ty + 70, SANS_SEMI, 44, INK, 1)
    rrect(ctx, X0 + 340, ty + 236, 330, 64, 32); rgba(ctx, ACCENT); ctx.fill()
    text(ctx, m.get("cover_tag", "THE BREAKDOWN" if m.get("ticker") else "SUNDAY BRIEF"), X0 + 340 + 165, ty + 279,
         MONO_BOLD, 26, INK, 1, align="center", tracking=0.06)
    return surf
