import os, sys, math, subprocess
sys.path.insert(0, '/home/claude/reel')
os.environ['REEL_LANG'] = 'hi'
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import reel as R
import reel2 as R2
from reel import (W, H, FPS, GREEN, GOLD, WHITE, FB, FM, FSYM, text_img, pill, put, _paste, phone, crop_card,
                  shadowed, rrect_mask, glow_sprite, background, sweep, eo, eio, eback, prog, _cache)

RED = (239, 68, 68)
# audio pieces kept from the source (src_start, src_end)
PIECES = [(0.0, 31.95), (35.85, 37.5), (44.5, 46.75), (49.0, 52.62)]
OFF = []
o = 0
for a, b in PIECES:
    OFF.append((a, b, o)); o += b - a
AUDIO_END = o          # ~39.5
DUR = AUDIO_END + 6.5  # CTA tail

def m(ts):
    for a, b, oo in OFF:
        if a - 0.3 <= ts <= b + 0.3: return oo + (ts - a)
    raise ValueError(ts)

# subtitle chunks: list of [(word, src_time), ...]
RAW = [
 [('अरे', .25), ('भाई', .3), ('साहब!', .5)],
 [('आपका', 1.25), ('बिज़नेस', 1.75), ('है,', 2.0), ('दुकान', 2.25), ('है,', 3.1)],
 [('माल', 3.3), ('है,', 3.7), ('लेकिन', 4.25)],
 [('Instagram', 5.0), ('पे', 5.25), ('नाम', 5.5), ('नहीं', 6.0), ('है!', 6.15)],
 [('अरे', 7.0), ('ऐसा', 7.05), ('कैसे', 7.25), ('चलेगा', 7.5), ('भाई', 7.75), ('फिर?', 8.0)],
 [('तो', 8.5), ('आपके', 8.55), ('बिज़नेस', 8.75), ('को', 9.0), ('शर्मा', 9.25), ('जी', 9.5), ('भी', 9.55)],
 [('जानते', 9.75), ('होंगे?', 10.0)],
 [('एक', 10.25), ('बार', 11.0), ('मैं', 11.25), ('एक', 11.3), ('दुकान', 11.5), ('गया,', 11.75)],
 [('दुकानदार', 12.25), ('बोला,', 12.75), ('साहब,', 13.0)],
 [('हमारा', 13.5), ('बिज़नेस', 13.75), ('बहुत', 14.0), ('मशहूर', 14.5), ('है!', 14.75)],
 [('मैंने', 15.5), ('पूछा,', 15.6)],
 [('Instagram', 16.5), ('पे?', 16.75), ('बोला,', 17.0), ('नहीं!', 18.0)],
 [('Facebook', 19.0), ('पे?', 19.25), ('बोला,', 19.5), ('नहीं!', 20.5)],
 [('अरे', 21.75), ('देव', 21.8), ('शपथ!', 22.0)],
 [('फिर', 23.0), ('मशहूर', 23.05), ('कैसे', 23.5), ('हो?', 23.75)],
 [('देखिए', 24.5), ('भाई', 24.75), ('साहब,', 25.0)],
 [('आजकल', 25.75), ('बिज़नेस', 26.0), ('को', 26.25), ('ऑनलाइन', 26.5), ('करना', 26.75)],
 [('बहुत', 27.0), ('ज़रूरी', 27.25), ('है!', 27.6)],
 [('सोशल', 27.75), ('मीडिया', 28.5), ('पे', 28.75), ('वीडियो', 29.0), ('डालिए,', 29.25)],
 [('प्रोडक्ट', 29.75), ('दिखाइए,', 30.0), ('कस्टमर', 30.5), ('बढ़ाइए!', 30.75)],
 [('तो', 36.0), ('हम', 36.25), ('हैं', 36.3), ('ना', 36.5), ('भाई', 36.75), ('साहब!', 36.8)],
 [('भाई', 44.75), ('साहब,', 44.8), ('दुकान', 45.75), ('आपकी,', 46.0)],
 [('बिज़नेस', 49.25), ('ऑनलाइन', 49.5), ('लाइए,', 50.5)],
 [('बात', 51.0), ('बनेगी!', 52.0)],
]
CHUNKS = [[(w, m(ts)) for w, ts in ch] for ch in RAW]
SPANS = []
for i, ch in enumerate(CHUNKS):
    t0 = ch[0][1] - 0.05
    t1 = CHUNKS[i + 1][0][1] - 0.05 if i + 1 < len(CHUNKS) else AUDIO_END + 0.3
    t1 = min(t1, ch[-1][1] + 1.4)
    SPANS.append((t0, t1))

