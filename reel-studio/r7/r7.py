"""Reel 7: 'Digital Power' — owner-supplied speech audio, Shri Tech visuals, light + dark scenes, Hindi/English subtitles."""
import sys, math, random
sys.path.insert(0, '/home/claude/r7')      # r7 words.py wins
sys.path.insert(1, '/home/claude/salon')
sys.path.insert(2, '/home/claude/clinic')
import numpy as np
import salon as L
from salon import *
from clinic import icon_badge
from PIL import Image, ImageDraw, ImageFilter

GOLD = (202, 138, 4)
END = 89.0
SC = [0.0, 12.1, 25.1, 39.2, 46.4, 58.2, 65.7, 76.3, 85.2, END]
UP = '/mnt/user-data/uploads/'
MS = '/home/claude/manual/screens/'

# ---------------- pieces ----------------
def phone_img(src, w=340, dark=False, top=0.0, frac=None):
    """Phone mockup with a real Shri Tech screenshot. dark=True -> deep-green frame for dark scenes."""
    key = ('ph7', src, w, dark, top)
    def mk():
        h = int(w * 2.05)
        sc = Image.open(src).convert('RGB')
        iw = w - 30
        s2 = sc.resize((iw, int(sc.height * iw / sc.width)), Image.LANCZOS)
        ih = h - 50
        y0 = int(top * s2.height)
        s2 = s2.crop((0, y0, iw, y0 + ih))
        p = Pad(w, h)
        fr = (12, 40, 24) if dark else WHITE
        p.rect((0, 0, w - 1, h - 1), 50, fill=fr + (255,), outline=((60, 160, 100) if dark else MINT2) + (255,), width=4)
        im = p.img()
        m = Image.new('L', (iw, ih), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, iw - 1, ih - 1), 36, fill=255)
        im.paste(s2, (15, 25), m)
        q = Pad(w, h); q.rect((w / 2 - 44, 32, w / 2 + 44, 48), 8, fill=(0, 0, 0, 255))
        im.alpha_composite(q.img())
        # glossy sheen
        sh = Image.new('L', im.size, 0)
        ImageDraw.Draw(sh).polygon([(0, 0), (w * 0.62, 0), (0, h * 0.42)], fill=46)
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        sh = Image.fromarray(np.minimum(np.array(sh), np.array(im.getchannel('A'))))
        im.alpha_composite(Image.merge('RGBA', [Image.new('L', im.size, 255)] * 3 + [sh]))
        return with_shadow(im, blur=32, off=22, alpha=0.32 if not dark else 0.5, color=(0, 0, 0) if dark else DEEP)
    return cached(key, mk)
def lphone(name, w=340, top=0.0): return phone_img(MS + name + '.jpg', w, False, top)
def dphone(name, w=340, top=0.0): return phone_img(UP + name + '-image.jpg', w, True, top)

def gtext(txt, size, c1=(254, 240, 138), c2=(217, 150, 6), path=PB, shadow=(0, 0, 0), sa=0.35):
    key = ('gt', txt, size, c1, c2, shadow)
    def mk():
        f = font(path, size); bb = f.getbbox(txt)
        w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((30 - bb[0], 30 - bb[1]), txt, font=f, fill=255)
        t = np.linspace(0, 1, h)[:, None, None]
        col = np.array(c1) * (1 - t) + np.array(c2) * t
        band = np.exp(-((t - 0.3) / 0.13) ** 2) * 0.45
        col = col + (255 - col) * band
        arr = np.broadcast_to(col, (h, w, 3)).astype(np.uint8)
        im = Image.fromarray(np.dstack([arr, np.array(m)]), 'RGBA')
        out = Image.new('RGBA', (w, h + 10), (0, 0, 0, 0))
        sh = m.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * sa))
        out.paste(Image.new('RGBA', (w, h), shadow + (255,)), (0, 8), sh)
        out.alpha_composite(im, (0, 0))
        return out
    return cached(key, mk)

