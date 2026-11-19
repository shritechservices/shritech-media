"""Glossy layer: gradient fills, sheen, 3D bevel on art, richer background. Patches kit functions in place."""
import numpy as np
import kit
from kit import *

def lighten(c, t): return tuple(int(v + (255 - v) * t) for v in c)
def darken(c, t): return tuple(int(v * (1 - t)) for v in c)

def grad_mask_fill(img, mask, c1, c2, bbox=None, sheen=0.28):
    """Fill 'mask' (L, full size) with vertical gradient c1->c2 over its bbox, plus a top sheen."""
    bb = bbox or mask.getbbox()
    if not bb: return
    x0, y0, x1, y1 = bb
    h = max(1, y1 - y0)
    t = np.clip((np.arange(img.size[1])[:, None] - y0) / h, 0, 1)
    col = np.array(c1)[None, :] * (1 - t) + np.array(c2)[None, :] * t
    if sheen:
        band = np.exp(-((t - 0.22) / 0.16) ** 2) * sheen
        col = col + (255 - col) * band
    strip = Image.fromarray(np.repeat(col[:, None, :], img.size[0], axis=1).astype(np.uint8))
    img.paste(strip, (0, 0), mask)

def gshape(img, draw_fn, c1, c2, sheen=0.28):
    m = Image.new('L', img.size, 0); draw_fn(ImageDraw.Draw(m))
    grad_mask_fill(img, m, c1, c2, sheen=sheen)
    return m

def gellipse(img, cx, cy, rx, ry, c1, c2, sheen=0.3):
    return gshape(img, lambda d: d.ellipse(P((cx - rx, cy - ry), (cx + rx, cy + ry)), fill=255), c1, c2, sheen)

def grrect(img, box, r, c1, c2, sheen=0.25):
    return gshape(img, lambda d: d.rounded_rectangle(P(box[:2], box[2:]), r * S, fill=255), c1, c2, sheen)

# ---------- glossy art pass ----------
def glossify(img, bg, y0=92, y1=440):
    Y0, Y1 = int(y0 * S), int(y1 * S)
    a = np.asarray(img.crop((0, Y0, W, Y1))).astype(np.float32)
    b = np.asarray(bg.crop((0, Y0, W, Y1))).astype(np.float32)
    diff = np.abs(a - b).max(axis=2)
    m = np.clip((diff - 18) / 40, 0, 1)                       # soft art mask
    mi = Image.fromarray((m * 255).astype(np.uint8))
    bl = np.asarray(mi.filter(ImageFilter.GaussianBlur(5 * S))).astype(np.float32) / 255
    sh = np.roll(np.roll(bl, int(3 * S), 0), int(3 * S), 1)
    hi = np.clip(bl - sh, 0, 1) * 2.2                          # top-left edges -> highlight
    lo = np.clip(sh - bl, 0, 1) * 1.6                          # bottom-right edges -> shade
    H_, W_ = m.shape
    yy = np.linspace(0, 1, H_)[:, None]; xx = np.linspace(0, 1, W_)[None, :]
    vert = 1.06 - 0.12 * yy                                    # light from the top
    band = np.exp(-(((xx * 0.9 + yy * 0.6) - 0.62) / 0.11) ** 2) * 0.18   # diagonal sheen
    out = a * vert[..., None]
    out = out + (255 - out) * (hi[..., None] * 0.55 + band[..., None])
    out = out * (1 - lo[..., None] * 0.28)
    # drop shadow of the art onto the background
    shd = np.asarray(mi.filter(ImageFilter.GaussianBlur(9 * S))).astype(np.float32) / 255
    shd = np.roll(shd, int(9 * S), 0) * 0.20
    base_ = b * (1 - shd[..., None]) + np.array(DEEP)[None, None, :] * shd[..., None]
    res = base_ * (1 - m[..., None]) + np.clip(out, 0, 255) * m[..., None]
    img.paste(Image.fromarray(res.astype(np.uint8)), (0, Y0))

