"""Illustrated people + business scenes (used in place of photos). Flat-glossy style, brand colours."""
from eng import *

SKIN = [(241, 194, 150), (224, 172, 130), (198, 140, 100), (232, 185, 140)]
HAIR = (35, 30, 28)

def _g(img, fn, c1, c2, sh=0.3): return gshape(img, fn, c1, c2, sh)

def person(img, cx, by, s=1.0, g='m', mood='happy', shirt=((74, 222, 128), (21, 101, 52)), skin=0, prop=None, hair=None):
    """bust; by = bottom y. s ~ 1 => 300px tall."""
    sk = SKIN[skin % 4]; hc = hair or HAIR
    d = lambda: ImageDraw.Draw(img)
    hy = by - 215 * s          # head centre
    # body
    _g(img, lambda dd: dd.rounded_rectangle(P((cx - 110 * s, by - 120 * s), (cx + 110 * s, by + 40 * s)), 60 * s * S, fill=255), shirt[0], shirt[1], 0.3)
    # neck
    _g(img, lambda dd: dd.rectangle(P((cx - 22 * s, hy + 50 * s), (cx + 22 * s, by - 110 * s)), fill=255), lighten(sk, .1), darken(sk, .12), 0)
    # collar V
    d().polygon(P((cx - 30 * s, by - 120 * s), (cx, by - 80 * s), (cx + 30 * s, by - 120 * s)), fill=lighten(sk, 0.05))
    if g == 'f':   # long hair behind
        _g(img, lambda dd: dd.rounded_rectangle(P((cx - 78 * s, hy - 60 * s), (cx + 78 * s, hy + 110 * s)), 60 * s * S, fill=255), lighten(hc, .15), hc, 0.15)
    # head
    _g(img, lambda dd: dd.ellipse(P((cx - 62 * s, hy - 72 * s), (cx + 62 * s, hy + 72 * s)), fill=255), lighten(sk, .12), darken(sk, .08), 0.25)
    # ears
    for sg in (-1, 1): _g(img, lambda dd, sg=sg: dd.ellipse(P((cx + sg * 60 * s - 12 * s, hy - 10 * s), (cx + sg * 60 * s + 12 * s, hy + 20 * s)), fill=255), sk, darken(sk, .1), 0)
    # hair top
    if g == 'm':
        _g(img, lambda dd: dd.chord(P((cx - 66 * s, hy - 84 * s), (cx + 66 * s, hy + 30 * s)), 180, 360, fill=255), lighten(hc, .2), hc, 0.2)
        d().polygon(P((cx - 66 * s, hy - 26 * s), (cx - 40 * s, hy - 50 * s), (cx - 60 * s, hy + 4 * s)), fill=hc)
    else:
        _g(img, lambda dd: dd.chord(P((cx - 68 * s, hy - 86 * s), (cx + 68 * s, hy + 40 * s)), 180, 360, fill=255), lighten(hc, .2), hc, 0.2)
        d().ellipse(P((cx - 4 * s, hy - 70 * s), (cx + 8 * s, hy - 58 * s)), fill=YEL)   # bindi/clip accent
    # face
    ey = hy + 4 * s
    for sg in (-1, 1):
        d().ellipse(P((cx + sg * 24 * s - 6 * s, ey - 7 * s), (cx + sg * 24 * s + 6 * s, ey + 7 * s)), fill=(40, 32, 28))
        d().ellipse(P((cx + sg * 24 * s - 2 * s, ey - 5 * s), (cx + sg * 24 * s + 2 * s, ey - 1 * s)), fill=WHITE)
        if mood == 'worry':
            d().line(P((cx + sg * 12 * s, ey - 27 * s), (cx + sg * 36 * s, ey - 17 * s)), fill=hc, width=int(5 * s * S))
        else:
            d().arc(P((cx + sg * 24 * s - 14 * s, ey - 28 * s), (cx + sg * 24 * s + 14 * s, ey - 10 * s)), 200, 340, fill=hc, width=int(5 * s * S))
    my = hy + 38 * s
    if mood == 'worry':
        d().arc(P((cx - 18 * s, my), (cx + 18 * s, my + 22 * s)), 200, 340, fill=(120, 50, 40), width=int(5 * s * S))
        _g(img, lambda dd: dd.ellipse(P((cx + 46 * s, hy - 40 * s), (cx + 58 * s, hy - 22 * s)), fill=255), (220, 240, 255), (150, 190, 230), 0)  # sweat drop
    else:
        d().chord(P((cx - 24 * s, my - 14 * s), (cx + 24 * s, my + 20 * s)), 0, 180, fill=(160, 50, 50))
        d().rectangle(P((cx - 18 * s, my + 2 * s), (cx + 18 * s, my + 7 * s)), fill=WHITE)
    # arm + prop
    if prop == 'phone':
        _g(img, lambda dd: dd.rounded_rectangle(P((cx + 70 * s, by - 150 * s), (cx + 120 * s, by - 60 * s)), 26 * s * S, fill=255), shirt[0], shirt[1], 0.2)
        _g(img, lambda dd: dd.rounded_rectangle(P((cx + 86 * s, by - 236 * s), (cx + 136 * s, by - 140 * s)), 10 * s * S, fill=255), (60, 70, 66), (15, 20, 18), 0.3)
        d().rounded_rectangle(P((cx + 91 * s, by - 228 * s), (cx + 131 * s, by - 150 * s)), 6 * s * S, fill=(187, 247, 208))
        _g(img, lambda dd: dd.ellipse(P((cx + 84 * s, by - 172 * s), (cx + 112 * s, by - 140 * s)), fill=255), sk, darken(sk, .1), 0)
    elif mood == 'worry':
        _g(img, lambda dd: dd.ellipse(P((cx - 84 * s, hy - 20 * s), (cx - 50 * s, hy + 20 * s)), fill=255), sk, darken(sk, .1), 0)   # hand on cheek

