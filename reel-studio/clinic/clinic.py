import sys, os, math, random
sys.path.insert(0, '/home/claude/clinic')      # clinic words.py wins
sys.path.insert(1, '/home/claude/salon')
import salon as L
from salon import *
from PIL import Image, ImageDraw, ImageFilter

UP = '/mnt/user-data/uploads/'
END = 48.4

# ---------- shared pieces ----------
def phone_shot(name, w=400, scroll=0.0, hcrop=None):
    """White phone with a ShriTech website screenshot inside."""
    key = ('phone', name, w, round(scroll, 2))
    def mk():
        h = int(w * 2.05)
        sc = Image.open(UP + name + '-image.jpg').convert('RGB')
        iw = w - 36
        s2 = sc.resize((iw, int(sc.height * iw / sc.width)), Image.LANCZOS)
        ih = h - 60
        y0 = int(max(0, s2.height - ih) * scroll)
        s2 = s2.crop((0, y0, iw, y0 + ih))
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 56, fill=WHITE + (255,), outline=MINT2 + (255,), width=4)
        im = p.img()
        m = Image.new('L', (iw, ih), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, iw - 1, ih - 1), 40, fill=255)
        im.paste(s2, (18, 30), m)
        q = Pad(w, h); q.rect((w / 2 - 50, 38, w / 2 + 50, 56), 9, fill=(0, 0, 0, 255))
        im.alpha_composite(q.img())
        return with_shadow(im, blur=30, off=20, alpha=0.25)
    return cached(key, mk)

def tooth_img(size=220, sparkle=False, col=WHITE):
    def mk():
        p = Pad(size, size)
        s = size / 220
        p.rect((40 * s, 30 * s, 180 * s, 140 * s), 56 * s, fill=col + (255,), outline=DEEP + (255,), width=6 * s)
        p.poly([(52 * s, 110 * s), (90 * s, 110 * s), (84 * s, 200 * s), (64 * s, 200 * s)], fill=col + (255,))
        p.poly([(130 * s, 110 * s), (168 * s, 110 * s), (156 * s, 200 * s), (136 * s, 200 * s)], fill=col + (255,))
        p.line([(52 * s, 110 * s), (64 * s, 200 * s), (84 * s, 200 * s), (96 * s, 140 * s), (124 * s, 140 * s), (136 * s, 200 * s), (156 * s, 200 * s), (168 * s, 110 * s)], DEEP + (255,), 6 * s)
        p.rect((46 * s, 100 * s, 174 * s, 128 * s), 8 * s, fill=col + (255,))
        p.ell((70 * s, 52 * s, 96 * s, 70 * s), fill=WHITE + (200,))
        return p.img()
    return cached(('tooth', size, col), mk)

def icon_badge(kind, r=58, bg=YEL, fg=DEEP):
    def mk():
        p = Pad(r * 2, r * 2)
        p.ell((0, 0, r * 2 - 1, r * 2 - 1), fill=bg + (255,))
        c = r
        if kind == 'cross':
            p.rect((c - 12, c - 34, c + 12, c + 34), 6, fill=fg + (255,)); p.rect((c - 34, c - 12, c + 34, c + 12), 6, fill=fg + (255,))
        elif kind == 'eye':
            p.ell((c - 38, c - 20, c + 38, c + 20), fill=WHITE + (255,), outline=fg + (255,), width=5); p.ell((c - 13, c - 13, c + 13, c + 13), fill=fg + (255,))
        elif kind == 'skin':
            for k in range(3):
                p.ell((c - 30 + k * 20, c - 18 - k * 6, c - 10 + k * 20, c + 2 - k * 6), fill=WHITE + (255,))
            p.arc((c - 34, c - 30, c + 34, c + 38), 20, 160, fg + (255,), 6)
        elif kind == 'physio':
            p.ell((c - 10, c - 40, c + 10, c - 20), fill=fg + (255,))
            p.line([(c, c - 18), (c, c + 12), (c - 22, c + 38)], fg + (255,), 8); p.line([(c, c + 12), (c + 24, c + 34)], fg + (255,), 8)
            p.line([(c - 30, c - 6), (c + 30, c - 14)], fg + (255,), 8)
        elif kind == 'steth':
            p.arc((c - 30, c - 36, c + 10, c + 20), 0, 180, fg + (255,), 7)
            p.line([(c - 10, c + 20), (c - 10, c + 30)], fg + (255,), 7)
            p.arc((c - 10, c + 4, c + 34, c + 44), 90, 360, fg + (255,), 7)
            p.ell((c + 22, c - 2, c + 42, c + 18), fill=fg + (255,))
        im = p.img()
        if kind == 'tooth':
            t = tooth_img(int(r * 1.3)); im.alpha_composite(t, (int(r - t.width / 2), int(r - t.height / 2)))
        return with_shadow(im, blur=10, off=6, alpha=0.22)
    return cached(('ib', kind, r, bg, fg), mk)

def card(w, h, fill=WHITE, r=30, outline=None):
    p = Pad(w, h); p.rect((0, 0, w - 1, h - 1), r, fill=fill + (255,), outline=(outline + (255,)) if outline else None, width=3); return p

