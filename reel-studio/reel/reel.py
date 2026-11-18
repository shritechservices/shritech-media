import math, random, sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from captions import draw_caption

W, H, FPS = 1080, 1920, 30
LANG = os.environ.get('REEL_LANG', 'hi')
EN = {'रोज़ नई पोस्ट': 'Still designing', 'डिज़ाइन करने में': 'posts by hand', 'समय बर्बाद?': 'every day?', 'अब नहीं!': 'Not anymore!', 'AI करेगा आपका काम': 'Let AI do the work', 'AI से बिज़नेस पोस्ट': 'AI business posts', 'सिर्फ 1 मिनट में!': 'in just 1 minute!', 'स्टेप 1': 'STEP 1', 'स्टेप 2': 'STEP 2', 'स्टेप 3': 'STEP 3', 'अपनी बिज़नेस डिटेल्स भरें': 'Add your business details', 'नाम': 'Name', 'लोगो': 'Logo', 'ब्रांड कलर': 'Brand colours', 'हिंदी / English': 'Hindi / English', 'AI बनाए शानदार डिज़ाइन': 'AI creates stunning designs', 'सेकंडों में!': 'in seconds!', 'आपके रंग + आपका लोगो': 'Your colours + your logo', 'एक क्लिक में पोस्ट': 'Post in one click', 'Facebook + Instagram पर एक साथ': 'Facebook + Instagram together', 'WhatsApp बल्क मैसेजिंग': 'WhatsApp bulk messaging', 'Excel से कॉन्टैक्ट्स अपलोड करें': 'Upload contacts from Excel', 'कॉन्टैक्ट्स एक फ़ाइल में': 'contacts in one file', 'डुप्लीकेट अपने-आप साफ़': 'Duplicates auto-cleaned', 'मार्केटिंग कैम्पेन': 'Marketing campaigns', 'ऑफ़र सीधे ग्राहक के WhatsApp पर': "Offers straight to customers' WhatsApp", 'किसने देखा, किसने जवाब दिया': 'Who saw it, who replied', 'सब ट्रैक करें!': 'Track it all!', 'रिप्लाई चैट': 'Reply chat', 'टेम्पलेट्स': 'Templates', 'अधिक जानकारी के लिए': 'For more information', 'संपर्क करें': 'Contact us', 'AI पोस्ट डिज़ाइन': 'AI post design', 'वन-क्लिक सोशल पोस्टिंग': 'One-click social posting', 'WhatsApp मार्केटिंग': 'WhatsApp marketing', 'आज ही कॉल करें!': 'Call us today!'}
def tr(s): return EN.get(s, s) if LANG == 'en' else s
DUR = 60.0
UP = '/mnt/user-data/uploads/'
FB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
FSYM = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
GREEN = (34, 197, 94)
GOLD = (250, 204, 21)
WHITE = (255, 255, 255)

def font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)

# ---------------- easing ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def eback(x, s=1.7):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def prog(t, a, d): return clamp((t - a) / d)

# ---------------- assets ----------------
_cache = {}
def shot(name):
    if name not in _cache:
        _cache[name] = Image.open(UP + name + '-image.jpg').convert('RGB')
    return _cache[name]

def text_img(txt, size, fill=WHITE, path=FB, grad=None, glow=None, shadow=True, stroke=0):
    txt = tr(txt)
    key = ('t', txt, size, fill, path, grad, glow, shadow, stroke)
    if key in _cache: return _cache[key]
    f = font(path, size)
    while f.getlength(txt) > 980 and size > 30:
        size = int(size * 0.94); f = font(path, size)
    l, t, r, b = f.getbbox(txt, stroke_width=stroke)
    pad = 60
    w, h = r - l + pad * 2, b - t + pad * 2
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).text((pad - l, pad - t), txt, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if glow:
        g = mask.filter(ImageFilter.GaussianBlur(18)).point(lambda v: min(255, v * 1.6))
        layer = Image.new('RGBA', (w, h), glow + (0,)); layer.putalpha(g)
        out = Image.alpha_composite(out, layer)
    if shadow:
        s = Image.new('L', (w, h), 0); s.paste(mask, (0, 10))
        s = s.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * 0.85))
        layer = Image.new('RGBA', (w, h), (0, 0, 0, 0)); layer.putalpha(s)
        out = Image.alpha_composite(out, layer)
    if grad:
        g = Image.new('RGBA', (w, h))
        a = np.linspace(0, 1, h)[:, None, None]
        c1, c2 = np.array(grad[0]), np.array(grad[1])
        arr = (c1 * (1 - a) + c2 * a).astype(np.uint8)
        arr = np.broadcast_to(arr, (h, w, 3))
        g = Image.fromarray(np.dstack([arr, np.array(mask)]).astype(np.uint8), 'RGBA')
    else:
        g = Image.new('RGBA', (w, h), fill + (0,)); g.putalpha(mask)
    out = Image.alpha_composite(out, g)
    _cache[key] = out
    return out

