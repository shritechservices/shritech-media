import sys, math, random
sys.path.insert(0, '/home/claude/r6')       # r6 words.py wins
sys.path.insert(1, '/home/claude/salon')
sys.path.insert(2, '/home/claude/clinic')
import salon as L
from salon import *
from clinic import phone_shot, card, icon_badge
from PIL import Image, ImageDraw, ImageFilter

END = 27.6
SC = [0.0, 2.9, 5.3, 9.45, 12.1, 14.85, 18.85, 23.95, 26.35, END]

# ---------- pieces ----------
POSTC = [(YEL2, GREEN), (MINT2, GREEN2), (PALEY, YEL), (GREEN, DEEP), (YEL, GREEN2)]
def mini_post(i, w=150):
    def mk():
        h = int(w * 1.25)
        c1, c2 = POSTC[i % 5]
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 16, fill=WHITE + (255,), outline=MINT2 + (255,), width=2)
        p.rect((8, 8, w - 8, h * 0.68), 10, fill=c1 + (255,))
        p.ell((w * .3, h * .16, w * .7, h * .5), fill=c2 + (255,))
        p.rect((12, h * .74, w * .8, h * .74 + 8), 4, fill=MINT2 + (255,))
        p.rect((12, h * .84, w * .55, h * .84 + 8), 4, fill=MINT2 + (255,))
        return p.img()
    return cached(('mpost', i % 5, w), mk)

def ai_chip(size=200, glow=0.0):
    def mk():
        p = Pad(size, size)
        s = size / 200
        for k in range(4):
            for side in range(4):
                o = 50 * s + k * 33 * s
                if side == 0: p.rect((o - 6 * s, 8 * s, o + 6 * s, 40 * s), 4, fill=GREEN2 + (255,))
                if side == 1: p.rect((o - 6 * s, 160 * s, o + 6 * s, 192 * s), 4, fill=GREEN2 + (255,))
                if side == 2: p.rect((8 * s, o - 6 * s, 40 * s, o + 6 * s), 4, fill=GREEN2 + (255,))
                if side == 3: p.rect((160 * s, o - 6 * s, 192 * s, o + 6 * s), 4, fill=GREEN2 + (255,))
        p.rect((36 * s, 36 * s, 164 * s, 164 * s), 26 * s, fill=DEEP + (255,))
        p.rect((50 * s, 50 * s, 150 * s, 150 * s), 18 * s, outline=GREEN + (255,), width=4 * s)
        p.text((100 * s, 102 * s), 'AI', int(60 * s), YEL, PB, anchor='mm')
        return with_shadow(p.img(), blur=18, off=10, alpha=0.25)
    return cached(('aichip', size), mk)

def bolt(size=90, col=YEL):
    def mk():
        p = Pad(size, size)
        s = size / 90
        p.poly([(50 * s, 2 * s), (14 * s, 52 * s), (42 * s, 52 * s), (34 * s, 88 * s), (76 * s, 34 * s), (48 * s, 34 * s)], fill=col + (255,))
        return p.img()
    return cached(('bolt', size, col), mk)

def owner_card(label='आप', w=360, h=440, mood='happy'):
    return portrait_card(label, mood, w, h, bg1=PALEY, bg2=YEL)

def hand(size=150):
    def mk():
        p = Pad(size, int(size * 1.3))
        s = size / 150
        p.rect((55 * s, 10 * s, 85 * s, 120 * s), 15 * s, fill=SKIN + (255,), outline=DEEP + (255,), width=4 * s)
        p.rect((30 * s, 90 * s, 130 * s, 190 * s), 40 * s, fill=SKIN + (255,), outline=DEEP + (255,), width=4 * s)
        p.rect((57 * s, 85 * s, 83 * s, 100 * s), 6 * s, fill=SKIN + (255,))
        return p.img()
    return cached(('hand', size), mk)

def counter_pill(icon, n, label, bg=WHITE, fg=DEEP):
    return pill(f'{icon}  {n}  {label}', 30, bg=bg, fg=fg, path=PB)

