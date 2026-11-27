"""Scene renderers. Each takes (ctx, sc, t, D, env) where t is seconds into the scene and D its length.

Scene types: hook, map, stats, bars, timeline, versus, list, line, intercept, stack, big, outro.
"""
import math
import cairo
from engine.style import *          # noqa: F401,F403
from engine import geo, swan


# ---------------------------------------------------------------- shared heading
def heading(ctx, sc, t, env):
    """Section label + serif headline. Returns the y where the graphic zone can start."""
    idx = sc.get("_n", 1)
    a = ease_out(prog(t, 0.0, 0.4))
    label = sc.get("label", "").upper()
    if label:
        x = X0
        x += text(ctx, f"{idx:02d}", x, TITLE_Y, MONO, 24, env["accent"], a)
        text(ctx, "  /  " + label, x, TITLE_Y, MONO, 24, MUTED, a, tracking=0.06)
    bottom = TITLE_Y
    if sc.get("title"):
        bottom = reveal_lines(ctx, sc["title"], X0, TITLE_Y + 96, sc.get("title_size", 84), X1 - X0, t,
                              start=0.08, accent=env["accent"])
    return max(ZONE[1], bottom + 64)


def zone(top):
    return ZONE[0], top, ZONE[2], (ZONE[1] + ZONE[3]) - top


def value_of(item, p=1.0):
    if "text" in item: return item["text"]
    return fmt(item["value"] * p, item)


# ---------------------------------------------------------------- hook
def element_tile(ctx, x, y, s, t, env, start=0.3):
    sym, num, name, col = env["commodity"]
    p = ease_out(prog(t, start, 0.9))
    if p <= 0: return
    rrect(ctx, x, y, s, s, 30); rgba(ctx, CARD, 0.95 * p); ctx.fill()
    # border draws around the tile
    per = 4 * s
    ctx.set_dash([per * p, per]); rrect(ctx, x, y, s, s, 30); rgba(ctx, col, 0.9); ctx.set_line_width(3); ctx.stroke()
    ctx.set_dash([])
    q = ease_out(prog(t, start + 0.35, 0.7))
    text(ctx, str(num), x + 26, y + 52, MONO, 30, MUTED, q)
    sz = s * (0.48 if len(sym) <= 2 else 0.34)
    text(ctx, sym, x + s / 2, y + s * 0.64 + (1 - q) * 20, SERIF, sz, INK, q, align="center")
    text(ctx, name.upper(), x + s / 2, y + s - 30, MONO, 22, col, q, align="center", tracking=0.08)


HOOK_STAT_SIZE = 190   # serif size of the hook's headline number (shrinks to fit the width)


def hook_stat_size(ctx, st):
    size = HOOK_STAT_SIZE
    full = fmt(st["value"], st) if "value" in st else st.get("text", "")
    while width(ctx, full, SERIF, size) > X1 - X0 and size > 100: size -= 10
    return size


def hook(ctx, sc, t, D, env):
    """Opener. Everything lands fast (the first 1.5s decides the scroll): the kicker is up on frame one, the
    title slides in from t=0, and an optional `stat` (the hook's headline number) counts up in red."""
    a = ease_out(prog(t, 0.0, 0.25))
    text(ctx, sc.get("kicker", "").upper(), X0, 330, MONO, 26, env["accent"], max(0.35, a), tracking=0.08)
    bottom = reveal_lines(ctx, sc["title"], X0, 460, sc.get("title_size", 108), X1 - X0, t, start=0.0,
                          stagger=0.1, dur=0.6, accent=env["accent"])
    gy = max(800, bottom + 150)
    tile = 340
    st = sc.get("stat")
    if st:
        size = hook_stat_size(ctx, st)
        base = bottom + 64 + size * 0.78
        p = prog(t, 0.2, 0.9)                       # count-up lands at ~1.4s real time
        q = ease_out(prog(t, 0.15, 0.3))
        val = fmt(st["value"] * ease_out(p), st) if "value" in st else st.get("text", "")
        text(ctx, val, X0 - 4, base + (1 - q) * 30, SERIF, size, env["accent"], q)
        # underline sweeps across as the number lands, then the caption arrives
        u = ease_out(prog(t, 0.95, 0.45))
        if u > 0:
            full_w = width(ctx, fmt(st["value"], st) if "value" in st else st.get("text", ""), SERIF, size)
            rrect(ctx, X0, base + 22, full_w * u, 5, 2.5); rgba(ctx, env["accent"], 0.85); ctx.fill()
        if st.get("caption"):
            text(ctx, st["caption"].upper(), X0, base + 76, MONO, 24, MUTED, ease_out(prog(t, 1.05, 0.4)),
                 tracking=0.06)
        gy = base + (128 if st.get("caption") else 80)
        tile = int(min(340, max(300, 1370 - gy)))
    element_tile(ctx, X0, gy, tile, t, env, start=0.45 if st else 0.55)
    chips = sc.get("chips", [])[:3]
    cx, cw = X0 + tile + 32, X1 - (X0 + tile + 32)
    ch = (tile - 16 * (len(chips) - 1)) / max(1, len(chips))
    c0 = 0.6 if st else 0.8
    for i, c in enumerate(chips):
        p = ease_out(prog(t, c0 + i * 0.15, 0.6))
        if p <= 0: continue
        y = gy + i * (ch + 16) + (1 - p) * 30
        card(ctx, cx, y, cw, ch, p, r=22)
        text(ctx, c["label"].upper(), cx + 28, y + ch / 2 - 10, MONO, 21, MUTED, p, tracking=0.06)
        cp = ease_out(prog(t, c0 + 0.15 + i * 0.15, 0.9))
        text(ctx, value_of(c, cp), cx + 28, y + ch / 2 + 38, MONO_BOLD, 46 if tile >= 330 else 42, INK, p)


# ---------------------------------------------------------------- map
def _ring_path(ctx, ring, proj):
    for i, (lo, la) in enumerate(ring):
        x, y = proj(lo, la)
        (ctx.move_to if i == 0 else ctx.line_to)(x, y)
    ctx.close_path()