def big_num(n, label):
    def mk():
        p = Pad(560, 220)
        p.ell((10, 10, 210, 210), fill=YEL + (255,))
        p.text((110, 112), str(n), 130, DEEP, PB, anchor='mm')
        p.text((240, 110), label, 74, DEEP, PB, anchor='lm')
        return with_shadow(p.img(), blur=14, off=8, alpha=0.2)
    return cached(('bignum', n, label), mk)

# ---------- scenes ----------
SC = [0.0, 4.1, 7.3, 14.7, 22.1, 28.0, 32.7, 37.2, 41.0, 46.85, END]

def clinic_front(slots_on):
    key = ('front', slots_on)
    def mk():
        w, h = 760, 640
        p = Pad(w, h)
        p.rect((0, 120, w - 1, h - 1), 36, fill=WHITE + (255,))
        p.rect((60, 40, w - 60, 160), 30, fill=GREEN + (255,))
        p.text((w / 2 + 30, 100), 'CLINIC', 60, WHITE, PB, anchor='mm')
        p.rect((180, 70, 240, 130), 12, fill=WHITE + (255,))
        p.rect((203, 78, 217, 122), 3, fill=GREEN + (255,)); p.rect((188, 93, 232, 107), 3, fill=GREEN + (255,))
        # door
        p.rect((300, 330, 460, h - 1), 18, fill=MINT2 + (255,), outline=GREEN2 + (255,), width=4)
        p.ell((428, 480, 444, 496), fill=YEL + (255,))
        # windows
        for x in (80, 520):
            p.rect((x, 220, x + 160, 380), 18, fill=MINT + (255,), outline=GREEN2 + (255,), width=4)
            p.line([(x + 80, 220), (x + 80, 380)], GREEN2 + (255,), 4); p.line([(x, 300), (x + 160, 300)], GREEN2 + (255,), 4)
        p.rect((0, h - 30, w - 1, h - 1), 10, fill=YEL + (255,))
        return with_shadow(p.img(), blur=30, off=20, alpha=0.18)
    return cached(key, mk)

def slot_board(filled):
    key = ('slots', filled)
    def mk():
        w, h = 420, 470
        p = card(w, h)
        p.rect((0, 0, w - 1, 84), 30, fill=DEEP + (255,)); p.rect((0, 50, w - 1, 84), 0, fill=DEEP + (255,))
        p.text((28, 44), 'आज के अपॉइंटमेंट', 28, YEL, PB, anchor='lm')
        times = ['10:00', '11:00', '12:00', '4:00', '5:00', '6:00']
        for i, tm in enumerate(times):
            y = 112 + i * 58
            p.text((30, y + 20), tm, 24, DEEP, FB, anchor='lm')
            on = i < filled
            p.rect((130, y, w - 30, y + 42), 12, fill=(GREEN if on else MINT) + (255,), outline=None if on else MINT2 + (255,), width=2)
            p.text((150, y + 21), 'बुक ✓' if on else 'खाली', 22, WHITE if on else (120, 150, 130), PB, anchor='lm')
        return with_shadow(p.img(), blur=24, off=14, alpha=0.2)
    return cached(key, mk)

def c1(t):
    b = bg_light(t)
    headline(b, t, 0, [(0.1, [bold('अपॉइंटमेंट्स', 100)]), (1.0, [bold('कैसे', 86), accent('badhayein?', 100)])], y0=300)
    p = eback(prog(t, 0.05, 0.6))
    put(b, clinic_front(0), W / 2 - 120, 1000 + (1 - p) * 100, scale=0.78 * (0.9 + 0.1 * p) * (1 + 0.015 * t), alpha=min(1, p * 2))
    q = eback(prog(t, 1.9, 0.5))
    filled = 0 if t < 2.6 else min(2, int((t - 2.6) * 3))
    put(b, slot_board(filled), W / 2 + 250, 1010 + math.sin(t * 2) * 6, scale=0.85 * q, rot=4 * (1 - q))
    for i, (k, x, y, t0) in enumerate([('tooth', 160, 700, 1.15), ('eye', 920, 640, 1.35), ('skin', 130, 1270, 1.55)]):
        if t > t0: put(b, icon_badge(k, 52, YEL if i % 2 == 0 else GREEN, DEEP), x, y + math.sin(t * 2.4 + i) * 10, scale=eback(prog(t, t0, 0.35)))
    if t > 3.25:
        put(b, pill('टास्क मिला  ✓', 34, bg=GREEN, fg=WHITE, path=PB), W / 2, 1290, scale=eback(prog(t, 3.25, 0.4), 2.2), rot=-4)
    return b, False