CF = ImageFont.truetype(FB, 64, layout_engine=ImageFont.Layout.RAQM)
SPACE = 30
def cap_img(ci, active):
    key = ('cap', ci, active)
    if key in _cache: return _cache[key]
    ws = [w for w, _ in CHUNKS[ci]]
    widths = [CF.getlength(w) for w in ws]
    tw = sum(widths) + SPACE * (len(ws) - 1)
    scale = min(1.0, 960 / (tw + 70))
    asc, desc = CF.getmetrics()
    bh, bw, pad = asc + desc + 44, int(tw + 70), 50
    im = Image.new('RGBA', (bw + pad * 2, bh + pad * 2), (0, 0, 0, 0))
    sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 10, pad + bw, pad + bh + 10), 32, fill=210)
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); layer.putalpha(sh)
    im = Image.alpha_composite(im, layer)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + bw, pad + bh), 32, fill=(8, 14, 10, 215), outline=GREEN + (235,), width=4)
    x, y = pad + 35, pad + 20
    for j, (w, wd) in enumerate(zip(ws, widths)):
        if j == active:
            bb = d.textbbox((x, y), w, font=CF)
            d.rounded_rectangle((x - 10, min(bb[1], y + 12) - 8, x + wd + 10, max(bb[3], y + asc) + 8), 14, fill=GOLD + (255,))
            d.text((x, y), w, font=CF, fill=(10, 20, 12))
        else:
            col = (255, 255, 255) if (active is None or j < active) else (200, 212, 205)
            d.text((x + 2, y + 3), w, font=CF, fill=(0, 0, 0, 160)); d.text((x, y), w, font=CF, fill=col)
        x += wd + SPACE
    if scale < 1: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    _cache[key] = im
    return im

def draw_caption(base, t, cy=1650):
    for ci, (t0, t1) in enumerate(SPANS):
        if t0 <= t < t1:
            active = None
            for j, (_, wt) in enumerate(CHUNKS[ci]):
                if wt - 0.03 <= t: active = j
            p = min(1, (t - t0) / 0.15)
            put(base, cap_img(ci, active), W / 2, cy + 18 * (1 - p), scale=0.88 + 0.12 * eo(p))
            return

# ---------- icons ----------
def mark(ok, r=70):
    key = ('mark', ok, r)
    if key in _cache: return _cache[key]
    S = 3; s = r * 2 * S
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = GREEN if ok else RED
    d.ellipse((0, 0, s - 1, s - 1), fill=c + (255,))
    lw = int(s * 0.12)
    if ok: d.line([(s * .27, s * .52), (s * .44, s * .69), (s * .74, s * .33)], fill=(255, 255, 255), width=lw, joint='curve')
    else:
        d.line([(s * .3, s * .3), (s * .7, s * .7)], fill=(255, 255, 255), width=lw)
        d.line([(s * .7, s * .3), (s * .3, s * .7)], fill=(255, 255, 255), width=lw)
    im = im.resize((r * 2, r * 2), Image.LANCZOS)
    out = shadowed(im, radius=r, blur=16, off=10, glow=c, glow_a=0.6)
    _cache[key] = out
    return out