def gbox(w, h, c1, c2, r=34, border=None):
    """glossy gradient rounded box"""
    key = ('gbox', w, h, c1, c2, r, border)
    def mk():
        t = np.linspace(0, 1, h)[:, None, None]
        col = np.array(c1) * (1 - t) + np.array(c2) * t
        band = np.exp(-((t - 0.18) / 0.12) ** 2) * 0.35
        col = col + (255 - col) * band
        arr = np.broadcast_to(col, (h, w, 3)).astype(np.uint8)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
        im = Image.fromarray(np.dstack([arr, np.array(m)]), 'RGBA')
        if border: ImageDraw.Draw(im).rounded_rectangle((1, 1, w - 2, h - 2), r, outline=border + (255,), width=3)
        return im
    return cached(key, mk)

def node(txt, sub=None, w=300, h=110, kind='g', size=38):
    key = ('node7', txt, sub, w, h, kind, size)
    def mk():
        cs = {'g': ((74, 222, 128), (21, 128, 61), WHITE), 'y': ((254, 240, 138), (234, 170, 8), DEEP),
              'w': ((255, 255, 255), (230, 248, 236), DEEP), 'd': ((40, 140, 75), (6, 46, 25), WHITE)}[kind]
        im = gbox(w, h, cs[0], cs[1], h // 2, border=(255, 255, 255) if kind in 'gd' else (187, 247, 208)).copy()
        d = ImageDraw.Draw(im)
        if sub:
            d.text((w / 2, h * 0.38), txt, font=font(PB, size), fill=cs[2], anchor='mm')
            d.text((w / 2, h * 0.74), sub, font=font(FB, int(size * 0.55)), fill=cs[2], anchor='mm')
        else:
            d.text((w / 2, h / 2), txt, font=font(PB, size), fill=cs[2], anchor='mm')
        return with_shadow(im, blur=16, off=10, alpha=0.3)
    return cached(key, mk)

def numdot(n, r=34, kind='y'):
    def mk():
        im = gbox(r * 2, r * 2, (254, 240, 138) if kind == 'y' else (74, 222, 128), (217, 150, 6) if kind == 'y' else (21, 128, 61), r).copy()
        ImageDraw.Draw(im).text((r, r + 1), str(n), font=font(PB, int(r * 1.1)), fill=DEEP if kind == 'y' else WHITE, anchor='mm')
        return with_shadow(im, blur=8, off=5, alpha=0.3)
    return cached(('nd', n, r, kind), mk)

def arrow(base, x0, y0, x1, y1, k, col=YEL, w=8):
    if k <= 0: return
    xe, ye = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    d = ImageDraw.Draw(base)
    d.line([(x0, y0), (xe, ye)], fill=col, width=w)
    if k > 0.95:
        a = math.atan2(y1 - y0, x1 - x0)
        p = [(xe, ye), (xe - 26 * math.cos(a - 0.5), ye - 26 * math.sin(a - 0.5)), (xe - 26 * math.cos(a + 0.5), ye - 26 * math.sin(a + 0.5))]
        d.polygon(p, fill=col)

def rays(base, cx, cy, t, r0=120, r1=520, n=24, col=(254, 240, 138), alpha=70):
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(n):
        a = i * 2 * math.pi / n + t * 0.2; da = math.pi / n * 0.45
        d.polygon([(cx + r0 * math.cos(a - da), cy + r0 * math.sin(a - da)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                   (cx + r0 * math.cos(a + da), cy + r0 * math.sin(a + da))], fill=col + (alpha,))
    base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))