def roadmap(lit):
    key = ('road', lit)
    def mk():
        w, h = 900, 700
        p = Pad(w, h)
        pts = [(140, 590), (300, 430), (560, 470), (760, 250)]
        for a, c in zip(pts, pts[1:]):
            p.line([a, c], MINT2 + (255,), 26)
            for k in range(0, 10, 2):
                x0 = lerp(a[0], c[0], k / 10); y0 = lerp(a[1], c[1], k / 10)
                x1 = lerp(a[0], c[0], (k + 1) / 10); y1 = lerp(a[1], c[1], (k + 1) / 10)
                p.line([(x0, y0), (x1, y1)], WHITE + (255,), 6)
        labels = [('1', 'एजुकेशन रील्स'), ('2', 'पेशेंट रिव्यूज़'), ('3', 'गूगल प्रोफ़ाइल'), ('★', 'रिमाइंडर्स')]
        for i, ((x, y), (n, lb)) in enumerate(zip(pts, labels)):
            on = i < lit
            p.ell((x - 52, y - 52, x + 52, y + 52), fill=(YEL if on else WHITE) + (255,), outline=(DEEP if on else MINT2) + (255,), width=5)
            p.text((x, y + 2), n, 50, DEEP, PB if n != '★' else FSYM, anchor='mm')
            f = font(PB, 30); tw = f.getlength(lb)
            ly = y + 92 if i % 2 == 0 else y - 92
            p.rect((x - tw / 2 - 22, ly - 30, x + tw / 2 + 22, ly + 30), 30, fill=(DEEP if on else WHITE) + (255,))
            p.text((x, ly), lb, 30, YEL if on else DEEP, PB, anchor='mm')
        return with_shadow(p.img(), blur=16, off=10, alpha=0.18)
    return cached(key, mk)

def c2(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 4.1, [(4.15, [bold('हमारा', 92), accent('3-step', 104)]), (4.8, [bold('ग्रोथ प्लान', 100)])], y0=300)
    lit = 0 if t < 6.4 else 1
    p = eo(prog(t, 4.3, 0.7))
    put(b, roadmap(lit), W / 2 + 20, 930 + (1 - p) * 120, alpha=p)
    if t > 6.4:
        put(b, big_num(1, 'पहला'), W / 2 + 40, 600, scale=eback(prog(t, 6.4, 0.4), 2.2))
        q = prog(t, 6.4, 0.6)
        for k in range(8):
            a = k * math.pi / 4
            sparkle(b, 250 + math.cos(a) * 110 * q, 1170 + math.sin(a) * 110 * q, t, 6.4 + k * 0.03, 18, YEL if k % 2 else GREEN)
    # walker on path
    k = eio(prog(t, 4.6, 1.6))
    return b, False

def reel_screen(topic, views):
    key = ('reelscr', topic, views)
    def mk():
        w, h = 430, 860
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 56, fill=WHITE + (255,), outline=MINT2 + (255,), width=4)
        p.rect((18, 26, w - 18, h - 26), 42, fill=(PALEY if topic == 'gums' else MINT) + (255,))
        p.rect((w / 2 - 50, 38, w / 2 + 50, 56), 9, fill=DEEP + (255,))
        title = 'ब्लीडिंग गम्स?' if topic == 'gums' else 'स्केलिंग क्या है?'
        p.rect((40, 92, w - 40, 170), 20, fill=WHITE + (255,))
        p.text((w / 2, 131), title, 38, DEEP, PB, anchor='mm')
        p.rect((40, h - 200, w - 40, h - 140), 30, fill=(YEL if topic == 'gums' else GREEN) + (255,))
        p.text((w / 2, h - 170), 'इसे इग्नोर ना करें!' if topic == 'gums' else 'दाँत साफ़ & मज़बूत', 26, DEEP if topic == 'gums' else WHITE, PB, anchor='mm')
        p.text((40, h - 90), '▶  ' + views + ' व्यूज़', 26, DEEP, FSYM if False else PB, anchor='lm')
        for i, sym in enumerate(['♥', '✓', '↻']):
            cy = 360 + i * 90
            p.ell((w - 92, cy - 30, w - 32, cy + 30), fill=WHITE + (255,))
            p.text((w - 62, cy), sym, 30, GREEN2, FSYM, anchor='mm')
        im = p.img()
        if topic == 'gums':
            tth = tooth_img(240)
            im.alpha_composite(tth, (int(w / 2 - 120 - 20), 300))
            q = Pad(w, h)
            for dx, dy in ((0, 0), (40, 30)):
                cx, cy = w / 2 - 20 + dx - 30, 540 + dy
                q.poly([(cx, cy - 22), (cx - 14, cy), (cx + 14, cy)], fill=YEL + (255,))
                q.ell((cx - 14, cy - 10, cx + 14, cy + 18), fill=YEL + (255,))
            im.alpha_composite(q.img())
        else:
            tth = tooth_img(240)
            im.alpha_composite(tth, (int(w / 2 - 120 - 20), 300))
            q = Pad(w, h)
            q.line([(300, 330), (220, 430)], DEEP + (255,), 10); q.ell((205, 420, 235, 450), fill=YEL + (255,))
            im.alpha_composite(q.img())
        return with_shadow(im, blur=30, off=20, alpha=0.25)
    return cached(key, mk)

