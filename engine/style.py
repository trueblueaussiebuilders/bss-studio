"""Shared look: canvas, palette, fonts, easing and text helpers."""
import math, os, random
import cairo

W, H, FPS = 1080, 1920, 30

# Layout (Reels UI covers roughly the top 200px and the bottom 20%, plus a strip on the right)
X0, X1 = 72, 1008            # content edges
TITLE_Y = 330                # section label baseline; headline sits under it
ZONE = (72, 600, 936, 740)   # graphic zone x, y, w, h
SUB_Y = 1405                 # subtitle block top
SAFE_BOTTOM = 1530

def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

BG = hexrgb("#0B0B0C")
INK = hexrgb("#F3F0EA")        # warm white
MUTED = hexrgb("#8E8B85")
FAINT = hexrgb("#3A3A3D")
CARD = hexrgb("#141416")
LINE = hexrgb("#26262A")
ACCENT = hexrgb("#E5484D")     # the swan's beak
UP = hexrgb("#3DD68C")
DOWN = hexrgb("#F2555A")
PAPER = hexrgb("#F3F0EA")
NIGHT = hexrgb("#0B0B0C")

# Commodity -> (symbol, atomic number or "", display name, accent colour)
COMMODITIES = {
    "gold": ("Au", 79, "Gold", "#E2B84E"), "silver": ("Ag", 47, "Silver", "#C9CDD3"),
    "copper": ("Cu", 29, "Copper", "#D9824B"), "nickel": ("Ni", 28, "Nickel", "#9FB3A6"),
    "lithium": ("Li", 3, "Lithium", "#8FD3C6"), "uranium": ("U", 92, "Uranium", "#B8D94A"),
    "rare earths": ("REE", "", "Rare earths", "#A89BF2"), "graphite": ("C", 6, "Graphite", "#9AA0A8"),
    "tin": ("Sn", 50, "Tin", "#B7C0C9"), "tungsten": ("W", 74, "Tungsten", "#8EA6C8"),
    "antimony": ("Sb", 51, "Antimony", "#C2A6D9"), "vanadium": ("V", 23, "Vanadium", "#6FB6E8"),
    "zinc": ("Zn", 30, "Zinc", "#9CC0D9"), "iron ore": ("Fe", 26, "Iron ore", "#C8644A"),
    "manganese": ("Mn", 25, "Manganese", "#D98FB0"), "cobalt": ("Co", 27, "Cobalt", "#5B7FE0"),
    "mineral sands": ("Ti", 22, "Mineral sands", "#D9C59A"), "phosphate": ("P", 15, "Phosphate", "#E0A86B"),
    "potash": ("K", 19, "Potash", "#E07B9A"), "helium": ("He", 2, "Helium", "#7FD8F0"),
    "gallium": ("Ga", 31, "Gallium", "#9FD0B0"), "germanium": ("Ge", 32, "Germanium", "#B0B6C8"),
    "scandium": ("Sc", 21, "Scandium", "#A3C9A8"), "niobium": ("Nb", 41, "Niobium", "#7FA7C9"),
    "platinum": ("Pt", 78, "PGMs", "#D0D4DA"), "coal": ("C", 6, "Met coal", "#8A8A8A"),
    "oil and gas": ("CH₄", "", "Oil & gas", "#E3A04F"), "hydrogen": ("H", 1, "Hydrogen", "#8FC7F2"),
    "commodities": ("$", "", "Commodities", "#E5484D"),
}

def commodity(name):
    s, n, label, col = COMMODITIES.get((name or "").lower(), ("•", "", (name or "").title(), "#E5484D"))
    return s, n, label, hexrgb(col)


# Fonts (installed from assets/fonts by tools/install.sh)
SERIF, SERIF_IT = "BSS Serif", "BSS Serif Italic"
SANS, SANS_MED, SANS_SEMI, SANS_BOLD = "BSS Sans", "BSS Sans Medium", "BSS Sans Semi", "BSS Sans Bold"
MONO, MONO_BOLD = "BSS Mono", "BSS Mono Bold"


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def prog(t, start, dur): return clamp((t - start) / dur) if dur > 0 else float(t >= start)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in_out(x): x = clamp(x); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2
def ease_back(x, s=1.4): x = clamp(x); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2
def lerp(a, b, x): return a + (b - a) * x


# ---------- drawing helpers ----------
def rgba(ctx, col, a=1.0):
    ctx.set_source_rgba(col[0], col[1], col[2], a)

def font(ctx, face, size):
    ctx.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def width(ctx, s, face, size, tracking=0.0):
    font(ctx, face, size)
    return ctx.text_extents(s).x_advance + tracking * size * max(0, len(s) - 1)