def social_icon(kind, size=300):
    key = ('soc', kind, size)
    if key in _cache: return _cache[key]
    s = size
    if kind == 'ig':
        yy, xx = np.mgrid[0:s, 0:s] / s
        k = np.clip((xx * 0.4 + (1 - yy) * 0.6), 0, 1)[..., None]
        c1, c2, c3 = np.array((254, 218, 117)), np.array((214, 41, 118)), np.array((79, 91, 213))
        arr = np.where(k < .5, c1 * (1 - k * 2) + c2 * (k * 2), c2 * (2 - k * 2) + c3 * (k * 2 - 1))
        im = Image.fromarray(arr.astype(np.uint8)).convert('RGBA'); im.putalpha(rrect_mask(s, s, int(s * 0.28)))
        tx = text_img('ig', int(s * 0.5), WHITE, shadow=False)
    else:
        im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        m_ = Image.new('L', (s * 3, s * 3), 0); ImageDraw.Draw(m_).ellipse((0, 0, s * 3 - 1, s * 3 - 1), fill=255)
        im = Image.new('RGBA', (s, s), (24, 119, 242, 255)); im.putalpha(m_.resize((s, s), Image.LANCZOS))
        tx = text_img('f', int(s * 0.62), WHITE, shadow=False)
    _paste(im, tx, s // 2 - tx.width // 2, s // 2 - tx.height // 2 + int(s * 0.03))
    out = shadowed(im, radius=int(s * 0.3), blur=26, off=18, glow=(214, 41, 118) if kind == 'ig' else (24, 119, 242), glow_a=0.6)
    _cache[key] = out
    return out

def shop_icon(w=520):
    key = ('shop', w)
    if key in _cache: return _cache[key]
    h = int(w * 0.85); S = 2
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    W2, H2 = w * S, h * S
    d.rounded_rectangle((W2 * .08, H2 * .32, W2 * .92, H2 * .98), 24 * S, fill=(30, 46, 38, 255), outline=GREEN + (255,), width=6 * S)
    n = 7; aw = W2 / n
    for i in range(n):
        c = GOLD if i % 2 == 0 else (255, 255, 255)
        d.pieslice((i * aw, H2 * .18, (i + 1) * aw, H2 * .42), 0, 180, fill=c + (255,))
        d.rectangle((i * aw, H2 * .06, (i + 1) * aw, H2 * .30), fill=c + (255,))
    d.rectangle((W2 * .38, H2 * .58, W2 * .62, H2 * .98), fill=(14, 22, 18, 255), outline=GREEN + (255,), width=4 * S)
    d.rectangle((W2 * .14, H2 * .55, W2 * .32, H2 * .75), fill=(120, 200, 150, 120))
    d.rectangle((W2 * .68, H2 * .55, W2 * .86, H2 * .75), fill=(120, 200, 150, 120))
    im = im.resize((w, h), Image.LANCZOS)
    tx = text_img('दुकान', 52, (10, 20, 12), shadow=False)
    out = shadowed(im, radius=24, blur=22, off=16, glow=GOLD, glow_a=0.35)
    _cache[key] = out
    return out

def bubble(txt, size=54, col=WHITE):
    key = ('bub', txt, size)
    if key in _cache: return _cache[key]
    tx = text_img(txt, size, (10, 20, 12), shadow=False)
    w, h = tx.width - 120 + 80, tx.height - 120 + 60
    im = Image.new('RGBA', (w, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=col + (255,))
    d.polygon([(60, h - 2), (110, h - 2), (50, h + 38)], fill=col + (255,))
    _paste(im, tx, 40 - 60, 30 - 60)
    out = shadowed(im, radius=34, blur=18, off=12, glow=GOLD, glow_a=0.35)
    _cache[key] = out
    return out

def big(txt, size, style='g'):
    if style == 'g': return text_img(txt, size, grad=(GREEN, GOLD), glow=GREEN)
    if style == 'gold': return text_img(txt, size, GOLD, glow=(180, 120, 0))
    if style == 'red': return text_img(txt, size, (255, 90, 90), glow=RED)
    return text_img(txt, size, WHITE)

def pop(base, im, x, y, t, ta, dur=0.35, rot=0, wob=True, out_t=None, s0=0.3):
    p = prog(t, ta, dur)
    if p <= 0: return
    a = eo(p)
    sc = s0 + (1 - s0) * eback(p, 2.2)
    if out_t is not None:
        e = prog(t, out_t, 0.2); a *= 1 - e; sc *= 1 + 0.2 * e
    if wob: rot += 2 * math.sin(t * 4 + x * 0.01)
    put(base, im, x, y + 6 * math.sin(t * 3 + y * 0.01), scale=sc, rot=rot, alpha=a)

def shake(t, ta, dur=0.5, amp=22):
    p = prog(t, ta, dur)
    if p <= 0 or p >= 1: return 0, 0
    k = (1 - p) * amp
    return k * math.sin(t * 90), k * math.cos(t * 77)

# ---------- scenes (output time) ----------
def T(src): return m(src)

def scenes(base, t):
    # S0 0 - 1.2
    if t < 1.2:
        pop(base, big('अरे भाई', 120, 'w'), W / 2, 700, t, 0.2, out_t=1.0)
        pop(base, big('साहब!', 200), W / 2, 900, t, 0.45, rot=-4, out_t=1.0)
    # S1 business/dukan/maal + lekin
    elif t < 4.95:
        put(base, big('आपका बिज़नेस', 92, 'w'), W / 2, 420, alpha=eo(prog(t, 1.25, 0.3)) * (1 - prog(t, 4.75, 0.2)))
        items = [('बिज़नेस', 1.75, 640), ('दुकान', 2.25, 820), ('माल', 3.3, 1000)]
        for txt, ta, y in items:
            pop(base, pill(txt, 54, icon=True), W / 2 - 60, y, t, ta, out_t=4.75)
            pop(base, mark(True, 52), W / 2 + 260, y, t, ta + 0.1, out_t=4.75)
        pop(base, big('लेकिन…', 140, 'gold'), W / 2, 1260, t, 4.25, rot=-3, out_t=4.8)
    # S2 instagram pe naam nahi
    elif t < 6.95:
        pop(base, social_icon('ig', 340), W / 2, 820, t, 5.0, dur=0.4)
        pop(base, big('Instagram पे नाम?', 80, 'w'), W / 2, 460, t, 5.1)
        dx, dy = shake(t, 6.0)
        pop(base, mark(False, 120), W / 2 + 140 + dx, 960 + dy, t, 6.0, dur=0.3, s0=2.0)
        pop(base, big('नहीं है!', 150, 'red'), W / 2 + dx, 1280 + dy, t, 6.05, rot=-4)
    # S3 aisa kaise chalega
    elif t < 8.45:
        dx, dy = shake(t, 7.25, 0.6, 16)
        pop(base, big('ऐसा कैसे', 130, 'w'), W / 2 + dx, 680 + dy, t, 7.05)
        pop(base, big('चलेगा?!', 190, 'gold'), W / 2 + dx, 900 + dy, t, 7.5, rot=-5)
        for k in range(3):
            pop(base, big('?', 160 - k * 30, 'g'), [170, 900, 820][k], [520, 520, 1250][k], t, 7.6 + 0.15 * k, rot=[-18, 15, 10][k])
    # S4 sharma ji
    elif t < 10.95:
        pop(base, big('शर्मा जी', 190, 'g'), W / 2, 720, t, 9.25, rot=-3)
        pop(base, big('भी जानते होंगे?', 96, 'w'), W / 2, 960, t, 9.75)
        pop(base, pill('😅  मोहल्ले तक ही सीमित?', 46, bg=(44, 34, 4), fg=GOLD, border=GOLD, path=FB), W / 2, 1200, t, 10.1) if False else \
            pop(base, pill('मोहल्ले तक ही मशहूर?', 48, bg=(44, 34, 4), fg=GOLD, border=GOLD), W / 2, 1200, t, 10.1)
    # S5 shop story
    elif t < 13.45:
        pop(base, shop_icon(560), W / 2, 980, t, 11.4, dur=0.45)
        pop(base, big('एक दुकान पर…', 92, 'w'), W / 2, 470, t, 11.0)
        pop(base, bubble('साहब…'), W / 2 + 180, 640, t, 12.75)
    # S6 mashhoor
    elif t < 15.45:
        put(base, shop_icon(560), W / 2, 1050)
        pop(base, bubble('हमारा बिज़नेस बहुत मशहूर है!', 50), W / 2, 560, t, 13.5)
        for k in range(6):
            a = max(0, math.sin(t * 5 + k)) * eo(prog(t, 14.5, 0.3))
            put(base, glow_sprite(GOLD, 14), 150 + k * 155, 760 + 40 * math.sin(k * 2), scale=0.6 + 0.8 * a, alpha=a)
        pop(base, big('मशहूर!', 160, 'gold'), W / 2, 780, t, 14.5, rot=-5)
    # S7 instagram? nahi
    elif t < 18.95:
        pop(base, big('मैंने पूछा…', 100, 'w'), W / 2, 450, t, 15.5)
        pop(base, social_icon('ig', 320), W / 2, 860, t, 16.5)
        pop(base, big('Instagram पे?', 84, 'g'), W / 2, 1140, t, 16.6)
        dx, dy = shake(t, 18.0)
        pop(base, mark(False, 110), W / 2 + 140 + dx, 980 + dy, t, 18.0, dur=0.3, s0=2.0)
        pop(base, big('नहीं!', 130, 'red'), W / 2 + dx, 1330 + dy, t, 18.05, rot=4)
    # S8 facebook? nahi
    elif t < 21.7:
        pop(base, social_icon('fb', 320), W / 2, 820, t, 19.0)
        pop(base, big('Facebook पे?', 84, 'g'), W / 2, 1100, t, 19.1)
        dx, dy = shake(t, 20.5)
        pop(base, mark(False, 110), W / 2 + 140 + dx, 940 + dy, t, 20.5, dur=0.3, s0=2.0)
        pop(base, big('नहीं!', 130, 'red'), W / 2 + dx, 1310 + dy, t, 20.55, rot=-4)
    # S9 are dev shapat
    elif t < 22.95:
        dx, dy = shake(t, 21.8, 0.9, 30)
        pop(base, big('अरे देव', 150, 'w'), W / 2 + dx, 700 + dy, t, 21.75)
        pop(base, big('शपथ!', 230, 'red'), W / 2 + dx, 950 + dy, t, 22.0, rot=-6)
    # S10 phir mashhoor kaise
    elif t < 24.45:
        pop(base, big('फिर मशहूर', 120, 'w'), W / 2, 560, t, 23.0)
        pop(base, big('कैसे?', 190, 'gold'), W / 2, 780, t, 23.5, rot=4)
        pop(base, big('?', 420, 'g'), W / 2, 1180, t, 23.6, rot=-8 + 6 * math.sin(t * 3))
    # S11 dekhiye bhai sahab -> brand
    elif t < 25.7:
        p = prog(t, 24.5, 0.5)
        l1 = text_img('Shri', 180, WHITE); l2 = text_img('Tech', 180, GREEN, glow=GREEN)
        sc = 0.3 + 0.7 * eback(p, 2); tw = (l1.width - 120 + l2.width - 120) * sc
        put(base, l1, W / 2 - tw / 2 + (l1.width - 120) * sc / 2, 820, scale=sc, alpha=eo(p))
        put(base, l2, W / 2 + tw / 2 - (l2.width - 120) * sc / 2, 820, scale=sc, alpha=eo(p))
        pop(base, big('देखिए भाई साहब…', 80, 'w'), W / 2, 560, t, 24.55)
        pop(base, pill('AI से बिज़नेस को ऑनलाइन लाइए', 44, bg=(44, 34, 4), fg=GOLD, border=GOLD), W / 2, 1040, t, 24.9)
    # S12 online zaroori
    elif t < 27.7:
        pop(base, big('बिज़नेस ऑनलाइन', 100, 'g'), W / 2, 400, t, 25.75)
        pop(base, big('बहुत ज़रूरी!', 80, 'w'), W / 2, 540, t, 27.1)
        p = prog(t, 25.8, 0.6)
        put(base, phone('173cd744', 0.2 * eio(prog(t, 26.2, 1.4))), W / 2, 1150 + 700 * (1 - eback(p, 1.2)) + 14 * math.sin(t * 2),
            scale=0.82, rot=6 * (1 - eo(p)) + 1.5 * math.sin(t * 1.3), alpha=eo(p))
    # S13 social media post
    elif t < 29.7:
        pop(base, big('सोशल मीडिया पर', 96, 'g'), W / 2, 400, t, 27.75)
        pop(base, big('एक क्लिक में पोस्ट', 72, 'w'), W / 2, 530, t, 28.1)
        pop(base, crop_card('3c987a50', (30, 808, 1050, 1625), 820, glow=GOLD), W / 2, 1040, t, 27.9, dur=0.45, rot=-2)
    # S14 product / designs
    elif t < 30.45:
        pop(base, big('प्रोडक्ट दिखाइए', 100, 'g'), W / 2, 420, t, 29.75)
        cards = [crop_card('dfd79390', (78, 885, 370, 1176), 420), crop_card('dfd79390', (711, 885, 1001, 1176), 420, glow=GOLD),
                 crop_card('dfd79390', (394, 885, 686, 1176), 470, glow=GOLD)]
        for i, (c, x, r) in enumerate(zip(cards, [270, 810, 540], [-12, 12, 0])):
            pop(base, c, x, 1000 + (0 if i == 2 else 60), t, 29.8 + 0.08 * i, dur=0.3, rot=r)
        pop(base, pill('AI डिज़ाइन, सेकंडों में', 44, bg=(44, 34, 4), fg=GOLD, border=GOLD), W / 2, 1360, t, 30.0)
    # S15 customers via whatsapp
    elif t < 31.95:
        pop(base, big('कस्टमर बढ़ाइए!', 104, 'g'), W / 2, 400, t, 30.5)
        pop(base, pill('WhatsApp बल्क मार्केटिंग', 46, icon=True), W / 2, 540, t, 30.65)
        pop(base, crop_card('4e9d3978', (69, 268, 1011, 1690), 600), W / 2, 1080, t, 30.6, dur=0.4, rot=2)
        for k in range(4):
            pop(base, big('↑', 110 - k * 10, 'g') if False else mark(True, 34), [140, 940, 160, 930][k], [800, 900, 1250, 1300][k], t, 30.9 + 0.1 * k)
    # S16 to hum hain na
    elif t < T(37.5):
        ta = T(36.0)
        pop(base, big('तो हम हैं ना!', 130, 'g'), W / 2, 640, t, ta + 0.2, rot=-3)
        p = prog(t, ta + 0.4, 0.5)
        l1 = text_img('Shri', 170, WHITE); l2 = text_img('Tech', 170, GREEN, glow=GREEN)
        sc = 0.3 + 0.7 * eback(p, 2); tw = (l1.width - 120 + l2.width - 120) * sc
        put(base, l1, W / 2 - tw / 2 + (l1.width - 120) * sc / 2, 920, scale=sc, alpha=eo(p))
        put(base, l2, W / 2 + tw / 2 - (l2.width - 120) * sc / 2, 920, scale=sc, alpha=eo(p))
        for k in range(3):
            ph = ((t - ta) * 0.9 + k / 3) % 1
            put(base, R2.ring(120 + 330 * ph, (1 - ph) * eo(p), GOLD if k % 2 else GREEN), W / 2, 920)
    # S17 dukan aapki
    elif t < T(46.75):
        ta = T(44.5)
        pop(base, big('दुकान आपकी,', 120, 'w'), W / 2, 600, t, T(45.75))
        pop(base, big('ऑनलाइन पहचान', 110, 'g'), W / 2, 790, t, T(46.0) + 0.1)
        pop(base, pill('ShriTech के साथ', 50, bg=(44, 34, 4), fg=GOLD, border=GOLD), W / 2, 960, t, T(46.0) + 0.3)
        pop(base, shop_icon(420), W / 2, 1270, t, ta + 0.1)
    # S18 business online laiye, baat banegi
    elif t < AUDIO_END:
        pop(base, big('बिज़नेस ऑनलाइन', 110, 'w'), W / 2, 560, t, T(49.25))
        pop(base, big('लाइए!', 150, 'g'), W / 2, 740, t, T(50.5), rot=-3)
        ps = prog(t, T(52.0) - 0.1, 0.4)
        if ps > 0:
            put(base, big('बात बनेगी!', 190, 'gold'), W / 2, 1100, scale=2.4 - 1.4 * eback(ps, 2.5), rot=-6, alpha=eo(ps))
        for k in range(8):
            a = max(0, math.sin(t * 6 + k * 1.7)) * eo(prog(t, T(52.0), 0.3))
            put(base, glow_sprite(GOLD if k % 2 else GREEN, 12), 120 + k * 120, 1000 + 260 * (k % 2), scale=0.6 + 0.8 * a, alpha=a)
    else:
        R2.s_cta(base, t, AUDIO_END, DUR)

BOUNDS = [1.2, 4.95, 6.95, 8.45, 10.95, 13.45, 15.45, 18.95, 21.7, 22.95, 24.45, 25.7, 27.7, 29.7, 30.45, 31.95,
          None, None, None]

def topbar(base, t):
    a = eo(prog(t, 0.3, 0.5)) * (1 - eo(prog(t, AUDIO_END, 0.4)))
    if a <= 0: return
    logo1 = text_img('Shri', 46, WHITE); logo2 = text_img('Tech', 46, GREEN, glow=GREEN)
    put(base, logo1, 70 + logo1.width / 2 - 60, 150, alpha=a)
    put(base, logo2, 70 + logo1.width - 120 - 60 + logo2.width / 2 + 4, 150, alpha=a)
    p = pill('☎ 9993615146', 34, bg=(40, 32, 6), fg=GOLD, border=GOLD, path=FSYM)
    put(base, p, W - 70 - p.width / 2 + 60, 150, scale=1 + 0.04 * math.sin(t * 6), alpha=a)

CUTS = [1.2, 4.95, 6.95, 8.45, 10.95, 13.45, 15.45, 18.95, 21.7, 22.95, 24.45, 25.7, 27.7, 29.7, 30.45, 31.95,
        T(37.5), T(46.75), AUDIO_END]

def frame(t):
    flash = max([max(0, 1 - abs(t - b) / 0.12) for b in CUTS] + [0])
    base = background(t * 1.6, accent=flash * 0.6)
    scenes(base, t)
    topbar(base, t)
    draw_caption(base, t)
    for b in [24.5, AUDIO_END]: sweep(base, (t - (b - 0.3)) / 0.6)
    out = base.convert('RGB')
    if t < 0.15: out = Image.blend(Image.new('RGB', (W, H)), out, t / 0.15)
    return out

def render(a, b, path):
    tmp = path + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-crf', '19', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(round(a * FPS)), int(round(min(b, DUR) * FPS))):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, path)

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            frame(float(ts)).save(f'/home/claude/meme/st_{ts}.jpg', quality=85)
    elif sys.argv[1] == 'info':
        print('audio end', AUDIO_END, 'dur', DUR)
        for ch, sp in zip(CHUNKS, SPANS): print(round(sp[0], 2), round(sp[1], 2), ' '.join(w for w, _ in ch))
    else:
        render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