# ---------- richer background ----------
def base():
    img = vgrad((255, 255, 255), (236, 252, 243))
    glow(img, 540, 240, 380, (254, 240, 150), 0.55)
    glow(img, 980, 120, 260, (187, 247, 208), 0.45)
    glow(img, 80, 520, 260, (254, 243, 170), 0.35)
    glow(img, 540, 900, 520, (209, 250, 223), 0.5)
    # soft gradient wave behind the art
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m)
    pts = bez((0, 330), (540, 470), (1080, 300), 40) + [(1080, 430), (0, 430)]
    d.polygon(P(*pts), fill=70)
    m = m.filter(ImageFilter.GaussianBlur(20 * S))
    img.paste(Image.new('RGB', img.size, (220, 252, 231)), (0, 0), m)
    # bokeh
    random.seed(11)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for _ in range(18):
        x, y, r = random.uniform(40, 1040), random.uniform(110, 420), random.uniform(6, 18)
        c = random.choice([YEL, LGREEN, (253, 224, 71)])
        dl.ellipse(P((x - r, y - r), (x + r, y + r)), fill=c + (random.randint(28, 60),))
    lay = lay.filter(ImageFilter.GaussianBlur(2 * S)); img.paste(lay, (0, 0), lay)
    return img

# ---------- glossy UI pieces ----------
def greeting(img, title, line2, y_title=478, y2=543):
    s = fit(title, 80, PB, 980)
    grad_text(img, (540, y_title), title, s, (21, 128, 61), (6, 52, 28), PB, 'mm', shadow=(GOLD, 0.25), gloss=False)
    if line2:
        s2 = fit(line2, 42, PB, 900)
        w = tw(line2, s2, PB)
        grrect(img, (540 - w / 2 - 20, y2 - 10, 540 + w / 2 + 20, y2 + 24), 12, (254, 243, 160), (250, 214, 60), 0.35)
        text(img, (540, y2), line2, s2, (21, 110, 52), PB, 'mm')

def story_pill(img, txt, y=590):
    segs = segs_fit(parse(txt, 27, WHITE, (254, 240, 138)), 900)
    w = rich_w(segs) + 64
    shadow(img, (540 - w / 2, y, 540 + w / 2, y + 52), 26, blur=10, alpha=0.25, off=6, color=DEEP)
    grrect(img, (540 - w / 2, y, 540 + w / 2, y + 52), 26, (52, 211, 110), (21, 128, 61), 0.35)
    rich2(img, 540, y + 25, segs)

def card(img, box, r, ol=None):
    shadow(img, box, r, blur=12, alpha=0.12, off=6, color=DEEP)
    grrect(img, box, r, (255, 255, 255), (240, 253, 244), 0.0)
    rrect(img, box, r, outline=ol or (187, 247, 208), width=2 if not ol else 3)

def node(img, cx, cy, r, ic, num=None):
    d = ImageDraw.Draw(img)
    shadow(img, (cx - r, cy - r, cx + r, cy + r), r, blur=8, alpha=0.18, off=5, color=DEEP)
    gellipse(img, cx, cy, r, r, (52, 211, 110), (21, 128, 61), 0.25)          # green ring
    gellipse(img, cx, cy, r - 5, r - 5, (255, 255, 255), (220, 252, 231), 0.0)  # face
    tmp = Image.new('RGBA', (int(110 * S), int(110 * S)), (0, 0, 0, 0))
    icon(tmp, ic, 55, 55, DEEP, YEL, (240, 253, 244))
    sz = int(r * 1.45 * S); tmp = tmp.resize((sz, sz), Image.LANCZOS)
    img.paste(tmp, (int(cx * S - sz / 2), int(cy * S - sz / 2)), tmp)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).ellipse(P((cx - r * 0.7, cy - r * 0.92), (cx + r * 0.7, cy - r * 0.2)), fill=60)
    img.paste(Image.new('RGB', img.size, WHITE), (0, 0), m.filter(ImageFilter.GaussianBlur(3 * S)))
    if num:
        bx, by = cx + r * 0.72, cy - r * 0.72
        gellipse(img, bx, by, 17, 17, (254, 240, 138), (234, 179, 8), 0.3)
        text(img, (bx, by + 1), str(num), 20, DEEP, PB, 'mm')

