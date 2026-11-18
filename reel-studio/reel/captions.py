import json, re, sys, os
LANG = os.environ.get('REEL_LANG', 'hi')
VO = '/home/claude/reel/vo' + {'en': '_en', 'hi2': '_hi2'}.get(LANG, '')
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/claude/reel')
if LANG == 'en':
    from script_en import SEG
elif LANG == 'hi2':
    from script_hi2 import SEG
else:
    from script import SEG

FB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
SPOKEN_LEN = {'ShriTech': 6, 'AI': 3, 'Facebook': 7, 'Instagram': 9, 'WhatsApp': 7, 'Excel': 5, '1': 2,
              '99936': 16, '15146': 16}
if LANG == 'hi2': SPOKEN_LEN = {'ShriTech': 6, 'AI': 3, '4': 3, '10': 2, 'Growth': 5, 'Pro': 4, 'Meta': 4, 'WhatsApp': 7, '400': 5, '1000': 7, '₹1799': 20, '₹3999': 18, '₹399': 17, '₹999': 16, '₹086': 10, '99936': 16, '15146': 16}
if LANG == 'en': SPOKEN_LEN = {'ShriTech': 8, '1': 3, '99936': 30, '15146': 30, "customers'": 9}

def wlen(w):
    core = re.sub(r'[,।!?:.]', '', w)
    return SPOKEN_LEN.get(core, max(2, len(core)))

def build():
    info = json.load(open(VO + '/info.json'))
    words = []  # (word, t0, t1, seg)
    for seg, inf in zip(SEG, info):
        a, b, _, sub = seg
        start = a + max(0.0, (b - a - inf['dur']) * 0.3)
        inf['place'] = start
        x, sr = sf.read(f"{VO}/s{inf['i']}.wav")
        # voiced regions (frames of 20ms)
        hop = int(sr * 0.02)
        e = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
        voiced = e > 0.015
        # fill gaps shorter than 100 ms
        vi = voiced.copy()
        gap = 0
        for k in range(len(vi)):
            if not voiced[k]: gap += 1
            else:
                if 0 < gap <= 5: vi[k - gap:k] = True
                gap = 0
        times = np.where(vi)[0] * 0.02  # voiced timeline
        ws = sub.split()
        L = np.array([wlen(w) for w in ws], float)
        cum = np.concatenate([[0], np.cumsum(L)]) / L.sum()
        n = len(times)
        for j, w in enumerate(ws):
            i0 = min(n - 1, int(cum[j] * n)); i1 = min(n - 1, max(i0, int(cum[j + 1] * n) - 1))
            words.append((w, start + times[i0], start + times[i1] + 0.02, inf['i']))
    return words, info

WORDS, INFO = build()
FONT = ImageFont.truetype(FB, 60, layout_engine=ImageFont.Layout.RAQM)
MAXW = 900
SPACE = 30

def wwidth(w): return FONT.getlength(w)

# chunk into caption lines: phrases at punctuation, balanced splits, merge tiny ones
def width_of(ks): return sum(wwidth(WORDS[k][0]) for k in ks) + SPACE * (len(ks) - 1)
CHUNKS = []
segs = {}
for k, wd in enumerate(WORDS): segs.setdefault(wd[3], []).append(k)
for sg in sorted(segs):
    phrases, cur = [], []
    for k in segs[sg]:
        cur.append(k)
        if re.search(r'[,।!?:.]$', WORDS[k][0]): phrases.append(cur); cur = []
    if cur: phrases.append(cur)
    out = []
    def split(p):
        if width_of(p) <= MAXW and len(p) <= 6: out.append(p); return
        n = len(p); best = min(range(1, n), key=lambda m: abs(width_of(p[:m]) - width_of(p[m:])))
        split(p[:best]); split(p[best:])
    for p in phrases: split(p)
    merged = []
    for p in out:
        if merged and (len(p) <= 2 or len(merged[-1]) <= 1) and width_of(merged[-1] + p) <= MAXW and len(merged[-1] + p) <= 6:
            merged[-1] = merged[-1] + p
        else: merged.append(p)
    CHUNKS += merged
SPANS = []
for ci, ch in enumerate(CHUNKS):
    t0 = WORDS[ch[0]][1] - 0.08
    t1 = WORDS[ch[-1]][2] + 0.45
    if ci + 1 < len(CHUNKS): t1 = min(t1, WORDS[CHUNKS[ci + 1][0]][1] - 0.08)
    SPANS.append((t0, t1))

_cache = {}
def caption_img(ci, active):
    key = (ci, active)
    if key in _cache: return _cache[key]
    ch = CHUNKS[ci]
    ws = [WORDS[k][0] for k in ch]
    widths = [wwidth(w) for w in ws]
    tw = sum(widths) + SPACE * (len(ws) - 1)
    asc, desc = FONT.getmetrics()
    bh = asc + desc + 40
    bw = int(tw + 70)
    pad = 50
    im = Image.new('RGBA', (bw + pad * 2, bh + pad * 2), (0, 0, 0, 0))
    # shadow + box
    sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 10, pad + bw, pad + bh + 10), 30, fill=200)
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); layer.putalpha(sh)
    im = Image.alpha_composite(im, layer)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + bw, pad + bh), 30, fill=(8, 14, 10, 205), outline=(34, 197, 94, 230), width=3)
    x = pad + 35
    y = pad + 18
    for j, (w, wd) in enumerate(zip(ws, widths)):
        k = ch[j]
        if k == active:
            bb = d.textbbox((x, y), w, font=FONT); d.rounded_rectangle((x - 10, min(bb[1], y + 12) - 8, x + wd + 10, max(bb[3], y + asc) + 8), 14, fill=(250, 204, 21, 255))
            d.text((x, y), w, font=FONT, fill=(10, 20, 12))
        else:
            col = (255, 255, 255) if (active is None or k < active) else (205, 215, 208)
            d.text((x + 2, y + 3), w, font=FONT, fill=(0, 0, 0, 160))
            d.text((x, y), w, font=FONT, fill=col)
        x += wd + SPACE
    _cache[key] = im
    return im

def draw_caption(base, t, cy=1630):
    for ci, (t0, t1) in enumerate(SPANS):
        if t0 <= t < t1:
            active = None
            for k in CHUNKS[ci]:
                if WORDS[k][1] - 0.04 <= t: active = k
            im = caption_img(ci, active)
            p = min(1, (t - t0) / 0.18)
            sc = 0.88 + 0.12 * (1 - (1 - p) ** 3)
            if sc < 0.999:
                im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
            x = int(540 - im.width / 2); y = int(cy - im.height / 2 + 20 * (1 - p))
            base.alpha_composite(im, (x, y))
            return

if __name__ == '__main__':
    for ci, ch in enumerate(CHUNKS):
        print(round(SPANS[ci][0], 2), round(SPANS[ci][1], 2), ' '.join(WORDS[k][0] for k in ch))