def rrect_mask(w, h, r, scale=3):
    m = Image.new('L', (w * scale, h * scale), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * scale - 1, h * scale - 1), r * scale, fill=255)
    return m.resize((w, h), Image.LANCZOS)

def shadowed(img, radius=28, blur=28, off=22, glow=GREEN, glow_a=0.55, dark_a=0.75):
    """Rounded card + dark drop shadow + coloured glow."""
    w, h = img.size
    pad = blur * 3 + off
    W2, H2 = w + pad * 2, h + pad * 2
    m = rrect_mask(w, h, radius)
    out = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
    if glow:
        gm = Image.new('L', (W2, H2), 0); gm.paste(m, (pad, pad))
        gm = gm.filter(ImageFilter.GaussianBlur(blur * 1.3)).point(lambda v: int(v * glow_a))
        gl = Image.new('RGBA', (W2, H2), glow + (0,)); gl.putalpha(gm)
        out = Image.alpha_composite(out, gl)
    dm = Image.new('L', (W2, H2), 0); dm.paste(m, (pad + off // 2, pad + off))
    dm = dm.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * dark_a))
    dl = Image.new('RGBA', (W2, H2), (0, 0, 0, 0)); dl.putalpha(dm)
    out = Image.alpha_composite(out, dl)
    card = img.convert('RGBA'); card.putalpha(ImageChops.multiply(card.getchannel('A'), m))
    out.alpha_composite(card, (pad, pad))
    return out

# phone frame
SW, SH = 560, 1010  # screen
BZ = 16
PW, PH = SW + BZ * 2, SH + BZ * 2
def phone_shell():
    if 'shell' in _cache: return _cache['shell']
    body = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    d.rounded_rectangle((0, 0, PW - 1, PH - 1), 64, fill=(24, 26, 25, 255), outline=(70, 80, 74, 255), width=3)
    d.rounded_rectangle((4, 4, PW - 5, PH - 5), 60, outline=(40, 45, 42, 255), width=2)
    # side buttons
    sh = shadowed(body, radius=64, blur=34, off=30, glow=GREEN, glow_a=0.6)
    _cache['shell'] = sh
    return sh

SCREEN_MASK = None
def phone(name, sy=0.0, name2=None, mix=0.0):
    """sy = scroll fraction 0..1; name2/mix = slide transition to another screenshot."""
    global SCREEN_MASK
    if SCREEN_MASK is None: SCREEN_MASK = rrect_mask(SW, SH, 48)
    def screen(n, s):
        im = shot(n); sc = SW / im.width
        visible = SH / sc
        y0 = (im.height - visible) * s
        return im.crop((0, int(y0), im.width, int(y0 + visible))).resize((SW, SH), Image.BILINEAR)
    scr = screen(name, sy)
    if name2 and mix > 0:
        s2 = screen(name2, 0.0)
        off = int(SW * eio(mix))
        canvas = Image.new('RGB', (SW, SH))
        canvas.paste(scr, (-off, 0)); canvas.paste(s2, (SW - off, 0))
        scr = canvas
    shell = phone_shell().copy()
    pad = (shell.width - PW) // 2
    scr = scr.convert('RGBA'); scr.putalpha(SCREEN_MASK)
    shell.alpha_composite(scr, (pad + BZ, pad + BZ))
    # glass reflection
    if 'refl' not in _cache:
        r = Image.new('L', (SW, SH), 0)
        ImageDraw.Draw(r).polygon([(0, 0), (SW * 0.55, 0), (0, SH * 0.45)], fill=22)
        r = ImageChops.multiply(r, SCREEN_MASK)
        rl = Image.new('RGBA', (SW, SH), (255, 255, 255, 0)); rl.putalpha(r)
        _cache['refl'] = rl
    shell.alpha_composite(_cache['refl'], (pad + BZ, pad + BZ))
    # notch
    d = ImageDraw.Draw(shell)
    cx = shell.width // 2
    d.rounded_rectangle((cx - 60, pad + BZ + 10, cx + 60, pad + BZ + 38), 14, fill=(0, 0, 0, 255))
    return shell

