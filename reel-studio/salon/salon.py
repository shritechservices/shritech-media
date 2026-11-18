import math, random, sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from words import GROUPS, SPANS

W, H, FPS = 1080, 1920, 30
END = 36.2
FD = '/usr/share/fonts/truetype/google-fonts/'
PB = '/home/claude/salon/fonts/PB.ttf'          # Poppins ExtraBold
FB = FD + 'Poppins-Bold.ttf'
FM = FD + 'Poppins-Medium.ttf'
PF = '/home/claude/salon/fonts/PF.ttf'          # Playfair Display Italic
FSYM = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

WHITE = (255, 255, 255)
GREEN = (34, 197, 94)
GREEN2 = (22, 163, 74)
DEEP = (10, 61, 34)
MINT = (240, 253, 244)
MINT2 = (209, 250, 223)
YEL = (250, 204, 21)
YEL2 = (253, 224, 71)
PALEY = (254, 249, 219)
SKIN = (255, 236, 186)
HAIR = (20, 83, 45)

_F = {}
def font(path, size):
    k = (path, size)
    if k not in _F:
        f = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
        if path == PF:
            try: f.set_variation_by_name('Bold Italic')
            except Exception: pass
        _F[k] = f
    return _F[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def eback(x, s=1.7):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def prog(t, a, d): return clamp((t - a) / d)
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))

# ---------------- compositing ----------------
def _paste(base, im, x, y):
    bx0, by0 = max(0, x), max(0, y)
    bx1, by1 = min(base.width, x + im.width), min(base.height, y + im.height)
    if bx1 <= bx0 or by1 <= by0: return
    base.alpha_composite(im.crop((bx0 - x, by0 - y, bx1 - x, by1 - y)), (bx0, by0))