# ---------- props ----------
def pr_box(img, x, y, w, h, g=GOLDG, r=8):
    _g(img, lambda dd: dd.rounded_rectangle(P((x, y), (x + w, y + h)), r * S, fill=255), g[0], g[1], 0.3)

def prop(img, kind, cx, cy, s=1.0):
    d = ImageDraw.Draw(img)
    if kind == 'shop':
        pr_box(img, cx - 120 * s, cy - 20 * s, 240 * s, 130 * s, ((255, 255, 255), (220, 236, 228)))
        for i in range(6):
            x0 = cx - 120 * s + i * 40 * s
            _g(img, lambda dd, x0=x0, i=i: dd.chord(P((x0, cy - 70 * s), (x0 + 40 * s, cy - 10 * s)), 0, 180, fill=255), *(GOLDG if i % 2 else GREENG))
        pr_box(img, cx - 130 * s, cy - 90 * s, 260 * s, 46 * s, GREENG, 10)
        for i in range(3): pr_box(img, cx - 100 * s + i * 70 * s, cy + 20 * s, 50 * s, 60 * s, GOLDG if i != 1 else GREENG, 6)
    elif kind == 'books':
        for i, gg in enumerate([GREENG, GOLDG, DEEPG]): pr_box(img, cx - 90 * s + i * 8 * s, cy + 40 * s - i * 36 * s, 180 * s, 34 * s, gg, 6)
        _g(img, lambda dd: dd.polygon(P((cx - 60 * s, cy - 80 * s), (cx, cy - 104 * s), (cx + 60 * s, cy - 80 * s), (cx, cy - 56 * s)), fill=255), (60, 70, 66), (10, 18, 13))
    elif kind == 'plate':
        gellipse(img, cx, cy + 20 * s, 120 * s, 40 * s, (255, 255, 255), (210, 225, 218), 0.3)
        for (dx, dy, gg) in [(-40, 0, GOLDG), (10, -14, GREENG), (50, 4, GOLDG), (-6, 16, ((254, 220, 160), (217, 120, 40)))]:
            gellipse(img, cx + dx * s, cy + dy * s, 34 * s, 22 * s, *gg, 0.4)
        _g(img, lambda dd: dd.rounded_rectangle(P((cx - 50 * s, cy - 150 * s), (cx + 50 * s, cy - 70 * s)), 30 * s * S, fill=255), (255, 255, 255), (225, 235, 230))   # chef hat
    elif kind == 'scissors':
        for sg in (-1, 1):
            d.line(P((cx, cy), (cx + sg * 60 * s, cy - 120 * s)), fill=(120, 130, 125), width=int(10 * s * S))
            gellipse(img, cx - sg * 30 * s, cy + 40 * s, 26 * s, 26 * s, *GOLDG, 0.3); gellipse(img, cx - sg * 30 * s, cy + 40 * s, 13 * s, 13 * s, (255, 255, 255), (240, 240, 240), 0)
        gellipse(img, cx + 120 * s, cy - 40 * s, 60 * s, 80 * s, (230, 245, 250), (170, 210, 220), 0.4)    # mirror
    elif kind == 'laptop':
        pr_box(img, cx - 110 * s, cy - 80 * s, 220 * s, 140 * s, ((60, 70, 66), (15, 20, 18)), 12)
        pr_box(img, cx - 98 * s, cy - 68 * s, 196 * s, 116 * s, ((236, 253, 243), (167, 243, 208)), 6)
        for i, hh in enumerate((30, 50, 40, 70)): pr_box(img, cx - 70 * s + i * 34 * s, cy + 30 * s - hh * s, 22 * s, hh * s, GREENG if i != 3 else GOLDG, 3)
        pr_box(img, cx - 140 * s, cy + 60 * s, 280 * s, 18 * s, ((200, 210, 205), (120, 135, 128)), 8)
    elif kind == 'dumbbell':
        pr_box(img, cx - 90 * s, cy - 8 * s, 180 * s, 16 * s, ((200, 210, 205), (110, 125, 118)), 6)
        for sg in (-1, 1): pr_box(img, cx + sg * 90 * s - 24 * s, cy - 50 * s, 48 * s, 100 * s, DEEPG, 10)
    elif kind == 'house':
        _g(img, lambda dd: dd.polygon(P((cx - 130 * s, cy - 20 * s), (cx, cy - 130 * s), (cx + 130 * s, cy - 20 * s)), fill=255), *GREENG)
        pr_box(img, cx - 100 * s, cy - 20 * s, 200 * s, 140 * s, ((255, 255, 255), (230, 240, 235)), 4)
        pr_box(img, cx - 25 * s, cy + 40 * s, 50 * s, 80 * s, GOLDG, 4)
        for sg in (-1, 1): pr_box(img, cx + sg * 60 * s - 22 * s, cy + 10 * s, 44 * s, 40 * s, ((200, 230, 250), (120, 170, 210)), 4)
    elif kind == 'dress':
        d.arc(P((cx - 20 * s, cy - 150 * s), (cx + 20 * s, cy - 110 * s)), 180, 360, fill=(120, 130, 125), width=int(5 * s * S))
        _g(img, lambda dd: dd.polygon(P((cx - 40 * s, cy - 110 * s), (cx + 40 * s, cy - 110 * s), (cx + 100 * s, cy + 100 * s), (cx - 100 * s, cy + 100 * s)), fill=255), *GOLDG)
        pr_box(img, cx - 44 * s, cy - 40 * s, 88 * s, 16 * s, GREENG, 6)
    elif kind == 'gift':
        pr_box(img, cx - 80 * s, cy - 40 * s, 160 * s, 130 * s, GOLDG, 10); pr_box(img, cx - 92 * s, cy - 70 * s, 184 * s, 40 * s, GOLDG, 8)
        pr_box(img, cx - 12 * s, cy - 70 * s, 24 * s, 160 * s, GREENG, 4)
        for sg in (-1, 1): gellipse(img, cx + sg * 26 * s, cy - 88 * s, 28 * s, 18 * s, *GREENG, 0.3)
    elif kind == 'flask':
        _g(img, lambda dd: dd.polygon(P((cx - 20 * s, cy - 120 * s), (cx + 20 * s, cy - 120 * s), (cx + 20 * s, cy - 50 * s), (cx + 80 * s, cy + 80 * s), (cx - 80 * s, cy + 80 * s), (cx - 20 * s, cy - 50 * s)), fill=255), (240, 250, 255), (190, 220, 235), 0.4)
        _g(img, lambda dd: dd.polygon(P((cx - 52 * s, cy + 20 * s), (cx + 52 * s, cy + 20 * s), (cx + 80 * s, cy + 80 * s), (cx - 80 * s, cy + 80 * s)), fill=255), *GREENG)
        gellipse(img, cx + 120 * s, cy, 40 * s, 40 * s, (255, 255, 255), (220, 230, 225), 0.3)
        d.line(P((cx + 100 * s, cy), (cx + 140 * s, cy)), fill=(200, 40, 40), width=int(10 * s * S)); d.line(P((cx + 120 * s, cy - 20 * s), (cx + 120 * s, cy + 20 * s)), fill=(200, 40, 40), width=int(10 * s * S))
    elif kind == 'phone':
        pr_box(img, cx - 60 * s, cy - 120 * s, 120 * s, 230 * s, ((60, 70, 66), (15, 20, 18)), 20)
        pr_box(img, cx - 50 * s, cy - 104 * s, 100 * s, 196 * s, ((236, 253, 243), (167, 243, 208)), 12)
        for i in range(3): pr_box(img, cx - 38 * s, cy - 84 * s + i * 56 * s, 76 * s, 40 * s, GOLDG if i == 0 else GREENG, 8)
    elif kind == 'bell':
        _g(img, lambda dd: dd.chord(P((cx - 90 * s, cy - 80 * s), (cx + 90 * s, cy + 90 * s)), 180, 360, fill=255), *GOLDG)
        pr_box(img, cx - 110 * s, cy + 4 * s, 220 * s, 20 * s, GOLDG, 6); gellipse(img, cx, cy - 92 * s, 12 * s, 12 * s, *GOLDG)
    elif kind == 'briefcase':
        pr_box(img, cx - 110 * s, cy - 50 * s, 220 * s, 140 * s, ((120, 80, 50), (70, 45, 25)), 14)
        d.rounded_rectangle(P((cx - 40 * s, cy - 82 * s), (cx + 40 * s, cy - 48 * s)), 10 * s * S, outline=(70, 45, 25), width=int(8 * s * S))
        pr_box(img, cx - 16 * s, cy, 32 * s, 24 * s, GOLDG, 4)
    elif kind == 'sofa':
        pr_box(img, cx - 140 * s, cy - 40 * s, 280 * s, 90 * s, GREENG, 26); pr_box(img, cx - 160 * s, cy, 60 * s, 90 * s, DEEPG, 20); pr_box(img, cx + 100 * s, cy, 60 * s, 90 * s, DEEPG, 20)
        pr_box(img, cx - 110 * s, cy + 30 * s, 220 * s, 50 * s, GOLDG, 14)
    elif kind == 'wrench':
        d.line(P((cx - 100 * s, cy + 100 * s), (cx + 60 * s, cy - 60 * s)), fill=(140, 150, 145), width=int(22 * s * S))
        gellipse(img, cx + 80 * s, cy - 80 * s, 46 * s, 46 * s, (220, 228, 224), (120, 135, 128), 0.3)
        gellipse(img, cx + 96 * s, cy - 96 * s, 20 * s, 20 * s, (255, 255, 255), (240, 245, 242), 0)
        gear_ = lambda: None
    elif kind == 'ring':
        d.ellipse(P((cx - 70 * s, cy - 40 * s), (cx + 70 * s, cy + 100 * s)), outline=(217, 159, 6), width=int(18 * s * S))
        _g(img, lambda dd: dd.polygon(P((cx - 40 * s, cy - 60 * s), (cx, cy - 110 * s), (cx + 40 * s, cy - 60 * s), (cx, cy - 20 * s)), fill=255), (240, 250, 255), (160, 200, 230), 0.5)
    elif kind == 'monitor':
        pr_box(img, cx - 130 * s, cy - 100 * s, 260 * s, 170 * s, ((60, 70, 66), (15, 20, 18)), 14)
        pr_box(img, cx - 116 * s, cy - 86 * s, 232 * s, 142 * s, ((236, 253, 243), (167, 243, 208)), 8)
        T(img, (cx, cy - 16 * s), '</>', 50 * s, DEEP, 'pb', 'mm'); pr_box(img, cx - 20 * s, cy + 70 * s, 40 * s, 40 * s, ((200, 210, 205), (120, 135, 128)), 4)
    elif kind == 'camera':
        pr_box(img, cx - 120 * s, cy - 70 * s, 240 * s, 150 * s, ((60, 70, 66), (15, 20, 18)), 20)
        gellipse(img, cx, cy + 4 * s, 56 * s, 56 * s, (90, 100, 96), (20, 25, 22), 0.4); gellipse(img, cx, cy + 4 * s, 34 * s, 34 * s, (120, 190, 230), (20, 60, 90), 0.5)
        pr_box(img, cx + 60 * s, cy - 90 * s, 40 * s, 24 * s, GOLDG, 6)
    elif kind == 'yoga':
        pr_box(img, cx - 140 * s, cy + 60 * s, 280 * s, 24 * s, GOLDG, 12)
        gellipse(img, cx, cy - 90 * s, 26 * s, 26 * s, *GREENG)
        _g(img, lambda dd: dd.polygon(P((cx, cy - 64 * s), (cx + 50 * s, cy + 20 * s), (cx - 50 * s, cy + 20 * s)), fill=255), *GREENG)
        gellipse(img, cx, cy + 40 * s, 110 * s, 30 * s, *GREENG)
    elif kind == 'guitar':
        gellipse(img, cx, cy + 40 * s, 70 * s, 64 * s, *GOLDG, 0.4); gellipse(img, cx, cy - 20 * s, 52 * s, 48 * s, *GOLDG, 0.4)
        gellipse(img, cx, cy + 20 * s, 18 * s, 18 * s, (60, 40, 20), (30, 20, 10), 0)
        pr_box(img, cx - 10 * s, cy - 180 * s, 20 * s, 160 * s, ((120, 80, 50), (70, 45, 25)), 4)
    elif kind == 'juice':
        _g(img, lambda dd: dd.polygon(P((cx - 60 * s, cy - 100 * s), (cx + 60 * s, cy - 100 * s), (cx + 44 * s, cy + 100 * s), (cx - 44 * s, cy + 100 * s)), fill=255), (254, 220, 120), (234, 140, 8), 0.4)
        d.line(P((cx + 20 * s, cy - 150 * s), (cx + 6 * s, cy - 60 * s)), fill=(34, 197, 94), width=int(10 * s * S))
        gellipse(img, cx - 50 * s, cy - 100 * s, 30 * s, 30 * s, *GREENG)
    elif kind == 'boxes':
        for (dx, dy, w, gg) in [(-90, 0, 120, GOLDG), (40, 20, 100, GREENG), (-30, -90, 100, ((254, 220, 160), (200, 140, 60)))]:
            pr_box(img, cx + dx * s, cy + dy * s, w * s, 90 * s, gg, 6)
            d.line(P((cx + dx * s + w * s / 2, cy + dy * s), (cx + dx * s + w * s / 2, cy + dy * s + 90 * s)), fill=(255, 255, 255), width=int(6 * s * S))
    elif kind == 'milk':
        pr_box(img, cx - 60 * s, cy - 60 * s, 120 * s, 170 * s, ((240, 245, 250), (180, 195, 205)), 30)
        pr_box(img, cx - 34 * s, cy - 100 * s, 68 * s, 50 * s, ((240, 245, 250), (180, 195, 205)), 10)
        pr_box(img, cx - 60 * s, cy, 120 * s, 30 * s, GREENG, 4)
    elif kind == 'bat':
        _g(img, lambda dd: dd.polygon(P((cx - 20 * s, cy - 140 * s), (cx + 20 * s, cy - 140 * s), (cx + 40 * s, cy + 110 * s), (cx - 40 * s, cy + 110 * s)), fill=255), (254, 230, 170), (210, 160, 90), 0.3)
        gellipse(img, cx + 90 * s, cy + 80 * s, 28 * s, 28 * s, (230, 60, 50), (150, 20, 20), 0.4)
    elif kind == 'flowers':
        for (dx, dy) in [(-60, 0), (0, -50), (60, 0), (-30, 50), (30, 50)]:
            for i in range(8):
                a = i * math.pi / 4
                gellipse(img, cx + dx * s + 22 * s * math.cos(a), cy + dy * s + 22 * s * math.sin(a), 16 * s, 16 * s, *GOLDG, 0.3)
            gellipse(img, cx + dx * s, cy + dy * s, 12 * s, 12 * s, *GREENG)
    elif kind == 'bag':
        pr_box(img, cx - 90 * s, cy - 80 * s, 180 * s, 200 * s, GREENG, 40); pr_box(img, cx - 60 * s, cy + 10 * s, 120 * s, 70 * s, GOLDG, 16)
        d.arc(P((cx - 40 * s, cy - 120 * s), (cx + 40 * s, cy - 50 * s)), 180, 360, fill=DEEP, width=int(10 * s * S))
    elif kind == 'printer':
        pr_box(img, cx - 130 * s, cy - 40 * s, 260 * s, 110 * s, ((200, 210, 205), (110, 125, 118)), 18)
        pr_box(img, cx - 80 * s, cy - 110 * s, 160 * s, 80 * s, ((255, 255, 255), (230, 235, 232)), 4)
        pr_box(img, cx - 80 * s, cy + 50 * s, 160 * s, 80 * s, ((255, 255, 255), (230, 235, 232)), 4); T(img, (cx, cy + 92 * s), 'अ', 44 * s, DEEP, 'pb', 'mm')
    elif kind == 'suitcase':
        pr_box(img, cx - 80 * s, cy - 60 * s, 160 * s, 180 * s, GOLDG, 20)
        d.rounded_rectangle(P((cx - 30 * s, cy - 100 * s), (cx + 30 * s, cy - 56 * s)), 10 * s * S, outline=DEEP, width=int(8 * s * S))
        for sg in (-1, 1): pr_box(img, cx + sg * 40 * s - 6 * s, cy - 60 * s, 12 * s, 180 * s, GREENG, 4)
        _g(img, lambda dd: dd.polygon(P((cx + 110 * s, cy - 120 * s), (cx + 220 * s, cy - 150 * s), (cx + 140 * s, cy - 100 * s)), fill=255), (255, 255, 255), (200, 215, 208))
    elif kind == 'bricks':
        for r_ in range(3):
            for c_ in range(3 - r_ % 2):
                pr_box(img, cx - 120 * s + c_ * 82 * s + (r_ % 2) * 41 * s, cy + 40 * s - r_ * 44 * s, 76 * s, 38 * s, ((254, 200, 140), (200, 110, 50)), 4)
        _g(img, lambda dd: dd.chord(P((cx - 70 * s, cy - 170 * s), (cx + 70 * s, cy - 50 * s)), 180, 360, fill=255), *GOLDG)
    elif kind == 'wheat':
        for k in (-40, 0, 40):
            d.line(P((cx + k * s, cy + 120 * s), (cx + k * s * 1.3, cy - 80 * s)), fill=(217, 159, 6), width=int(6 * s * S))
            for j in range(5):
                y = cy - 70 * s + j * 22 * s
                gellipse(img, cx + k * s * 1.25 - 12 * s, y, 11 * s, 7 * s, *GOLDG, 0.3); gellipse(img, cx + k * s * 1.25 + 12 * s, y, 11 * s, 7 * s, *GOLDG, 0.3)
    elif kind == 'lipstick':
        pr_box(img, cx - 40 * s, cy - 20 * s, 80 * s, 130 * s, GOLDG, 10)
        _g(img, lambda dd: dd.polygon(P((cx - 30 * s, cy - 20 * s), (cx - 30 * s, cy - 100 * s), (cx + 30 * s, cy - 130 * s), (cx + 30 * s, cy - 20 * s)), fill=255), (240, 110, 130), (180, 40, 70), 0.4)
        gellipse(img, cx + 120 * s, cy + 20 * s, 60 * s, 60 * s, (255, 230, 220), (230, 170, 150), 0.4)
    elif kind == 'car':
        _g(img, lambda dd: dd.rounded_rectangle(P((cx - 160 * s, cy - 20 * s), (cx + 160 * s, cy + 60 * s)), 30 * s * S, fill=255), *GREENG)
        _g(img, lambda dd: dd.polygon(P((cx - 90 * s, cy - 20 * s), (cx - 50 * s, cy - 80 * s), (cx + 60 * s, cy - 80 * s), (cx + 110 * s, cy - 20 * s)), fill=255), *GREENG)
        pr_box(img, cx - 40 * s, cy - 70 * s, 90 * s, 44 * s, ((200, 230, 250), (120, 170, 210)), 6)
        for sg in (-1, 1): gellipse(img, cx + sg * 90 * s, cy + 60 * s, 36 * s, 36 * s, (60, 70, 66), (15, 20, 18), 0.3)
    elif kind == 'pot':
        _g(img, lambda dd: dd.chord(P((cx - 110 * s, cy - 80 * s), (cx + 110 * s, cy + 110 * s)), 0, 180, fill=255), (230, 235, 240), (140, 150, 160), 0.5)
        pr_box(img, cx - 120 * s, cy - 6 * s, 240 * s, 20 * s, ((230, 235, 240), (140, 150, 160)), 8)
        _g(img, lambda dd: dd.chord(P((cx - 70 * s, cy - 60 * s), (cx + 70 * s, cy + 30 * s)), 180, 360, fill=255), *GOLDG)
    elif kind == 'stetho':
        d.arc(P((cx - 90 * s, cy - 120 * s), (cx + 90 * s, cy + 60 * s)), 0, 180, fill=(60, 70, 66), width=int(12 * s * S))
        for sg in (-1, 1): d.line(P((cx + sg * 90 * s, cy - 30 * s), (cx + sg * 70 * s, cy - 120 * s)), fill=(60, 70, 66), width=int(10 * s * S))
        gellipse(img, cx, cy + 90 * s, 34 * s, 34 * s, (220, 228, 224), (120, 135, 128), 0.4)
        pr_box(img, cx + 90 * s, cy - 40 * s, 110 * s, 110 * s, ((255, 255, 255), (230, 240, 235)), 16)
        pr_box(img, cx + 135 * s, cy - 25 * s, 20 * s, 80 * s, GREENG, 4); pr_box(img, cx + 105 * s, cy + 5 * s, 80 * s, 20 * s, GREENG, 4)
    elif kind == 'teddy':
        for sg in (-1, 1): gellipse(img, cx + sg * 50 * s, cy - 110 * s, 26 * s, 26 * s, (214, 160, 100), (160, 100, 50), 0.3)
        gellipse(img, cx, cy - 70 * s, 64 * s, 58 * s, (214, 160, 100), (160, 100, 50), 0.3)
        gellipse(img, cx, cy + 60 * s, 80 * s, 80 * s, (214, 160, 100), (160, 100, 50), 0.3)
        gellipse(img, cx, cy - 52 * s, 24 * s, 18 * s, (240, 210, 170), (214, 170, 120), 0)
        for sg in (-1, 1): d.ellipse(P((cx + sg * 22 * s - 6 * s, cy - 90 * s), (cx + sg * 22 * s + 6 * s, cy - 78 * s)), fill=(30, 20, 10))
        pr_box(img, cx - 30 * s, cy - 20 * s, 60 * s, 20 * s, GREENG, 8)
    elif kind == 'stupa':
        _g(img, lambda dd: dd.chord(P((cx - 130 * s, cy - 110 * s), (cx + 130 * s, cy + 150 * s)), 180, 360, fill=255), (255, 251, 225), (240, 198, 70))
        pr_box(img, cx - 150 * s, cy + 20 * s, 300 * s, 30 * s, GOLDG, 4); pr_box(img, cx - 20 * s, cy - 150 * s, 40 * s, 40 * s, GREENG, 4)
    else:   # generic sparkle badge
        gellipse(img, cx, cy, 100 * s, 100 * s, *GOLDG, 0.4); sparkle(img, cx, cy, 60 * s, WHITE)