def stat_card(icon, num, label, k):
    key = ('stat', icon, num, label)
    def mk():
        w, h = 860, 250
        im = gbox(w, h, (30, 110, 62), (8, 46, 26), 40, border=(74, 222, 128)).copy()
        d = ImageDraw.Draw(im)
        ic = gbox(150, 150, (254, 240, 138), (217, 150, 6), 40)
        im.alpha_composite(ic, (40, 50))
        if icon == 'play':
            d.polygon([(100, 92), (100, 158), (156, 125)], fill=DEEP)
        else:
            d.rounded_rectangle((78, 88, 152, 162), 20, outline=DEEP, width=9)
            d.ellipse((99, 109, 131, 141), outline=DEEP, width=9); d.ellipse((134, 96, 144, 106), fill=DEEP)
        d.text((230, 110), num, font=font(PB, 96), fill=(254, 240, 138), anchor='lm')
        d.text((232, 196), label, font=font(PB, 40), fill=WHITE, anchor='lm')
        return with_shadow(im, blur=24, off=14, alpha=0.45, color=(0, 0, 0))
    return cached(key, mk)

def bars_card(k):
    key = ('bars', round(k, 2))
    def mk():
        w, h = 820, 480
        im = gbox(w, h, (255, 255, 255), (236, 252, 243), 36, border=(187, 247, 208)).copy()
        d = ImageDraw.Draw(im)
        d.text((40, 52), 'Mobile Data Users', font=font(PB, 34), fill=DEEP, anchor='lm')
        d.text((w - 40, 52), 'भारत', font=font(PB, 30), fill=GREEN2, anchor='rm')
        vals = [0.12, 0.2, 0.33, 0.48, 0.66, 0.84, 1.0]
        bw = 70; gap = (w - 80 - bw * 7) / 6
        for i, v in enumerate(vals):
            kk = eio(clamp(k * 1.6 - i * 0.09))
            bh = 300 * v * kk
            x = 40 + i * (bw + gap)
            if bh > 2:
                bar = gbox(bw, int(bh) + 1, (110, 231, 160) if i < 6 else (254, 240, 138), (21, 128, 61) if i < 6 else (217, 150, 6), 14)
                im.alpha_composite(bar, (int(x), int(h - 50 - bh)))
            d.text((x + bw / 2, h - 26), str(2014 + i * 2) if i < 6 else 'आज', font=font(FB, 20), fill=DEEP, anchor='mm')
        return with_shadow(im, blur=24, off=14, alpha=0.22)
    return cached(key, mk)

def logo_dark(size=90):
    return cached(('logod', size), lambda: line_img([('Shri', size, WHITE, PB), ('Tech', size, (74, 222, 128), PB)], gap=6))

def hub_center():
    def mk():
        r = 150
        im = gbox(r * 2, r * 2, (255, 255, 255), (220, 252, 231), r, border=(254, 240, 138)).copy()
        lg = logo(56)
        im.alpha_composite(lg, (int(r - lg.width / 2), int(r - lg.height / 2) - 16))
        ImageDraw.Draw(im).text((r, r + 58), 'एक प्लेटफ़ॉर्म', font=font(PB, 26), fill=GREEN2, anchor='mm')
        return with_shadow(im, blur=30, off=12, alpha=0.4, color=(0, 0, 0))
    return cached('hubc', mk)

# ---------------- scenes ----------------
def k1(t):
    b = bg_green(t)
    rays(b, W / 2, 330, t, 60, 700, 28, alpha=26)
    headline(b, t, 0, [(0.05, [bold('Social Media', 96, WHITE)]), (1.1, [bold('के इस दौर में', 84, YEL)])], y0=300)
    if t > 2.4: put(b, pill('भारत में', 40, bg=YEL, fg=DEEP, path=PB, padx=34, pady=14, dot=GREEN2), W / 2, 590, scale=eback(prog(t, 2.4, 0.4)))
    if t > 3.3:
        n = int(500 * eio(prog(t, 3.3, 2.0)))
        lab = 'YouTube Users' if t > 6.1 else 'Users…'
        put(b, stat_card('play', f'{n} Million+', lab, 1), W / 2, 830, scale=eback(prog(t, 3.3, 0.45)))
    if t > 7.8:
        n = int(500 * eio(prog(t, 7.8, 2.0)))
        lab = 'Instagram Users' if t > 10.4 else 'Users…'
        put(b, stat_card('cam', f'{n} Million+', lab, 1), W / 2, 1110, scale=eback(prog(t, 7.8, 0.45)))
    return b, True