def _pin(ctx, x, y, col, p, t, pulse=True, big=True):
    if p <= 0: return
    ctx.new_path()
    r = (13 if big else 8) * ease_back(p)
    if pulse and p >= 1:
        for k in range(2):
            ph = ((t * 0.8) + k * 0.5) % 1.0
            ctx.arc(x, y, r + ph * 60, 0, 2 * math.pi); rgba(ctx, col, 0.45 * (1 - ph)); ctx.set_line_width(2); ctx.stroke()
    ctx.arc(x, y, r + 5, 0, 2 * math.pi); rgba(ctx, BG, 0.9 * p); ctx.fill()
    ctx.arc(x, y, r, 0, 2 * math.pi); rgba(ctx, col, p); ctx.fill()


def _pin_label_box(ctx, pn, x, y, zx, zw):
    """Where a pin's name card sits (x, y, w, h), matching the drawing code below."""
    kind = pn.get("kind", "project")
    side = pn.get("side", "right" if x < zx + zw * 0.62 else "left")
    size = 32 if kind == "project" else 26
    lw = max(width(ctx, pn["name"], SANS_SEMI, size), width(ctx, pn.get("sub", ""), MONO, 21)) + 36
    lh = 78 if pn.get("sub") else 54
    lx = x + 26 if side == "right" else x - 26 - lw
    return lx, y - lh / 2 + pn.get("dy", 0), lw, lh


def _lake_labels(ctx, lakes, proj, bbox, zone_, pins, inset_box, q):
    """Name the big lakes in faint serif italic, where the name fits inside the map and clears pins, cards and the inset."""
    if q <= 0: return []
    zx, zy, zw, zh = zone_
    avoid = []
    for pn in pins:
        x, y = proj(pn["lon"], pn["lat"])
        avoid.append((x - 24, y - 24, 48, 48))
        avoid.append(_pin_label_box(ctx, pn, x, y, zx, zw))
    if inset_box: avoid.append(inset_box)
    placed, out = 0, []
    for lk in sorted(lakes, key=lambda l: -((l["b"][2] - l["b"][0]) * (l["b"][3] - l["b"][1]))):
        if not lk["n"] or placed >= 3: continue
        ring = max(lk["r"], key=len)
        pts = [proj(lo, la) for lo, la in ring]
        xs = [p_[0] for p_ in pts]; ys = [p_[1] for p_ in pts]
        if max(xs) - min(xs) < 70 and max(ys) - min(ys) < 70: continue      # too small to name
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        name = lk["n"]
        w_ = width(ctx, name, SERIF_IT, 26)
        # on the lake when the name fits inside it, else below, above, right or left of it
        cands = [(cx - w_ / 2, cy - 20)] if w_ < max(xs) - min(xs) - 16 else []
        cands += [(cx - w_ / 2, max(ys) + 8), (cx - w_ / 2, min(ys) - 36), (max(xs) + 12, cy - 20), (min(xs) - 12 - w_, cy - 20)]
        box = None
        for bx, by in cands:
            b_ = (bx, by, w_, 28)
            if bx < zx + 8 or bx + w_ > zx + zw - 8 or by < zy + 50 or by + 28 > zy + zh - 50: continue
            if any(bx < a[0] + a[2] + 10 and a[0] < bx + w_ + 10 and by < a[1] + a[3] + 8 and a[1] < by + 36
                   for a in avoid): continue
            box = b_; break
        if not box: continue
        avoid.append(box); placed += 1; out.append(box)
        text(ctx, name, box[0], box[1] + 22, SERIF_IT, 26, MUTED, q)
    return out


MAP_ZOOM = 1.1   # scene-time units (x SLOW, ~1.4s real) for the opening Australia -> region zoom


def _inset_box(sc, zy, zh):
    """The locator inset's (x, y, w, h), or None when the map has no inset."""
    if sc.get("inset") and isinstance(sc.get("region"), (str, list)) and sc.get("region") not in ("AU", "WORLD"):
        return (X1 - 230, zy + zh - 200, 230, 200)
    return None