def c3(t):
    b = bg_light(t)
    ghost_word(b, 'REELS', t, 760, GREEN, 0.07)
    headline(b, t, 7.3, [(7.35, [bold('पेशेंट एजुकेशन', 92)]), (8.35, [accent('reels', 120)])], y0=290)
    topic = 'gums' if t < 12.9 else 'scale'
    tr = clamp(prog(t, 12.75, 0.15) - prog(t, 12.9, 0.15))
    views = int(lerp(1200, 12400, eio(prog(t, 8.5, 5.5))))
    vs = f'{views/1000:.1f}K'
    p = eback(prog(t, 7.3, 0.55))
    put(b, reel_screen(topic, vs), W / 2 - 60, 1010 + (1 - p) * 150 + math.sin(t * 1.8) * 6, scale=0.9 * (1 - 0.1 * tr), rot=-3 + 3 * math.sin(t * 0.7), alpha=min(1, p * 2) * (1 - 0.6 * tr))
    # other clinics' topics
    chips = [('स्किन केयर टिप्स', 'skin', 10.6, 860, 700), ('आँखों की देखभाल', 'eye', 11.3, 870, 900), ('फिज़ियो एक्सरसाइज़', 'physio', 12.0, 860, 1100)]
    for txt, k, t0, x, y in chips:
        if t > t0:
            q = eback(prog(t, t0, 0.4))
            put(b, icon_badge(k, 44, YEL, DEEP), x - 150, y, scale=q)
            put(b, pill(txt, 24, bg=WHITE, fg=DEEP, path=PB), x + 20, y + 60, scale=q)
    if t > 9.95:
        put(b, pill('ज़रूरी जानकारी', 28, bg=YEL, fg=DEEP, path=PB, dot=GREEN), 840, 1310, scale=eback(prog(t, 9.95, 0.35)), rot=-6)
    for x, y, t0 in [(240, 900, 13.0), (500, 820, 13.2), (300, 1180, 13.4)]:
        sparkle(b, x, y, t, t0, 28)
    return b, False

def review(name, text, stars=5, verified=True):
    def mk():
        w, h = 760, 170
        p = card(w, h, r=28)
        p.ell((24, 30, 104, 110), fill=MINT2 + (255,)); p.text((64, 72), name[0], 40, GREEN2, PB, anchor='mm')
        p.text((126, 52), name, 30, DEEP, PB, anchor='lm')
        for i in range(stars):
            cx, cy, r = 136 + i * 34, 94, 14
            pts = [(cx + math.cos(-math.pi / 2 + k * math.pi / 5) * (r if k % 2 == 0 else r * .45), cy + math.sin(-math.pi / 2 + k * math.pi / 5) * (r if k % 2 == 0 else r * .45)) for k in range(10)]
            p.poly(pts, fill=YEL + (255,))
        p.text((126, 136), text, 25, (40, 90, 60), FM, anchor='lm')
        if verified:
            p.rect((w - 200, 32, w - 26, 72), 20, fill=MINT + (255,))
            p.text((w - 113, 52), '✓ परमिशन', 21, GREEN2, PB, anchor='mm')
        return with_shadow(p.img(), blur=18, off=10, alpha=0.2)
    return cached(('rev', name, text, verified), mk)

def shield(fill_k):
    key = ('shield', round(fill_k, 2))
    def mk():
        w, h = 260, 300
        p = Pad(w, h)
        pts = [(w / 2, 10), (w - 20, 60), (w - 30, 170), (w / 2, h - 10), (30, 170), (20, 60)]
        p.poly(pts, fill=MINT2 + (255,))
        im = p.img()
        q = Pad(w, h); q.poly(pts, fill=GREEN + (255,))
        g = q.img(); cut = int(h - h * fill_k)
        mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rectangle((0, cut, w, h), fill=255)
        g.putalpha(Image.fromarray(np.minimum(np.array(g.getchannel('A')), np.array(mask))))
        im.alpha_composite(g)
        r = Pad(w, h); r.line([(85, 150), (120, 190), (185, 110)], WHITE + (255,), 16)
        im.alpha_composite(r.img())
        return with_shadow(im, blur=16, off=10, alpha=0.2)
    return cached(key, mk)

def c4(t):
    b = bg_light(t, tint=(255, 253, 240))
    if t < 15.5:
        put(b, big_num(2, 'दूसरा'), W / 2, 760, scale=eback(prog(t, 14.75, 0.4), 2.2))
    headline(b, t, 14.7, [(15.6, [bold('जेनुइन', 92), accent('reviews', 110)])], y0=310)
    revs = [('प्रिया शर्मा', '“दर्द बिल्कुल नहीं हुआ, डॉक्टर ने सब समझाया”', 15.65),
            ('रोहित वर्मा', '“साफ़ क्लिनिक, टाइम पर अपॉइंटमेंट”', 16.15),
            ('अंजलि मेहता', '“स्किन ट्रीटमेंट का रिज़ल्ट शानदार”', 16.6)]
    for i, (n, tx, t0) in enumerate(revs):
        if t > t0:
            q = eback(prog(t, t0, 0.45))
            put(b, review(n, tx, verified=t > 18.5), W / 2 + (1 - q) * 600 * (1 if i % 2 else -1), 620 + i * 200, alpha=min(1, q * 2))
    if t > 16.95:
        put(b, pill('★ हाइलाइट', 28, bg=YEL, fg=DEEP, path=PB), 870, 560, scale=eback(prog(t, 16.95, 0.35)), rot=8)
    if t > 18.1:
        q = eback(prog(t, 18.1, 0.4))
        on = t > 18.6
        put(b, cached(('consent', on), lambda: consent(on)), W / 2, 1230, scale=q)
    if t > 19.7:
        k = eio(prog(t, 20.9, 0.8))
        put(b, shield(k), 220, 1230, scale=eback(prog(t, 19.7, 0.4)))
        put(b, pill('ट्रस्ट  ' + str(int(40 + 58 * k)) + '%', 30, bg=DEEP, fg=YEL, path=PB), 870, 1230, scale=eback(prog(t, 20.8, 0.35)))
    return b, False

