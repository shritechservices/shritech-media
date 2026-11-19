"""ShriTech festival poster generator (1080x1350, drawn at 2x then downsampled).
Light theme = green + yellow + white. Dark theme = green + yellow + black."""
import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

S = 2
W, H = 1080 * S, 1350 * S
GF = '/usr/share/fonts/truetype/google-fonts/'
PB = '/home/claude/salon/fonts/PB.ttf'       # Poppins ExtraBold
PBD = GF + 'Poppins-Bold.ttf'
PSB = GF + 'Poppins-SemiBold.ttf'
PM = GF + 'Poppins-Medium.ttf'
PF = '/home/claude/salon/fonts/PF.ttf'       # Playfair Display Italic
SYM = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

DEEP = (8, 58, 32); GREEN = (22, 163, 74); LGREEN = (74, 222, 128); MINT = (236, 253, 243)
YEL = (250, 204, 21); GOLD = (234, 179, 8); LYEL = (254, 240, 138); PALEY = (255, 251, 224)
WHITE = (255, 255, 255); BLACK = (6, 9, 7); CHAR = (14, 22, 17)

_F = {}
def F(path, size):
    k = (path, size)
    if k not in _F:
        if not __import__('os').path.exists(path): path = PBD
        _F[k] = ImageFont.truetype(path, int(size * S), layout_engine=ImageFont.Layout.RAQM)
    return _F[k]

def tw(txt, size, path): return F(path, size).getlength(txt) / S

def text(img, xy, txt, size, fill, path=PB, anchor='la'):
    d = ImageDraw.Draw(img)
    d.text((xy[0] * S, xy[1] * S), txt, font=F(path, size), fill=fill, anchor=anchor)

def grad_text(img, xy, txt, size, c1, c2, path=PB, anchor='la', shadow=None, gloss=True):
    """Vertical-gradient (glossy) text."""
    f = F(path, size)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).text((xy[0] * S, xy[1] * S), txt, font=f, fill=255, anchor=anchor)
    bb = m.getbbox()
    if not bb: return
    if shadow:
        sh = m.filter(ImageFilter.GaussianBlur(6 * S)).point(lambda v: int(v * shadow[1]))
        sh = ImageChops.offset(sh, 0, 4 * S)
        img.paste(Image.new('RGB', img.size, shadow[0]), (0, 0), sh)
    y0, y1 = bb[1], bb[3]
    g = np.zeros((img.size[1], 1, 3), np.float32)
    for i, c in enumerate([c1, c2]): pass
    ys = np.arange(img.size[1])[:, None]
    tt = np.clip((ys - y0) / max(1, y1 - y0), 0, 1)
    col = (np.array(c1)[None, :] * (1 - tt) + np.array(c2)[None, :] * tt)
    if gloss:  # bright band in upper third
        band = np.exp(-((tt - 0.28) / 0.12) ** 2) * 0.35
        col = col + (255 - col) * band
    strip = Image.fromarray(np.repeat(col[:, None, :], img.size[0], axis=1).astype(np.uint8))
    img.paste(strip, (0, 0), m)

def rrect(img, box, r, fill=None, outline=None, width=1, alpha=255):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([v * S for v in box], r * S, fill=(fill + (alpha,)) if fill else None,
                                          outline=(outline + (255,)) if outline else None, width=int(width * S))
    img.paste(lay, (0, 0), lay)