def k2(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 12.1, [(12.15, [bold('हमारे यहां', 86)]), (13.1, [bold('अलग-अलग मुद्दों पर', 80, GREEN2)])], y0=290)
    q = eback(prog(t, 12.2, 0.5))
    put(b, lphone('p20-chat-clean', 330, 0.0), W / 2, 1010 + (1 - q) * 160, alpha=min(1, q * 2), rot=math.sin(t) * 1.5)
    chips = [('खुलकर बहस', 15.4, 230, 690, WHITE), ('अलग नज़रिया', 17.1, 860, 760, YEL), ('दृष्टिकोण', 18.0, 210, 920, YEL),
             ('जनता की चर्चा', 19.3, 870, 1000, WHITE), ('Likes', 20.0, 200, 1140, GREEN), ('Shares', 20.4, 880, 1220, GREEN)]
    for i, (tx, t0, x, y, c) in enumerate(chips):
        if t > t0:
            put(b, bubble(tx, 32) if c == WHITE else pill(tx, 32, bg=c, fg=WHITE if c == GREEN else DEEP, path=PB, padx=28, pady=14),
                x, y + math.sin(t * 2 + i) * 8, scale=eback(prog(t, t0, 0.4)))
    if t > 21.2:
        put(b, gbox(820, 110, (52, 211, 110), (21, 128, 61), 55), W / 2, 1330, scale=eback(prog(t, 21.2, 0.4)))
        put(b, text_img('इसमें सबसे बड़ी भूमिका किसकी?', 40, WHITE, PB), W / 2, 1330, alpha=prog(t, 21.4, 0.3))
    return b, False

def k3(t):
    b = bg_green(t)
    if t < 27.2:
        rays(b, W / 2, 800, t, 140, 900, 32, alpha=40)
        p = eback(prog(t, 25.6, 0.5), 2.2)
        put(b, text_img('वह है', 64, WHITE, PB), W / 2, 560, alpha=prog(t, 25.15, 0.3))
        put(b, gtext('Digital', 190), W / 2, 790, scale=p)
        put(b, gtext('Power', 220, (255, 255, 255), (134, 239, 172)), W / 2, 1020, scale=eback(prog(t, 26.1, 0.5), 2.2))
        return b, True
    put(b, gtext('Digital Power', 76), W / 2, 270, alpha=prog(t, 27.2, 0.3))
    put(b, pill('12-13 साल पहले', 40, bg=YEL, fg=DEEP, path=PB, padx=34, pady=14), W / 2, 400, scale=eback(prog(t, 27.3, 0.4)))
    if t > 28.9: put(b, node('Mobile', 'मोबाइल', 340, 130, 'w', 44), 300, 600, scale=eback(prog(t, 28.9, 0.4)))
    if t > 30.1:
        put(b, text_img('+', 90, YEL, PB), W / 2, 600, scale=eback(prog(t, 30.1, 0.3)))
        put(b, node('Internet', 'इंटरनेट', 340, 130, 'w', 44), 780, 600, scale=eback(prog(t, 30.3, 0.4)))
    arrow(b, W / 2, 690, W / 2, 790, eo(prog(t, 31.2, 0.5)))
    if t > 32.2: put(b, node('= शक्ति', 'अपने आप में एक ताकत', 560, 140, 'y', 52), W / 2, 870, scale=eback(prog(t, 32.4, 0.45)))
    if t > 34.9:
        arrow(b, W / 2 - 120, 950, 300, 1050, eo(prog(t, 34.9, 0.5)))
        put(b, node('Access', 'जिसके पास था', 380, 130, 'g', 46), 300, 1120, scale=eback(prog(t, 36.0, 0.4)))
    if t > 37.1:
        arrow(b, 500, 1120, 580, 1120, eo(prog(t, 37.1, 0.4)))
        put(b, node('Opportunities', 'उसी के पास मौके', 420, 130, 'y', 42), 790, 1120, scale=eback(prog(t, 37.6, 0.4)))
    return b, True