def put(base, im, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01: return
    if abs(scale - 1) > 0.003:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    _paste(base, im, int(cx - im.width / 2), int(cy - im.height / 2))

SYMS = set('→↑↻✓✦☎♥🔒')
def split_runs(txt, path):
    runs = []
    for ch in txt:
        p = FSYM if ch in SYMS else path
        if runs and runs[-1][1] == p: runs[-1][0] += ch
        else: runs.append([ch, p])
    return [(r, p) for r, p in runs]
def twidth(txt, size, path):
    return sum(font(p, size).getlength(r) for r, p in split_runs(txt, path))

class Pad:
    """Supersampled (2x) drawing surface; coordinates in output pixels."""
    K = 2
    def __init__(s, w, h, bg=(0, 0, 0, 0)):
        s.w, s.h = w, h
        s.im = Image.new('RGBA', (w * s.K, h * s.K), bg)
        s.d = ImageDraw.Draw(s.im)
    def _b(s, b): return [v * s.K for v in b]
    def rect(s, b, r=0, fill=None, outline=None, width=1):
        s.d.rounded_rectangle(s._b(b), r * s.K, fill=fill, outline=outline, width=int(width * s.K))
    def ell(s, b, fill=None, outline=None, width=1):
        s.d.ellipse(s._b(b), fill=fill, outline=outline, width=int(width * s.K))
    def pie(s, b, a0, a1, fill):
        s.d.pieslice(s._b(b), a0, a1, fill=fill)
    def arc(s, b, a0, a1, fill, width=1):
        s.d.arc(s._b(b), a0, a1, fill=fill, width=int(width * s.K))
    def line(s, pts, fill, width=1):
        s.d.line([v * s.K for p in pts for v in p], fill=fill, width=int(width * s.K), joint='curve')
    def poly(s, pts, fill):
        s.d.polygon([(x * s.K, y * s.K) for x, y in pts], fill=fill)
    def text(s, xy, txt, size, fill, path=FB, anchor='la'):
        runs = split_runs(txt, path)
        if len(runs) == 1:
            s.d.text((xy[0] * s.K, xy[1] * s.K), txt, font=font(runs[0][1], size * s.K), fill=fill, anchor=anchor); return
        tw = sum(font(p, size * s.K).getlength(r) for r, p in runs)
        x = xy[0] * s.K - {'l': 0, 'm': tw / 2, 'r': tw}[anchor[0]]
        for r, p in runs:
            f = font(p, size * s.K)
            s.d.text((x, xy[1] * s.K), r, font=f, fill=fill, anchor='l' + anchor[1]); x += f.getlength(r)
    def img(s):
        return s.im.resize((s.w, s.h), Image.LANCZOS)

_C = {}
def cached(key, fn):
    if key not in _C: _C[key] = fn()
    return _C[key]

def with_shadow(im, blur=26, off=16, alpha=0.22, color=DEEP):
    pad = blur * 2 + off
    out = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    a = Image.new('L', out.size, 0)
    a.paste(im.getchannel('A'), (pad, pad + off))
    a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
    sh = Image.new('RGBA', out.size, color + (0,)); sh.putalpha(a)
    out.alpha_composite(sh)
    out.alpha_composite(im, (pad, pad))
    return out

def text_img(txt, size, fill=DEEP, path=PB, track=0):
    key = ('t', txt, size, fill, path, track)
    if key in _C: return _C[key]
    f = font(path, size)
    l, t, r, b = f.getbbox(txt)
    pad = 20
    im = Image.new('RGBA', (int(r - l + pad * 2 + track * len(txt)), int(b - t + pad * 2)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if track:
        x = pad - l
        for ch in txt:
            d.text((x, pad - t), ch, font=f, fill=fill); x += f.getlength(ch) + track
    else:
        d.text((pad - l, pad - t), txt, font=f, fill=fill)
    _C[key] = im
    return im

def line_img(segs, gap=18):
    """segs: list of (text, size, color, path). Baseline-aligned row."""
    key = ('line', tuple(segs), gap)
    if key in _C: return _C[key]
    asc = max(font(p, s).getmetrics()[0] for _, s, _, p in segs)
    desc = max(font(p, s).getmetrics()[1] for _, s, _, p in segs)
    widths = [font(p, s).getlength(tx) for tx, s, _, p in segs]
    Wt = int(sum(widths) + gap * (len(segs) - 1) + 40)
    im = Image.new('RGBA', (Wt, asc + desc + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = 20
    for (tx, s, c, p), w in zip(segs, widths):
        d.text((x, asc + 15), tx, font=font(p, s), fill=c, anchor='ls'); x += w + gap
    _C[key] = im
    return im

def pill(txt, size=30, bg=WHITE, fg=DEEP, border=None, path=FB, padx=26, pady=12, dot=None, shadow=True):
    key = ('pill', txt, size, bg, fg, border, path, padx, pady, dot, shadow)
    if key in _C: return _C[key]
    f = font(path, size)
    l = 0; r = twidth(txt, size, path)
    asc, desc = f.getmetrics()
    dx = int(size * 0.9) if dot else 0
    w, h = int(r - l + padx * 2 + dx), int(asc + desc * 0.5 + pady * 2)
    p = Pad(w, h)
    p.rect((0, 0, w - 1, h - 1), h // 2, fill=bg + (255,), outline=(border + (255,)) if border else None, width=3)
    if dot: p.ell((padx, h / 2 - size * 0.22, padx + size * 0.44, h / 2 + size * 0.22), fill=dot)
    p.text((padx + dx, h / 2), txt, size, fg, path, anchor='lm')
    im = p.img()
    if shadow: im = with_shadow(im, blur=12, off=6, alpha=0.18)
    _C[key] = im
    return im

# ---------------- backgrounds ----------------
yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
def bg_light(t, tint=WHITE, glow=GREEN, glow2=YEL):
    def mk():
        arr = np.zeros((H // 4, W // 4, 3), np.float32); arr[:] = tint
        return arr
    arr = cached(('bgbase', tint), mk).copy()
    for (cx, cy, r, c, a) in [(0.15 + 0.08 * math.sin(t * .5), 0.2, 90, glow, 0.10), (0.9, 0.78 + 0.05 * math.cos(t * .4), 100, glow2, 0.14)]:
        g = np.exp(-(((xx - cx * W / 4) ** 2 + (yy - cy * H / 4) ** 2) / (2 * r * r)))[..., None] * a
        arr = arr * (1 - g) + np.array(c, np.float32) * g
    im = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).convert('RGBA')
    im.alpha_composite(cached(('grid', tint), lambda: grid(tint)))
    return im

def grid(tint):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    c = DEEP + (14,)
    for x in range(0, W, 54): d.line((x, 0, x, H), fill=c, width=1)
    for y in range(0, H, 54): d.line((0, y, W, y), fill=c, width=1)
    return g

def bg_green(t):
    def mk():
        a = np.zeros((H // 4, W // 4, 3), np.float32)
        r = np.sqrt((xx - W / 8) ** 2 + (yy - H / 9) ** 2) / (H / 4)
        r = r[..., None]
        a[:] = np.array(GREEN2) * (1 - r) + np.array((8, 70, 38)) * r
        return a
    arr = cached('bgg', mk).copy()
    g = np.exp(-(((xx - (0.5 + 0.2 * math.sin(t)) * W / 4) ** 2 + (yy - 0.3 * H / 4) ** 2) / (2 * 80 * 80)))[..., None] * 0.18
    arr = arr * (1 - g) + np.array(YEL, np.float32) * g
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).convert('RGBA')

def ghost_word(base, txt, t, y, color, alpha=0.08, speed=40):
    im = cached(('ghost', txt, color), lambda: outline_text(txt, 330, color))
    x = W / 2 - (t * speed) % 200 + 100
    put(base, im, x, y, alpha=alpha)

def outline_text(txt, size, color):
    f = font(PB, size); l, t, r, b = f.getbbox(txt)
    im = Image.new('RGBA', (r - l + 40, b - t + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - l, 20 - t), txt, font=f, fill=(0, 0, 0, 0), stroke_width=4, stroke_fill=color + (255,))
    return im

# ---------------- headline ----------------
def headline(base, t, t0, rows, y0=330, dark=False):
    """rows: list of (start_time, segs). Each row slides up + fades in."""
    y = y0
    for (ts, segs) in rows:
        im = line_img(segs)
        p = eo(prog(t, ts, 0.45))
        if p > 0:
            put(base, im, W / 2, y + (1 - p) * 40, alpha=p)
        y += im.height - 22

def accent(txt, size, color=GREEN): return (txt, size, color, PF)
def bold(txt, size, color=DEEP): return (txt, size, color, PB)

# ---------------- top bar ----------------
METER = [(0, 40), (4.4, 22), (8.4, 22), (11.1, 12), (12.4, 12), (13.2, 6), (15.0, 6), (16.0, 48), (17.6, 62), (19.0, 71), (21.0, 72), (22.6, 80), (24.2, 86), (26.8, 87), (28.4, 94), (30.0, 94), (31.6, 97), (33.0, 99), (36.5, 99)]
def meter(t):
    for (a, va), (b, vb) in zip(METER, METER[1:]):
        if a <= t <= b: return lerp(va, vb, eio((t - a) / max(0.01, min(0.8, b - a))))
    return 99

def topbar(base, t, dark=False):
    fg = WHITE if dark else DEEP
    bgc = (255, 255, 255) if not dark else (16, 90, 50)
    left = pill('SHRI TECH  ·  ☎ 9993615146', 24, bg=bgc, fg=fg, path=FB, padx=20, pady=10, dot=YEL if dark else GREEN, shadow=not dark)
    put(base, left, 40 + left.width / 2 - 14, 120)
    v = meter(t)
    key = ('meter', int(v), dark)
    def mk():
        w, h = 330, 52
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), h // 2, fill=bgc + (255,))
        p.text((20, h / 2), 'रिपीट क्लाइंट्स', 21, fg, FB, anchor='lm')
        x0, x1 = 178, 262
        p.rect((x0, h / 2 - 4, x1, h / 2 + 4), 4, fill=(fg + (50,)))
        col = YEL if (dark or v > 30) else (234, 179, 8)
        p.rect((x0, h / 2 - 4, x0 + (x1 - x0) * v / 100, h / 2 + 4), 4, fill=(GREEN if v > 30 else col) + (255,))
        p.text((w - 18, h / 2), f'{int(v)}%', 21, fg, FB, anchor='rm')
        im = p.img()
        return with_shadow(im, blur=12, off=6, alpha=0.18) if not dark else im
    im = cached(key, mk)
    put(base, im, W - 40 - im.width / 2 + (14 if not dark else 0), 120)

# ---------------- captions ----------------
CAP_Y = 1450
def word_img(txt, size, fg):
    return text_img(txt, size, fg, PB)

def draw_caption(base, t, dark=False):
    gi = None
    for i, (a, b) in enumerate(SPANS):
        if a <= t < b: gi = i
    if gi is None: return
    g = GROUPS[gi]
    size = 60
    f = font(PB, size)
    sp = 22
    ws = [f.getlength(w[1]) for w in g]
    total = sum(ws) + sp * (len(g) - 1)
    x = W / 2 - total / 2
    a0, b0 = SPANS[gi]
    fade = min(prog(t, a0, 0.12), 1 - prog(t, b0 - 0.1, 0.1))
    base_fg = WHITE if dark else DEEP
    for k, (w, wd) in enumerate(zip(g, ws)):
        st = w[0]
        nxt = g[k + 1][0] if k + 1 < len(g) else 99
        style = w[2] if len(w) > 2 else ''
        active = st <= t < nxt
        said = t >= st
        cx = x + wd / 2
        if active:
            pp = eback(prog(t, st, 0.18))
            if style == 'y': bgc, fg = YEL, DEEP
            elif style == 'g': bgc, fg = GREEN, WHITE
            else: bgc, fg = (WHITE, DEEP) if dark else (DEEP, WHITE)
            box = cached(('cbox', w[1], bgc, fg), lambda: cap_box(w[1], wd, bgc, fg))
            put(base, box, cx, CAP_Y, scale=0.85 + 0.15 * pp, alpha=fade)
        else:
            im = word_img(w[1], size, base_fg)
            put(base, im, cx, CAP_Y, alpha=fade * (1.0 if said else 0.32))
        x += wd + sp

def cap_box(txt, wd, bgc, fg):
    f = font(PB, 60)
    asc, desc = f.getmetrics()
    w, h = int(wd + 34), 92
    p = Pad(w, h)
    p.rect((0, 0, w - 1, h - 1), 18, fill=bgc + (255,))
    p.text((w / 2, h / 2 + 2), txt, 60, fg, PB, anchor='mm')
    return with_shadow(p.img(), blur=10, off=6, alpha=0.25)

# ================= illustrations =================
def plant(h=170):
    def mk():
        p = Pad(110, h + 20)
        p.rect((25, h - 50, 85, h + 10), 10, fill=YEL + (255,))
        for ang, ln in [(-30, 0.8), (-8, 1.0), (14, 0.9), (34, 0.7)]:
            cx = 55; cy = h - 45
            ex = cx + math.sin(math.radians(ang)) * (h - 60) * ln
            ey = cy - math.cos(math.radians(ang)) * (h - 60) * ln
            p.line([(cx, cy), (ex, ey)], GREEN2 + (255,), 5)
            for k in (0.45, 0.75):
                lx, ly = lerp(cx, ex, k), lerp(cy, ey, k)
                p.ell((lx - 16, ly - 9, lx + 16, ly + 9), fill=GREEN + (255,))
            p.ell((ex - 14, ey - 18, ex + 14, ey + 10), fill=GREEN + (255,))
        return p.img()
    return cached(('plant', h), mk)

def mirror_station(bulb_phase):
    w, h = 660, 560
    key = ('mirror', int(bulb_phase * 6) % 6)
    def mk():
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 40, fill=WHITE + (255,))
        p.rect((0, h - 120, w - 1, h - 1), 40, fill=MINT + (255,))
        # mirror arch
        mx0, mx1, my0, my1 = 190, 470, 70, 380
        p.rect((mx0 - 14, my0 - 14, mx1 + 14, my1 + 14), 150, fill=YEL + (255,))
        p.rect((mx0, my0, mx1, my1), 140, fill=MINT2 + (255,))
        p.poly([(mx0 + 40, my1 - 30), (mx0 + 150, my0 + 60), (mx0 + 190, my0 + 60), (mx0 + 80, my1 - 30)], fill=WHITE + (120,))
        # bulbs around arch
        n = 13
        for i in range(n):
            a = math.pi + math.pi * i / (n - 1)
            if a <= 2 * math.pi:
                cx = (mx0 + mx1) / 2 + math.cos(a) * ((mx1 - mx0) / 2 + 30)
                cy = my0 + 140 + math.sin(a) * 175 if True else 0
                on = (i + int(bulb_phase * 6)) % 3 != 0
                if on: p.ell((cx - 20, cy - 20, cx + 20, cy + 20), fill=YEL2 + (90,))
                p.ell((cx - 11, cy - 11, cx + 11, cy + 11), fill=(YEL if on else PALEY) + (255,), outline=(234, 179, 8, 255), width=2)
        for side in (mx0 - 45, mx1 + 45):
            for cy in (250, 320):
                on = int(bulb_phase * 6 + cy) % 2 == 0
                p.ell((side - 11, cy - 11, side + 11, cy + 11), fill=(YEL if on else PALEY) + (255,), outline=(234, 179, 8, 255), width=2)
        # counter
        p.rect((80, 395, 580, 425), 10, fill=GREEN2 + (255,))
        for bx, bh, c in [(130, 46, YEL), (165, 34, GREEN), (480, 40, WHITE), (515, 54, YEL)]:
            p.rect((bx, 395 - bh, bx + 24, 395), 6, fill=c + (255,), outline=DEEP + (255,), width=2)
        # chair
        p.rect((255, 300, 405, 420), 40, fill=DEEP + (255,))
        p.rect((235, 420, 425, 460), 20, fill=DEEP + (255,))
        p.rect((318, 460, 342, 510), 6, fill=DEEP + (255,))
        p.rect((270, 505, 390, 522), 8, fill=DEEP + (255,))
        im = p.img()
        for x in (70, 590):
            pl = plant(190); im.alpha_composite(pl, (x - 55, 520 - pl.height))
        return with_shadow(im, blur=30, off=20, alpha=0.18)
    return cached(key, mk)

def tag(txt, sub, bg=YEL, fg=DEEP, size=64, rot=0):
    def mk():
        f = font(PB, size)
        w = int(f.getlength(txt) + 90); h = int(size * 1.9)
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 24, fill=bg + (255,))
        p.ell((22, h / 2 - 10, 42, h / 2 + 10), fill=DEEP + (255,))
        p.text((w / 2 + 16, h * 0.42), txt, size, fg, PB, anchor='mm')
        p.text((w / 2 + 16, h * 0.80), sub, int(size * 0.32), GREEN2 if bg != GREEN else WHITE, PB, anchor='mm')
        return with_shadow(p.img(), blur=16, off=10, alpha=0.25)
    return cached(('tag', txt, sub, bg, fg, size), mk)

def person(phase, walking=True, scale=1.0):
    """Small walking customer figure (~190px tall)."""
    key = ('person', round(phase % 1, 2) if walking else -1)
    def mk():
        w, h = 120, 240
        p = Pad(w, h)
        sw = math.sin(phase * 2 * math.pi) * (22 if walking else 0)
        hip = (60, 150)
        for s in (1, -1):
            ang = math.radians(sw * s)
            kx = hip[0] + math.sin(ang) * 75; ky = hip[1] + math.cos(ang) * 75
            p.line([hip, (kx, ky)], DEEP + (255,), 16)
            p.rect((kx - 12 + 8 * s * 0, ky - 4, kx + 16, ky + 8), 4, fill=DEEP + (255,))
        for s in (1, -1):
            ang = math.radians(-sw * s * 0.8)
            p.line([(60, 70), (60 + math.sin(ang) * 60, 70 + math.cos(ang) * 60)], SKIN + (255,), 12)
        p.rect((36, 58, 84, 158), 20, fill=WHITE + (255,), outline=GREEN2 + (255,), width=3)
        p.ell((38, 4, 82, 50), fill=SKIN + (255,))
        p.pie((36, 0, 84, 40), 180, 360, fill=HAIR + (255,))
        return p.img()
    return cached(key, mk)

def door():
    def mk():
        w, h = 360, 560
        p = Pad(w, h)
        p.rect((20, 60, w - 20, h), 150, fill=YEL + (255,))
        p.rect((40, 80, w - 40, h), 135, fill=PALEY + (255,))
        p.rect((60, 100, w - 60, h), 120, fill=WHITE + (255,))
        p.rect((w / 2 - 70, 0, w / 2 + 70, 50), 14, fill=DEEP + (255,))
        p.text((w / 2, 25), 'SALON', 26, YEL, PB, anchor='mm')
        return p.img()
    return cached('door', mk)

def search_bar(txt, caret):
    w, h = 600, 86
    p = Pad(w, h)
    p.rect((0, 0, w - 1, h - 1), h // 2, fill=WHITE + (255,), outline=MINT2 + (255,), width=3)
    p.ell((30, 26, 58, 54), outline=DEEP + (255,), width=4); p.line([(54, 50), (66, 62)], DEEP + (255,), 5)
    p.text((88, h / 2), txt + ('|' if caret else ''), 30, DEEP, FM, anchor='lm')
    return with_shadow(p.img(), blur=14, off=8, alpha=0.18)

def price_card(k_new, strike_p):
    """k_new 0..1 shows discounted prices."""
    key = ('price', round(k_new, 2), round(strike_p, 2))
    def mk():
        w, h = 600, 520
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 30, fill=WHITE + (255,), outline=MINT2 + (255,), width=4)
        p.text((w / 2, 70), 'S E R V I C E S', 34, DEEP, PB, anchor='mm')
        p.line([(220, 108), (380, 108)], YEL + (255,), 4)
        rows = [('हेयरकट', '₹800', '₹240'), ('हेयर स्पा', '₹1,800', '₹540'), ('केराटिन', '₹4,500', '₹1,350'), ('ग्लोबल कलर', '₹3,200', '₹960')]
        for i, (n, old, new) in enumerate(rows):
            y = 170 + i * 88
            p.text((50, y), n, 32, DEEP, FB, anchor='lm')
            f = font(PB, 32)
            if k_new <= 0:
                p.text((w - 50, y), old, 32, DEEP, PB, anchor='rm')
            else:
                p.text((w - 50, y - 18), old, 24, (DEEP[0], DEEP[1], DEEP[2], 140), FB, anchor='rm')
                lw = f.getlength(old) * 0.75
                p.line([(w - 50 - lw * strike_p, y - 18), (w - 50, y - 18)], GREEN2 + (255,), 3)
                if k_new > 0.3:
                    p.text((w - 50, y + 18), new, 36, GREEN2, PB, anchor='rm')
            if i < 3: p.line([(50, y + 44), (w - 50, y + 44)], MINT2 + (255,), 2)
        return with_shadow(p.img(), blur=26, off=16, alpha=0.2)
    return cached(key, mk)

def badge(txt, sub, r=110, bg=YEL, fg=DEEP):
    def mk():
        p = Pad(r * 2 + 20, r * 2 + 20)
        n = 24
        pts = []
        for i in range(n * 2):
            a = math.pi * i / n
            rr = r if i % 2 == 0 else r * 0.88
            pts.append((r + 10 + math.cos(a) * rr, r + 10 + math.sin(a) * rr))
        p.poly(pts, fill=bg + (255,))
        p.text((r + 10, r - 6), txt, int(r * 0.55), fg, PB, anchor='mm')
        p.text((r + 10, r + r * 0.45), sub, int(r * 0.22), fg, PB, anchor='mm')
        return with_shadow(p.img(), blur=14, off=8, alpha=0.25)
    return cached(('badge', txt, sub, r, bg), mk)

def stamp(txt):
    def mk():
        f = font(PB, 64); w = int(f.getlength(txt) + 80); h = 120
        p = Pad(w, h)
        p.rect((4, 4, w - 5, h - 5), 16, outline=DEEP + (255,), width=8)
        p.rect((14, 14, w - 15, h - 15), 10, fill=YEL + (230,))
        p.text((w / 2, h / 2 + 2), txt, 64, DEEP, PB, anchor='mm')
        return p.img()
    return cached(('stamp', txt), mk)

def face(p, cx, cy, s=1.0, mood='calm', hair=HAIR, styled=True):
    """Draw a stylised client bust onto Pad p (centre of face at cx, cy)."""
    # hair back
    if styled:
        p.rect((cx - 120 * s, cy - 130 * s, cx + 120 * s, cy + 210 * s), 110 * s, fill=hair + (255,))
    else:
        for k in range(9):
            a = -0.9 + k * 0.22
            p.line([(cx + math.sin(a) * 90 * s, cy - 60 * s), (cx + math.sin(a) * 150 * s, cy + 160 * s + (k % 3) * 20 * s)], hair + (255,), int(26 * s))
    # shoulders
    p.pie((cx - 190 * s, cy + 150 * s, cx + 190 * s, cy + 420 * s), 180, 360, fill=GREEN2 + (255,))
    p.rect((cx - 28 * s, cy + 70 * s, cx + 28 * s, cy + 170 * s), 14 * s, fill=SKIN + (255,))
    p.ell((cx - 88 * s, cy - 100 * s, cx + 88 * s, cy + 110 * s), fill=SKIN + (255,))
    # fringe
    p.pie((cx - 96 * s, cy - 120 * s, cx + 96 * s, cy + 40 * s), 180, 360, fill=hair + (255,))
    if styled:
        p.rect((cx - 120 * s, cy - 50 * s, cx - 72 * s, cy + 200 * s), 24 * s, fill=hair + (255,))
        p.rect((cx + 72 * s, cy - 50 * s, cx + 120 * s, cy + 200 * s), 24 * s, fill=hair + (255,))
    ec = DEEP + (255,)
    if mood == 'happy':
        p.arc((cx - 52 * s, cy - 6 * s, cx - 18 * s, cy + 24 * s), 200, 340, ec, 6 * s)
        p.arc((cx + 18 * s, cy - 6 * s, cx + 52 * s, cy + 24 * s), 200, 340, ec, 6 * s)
        p.pie((cx - 36 * s, cy + 30 * s, cx + 36 * s, cy + 80 * s), 0, 180, fill=DEEP + (255,))
    else:
        p.arc((cx - 52 * s, cy - 10 * s, cx - 18 * s, cy + 16 * s), 20, 160, ec, 6 * s)
        p.arc((cx + 18 * s, cy - 10 * s, cx + 52 * s, cy + 16 * s), 20, 160, ec, 6 * s)
        p.arc((cx - 24 * s, cy + 36 * s, cx + 24 * s, cy + 66 * s), 20, 160, ec, 6 * s)
    p.ell((cx - 66 * s, cy + 24 * s, cx - 40 * s, cy + 42 * s), fill=YEL + (110,))
    p.ell((cx + 40 * s, cy + 24 * s, cx + 66 * s, cy + 42 * s), fill=YEL + (110,))

def portrait_card(label, mood='calm', w=480, h=600, bg1=YEL2, bg2=GREEN, styled=True, dark=False):
    def mk():
        p = Pad(w, h)
        g = Image.new('RGBA', (w * 2, h * 2))
        a = np.linspace(0, 1, h * 2)[:, None, None]
        c1 = np.array((16, 90, 50) if dark else bg1); c2 = np.array(DEEP if dark else bg2)
        arr = np.broadcast_to((c1 * (1 - a) + c2 * a), (h * 2, w * 2, 3)).astype(np.uint8)
        g = Image.fromarray(np.dstack([arr, np.full((h * 2, w * 2), 255, np.uint8)]), 'RGBA')
        m = Image.new('L', g.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), 60, fill=255)
        p.im.paste(g, (0, 0), m)
        if label:
            p.rect((30, 28, 30 + font(PB, 20).getlength(label) + 36, 70), 10, fill=(DEEP if not dark else YEL) + (255,))
            p.text((48, 49), label, 20, YEL if not dark else DEEP, PB, anchor='lm')
        face(p, w / 2, h * 0.47, s=w / 520, mood=mood, styled=styled)
        im = p.img()
        m2 = Image.new('L', (w, h), 0); ImageDraw.Draw(m2).rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')), np.array(m2))))
        return with_shadow(im, blur=30, off=20, alpha=0.25)
    return cached(('portrait', label, mood, w, h, bg1, bg2, styled, dark), mk)

def bubble(txt, size=30, w=None):
    def mk():
        f = font(FB, size); tw = f.getlength(txt)
        ww = int(tw + 60); h = int(size * 2.4)
        p = Pad(ww, h + 20)
        p.rect((0, 0, ww - 1, h), 24, fill=WHITE + (255,))
        p.poly([(40, h - 2), (70, h - 2), (36, h + 18)], fill=WHITE + (255,))
        p.text((ww / 2, h / 2), txt, size, DEEP, FB, anchor='mm')
        return with_shadow(p.img(), blur=14, off=8, alpha=0.22)
    return cached(('bubble', txt, size), mk)

def sparkle(base, x, y, t, t0, size=26, col=YEL):
    p = prog(t, t0, 0.5)
    if p <= 0: return
    s = math.sin(p * math.pi) if p < 1 else 0.6 + 0.4 * math.sin(t * 6 + x)
    im = cached(('spark', size, col), lambda: spark_img(size, col))
    put(base, im, x, y, scale=max(0.05, s), rot=t * 40)

def spark_img(size, col):
    p = Pad(size * 2, size * 2)
    c = size
    p.poly([(c, 0), (c + size * .25, c - size * .25), (2 * c, c), (c + size * .25, c + size * .25), (c, 2 * c), (c - size * .25, c + size * .25), (0, c), (c - size * .25, c - size * .25)], fill=col + (255,))
    return p.img()

def heart_img(size=40, col=GREEN):
    def mk():
        p = Pad(size, size)
        r = size / 4
        p.ell((0, 0, size / 2 + 2, size / 2 + 2), fill=col + (255,))
        p.ell((size / 2 - 2, 0, size, size / 2 + 2), fill=col + (255,))
        p.poly([(1, size * .33), (size - 1, size * .33), (size / 2, size)], fill=col + (255,))
        return p.img()
    return cached(('heart', size, col), mk)

def phone_card(i, likes):
    w, h = 250, 440
    key = ('pc', i, likes)
    def mk():
        bgs = [(YEL2, GREEN), (MINT2, GREEN2), (PALEY, YEL)]
        base = portrait_card(None, 'happy' if i == 1 else 'calm', w, h, bg1=bgs[i][0], bg2=bgs[i][1])
        im = base.copy()
        d = Pad(im.width, im.height)
        ox = (im.width - w) / 2; oy = (im.height - h) / 2 - 10
        d.ell((ox + w / 2 - 34, oy + h * 0.47 - 34, ox + w / 2 + 34, oy + h * 0.47 + 34), fill=WHITE + (200,))
        d.poly([(ox + w / 2 - 10, oy + h * .47 - 16), (ox + w / 2 - 10, oy + h * .47 + 16), (ox + w / 2 + 16, oy + h * .47)], fill=DEEP + (255,))
        d.rect((ox + 16, oy + h - 56, ox + 130, oy + h - 16), 20, fill=WHITE + (235,))
        d.text((ox + 30, oy + h - 36), f'♥ {likes}', 22, GREEN2, FSYM, anchor='lm')
        im.alpha_composite(d.img())
        return im
    return cached(key, mk)

def calendar(filled, booked):
    key = ('cal', filled, booked)
    def mk():
        w, h = 560, 600
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 30, fill=WHITE + (255,))
        p.rect((0, 0, w - 1, 100), 30, fill=DEEP + (255,)); p.rect((0, 60, w - 1, 100), 0, fill=DEEP + (255,))
        p.text((36, 52), 'बुकिंग्स', 32, YEL, PB, anchor='lm')
        p.text((w - 36, 52), 'इस हफ़्ते', 24, WHITE, FB, anchor='rm')
        days = 'सो मं बु गु शु श र'.split()
        for j, dname in enumerate(days):
            p.text((62 + j * 72, 140), dname, 22, DEEP, FB, anchor='mm')
        order = [(r, c) for r in range(4) for c in range(7)]
        rnd = random.Random(3); rnd.shuffle(order)
        on = set(order[:filled])
        for r in range(4):
            for c in range(7):
                x, y = 34 + c * 72, 180 + r * 82
                if (r, c) in on:
                    p.rect((x, y, x + 56, y + 56), 12, fill=(GREEN if (r + c) % 3 else YEL) + (255,))
                    p.line([(x + 15, y + 29), (x + 25, y + 40), (x + 42, y + 17)], (WHITE if (r + c) % 3 else DEEP) + (255,), 6)
                else:
                    p.rect((x, y, x + 56, y + 56), 12, fill=MINT + (255,), outline=MINT2 + (255,), width=2)
        p.text((w / 2, h - 40), f'स्लॉट बुक  {booked}/28', 28, DEEP, PB, anchor='mm')
        return with_shadow(p.img(), blur=30, off=20, alpha=0.2)
    return cached(key, mk)

def editor(play):
    w, h = 620, 640
    key = ('ed', round(play, 2))
    def mk():
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 30, fill=WHITE + (255,))
        p.ell((30, 28, 46, 44), fill=GREEN + (255,))
        p.text((58, 36), 'PREVIEW', 20, DEEP, PB, anchor='lm')
        p.text((w - 30, 36), '4K · 9:16', 20, DEEP, FB, anchor='rm')
        p.rect((30, 64, w - 30, 420), 20, fill=MINT + (255,))
        im = p.img()
        pc = portrait_card(None, 'happy', 200, 330, bg1=YEL2, bg2=GREEN)
        im.alpha_composite(pc, (int(w / 2 - pc.width / 2), int(242 - pc.height / 2)))
        q = Pad(w, h)
        q.text((30, 456), '00:00:' + f'{int(play * 15):02d}', 20, DEEP, FB, anchor='lm')
        q.text((w - 30, 456), 'TIMELINE', 20, DEEP, FB, anchor='rm')
        rows = [[(30, 190, GREEN), (200, 300, YEL), (310, 470, GREEN), (480, 590, YEL)],
                [(30, 140, YEL), (150, 330, MINT2), (340, 440, YEL), (450, 590, GREEN)]]
        for r, segs in enumerate(rows):
            for a, b, c in segs:
                q.rect((a, 490 + r * 56, b, 530 + r * 56), 10, fill=c + (255,))
        px = 30 + (w - 60) * play
        q.line([(px, 478), (px, 610)], DEEP + (255,), 4)
        q.poly([(px - 10, 474), (px + 10, 474), (px, 488)], fill=DEEP + (255,))
        im.alpha_composite(q.img())
        return with_shadow(im, blur=30, off=20, alpha=0.2)
    return cached(key, mk)

def logo(size=120):
    return cached(('logo', size), lambda: line_img([('Shri', size, DEEP, PB), ('Tech', size, GREEN, PB)], gap=6))

# ================= scenes =================
SC = [0.0, 4.4, 8.4, 12.35, 14.95, 18.95, 24.15, 26.6, 29.95, 32.7, 34.45, END]

def s1(t):
    b = bg_light(t)
    headline(b, t, 0, [(0.1, [bold('डिस्काउंट =', 96)]), (1.6, [bold('ज़्यादा', 84), accent('customers?', 96)])], y0=300)
    if t > 1.6:
        u = eo(prog(t, 1.9, 0.4)); d = ImageDraw.Draw(b)
        d.rounded_rectangle((W / 2 - 240, 520, W / 2 - 240 + 480 * u, 528), 4, fill=YEL)
    p = eback(prog(t, 0.0, 0.6))
    ms = mirror_station(t)
    put(b, ms, W / 2, 950 + (1 - p) * 120, scale=(0.9 + 0.1 * p) * (1 + 0.02 * t / 4.4), alpha=min(1, p * 2))
    if t > 3.0:
        q = eback(prog(t, 3.0, 0.45), 2.2)
        put(b, tag('50%', 'OFF'), 760, 760, scale=q, rot=-12 + 6 * math.sin((t - 3) * 5) * (1 - prog(t, 3, 1.2)))
    if t > 3.25:
        q = eback(prog(t, 3.25, 0.35))
        put(b, pill('कस्टमर्स  ↑  ?', 30, bg=DEEP, fg=YEL, path=PB), 330, 1180, scale=q)
    return b, False

def s2(t):
    b = bg_green(t)
    ghost_word(b, 'GALAT', t, 760, WHITE, 0.10)
    p = prog(t, 4.4, 0.35)
    sc = lerp(1.6, 1.0, eo(p))
    shake = (1 - prog(t, 4.75, 0.3)) * math.sin(t * 80) * 10 if t > 4.7 else 0
    put(b, text_img('गलत', 230, WHITE, PB), W / 2 + shake, 560, scale=sc, alpha=min(1, p * 3))
    q = eo(prog(t, 4.6, 0.4))
    put(b, text_img('soch!', 170, YEL, PF), W / 2, 790 + (1 - q) * 50, alpha=q)
    if t > 5.0:
        q = eo(prog(t, 5.0, 0.45))
        bar = 0.18 + 0.27 * eio(prog(t, 5.2, 1.4)) + 0.5 * eio(prog(t, 7.0, 1.1))
        secs = int(lerp(6, 34, bar))
        im = cached(('prog', round(bar, 2)), lambda: progress_card(bar, secs))
        put(b, im, W / 2, 1110 + (1 - q) * 80, alpha=q)
    if t > 6.75:
        q = eback(prog(t, 6.75, 0.4))
        put(b, pill('असली वजह  ·  लास्ट में  🔒', 30, bg=YEL, fg=DEEP, path=PB) if False else lockpill(), W / 2, 975, scale=q)
    return b, True

def lockpill():
    def mk():
        txt = 'असली वजह  ·  लास्ट में'
        f = font(PB, 30); tw = f.getlength(txt)
        w, h = int(tw + 110), 66
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), h // 2, fill=YEL + (255,))
        p.text((30, h / 2), txt, 30, DEEP, PB, anchor='lm')
        lx = 30 + tw + 22
        p.arc((lx, 14, lx + 26, 40), 180, 360, DEEP + (255,), 4)
        p.rect((lx - 4, 26, lx + 30, 52), 6, fill=DEEP + (255,))
        return with_shadow(p.img(), blur=12, off=6, alpha=0.3)
    return cached('lockpill', mk)

def progress_card(bar, secs):
    w, h = 720, 150
    p = Pad(w, h)
    p.rect((0, 0, w - 1, h - 1), 30, fill=(255, 255, 255, 40), outline=(255, 255, 255, 90), width=2)
    p.poly([(40, 38), (40, 66), (62, 52)], fill=YEL + (255,))
    p.text((80, 52), 'वीडियो एंड तक देखना', 30, WHITE, PB, anchor='lm')
    p.text((w - 40, 52), f'0:{secs:02d} / 0:35', 26, WHITE, FB, anchor='rm')
    p.rect((40, 100, w - 40, 112), 6, fill=(255, 255, 255, 70))
    x = 40 + (w - 80) * bar
    p.rect((40, 100, x, 112), 6, fill=YEL + (255,))
    p.ell((x - 16, 90, x + 16, 122), fill=WHITE + (255,))
    return p.img()

def s3(t):
    b = bg_light(t, tint=WHITE)
    headline(b, t, 8.4, [(8.45, [bold('एक बार', 100)]), (8.8, [accent('aayega...', 104)])], y0=290)
    floor_y = 1260
    d = ImageDraw.Draw(b)
    d.rounded_rectangle((140, floor_y, 940, floor_y + 6), 3, fill=MINT2)
    pin = eo(prog(t, 8.4, 0.5))
    put(b, door(), W / 2, floor_y - 280 + (1 - pin) * 60, alpha=pin)
    for x in (300, 780):
        pl = plant(170)
        put(b, pl, x, floor_y - pl.height / 2, alpha=pin)
    # visitor walks in, then walks out
    if t < 10.55:
        k = eio(prog(t, 9.3, 0.95))
        x = lerp(120, W / 2, k); sc = lerp(1.0, 0.82, k)
        walking = 0 < k < 1
        al = 1 - prog(t, 10.2, 0.3)
        put(b, person(t * 1.6, walking), x, floor_y - 120 * sc, scale=sc, alpha=al)
        if t > 9.85:
            put(b, pill('विज़िट 1', 26, bg=WHITE, fg=DEEP, path=PB, dot=GREEN), W / 2 + 120, 840, scale=eback(prog(t, 9.85, 0.35)))
    else:
        k = eio(prog(t, 10.6, 1.0))
        x = lerp(W / 2, 980, k); sc = lerp(0.82, 1.0, k)
        al = prog(t, 10.55, 0.2) * (1 - prog(t, 11.6, 0.3))
        im = person(t * 1.6, 0 < k < 1).transpose(Image.FLIP_LEFT_RIGHT)
        put(b, im, x, floor_y - 120 * sc, scale=sc, alpha=al)
    # discount tags orbiting
    if t > 11.0:
        q = eback(prog(t, 11.0, 0.4))
        for i, (tx, sub, bgc) in enumerate([('20%', 'OFF', YEL), ('₹99', 'FLAT', GREEN), ('30%', 'OFF', YEL)]):
            a = t * 1.2 + i * 2.1
            cx = W / 2 + math.cos(a) * 330; cy = 900 + math.sin(a) * 120
            put(b, tag(tx, sub, bg=bgc, fg=DEEP if bgc == YEL else WHITE, size=44), cx, cy, scale=q * 0.9, rot=math.sin(a) * 10)
    if t > 11.45:
        q = eo(prog(t, 11.45, 0.3))
        txt = 'discount near me'
        n = int(len(txt) * prog(t, 11.6, 0.6))
        put(b, search_bar(txt[:n], int(t * 4) % 2 == 0), W / 2, 1340 - 0 * q, alpha=q)
    return b, False

def s4(t):
    b = bg_light(t, tint=(255, 253, 240))
    ghost_word(b, 'SASTA', t, 780, DEEP, 0.06)
    headline(b, t, 12.35, [(12.4, [bold('सस्ता सैलून', 100)]), (12.75, [accent('image', 110)])], y0=290)
    p = eback(prog(t, 12.35, 0.5))
    sag = eio(prog(t, 13.9, 0.6))
    kn = eo(prog(t, 12.75, 0.4)); st = eo(prog(t, 12.75, 0.3))
    put(b, price_card(kn, st), W / 2, 980 + sag * 20, scale=0.9 + 0.1 * p, rot=-3 * sag, alpha=min(1, p * 2))
    if t > 13.1:
        q = eback(prog(t, 13.1, 0.5), 2.0)
        put(b, badge('70%', 'OFF', 110), 830, 740, scale=q, rot=(1 - q) * 120 + 8)
    if t > 13.5:
        q = prog(t, 13.5, 0.22)
        put(b, stamp('सस्ता सैलून'), W / 2 + 40, 1150, scale=lerp(1.8, 1.0, eo(q)), rot=-8, alpha=min(1, q * 2))
    return b, False

def s5(t):
    b = bg_light(t)
    headline(b, t, 14.95, [(15.0, [bold('याद रहता है', 96)]), (17.15, [accent('aapka kaam', 104)])], y0=290)
    p = eback(prog(t, 14.95, 0.55))
    fl = math.sin(t * 2) * 8
    put(b, portrait_card('TRANSFORMATION', 'calm'), W / 2, 990 + fl + (1 - p) * 100, scale=0.92 + 0.08 * p, alpha=min(1, p * 2))
    if t > 15.4:
        q = eback(prog(t, 15.4, 0.35))
        put(b, pill('↻  वापस आई', 28, bg=WHITE, fg=DEEP, path=PB), 300, 780 + fl, scale=q)
    if t > 15.7:
        v = 2 if t < 16.0 else (3 if t < 17.55 else 4)
        q = eback(prog(t, 15.7, 0.35))
        bump = 1 + 0.15 * (1 - prog(t, 16.0, 0.25)) * (t > 16.0) + 0.15 * (1 - prog(t, 17.55, 0.25)) * (t > 17.55)
        put(b, pill(f'विज़िट {v}', 30, bg=DEEP, fg=YEL, path=PB), 310, 1210 + fl, scale=q * bump)
    for i, (x, y, t0) in enumerate([(820, 760, 16.1), (260, 980, 16.6), (850, 1180, 17.2)]):
        sparkle(b, x, y + fl, t, t0, 30, YEL if i % 2 == 0 else GREEN)
    if t > 17.9:
        q = eback(prog(t, 17.9, 0.4))
        put(b, bubble('“वही स्टाइलिस्ट चाहिए!”', 30), 790, 1040 + fl, scale=q)
    return b, False

def s6(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 18.95, [(19.0, [bold('BEFORE', 92), ('→', 80, DEEP, FSYM), accent('after', 110)])], y0=330)
    cy = 960
    if t < 20.75:
        p = eback(prog(t, 18.95, 0.5))
        before = portrait_card(None, 'calm', 560, 700, bg1=(236, 240, 236), bg2=(214, 222, 216), styled=False)
        after = portrait_card(None, 'happy', 560, 700, bg1=YEL2, bg2=GREEN)
        split = lerp(0.92, 0.12, eio(prog(t, 19.15, 1.4)))
        im = before.copy()
        cut = int(after.width * split)
        im.paste(after.crop((cut, 0, after.width, after.height)), (cut, 0))
        dd = ImageDraw.Draw(im)
        dd.rectangle((cut - 3, 70, cut + 3, after.height - 90), fill=WHITE)
        dd.ellipse((cut - 26, after.height / 2 - 26, cut + 26, after.height / 2 + 26), fill=WHITE, outline=DEEP, width=3)
        dd.text((cut, after.height / 2), '‹ ›', font=font(FSYM, 26), fill=DEEP, anchor='mm')
        put(b, im, W / 2, cy + (1 - p) * 80, scale=0.9 + 0.1 * p, alpha=min(1, p * 2))
        put(b, pill('BEFORE', 24, bg=DEEP, fg=WHITE, path=PB), 300, 680, alpha=min(1, p * 2))
        put(b, pill('AFTER ✦', 24, bg=YEL, fg=DEEP, path=PB), 790, 680, alpha=min(1, p * 2) * prog(t, 19.75, 0.3))
    elif t < 22.55:
        p = eback(prog(t, 20.75, 0.45))
        put(b, portrait_card('CLIENT REACTION', 'happy', 560, 700, bg1=PALEY, bg2=YEL), W / 2, cy, scale=0.85 + 0.15 * p, rot=(1 - p) * 6, alpha=min(1, p * 2))
        for i in range(6):
            ph = (t - 20.9 - i * 0.25)
            if ph > 0:
                k = (ph % 1.5) / 1.5
                put(b, heart_img(46, GREEN if i % 2 else YEL), 300 + i * 95 + math.sin(ph * 4) * 20, 1180 - k * 500, alpha=math.sin(k * math.pi))
        if t > 21.4:
            q = eback(prog(t, 21.4, 0.4))
            put(b, stars_pill(), W / 2, 1250, scale=q)
    else:
        p = eback(prog(t, 22.55, 0.45))
        put(b, team_card(), W / 2, cy, scale=0.85 + 0.15 * p, rot=(1 - p) * -6, alpha=min(1, p * 2))
        if t > 22.75:
            put(b, pill('कलर', 26, bg=YEL, fg=DEEP, path=PB), 380, 1250, scale=eback(prog(t, 22.75, 0.3)))
            put(b, pill('कट', 26, bg=WHITE, fg=DEEP, path=PB), 700, 1250, scale=eback(prog(t, 23.0, 0.3)))
        for x, y, t0 in [(250, 720, 23.5), (840, 820, 23.65), (820, 1150, 23.8)]:
            sparkle(b, x, y, t, t0, 30)
    return b, False

def stars_pill():
    def mk():
        w, h = 420, 84
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), h // 2, fill=WHITE + (255,))
        for i in range(5):
            cx, cy, r = 50 + i * 40, h / 2, 16
            pts = []
            for k in range(10):
                a = -math.pi / 2 + k * math.pi / 5
                rr = r if k % 2 == 0 else r * 0.45
                pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
            p.poly(pts, fill=YEL + (255,))
        p.text((250, h / 2), '“So pretty!”', 30, DEEP, PB, anchor='lm')
        return with_shadow(p.img(), blur=14, off=8, alpha=0.22)
    return cached('stars', mk)