def consent(on):
    w, h = 470, 100
    p = card(w, h, r=50)
    p.text((36, h / 2), 'पेशेंट की परमिशन', 28, DEEP, PB, anchor='lm')
    p.rect((w - 130, 26, w - 36, 74), 24, fill=(GREEN if on else MINT2) + (255,))
    cx = w - 60 if on else w - 106
    p.ell((cx - 20, 30, cx + 20, 70), fill=WHITE + (255,))
    return with_shadow(p.img(), blur=14, off=8, alpha=0.2)

def map_card(rank_k, booked):
    key = ('map', round(rank_k, 2), booked)
    def mk():
        w, h = 760, 720
        p = card(w, h, r=32)
        p.rect((20, 20, w - 20, 330), 22, fill=MINT + (255,))
        for (a, c) in [((20, 120), (w - 20, 200)), ((260, 20), (330, 330)), ((20, 280), (w - 20, 240)), ((560, 20), (520, 330))]:
            p.line([a, c], WHITE + (255,), 18)
        for (x, y, c) in [(150, 100, YEL), (430, 270, YEL), (640, 140, YEL), (380, 150, GREEN)]:
            big = c == GREEN
            r = 30 if big else 20
            p.ell((x - r, y - r * 2, x + r, y), fill=c + (255,))
            p.poly([(x - r * 0.7, y - r * 0.6), (x + r * 0.7, y - r * 0.6), (x, y + r * 0.6)], fill=c + (255,))
            p.ell((x - r * 0.4, y - r * 1.4, x + r * 0.4, y - r * 0.6), fill=WHITE + (255,))
        im = p.img()
        # listing rows: our clinic rises to #1
        q = Pad(w, h)
        rows = [('City Clinic', '4.1', False), ('Care Plus', '4.3', False), ('Smile Care Clinic', '4.9', True)]
        ys = [370, 470, 570]
        for i, (n, rt, ours) in enumerate(rows):
            y = ys[i]
            if ours: y = lerp(570, 370, eio(rank_k))
            elif rank_k > 0: y = ys[i] + 100 * eio(rank_k)
            fillc = PALEY if ours else WHITE
            q.rect((20, y, w - 20, y + 88), 20, fill=fillc + (255,), outline=(YEL if ours else MINT2) + (255,), width=3)
            q.text((44, y + 32), n, 28, DEEP, PB, anchor='lm')
            q.text((44, y + 64), '★ ' + rt + ('  · 0.8 km' if ours else '  · 2 km'), 22, GREEN2, FB, anchor='lm')
            if ours:
                q.rect((w - 250, y + 20, w - 40, y + 68), 24, fill=(YEL if booked else GREEN) + (255,))
                q.text((w - 145, y + 44), 'बुक हो गया ✓' if booked else 'अपॉइंटमेंट बुक', 22, DEEP if booked else WHITE, PB, anchor='mm')
        im.alpha_composite(q.img())
        return with_shadow(im, blur=26, off=16, alpha=0.2)
    return cached(key, mk)

def c5(t):
    b = bg_light(t)
    if t < 23.0:
        put(b, big_num(3, 'तीसरा'), W / 2, 760, scale=eback(prog(t, 22.2, 0.4), 2.2))
    headline(b, t, 22.1, [(23.15, [bold('गूगल प्रोफ़ाइल', 92)]), (23.85, [accent('optimised', 104)])], y0=290)
    if t > 22.9:
        txt = 'clinic near me'
        n = int(len(txt) * prog(t, 23.0, 0.8))
        put(b, search_bar(txt[:n], int(t * 4) % 2 == 0), W / 2, 590, alpha=prog(t, 22.9, 0.2))
    if t > 23.4:
        q = eback(prog(t, 23.4, 0.5))
        rank = prog(t, 24.0, 0.9)
        booked = t > 26.0
        tap = 1 - 0.04 * math.sin(math.pi * prog(t, 25.55, 0.3))
        put(b, map_card(rank, booked), W / 2, 1010, scale=0.92 * q * tap, alpha=min(1, q * 2))
        if t > 24.6:
            put(b, pill('#1 रैंक', 30, bg=YEL, fg=DEEP, path=PB), 900, 840, scale=eback(prog(t, 24.6, 0.35)), rot=8)
    if t > 26.35:
        steps = ['समय चुनें', 'नाम डालें', 'कन्फर्म ✓']
        for i, s_ in enumerate(steps):
            t0 = 26.4 + i * 0.25
            if t > t0:
                put(b, pill(s_, 26, bg=GREEN if i == 2 else WHITE, fg=WHITE if i == 2 else DEEP, path=PB), 230 + i * 310, 1360, scale=eback(prog(t, t0, 0.3)))
    return b, False