def crop_card(name, box, width, radius=26, glow=GREEN):
    key = ('cc', name, box, width, glow)
    if key in _cache: return _cache[key]
    im = shot(name).crop(box)
    h = int(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS)
    out = shadowed(im, radius=radius, blur=24, off=20, glow=glow, glow_a=0.5)
    _cache[key] = out
    return out

def pill(txt, size=38, bg=(16, 40, 26), fg=GREEN, border=GREEN, path=FB, icon=False):
    txt = tr(txt)
    key = ('pill', txt, size, bg, fg, border, icon)
    if key in _cache: return _cache[key]
    f = font(path, size)
    l, t, r, b = f.getbbox(txt)
    h = int(size * 1.9)
    ic = int(size * 1.1) + 16 if icon else 0
    w = int(r - l + size * 1.4 + ic)
    S = 2
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * S - 1, h * S - 1), h * S // 2, fill=bg + (245,), outline=border + (255,), width=4 * S)
    if icon:
        cx, cy, rr = (size * 0.7 + size * 0.55) * S, h * S / 2, size * 0.55 * S
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=fg + (255,))
        d.line([(cx - rr * 0.45, cy + rr * 0.02), (cx - rr * 0.1, cy + rr * 0.38), (cx + rr * 0.5, cy - rr * 0.35)], fill=bg + (255,), width=int(rr * 0.28), joint='curve')
    im = im.resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.text(((w - ic - (r - l)) / 2 - l + ic, (h - (b - t)) / 2 - t), txt, font=f, fill=fg)
    out = shadowed(im, radius=h // 2, blur=14, off=10, glow=border, glow_a=0.45, dark_a=0.7)
    _cache[key] = out
    return out

# ---------------- compositing helpers ----------------
def put(base, im, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01: return
    if abs(scale - 1) > 0.003:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = im.getchannel('A').point(lambda v: int(v * alpha))
        im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))) if False else \
        _paste(base, im, int(cx - im.width / 2), int(cy - im.height / 2))

def _paste(base, im, x, y):
    # alpha_composite with clipping
    bx0, by0 = max(0, x), max(0, y)
    bx1, by1 = min(base.width, x + im.width), min(base.height, y + im.height)
    if bx1 <= bx0 or by1 <= by0: return
    sub = im.crop((bx0 - x, by0 - y, bx1 - x, by1 - y))
    base.alpha_composite(sub, (bx0, by0))

# ---------------- background ----------------
rng = random.Random(7)
PARTS = [(rng.random() * W, rng.random() * H, rng.uniform(2, 6), rng.uniform(20, 70), rng.random() * 6.28, rng.choice([GREEN, GOLD, WHITE])) for _ in range(46)]
LW, LH = 135, 240
yy, xx = np.mgrid[0:LH, 0:LW].astype(np.float32)

