"""8 different layouts + tribute. Each takes (img, p, L) where p = post dict and L = language block (hi/en)."""
from eng import *

def fonts(lang, style):
    """display font + script font per post style (varies across posts)"""
    if lang == 'hi':
        disp = ['rozha', 'yatra', 'eczar', 'khand', 'martel', 'laila', 'amita', 'teko'][style % 8]
        return disp, 'amita' if disp != 'amita' else 'kalam', 'baloo', 'mukta'
    disp = ['play', 'oswald', 'bebas', 'mont', 'playi', 'oswald', 'play', 'bebas'][style % 8]
    return disp, ['vibes', 'dance', 'playi', 'vibes'][style % 4], 'mont', 'mont'

def wish_block(img, cx, y, L, lang, style, maxw=900, size=74, anchor='m', script_first=True):
    disp, scr, body, bold = fonts(lang, style)
    lines = wrap(L['wish'], size, disp, maxw)
    if len(lines) > 2: size = int(size * 0.8); lines = wrap(L['wish'], size, disp, maxw)
    a = {'m': 'mm', 'l': 'lm', 'r': 'rm'}[anchor]
    for ln_ in lines:
        GT(img, (cx, y), ln_, size, (21, 128, 61), (6, 52, 28), disp, a, maxw=maxw, shadow=(GOLD, 0.25)); y += size * 1.08
    if L.get('wish2'):
        s2 = 38 if lang == 'hi' else 44
        f2 = scr
        for ln_ in wrap(L['wish2'], s2, f2, maxw):
            GT(img, (cx, y + 4), ln_, s2, (234, 179, 8), (161, 98, 7), f2, a, maxw=maxw); y += s2 * 1.25
    return y

def head_block(img, x, y, L, lang, style, maxw, size=46, color=INK, anchor='l'):
    disp, scr, body, bold = fonts(lang, style + 3)
    a = {'m': 'mm', 'l': 'lm', 'r': 'rm'}[anchor]
    for ln_ in wrap(L['head'], size, bold, maxw):
        GT(img, (x, y), ln_, size, (21, 128, 61), (6, 52, 28), bold, a, maxw=maxw); y += size * 1.18
    return y

def problem_solution(img, box, L, lang, vertical=False):
    x0, y0, x1, y1 = box
    pt, st = ('समस्या', 'Shri Tech से हल') if lang == 'hi' else ('The problem', 'The Shri Tech fix')
    if vertical:
        hm = (y1 - y0 - 24) / 2
        bubble(img, (x0, y0, x1, y0 + hm), L['prob'], lang, 'bl', 'y', 23, title=pt)
        bubble(img, (x0, y0 + hm + 24, x1, y1), L['sol'], lang, 'tr', 'g', 23, title=st)
    else:
        wm = (x1 - x0 - 50) / 2
        bubble(img, (x0, y0, x0 + wm, y1), L['prob'], lang, 'bl', 'y', 23, title=pt)
        bubble(img, (x0 + wm + 50, y0, x1, y1), L['sol'], lang, 'br', 'g', 23, title=st)
        cx = x0 + wm + 25; cy = (y0 + y1) / 2
        gellipse(img, cx, cy, 24, 24, (254, 240, 138), (234, 179, 8), 0.3)
        ImageDraw.Draw(img).polygon(P((cx - 8, cy - 11), (cx + 11, cy), (cx - 8, cy + 11)), fill=DEEP)

# ---------------- A: photo left, wishes right, problem->solution bottom ----------------
def lay_A(img, p, L, lang):
    st = p['n']
    photo(img, p['ph'], (48, 124, 500, 760), 'round', 40)
    label_pill(img, 72, 690, L['tag'], lang, 'g', 20)
    paste_art(img, p['art'], (530, 116, 1032, 360))
    y = wish_block(img, 781, 410, L, lang, st, maxw=480, size=64)
    head_block(img, 781, max(y + 30, 620), L, lang, st, 480, 32, anchor='m')
    problem_solution(img, (48, 800, 1032, 1040), L, lang)
    chips_row(img, 540, 1080, L['feats'], lang, 'w', 21)
    rrect(img, (48, 1150, 1032, 1152), 1, fill=(187, 247, 208))

