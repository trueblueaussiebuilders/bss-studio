"""Render the brand kit: profile pictures, story highlight covers and the pinned intro carousel.

  python -m brand.make --out brand/out
"""
import argparse, math, os
import cairo
from engine.style import *          # noqa: F401,F403
from engine import swan


def surface(w, h, bg):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s)
    rgba(c, bg); c.paint()
    return s, c


def profile(out):
    # Light: black swan on warm paper. Instagram crops to a circle, so the mark sits well inside it.
    s, c = surface(1080, 1080, PAPER)
    swan.draw(c, 150, 120, 780, body=NIGHT, beak=ACCENT, eye=PAPER)
    s.write_to_png(os.path.join(out, "profile_light.png"))
    s, c = surface(1080, 1080, NIGHT)
    swan.draw(c, 150, 120, 780, body=PAPER, beak=ACCENT, eye=NIGHT)
    s.write_to_png(os.path.join(out, "profile_dark.png"))


def highlight(out, name, glyph, label):
    s, c = surface(1080, 1920, NIGHT)
    cx, cy = 540, 960
    c.arc(cx, cy, 300, 0, 2 * math.pi); rgba(c, CARD); c.fill()
    c.arc(cx, cy, 300, 0, 2 * math.pi); rgba(c, ACCENT); c.set_line_width(6); c.stroke()
    if glyph == "swan":
        swan.draw(c, cx - 190, cy - 200, 380, body=INK, beak=ACCENT, eye=CARD)
    else:
        size = 300 if len(glyph) == 1 else 220
        font(c, SERIF, size); e = c.text_extents(glyph)
        text(c, glyph, cx - e.x_bearing - e.width / 2, cy - e.y_bearing - e.height / 2, SERIF, size, INK)
    text(c, label.upper(), cx, cy + 420, MONO, 40, MUTED, 1, align="center", tracking=0.2)
    s.write_to_png(os.path.join(out, f"highlight_{name}.png"))


def slide(out, n, kicker, title, body, foot=None):
    s, c = surface(1080, 1350, NIGHT)
    background(c, 0.0)
    swan.draw(c, 68, 70, 64, body=INK, beak=ACCENT, eye=NIGHT)
    text(c, "BLACK SWAN STOCKS", 146, 116, SANS_SEMI, 27, INK, 1, tracking=0.16)
    text(c, f"{n}/3", 1012, 116, MONO, 26, MUTED, 1, align="right")
    text(c, kicker.upper(), 72, 300, MONO, 28, ACCENT, 1, tracking=0.1)
    y = 400
    for ln in rich_lines(c, title, 100, 936):
        rich_draw_line(c, ln, 72, y, 100, INK, ACCENT); y += 108
    y += 40
    for para in body:
        for ln in wrap(c, para, SANS_MED, 42, 936):
            text(c, ln, 72, y, SANS_MED, 42, INK, 0.9); y += 58
        y += 26
    if foot:
        text(c, foot, 72, 1270, MONO, 24, MUTED, 1)
    s.write_to_png(os.path.join(out, f"pinned_{n}.png"))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="brand/out"); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    profile(a.out)
    for name, glyph, label in [("stocks", "W", "Speccies"), ("sunday", "S", "Sundays"), ("howto", "?", "How to read"),
                               ("fineprint", "§", "Fine print"), ("about", "swan", "About")]:
        highlight(a.out, name, glyph, label)
    slide(a.out, 1, "Welcome", "ASX speccies, *explained* in under a minute.",
          ["Every Monday, Wednesday and Friday we break down one speculative ASX miner: what it owns, "
           "where it is, the numbers, and what's coming up.",
           "Every Sunday: one big-picture topic that moves the whole sector, like gold prices, mining costs or China."],
          "Swipe for more")
    slide(a.out, 2, "How to read a breakdown", "Both sides, *every* time.",
          ["The project: what and where.", "The numbers: price, market cap, cash, resource.",
           "The catalysts: what's coming and when.", "The scorecard: what's going for it and against it.",
           "Figures come from ASX announcements and are dated on screen."], "Swipe for more")
    slide(a.out, 3, "The fine print", "Information, *not* advice.",
          ["Everything here is general information only. It doesn't consider your objectives, finances or needs, "
           "and it isn't a recommendation to buy or sell anything.",
           "Speculative stocks are high risk and can lose most or all of their value. We don't hold positions in "
           "companies we feature. Do your own research and consider a licensed adviser."])
    print("brand kit ->", a.out)


if __name__ == "__main__":
    main()
