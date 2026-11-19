"""Series v3 engine: real photos + stylish fonts + 8 varied layouts. Light theme (green/yellow/white).
Header (logo + number) and footer (number + logo) stay the same; the middle changes per post."""
import sys, os
sys.path.insert(0, '/home/claude/posters/series')
import numpy as np
import gloss, kit
from art2 import *          # ART + primitives (gradient-filled)
from gloss import grrect, gellipse, gshape, grad_mask_fill, lighten, darken

FD = '/home/claude/fonts2/'
FNT = dict(
    rozha=FD + 'RozhaOne-Regular.ttf', yatra=FD + 'YatraOne-Regular.ttf', amita=FD + 'Amita-Bold.ttf',
    tiro=FD + 'TiroDevanagariHindi-Regular.ttf', tiroi=FD + 'TiroDevanagariHindi-Italic.ttf', eczar=FD + 'Eczar[wght].ttf',
    khand=FD + 'Khand-Bold.ttf', teko=FD + 'Teko[wght].ttf', baloo=FD + 'Baloo2[wght].ttf', kalam=FD + 'Kalam-Bold.ttf',
    mukta=FD + 'Mukta-ExtraBold.ttf', muktam=FD + 'Mukta-Medium.ttf', laila=FD + 'Laila-Bold.ttf', martel=FD + 'Martel-ExtraBold.ttf',
    playi=FD + 'PlayfairDisplay-Italic[wght].ttf', play=FD + 'PlayfairDisplay[wght].ttf', bebas=FD + 'BebasNeue-Regular.ttf',
    vibes=FD + 'GreatVibes-Regular.ttf', oswald=FD + 'Oswald[wght].ttf', dance=FD + 'DancingScript[wght].ttf',
    mont=FD + 'Montserrat[wght].ttf', monti=FD + 'Montserrat-Italic[wght].ttf', pb=PB, pbd=PBD, pm=PM)
_VAR = {'eczar': b'ExtraBold', 'teko': b'SemiBold', 'baloo': b'ExtraBold', 'playi': b'Bold', 'play': b'Black', 'oswald': b'Bold',
        'dance': b'Bold', 'mont': b'ExtraBold', 'monti': b'Bold'}
_FC = {}
def ft(name, size):
    k = (name, int(size * S))
    if k not in _FC:
        f = ImageFont.truetype(FNT[name], int(size * S), layout_engine=ImageFont.Layout.RAQM)
        if name in _VAR:
            try: f.set_variation_by_name(_VAR[name])
            except Exception: pass
        _FC[k] = f
    return _FC[k]

def twf(txt, size, name): return ft(name, size).getlength(txt) / S

def T(img, xy, txt, size, color, name='pb', anchor='la', maxw=None):
    if maxw:
        while size > 12 and twf(txt, size, name) > maxw: size -= 1
    ImageDraw.Draw(img).text((xy[0] * S, xy[1] * S), txt, font=ft(name, size), fill=color, anchor=anchor)
    return size

def GT(img, xy, txt, size, c1, c2, name='pb', anchor='la', maxw=None, shadow=None):
    """gradient text"""
    if maxw:
        while size > 12 and twf(txt, size, name) > maxw: size -= 1
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).text((xy[0] * S, xy[1] * S), txt, font=ft(name, size), fill=255, anchor=anchor)
    if shadow:
        sh = m.filter(ImageFilter.GaussianBlur(5 * S)).point(lambda v: int(v * shadow[1]))
        img.paste(Image.new('RGB', img.size, shadow[0]), (0, int(4 * S)), sh)
    grad_mask_fill(img, m, c1, c2, sheen=0.0)
    return size

def wrap(txt, size, name, maxw):
    words = txt.split(' '); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if twf(t, size, name) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def para(img, x, y, txt, size, color, name, maxw, lh=1.35, anchor='l'):
    for ln_ in wrap(txt, size, name, maxw):
        a = {'l': 'lm', 'm': 'mm', 'r': 'rm'}[anchor]
        T(img, (x, y), ln_, size, color, name, a); y += size * lh
    return y