def map_scene(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    bbox = geo.resolve_region(sc.get("region", "AU"))
    rect = (zx, zy, zw, zh)
    final = geo.Projection(bbox, rect, pad=10)
    # opening zoom: start on Australia (or the continent around an overseas region) and ease into the region
    src = None if sc.get("zoom", True) is False else geo.zoom_context(bbox, sc.get("zoom_from"))
    e = 1.0
    if src:
        e = ease_in_out(prog(t, 0.1, MAP_ZOOM))
        proj = final if e >= 1 else geo.camera(geo.Projection(src, rect, pad=10), final, e)
        off = MAP_ZOOM - 0.6          # pins, links and labels arrive as the zoom lands (no dead frames)
    else:
        proj, off = final, 0.0
    tt = t - off
    view = geo.view_bbox(proj, rect) if e < 1 else bbox
    pins = sc.get("pins", [])
    focus = next((p for p in pins if p.get("kind", "project") == "project"), pins[0] if pins else None)
    fx, fy = final(focus["lon"], focus["lat"]) if focus else (zx + zw / 2, zy + zh / 2)
    # slow push-in around the project (after the zoom)
    z = 1 + 0.06 * ease_in_out(prog(t, off, D - off))
    ctx.push_group()
    ctx.save()
    ctx.rectangle(0, zy - 20, W, zh + 40); ctx.clip()
    ctx.translate(fx, fy); ctx.scale(z, z); ctx.translate(-fx, -fy)
    rp = ease_out(prog(t, 0.0, 0.6)) if src else ease_out(prog(t, 0.15, 1.3))
    ctx.save()
    rx, ry = proj(*((focus["lon"], focus["lat"]) if focus else (proj.lo, proj.la)))
    ctx.arc(rx, ry, 40 + rp * 1900, 0, 2 * math.pi); ctx.clip()
    rings = geo.rings_in(view)
    for name, ring in rings:
        _ring_path(ctx, ring, proj)
        hl = name in sc.get("highlight", ["Australia"])
        rgba(ctx, INK, 0.075 if hl else 0.035); ctx.fill_preserve()
        rgba(ctx, INK, 0.42 if hl else 0.16); ctx.set_line_width(2 if hl else 1.2); ctx.stroke()
    lakes = geo.lakes_in(view, min_deg=(view[2] - view[0]) / 120) if sc.get("lakes", True) else []
    for lk in lakes:
        for ring in lk["r"]:
            _ring_path(ctx, ring, proj)
            if lk["s"]:     # salt lake: a pale pan with a fine edge
                rgba(ctx, INK, 0.10); ctx.fill_preserve(); rgba(ctx, INK, 0.30); ctx.set_line_width(1.2); ctx.stroke()
            else:           # fresh water reads as sea
                rgba(ctx, BG, 1.0); ctx.fill_preserve(); rgba(ctx, INK, 0.30); ctx.set_line_width(1.2); ctx.stroke()
    if view[0] < 154 and view[2] > 112 and view[1] < -10 and view[3] > -44 and sc.get("states", True):
        ctx.save()
        for name, ring in rings:
            if name == "Australia": _ring_path(ctx, ring, proj)
        ctx.clip()
        ctx.set_dash([8, 8]); rgba(ctx, INK, 0.16); ctx.set_line_width(1.5)
        for line in geo.AU_BORDERS:
            for i, (lo, la) in enumerate(line):
                x, y = proj(lo, la); (ctx.move_to if i == 0 else ctx.line_to)(x, y)
            ctx.stroke()
        ctx.set_dash([])
        ctx.restore()
    if src and e < 1:
        q = ease_out(prog(t, 0.05, 0.35)) * (1 - prog(t, 0.1 + MAP_ZOOM * 0.7, MAP_ZOOM * 0.3))
        bx0, by0 = proj(bbox[0], bbox[3]); bx1, by1 = proj(bbox[2], bbox[1])
        ctx.rectangle(bx0, by0, bx1 - bx0, by1 - by0); rgba(ctx, env["accent"], 0.95 * q); ctx.set_line_width(3); ctx.stroke()
        if focus:
            px, py = proj(focus["lon"], focus["lat"])
            ctx.new_path(); ctx.arc(px, py, 7, 0, 2 * math.pi); rgba(ctx, env["accent"], q); ctx.fill()
    for k, an in enumerate(sc.get("areas", [])):
        poly = geo.AREAS.get(an)
        if not poly: continue
        q = ease_out(prog(tt, 0.5 + 0.15 * k, 0.8))
        _ring_path(ctx, poly, proj)
        rgba(ctx, env["accent"], 0.10 * q); ctx.fill_preserve()
        ctx.set_dash([10, 6]); rgba(ctx, env["accent"], 0.75 * q); ctx.set_line_width(2.5); ctx.stroke(); ctx.set_dash([])
        cx_ = sum(proj(*pt)[0] for pt in poly) / len(poly); cy_ = sum(proj(*pt)[1] for pt in poly) / len(poly)
        text(ctx, an.upper(), cx_, cy_ + 70, MONO, 24, env["accent"], q, align="center", tracking=0.2)
    ctx.restore()
    if sc.get("context", True):
        q = ease_out(prog(tt, 0.8, 0.8))
        taken = [proj(p_["lon"], p_["lat"]) for p_ in pins]
        inset_box = _inset_box(sc, zy, zh)
        lake_boxes = _lake_labels(ctx, lakes, final, bbox, (zx, zy, zw, zh), pins, inset_box, q)
        for nm, lo, la in geo.TOWNS:
            if not (bbox[0] < lo < bbox[2] and bbox[1] < la < bbox[3]): continue
            x, y = proj(lo, la)
            if any(abs(x - a) < 150 and abs(y - b) < 70 for a, b in taken): continue
            if inset_box and x + 10 + width(ctx, nm, MONO, 19) * 1.1 > inset_box[0] - 12 and y + 12 > inset_box[1] - 12:
                continue   # would sit under the locator inset
            tw = width(ctx, nm.upper(), MONO, 19) * 1.1
            if any(x - 6 < b[0] + b[2] and b[0] < x + 16 + tw and y - 14 < b[1] + b[3] and b[1] < y + 14 for b in lake_boxes):
                continue   # would sit on a lake name
            taken.append((x, y))
            ctx.new_path(); ctx.arc(x, y, 4, 0, 2 * math.pi); rgba(ctx, INK, 0.5 * q); ctx.fill()
            text(ctx, nm.upper(), x + 10, y + 7, MONO, 19, MUTED, q * 0.9, tracking=0.04)
    # links (distance lines)
    named = {p["name"]: p for p in pins}
    for i, ln in enumerate(sc.get("links", [])):
        a_, b_ = named.get(ln["from"]), named.get(ln["to"])
        if not a_ or not b_: continue
        p = ease_in_out(prog(tt, 1.4 + i * 0.3, 0.9))
        if p <= 0: continue
        x0, y0 = proj(a_["lon"], a_["lat"]); x1_, y1_ = proj(b_["lon"], b_["lat"])
        ctx.set_dash([10, 8]); rgba(ctx, INK, 0.7); ctx.set_line_width(2.5)
        ctx.move_to(x0, y0); ctx.line_to(lerp(x0, x1_, p), lerp(y0, y1_, p)); ctx.stroke(); ctx.set_dash([])
        lab = ln.get("label") or f"~{geo.km_between((a_['lon'], a_['lat']), (b_['lon'], b_['lat'])):,.0f} km"
        q = ease_out(prog(tt, 1.9 + i * 0.3, 0.5))
        mx, my = (x0 + x1_) / 2, (y0 + y1_) / 2
        w_ = width(ctx, lab, MONO_BOLD, 24) + 28
        rrect(ctx, mx - w_ / 2, my - 22, w_, 44, 22); rgba(ctx, INK, q); ctx.fill()
        if q > 0.5: layout_box(ctx, "card", mx - w_ / 2, my - 22, w_, 44, lab)
        text(ctx, lab, mx, my + 8, MONO_BOLD, 24, BG, q, align="center")
    # pins + labels
    for i, pn in enumerate(pins):
        kind = pn.get("kind", "project")
        col = env["accent"] if kind == "project" else (env["commodity"][3] if kind == "mine" else INK)
        st = 0.9 if kind == "project" else 1.2 + 0.15 * i
        p = ease_out(prog(tt, st, 0.5))
        x, y = proj(pn["lon"], pn["lat"])
        _pin(ctx, x, y, col, p, t, pulse=(kind == "project"), big=(kind == "project"))
        q = ease_out(prog(tt, st + 0.25, 0.5))
        if q <= 0: continue
        side = pn.get("side", "right" if x < zx + zw * 0.62 else "left")
        size = 32 if kind == "project" else 26
        lw = max(width(ctx, pn["name"], SANS_SEMI, size), width(ctx, pn.get("sub", ""), MONO, 21)) + 36
        lh = 78 if pn.get("sub") else 54
        lx = x + 26 if side == "right" else x - 26 - lw
        ly = y - lh / 2 + pn.get("dy", 0)
        card(ctx, lx + (1 - q) * (-14 if side == "right" else 14), ly, lw, lh, q, r=14,
             fill=CARD if kind != "project" else (0.17, 0.08, 0.09))
        text(ctx, pn["name"], lx + 18, ly + (36 if pn.get("sub") else 37), SANS_SEMI, size, INK, q)
        if pn.get("sub"): text(ctx, pn["sub"], lx + 18, ly + 64, MONO, 21, MUTED, q)
    ctx.restore()
    pat = ctx.pop_group()
    fade = cairo.LinearGradient(0, zy - 20, 0, zy + zh + 20)
    f0 = 70 / (zh + 40)
    fade.add_color_stop_rgba(0, 0, 0, 0, 0); fade.add_color_stop_rgba(f0, 0, 0, 0, 1)
    fade.add_color_stop_rgba(1 - f0, 0, 0, 0, 1); fade.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(pat); ctx.mask(fade)
    # locator inset
    if _inset_box(sc, zy, zh):
        q = ease_out(prog(tt, 0.6, 0.6))
        ix, iy, iw, ih = _inset_box(sc, zy, zh)
        card(ctx, ix, iy, iw, ih, q, r=18)
        ireg = geo.inset_region(bbox)
        ip = geo.Projection(ireg, (ix, iy, iw, ih), pad=16)
        for name, ring in geo.rings_in(ireg):
            if ireg == geo.REGIONS["AU"] and name != "Australia": continue
            _ring_path(ctx, ring, ip); rgba(ctx, INK, 0.25 * q); ctx.fill()
        bx0, by0 = ip(bbox[0], bbox[3]); bx1, by1 = ip(bbox[2], bbox[1])
        ctx.rectangle(bx0, by0, bx1 - bx0, by1 - by0); rgba(ctx, env["accent"], q); ctx.set_line_width(2.5); ctx.stroke()


# ---------------------------------------------------------------- stats grid
def stats(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    items = sc["items"][:6]
    cols = 2 if len(items) > 1 else 1
    rows = math.ceil(len(items) / cols)
    gap = 22
    cw = (zw - gap * (cols - 1)) / cols
    ch = min(280, (zh - gap * (rows - 1)) / rows)
    oy = zy + max(0, (zh - (rows * ch + gap * (rows - 1))) * 0.4)
    for i, it in enumerate(items):
        r_, c_ = divmod(i, cols)
        x, y = zx + c_ * (cw + gap), oy + r_ * (ch + gap)
        p = ease_out(prog(t, 0.45 + i * 0.16, 0.6))
        if p <= 0: continue
        y += (1 - p) * 40
        card(ctx, x, y, cw, ch, p)
        text(ctx, it["label"].upper(), x + 32, y + 60, MONO, 24, MUTED, p, tracking=0.06)
        cp = ease_out(prog(t, 0.6 + i * 0.16, 1.1))
        v = value_of(it, cp)
        size = 84
        while width(ctx, v, MONO_BOLD, size) > cw - 64 and size > 34: size -= 2
        text(ctx, v, x + 32, y + ch * 0.62, MONO_BOLD, size, env["accent"] if it.get("highlight") else INK, p)
        if it.get("note"):
            text(ctx, it["note"], x + 32, y + ch - 32, SANS, 26, MUTED, p)


# ---------------------------------------------------------------- horizontal bars
def bars(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    items = sc["bars"][:6]
    spec = sc.get("fmt", {})
    note_h = (50 if sc.get("note") else 0) + (260 if sc.get("callout") else 0)
    rh = min(190, (zh - note_h) / len(items))
    vmax = max(b["value"] for b in items) or 1
    maxw = zw * 0.66
    oy = zy + max(0, (zh - note_h - rh * len(items)) * 0.4)
    for i, b in enumerate(items):
        y = oy + i * rh
        p = ease_out(prog(t, 0.45 + i * 0.18, 0.5))
        if p <= 0: continue
        hl = b.get("highlight")
        text(ctx, b["label"], zx, y + 40, SANS_SEMI if hl else SANS_MED, 36, INK if hl else MUTED, p)
        gp = ease_in_out(prog(t, 0.6 + i * 0.18, 1.0))
        bw = max(8, maxw * b["value"] / vmax * gp)
        rrect(ctx, zx, y + 62, bw, 64, 14)
        rgba(ctx, env["accent"] if hl else FAINT, p); ctx.fill()
        text(ctx, fmt(b["value"] * gp, {**spec, **b.get("fmt", {})}) + (b.get("tag", "") and "  " + b["tag"]),
             zx + bw + 22, y + 108, MONO_BOLD, 40, INK if hl else MUTED, p)
    co = sc.get("callout")
    if co:
        q = ease_out(prog(t, 0.6 + len(items) * 0.18 + 0.8, 0.7))
        cy_ = oy + rh * len(items) + 40
        rgba(ctx, LINE, q); ctx.set_line_width(2); ctx.move_to(zx, cy_); ctx.line_to(zx + zw * q, cy_); ctx.stroke()
        text(ctx, co["text"], zx, cy_ + 170 + (1 - q) * 30, SERIF, 190, env["accent"], q)
        cw_ = width(ctx, co["text"], SERIF, 190) + 36
        for k, ln in enumerate(wrap(ctx, co.get("caption", ""), SANS_MED, 36, zw - cw_)[:3]):
            text(ctx, ln, zx + cw_, cy_ + 90 + k * 46, SANS_MED, 36, INK, q)
    if sc.get("note"):
        q = ease_out(prog(t, 1.2, 0.6))
        for k, ln in enumerate(wrap(ctx, sc["note"], SANS, 24, zw)[:2]):
            text(ctx, ln, zx, zy + zh - 30 + k * 30 - (30 if len(wrap(ctx, sc["note"], SANS, 24, zw)) > 1 else 0), SANS, 24, MUTED, q)


# ---------------------------------------------------------------- timeline
def timeline(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    ev = sc["events"][:5]
    n = len(ev)
    step = min(200, (zh - 40) / n)
    lx = zx + 26
    spread = max(0.5, min(0.55 * D, 4.0)) / n
    lp = ease_in_out(prog(t, 0.35, spread * n + 0.4))
    rgba(ctx, FAINT); ctx.set_line_width(3)
    ctx.move_to(lx, zy + 18); ctx.line_to(lx, zy + 18 + (step * (n - 1) + 10) * lp); ctx.stroke()
    for i, e in enumerate(ev):
        y = zy + 18 + i * step
        p = ease_out(prog(t, 0.45 + i * spread, 0.5))
        if p <= 0: continue
        done = e.get("done", False)
        ctx.new_path()
        if done:
            ctx.arc(lx, y, 13 * ease_back(p), 0, 2 * math.pi); rgba(ctx, MUTED, p); ctx.fill()
            rgba(ctx, BG, p); ctx.set_line_width(3)
            ctx.move_to(lx - 6, y); ctx.line_to(lx - 1, y + 5); ctx.line_to(lx + 7, y - 5); ctx.stroke()
        else:
            ph = (t * 0.9) % 1
            ctx.new_path(); ctx.arc(lx, y, 13 + ph * 18, 0, 2 * math.pi); rgba(ctx, env["accent"], 0.5 * (1 - ph) * p); ctx.set_line_width(2); ctx.stroke()
            ctx.arc(lx, y, 13 * ease_back(p), 0, 2 * math.pi); rgba(ctx, BG, p); ctx.fill_preserve()
            rgba(ctx, env["accent"], p); ctx.set_line_width(4); ctx.stroke()
        tx = lx + 46 + (1 - p) * 20
        text(ctx, e["when"].upper(), tx, y + 10, MONO, 27, env["accent"] if not done else MUTED, p, tracking=0.05)
        for k, ln in enumerate(wrap(ctx, e["text"], SANS_MED, 40, zw - 90)[:2]):
            text(ctx, ln, tx, y + 64 + k * 48, SANS_MED, 40, INK if not done else MUTED, p)


# ---------------------------------------------------------------- catalysts (what's coming and why it matters)
def catalysts(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    items = sc["items"][:4]
    n = len(items)
    gap = 20
    blocks = []
    for it in items:
        why = wrap(ctx, it.get("why", ""), SANS, 34, zw - 120)[:2]
        title = wrap(ctx, it["title"], SANS_SEMI, 42, zw - 120)[:2]
        blocks.append((title, why, 78 + len(title) * 50 + len(why) * 44 + 16))
    total = sum(b[2] for b in blocks) + gap * (n - 1)
    y = zy + max(0, (zh - total) * 0.35)
    spread = max(0.6, D * 0.62 / n)
    for i, (it, (title, why, h)) in enumerate(zip(items, blocks)):
        st = 0.45 + i * spread
        p = ease_out(prog(t, st, 0.6))
        if p > 0:
            active = i == n - 1 or t < 0.45 + (i + 1) * spread
            yy = y + (1 - p) * 36
            rrect(ctx, zx, yy, zw, h, 24); rgba(ctx, CARD, 0.92 * p); ctx.fill_preserve()
            rgba(ctx, env["accent"] if active else LINE, p); ctx.set_line_width(3 if active else 2); ctx.stroke()
            text(ctx, f"{i + 1}", zx + 40, yy + 74, SERIF, 64, env["accent"] if active else MUTED, p, align="center")
            tx = zx + 90
            text(ctx, it.get("when", "").upper(), tx, yy + 44, MONO, 24, env["accent"], p, tracking=0.06)
            if it.get("status"):
                sw = width(ctx, it["status"].upper(), MONO, 20, 0.06) + 28
                rrect(ctx, zx + zw - sw - 24, yy + 20, sw, 36, 18); rgba(ctx, INK, 0.12 * p); ctx.fill()
                text(ctx, it["status"].upper(), zx + zw - sw / 2 - 24, yy + 45, MONO, 20, INK, p, align="center", tracking=0.06)
            for k, ln in enumerate(title):
                text(ctx, ln, tx, yy + 100 + k * 50, SANS_SEMI, 42, INK, p)
            q = ease_out(prog(t, st + 0.35, 0.6))
            wy = yy + 100 + len(title) * 50 + 6
            for k, ln in enumerate(why):
                text(ctx, ln, tx, wy + k * 44, SANS, 34, MUTED, q)
        y += h + gap


# ---------------------------------------------------------------- versus (two stacked cards)
def _bullet_h(ctx, w, pts, lh=48, gap=26):
    return 112 + sum(len(wrap(ctx, s, SANS_MED, 38, w - 120)) * lh + gap for s in pts) + 14


def _bullet_card(ctx, x, y, w, title, pts, col, glyph, t, start, spread, lh=48, gap=26):
    p = ease_out(prog(t, start, 0.5))
    if p <= 0: return 0
    lines = [wrap(ctx, s, SANS_MED, 38, w - 120) for s in pts]
    h = 112 + sum(len(l) * lh + gap for l in lines) + 14
    card(ctx, x, y, w, h, p)
    # glyph
    gx, gy = x + 46, y + 52
    ctx.move_to(gx - 12, gy + (8 if glyph == "up" else -8)); ctx.line_to(gx + 12, gy + (8 if glyph == "up" else -8))
    ctx.line_to(gx, gy + (-12 if glyph == "up" else 12)); ctx.close_path(); rgba(ctx, col, p); ctx.fill()
    text(ctx, title.upper(), x + 76, y + 64, MONO, 28, col, p, tracking=0.08)
    yy = y + 128
    for i, ls in enumerate(lines):
        q = ease_out(prog(t, start + 0.25 + i * spread, 0.5))
        for k, ln in enumerate(ls):
            text(ctx, ln, x + 76 + (1 - q) * 16, yy + k * lh, SANS_MED, 38, INK, q)
        ctx.new_path(); ctx.arc(x + 48, yy - 12, 5, 0, 2 * math.pi); rgba(ctx, col, q); ctx.fill()
        yy += len(ls) * lh + gap
    return h


def versus(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    a, b = sc["for"], sc["against"]
    spread = max(0.35, (D * 0.42) / max(1, len(a["points"]) + len(b["points"])))
    # versus is the last scene, so both cards must clear the disclaimer card that rises at the end:
    # tighten the bullet spacing step by step until they fit (most videos need one small step)
    limit = SAFE_BOTTOM - (74 + len(wrap(ctx, env.get("disclaimer", ""), SANS, 27, X1 - X0 - 120)) * 36) - 16
    lh, gap, between = 48, 26, 24
    while zy + _bullet_h(ctx, zw, a["points"], lh, gap) + between + _bullet_h(ctx, zw, b["points"], lh, gap) > limit and lh > 42:
        lh, gap, between = lh - 1, max(14, gap - 2), max(16, between - 1)
    h1 = _bullet_card(ctx, zx, zy, zw, a.get("title", "Going for it"), a["points"], UP, "up", t, 0.4, spread, lh, gap)
    st2 = 0.4 + 0.3 + spread * len(a["points"])
    if h1 == 0: return
    _bullet_card(ctx, zx, zy + h1 + between, zw, b.get("title", "Working against it"), b["points"], DOWN, "down", t, st2, spread, lh, gap)


# ---------------------------------------------------------------- numbered list
def listing(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    items = sc["items"][:5]
    spread = max(0.35, (D * 0.5) / len(items))
    y = zy
    for i, it in enumerate(items):
        p = ease_out(prog(t, 0.45 + i * spread, 0.5))
        lines = wrap(ctx, it, SANS_MED, 40, zw - 110)
        h = len(lines) * 50 + 50
        if p > 0:
            text(ctx, f"{i + 1:02d}", zx, y + 44, MONO_BOLD, 30, env["accent"], p)
            for k, ln in enumerate(lines):
                text(ctx, ln, zx + 90 + (1 - p) * 20, y + 46 + k * 50, SANS_MED, 40, INK, p)
            rgba(ctx, LINE, p); ctx.set_line_width(2)
            ctx.move_to(zx, y + h - 6); ctx.line_to(zx + zw * ease_out(prog(t, 0.5 + i * spread, 0.8)), y + h - 6); ctx.stroke()
        y += h + 10


# ---------------------------------------------------------------- line chart
def line(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    ser = sc["series"]
    spec = sc.get("fmt", {})
    ys = [v for _, v in ser]
    lo, hi = min(ys), max(ys)
    pad = (hi - lo) * 0.12 or abs(hi) * 0.1 or 1
    lo, hi = sc.get("ymin", lo - pad), sc.get("ymax", hi + pad)
    cx, cy, cw, chh = zx, zy + 20, zw - 150, zh - 90
    X = lambda i: cx + cw * i / (len(ser) - 1)
    Y = lambda v: cy + chh * (1 - (v - lo) / (hi - lo))
    a = ease_out(prog(t, 0.2, 0.5))
    for k in range(4):
        gv = lo + (hi - lo) * k / 3
        gy = Y(gv)
        rgba(ctx, INK, 0.07 * a); ctx.set_line_width(1); ctx.move_to(cx, gy); ctx.line_to(cx + cw, gy); ctx.stroke()
        text(ctx, fmt(gv, spec), cx + cw + 16, gy + 8, MONO, 21, MUTED, a)
    for i in sorted({0, len(ser) // 2, len(ser) - 1}):
        text(ctx, str(ser[i][0]), X(i), cy + chh + 46, MONO, 22, MUTED, a,
             align="left" if i == 0 else "right" if i == len(ser) - 1 else "center")
    p = ease_in_out(prog(t, 0.5, min(2.6, D * 0.55)))
    col = env["commodity"][3] if sc.get("color") == "commodity" else env["accent"]
    pts = [(X(i), Y(v)) for i, (_, v) in enumerate(ser)]
    xr = cx + cw * p
    ctx.save(); ctx.rectangle(cx - 10, cy - 40, cw * p + 12, chh + 80); ctx.clip()
    ctx.move_to(*pts[0])
    for q in pts[1:]: ctx.line_to(*q)
    ctx.line_to(pts[-1][0], cy + chh); ctx.line_to(pts[0][0], cy + chh); ctx.close_path()
    g = cairo.LinearGradient(0, cy, 0, cy + chh)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], 0.28); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(g); ctx.fill()
    ctx.move_to(*pts[0])
    for q in pts[1:]: ctx.line_to(*q)
    rgba(ctx, col, 0.25); ctx.set_line_width(12); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    rgba(ctx, col); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()
    # moving head + value
    fi = p * (len(ser) - 1); i0 = min(int(fi), len(ser) - 2); fr = fi - i0
    hx, hy = lerp(pts[i0][0], pts[i0 + 1][0], fr), lerp(pts[i0][1], pts[i0 + 1][1], fr)
    hv = lerp(ser[i0][1], ser[i0 + 1][1], fr)
    if p > 0:
        ctx.new_path(); ctx.arc(hx, hy, 10, 0, 2 * math.pi); rgba(ctx, INK); ctx.fill()
        lab = fmt(hv, spec); w_ = width(ctx, lab, MONO_BOLD, 28) + 28
        bx = min(hx + 18, cx + cw + 150 - w_); by = hy - 66
        rrect(ctx, bx, by, w_, 46, 23); rgba(ctx, INK); ctx.fill()
        text(ctx, lab, bx + 14, by + 32, MONO_BOLD, 28, BG)
    for k, an in enumerate(sc.get("annotations", [])):
        i = an["at"]
        if i / (len(ser) - 1) > p + 1e-6: continue
        q = ease_out(prog(t, 0.6 + (i / (len(ser) - 1)) * min(2.6, D * 0.55), 0.5))
        ax, ay = pts[i]
        up = an.get("above", True)
        ly = ay - 110 if up else ay + 110
        rgba(ctx, INK, 0.5 * q); ctx.set_line_width(1.5); ctx.move_to(ax, ay); ctx.line_to(ax, ly + (24 if up else -24)); ctx.stroke()
        ctx.new_path(); ctx.arc(ax, ay, 7, 0, 2 * math.pi); rgba(ctx, col, q); ctx.fill()
        tw = width(ctx, an["text"], SANS_SEMI, 26) + 28
        tx = clamp(ax - tw / 2, cx, cx + cw + 140 - tw)
        card(ctx, tx, ly - 22, tw, 46, q, r=12)
        text(ctx, an["text"], tx + 14, ly + 10, SANS_SEMI, 26, INK, q)
    if sc.get("note"):
        text(ctx, sc["note"], zx, zy + zh + 10, SANS, 22, MUTED, a)


# ---------------------------------------------------------------- drill intercept
def intercept(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    holes = sc["holes"][:2]
    col = env["commodity"][3]
    gy = zy + 90
    a = ease_out(prog(t, 0.2, 0.6))
    # ground layers
    bands = [(0.0, 0.10, 0.055), (0.10, 0.32, 0.035), (0.32, 1.0, 0.05)]
    for b0, b1, al in bands:
        ctx.rectangle(zx, gy + (zh - 90) * b0, zw, (zh - 90) * (b1 - b0)); rgba(ctx, INK, al * a); ctx.fill()
    ctx.save(); ctx.rectangle(zx, gy, zw, zh - 90); ctx.clip()
    rgba(ctx, INK, 0.05 * a); ctx.set_line_width(1.5)
    for k in range(-20, 40):
        x = zx + k * 46
        ctx.move_to(x, gy + (zh - 90) * 0.32); ctx.line_to(x + 400, gy + zh); ctx.stroke()
    ctx.restore()
    rgba(ctx, INK, 0.6 * a); ctx.set_line_width(2.5); ctx.move_to(zx, gy); ctx.line_to(zx + zw, gy); ctx.stroke()
    text(ctx, "SURFACE", zx + zw, gy - 14, MONO, 20, MUTED, a, align="right")
    dmax = max(h["depth"] for h in holes)
    ang = math.radians(sc.get("dip", 72))
    L = (zh - 120) / math.sin(ang)
    pxm = L / dmax
    for j, h in enumerate(holes):
        x0 = zx + 120 + j * 170
        st = 0.5 + j * 0.6
        dp = ease_in_out(prog(t, st, 1.6))
        if dp <= 0: continue
        # rig
        rgba(ctx, INK, 0.9); ctx.set_line_width(4)
        ctx.move_to(x0 - 24, gy); ctx.line_to(x0, gy - 64); ctx.line_to(x0 + 24, gy); ctx.stroke()
        text(ctx, h.get("id", ""), x0, gy - 78, MONO, 20, MUTED, 1, align="center")
        dx, dy = math.cos(ang) * pxm, math.sin(ang) * pxm
        d = h["depth"] * dp
        rgba(ctx, INK, 0.75); ctx.set_line_width(5); ctx.move_to(x0, gy); ctx.line_to(x0 + dx * d, gy + dy * d); ctx.stroke()
        f0, f1 = h["from"], h["from"] + h["width"]
        if d > f0:
            e = min(d, f1)
            for lw, al in ((40, 0.15), (24, 0.35), (13, 1.0)):
                rgba(ctx, col, al); ctx.set_line_width(lw); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                ctx.move_to(x0 + dx * f0, gy + dy * f0); ctx.line_to(x0 + dx * e, gy + dy * e); ctx.stroke()
            ctx.set_line_cap(cairo.LINE_CAP_BUTT)
            q = ease_out(prog(t, st + 1.6 * (f1 / h["depth"]) + 0.1, 0.6))
            mx, my = x0 + dx * (f0 + f1) / 2, gy + dy * (f0 + f1) / 2
            big = h["headline"]
            sub = h.get("sub", f"from {f0:g}m")
            lw_ = max(width(ctx, big, SERIF, 66), width(ctx, sub, MONO, 24)) + 48
            lx = X1 - lw_; ly = my - 64
            rgba(ctx, INK, 0.55 * q); ctx.set_line_width(2); ctx.move_to(mx + 18, my); ctx.line_to(lerp(mx + 18, lx, q), my); ctx.stroke()
            card(ctx, lx, ly, lw_, 128, q, r=18)
            text(ctx, big, lx + 24, ly + 70, SERIF, 66, INK, q)
            text(ctx, sub, lx + 24, ly + 106, MONO, 24, col, q)
    if sc.get("note"):
        text(ctx, sc["note"], zx, zy + zh + 6, SANS, 22, MUTED, a)


# ---------------------------------------------------------------- cost stack vs price
def stack(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    items, price, spec = sc["items"], sc["price"], sc.get("fmt", {})
    total = sum(i["value"] for i in items)
    vmax = max(total, price["value"]) * 1.12
    bx, bw, base, hh = zx + 10, 300, zy + zh - 30, zh - 70
    Y = lambda v: base - hh * v / vmax
    acc = 0
    shades = [0.55, 0.42, 0.32, 0.24, 0.17, 0.12]
    # label slots: centred on each segment, then pushed apart so thin segments don't collide
    mids, a_ = [], 0
    for it in items:
        mids.append((Y(a_) + Y(a_ + it["value"])) / 2); a_ += it["value"]
    slots = list(mids)
    for k in range(1, len(slots)):
        slots[k] = min(slots[k], slots[k - 1] - 66)
    for i, it in enumerate(items):
        p = ease_out(prog(t, 0.45 + i * 0.3, 0.5))
        if p <= 0: break
        y0, y1 = Y(acc), Y(acc + it["value"] * p)
        ctx.rectangle(bx, y1, bw, y0 - y1 - 3); rgba(ctx, INK, shades[i % len(shades)]); ctx.fill()
        ly = slots[i]
        rgba(ctx, INK, 0.35 * p); ctx.set_line_width(1.5)
        ctx.move_to(bx + bw + 6, mids[i]); ctx.line_to(bx + bw + 22, ly - 10); ctx.stroke()
        text(ctx, it["label"], bx + bw + 30, ly - 2, SANS_MED, 30, INK, p)
        text(ctx, fmt(it["value"], spec), bx + bw + 30, ly + 30, MONO, 24, MUTED, p)
        acc += it["value"] * p
    q = ease_out(prog(t, 0.45 + len(items) * 0.3, 0.6))
    if q > 0:
        tw = width(ctx, sc.get("total_label", "All-in cost") + "  " + fmt(total, spec), MONO_BOLD, 26)
        text(ctx, sc.get("total_label", "All-in cost").upper() + "  " + fmt(total, spec), bx, Y(total) - 18, MONO_BOLD, 26, INK, q)
        py = Y(price["value"])
        ctx.set_dash([14, 10]); rgba(ctx, env["accent"], q); ctx.set_line_width(3)
        ctx.move_to(zx, py); ctx.line_to(zx + (zw) * q, py); ctx.stroke(); ctx.set_dash([])
        text(ctx, f"{price['label']}  {fmt(price['value'], spec)}", zx + zw, py - 16, MONO_BOLD, 26, env["accent"], q, align="right")
        m = price["value"] - total
        if m > 0:
            r_ = ease_out(prog(t, 0.75 + len(items) * 0.3, 0.6))
            ctx.rectangle(bx, py, bw, (Y(total) - py) * r_); rgba(ctx, env["accent"], 0.22); ctx.fill()
            text(ctx, sc.get("margin_label", "Margin"), bx + bw / 2, (py + Y(total)) / 2 + 2, SANS_SEMI, 28, INK, r_, align="center")
            text(ctx, fmt(m, spec), bx + bw / 2, (py + Y(total)) / 2 + 34, MONO_BOLD, 26, env["accent"], r_, align="center")
    if sc.get("note"):
        text(ctx, sc["note"], zx, zy + zh + 10, SANS, 22, MUTED, ease_out(prog(t, 0.3, 0.5)))


# ---------------------------------------------------------------- one big number
def big(ctx, sc, t, D, env):
    top = heading(ctx, sc, t, env)
    zx, zy, zw, zh = zone(top)
    p = ease_out(prog(t, 0.35, 0.6))
    cp = ease_out(prog(t, 0.35, 1.4))
    v = value_of(sc, cp)
    size = sc.get("size", 210)
    while width(ctx, v, SERIF, size) > zw and size > 80: size -= 6
    cy = zy + zh * 0.45
    text(ctx, v, W / 2, cy + (1 - p) * 40, SERIF, size, env["accent"] if sc.get("accent", True) else INK, p, align="center")
    q = ease_out(prog(t, 0.7, 0.6))
    for k, ln in enumerate(wrap(ctx, sc.get("caption", ""), SANS_MED, 38, zw - 60)[:3]):
        text(ctx, ln, W / 2, cy + 90 + k * 50, SANS_MED, 38, INK, q, align="center")
    if sc.get("sub"):   # wraps to two lines rather than running off the screen
        for k, ln in enumerate(wrap(ctx, sc["sub"], MONO, 22, zw - 40)[:2]):
            text(ctx, ln, W / 2, cy + 90 + 3 * 50 + 10 + k * 32, MONO, 22, MUTED, q, align="center")


# ---------------------------------------------------------------- outro
def outro(ctx, sc, t, D, env):
    p = ease_out(prog(t, 0.0, 0.8))
    s = 300
    swan.draw(ctx, W / 2 - s / 2, 330 + (1 - p) * 30, s, body=INK, beak=ACCENT, eye=BG)
    q = ease_out(prog(t, 0.3, 0.6))
    text(ctx, "BLACK SWAN STOCKS", W / 2, 720, SANS_SEMI, 48, INK, q, align="center", tracking=0.2)
    text(ctx, sc.get("line1", "ASX junior miners, explained. Mon · Wed · Fri"), W / 2, 786, MONO, 28, MUTED, q, align="center")
    text(ctx, sc.get("line2", "Sunday: the big picture"), W / 2, 830, MONO, 28, MUTED, q, align="center")
    r_ = ease_out(prog(t, 0.6, 0.6))
    bx, by, bw = X0, 900, X1 - X0
    disc = sc.get("disclaimer") or env["disclaimer"]
    lines = wrap(ctx, disc, SANS, 32, bw - 70)
    bh = 96 + len(lines) * 44
    card(ctx, bx, by, bw, bh, r_)
    text(ctx, "THE FINE PRINT", bx + 35, by + 54, MONO, 22, env["accent"], r_, tracking=0.1)
    for k, ln in enumerate(lines):
        text(ctx, ln, bx + 35, by + 104 + k * 44, SANS, 32, INK, r_ * 0.85)
    f = ease_out(prog(t, 1.0, 0.6))
    text(ctx, sc.get("cta", "Follow for the next one"), W / 2, by + bh + 130, SERIF_IT, 76, INK, f, align="center")


RENDER = {"hook": hook, "map": map_scene, "stats": stats, "bars": bars, "timeline": timeline, "versus": versus,
          "list": listing, "line": line, "catalysts": catalysts, "intercept": intercept, "stack": stack, "big": big, "outro": outro}