def team_card():
    def mk():
        w, h = 560, 700
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 30, fill=DEEP + (255,))
        p.rect((30, 28, 330, 70), 10, fill=YEL + (255,))
        p.text((48, 49), 'YOUR TEAM · YOUR STYLE', 20, DEEP, PB, anchor='lm')
        im = p.img()
        for i, (x, mood) in enumerate([(180, 'calm'), (390, 'happy')]):
            q = Pad(w, h)
            s = 0.62
            cx, cy = x, 360
            q.pie((cx - 150 * s, cy + 160 * s, cx + 150 * s, cy + 480 * s), 180, 360, fill=(GREEN if i else YEL) + (255,))
            q.ell((cx - 80 * s, cy - 90 * s, cx + 80 * s, cy + 100 * s), fill=SKIN + (255,))
            q.pie((cx - 90 * s, cy - 120 * s, cx + 90 * s, cy + 40 * s), 180, 360, fill=(YEL2 if i else (5, 40, 22)) + (255,))
            if i == 0: q.ell((cx - 40 * s, cy - 190 * s, cx + 40 * s, cy - 110 * s), fill=(5, 40, 22, 255))
            q.arc((cx - 40 * s, cy - 10 * s, cx - 10 * s, cy + 15 * s), 200 if mood == 'happy' else 20, 340 if mood == 'happy' else 160, DEEP + (255,), 5)
            q.arc((cx + 10 * s, cy - 10 * s, cx + 40 * s, cy + 15 * s), 200 if mood == 'happy' else 20, 340 if mood == 'happy' else 160, DEEP + (255,), 5)
            q.arc((cx - 22 * s, cy + 30 * s, cx + 22 * s, cy + 60 * s), 20, 160, DEEP + (255,), 5)
            im.alpha_composite(q.img())
        # scissors icon
        q = Pad(w, h)
        q.ell((420, 560, 460, 600), outline=YEL + (255,), width=5); q.ell((470, 560, 510, 600), outline=YEL + (255,), width=5)
        q.line([(450, 565), (500, 470)], YEL + (255,), 5); q.line([(480, 565), (430, 470)], YEL + (255,), 5)
        im.alpha_composite(q.img())
        return with_shadow(im, blur=30, off=20, alpha=0.3)
    return cached('team', mk)