def k4(t):
    b = bg_light(t, tint=(255, 253, 240))
    headline(b, t, 39.2, [(39.25, [bold('2014', 112, GREEN2), bold('के बाद', 92)]), (41.3, [bold('भारत ने Mobile Data को', 64)])], y0=290)
    k = prog(t, 39.6, 4.0)
    put(b, bars_card(round(eio(k), 2)), W / 2, 1000, scale=eback(prog(t, 39.4, 0.45)))
    if t > 43.9:
        put(b, badge('✓', 'AFFORDABLE', 120, bg=YEL, fg=DEEP), 860, 720, scale=eback(prog(t, 43.9, 0.45), 2.4), rot=-10)
    if t > 45.5:
        put(b, pill('अब हर हाथ में Internet', 40, bg=DEEP, fg=YEL, path=PB, padx=34, pady=14), W / 2, 1320, scale=eback(prog(t, 45.5, 0.4)))
    return b, False

STEPS5 = [('बताइए', 'बिज़नेस डिटेल'), ('पोस्ट तैयार', 'पोस्टर + कैप्शन'), ('पोस्ट करें', 'FB + IG + WhatsApp')]
def k5(t):
    b = bg_light(t, tint=MINT)
    if t < 52.5:
        headline(b, t, 46.4, [(46.45, [bold('आज छोटे शहर का', 80)]), (48.5, [bold('विद्यार्थी भी', 86, GREEN2)])], y0=290)
        q = eback(prog(t, 46.6, 0.5))
        put(b, portrait_card('विद्यार्थी', 'happy', 380, 470), 300, 980 + (1 - q) * 120, alpha=min(1, q * 2))
        put(b, lphone('p04-front-clean', 300, 0.04), 780, 1000, rot=4, alpha=prog(t, 47.0, 0.5))
        if t > 49.8:
            put(b, pill('Digital Learning', 42, bg=GREEN, fg=WHITE, path=PB, padx=36, pady=16, dot=YEL), W / 2, 1330, scale=eback(prog(t, 49.8, 0.4)))
        return b, False
    headline(b, t, 52.5, [(52.55, [bold('गांव का दुकानदार भी', 76)]), (55.8, [bold('नए Customers तक', 80, GREEN2)])], y0=280)
    put(b, gbox(700, 74, (22, 110, 56), (6, 46, 25), 37), W / 2, 560, alpha=prog(t, 52.7, 0.3))
    put(b, line_img([('Shri', 36, WHITE, PB), ('Tech', 36, (74, 222, 128), PB), ('के साथ सिर्फ', 34, WHITE, PB), ('3 स्टेप', 36, YEL, PB)], gap=12), W / 2, 560, alpha=prog(t, 52.8, 0.3))
    xs = [190, 540, 890]; y = 760
    for i, (a, s) in enumerate(STEPS5):
        t0 = 53.1 + i * 0.9
        if t > t0:
            put(b, node(a, s, 300, 130, ['y', 'g', 'w'][i], 38), xs[i], y, scale=eback(prog(t, t0, 0.4)))
            put(b, numdot(i + 1), xs[i] - 130, y - 62, scale=eback(prog(t, t0 + 0.1, 0.35)))
        if i < 2: arrow(b, xs[i] + 150, y, xs[i + 1] - 150, y, eo(prog(t, t0 + 0.4, 0.4)), col=GREEN2, w=7)
    q = eback(prog(t, 53.4, 0.5))
    put(b, portrait_card('दुकानदार', 'happy', 300, 370), 290, 1110 + (1 - q) * 100, alpha=min(1, q * 2))
    put(b, lphone('p11-review-clean', 250, 0.06), 800, 1110, rot=-4, alpha=prog(t, 54.0, 0.5))
    if t > 55.8:
        put(b, pill('नए Customers', 34, bg=YEL, fg=DEEP, path=PB, dot=GREEN2), 540, 1000, scale=eback(prog(t, 55.8, 0.4)))
    return b, False