# ---------------- B: festival hero on top, business card below with circle photo ----------------
def lay_B(img, p, L, lang):
    st = p['n']
    paste_art(img, p['art'], (90, 110, 990, 380))
    y = wish_block(img, 540, 430, L, lang, st, maxw=960, size=70)
    y0 = max(y + 10, 560)
    card_ = (48, y0, 1032, 1190)
    shadow(img, card_, 32, blur=16, alpha=0.18, off=8, color=DEEP)
    grrect(img, card_, 32, (255, 255, 255), (240, 253, 244), 0)
    rrect(img, card_, 32, outline=(187, 247, 208), width=2)
    ph = 290
    photo(img, p['ph'], (74, y0 + 26, 74 + ph, y0 + 26 + ph), 'circle')
    x = 74 + ph + 30; mw = 1032 - 26 - x
    yy = head_block(img, x, y0 + 60, L, lang, st, mw, 38)
    checks(img, x, yy + 20, L['feats'], lang, 26, 50, mw)
    problem_solution(img, (70, y0 + ph + 50, 1010, 1170), L, lang)

# ---------------- C: business on top, festival band at the bottom ----------------
def lay_C(img, p, L, lang):
    st = p['n']
    photo(img, p['ph'], (560, 120, 1032, 600), 'arch')
    label_pill(img, 48, 132, L['tag'], lang, 'g', 21)
    yy = head_block(img, 48, 220, L, lang, st, 490, 50)
    yy = checks(img, 48, yy + 26, L['feats'], lang, 24, 50, 490)
    problem_solution(img, (48, 628, 1032, 830), L, lang)
    band = (48, 860, 1032, 1190)
    shadow(img, band, 34, blur=16, alpha=0.18, off=8, color=GOLD)
    grrect(img, band, 34, (255, 252, 232), (254, 236, 150), 0.25)
    rrect(img, band, 34, outline=YEL, width=3)
    paste_art(img, p['art'], (70, 880, 470, 1170))
    wish_block(img, 760, 960, L, lang, st, maxw=520, size=58)

# ---------------- D: big diagonal photo, wishes on the side ----------------
def lay_D(img, p, L, lang):
    st = p['n']
    photo(img, p['ph'], (0, 104, 700, 690), 'diag', frame=False, fade=True)
    gshape(img, lambda d: d.polygon(P((546, 104), (566, 104), (436, 690), (416, 690)), fill=255), (254, 240, 138), (234, 179, 8), 0.3)
    f = 'mukta' if lang == 'hi' else 'mont'
    yy = 560
    for ln_ in wrap(L['head'], 32, f, 440):
        T(img, (60, yy), ln_, 32, WHITE, f, 'lm'); yy += 40
    paste_art(img, p['art'], (640, 112, 1040, 360))
    wish_block(img, 1032, 420, L, lang, st, maxw=420, size=58, anchor='r')
    problem_solution(img, (48, 730, 1032, 960), L, lang)
    chips_row(img, 540, 1000, L['feats'], lang, 'g', 21)
    label_pill(img, 540, 1080, L['tag'], lang, 'y', 22, 'm')

# ---------------- E: centre circle photo with festival art around ----------------
def lay_E(img, p, L, lang):
    st = p['n']
    y = wish_block(img, 540, 150, L, lang, st, maxw=960, size=70)
    r = 190; cy = y + r + 10
    gellipse(img, 540, cy, r + 24, r + 24, (254, 240, 138), (217, 159, 6), 0.35)
    photo(img, p['ph'], (540 - r, cy - r, 540 + r, cy + r), 'circle')
    paste_art(img, p['art'], (40, cy - 170, 320, cy + 170))
    paste_art(img, p['art'], (760, cy - 170, 1040, cy + 170))
    label_pill(img, 540, cy + r + 4, L['tag'], lang, 'g', 22, 'm')
    y2 = cy + r + 66
    problem_solution(img, (48, y2, 1032, 1110), L, lang)
    chips_row(img, 540, 1130, L['feats'], lang, 'w', 23)

# ---------------- F: a real person with a problem -> solved by Shri Tech ----------------
def lay_F(img, p, L, lang):
    st = p['n']
    paste_art(img, p['art'], (40, 108, 470, 390))
    wish_block(img, 1032, 190, L, lang, st, maxw=560, size=72, anchor='r')
    photo(img, p.get('ph_worry', 'worried'), (48, 410, 380, 742), 'circle')
    pt = 'समस्या' if lang == 'hi' else 'The problem'
    bubble(img, (406, 440, 1032, 700), L['prob'], lang, 'bl', 'y', 32, title=pt)
    photo(img, p['ph'], (700, 770, 1032, 1102), 'circle')
    st_ = 'Shri Tech से हल' if lang == 'hi' else 'The Shri Tech fix'
    bubble(img, (48, 770, 676, 1010), L['sol'], lang, 'br', 'g', 32, title=st_)
    chips_row(img, 362, 1040, L['feats'][:2], lang, 'w', 24, maxw=640)
    label_pill(img, 362, 1112, L['tag'], lang, 'y', 24, 'm')