def text(ctx, s, x, y, face, size, col=INK, a=1.0, align="left", tracking=0.0):
    """Draw text with its baseline at y. tracking is extra letter spacing in ems."""
    if a <= 0 or not s: return 0
    font(ctx, face, size)
    w = width(ctx, s, face, size, tracking)
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    rgba(ctx, col, a)
    if tracking:
        cx = x
        for ch in s:
            ctx.move_to(cx, y); ctx.show_text(ch); cx += ctx.text_extents(ch).x_advance + tracking * size
    else:
        ctx.move_to(x, y); ctx.show_text(s)
    return w

def wrap(ctx, s, face, size, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if width(ctx, trial, face, size) <= maxw or not cur: cur = trial
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()

def card(ctx, x, y, w, h, a=1.0, r=26, fill=CARD, stroke=LINE):
    rrect(ctx, x, y, w, h, r); rgba(ctx, fill, 0.92 * a); ctx.fill_preserve()
    rgba(ctx, stroke, a); ctx.set_line_width(2); ctx.stroke()


# ---------- rich headline: *word* = italic serif in the accent colour ----------
def _tokens(s):
    out, ital = [], False
    for part in s.split("*"):
        for w_ in part.split():
            out.append((w_, ital))
        ital = not ital
    return out

def rich_lines(ctx, s, size, maxw):
    toks, lines, cur, curw = _tokens(s), [], [], 0.0
    space = width(ctx, " ", SERIF, size)
    for w_, it in toks:
        ww = width(ctx, w_, SERIF_IT if it else SERIF, size)
        if cur and curw + space + ww > maxw:
            lines.append(cur); cur, curw = [], 0.0
        curw += (space if cur else 0) + ww; cur.append((w_, it, ww))
    if cur: lines.append(cur)
    return lines

def rich_draw_line(ctx, line, x, y, size, col=INK, accent=ACCENT, a=1.0, align="left"):
    space = width(ctx, " ", SERIF, size)
    total = sum(w_ for _, _, w_ in line) + space * (len(line) - 1)
    if align == "center": x -= total / 2
    for word, it, ww in line:
        text(ctx, word, x, y, SERIF_IT if it else SERIF, size, accent if it else col, a)
        x += ww + space
    return total

def reveal_lines(ctx, s, x, y, size, maxw, t, start=0.0, stagger=0.12, dur=0.7, lead=1.08, col=INK,
                 accent=ACCENT, align="left", a=1.0):
    """Serif headline whose lines slide up from behind a mask, one after another. Returns bottom y."""
    lines = rich_lines(ctx, s, size, maxw)
    lh = size * lead
    for i, ln in enumerate(lines):
        p = ease_out(prog(t, start + i * stagger, dur))
        if p <= 0: continue
        by = y + i * lh
        ctx.save()
        ctx.rectangle(0, by - size * 1.05, W, size * 1.38); ctx.clip()
        rich_draw_line(ctx, ln, x, by + (1 - p) * size * 1.1, size, col, accent, a, align)
        ctx.restore()
    return y + (len(lines) - 1) * lh


# ---------- number formatting ----------
def fmt(v, spec):
    """spec: dict(prefix, suffix, dp). v is a float."""
    dp = spec.get("dp", 0)
    s = f"{v:,.{dp}f}"
    return f"{spec.get('prefix', '')}{s}{spec.get('suffix', '')}"


# ---------- background ----------
_grain = []

def _make_grain(seed):
    rnd = random.Random(seed)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 270, 480)
    data = s.get_data()
    for i in range(0, len(data), 4):
        v = rnd.randint(0, 255)
        data[i] = data[i + 1] = data[i + 2] = v; data[i + 3] = 255
    s.mark_dirty()
    return s

def background(ctx, t, grid=True):
    rgba(ctx, BG); ctx.paint()
    g = cairo.RadialGradient(W * 0.5, H * 0.36, 60, W * 0.5, H * 0.45, H * 0.75)
    g.add_color_stop_rgba(0, 0.11, 0.11, 0.12, 1); g.add_color_stop_rgba(1, BG[0], BG[1], BG[2], 1)
    ctx.set_source(g); ctx.paint()
    if grid:
        ctx.set_line_width(1)
        rgba(ctx, INK, 0.028)
        for x in range(0, W + 1, 90):
            ctx.move_to(x + 0.5, 0); ctx.line_to(x + 0.5, H)
        for y in range(30, H, 90):
            ctx.move_to(0, y + 0.5); ctx.line_to(W, y + 0.5)
        ctx.stroke()
    if not _grain:
        _grain.extend(_make_grain(k) for k in range(4))
    ctx.save()
    ctx.scale(4, 4)
    ctx.set_source_surface(_grain[0], 0, 0)   # static grain: animated grain triples the file size
    ctx.get_source().set_filter(cairo.FILTER_NEAREST)
    ctx.paint_with_alpha(0.035)
    ctx.restore()