def missed_chart(k):
    key = ('missed', round(k, 2))
    def mk():
        w, h = 440, 360
        p = card(w, h)
        p.text((30, 44), 'मिस्ड विज़िट्स', 28, DEEP, PB, anchor='lm')
        vals = [1.0, 0.85, 0.7, 0.45, 0.35, 0.25]
        for i, v in enumerate(vals):
            vv = lerp(1.0, v, k)
            x = 40 + i * 64
            hh = 200 * vv
            p.rect((x, 320 - hh, x + 44, 320), 10, fill=(YEL if i < 2 else GREEN) + (255,))
        p.rect((w - 150, 24, w - 26, 66), 20, fill=GREEN + (255,))
        p.text((w - 88, 45), f'-{int(70 * k)}%', 24, WHITE, PB, anchor='mm')
        return with_shadow(p.img(), blur=20, off=12, alpha=0.2)
    return cached(key, mk)

def notif(title, body, w=600):
    def mk():
        h = 130
        p = card(w, h, r=28)
        p.ell((24, 30, 94, 100), fill=GREEN + (255,))
        p.text((59, 66), '✓', 36, WHITE, FSYM, anchor='mm')
        p.text((116, 46), title, 24, GREEN2, PB, anchor='lm')
        p.text((116, 88), body, 26, DEEP, PB, anchor='lm')
        return with_shadow(p.img(), blur=16, off=10, alpha=0.22)
    return cached(('notif', title, body, w), mk)

def c6(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 28.0, [(28.1, [bold('अपॉइंटमेंट', 92)]), (28.95, [accent('reminders', 110)])], y0=290)
    p = eback(prog(t, 28.0, 0.55))
    put(b, phone_shot('4e9d3978', 380, 0.0), 300, 1030 + (1 - p) * 150, rot=-5, alpha=min(1, p * 2))
    ns = [('WhatsApp रिमाइंडर', 'कल सुबह 11 बजे आपका अपॉइंटमेंट', 28.6), ('अपॉइंटमेंट कन्फर्म', 'डॉ. मेहता · शाम 5:00', 29.3), ('फॉलो-अप', '7 दिन बाद चेक-अप', 29.9)]
    for i, (a, c, t0) in enumerate(ns):
        if t > t0:
            q = eback(prog(t, t0, 0.4))
            put(b, notif(a, c, 560), 700 + (1 - q) * 400, 700 + i * 150, alpha=min(1, q * 2))
    if t > 30.9:
        q = eback(prog(t, 30.9, 0.4))
        put(b, missed_chart(eio(prog(t, 31.2, 1.1))), 760, 1210, scale=0.9 * q)
    return b, True if False else False