def ribbon2(img, aud, prob, sol, y=1098):
    shadow(img, (M, y, 1080 - M, y + 92), 22, blur=12, alpha=0.15, off=6, color=GOLD)
    grrect(img, (M, y, 1080 - M, y + 92), 22, (255, 251, 225), (254, 240, 138), 0.3)
    rrect(img, (M, y, 1080 - M, y + 92), 22, outline=YEL, width=3)
    l1 = segs_fit([(aud + ' की परेशानी:', 21, (120, 90, 10), PBD), (prob, 21, SUB, PM)], 900)
    rich2(img, 540, y + 27, l1)
    l2 = segs_fit([('@ST', 25), ('का हल:', 25, DEEP, PB), (sol, 25, (21, 128, 61), PB)], 920)
    rich2(img, 540, y + 64, l2)

def cta(img, line, y=1214):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rectangle(P((0, y), (1080, 1350)), fill=255)
    grad_mask_fill(img, m, (22, 110, 56), (6, 46, 25), sheen=0.0)
    glow(img, 860, y + 60, 220, (34, 197, 94), 0.25)
    lay = Image.new('L', img.size, 0)
    ImageDraw.Draw(lay).polygon(P((520, y), (640, y), (560, 1350), (440, 1350)), fill=22)
    img.paste(Image.new('RGB', img.size, WHITE), (0, 0), lay.filter(ImageFilter.GaussianBlur(8 * S)))
    s = fit(line, 25, PBD, 640)
    text(img, (M, y + 40), line, s, (187, 247, 208), PBD, 'lm')
    phone_icon(img, M + 26, y + 96, 44, YEL)
    grad_text(img, (M + 64, y + 96), '9993615146', 60, (254, 240, 138), (234, 179, 8), PB, 'lm', gloss=True)
    size = 38; lw = logo_width(size)
    logo(img, 1080 - M - lw, y + 26, size, dark=True)
    text(img, (1080 - M, y + 104), 'Shri Balaji Digital Services', 20, WHITE, PM, 'rm')

def tribute_footer(img, line, y=1214):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rectangle(P((0, y), (1080, 1350)), fill=255)
    grad_mask_fill(img, m, (22, 110, 56), (6, 46, 25), sheen=0.0)
    text(img, (540, y + 44), line, fit(line, 26, PBD, 980), (187, 247, 208), PBD, 'mm')
    size = 34; lw = logo_width(size)
    tot = lw + 40 + tw('9993615146', 34, PB) + 50
    x = 540 - tot / 2
    logo(img, x, y + 72, size, dark=True)
    phone_icon(img, x + lw + 60, y + 98, 30, YEL)
    text(img, (x + lw + 86, y + 98), '9993615146', 34, YEL, PB, 'lm')

_phone0 = kit.phone
def phone(img, x, y, w, h, kind='poster', label='ऑफर', badge=None):
    _phone0(img, x, y, w, h, kind, label, badge)
    if kind in ('poster', 'wa'):   # glossy poster on the phone
        bx0, bx1 = x + 22, x + w - 22; y0 = y + 84; ph = (bx1 - bx0) * 0.78
        grrect(img, (bx0, y0, bx1, y0 + ph), 12, (254, 249, 195), (250, 214, 60), 0.3)
        c = ((bx0 + bx1) / 2, y0 + ph * 0.42)
        glow(img, c[0], c[1], 40, WHITE, 0.6)
        sparkle(img, c[0], c[1], 26, (21, 128, 61)); sparkle(img, c[0] + 30, c[1] - 22, 10, WHITE)
        text(img, (c[0], y0 + ph - 30), label, fit(label, 16, PB, bx1 - bx0 - 20), DEEP, PB, 'mm')
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon(P((x + 12, y + 12), (x + w * 0.7, y + 12), (x + 12, y + h * 0.45)), fill=34)
    img.paste(Image.new('RGB', img.size, WHITE), (0, 0), m.filter(ImageFilter.GaussianBlur(10 * S)))

for name in ('base', 'greeting', 'story_pill', 'card', 'node', 'cta', 'tribute_footer', 'phone'):
    setattr(kit, name, globals()[name])