def doc_card(k):
    key = ('doc', round(k, 2))
    def mk():
        w, h = 560, 470
        p = card(w, h, r=30)
        p.rect((0, 0, w - 1, 80), 30, fill=DEEP + (255,)); p.rect((0, 46, w - 1, 80), 0, fill=DEEP + (255,))
        p.text((30, 42), 'कैप्शन लिखा जा रहा है…', 26, YEL, PB, anchor='lm')
        lines = ['दिवाली धमाका ऑफ़र! 🎉', 'सभी कपड़ों पर 30% छूट', 'सिर्फ़ 3 दिन — आज ही आएँ', '#Sale #Diwali #Offer']
        total = sum(len(x) for x in lines); shown = int(total * k)
        y = 130
        for ln in lines:
            if shown <= 0: break
            part = ln[:shown]; shown -= len(ln)
            p.text((36, y), part.replace('🎉', ''), 30, DEEP if not part.startswith('#') else GREEN2, PB if y == 130 else FB, anchor='lm')
            y += 74
        if k < 1:
            p.rect((36, y - 20, 44, y + 20), 2, fill=GREEN + (255,))
        return with_shadow(p.img(), blur=24, off=14, alpha=0.2)
    return cached(key, mk)

def gen_tile(i, k, w=170):
    key = ('tile', i, round(k, 1), w)
    def mk():
        base = mini_post(i, w).copy()
        if k < 1:
            sh = Image.new('RGBA', base.size, MINT + (255,))
            d = ImageDraw.Draw(sh)
            x = int(base.width * (k * 2 - 0.5))
            d.polygon([(x - 40, 0), (x + 10, 0), (x + 50, base.height), (x, base.height)], fill=WHITE + (255,))
            m = Image.new('L', base.size, 0); ImageDraw.Draw(m).rectangle((0, int(base.height * k), base.width, base.height), fill=255)
            base.paste(sh, (0, 0), m)
        return with_shadow(base, blur=12, off=6, alpha=0.18)
    return cached(key, mk)

def eq_card(txt, sub, bg, fg, w=290, h=200, icon=None):
    def mk():
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 30, fill=bg + (255,))
        p.text((w / 2, h * 0.42), txt, 44, fg, PB, anchor='mm')
        p.text((w / 2, h * 0.75), sub, 26, fg, FB, anchor='mm')
        return with_shadow(p.img(), blur=18, off=10, alpha=0.22)
    return cached(('eq', txt, sub, bg, w, h), mk)