GREENG = ((74, 222, 128), (21, 101, 52)); DEEPG = ((34, 140, 70), (6, 46, 25)); GOLDG = ((254, 240, 138), (217, 159, 6))
CREAM = (255, 251, 235); INK = DEEP; SUB = (55, 80, 64)

# ---------- backgrounds (same palette, different mood per layout) ----------
def bg(variant=0):
    img = gloss.base() if variant == 0 else vgrad(*[((255, 253, 240), (236, 252, 243)), ((240, 253, 244), (255, 251, 225)),
                                                   ((255, 255, 255), (230, 250, 238)), ((255, 250, 228), (255, 255, 255))][variant - 1])
    if variant:
        glow(img, 900 if variant % 2 else 180, 260, 360, (254, 240, 150), 0.5)
        glow(img, 180 if variant % 2 else 900, 900, 420, (187, 247, 208), 0.45)
    return img

# ---------- festival art as a glossy RGBA layer ----------
_ART = {}
def art_layer(key):
    if key in _ART: return _ART[key]
    fn = ART[key]; Y1 = int(450 * S)
    Bk = Image.new('RGB', (W, H), (0, 0, 0)); fn(Bk)
    Wt = Image.new('RGB', (W, H), (255, 255, 255)); fn(Wt)
    b = np.asarray(Bk.crop((0, 0, W, Y1))).astype(np.float32); w = np.asarray(Wt.crop((0, 0, W, Y1))).astype(np.float32)
    al = np.clip(1 - (w - b).mean(axis=2) / 255, 0, 1)
    col = np.clip(b / np.maximum(al[..., None], 1e-3), 0, 255)
    solid = np.clip((al - 0.55) / 0.3, 0, 1)
    mi = Image.fromarray((solid * 255).astype(np.uint8))
    hi = 0; lo = 0
    for rad, off, kh, kl in ((4, 3, 2.0, 1.4), (14, 8, 1.3, 0.9)):
        bl = np.asarray(mi.filter(ImageFilter.GaussianBlur(rad * S))).astype(np.float32) / 255
        sh = np.roll(np.roll(bl, int(off * S), 0), int(off * S), 1)
        hi = hi + np.clip(bl - sh, 0, 1) * kh; lo = lo + np.clip(sh - bl, 0, 1) * kl
    hi = np.clip(hi, 0, 1); lo = np.clip(lo, 0, 1)
    out = col + (255 - col) * hi[..., None] * 0.5
    out = np.clip(out * (1 - lo[..., None] * 0.25), 0, 255)
    rgba = np.dstack([out, al * 255]).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    im = im.crop(bb) if bb else im
    _ART[key] = im
    return im

def paste_art(img, key, box, align='m', shadow_=True):
    a = art_layer(key)
    x0, y0, x1, y1 = [v * S for v in box]
    sc = min((x1 - x0) / a.width, (y1 - y0) / a.height)
    a2 = a.resize((max(1, int(a.width * sc)), max(1, int(a.height * sc))), Image.LANCZOS)
    px = int(x0 + ((x1 - x0) - a2.width) / 2) if align == 'm' else (int(x0) if align == 'l' else int(x1 - a2.width))
    py = int(y0 + ((y1 - y0) - a2.height) / 2)
    if shadow_:
        sh = a2.getchannel('A').filter(ImageFilter.GaussianBlur(10 * S)).point(lambda v: int(v * 0.18))
        img.paste(Image.new('RGB', a2.size, DEEP), (px, py + int(8 * S)), sh)
    img.paste(a2, (px, py), a2)
    return (px / S, py / S, (px + a2.width) / S, (py + a2.height) / S)

# ---------- real photos ----------
PH = '/home/claude/photos/'
def _load(key):
    for ext in ('.jpg', '.jpeg', '.png'):
        p = PH + key + ext
        if os.path.exists(p): return Image.open(p).convert('RGB')
    return None