def s7(t):
    b = bg_light(t)
    headline(b, t, 24.15, [(24.2, [bold('रोज़ दिखाओ', 100)]), (24.95, [accent('apna kaam.', 104)])], y0=290)
    starts = [24.2, 24.55, 24.75]
    pos = [(W / 2 - 290, 980, -8), (W / 2, 950, 0), (W / 2 + 290, 980, 8)]
    for i in (0, 2, 1):
        t0 = starts[i]
        if t < t0: continue
        q = eback(prog(t, t0, 0.45))
        likes = ['1.2K', '3.8K', '940'][i]
        if t > 25.4: likes = ['2.6K', '7.4K', '1.9K'][i]
        x, y, r = pos[i]
        put(b, phone_card(i, likes), x, y + (1 - q) * 200 + math.sin(t * 2 + i) * 6, scale=(0.95 if i != 1 else 1.08) * (0.7 + 0.3 * q), rot=r * q, alpha=min(1, q * 2))
    for i in range(5):
        ph = t - 25.0 - i * 0.2
        if ph > 0:
            k = (ph % 1.2) / 1.2
            put(b, heart_img(40, GREEN if i % 2 else YEL), 380 + i * 80, 1150 - k * 420, alpha=math.sin(k * math.pi))
    if t > 24.75:
        q = eo(prog(t, 24.75, 0.3))
        n = int(7 * prog(t, 25.0, 1.3) + 0.999) if t > 25.0 else 0
        put(b, cached(('week', n), lambda: week_pill(n)), W / 2, 1290, alpha=q)
    return b, False