STEPS6 = [('Excel से कॉन्टैक्ट', 'एक साथ अपलोड'), ('मैसेज टेम्पलेट', 'Meta से मंज़ूर'), ('एक क्लिक में भेजें', 'सबको या ग्रुप को'), ('रिपोर्ट + चैट', 'किसने पढ़ा, सब दिखे')]
def k6(t):
    b = bg_green(t)
    if t < 62.9:
        headline(b, t, 58.2, [(58.25, [bold('एक युवा भी', 84, WHITE)]), (59.5, [bold('Online आगे बढ़ सकता है', 64, YEL)])], y0=280)
    else:
        rays(b, W / 2, 420, t, 80, 600, 28, alpha=34)
        put(b, gtext('Power to', 110, (255, 255, 255), (187, 247, 208)), W / 2, 340, scale=eback(prog(t, 62.9, 0.4)))
        put(b, gtext('Empower', 150), W / 2, 500, scale=eback(prog(t, 64.2, 0.45), 2.3))
    q = eback(prog(t, 58.4, 0.5))
    put(b, dphone('4e9d3978', 330, 0.0), 260, 1020 + (1 - q) * 140, alpha=min(1, q * 2), rot=-3)
    put(b, line_img([('Shri', 34, WHITE, PB), ('Tech', 34, (74, 222, 128), PB), ('WhatsApp', 34, YEL, PB)], gap=10), 740, 700, alpha=prog(t, 58.6, 0.3))
    for i, (a, s) in enumerate(STEPS6):
        t0 = 58.9 + i * 0.9; y = 800 + i * 150
        if i < 3: arrow(b, 560, y + 50, 560, y + 100, eo(prog(t, t0 + 0.4, 0.3)), col=YEL, w=6)
        if t > t0:
            put(b, numdot(i + 1, 30), 560, y, scale=eback(prog(t, t0, 0.35)))
            put(b, node(a, s, 400, 112, 'w' if i % 2 == 0 else 'y', 32), 800, y, scale=eback(prog(t, t0 + 0.08, 0.4)))
    return b, True

def k7(t):
    b = bg_light(t)
    headline(b, t, 65.7, [(66.8, [bold('Street Vendor', 82)]), (68.3, [bold('और', 70), bold('Car Showroom', 82, GREEN2)])], y0=280)
    q1 = eback(prog(t, 66.8, 0.5)); q2 = eback(prog(t, 69.1, 0.5))
    put(b, portrait_card('ठेले वाला', 'happy', 330, 410, bg1=PALEY, bg2=YEL), 280, 840 + (1 - q1) * 100, alpha=min(1, q1 * 2))
    if t > 69.0: put(b, portrait_card('Car Showroom', 'calm', 330, 410), 800, 840 + (1 - q2) * 100, alpha=min(1, q2 * 2))
    if t > 72.3:
        put(b, pill('छोटा scale', 30, bg=WHITE, fg=DEEP, path=PB), 280, 1080, scale=eback(prog(t, 72.3, 0.35)))
        put(b, pill('बड़ा scale', 30, bg=DEEP, fg=YEL, path=PB), 800, 1080, scale=eback(prog(t, 72.6, 0.35)))
    if t > 73.9:
        k = eo(prog(t, 73.9, 0.6))
        arrow(b, 280, 1120, 470, 1230, k, col=GREEN2, w=7); arrow(b, 800, 1120, 610, 1230, k, col=GREEN2, w=7)
        put(b, gbox(560, 110, (255, 255, 255), (220, 252, 231), 55, border=(254, 240, 138)), W / 2, 1290, scale=eback(prog(t, 74.2, 0.4)))
        put(b, logo(58), W / 2, 1290, scale=eback(prog(t, 74.3, 0.4)))
        if t > 75.0: put(b, pill('दोनों के लिए एक प्लेटफ़ॉर्म', 30, bg=YEL, fg=DEEP, path=PB), W / 2, 1375, scale=eback(prog(t, 75.0, 0.35)))
    return b, False