def shadow(img, box, r, blur=24, alpha=0.35, off=12, color=(0, 0, 0)):
    m = Image.new('L', img.size, 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(m).rounded_rectangle([x0 * S, (y0 + off) * S, x1 * S, (y1 + off) * S], r * S, fill=int(255 * alpha))
    m = m.filter(ImageFilter.GaussianBlur(blur * S))
    img.paste(Image.new('RGB', img.size, color), (0, 0), m)

def glow(img, cx, cy, r, color, alpha):
    m = Image.new('L', (W // 4, H // 4), 0)
    ImageDraw.Draw(m).ellipse([(cx - r) * S / 4, (cy - r) * S / 4, (cx + r) * S / 4, (cy + r) * S / 4], fill=int(255 * alpha))
    m = m.filter(ImageFilter.GaussianBlur(r * S / 8)).resize(img.size, Image.BILINEAR)
    img.paste(Image.new('RGB', img.size, color), (0, 0), m)

def vgrad(c1, c2, h=H, w=W):
    t = np.linspace(0, 1, h)[:, None]
    col = np.array(c1)[None] * (1 - t) + np.array(c2)[None] * t
    return Image.fromarray(np.repeat(col[:, None, :], w, axis=1).astype(np.uint8))

def grad_box(img, box, r, c1, c2, gloss=True):
    x0, y0, x1, y1 = [int(v * S) for v in box]
    g = vgrad(c1, c2, y1 - y0, x1 - x0)
    if gloss:
        hl = Image.new('L', g.size, 0)
        ImageDraw.Draw(hl).rounded_rectangle([6 * S, 4 * S, g.size[0] - 6 * S, g.size[1] * 0.45], r * S, fill=60)
        hl = hl.filter(ImageFilter.GaussianBlur(4 * S))
        g.paste(Image.new('RGB', g.size, WHITE), (0, 0), hl)
    m = Image.new('L', g.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, g.size[0] - 1, g.size[1] - 1], r * S, fill=255)
    img.paste(g, (x0, y0), m)

def check(img, cx, cy, r, bg, fg):
    d = ImageDraw.Draw(img)
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=bg)
    pts = [(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)]
    d.line([(x * S, y * S) for x, y in pts], fill=fg, width=int(r * 0.28 * S), joint='curve')

def phone_icon(img, cx, cy, size, fill):
    text(img, (cx, cy), '☎', size, fill, SYM, 'mm')

def phone_mock(img, shot, x, y, w, rot=0, dark=False, crop_top=0, crop_h=None, frame=None):
    """Phone with a real app screenshot inside."""
    sc = Image.open(shot).convert('RGB')
    if crop_h: sc = sc.crop((0, crop_top, sc.width, crop_top + crop_h))
    bez = 14
    iw = int((w - 2 * bez) * S)
    s2 = sc.resize((iw, int(sc.height * iw / sc.width)), Image.LANCZOS)
    ph_h = s2.height + int(2 * bez * S) + int(18 * S)
    pw = int(w * S)
    ph = Image.new('RGBA', (pw, ph_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ph)
    fc = frame or ((30, 36, 32) if dark else (20, 26, 22))
    d.rounded_rectangle([0, 0, pw - 1, ph_h - 1], int(46 * S), fill=fc + (255,))
    d.rounded_rectangle([3 * S, 3 * S, pw - 4 * S, ph_h - 4 * S], int(44 * S), outline=(90, 100, 94, 255), width=int(2 * S))
    m = Image.new('L', s2.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, s2.width - 1, s2.height - 1], int(34 * S), fill=255)
    ph.paste(s2, (int(bez * S), int((bez + 18) * S)), m)
    d.rounded_rectangle([pw / 2 - 40 * S, 10 * S, pw / 2 + 40 * S, 22 * S], 6 * S, fill=(0, 0, 0, 255))
    # glossy diagonal sheen
    sheen = Image.new('L', ph.size, 0)
    ImageDraw.Draw(sheen).polygon([(0, 0), (pw * 0.55, 0), (0, ph_h * 0.45)], fill=38)
    sheen = sheen.filter(ImageFilter.GaussianBlur(10 * S))
    sheen = ImageChops.multiply(sheen, ph.getchannel('A'))
    ph.paste(Image.new('RGBA', ph.size, (255, 255, 255, 255)), (0, 0), sheen)
    if rot: ph = ph.rotate(rot, resample=Image.BICUBIC, expand=True)
    # shadow
    P = 60 * S
    a = Image.new('L', (ph.size[0] + 2 * P, ph.size[1] + 2 * P), 0); a.paste(ph.getchannel('A'), (P, P))
    a = a.filter(ImageFilter.GaussianBlur(18 * S)).point(lambda v: int(v * 0.3))
    img.paste(Image.new('RGB', a.size, (0, 0, 0)), (int(x * S) - P, int((y + 16) * S) - P), a)
    img.paste(ph, (int(x * S), int(y * S)), ph)
    return ph.size[0] / S, ph.size[1] / S

def logo(img, x, y, size, dark=False):
    """Shri Tech wordmark with a small leaf-spark mark."""
    d = ImageDraw.Draw(img)
    r = size * 0.62
    cx, cy = x + r, y + size * 0.62
    grad_box(img, (cx - r, cy - r, cx + r, cy + r), r * 0.42, LGREEN, GREEN)
    text(img, (cx, cy + size * 0.02), 'S', size * 0.95, WHITE if not dark else BLACK, PB, 'mm')
    d.ellipse([(cx + r * 0.55) * S, (cy - r * 1.05) * S, (cx + r * 1.0) * S, (cy - r * 0.6) * S], fill=YEL)
    x2 = x + 2 * r + size * 0.28
    text(img, (x2, cy), 'Shri', size, WHITE if dark else DEEP, PB, 'lm')
    text(img, (x2 + tw('Shri', size, PB) + size * 0.16, cy), 'Tech', size, GREEN if not dark else LGREEN, PB, 'lm')
    return x2 + tw('Shri Tech', size, PB) + size * 0.2

def sparkle(img, cx, cy, r, color, alpha=255):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    pts = []
    for i in range(8):
        a = i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.22
        pts.append(((cx + rr * math.cos(a)) * S, (cy + rr * math.sin(a)) * S))
    d.polygon(pts, fill=color + (alpha,))
    img.paste(lay, (0, 0), lay)

def finish(img, path):
    out = img.resize((W // S, H // S), Image.LANCZOS)
    out.save(path, quality=95, subsampling=0)
    return out