def week_pill(n):
    w, h = 640, 84
    p = Pad(w, h)
    p.rect((0, 0, w - 1, h - 1), h // 2, fill=WHITE + (255,))
    p.text((34, h / 2), 'रोज़ पोस्ट', 26, DEEP, PB, anchor='lm')
    for i, dname in enumerate('सो मं बु गु शु श र'.split()):
        cx = 220 + i * 58
        on = i < n
        p.ell((cx - 23, h / 2 - 23, cx + 23, h / 2 + 23), fill=(GREEN if on else MINT) + (255,))
        if on: p.line([(cx - 10, h / 2), (cx - 2, h / 2 + 9), (cx + 12, h / 2 - 9)], WHITE + (255,), 5)
        else: p.text((cx, h / 2), dname, 18, DEEP, FB, anchor='mm')
    return with_shadow(p.img(), blur=14, off=8, alpha=0.2)

def s8(t):
    b = bg_light(t)
    headline(b, t, 26.6, [(26.65, [bold('प्राइस नहीं,', 100)]), (28.35, [accent('appointments.', 100)])], y0=290)
    if t < 28.3:
        q = eback(prog(t, 26.7, 0.4))
        put(b, cached('pq', lambda: strike_chip('प्राइस क्या है?', 0)), W / 2 - 120, 820, scale=q)
        if t > 27.2:
            k = eo(prog(t, 27.2, 0.35))
            put(b, cached(('pqs', round(k, 2)), lambda: strike_chip('प्राइस क्या है?', k)), W / 2 - 120, 820)
        q2 = eback(prog(t, 26.95, 0.4))
        put(b, tag('₹ ???', 'PRICE', bg=YEL, size=70), W / 2 + 170, 1050, scale=q2 * (1 - 0.3 * prog(t, 27.6, 0.5)), rot=6, alpha=1 - 0.5 * prog(t, 27.6, 0.5))
        put(b, calendar(0, 0), W / 2, 1060, scale=0.5, alpha=0.35 * prog(t, 27.4, 0.5))
    else:
        q = eback(prog(t, 28.3, 0.5))
        k = prog(t, 28.5, 1.4)
        filled = int(6 + 18 * eio(k))
        put(b, calendar(filled, filled), W / 2, 1010, scale=0.6 + 0.4 * q, alpha=min(1, q * 2))
    return b, False

def strike_chip(txt, k):
    f = font(PB, 34); tw = f.getlength(txt)
    w, h = int(tw + 70), 80
    p = Pad(w, h + 20)
    p.rect((0, 0, w - 1, h), 24, fill=WHITE + (255,))
    p.poly([(40, h - 2), (70, h - 2), (36, h + 18)], fill=WHITE + (255,))
    p.text((w / 2, h / 2), txt, 34, DEEP, PB, anchor='mm')
    if k > 0: p.line([(30, h / 2), (30 + (w - 60) * k, h / 2)], GREEN2 + (255,), 6)
    return with_shadow(p.img(), blur=14, off=8, alpha=0.22)

def s9(t):
    b = bg_light(t, tint=YEL2, glow=WHITE, glow2=GREEN)
    ghost_word(b, 'CONTENT', t, 1050, DEEP, 0.07)
    # LESS discount
    p = eo(prog(t, 29.95, 0.4))
    shrink = eio(prog(t, 30.55, 0.6))
    y = lerp(720, 1180, eio(prog(t, 31.5, 0.5)))
    sc = lerp(1.0, 0.62, shrink)
    al = p * lerp(1.0, 0.5, eio(prog(t, 31.5, 0.5)))
    put(b, text_img('कम', 50, DEEP, PB), W / 2, y - 120 * sc, scale=sc, alpha=al)
    put(b, text_img('डिस्काउंट।', 150, DEEP, PB), W / 2, y, scale=sc, alpha=al)
    if t > 30.15 and t < 31.6:
        k = eo(prog(t, 30.75, 0.4))
        d = ImageDraw.Draw(b)
        if k > 0: d.rounded_rectangle((W / 2 - 330 * sc, y - 6, W / 2 - 330 * sc + 660 * sc * k, y + 8), 6, fill=GREEN2)
    if t > 31.5:
        q = eback(prog(t, 31.5, 0.5))
        put(b, text_img('ज़्यादा', 54, DEEP, PB), W / 2, 600, alpha=prog(t, 31.5, 0.3))
        put(b, text_img('content.', 230, DEEP, PF), W / 2, 790, scale=0.7 + 0.3 * q, alpha=min(1, q * 2))
        u = eo(prog(t, 31.8, 0.4))
        d = ImageDraw.Draw(b)
        d.rounded_rectangle((W / 2 - 300, 930, W / 2 - 300 + 600 * u, 942), 6, fill=GREEN2)
        if t > 31.95:
            put(b, pill('कंटेंट  ↑  बढ़ाओ', 30, bg=DEEP, fg=YEL, path=PB), W / 2, 1010, scale=eback(prog(t, 31.95, 0.35)))
    return b, False

def s10(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 32.7, [(32.75, [bold('आपकी रील्स,', 96)]), (33.4, [bold('हमारी', 84, GREEN2), accent('creativity.', 96)])], y0=280)
    q = eback(prog(t, 32.7, 0.5))
    play = prog(t, 32.8, 1.7)
    put(b, editor(play), W / 2, 1000 + (1 - q) * 100, scale=0.88 + 0.12 * q, alpha=min(1, q * 2))
    chips = [('AI पोस्ट डिज़ाइन', 33.45, 250, 690, YEL), ('1-क्लिक FB + Insta', 33.65, 830, 760, WHITE), ('WhatsApp मार्केटिंग', 33.85, 300, 1290, GREEN)]
    for txt, t0, x, y, c in chips:
        if t > t0:
            put(b, pill(txt, 28, bg=c, fg=WHITE if c == GREEN else DEEP, path=PB), x, y + math.sin(t * 3 + x) * 6, scale=eback(prog(t, t0, 0.35)))
    return b, False

def s11(t):
    b = bg_light(t, glow=GREEN, glow2=YEL)
    q = eback(prog(t, 34.45, 0.5))
    put(b, logo(150), W / 2, 560, scale=0.7 + 0.3 * q, alpha=min(1, q * 2))
    put(b, text_img('AI पोस्ट  ·  1-क्लिक पोस्टिंग  ·  WhatsApp', 30, GREEN2, PB), W / 2, 680, alpha=prog(t, 34.6, 0.3))
    # follow button
    k = eback(prog(t, 34.6, 0.45))
    pulse = 1 + 0.05 * math.sin(max(0, t - 35.0) * 9) * (t > 35.0)
    tap = 1 - 0.08 * math.sin(math.pi * prog(t, 34.95, 0.25))
    put(b, follow_btn(t > 35.05), W / 2, 880, scale=k * pulse * tap)
    if 34.75 < t:
        hp = eo(prog(t, 34.75, 0.25))
        put(b, cached('cursor', cursor_img), W / 2 + 180 - 40 * hp, 960 + 60 * (1 - hp), alpha=hp * (1 - prog(t, 35.6, 0.3)))
    c = eback(prog(t, 34.8, 0.45))
    put(b, text_img('अधिक जानकारी के लिए', 40, DEEP, PB), W / 2, 1075, alpha=prog(t, 34.8, 0.3))
    put(b, phone_pill(), W / 2, 1185, scale=c)
    return b, False

def follow_btn(done):
    def mk():
        txt = 'फॉलो किया ✓' if done else '+  फॉलो करो'
        tw = twidth(txt, 56, PB)
        w, h = int(tw + 120), 120
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), h // 2, fill=(YEL if done else GREEN) + (255,))
        p.text((w / 2, h / 2 + 2), txt, 56, DEEP if done else WHITE, PB, anchor='mm')
        return with_shadow(p.img(), blur=18, off=10, alpha=0.3)
    return cached(('follow', done), mk)