HUB = [('AI पोस्टर', 'g'), ('FB + Instagram', 'w'), ('WhatsApp', 'g'), ('लाइव चैट', 'w'), ('रिपोर्ट', 'g'), ('Payments', 'y')]
def k8(t):
    b = bg_green(t)
    headline(b, t, 76.3, [(76.35, [bold('Digital Payments', 84, WHITE)]), (78.8, [bold('एक ही', 70, WHITE), bold('Ecosystem', 84, YEL)])], y0=270)
    cx, cy, R = W / 2, 930, 330
    rays(b, cx, cy, t, 160, 520, 24, alpha=30)
    for i, (txt, kind) in enumerate(HUB):
        a = -math.pi / 2 + i * math.pi / 3
        x, y = cx + R * math.cos(a), cy + R * 0.82 * math.sin(a)
        t0 = 77.0 + i * 0.55
        arrow(b, cx + 150 * math.cos(a), cy + 150 * 0.82 * math.sin(a), x - 100 * math.cos(a), y - 50 * math.sin(a), eo(prog(t, t0, 0.4)), col=YEL, w=5)
        if t > t0: put(b, node(txt, None, 270, 90, kind, 30), x, y, scale=eback(prog(t, t0 + 0.2, 0.4)))
    put(b, hub_center(), cx, cy, scale=eback(prog(t, 76.6, 0.5)) * (1 + 0.03 * math.sin(t * 4)))
    if t > 82.2:
        put(b, gbox(760, 116, (254, 240, 138), (217, 150, 6), 58), W / 2, 1335, scale=eback(prog(t, 82.2, 0.4)))
        put(b, text_img('छोटा हो या बड़ा — सबके लिए', 46, DEEP, PB), W / 2, 1335, alpha=prog(t, 82.4, 0.3))
    return b, True

def k9(t):
    b = bg_light(t, glow=GREEN, glow2=YEL)
    q = eback(prog(t, 85.25, 0.5))
    put(b, logo(140), W / 2, 330, scale=0.7 + 0.3 * q, alpha=min(1, q * 2))
    put(b, text_img('अपने बिज़नेस को', 64, DEEP, PB), W / 2, 480, alpha=prog(t, 85.4, 0.3))
    put(b, gtext('Digital बनाइए', 110, (52, 211, 110), (6, 52, 28), shadow=GOLD, sa=0.3), W / 2, 610, scale=eback(prog(t, 85.6, 0.45)))
    put(b, lphone('p16-wa-clean', 260, 0.08), 330, 1000, rot=-7, alpha=prog(t, 85.7, 0.4))
    put(b, lphone('p07-dash-clean', 260, 0.06), 750, 1000, rot=7, alpha=prog(t, 85.9, 0.4))
    put(b, pill('Contact us — आज ही कॉल करें', 38, bg=DEEP, fg=YEL, path=PB, padx=34, pady=16), W / 2, 1300, scale=eback(prog(t, 86.2, 0.4)))
    return b, False