def photo(img, key, box, shape='round', r=34, frame=True, focus=(0.5, 0.4), fade=False):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    pw, ph = int(w * S), int(h * S)
    src = _load(key)
    if src is None:   # illustrated scene instead of a photo
        import illus
        src = illus.scene(key, w, h, 'worry' if key == 'worried' else 'happy', seed=sum(map(ord, key)) % 7)
    sc = max(pw / src.width, ph / src.height)
    im = src.resize((int(src.width * sc) + 1, int(src.height * sc) + 1), Image.LANCZOS)
    cx = int((im.width - pw) * focus[0]); cy = int((im.height - ph) * focus[1])
    im = im.crop((cx, cy, cx + pw, cy + ph))
    # gentle grade toward brand (warm + slight green in shadows) and gloss
    a = np.asarray(im).astype(np.float32)
    a = a * 1.03 + 4
    if fade:
        t = np.linspace(0, 1, ph)[:, None, None]
        f = np.clip((t - 0.55) / 0.45, 0, 1) * 0.85
        a = a * (1 - f) + np.array(DEEP)[None, None, :] * f
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    m = Image.new('L', (pw, ph), 0); d = ImageDraw.Draw(m)
    if shape == 'circle': d.ellipse((0, 0, pw - 1, ph - 1), fill=255)
    elif shape == 'diag': d.polygon([(0, 0), (pw, 0), (pw * 0.78, ph), (0, ph)], fill=255)
    elif shape == 'diagr': d.polygon([(pw * 0.22, 0), (pw, 0), (pw, ph), (0, ph)], fill=255)
    elif shape == 'arch': d.rounded_rectangle((0, 0, pw - 1, ph + pw // 2), pw // 2, fill=255)
    else: d.rounded_rectangle((0, 0, pw - 1, ph - 1), int(r * S), fill=255)
    if frame:
        sh = m.filter(ImageFilter.GaussianBlur(14 * S)).point(lambda v: int(v * 0.3))
        img.paste(Image.new('RGB', (pw, ph), DEEP), (int(x0 * S), int((y0 + 10) * S)), sh)
    img.paste(im, (int(x0 * S), int(y0 * S)), m)
    # sheen
    sm = Image.new('L', (pw, ph), 0)
    ImageDraw.Draw(sm).polygon([(0, 0), (pw * 0.55, 0), (0, ph * 0.5)], fill=40)
    sm = ImageChops.multiply(sm.filter(ImageFilter.GaussianBlur(20 * S)), m)
    img.paste(Image.new('RGB', (pw, ph), WHITE), (int(x0 * S), int(y0 * S)), sm)
    if frame:
        ring = Image.new('L', (pw, ph), 0); rd = ImageDraw.Draw(ring)
        if shape == 'circle': rd.ellipse((0, 0, pw - 1, ph - 1), outline=255, width=int(7 * S))
        elif shape == 'round': rd.rounded_rectangle((0, 0, pw - 1, ph - 1), int(r * S), outline=255, width=int(7 * S))
        img.paste(Image.new('RGB', (pw, ph), WHITE), (int(x0 * S), int(y0 * S)), ring)

# ---------- small components ----------
def chip(img, x, y, txt, lang, kind='g', size=20):
    f = 'baloo' if lang == 'hi' else 'mont'
    w = twf(txt, size, f) + 34; h = size + 22
    if kind == 'g': grrect(img, (x, y, x + w, y + h), h / 2, (74, 222, 128), (21, 128, 61), 0.3); c = WHITE
    elif kind == 'y': grrect(img, (x, y, x + w, y + h), h / 2, (254, 240, 138), (234, 179, 8), 0.3); c = DEEP
    else: grrect(img, (x, y, x + w, y + h), h / 2, (255, 255, 255), (236, 252, 243), 0); rrect(img, (x, y, x + w, y + h), h / 2, outline=(134, 199, 157), width=2); c = DEEP
    T(img, (x + w / 2, y + h / 2 + 1), txt, size, c, f, 'mm')
    return w

def chips_row(img, cx, y, items, lang, kind='w', size=23, gap=12, maxw=980):
    f = 'baloo' if lang == 'hi' else 'mont'
    ws = [twf(t, size, f) + 34 for t in items]
    while sum(ws) + gap * (len(ws) - 1) > maxw and len(items) > 2: items = items[:-1]; ws = ws[:-1]
    x = cx - (sum(ws) + gap * (len(ws) - 1)) / 2
    for t in items: x += chip(img, x, y, t, lang, kind, size) + gap

def bubble(img, box, txt, lang, tail='bl', kind='w', size=24, title=None):
    x0, y0, x1, y1 = box
    shadow(img, box, 26, blur=12, alpha=0.18, off=6, color=DEEP)
    if kind == 'w': grrect(img, box, 26, (255, 255, 255), (243, 250, 246), 0); c = INK
    elif kind == 'y': grrect(img, box, 26, (255, 249, 214), (253, 230, 138), 0.2); c = INK
    else: grrect(img, box, 26, (52, 211, 110), (21, 128, 61), 0.3); c = WHITE
    tc = (255, 255, 255) if kind == 'g' else ((254, 249, 214) if kind == 'y' else (243, 250, 246))
    tx = {'bl': (x0 + 40, y1), 'br': (x1 - 40, y1), 'tl': (x0 + 40, y0), 'tr': (x1 - 40, y0)}[tail]
    dy = 26 if tail[0] == 'b' else -26
    gcol = {'w': (243, 250, 246), 'y': (253, 230, 138), 'g': (21, 128, 61)}[kind]
    ImageDraw.Draw(img).polygon(P((tx[0] - 16, tx[1] - (2 if dy > 0 else -2)), (tx[0] + 16, tx[1] - (2 if dy > 0 else -2)), (tx[0] + (-14 if tail[1] == 'l' else 14), tx[1] + dy)), fill=gcol)
    f = 'baloo' if lang == 'hi' else 'mont'; fb = 'mukta' if lang == 'hi' else 'mont'
    size = max(size, 36)
    th = (size + 8) if title else 0
    while size > 16:
        lines = wrap(txt, size, f, x1 - x0 - 52)
        if th + len(lines) * size * 1.3 <= (y1 - y0) - 40: break
        size -= 1; th = (size + 8) if title else 0
    total = th + len(lines) * size * 1.3
    y = y0 + ((y1 - y0) - total) / 2 + size * 0.6
    if title:
        T(img, (x0 + 26, y), title, size - 4, (180, 120, 5) if kind != 'g' else (254, 240, 138), fb, 'lm', maxw=x1 - x0 - 52); y += size + 8
    for ln_ in lines:
        T(img, (x0 + 26, y), ln_, size, c, f, 'lm'); y += size * 1.3

def checks(img, x, y, items, lang, size=27, gap=52, maxw=440, color=INK):
    f = 'baloo' if lang == 'hi' else 'mont'
    for it in items:
        gellipse(img, x + 15, y, 15, 15, (74, 222, 128), (21, 128, 61), 0.3)
        ImageDraw.Draw(img).line(P((x + 8, y), (x + 13, y + 6), (x + 23, y - 6)), fill=WHITE, width=int(4 * S), joint='curve')
        T(img, (x + 42, y + 1), it, size, color, f, 'lm', maxw=maxw - 42); y += gap
    return y

def label_pill(img, x, y, txt, lang, kind='y', size=20, anchor='l'):
    f = 'mukta' if lang == 'hi' else 'mont'
    w = twf(txt, size, f) + 36; h = size + 20
    if anchor == 'm': x -= w / 2
    if kind == 'y': grrect(img, (x, y, x + w, y + h), h / 2, (254, 240, 138), (234, 179, 8), 0.3); c = DEEP
    else: grrect(img, (x, y, x + w, y + h), h / 2, (52, 211, 110), (21, 128, 61), 0.3); c = WHITE
    T(img, (x + w / 2, y + h / 2 + 1), txt, size, c, f, 'mm')
    return w

def header(img):
    import build2
    build2.header(img)

def footer(img, line):
    gloss.cta(img, line)

def wordmark_inline(img, x, cy, size, shri=DEEP, tech=(34, 197, 94)):
    wordmark(img, x, cy, size, shri=shri, tech=tech)
    return wordmark_w(size)