# ---------- scenes ----------
def feed_strip(t, speed, x, y, w=150, n=12, blur=0, alpha=1.0):
    """Vertical scrolling column of mini posts inside a phone-ish window."""
    hh = int(w * 1.25) + 16
    off = (t * speed) % hh
    for k in range(-1, n):
        put(L_cur, mini_post(k + int(t * speed // hh), w), x, y + k * hh - off, alpha=alpha)

def phone_frame(w=420, h=820):
    def mk():
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), 56, fill=(0, 0, 0, 0), outline=DEEP + (255,), width=14)
        p.rect((w / 2 - 60, 22, w / 2 + 60, 42), 10, fill=DEEP + (255,))
        return p.img()
    return cached(('pframe', w, h), mk)

def phone_feed(base, t, speed, cx, cy, w=420, h=820, blur=0, highlight=None):
    """Phone with scrolling feed. highlight=(k) shows one big post stopped."""
    inner = Image.new('RGBA', (w - 28, h - 28), WHITE + (255,))
    pw = (w - 28 - 30) // 2
    hh = int(pw * 1.25) + 14
    off = (t * speed) % hh
    for col in range(2):
        for k in range(-1, 7):
            idx = k + int(t * speed // hh) + col * 3
            im = mini_post(idx, pw)
            inner.alpha_composite(im, (10 + col * (pw + 10), int(14 + k * hh - off + (col * hh / 2))))
    if blur: inner = inner.filter(ImageFilter.GaussianBlur(blur))
    m = Image.new('L', inner.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, inner.width - 1, inner.height - 1), 44, fill=255)
    inner.putalpha(m)
    put(base, inner, cx, cy)
    put(base, phone_frame(w, h), cx, cy)

def r1(t):
    b = bg_light(t)
    headline(b, t, 0, [(0.1, [bold('AI से', 96), bold('100', 110, GREEN2), bold('पोस्ट', 96)]), (1.4, [accent('ban gayi?', 110)])], y0=300)
    # posts burst out of the AI chip into a 10x10 grid
    put(b, ai_chip(180), W / 2, 1000, scale=eback(prog(t, 0.0, 0.4)) * (1 + 0.05 * math.sin(t * 10)))
    n = int(100 * eio(prog(t, 0.3, 2.0)))
    for i in range(n):
        r, c = divmod(i, 10)
        tx, ty = 135 + c * 90, 640 + r * 74
        if 380 < tx < 700 and 900 < ty < 1100: continue
        k = eo(prog(t, 0.3 + i * 0.02, 0.35))
        put(b, mini_post(i, 64), lerp(W / 2, tx, k), lerp(1000, ty, k), scale=0.4 + 0.6 * k, alpha=k)
    put(b, counter_pill('', f'{n}', 'पोस्ट'), W / 2, 1380, scale=eback(prog(t, 0.4, 0.3)))
    return b, False

def r2(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 2.9, [(3.0, [bold('फिर भी', 92)]), (3.6, [bold('कोई', 92), accent('ruka nahi.', 104)])], y0=280)
    speed = 900
    phone_feed(b, t, speed, W / 2, 1010, blur=2)
    # thumb swiping up repeatedly
    ph = (t * 2.2) % 1
    put(b, hand(150), W / 2 + 230, 1150 - 260 * eio(ph), alpha=math.sin(ph * math.pi), rot=-10)
    put(b, counter_pill('♥', 0, 'लाइक्स'), 250, 700, scale=eback(prog(t, 3.5, 0.35)), rot=-6)
    put(b, counter_pill('↻', 0, 'शेयर'), 840, 760, scale=eback(prog(t, 3.75, 0.35)), rot=6)
    if t > 4.0:
        put(b, pill('स्क्रॉल… स्क्रॉल… स्क्रॉल…', 28, bg=DEEP, fg=YEL, path=PB), W / 2, 1300, scale=eback(prog(t, 4.0, 0.35)))
    return b, False

def r3(t):
    b = bg_light(t)
    headline(b, t, 5.3, [(5.4, [bold('स्पीड', 96, GREEN2), bold('AI की', 96)]), (7.1, [bold('बात', 96, GREEN2), accent('aapki.', 110)])], y0=280)
    # left: AI with lightning; right: owner with speech bubble
    p = eback(prog(t, 5.35, 0.45))
    lx, rx, y = 290, 790, 980
    put(b, ai_chip(230), lx, y + (1 - p) * 120, alpha=min(1, p * 2), rot=math.sin(t * 6) * 2)
    for i in range(3):
        ph = (t * 1.8 + i / 3) % 1
        put(b, bolt(70), lx - 140 + i * 110, y - 190 - ph * 60, alpha=math.sin(ph * math.pi) * p)
    put(b, pill('स्पीड', 30, bg=YEL, fg=DEEP, path=PB, dot=GREEN), lx, y + 190, alpha=p)
    q = eback(prog(t, 7.05, 0.45))
    if t > 7.0:
        put(b, owner_card('आप', 330, 410), rx, y + (1 - q) * 120, alpha=min(1, q * 2))
        put(b, bubble('“मेरी बात, मेरा अंदाज़”', 28), rx - 30, y - 290, scale=eback(prog(t, 7.4, 0.4)))
        put(b, pill('💬 बात', 30, bg=GREEN, fg=WHITE, path=PB) if False else pill('बात', 30, bg=GREEN, fg=WHITE, path=PB, dot=YEL), rx, y + 250, alpha=q)
    # plus sign
    if t > 7.0:
        put(b, text_img('+', 120, GREEN2, PB), W / 2, y, scale=eback(prog(t, 7.2, 0.35)))
    return b, False

def r4(t):
    b = bg_light(t, tint=(255, 253, 240))
    headline(b, t, 9.45, [(9.55, [bold('AI', 100, GREEN2), bold('टेक्स्ट', 100)]), (10.25, [accent('jaldi likhta hai', 92)])], y0=280)
    p = eback(prog(t, 9.45, 0.45))
    k = eio(prog(t, 9.7, 2.0))
    put(b, doc_card(k), W / 2 + 40, 1010 + (1 - p) * 100, alpha=min(1, p * 2))
    put(b, ai_chip(150), 220, 820, scale=p, rot=-8)
    sparkle(b, 300, 740, t, 9.9, 26)
    sparkle(b, 880, 1240, t, 10.4, 30, GREEN)
    if t > 11.1:
        put(b, pill('सिर्फ़ 5 सेकंड', 30, bg=DEEP, fg=YEL, path=PB), 820, 760, scale=eback(prog(t, 11.1, 0.35)), rot=6)
    return b, False

def r5(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 12.1, [(12.2, [bold('AI', 100, GREEN2), bold('इमेज', 100)]), (12.8, [accent('jaldi banata hai', 92)])], y0=280)
    p = eback(prog(t, 12.1, 0.5))
    put(b, phone_shot('21442f26', 330, 0.0), 250, 1010 + (1 - p) * 120, rot=-5, alpha=min(1, p * 2))
    for i in range(6):
        r, c = divmod(i, 2)
        t0 = 12.5 + i * 0.25
        if t > t0:
            k = prog(t, t0, 0.6)
            put(b, gen_tile(i, eio(k), 180), 640 + c * 220, 760 + r * 250, scale=eback(prog(t, t0, 0.3)))
    if t > 13.9:
        put(b, pill('✓ 6 डिज़ाइन तैयार', 28, bg=GREEN, fg=WHITE, path=PB), 750, 1360, scale=eback(prog(t, 13.9, 0.35)))
    return b, False

def r6(t):
    b = bg_light(t, tint=PALEY, glow=GREEN, glow2=YEL)
    headline(b, t, 14.85, [(14.95, [bold('क्या कहना है?', 96)]), (16.4, [bold('ये', 92), accent('aap', 110), bold('जानते हैं', 92)])], y0=280)
    p = eback(prog(t, 14.9, 0.5))
    put(b, owner_card('दुकान मालिक', 400, 500), W / 2, 1040 + math.sin(t * 2) * 6, alpha=min(1, p * 2), scale=0.9 + 0.1 * p)
    chips = [('आपकी कहानी', 15.2, -1), ('आपके कस्टमर', 15.6, 1), ('आपका ऑफ़र', 16.4, -1), ('आपकी भाषा', 16.8, 1), ('आपका भरोसा', 17.3, -1)]
    for i, (tx, t0, side) in enumerate(chips):
        if t > t0:
            a = t * 0.6 + i * 1.256
            cx = W / 2 + math.cos(a) * 380; cy = 1040 + math.sin(a) * 300
            put(b, pill(tx, 26, bg=[WHITE, YEL, GREEN][i % 3], fg=WHITE if i % 3 == 2 else DEEP, path=PB), cx, cy, scale=eback(prog(t, t0, 0.35)))
    if t > 17.7:
        put(b, heart_img(70, GREEN), W / 2 + 150, 820, scale=eback(prog(t, 17.7, 0.4)) * (1 + 0.08 * math.sin(t * 8)))
    return b, False

def r7(t):
    b = bg_light(t)
    if t < 21.75:
        headline(b, t, 18.85, [(18.95, [bold('बात आपकी', 92)]), (20.5, [bold('+', 92, GREEN2), bold('स्पीड AI की', 92)])], y0=280)
        y = 1000
        put(b, eq_card('आपकी बात', 'दिल से', YEL, DEEP), 230, y, scale=eback(prog(t, 19.2, 0.4)))
        if t > 20.5: put(b, text_img('+', 100, GREEN2, PB), 395, y, scale=eback(prog(t, 20.5, 0.3)))
        if t > 20.6: put(b, eq_card('AI स्पीड', '1 मिनट', GREEN, WHITE), 560, y, scale=eback(prog(t, 20.6, 0.4)))
        if t > 21.2: put(b, text_img('=', 100, GREEN2, PB), 725, y, scale=eback(prog(t, 21.2, 0.3)))
        if t > 21.35: put(b, eq_card('एंगेजमेंट', 'लाइक + शेयर', DEEP, YEL, w=250), 885, y, scale=eback(prog(t, 21.35, 0.4)))
    else:
        headline(b, t, 21.75, [(21.8, [bold('तब लोग', 92)]), (22.4, [accent('rukte hain!', 112)])], y0=280)
        # feed slows to a stop on one big post
        k = eio(prog(t, 21.8, 0.9))
        speed = lerp(900, 0, k)
        phone_feed(b, t if k < 1 else 22.7, speed, W / 2 - 150, 1020, w=400, h=780, blur=int(2 * (1 - k)))
        if t > 22.4:
            q = eback(prog(t, 22.4, 0.4))
            put(b, cached('bigpost', lambda: with_shadow(portrait_card('आपका ब्रांड', 'happy', 300, 380, bg1=YEL2, bg2=GREEN), blur=10, off=6, alpha=0.1)), W / 2 - 150, 1000, scale=q)
            put(b, hand(130), W / 2 + 40, 1190, alpha=prog(t, 22.5, 0.3))
        likes = int(lerp(0, 1240, eio(prog(t, 22.5, 1.3))))
        shares = int(lerp(0, 186, eio(prog(t, 22.7, 1.2))))
        if t > 22.5:
            put(b, counter_pill('♥', likes, 'लाइक्स', bg=GREEN, fg=WHITE), 830, 800, scale=eback(prog(t, 22.5, 0.3)))
            put(b, counter_pill('↻', shares, 'शेयर', bg=YEL), 830, 930, scale=eback(prog(t, 22.7, 0.3)))
            put(b, counter_pill('✓', int(shares / 6), 'इन्क्वायरी', bg=WHITE), 830, 1060, scale=eback(prog(t, 22.9, 0.3)))
        for i in range(5):
            ph = t - 22.6 - i * 0.2
            if ph > 0:
                kk = (ph % 1.2) / 1.2
                put(b, heart_img(40, GREEN if i % 2 else YEL), 300 + i * 50, 1200 - kk * 400, alpha=math.sin(kk * math.pi))
    return b, False

def r8(t):
    b = bg_light(t, tint=MINT)
    headline(b, t, 23.95, [(24.05, [bold('यही है', 96)]), (24.7, [bold('AI का', 92), accent('sahi use', 112)])], y0=280)
    q = eback(prog(t, 24.0, 0.5))
    put(b, phone_shot('173cd744', 330, 0.0), W / 2, 1020, scale=q, rot=-3 * (1 - q))
    for txt, t0, x, y, c in [('AI पोस्ट डिज़ाइन', 24.4, 230, 780, YEL), ('1-क्लिक FB + Insta', 24.7, 860, 900, WHITE), ('WhatsApp मार्केटिंग', 25.0, 230, 1230, GREEN)]:
        if t > t0:
            put(b, pill(txt, 26, bg=c, fg=WHITE if c == GREEN else DEEP, path=PB), x, y + math.sin(t * 3 + x) * 6, scale=eback(prog(t, t0, 0.35)))
    if t > 25.3:
        put(b, badge('✓', 'सही उपयोग', 95, bg=GREEN, fg=WHITE), 850, 1250, scale=eback(prog(t, 25.3, 0.4), 2.2), rot=-8)
    return b, False

def r9(t):
    b = bg_light(t, glow=GREEN, glow2=YEL)
    q = eback(prog(t, 26.35, 0.5))
    put(b, logo(150), W / 2, 520, scale=0.7 + 0.3 * q, alpha=min(1, q * 2))
    put(b, text_img('आपकी बात  +  हमारी AI स्पीड', 34, GREEN2, PB), W / 2, 640, alpha=prog(t, 26.45, 0.3))
    k = eback(prog(t, 26.5, 0.45))
    pulse = 1 + 0.05 * math.sin(max(0, t - 26.9) * 9) * (t > 26.9)
    tap = 1 - 0.08 * math.sin(math.pi * prog(t, 26.85, 0.25))
    put(b, follow_btn(t > 26.95), W / 2, 820, scale=k * pulse * tap)
    if t > 26.65:
        hp = eo(prog(t, 26.65, 0.2))
        put(b, cached('cursor', cursor_img), W / 2 + 180 - 40 * hp, 900 + 60 * (1 - hp), alpha=hp)
    put(b, text_img('अधिक जानकारी के लिए', 40, DEEP, PB), W / 2, 1060, alpha=prog(t, 26.7, 0.3))
    put(b, phone_pill(), W / 2, 1180, scale=eback(prog(t, 26.75, 0.45)))
    return b, False

def thumbnail():
    def mk():
        b = bg_light(0.5)
        put(b, cached('tg6', lambda: outline_text('AI', 520, GREEN)), W / 2, 1050, alpha=0.08)
        put(b, pill('बिज़नेस ओनर्स ध्यान दें!', 40, bg=DEEP, fg=YEL, path=PB, padx=36, pady=16), W / 2, 300)
        put(b, line_img([bold('AI से', 92), bold('100', 106, GREEN2), bold('पोस्ट…', 92)]), W / 2, 470)
        put(b, line_img([bold('फिर भी कोई', 82), accent('nahi ruka?', 94, GREEN2)]), W / 2, 605)
        for i in range(24):
            r, c = divmod(i, 6)
            put(b, mini_post(i, 90), 170 + c * 148, 820 + r * 130, alpha=0.55, rot=(i % 3 - 1) * 4)
        put(b, ai_chip(230), W / 2 - 240, 1180, rot=-6)
        put(b, owner_card('आप', 330, 410), W / 2 + 230, 1130, )
        put(b, text_img('+', 130, GREEN2, PB), W / 2, 1160)
        put(b, pill('सही उपयोग जानें  →', 38, bg=YEL, fg=DEEP, path=PB, padx=34, pady=14), W / 2, 1440)
        put(b, logo(110), W / 2, 1620)
        put(b, phone_pill(), W / 2, 1755, scale=0.85)
        return b.convert('RGB')
    return cached('thumb6', mk)

EM = [(0, 20), (2.9, 8), (4.2, 3), (5.3, 3), (7.1, 30), (9.45, 35), (12.1, 40), (14.85, 45), (16.7, 60), (19.0, 70), (21.35, 80), (22.5, 95), (24.0, 97), (30, 99)]
def emeter(t):
    for (a, va), (b2, vb) in zip(EM, EM[1:]):
        if a <= t <= b2: return lerp(va, vb, eio((t - a) / max(0.01, min(0.8, b2 - a))))
    return 99
def topbar(base, t, dark=False):
    fg = DEEP; bgc = WHITE
    left = pill('SHRI TECH  ·  ☎ 9993615146', 24, bg=bgc, fg=fg, path=FB, padx=20, pady=10, dot=GREEN)
    put(base, left, 40 + left.width / 2 - 14, 120)
    v = emeter(t)
    def mk():
        w, h = 330, 52
        p = Pad(w, h)
        p.rect((0, 0, w - 1, h - 1), h // 2, fill=bgc + (255,))
        p.text((20, h / 2), 'एंगेजमेंट', 21, fg, FB, anchor='lm')
        x0, x1 = 150, 262
        p.rect((x0, h / 2 - 4, x1, h / 2 + 4), 4, fill=(fg + (50,)))
        p.rect((x0, h / 2 - 4, x0 + (x1 - x0) * v / 100, h / 2 + 4), 4, fill=(GREEN if v > 25 else (234, 179, 8)) + (255,))
        p.text((w - 18, h / 2), f'{int(v)}%', 21, fg, FB, anchor='rm')
        return with_shadow(p.img(), blur=12, off=6, alpha=0.18)
    im = cached(('emeter', int(v)), mk)
    put(base, im, W - 40 - im.width / 2 + 14, 120)
L.topbar = topbar

L.SC = SC
L.END = END
L.SCENES = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
L.thumbnail = thumbnail
L.BR_Y, L.PH_Y = 1655, 1765
L.MODES = ['up', 'blur', 'left', 'color', 'pop', 'right', 'up', 'blur', 'pop']
L.PMODES = ['type', 'ring', 'glow', 'up', 'ring', 'left', 'glow', 'ring', 'glow']
# keep floating dots out of the subtitle + brand area
L.PARTS = [p for p in L.PARTS]
_orig_particles = L.particles
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
            if ts == 'thumb': thumbnail().save('/home/claude/r6/out/ShriTech_AI_SahiUse_Thumbnail.jpg', quality=92)
            else: L.frame(float(ts)).save(f'/home/claude/r6/st/st_{ts}.jpg', quality=85)
    else:
        L.render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