def cursor_img():
    p = Pad(80, 100)
    p.poly([(10, 6), (10, 80), (30, 62), (44, 94), (58, 88), (44, 56), (70, 56)], fill=DEEP + (255,))
    p.poly([(16, 20), (16, 66), (31, 53), (45, 82), (50, 80), (37, 50), (56, 50)], fill=WHITE + (255,))
    return p.img()

def phone_pill():
    def mk():
        txt = '9993615146'
        f = font(PB, 70); tw = f.getlength(txt)
        w, h = int(tw + 190), 130
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), h // 2, fill=YEL + (255,))
        p.ell((24, 17, 120, 113), fill=DEEP + (255,))
        p.text((72, 66), '☎', 52, YEL, FSYM, anchor='mm')
        p.text((140, h / 2 + 2), txt, 70, DEEP, PB, anchor='lm')
        return with_shadow(p.img(), blur=18, off=10, alpha=0.3)
    return cached('phonepill', mk)

SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]
TR = 0.22

def scene_at(t):
    for i in range(len(SC) - 1):
        if SC[i] <= t < SC[i + 1]: return i
    return len(SC) - 2


# ---------------- brand block under subtitles ----------------
BR_Y, PH_Y = 1590, 1688
MODES = ['up', 'left', 'blur', 'color', 'pop', 'right', 'hide', 'blur', 'color', 'left', 'up']
PMODES = ['type', 'ring', 'left', 'glow', 'up', 'ring', 'type', 'glow', 'up', 'ring', 'glow']