# ---------------- G: headline + phone showing the festival post made with Shri Tech ----------------
def lay_G(img, p, L, lang):
    st = p['n']
    label_pill(img, 48, 126, L['tag'], lang, 'g', 22)
    yy = head_block(img, 48, 230, L, lang, st, 530, 54)
    yy = checks(img, 48, yy + 26, L['feats'], lang, 28, 56, 530)
    problem_solution(img, (48, max(yy + 20, 640), 580, 1186), L, lang, vertical=True)
    x, y, w, h = 612, 124, 420, 1062
    shadow(img, (x, y, x + w, y + h), 50, blur=24, alpha=0.3, off=14, color=DEEP)
    grrect(img, (x, y, x + w, y + h), 50, (40, 52, 44), (10, 18, 13), 0.15)
    sx0, sy0, sx1, sy1 = x + 14, y + 14, x + w - 14, y + h - 14
    grrect(img, (sx0, sy0, sx1, sy1), 40, (255, 253, 240), (220, 252, 231), 0)
    rrect(img, (x + w / 2 - 50, y + 24, x + w / 2 + 50, y + 38), 7, fill=(10, 18, 13))
    wordmark(img, sx0 + 24, sy0 + 56, 22)
    paste_art(img, p['art'], (sx0 + 20, sy0 + 90, sx1 - 20, sy0 + 380))
    wish_block(img, (sx0 + sx1) / 2, sy0 + 430, dict(wish=L['wish']), lang, st, maxw=sx1 - sx0 - 40, size=42)
    photo(img, p['ph'], (sx0 + 22, sy0 + 590, sx1 - 22, sy1 - 96), 'round', 24, frame=False)
    for i, (lab, col) in enumerate([('f', (59, 89, 152)), ('ig', (214, 41, 118)), ('wa', (37, 211, 102))]):
        gx = sx0 + 80 + i * 116
        gellipse(img, gx, sy1 - 48, 26, 26, lighten(col, 0.2), darken(col, 0.2), 0.3)
        T(img, (gx, sy1 - 48), lab, 20, WHITE, 'pb', 'mm')

# ---------------- H: festival scene background + frosted glass card ----------------
def lay_H(img, p, L, lang):
    st = p['n']
    paste_art(img, p['art'], (40, 104, 1040, 520))
    card_ = (48, 470, 1032, 1190)
    lay = Image.new('L', img.size, 0); ImageDraw.Draw(lay).rounded_rectangle(P(card_[:2], card_[2:]), 40 * S, fill=200)
    shadow(img, card_, 40, blur=20, alpha=0.2, off=10, color=DEEP)
    img.paste(Image.new('RGB', img.size, WHITE), (0, 0), lay)
    rrect(img, card_, 40, outline=(253, 230, 138), width=3)
    y = wish_block(img, 540, 540, L, lang, st, maxw=900, size=66)
    photo(img, p['ph'], (76, y + 20, 436, y + 300), 'round', 30)
    x = 466
    yy = head_block(img, x, y + 50, L, lang, st, 540, 34)
    checks(img, x, yy + 16, L['feats'], lang, 22, 42, 540)
    problem_solution(img, (76, y + 330, 1004, 1170), L, lang)

LAYOUTS = dict(A=lay_A, B=lay_B, C=lay_C, D=lay_D, E=lay_E, F=lay_F, G=lay_G, H=lay_H)

# ---------------- Tribute (no selling) ----------------
def lay_T(img, p, L, lang):
    st = p['n']
    if p.get('ph'):
        photo(img, p['ph'], (48, 120, 1032, 560), 'round', 40, fade=True)
        paste_art(img, p['art'], (600, 140, 1010, 540))
    else:
        paste_art(img, p['art'], (60, 112, 1020, 560))
    y = wish_block(img, 540, 640, L, lang, st, maxw=960, size=72)
    box = (90, y + 30, 990, 1180)
    shadow(img, box, 30, blur=16, alpha=0.18, off=8, color=GOLD)
    grrect(img, box, 30, (255, 255, 255), (254, 246, 200), 0)
    rrect(img, box, 30, outline=YEL, width=3)
    disp, scr, body, bold = fonts(lang, st)
    yy = (box[1] + box[3]) / 2 - 31 * (len(L['quote']) - 1)
    for q in L['quote']:
        T(img, (540, yy), q, 42, INK, 'playi' if lang == 'en' else 'tiroi', 'mm', maxw=840); yy += 62