def glow_sprite(c, r):
    key = ('gs', c, r)
    if key in _cache: return _cache[key]
    s = r * 6
    m = Image.new('L', (s, s), 0)
    ImageDraw.Draw(m).ellipse((s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(r * 1.2))
    m2 = Image.new('L', (s, s), 0)
    ImageDraw.Draw(m2).ellipse((s / 2 - r * 0.45, s / 2 - r * 0.45, s / 2 + r * 0.45, s / 2 + r * 0.45), fill=255)
    m = ImageChops.lighter(m, m2)
    im = Image.new('RGBA', (s, s), c + (0,)); im.putalpha(m)
    _cache[key] = im
    return im

def grid_tile():
    if 'grid' in _cache: return _cache['grid']
    g = Image.new('RGBA', (W + 60, H + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    for x in range(0, W + 60, 60):
        for y in range(0, H + 60, 60):
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(120, 200, 150, 38))
    _cache['grid'] = g
    return g

def background(t, accent=0.0):
    arr = np.zeros((LH, LW, 3), np.float32)
    arr[:] = (6, 12, 9)
    blobs = [
        (0.25 + 0.15 * math.sin(t * 0.4), 0.25 + 0.1 * math.cos(t * 0.33), 70, (34, 197, 94), 0.55),
        (0.8 + 0.12 * math.cos(t * 0.37), 0.7 + 0.12 * math.sin(t * 0.29), 80, (250, 180, 21), 0.38),
        (0.5 + 0.3 * math.sin(t * 0.21 + 2), 0.95 + 0.05 * math.sin(t * 0.5), 60, (16, 120, 70), 0.5),
    ]
    for bx, by, r, c, a in blobs:
        d2 = ((xx - bx * LW) ** 2 + (yy - by * LH) ** 2) / (r * r)
        f = np.exp(-d2 * 2.2)[..., None] * a
        arr += f * np.array(c, np.float32)
    # vignette
    v = 1 - 0.55 * (((xx / LW - 0.5) ** 2 + (yy / LH - 0.5) ** 2) * 2.2)
    arr *= np.clip(v, 0.25, 1)[..., None]
    if accent > 0: arr += accent * 60
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).convert('RGBA')
    g = grid_tile()
    off = int((t * 18) % 60)
    img.alpha_composite(g.crop((off, off, off + W, off + H)))
    for (px, py, r, sp, ph, c) in PARTS:
        y = (py - t * sp) % (H + 100) - 50
        x = px + 20 * math.sin(t * 0.8 + ph)
        tw = 0.5 + 0.5 * math.sin(t * 2 + ph)
        s = glow_sprite(c, int(r))
        a = s.getchannel('A').point(lambda v, k=0.35 + 0.5 * tw: int(v * k))
        s2 = s.copy(); s2.putalpha(a)
        _paste(img, s2, int(x - s.width / 2), int(y - s.height / 2))
    return img

def sweep(base, p):
    """diagonal light sweep, p 0..1"""
    if p <= 0 or p >= 1: return
    if 'sweep' not in _cache:
        bw = 420
        m = Image.new('L', (bw, 1), 0)
        for i in range(bw):
            m.putpixel((i, 0), int(150 * math.sin(math.pi * i / bw) ** 2))
        m = m.resize((bw, H * 2))
        im = Image.new('RGBA', (bw, H * 2), (210, 255, 225, 0)); im.putalpha(m)
        _cache['sweep'] = im.rotate(-20, Image.BICUBIC, expand=True)
    s = _cache['sweep']
    x = -s.width + (W + s.width * 2) * p
    _paste(base, s, int(x - s.width / 2), int(H / 2 - s.height / 2))

# ---------------- persistent overlays ----------------
def topbar(base, t):
    a = eo(prog(t, 10.8, 0.6)) * (1 - eo(prog(t, 53.0, 0.5)))
    if a <= 0: return
    logo1 = text_img('Shri', 46, WHITE)
    logo2 = text_img('Tech', 46, GREEN, glow=GREEN)
    y = 150 - 30 * (1 - a)
    put(base, logo1, 70 + logo1.width / 2 - 60, y, alpha=a)
    put(base, logo2, 70 + logo1.width - 120 - 60 + logo2.width / 2 + 4, y, alpha=a)
    p = pill('☎ 9993615146', 34, bg=(40, 32, 6), fg=GOLD, border=GOLD, path=FSYM)
    pulse = 1 + 0.04 * math.sin(t * 6)
    put(base, p, W - 70 - p.width / 2 + 60, y, scale=pulse, alpha=a)

def headline(base, t, t0, lines, y0=330, exit_t=None):
    """lines: list of (text, size, style) style: 'w' white, 'g' gradient, 'gold'"""
    y = y0
    for i, (txt, size, st) in enumerate(lines):
        if st == 'g': im = text_img(txt, size, grad=(GREEN, GOLD), glow=GREEN)
        elif st == 'gold': im = text_img(txt, size, GOLD, glow=(180, 120, 0))
        elif st == 'gr': im = text_img(txt, size, GREEN, glow=GREEN)
        else: im = text_img(txt, size, WHITE, path=FB if size > 50 else FM)
        p = prog(t, t0 + 0.15 * i, 0.55)
        a = eo(p); sc = 0.6 + 0.4 * eback(p)
        if exit_t is not None:
            e = prog(t, exit_t, 0.35); a *= 1 - e; sc *= 1 + 0.25 * e
        put(base, im, W / 2, y + 40 * (1 - eo(p)), scale=sc, alpha=a)
        if i + 1 < len(lines): y += 0.66 * (size + lines[i + 1][1]) + 12

def phone_motion(t, t0, t1, cy=1150):
    p = prog(t, t0, 0.8)
    e = prog(t, t1 - 0.35, 0.35)
    y = cy + 900 * (1 - eback(p, 1.2)) - 0 * e
    rot = 8 * (1 - eo(p)) + 1.5 * math.sin(t * 1.3)
    sc = 0.92 + 0.08 * eo(p) - 0.15 * e
    y += 18 * math.sin(t * 1.7)
    return y, rot, sc, 1 - e

# ---------------- scenes ----------------
def s_hook(base, t):
    # flying generated designs in background
    cards = [crop_card('dfd79390', (394, 885, 686, 1176), 380, glow=GOLD),
             crop_card('dfd79390', (78, 885, 370, 1176), 380),
             crop_card('dfd79390', (711, 885, 1001, 1176), 380, glow=GOLD)]
    for i, c in enumerate(cards):
        p = prog(t, 0.2 + i * 0.25, 1.0)
        x = [230, 850, 540][i]; y = [1300, 1420, 1600][i]
        x += 60 * math.sin(t + i)
        put(base, c, x, y + 500 * (1 - eo(p)), scale=0.9 + 0.1 * eo(p), rot=[-12, 10, -4][i] + 3 * math.sin(t * 1.5 + i),
            alpha=eo(p) * (1 - prog(t, 4.6, 0.4)) * 0.95)
    headline(base, t, 0.2, [('रोज़ नई पोस्ट', 92, 'w'), ('डिज़ाइन करने में', 92, 'w'), ('समय बर्बाद?', 124, 'gold')], y0=330, exit_t=2.7)
    # stamp
    p = prog(t, 2.9, 0.45)
    if p > 0:
        sc = 2.4 - 1.4 * eback(p, 2.5)
        a = eo(p) * (1 - prog(t, 4.65, 0.35))
        put(base, text_img('अब नहीं!', 190, grad=(GREEN, GOLD), glow=GREEN), W / 2, 560, scale=sc, rot=-6, alpha=a)
        put(base, text_img('AI करेगा आपका काम', 70, WHITE), W / 2, 790, scale=0.8 + 0.2 * eo(prog(t, 3.3, 0.4)), alpha=eo(prog(t, 3.3, 0.4)) * (1 - prog(t, 4.65, 0.35)))

def s_brand(base, t):
    t0 = 5.0
    p = prog(t, t0, 0.7)
    sc = 0.3 + 0.7 * eback(p, 2)
    a1 = eo(p) * (1 - prog(t, 10.6, 0.4))
    l1 = text_img('Shri', 190, WHITE); l2 = text_img('Tech', 190, GREEN, glow=GREEN)
    tw = (l1.width - 120 + l2.width - 120) * sc
    lift = 120 * eio(prog(t, t0 + 1.6, 0.7))
    cy = 400 - lift
    put(base, l1, W / 2 - tw / 2 + (l1.width - 120) * sc / 2, cy, scale=sc, alpha=a1)
    put(base, l2, W / 2 + tw / 2 - (l2.width - 120) * sc / 2, cy, scale=sc, alpha=a1)
    headline(base, t, t0 + 0.9, [('AI से बिज़नेस पोस्ट', 72, 'w'), ('सिर्फ 1 मिनट में!', 92, 'g')], y0=640 - lift, exit_t=10.6)
    y, rot, sc2, a = phone_motion(t, t0 + 1.4, 11.0, cy=1330)
    put(base, phone('173cd744', 0.25 * eio(prog(t, t0 + 2.5, 3.0))), W / 2, y, scale=sc2 * 0.82, rot=rot, alpha=a)

def side_pills(base, t, items, t0, tend):
    for i, (txt, x, y, c) in enumerate(items):
        p = prog(t, t0 + 0.3 * i, 0.5)
        a = eo(p) * (1 - prog(t, tend - 0.35, 0.35))
        pl = pill(txt, 36, bg=(14, 36, 22) if c == GREEN else (44, 34, 4), fg=c, border=c, icon=tr(txt) in ('Seen', 'Liked'))
        put(base, pl, x, y + 10 * math.sin(t * 2 + i), scale=0.5 + 0.5 * eback(p), rot=4 * math.sin(t + i * 2), alpha=a)

def s_create(base, t):
    t0, t1 = 11.0, 19.0
    headline(base, t, t0, [('स्टेप 1', 44, 'gr'), ('अपनी बिज़नेस डिटेल्स भरें', 70, 'w')], y0=290, exit_t=t1 - 0.35)
    y, rot, sc, a = phone_motion(t, t0 + 0.2, t1, cy=1160)
    mix = prog(t, t0 + 3.8, 0.6)
    put(base, phone('beb50932', 0.0 if mix < 1 else 0, '21442f26' if mix > 0 else None, mix) if mix < 1 else
        phone('21442f26', 0.3 * eio(prog(t, t0 + 4.6, 2.8))), W / 2, y, scale=sc * 0.95, rot=rot, alpha=a)
    side_pills(base, t, [('नाम', 170, 720, GREEN), ('लोगो', 910, 860, GOLD), ('ब्रांड कलर', 190, 1300, GOLD),
                         ('हिंदी / English', 870, 1480, GREEN)], t0 + 1.2, t1)

def s_ai(base, t):
    t0, t1 = 19.0, 26.0
    headline(base, t, t0, [('स्टेप 2', 44, 'gr'), ('AI बनाए शानदार डिज़ाइन', 70, 'w'), ('सेकंडों में!', 100, 'g')], y0=290, exit_t=t1 - 0.35)
    cards = [(crop_card('dfd79390', (78, 885, 370, 1176), 470), -1),
             (crop_card('dfd79390', (711, 885, 1001, 1176), 470, glow=GOLD), 1),
             (crop_card('dfd79390', (394, 885, 686, 1176), 520, glow=GOLD), 0)]
    e = prog(t, t1 - 0.35, 0.35)
    for i, (c, side) in enumerate(cards):
        p = prog(t, t0 + 0.6 + 0.3 * i, 0.8)
        fan = eback(prog(t, t0 + 1.8, 0.8), 1.4)
        x = W / 2 + side * 270 * fan
        y = 1180 + abs(side) * 60 * fan + 20 * math.sin(t * 1.6 + i)
        rot = -side * 12 * fan + 2 * math.sin(t * 1.2 + i)
        sc = (0.4 + 0.6 * eback(p)) * (1 + 0.04 * math.sin(t * 2 + i))
        put(base, c, x, y + 300 * (1 - eo(p)), scale=sc * (1 - 0.2 * e), rot=rot, alpha=eo(p) * (1 - e))
    # sparkles
    for k in range(6):
        ph = t * 3 + k
        a = max(0, math.sin(ph)) * eo(prog(t, t0 + 2, 0.5)) * (1 - e)
        put(base, glow_sprite(GOLD, 10), 140 + k * 160, 900 + 520 * (k % 2) + 30 * math.sin(ph), scale=0.8 + 0.6 * a, alpha=a)
    p = prog(t, t0 + 3.0, 0.5)
    put(base, pill('आपके रंग + आपका लोगो', 40, bg=(44, 34, 4), fg=GOLD, border=GOLD), W / 2, 760,
        scale=0.5 + 0.5 * eback(p), alpha=eo(p) * (1 - e))

def s_post(base, t):
    t0, t1 = 26.0, 33.0
    headline(base, t, t0, [('स्टेप 3', 44, 'gr'), ('एक क्लिक में पोस्ट', 84, 'g'), ('Facebook + Instagram पर एक साथ', 52, 'w')], y0=290, exit_t=t1 - 0.35)
    y, rot, sc, a = phone_motion(t, t0 + 0.2, t1, cy=1220)
    put(base, phone('3c987a50', 0.0), W / 2 - 150 * eio(prog(t, t0 + 1.8, 0.6)), y, scale=sc * 0.85, rot=rot, alpha=a * (1 - 0.35 * eio(prog(t, t0 + 1.8, 0.6))))
    card = crop_card('3c987a50', (30, 808, 1050, 1625), 640, glow=GOLD)
    p = prog(t, t0 + 1.9, 0.7)
    e = prog(t, t1 - 0.35, 0.35)
    put(base, card, W / 2 + 120 + 300 * (1 - eo(p)), 1180 + 12 * math.sin(t * 1.8), scale=(0.6 + 0.4 * eback(p)) * (1 + 0.03 * math.sin(t * 3)), rot=-3 + 1.5 * math.sin(t),
        alpha=eo(p) * (1 - e))
    # check bursts
    for i, yy_ in enumerate([1015, 1115]):
        pp = prog(t, t0 + 3.0 + 0.5 * i, 0.5)
        if pp > 0:
            r = 30 + 90 * eo(pp)
            ring = Image.new('RGBA', (int(r * 2 + 10), int(r * 2 + 10)), (0, 0, 0, 0))
            ImageDraw.Draw(ring).ellipse((5, 5, r * 2 + 5, r * 2 + 5), outline=GREEN + (int(255 * (1 - pp)),), width=6)
            put(base, ring, W / 2 + 380, yy_, alpha=1 - e)

def s_whatsapp(base, t):
    t0, t1 = 33.0, 40.0
    headline(base, t, t0, [('WhatsApp बल्क मैसेजिंग', 74, 'g'), ('Excel से कॉन्टैक्ट्स अपलोड करें', 54, 'w')], y0=300, exit_t=t1 - 0.35)
    y, rot, sc, a = phone_motion(t, t0 + 0.2, t1, cy=1210)
    put(base, phone('8de181ef', 0.15 * eio(prog(t, t0 + 1, 4))), W / 2, y, scale=sc * 0.88, rot=rot, alpha=a)
    # counter card
    p = prog(t, t0 + 1.6, 0.6); e = prog(t, t1 - 0.35, 0.35)
    if p > 0:
        n = int(5000 * eio(prog(t, t0 + 1.8, 1.8)))
        num = text_img(f'{n:,}', 110, grad=(GREEN, GOLD), glow=GREEN)
        lab = text_img('कॉन्टैक्ट्स एक फ़ाइल में', 42, WHITE, path=FM)
        if 'ccard' not in _cache:
            bg = Image.new('RGBA', (560, 300), (14, 22, 17, 240))
            d = ImageDraw.Draw(bg); d.rounded_rectangle((0, 0, 559, 299), 36, outline=GREEN + (255,), width=4)
            _cache['ccard'] = shadowed(bg, radius=36, blur=22, off=18)
        cc = _cache['ccard'].copy()
        _paste(cc, num, cc.width // 2 - num.width // 2, cc.height // 2 - num.height // 2 - 40)
        _paste(cc, lab, cc.width // 2 - lab.width // 2, cc.height // 2 - lab.height // 2 + 75)
        put(base, cc, W / 2 + 200, 1330 + 14 * math.sin(t * 2), scale=0.5 + 0.5 * eback(p), rot=-3, alpha=eo(p) * (1 - e))
    side_pills(base, t, [('डुप्लीकेट अपने-आप साफ़', 300, 780, GOLD)], t0 + 3.0, t1)

def s_campaign(base, t):
    t0, t1 = 40.0, 47.0
    headline(base, t, t0, [('मार्केटिंग कैम्पेन', 84, 'g'), ('ऑफ़र सीधे ग्राहक के WhatsApp पर', 52, 'w')], y0=300, exit_t=t1 - 0.35)
    y, rot, sc, a = phone_motion(t, t0 + 0.2, t1, cy=1220)
    k = eio(prog(t, t0 + 2.6, 0.6))
    put(base, phone('e5d0d48b', 0.35 * eio(prog(t, t0 + 0.8, 1.8))), W / 2 - 160 * k, y, scale=sc * 0.88 * (1 - 0.12 * k), rot=rot - 4 * k, alpha=a * (1 - 0.4 * k))
    card = crop_card('4e9d3978', (69, 268, 1011, 1690), 560)
    p = prog(t, t0 + 2.7, 0.7); e = prog(t, t1 - 0.35, 0.35)
    put(base, card, W / 2 + 140 + 400 * (1 - eo(p)), 1170 + 14 * math.sin(t * 1.6), scale=(0.6 + 0.4 * eback(p)), rot=3 - 1.5 * math.sin(t), alpha=eo(p) * (1 - e))

def s_track(base, t):
    t0, t1 = 47.0, 53.0
    headline(base, t, t0, [('किसने देखा, किसने जवाब दिया', 62, 'w'), ('सब ट्रैक करें!', 92, 'g')], y0=300, exit_t=t1 - 0.35)
    y, rot, sc, a = phone_motion(t, t0 + 0.2, t1, cy=1230)
    mix = prog(t, t0 + 2.8, 0.6)
    im = phone('76ff22fd', 0.3 * eio(prog(t, t0 + 0.8, 1.8)), '96a199dd', mix) if mix < 1 else phone('96a199dd', 0.2 * eio(prog(t, t0 + 3.5, 2)))
    put(base, im, W / 2, y, scale=sc * 0.88, rot=rot, alpha=a)
    side_pills(base, t, [('Seen', 190, 820, GREEN), ('Liked', 900, 960, GOLD), ('रिप्लाई चैट', 200, 1430, GOLD), ('टेम्पलेट्स', 880, 1380, GREEN)], t0 + 1.0, t1)

def phone_icon(size, color):
    key = ('pi', size, color)
    if key in _cache: return _cache[key]
    im = text_img('☎', size, color, path=FSYM, shadow=False)
    _cache[key] = im
    return im

def s_cta(base, t):
    t0 = 53.0
    headline(base, t, t0, [('अधिक जानकारी के लिए', 76, 'w'), ('संपर्क करें', 110, 'g')], y0=360)
    # call button
    p = prog(t, t0 + 0.8, 0.7)
    if p > 0:
        if 'callbtn' not in _cache:
            bw, bh = 900, 200
            bg = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
            arr = np.zeros((bh, bw, 4), np.uint8)
            gx = np.linspace(0, 1, bw)[None, :, None]
            col = np.array(GREEN) * (1 - gx) + np.array((22, 163, 74)) * gx
            arr[..., :3] = np.broadcast_to(col, (bh, bw, 3)); arr[..., 3] = 255
            bg = Image.fromarray(arr, 'RGBA')
            bg.putalpha(rrect_mask(bw, bh, 100))
            ic = text_img('☎', 96, (8, 30, 16), path=FSYM, shadow=False)
            _paste(bg, ic, 110 - ic.width // 2, bh // 2 - ic.height // 2)
            nm = text_img('9993615146', 104, (8, 30, 16), shadow=False)
            _paste(bg, nm, 520 - nm.width // 2, bh // 2 - nm.height // 2 + 4)
            _cache['callbtn'] = shadowed(bg, radius=100, blur=34, off=24, glow=GREEN, glow_a=0.9)
        # ripples
        for k in range(3):
            ph = ((t - t0) * 0.8 + k / 3) % 1
            r = Image.new('RGBA', (1100, 400), (0, 0, 0, 0))
            w2, h2 = 450 + 120 * ph, 100 + 90 * ph
            ImageDraw.Draw(r).rounded_rectangle((550 - w2, 200 - h2, 550 + w2, 200 + h2), int(h2), outline=GREEN + (int(200 * (1 - ph) * eo(p)),), width=5)
            put(base, r, W / 2, 800)
        pulse = 1 + 0.035 * math.sin((t - t0) * 7)
        put(base, _cache['callbtn'], W / 2, 800, scale=(0.3 + 0.7 * eback(p, 2.2)) * pulse, alpha=eo(p))
    # features recap pills
    feats = [('AI पोस्ट डिज़ाइन', 1010, GREEN), ('वन-क्लिक सोशल पोस्टिंग', 1115, GOLD), ('WhatsApp मार्केटिंग', 1220, GREEN)]
    for i, (txt, y, c) in enumerate(feats):
        pp = prog(t, t0 + 1.5 + 0.25 * i, 0.5)
        put(base, pill(txt, 40, bg=(14, 36, 22) if c == GREEN else (44, 34, 4), fg=c, border=c, icon=True),
            W / 2 + 500 * (1 - eo(pp)) * (1 if i % 2 else -1), y, scale=0.9 + 0.1 * eo(pp), alpha=eo(pp))
    # logo
    pp = prog(t, t0 + 2.6, 0.6)
    l1 = text_img('Shri', 100, WHITE); l2 = text_img('Tech', 100, GREEN, glow=GREEN)
    sc = 0.6 + 0.4 * eback(pp)
    tw = (l1.width - 120 + l2.width - 120) * sc
    put(base, l1, W / 2 - tw / 2 + (l1.width - 120) * sc / 2, 1350, scale=sc, alpha=eo(pp))
    put(base, l2, W / 2 + tw / 2 - (l2.width - 120) * sc / 2, 1350, scale=sc, alpha=eo(pp))
    pp = prog(t, t0 + 3.3, 0.5)
    put(base, text_img('आज ही कॉल करें!', 64, GOLD, glow=(180, 120, 0)), W / 2, 1460, scale=0.7 + 0.3 * eback(pp) + 0.03 * math.sin(t * 5), alpha=eo(pp))

SCENES = [(0, 5, s_hook), (5, 11, s_brand), (11, 19, s_create), (19, 26, s_ai), (26, 33, s_post),
          (33, 40, s_whatsapp), (40, 47, s_campaign), (47, 53, s_track), (53, 60, s_cta)]
BOUNDS = [s[1] for s in SCENES[:-1]]

def frame(t):
    acc = 0.0
    for b in BOUNDS:
        d = abs(t - b)
        if d < 0.15: acc = max(acc, 1 - d / 0.15)
    base = background(t, accent=acc * 0.5)
    for a, b, fn in SCENES:
        if a - 0.01 <= t < b + 0.01:
            fn(base, t)
    topbar(base, t)
    draw_caption(base, t)
    for b in BOUNDS:
        sweep(base, (t - (b - 0.35)) / 0.7)
    # fade in / out
    out = base.convert('RGB')
    if t < 0.3:
        out = Image.blend(Image.new('RGB', (W, H)), out, t / 0.3)
    return out

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
            frame(float(ts)).save(f'/home/claude/reel/still_{LANG}_{ts}.jpg', quality=85)
    else:
        render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