def dg_tribute(img, d):
    y0, y1 = 672, 1180
    shadow(img, (M + 30, y0, 1080 - M - 30, y1), 30, blur=16, alpha=0.18, off=8, color=GOLD)
    grrect(img, (M + 30, y0, 1080 - M - 30, y1), 30, (255, 255, 255), (254, 246, 200), 0.0)
    rrect(img, (M + 30, y0, 1080 - M - 30, y1), 30, outline=YEL, width=4)
    rrect(img, (M + 46, y0 + 16, 1080 - M - 46, y1 - 16), 22, outline=(253, 230, 138), width=2)
    for (x, y) in [(M + 80, y0 + 50), (1080 - M - 80, y0 + 50), (M + 80, y1 - 50), (1080 - M - 80, y1 - 50)]:
        sparkle(img, x, y, 14, GOLD)
    n = len(d['quote']); hq = n * 64 + (60 if d.get('by') else 0) + 46 * len(d.get('lines', [])) + 90
    y = (y0 + y1) / 2 - hq / 2
    grad_text(img, (540, y + 34), '“', 110, (254, 240, 138), (217, 159, 6), PB, 'mm', gloss=False); y += 100
    for ln_ in d['quote']:
        grad_text(img, (540, y), ln_, fit(ln_, 44, PB, 840), (21, 128, 61), (6, 52, 28), PB, 'mm', gloss=False); y += 66
    if d.get('by'):
        y += 10
        w = tw(d['by'], 26, PBD) + 50
        grrect(img, (540 - w / 2, y - 22, 540 + w / 2, y + 22), 22, (52, 211, 110), (21, 128, 61), 0.3)
        text(img, (540, y), d['by'], 26, WHITE, PBD, 'mm'); y += 56
    for ln_ in d.get('lines', []):
        y += 6; text(img, (540, y), ln_, fit(ln_, 24, PM, 840), SUB, PM, 'mm'); y += 40

kit.DIAGRAMS['tribute'] = dg_tribute


def glossy_art(img, art_fn, y1=450):
    """Render art on black and white to get exact colour+alpha, add bevel/sheen/shadow, composite on img."""
    Y1 = int(y1 * S)
    Bk = Image.new('RGB', img.size, (0, 0, 0)); art_fn(Bk)
    Wt = Image.new('RGB', img.size, (255, 255, 255)); art_fn(Wt)
    b = np.asarray(Bk.crop((0, 0, W, Y1))).astype(np.float32)
    w = np.asarray(Wt.crop((0, 0, W, Y1))).astype(np.float32)
    al = np.clip(1 - (w - b).mean(axis=2) / 255, 0, 1)
    col = np.clip(b / np.maximum(al[..., None], 1e-3), 0, 255)
    solid = np.clip((al - 0.55) / 0.3, 0, 1)                   # bevel only on solid shapes, not soft glows
    mi = Image.fromarray((solid * 255).astype(np.uint8))
    hi = 0; lo = 0
    for rad, off, kh, kl in ((4, 3, 2.0, 1.4), (14, 8, 1.3, 0.9)):
        bl = np.asarray(mi.filter(ImageFilter.GaussianBlur(rad * S))).astype(np.float32) / 255
        sh = np.roll(np.roll(bl, int(off * S), 0), int(off * S), 1)
        hi = hi + np.clip(bl - sh, 0, 1) * kh
        lo = lo + np.clip(sh - bl, 0, 1) * kl
    hi = np.clip(hi, 0, 1); lo = np.clip(lo, 0, 1)
    H_, W_ = al.shape
    yy = np.linspace(0, 1, H_)[:, None]; xx = np.linspace(0, 1, W_)[None, :]
    band = np.exp(-(((xx * 0.9 + yy * 0.6) - 0.62) / 0.11) ** 2) * 0.16
    out = col * (1.05 - 0.10 * yy)[..., None]
    out = out + (255 - out) * (hi[..., None] * 0.5 + band[..., None] * solid[..., None])
    out = np.clip(out * (1 - lo[..., None] * 0.25), 0, 255)
    bg = np.asarray(img.crop((0, 0, W, Y1))).astype(np.float32)
    shd = np.asarray(mi.filter(ImageFilter.GaussianBlur(9 * S))).astype(np.float32) / 255
    shd = np.roll(shd, int(8 * S), 0) * 0.18
    bg = bg * (1 - shd[..., None]) + np.array(DEEP)[None, None, :] * shd[..., None]
    res = bg * (1 - al[..., None]) + out * al[..., None]
    img.paste(Image.fromarray(res.astype(np.uint8)), (0, 0))