def c7(t):
    b = bg_green(t)
    ghost_word(b, 'FOCUS', t, 900, WHITE, 0.09)
    headline(b, t, 32.7, [(32.75, [bold('हमारा फोकस', 96, WHITE)])], y0=300)
    if t < 35.2:
        q = eback(prog(t, 34.1, 0.4))
        v = int(lerp(10000, 124000, eio(prog(t, 33.0, 1.4))))
        put(b, cached(('views', v // 1000, t > 34.55), lambda: views_pill(v, t > 34.55)), W / 2, 760, scale=0.9 + 0.1 * eo(prog(t, 33.0, 0.4)))
        if t > 34.15:
            put(b, text_img('सिर्फ़ व्यूज़ नहीं…', 70, YEL, PB), W / 2, 950, alpha=prog(t, 34.15, 0.3))
    else:
        put(b, text_img('असली', 90, WHITE, PB), W / 2, 560, alpha=prog(t, 35.25, 0.3))
        put(b, text_img('appointments.', 130, YEL, PF), W / 2, 700, scale=0.8 + 0.2 * eback(prog(t, 35.45, 0.4)), alpha=prog(t, 35.45, 0.3))
        k = prog(t, 35.6, 1.4)
        n = int(4 + 20 * eio(k))
        put(b, calendar(n, n), W / 2, 1110, scale=0.82 * eback(prog(t, 35.3, 0.45)))
        if t > 36.3:
            put(b, pill(f'कन्फर्म्ड  {n}', 32, bg=YEL, fg=DEEP, path=PB), W / 2, 1300, scale=eback(prog(t, 36.3, 0.35)))
    return b, True

def views_pill(v, struck):
    txt = f'{v:,} व्यूज़'
    f = font(PB, 64); tw = f.getlength(txt)
    w, h = int(tw + 140), 130
    p = Pad(w, h)
    p.rect((0, 0, w - 1, h - 1), h // 2, fill=WHITE + (255,))
    p.text((w / 2, h / 2 + 2), txt, 64, DEEP, PB, anchor='mm')
    if struck: p.line([(40, h / 2), (w - 40, h / 2)], YEL + (255,), 10)
    return p.img()

def comment_box(txt, sent):
    key = ('cbox', txt, sent)
    def mk():
        w, h = 760, 110
        p = card(w, h, r=55)
        p.ell((20, 20, 90, 90), fill=MINT2 + (255,)); p.text((55, 56), 'Dr', 26, GREEN2, PB, anchor='mm')
        p.text((116, h / 2), txt if txt else 'कमेंट लिखें…', 34, DEEP if txt else (150, 170, 155), PB, anchor='lm')
        p.ell((w - 96, 20, w - 26, 90), fill=(YEL if sent else GREEN) + (255,))
        p.poly([(w - 78, 40), (w - 40, 55), (w - 78, 70), (w - 72, 55)], fill=(DEEP if sent else WHITE) + (255,))
        return with_shadow(p.img(), blur=16, off=10, alpha=0.22)
    return cached(key, mk)

def c8(t):
    b = bg_light(t)
    headline(b, t, 37.2, [(37.35, [bold('आप', 92), accent('doctor', 110), bold('हैं?', 92)])], y0=320)
    kinds = [('tooth', 'डेंटल', 200, 620), ('skin', 'स्किन', 880, 600), ('eye', 'आई केयर', 170, 830), ('physio', 'फिज़ियो', 900, 830), ('steth', 'जनरल', W / 2, 760)]
    for i, (k, lb, x, y) in enumerate(kinds):
        t0 = 37.4 + i * 0.15
        if t > t0:
            q = eback(prog(t, t0, 0.4))
            yy_ = y + math.sin(t * 2 + i) * 8
            put(b, icon_badge(k, 60, YEL if i % 2 == 0 else GREEN, DEEP), x, yy_, scale=q)
            put(b, pill(lb, 24, bg=WHITE, fg=DEEP, path=PB), x, yy_ + 92, scale=q)
    if t > 38.6:
        q = eo(prog(t, 38.6, 0.3))
        txt = 'GROWTH'
        n = int(len(txt) * prog(t, 39.2, 0.5))
        sent = t > 39.95
        put(b, comment_box(txt[:n], sent), W / 2, 1110, alpha=q)
        put(b, pill('कमेंट करो', 30, bg=DEEP, fg=YEL, path=PB), W / 2 - 230, 1010, scale=eback(prog(t, 38.75, 0.3)), rot=-5)
        if n == 6:
            put(b, pill('GROWTH', 44, bg=GREEN, fg=WHITE, path=PB, padx=36), W / 2 + 200, 1010, scale=eback(prog(t, 39.4, 0.4), 2.4), rot=6)
    if t > 40.15:
        k = eo(prog(t, 40.15, 0.7))
        put(b, cached('plane', plane_img), lerp(W / 2 + 320, 980, k), lerp(1110, 700, k), alpha=1 - prog(t, 40.7, 0.2))
        put(b, pill('हम DM में भेजेंगे ✓', 30, bg=YEL, fg=DEEP, path=PB), W / 2, 1290, scale=eback(prog(t, 40.4, 0.35)))
    return b, False

def plane_img():
    p = Pad(120, 100)
    p.poly([(5, 50), (115, 5), (70, 95), (55, 60)], fill=GREEN + (255,))
    p.poly([(55, 60), (115, 5), (70, 95)], fill=GREEN2 + (255,))
    return p.img()

STRATS = ['पेशेंट एजुकेशन रील्स', 'रिव्यू & ट्रस्ट पोस्ट्स', 'गूगल प्रोफ़ाइल बूस्ट', 'WhatsApp रिमाइंडर्स', '1-क्लिक FB + Insta पोस्टिंग']
def strat_list(opened, hl):
    key = ('strat', opened, hl)
    def mk():
        w, h = 640, 560
        p = card(w, h, r=32)
        for i, s_ in enumerate(STRATS):
            y = 30 + i * 104
            on = i < opened
            p.rect((24, y, w - 24, y + 86), 22, fill=((PALEY if i == hl else MINT) if on else WHITE) + (255,), outline=(YEL if i == hl else MINT2) + (255,), width=3)
            p.ell((40, y + 15, 96, y + 71), fill=(GREEN if on else MINT2) + (255,))
            p.text((68, y + 44), str(i + 1), 30, WHITE if on else DEEP, PB, anchor='mm')
            if on: p.text((118, y + 43), s_, 28, DEEP, PB, anchor='lm')
            else:
                p.rect((118, y + 32, 380, y + 54), 10, fill=MINT + (255,))
            # lock / check
            cx = w - 66
            if on:
                p.line([(cx - 14, y + 44), (cx - 4, y + 54), (cx + 14, y + 32)], GREEN2 + (255,), 6)
            else:
                p.arc((cx - 12, y + 22, cx + 12, y + 46), 180, 360, DEEP + (255,), 5)
                p.rect((cx - 16, y + 34, cx + 16, y + 62), 6, fill=DEEP + (255,))
        return with_shadow(p.img(), blur=26, off=16, alpha=0.2)
    return cached(key, mk)

def growth_card(k):
    key = ('growth', round(k, 2))
    def mk():
        w, h = 640, 190
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 30, fill=DEEP + (255,))
        p.text((32, 44), 'नए पेशेंट्स / महीना', 24, (200, 230, 210), FB, anchor='lm')
        p.text((32, 118), f'+{int(40 * k)}', 72, YEL, PB, anchor='lm')
        pts = [(260 + i * 50, 150 - (i ** 1.6) * 9 * k - 10 * math.sin(i) * k) for i in range(8)]
        p.line(pts, GREEN + (255,), 7)
        p.ell((pts[-1][0] - 10, pts[-1][1] - 10, pts[-1][0] + 10, pts[-1][1] + 10), fill=YEL + (255,))
        return with_shadow(p.img(), blur=20, off=12, alpha=0.25)
    return cached(key, mk)

def c9(t):
    b = bg_light(t, tint=(255, 253, 240))
    headline(b, t, 41.0, [(41.15, [bold('5', 110, GREEN2), bold('स्ट्रैटेजीज़', 96)]), (42.8, [bold('नए', 80), accent('patients', 104), bold('के लिए', 80)])], y0=280)
    opened = 0 if t < 41.6 else min(5, 1 + int((t - 41.6) / 0.5))
    hl = opened - 1 if t < 44.5 else 4
    p = eback(prog(t, 41.0, 0.5))
    put(b, strat_list(opened, hl), W / 2 - 110, 960 + (1 - p) * 120, scale=0.92, alpha=min(1, p * 2))
    if t > 43.4:
        q = eback(prog(t, 43.4, 0.5))
        put(b, phone_shot('173cd744', 300, 0.0), 880, 960 + math.sin(t * 2) * 8, rot=6, scale=q)
    if t > 44.5:
        q = eback(prog(t, 44.5, 0.45))
        put(b, growth_card(eio(prog(t, 44.7, 1.4))), W / 2, 1320, scale=0.92 * q)
    return b, False

def c10(t):
    b = bg_light(t, glow=GREEN, glow2=YEL)
    q = eback(prog(t, 46.85, 0.5))
    put(b, logo(150), W / 2, 540, scale=0.7 + 0.3 * q, alpha=min(1, q * 2))
    put(b, text_img('क्लिनिक की डिजिटल ग्रोथ पार्टनर', 34, GREEN2, PB), W / 2, 660, alpha=prog(t, 47.0, 0.3))
    k = eback(prog(t, 47.0, 0.45))
    tap = 1 - 0.08 * math.sin(math.pi * prog(t, 47.25, 0.25))
    pulse = 1 + 0.05 * math.sin(max(0, t - 47.4) * 9) * (t > 47.4)
    put(b, follow_btn(t > 47.35), W / 2, 860, scale=k * tap * pulse)
    if t > 47.1:
        hp = eo(prog(t, 47.1, 0.2))
        put(b, cached('cursor', cursor_img), W / 2 + 180 - 40 * hp, 940 + 60 * (1 - hp), alpha=hp)
    put(b, text_img('अधिक जानकारी के लिए', 40, DEEP, PB), W / 2, 1180, alpha=prog(t, 47.2, 0.3))
    put(b, phone_pill(), W / 2, 1290, scale=eback(prog(t, 47.25, 0.45)))
    return b, False

# ---------- thumbnail ----------
def thumbnail():
    def mk():
        b = bg_light(0.5)
        put(b, cached('tg', lambda: outline_text('CLINIC', 330, GREEN)), W / 2, 1050, alpha=0.10)
        put(b, pill('क्लिनिक ओनर्स ध्यान दें!', 40, bg=DEEP, fg=YEL, path=PB, padx=36, pady=16), W / 2, 300)
        put(b, line_img([bold('खाली अपॉइंटमेंट', 104, DEEP)]), W / 2, 470)
        put(b, line_img([bold('स्लॉट्स?', 104, DEEP), accent('3 steps', 116, GREEN2)]), W / 2, 610)
        put(b, line_img([bold('में भरें!', 100, DEEP)]), W / 2, 745)
        put(b, calendar(22, 22), W / 2 + 140, 1170, scale=0.78, rot=-4)
        put(b, reel_screen('gums', '12.4K'), W / 2 - 260, 1180, scale=0.55, rot=7)
        for k, x, y in [('tooth', 140, 880), ('eye', 960, 860), ('steth', 940, 1430)]:
            put(b, icon_badge(k, 58, YEL, DEEP), x, y)
        put(b, logo(110), W / 2, 1610)
        put(b, phone_pill(), W / 2, 1745, scale=0.85)
        return b.convert('RGB')
    return cached('thumb', mk)

L.SC = SC
L.END = END
L.SCENES = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
L.thumbnail = thumbnail
L.MODES = ['up', 'blur', 'left', 'color', 'pop', 'right', 'up', 'hide', 'blur', 'up']
L.PMODES = ['type', 'ring', 'glow', 'left', 'ring', 'up', 'glow', 'ring', 'type', 'glow']

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            if ts == 'thumb': thumbnail().save('/home/claude/clinic/out/ShriTech_Clinic_Thumbnail.jpg', quality=92)
            else: L.frame(float(ts)).save(f'/home/claude/clinic/st/st_{ts}.jpg', quality=85)
    else:
        L.render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