# business -> (props, person gender, shirt)
BIZ = dict(
    shop=('shop', 'm'), coaching=('books', 'f'), restaurant=('plate', 'm'), salon=('scissors', 'f'), startup=('laptop', 'm'),
    sweets=('gift', 'm'), gym=('dumbbell', 'm'), realestate=('house', 'm'), boutique=('dress', 'f'), gifts=('gift', 'f'),
    lab=('flask', 'f'), women=('dress', 'f'), mobile=('phone', 'm'), hotel=('bell', 'm'), ca=('briefcase', 'm'),
    furniture=('sofa', 'f'), workshop=('wrench', 'm'), jewellery=('ring', 'f'), it=('monitor', 'm'), photo=('camera', 'm'),
    yoga=('yoga', 'f'), music=('guitar', 'm'), juice=('juice', 'f'), localbrand=('boxes', 'm'), delivery=('boxes', 'f'),
    dairy=('milk', 'm'), sports=('bat', 'm'), decorator=('flowers', 'f'), school=('bag', 'f'), printing=('printer', 'm'),
    travel=('suitcase', 'f'), construction=('bricks', 'm'), agri=('wheat', 'm'), cosmetics=('lipstick', 'f'), car=('car', 'm'),
    utensils=('pot', 'f'), allbiz=('shop', 'f'), clinic=('stetho', 'f'), mp=('stupa', 'm'), toys=('teddy', 'f'),
    homestay=('house', 'f'), smallbiz=('shop', 'm'), worried=(None, 'm'), happy=(None, 'f'))