def brand_logo(scheme, blur=0):
    def mk():
        if scheme == 'dark': segs = [('Shri', 70, WHITE, PB), ('Tech', 70, YEL, PB)]
        elif scheme == 'swap': segs = [('Shri', 70, GREEN2, PB), ('Tech', 70, DEEP, PB)]
        elif scheme == 'yel': segs = [('Shri', 70, DEEP, PB), ('Tech', 70, WHITE, PB)]
        else: segs = [('Shri', 70, DEEP, PB), ('Tech', 70, GREEN, PB)]
        im = line_img(segs, gap=4)
        if scheme == 'yel':
            p = Pad(im.width + 40, im.height + 4)
            p.rect((0, 6, im.width + 39, im.height - 4), 26, fill=YEL + (255,))
            bgp = p.img(); bgp.alpha_composite(im, (20, 0)); im = bgp
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        return im
    return cached(('blogo', scheme, blur), mk)

def phone_row(dark, digits=10, glow=0.0, ring=0.0):
    key = ('prow', dark, digits, round(glow, 1), round(ring, 2))
    def mk():
        num = '9993615146'
        f = font(PB, 50)
        w, h = int(f.getlength(num) + 150), 88
        p = Pad(w, h)
        bgc = (16, 90, 50) if dark else WHITE
        if glow > 0: p.rect((0, 0, w - 1, h - 1), h // 2, fill=mix(bgc, YEL, glow) + (255,))
        else: p.rect((0, 0, w - 1, h - 1), h // 2, fill=bgc + (255,))
        im = p.img()
        q = Pad(w, h)
        q.ell((12, 10, 80, 78), fill=(YEL if dark else GREEN) + (255,))
        ic = Pad(68, 68); ic.text((34, 36), '☎', 40, DEEP if dark else WHITE, FSYM, anchor='mm')
        ici = ic.img().rotate(math.sin(ring * math.pi * 8) * 22 * (ring > 0), Image.BICUBIC)
        im.alpha_composite(q.img()); im.alpha_composite(ici, (12, 10))
        if ring > 0:
            r = Pad(w, h)
            for k in (0, 0.5):
                rr = ((ring + k) % 1)
                r.ell((46 - 34 - rr * 14, 44 - 34 - rr * 14, 46 + 34 + rr * 14, 44 + 34 + rr * 14), outline=YEL + (int(255 * (1 - rr)),), width=4)
            im.alpha_composite(r.img())
        tx = Pad(w, h)
        col = DEEP if (not dark and glow < 0.5) else (DEEP if glow >= 0.5 else WHITE)
        tx.text((104, h / 2 + 2), num[:digits], 50, col, PB, anchor='lm')
        im.alpha_composite(tx.img())
        return with_shadow(im, blur=12, off=6, alpha=0.2) if not dark else im
    return cached(key, mk)

def brand_block(base, t, dark):
    i = scene_at(t); lt = t - SC[i]; ln = SC[i + 1] - SC[i]
    mode = MODES[i % len(MODES)]; pm = PMODES[i % len(PMODES)]
    p = eo(prog(lt, 0.15, 0.55))
    scheme = 'dark' if dark else ('yel' if i == 8 else 'light')
    x, y, al, sc, bl = W / 2, BR_Y, p, 1.0, 0
    if mode == 'up': y += (1 - p) * 120
    elif mode == 'left': x -= (1 - p) * 700
    elif mode == 'right': x += (1 - p) * 700
    elif mode == 'blur': bl = int(round((1 - p) * 14)); al = min(1, p * 1.5)
    elif mode == 'pop': sc = eback(prog(lt, 0.15, 0.5), 2.5); al = 1 if lt > 0.15 else 0
    elif mode == 'color':
        k = (lt * 1.5) % 3
        scheme = 'dark' if dark else ['light', 'swap', 'yel'][int(k)]
    elif mode == 'hide':
        # visible, ducks out mid-scene, rises again
        h = clamp(prog(lt, 0.9, 0.25) - prog(lt, 1.6, 0.35))
        al = p * (1 - h); y += h * 80
    # periodic shine pulse
    put(base, brand_logo(scheme, bl), x, y, scale=sc * (1 + 0.03 * math.sin(t * 3)), alpha=al)
    # phone row
    q = eo(prog(lt, 0.4, 0.5))
    px, py, pal = W / 2, PH_Y, q
    digits, glow, ring = 10, 0.0, 0.0
    if pm == 'type': digits = int(10 * prog(lt, 0.4, 0.8)); pal = 1 if lt > 0.4 else 0
    elif pm == 'left': px -= (1 - q) * 700
    elif pm == 'up': py += (1 - q) * 110
    elif pm == 'ring': ring = (lt * 0.9) % 1 if lt < ln - 0.1 else 0
    elif pm == 'glow': glow = 0.5 + 0.5 * math.sin(lt * 5)
    if digits <= 0: return
    put(base, phone_row(dark, digits, glow, ring), px, py, alpha=pal)
    # yellow highlight sweep under number every few seconds
    k = (t % 3.0) / 0.6
    if k < 1 and q > 0.9:
        d = ImageDraw.Draw(base)
        w0 = 400
        d.rounded_rectangle((W / 2 - 160 + w0 * 0 , PH_Y + 52, W / 2 - 160 + (w0) * eo(k), PH_Y + 60), 4, fill=YEL)

# ---------------- floating particles ----------------
_r = random.Random(11)
PARTS = [(_r.random() * W, _r.random() * H, _r.uniform(5, 14), _r.uniform(30, 80), _r.random() * 6.28, _r.choice([GREEN, YEL, YEL2])) for _ in range(26)]
def particles(base, t, dark):
    for (x, y, r, sp, ph, c) in PARTS:
        yy_ = (y - t * sp) % (H + 100) - 50
        xx_ = x + math.sin(t * 0.8 + ph) * 30
        if 1380 < yy_ < 1760: continue
        im = cached(('dot', int(r), c), lambda: dot_img(int(r), c))
        put(base, im, xx_, yy_, alpha=0.35 + 0.25 * math.sin(t * 2 + ph))

def dot_img(r, c):
    p = Pad(r * 2 + 2, r * 2 + 2); p.ell((1, 1, r * 2 + 1, r * 2 + 1), fill=c + (255,)); return p.img()

# ---------------- thumbnail ----------------
def thumbnail():
    def mk():
        b = bg_light(0.5)
        put(b, cached('thumb_ghost', lambda: outline_text('SALON', 330, GREEN)), W / 2, 1000, alpha=0.10)
        put(b, pill('सैलून ओनर्स ध्यान दें!', 40, bg=DEEP, fg=YEL, path=PB, padx=36, pady=16), W / 2, 300)
        put(b, line_img([bold('डिस्काउंट', 118, DEEP)]), W / 2, 505)
        st = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(st)
        d.rounded_rectangle((W / 2 - 300, 502, W / 2 + 300, 520), 9, fill=GREEN2)
        b.alpha_composite(st)
        put(b, line_img([bold('नहीं,', 100, DEEP), accent('content', 128, GREEN2)]), W / 2, 645)
        put(b, line_img([bold('से बढ़ेंगे कस्टमर!', 92, DEEP)]), W / 2, 780)
        put(b, portrait_card('AFTER ✦', 'happy', 470, 590, bg1=YEL2, bg2=GREEN), W / 2 + 150, 1200, rot=-4)
        put(b, portrait_card('BEFORE', 'calm', 380, 480, bg1=(236, 240, 236), bg2=(214, 222, 216), styled=False), W / 2 - 230, 1160, rot=6)
        put(b, badge('50%', 'OFF', 100), 210, 920, rot=-14)
        put(b, cached('xmark', xmark), 210, 920)
        put(b, bubble('“अपॉइंटमेंट चाहिए!”', 34), W / 2 + 230, 880)
        put(b, logo(110), W / 2, 1610)
        put(b, phone_pill(), W / 2, 1745, scale=0.85)
        return b.convert('RGB')
    return cached('thumb', mk)

def xmark():
    p = Pad(240, 240)
    p.line([(40, 40), (200, 200)], DEEP + (255,), 22); p.line([(200, 40), (40, 200)], DEEP + (255,), 22)
    return p.img()

THUMB = 0.5
def frame(T):
    if T < THUMB: return thumbnail()
    t = T - THUMB
    i = scene_at(t)
    img, dark = SCENES[i](t)
    if i > 0 and t - SC[i] < TR:
        k = eio((t - SC[i]) / TR)
        prev, _ = SCENES[i - 1](t)
        sc = 1 + 0.06 * k
        pz = prev.resize((int(W * sc), int(H * sc)), Image.BILINEAR).crop((int((W * sc - W) / 2), int((H * sc - H) / 2), int((W * sc - W) / 2) + W, int((H * sc - H) / 2) + H))
        img = Image.blend(pz.convert('RGB'), img.convert('RGB'), k).convert('RGBA')
    particles(img, t, dark)
    topbar(img, t, dark)
    draw_caption(img, t, dark)
    brand_block(img, t, dark)
    return img.convert('RGB')

def render(a, b, path):
    tmp = path + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-crf', '19', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, path)

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            frame(float(ts)).save(f'/home/claude/salon/st/st_{ts}.jpg', quality=85) if ts != 'thumb' else thumbnail().save('/home/claude/salon/out/ShriTech_Salon_Thumbnail.jpg', quality=92)
    else:
        render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
