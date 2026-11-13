"""The Black Swan mark, drawn as vector paths in a 100x100 box (origin top-left)."""
import math


def _path(ctx):
    # Neck front meets the breast, which rounds down into a long low hull with the tail lifting right.
    ctx.move_to(27.2, 60)
    ctx.curve_to(26.5, 71, 31, 80, 43, 82.5)             # breast to belly
    ctx.curve_to(58, 85.5, 77, 83.5, 88.5, 73.5)         # belly to tail
    ctx.curve_to(93, 69.5, 95.5, 62, 95, 55.5)           # tail tip lifts
    ctx.curve_to(88, 61.5, 80, 62.5, 72.5, 60.5)         # top of tail back to the wing
    ctx.curve_to(61, 49.5, 48.5, 49.5, 41.5, 57.5)       # wing hump down towards the neck
    ctx.curve_to(39.6, 59.8, 38.6, 62, 38.4, 64.5)       # back of neck base
    # Neck: rises in an S to the head (back edge)
    ctx.curve_to(36.2, 52, 42.2, 42, 40.6, 30)
    ctx.curve_to(39.8, 22, 35, 16, 29.8, 16.6)           # crown of head
    ctx.curve_to(26.4, 17, 23.8, 19.4, 22.6, 22.4)       # forehead to beak base (top)
    ctx.line_to(22.6, 26.2)                              # beak base (bottom)
    ctx.curve_to(27, 25, 32.4, 25.4, 33.6, 30.5)         # throat
    ctx.curve_to(35, 39, 26.2, 47.5, 27.2, 60)           # front of neck down into the breast
    ctx.close_path()


def _beak(ctx):
    ctx.move_to(23.0, 21.9)
    ctx.curve_to(19, 23.2, 14.6, 26, 11.8, 30.2)         # top edge down to the tip
    ctx.curve_to(15.6, 29, 19.4, 27.8, 23.0, 26.9)       # underside back to the face
    ctx.close_path()


def draw(ctx, x, y, size, body=(0.05, 0.05, 0.06), beak=(0.90, 0.28, 0.30), eye=None, flip=False):
    """Draw the swan with its 100x100 box at (x, y) scaled to `size` px."""
    ctx.save()
    ctx.translate(x, y)
    s = size / 100.0
    if flip:
        ctx.translate(size, 0); ctx.scale(-s, s)
    else:
        ctx.scale(s, s)
    ctx.set_source_rgb(*body); _path(ctx); ctx.fill()
    ctx.set_source_rgb(*beak); _beak(ctx); ctx.fill()
    if eye:
        ctx.set_source_rgb(*eye); ctx.arc(28.2, 20.6, 1.05, 0, 2 * math.pi); ctx.fill()
    ctx.restore()