def scene(key, w, h, mood='happy', seed=0):
    """returns an RGB image (w x h logical, at S) with an illustrated business scene"""
    kind, g = BIZ.get(key, (None, 'm'))
    big = Image.new('RGB', (W, H), WHITE)
    pal = [((236, 253, 243), (134, 239, 172)), ((255, 251, 225), (253, 224, 71)), ((240, 253, 244), (187, 247, 208))][seed % 3]
    m = Image.new('L', big.size, 0); ImageDraw.Draw(m).rectangle(P((0, 0), (w, h)), fill=255)
    grad_mask_fill(big, m, pal[0], pal[1], sheen=0.0)
    glow(big, w * 0.75, h * 0.3, min(w, h) * 0.5, (255, 255, 255), 0.6)
    for i in range(6):
        x = (seed * 37 + i * 97) % max(1, int(w)); y = (seed * 53 + i * 61) % max(1, int(h * 0.6))
        gellipse(big, x, y, 10 + i * 3, 10 + i * 3, (255, 255, 255), (230, 250, 238), 0)
    s = min(w, h) / 420
    if kind:
        prop(big, kind, w * 0.70, h * 0.50, s * 0.9)
    shirts = [GREENG, GOLDG, DEEPG, ((120, 200, 240), (30, 100, 160))]
    person(big, w * (0.36 if kind else 0.5), h + 10 * s, s * 1.05, g, mood, shirts[(seed + (1 if g == 'f' else 0)) % 4], seed % 4,
           prop='phone' if mood == 'happy' and seed % 2 == 0 else None)
    return big.crop((0, 0, int(w * S), int(h * S)))