def thumbnail():
    def mk():
        b = bg_light(0.6, tint=MINT)
        rays(b, W / 2, 760, 0.6, 120, 900, 30, col=(254, 236, 140), alpha=60)
        put(b, pill('हर बिज़नेस के लिए', 44, bg=DEEP, fg=YEL, path=PB, padx=38, pady=16), W / 2, 280)
        put(b, gtext('Digital', 200, (52, 211, 110), (6, 52, 28), shadow=GOLD, sa=0.3), W / 2, 470)
        put(b, gtext('Power', 220, (254, 240, 138), (202, 138, 4), shadow=DEEP, sa=0.3), W / 2, 680)
        put(b, line_img([bold('= नए', 80), bold('Customers', 84, GREEN2)]), W / 2, 840)
        put(b, lphone('p16-wa-clean', 260, 0.08), 250, 1250, rot=-9)
        put(b, lphone('p04-front-clean', 290, 0.04), W / 2, 1230)
        put(b, lphone('p07-dash-clean', 260, 0.06), 830, 1250, rot=9)
        put(b, logo(110), W / 2, 1610)
        put(b, phone_pill(), W / 2, 1755, scale=0.85)
        return b.convert('RGB')
    return cached('thumb7', mk)

GM = [(0, 10), (12.1, 25), (25.1, 40), (39.2, 55), (46.4, 65), (58.2, 75), (65.7, 85), (76.3, 95), (85.2, 99), (99, 99)]
def gm(t):
    for (a, va), (b2, vb) in zip(GM, GM[1:]):
        if a <= t <= b2: return lerp(va, vb, eio((t - a) / max(0.01, min(1.2, b2 - a))))
    return 99
def topbar(base, t, dark=False):
    fg = WHITE if dark else DEEP; bgc = (16, 90, 50) if dark else WHITE
    left = pill('SHRI TECH  ·  ☎ 9993615146', 24, bg=bgc, fg=fg, path=FB, padx=20, pady=10, dot=YEL if dark else GREEN, shadow=not dark)
    put(base, left, 40 + left.width / 2 - 14, 120)
    v = gm(t)
    def mk():
        w, h = 330, 52
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), h // 2, fill=bgc + (255,))
        p.text((20, h / 2), 'डिजिटल ग्रोथ', 21, fg, FB, anchor='lm')
        x0, x1 = 160, 262
        p.rect((x0, h / 2 - 4, x1, h / 2 + 4), 4, fill=(fg + (50,)))
        p.rect((x0, h / 2 - 4, x0 + (x1 - x0) * v / 100, h / 2 + 4), 4, fill=(YEL if dark else GREEN) + (255,))
        p.text((w - 18, h / 2), f'{int(v)}%', 21, fg, FB, anchor='rm')
        im = p.img()
        return with_shadow(im, blur=12, off=6, alpha=0.18) if not dark else im
    im = cached(('gm', int(v), dark), mk)
    put(base, im, W - 40 - im.width / 2 + (14 if not dark else 0), 120)
L.topbar = topbar

L.SC = SC
L.END = END
L.SCENES = [k1, k2, k3, k4, k5, k6, k7, k8, k9]
L.thumbnail = thumbnail
L.BR_Y, L.PH_Y = 1655, 1765
L.MODES = ['up', 'blur', 'left', 'color', 'pop', 'right', 'up', 'blur', 'pop']
L.PMODES = ['type', 'ring', 'glow', 'up', 'ring', 'left', 'glow', 'ring', 'glow']
def particles(base, t, dark):
    for (x, y, r, sp, ph, c) in L.PARTS:
        yy_ = (y - t * sp) % (H + 100) - 50
        xx_ = x + math.sin(t * 0.8 + ph) * 30
        if 1380 < yy_ < 1840: continue
        im = cached(('dot', int(r), c), lambda: L.dot_img(int(r), c))
        put(base, im, xx_, yy_, alpha=0.35 + 0.25 * math.sin(t * 2 + ph))
L.particles = particles

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            if ts == 'thumb': L.thumbnail().save('/home/claude/r7/out/ShriTech_DigitalPower_Thumbnail.jpg', quality=92)
            else: L.frame(float(ts)).save(f'/home/claude/r7/st/st_{ts}.jpg', quality=85)
    else:
        L.render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
