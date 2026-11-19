"""Shri Tech festival series kit - light theme only. One font family (Poppins): PB = headings, PBD = labels, PM = normal."""
import sys; sys.path.insert(0, '/home/claude/posters')
from v3 import *

INK = DEEP; SUB = (55, 80, 64); LINEC = (134, 199, 157); CARD_OL = (209, 250, 223); PALE = (254, 249, 195); HL = (254, 240, 138)
T = LIGHT
M = 48  # side margin

def fit(txt, size, path, maxw):
    while size > 12 and tw(txt, size, path) > maxw: size -= 1
    return size

def rich_w(segs):
    t = 0
    for s in segs:
        t += wordmark_w(s[1]) if s[0] == '@ST' else tw(s[0], s[1], s[3])
    return t + 10 * (len(segs) - 1)

def rich2(img, x, cy, segs, anchor='m', dark=False):
    """Like rich() but '@ST' renders the Shri Tech wordmark."""
    total = rich_w(segs)
    x = x - total / 2 if anchor == 'm' else (x - total if anchor == 'r' else x)
    for s in segs:
        if s[0] == '@ST':
            if dark: wordmark(img, x, cy, s[1], shri=WHITE, tech=LGREEN)
            else: wordmark(img, x, cy, s[1])
            x += wordmark_w(s[1]) + 10
        else:
            text(img, (x, cy), s[0], s[1], s[2], s[3], 'lm'); x += tw(s[0], s[1], s[3]) + 10

def segs_fit(segs, maxw):
    while rich_w(segs) > maxw and segs[0][1] > 14:
        segs = [(s[0], s[1] - 1) + tuple(s[2:]) for s in segs]
    return segs

def parse(txt, size, color=INK, accent=GREEN, font=PB):
    """'हर दुकान के लिए *WhatsApp मार्केटिंग*' -> segments; *..* = accent colour; {ST} = wordmark."""
    out = []
    import re
    for part in re.split(r'(\*[^*]+\*|\{ST\})', txt):
        if not part.strip(): continue
        if part == '{ST}': out.append(('@ST', size))
        elif part.startswith('*'): out.append((part[1:-1].strip(), size, accent, font))
        else: out.append((part.strip(), size, color, font))
    return out

# ---------------- page frame ----------------
def base():
    img = Image.new('RGB', (W, H), WHITE)
    glow(img, 540, 250, 340, (254, 243, 170), 0.55)
    glow(img, 540, 880, 520, (220, 252, 231), 0.55)
    return img

def header(img):
    logo(img, M, 34, 44, dark=False)
    num_pill(img, 1080 - M, 36, False)

def greeting(img, title, line2, y_title=468, y2=534):
    s = fit(title, 80, PB, 980)
    text(img, (540, y_title), title, s, INK, PB, 'mm')
    if line2:
        s2 = fit(line2, 42, PB, 900)
        w = tw(line2, s2, PB)
        rrect(img, (540 - w / 2 - 18, y2 - 8, 540 + w / 2 + 18, y2 + 22), 10, fill=HL)
        text(img, (540, y2), line2, s2, GREEN, PB, 'mm')

def story_pill(img, txt, y=584):
    segs = segs_fit(parse(txt, 27, WHITE, YEL), 900)
    w = rich_w(segs) + 64
    rrect(img, (540 - w / 2, y, 540 + w / 2, y + 52), 26, fill=GREEN)
    rich2(img, 540, y + 25, segs)

def ribbon(img, line, chips, y=1098):
    rrect(img, (M, y, 1080 - M, y + 92), 22, fill=PALE, outline=YEL, width=3)
    segs = segs_fit(parse(line, 24), 940)
    rich2(img, 540, y + 27, segs)
    ws = [tw(c, 18, PBD) + 26 for c in chips]
    while sum(ws) + 10 * (len(ws) - 1) > 950: chips = chips[:-1]; ws = ws[:-1]
    x = 540 - (sum(ws) + 10 * (len(ws) - 1)) / 2
    for c, w in zip(chips, ws):
        rrect(img, (x, y + 48, x + w, y + 75), 13, fill=WHITE, outline=LINEC, width=2)
        text(img, (x + w / 2, y + 61), c, 18, INK, PBD, 'mm')
        x += w + 10

def cta(img, line, y=1214):
    rrect(img, (0, y, 1080, 1350), 0, fill=DEEP)
    s = fit(line, 25, PBD, 640)
    text(img, (M, y + 40), line, s, (187, 247, 208), PBD, 'lm')
    phone_icon(img, M + 26, y + 96, 44, YEL)
    text(img, (M + 64, y + 96), '9993615146', 60, YEL, PB, 'lm')
    size = 38; lw = logo_width(size)
    logo(img, 1080 - M - lw, y + 26, size, dark=True)
    text(img, (1080 - M, y + 104), 'Shri Balaji Digital Services', 20, WHITE, PM, 'rm')

# ---------------- extra icons ----------------
def ic_photo(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 34, cy - 28), (cx + 34, cy + 28)), 8 * S, fill=bg, outline=c, width=5 * S)
    d.polygon(P((cx - 28, cy + 22), (cx - 8, cy - 2), (cx + 6, cy + 12), (cx + 14, cy + 4), (cx + 28, cy + 22)), fill=c)
    d.ellipse(P((cx + 8, cy - 20), (cx + 22, cy - 6)), fill=hi)

def ic_shield(img, cx, cy, c, hi, bg):
    d = L(img)
    pts = [(cx, cy - 36), (cx + 30, cy - 24), (cx + 26, cy + 10), (cx, cy + 36), (cx - 26, cy + 10), (cx - 30, cy - 24)]
    d.polygon(P(*pts), fill=bg); d.line(P(*(pts + [pts[0]])), fill=c, width=5 * S, joint='curve')
    d.line(P((cx - 12, cy), (cx - 2, cy + 10), (cx + 14, cy - 10)), fill=hi, width=6 * S)

def ic_clock(img, cx, cy, c, hi, bg):
    d = L(img)
    d.ellipse(P((cx - 34, cy - 34), (cx + 34, cy + 34)), fill=bg, outline=c, width=5 * S)
    d.line(P((cx, cy - 20), (cx, cy), (cx + 16, cy + 10)), fill=c, width=5 * S)
    d.ellipse(P((cx - 5, cy - 5), (cx + 5, cy + 5)), fill=hi)

def ic_eye(img, cx, cy, c, hi, bg):
    d = L(img)
    top = bez((cx - 38, cy), (cx, cy - 40), (cx + 38, cy), 20); bot = bez((cx + 38, cy), (cx, cy + 40), (cx - 38, cy), 20)
    d.line(P(*(top + bot)), fill=c, width=5 * S, joint='curve')
    d.ellipse(P((cx - 13, cy - 13), (cx + 13, cy + 13)), fill=c); d.ellipse(P((cx - 4, cy - 8), (cx + 4, cy)), fill=hi)

def ic_heart(img, cx, cy, c, hi, bg):
    heart_shape(img, cx, cy + 4, 34, c)
    sparkle(img, cx + 26, cy - 24, 9, hi)

def heart_shape(img, cx, cy, s, col):
    d = L(img)
    d.ellipse(P((cx - s, cy - s * 0.75), (cx, cy + s * 0.2)), fill=col)
    d.ellipse(P((cx, cy - s * 0.75), (cx + s, cy + s * 0.2)), fill=col)
    d.polygon(P((cx - s * 0.97, cy - s * 0.12), (cx + s * 0.97, cy - s * 0.12), (cx, cy + s * 0.95)), fill=col)

def ic_palette(img, cx, cy, c, hi, bg):
    d = L(img)
    d.ellipse(P((cx - 36, cy - 30), (cx + 36, cy + 30)), fill=bg, outline=c, width=5 * S)
    for (x, y, col) in [(cx - 16, cy - 10, GREEN), (cx + 2, cy - 16, hi), (cx + 18, cy - 4, DEEP), (cx - 10, cy + 10, LGREEN)]:
        d.ellipse(P((x - 7, y - 7), (x + 7, y + 7)), fill=col)

def ic_upload(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 34, cy + 6), (cx + 34, cy + 32)), 8 * S, outline=c, width=5 * S)
    d.rectangle(P((cx - 20, cy + 2), (cx + 20, cy + 12)), fill=bg)
    d.line(P((cx, cy + 16), (cx, cy - 30)), fill=c, width=6 * S)
    d.polygon(P((cx - 16, cy - 14), (cx, cy - 36), (cx + 16, cy - 14)), fill=c)
    d.ellipse(P((cx + 18, cy - 30), (cx + 32, cy - 16)), fill=hi)

def ic_check(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 32, cy - 32), (cx + 32, cy + 32)), 12 * S, fill=bg, outline=c, width=5 * S)
    d.line(P((cx - 16, cy + 2), (cx - 4, cy + 14), (cx + 18, cy - 12)), fill=c, width=7 * S)

def ic_chat(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 38, cy - 30), (cx + 14, cy + 6)), 12 * S, fill=c)
    d.polygon(P((cx - 28, cy + 4), (cx - 34, cy + 18), (cx - 16, cy + 4)), fill=c)
    d.rounded_rectangle(P((cx - 6, cy - 6), (cx + 38, cy + 26)), 12 * S, fill=bg, outline=c, width=4 * S)
    for x in (cx + 6, cx + 16, cx + 26): d.ellipse(P((x - 3, cy + 7), (x + 3, cy + 13)), fill=hi)

def ic_users(img, cx, cy, c, hi, bg):
    d = L(img)
    for dx, col, s in [(-16, c, 1.0), (16, hi, 0.85)]:
        x = cx + dx
        d.ellipse(P((x - 11 * s, cy - 28 * s), (x + 11 * s, cy - 6 * s)), fill=col)
        d.chord(P((x - 22 * s, cy - 2), (x + 22 * s, cy + 40 * s)), 180, 360, fill=col)

def ic_store(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rectangle(P((cx - 30, cy - 6), (cx + 30, cy + 32)), fill=bg, outline=c, width=5 * S)
    for i in range(4):
        x0 = cx - 36 + i * 18
        d.chord(P((x0, cy - 34), (x0 + 18, cy - 2)), 0, 180, fill=hi if i % 2 else c)
    d.rectangle(P((cx - 36, cy - 34), (cx + 36, cy - 18)), fill=c)
    d.rectangle(P((cx - 8, cy + 8), (cx + 8, cy + 32)), fill=c)

def ic_bell(img, cx, cy, c, hi, bg):
    d = L(img)
    d.chord(P((cx - 26, cy - 30), (cx + 26, cy + 30)), 180, 360, fill=c)
    d.rectangle(P((cx - 26, cy - 1), (cx + 26, cy + 14)), fill=c)
    d.rounded_rectangle(P((cx - 34, cy + 12), (cx + 34, cy + 20)), 4 * S, fill=c)
    d.ellipse(P((cx - 7, cy + 20), (cx + 7, cy + 32)), fill=hi)

def ic_star(img, cx, cy, c, hi, bg):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; r = 34 if i % 2 == 0 else 14
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    L(img).polygon(P(*pts), fill=hi); L(img).line(P(*(pts + [pts[0]])), fill=c, width=3 * S)

def ic_grow(img, cx, cy, c, hi, bg):
    d = L(img)
    d.line(P((cx - 34, cy + 24), (cx - 10, cy), (cx + 6, cy + 12), (cx + 32, cy - 22)), fill=c, width=6 * S, joint='curve')
    d.polygon(P((cx + 36, cy - 30), (cx + 16, cy - 26), (cx + 32, cy - 10)), fill=c)
    d.line(P((cx - 36, cy + 34), (cx + 36, cy + 34)), fill=hi, width=5 * S)

ICONS.update(photo=ic_photo, shield=ic_shield, clock=ic_clock, eye=ic_eye, heart=ic_heart, palette=ic_palette,
             upload=ic_upload, check=ic_check, chat=ic_chat, users=ic_users, store=ic_store, bell=ic_bell,
             star=ic_star, grow=ic_grow)

def node(img, cx, cy, r, ic, num=None):
    circ_node(img, cx, cy, r, T, ic, num=num)

# ---------------- vector phone ----------------
def phone(img, x, y, w, h, kind='poster', label='ऑफर', badge=None):
    d = L(img)
    shadow(img, (x, y, x + w, y + h), 34, blur=20, alpha=0.22, off=10, color=DEEP)
    d.rounded_rectangle(P((x, y), (x + w, y + h)), 34 * S, fill=(18, 30, 22))
    sx0, sy0, sx1, sy1 = x + 10, y + 10, x + w - 10, y + h - 10
    d.rounded_rectangle(P((sx0, sy0), (sx1, sy1)), 26 * S, fill=(240, 253, 244))
    d.rounded_rectangle(P((sx0, sy0), (sx1, sy0 + 60)), 26 * S, fill=WHITE)
    d.rectangle(P((sx0, sy0 + 32), (sx1, sy0 + 60)), fill=WHITE)
    wordmark(img, sx0 + 16, sy0 + 38, 16)
    bx0, bx1 = sx0 + 12, sx1 - 12
    y0 = sy0 + 74
    if kind in ('poster', 'wa'):
        ph = (bx1 - bx0) * 0.78
        d.rounded_rectangle(P((bx0, y0), (bx1, y0 + ph)), 12 * S, fill=PALE)
        c = ((bx0 + bx1) / 2, y0 + ph * 0.42)
        sparkle(img, c[0], c[1], 26, YEL); sparkle(img, c[0] + 30, c[1] - 22, 10, GREEN)
        text(img, (c[0], y0 + ph - 30), label, fit(label, 16, PB, bx1 - bx0 - 20), INK, PB, 'mm')
        y0 += ph + 12
        rows = [('Facebook', GREEN), ('Instagram', YEL), ('WhatsApp', LGREEN)] if kind == 'poster' else \
               [('भेजा गया', GREEN), ('पहुँचा', YEL), ('पढ़ा गया', LGREEN)]
        for lab, col in rows:
            if y0 + 34 > sy1 - 8: break
            d.rounded_rectangle(P((bx0, y0), (bx1, y0 + 32)), 10 * S, fill=WHITE)
            d.ellipse(P((bx0 + 8, y0 + 7), (bx0 + 26, y0 + 25)), fill=col)
            text(img, (bx0 + 34, y0 + 16), lab, 14, INK, PBD, 'lm')
            check(img, bx1 - 18, y0 + 16, 9, GREEN, WHITE)
            y0 += 40
    elif kind == 'chat':
        msgs = [('l', 'नमस्ते! ऑफर की जानकारी?'), ('r', 'जी ज़रूर, अभी भेजते हैं'), ('l', 'धन्यवाद!'), ('r', 'आपका स्वागत है')]
        for side, m_ in msgs:
            s = 14; wv = min(tw(m_, s, PM) + 24, bx1 - bx0 - 20)
            if side == 'l':
                d.rounded_rectangle(P((bx0, y0), (bx0 + wv, y0 + 36)), 12 * S, fill=WHITE)
                text(img, (bx0 + 12, y0 + 18), m_, s, INK, PM, 'lm')
            else:
                d.rounded_rectangle(P((bx1 - wv, y0), (bx1, y0 + 36)), 12 * S, fill=(187, 247, 208))
                text(img, (bx1 - 12, y0 + 18), m_, s, INK, PM, 'rm')
            y0 += 48
        d.rounded_rectangle(P((bx0, sy1 - 52), (bx1, sy1 - 14)), 19 * S, fill=WHITE, outline=CARD_OL, width=2 * S)
        d.ellipse(P((bx1 - 34, sy1 - 48), (bx1 - 4, sy1 - 18)), fill=GREEN)
    elif kind == 'dash':
        for i in range(2):
            xx = bx0 + i * ((bx1 - bx0) / 2 + 4)
            d.rounded_rectangle(P((xx, y0), (xx + (bx1 - bx0) / 2 - 4, y0 + 56)), 10 * S, fill=WHITE)
            d.rounded_rectangle(P((xx + 10, y0 + 12), (xx + 50, y0 + 22)), 4 * S, fill=LINEC)
            d.rounded_rectangle(P((xx + 10, y0 + 32), (xx + 70, y0 + 44)), 4 * S, fill=GREEN if i == 0 else YEL)
        y0 += 70
        d.rounded_rectangle(P((bx0, y0), (bx1, y0 + 120)), 10 * S, fill=WHITE)
        for i, hh in enumerate((30, 50, 22, 70, 44, 86, 60)):
            xx = bx0 + 14 + i * ((bx1 - bx0 - 28) / 7)
            d.rounded_rectangle(P((xx, y0 + 108 - hh), (xx + 14, y0 + 108)), 4 * S, fill=GREEN if i != 5 else YEL)
        y0 += 132
        for i in range(2):
            d.rounded_rectangle(P((bx0, y0), (bx1, y0 + 30)), 8 * S, fill=WHITE)
            d.rounded_rectangle(P((bx0 + 10, y0 + 11), (bx0 + 110, y0 + 19)), 4 * S, fill=LINEC)
            check(img, bx1 - 16, y0 + 15, 8, GREEN, WHITE)
            y0 += 38
    if badge:
        bw = tw(badge, 16, PB) + 28
        rrect(img, (x + w / 2 - bw / 2, y + h - 22, x + w / 2 + bw / 2, y + h + 10), 16, fill=YEL)
        text(img, (x + w / 2, y + h - 6), badge, 16, INK, PB, 'mm')

# ---------------- diagrams (zone y 664..1080) ----------------
def heading(img, txt, y=690, x=540, anchor='m', size=30):
    segs = segs_fit(parse(txt, size), 980 if anchor == 'm' else 690)
    rich2(img, x, y, segs, anchor)

def dg_hub(img, d):
    """phone centre + 4 nodes. d: label, nodes=[(icon,t1,t2)x4], kind"""
    top = 664; px, pw, ph = 540 - 120, 240, 410
    nodes = [(170, top + 70), (170, top + 290), (910, top + 70), (910, top + 290)]
    for (nx, ny) in nodes:
        side = px if nx < 540 else px + pw
        sx = nx + (52 if nx < 540 else -52)
        ty = top + 140 if ny < top + 200 else top + 330
        dashed(img, bez((sx, ny), ((sx + side) / 2, ny), (side, ty)), LINEC, w=3, dash=10, gap=9)
        L(img).ellipse(P((side - 7, ty - 7), (side + 7, ty + 7)), fill=GREEN)
    phone(img, px, top, pw, ph, d.get('kind', 'poster'), d.get('label', 'ऑफर'))
    for (nx, ny), (ic, a, b) in zip(nodes, d['nodes']):
        node(img, nx, ny, 50, ic)
        text(img, (nx, ny + 76), a, fit(a, 25, PB, 250), INK, PB, 'mm')
        text(img, (nx, ny + 110), b, fit(b, 20, PM, 250), SUB, PM, 'mm')

def dg_steps3(img, d):
    """phone left + heading + 3 cards right. d: head, steps=[(icon,text)], kind, label"""
    phone(img, M, 668, 252, 410, d.get('kind', 'poster'), d.get('label', 'ऑफर'))
    X0, X1 = 330, 1080 - M
    heading(img, d['head'], 690, X0, 'l', 29)
    top, ch, gap = 742, 96, 22
    n = len(d['steps'])
    for i, (ic, a) in enumerate(d['steps']):
        y0 = top + i * (ch + gap); yc = y0 + ch / 2
        rrect(img, (X0, y0, X1, y0 + ch), 24, fill=WHITE, outline=CARD_OL, width=2)
        node(img, X0 + 64, yc, 34, ic)
        text(img, (X0 + 118, yc), a, fit(a, 27, PB, X1 - X0 - 210), INK, PB, 'lm')
        bx = X1 - 50
        L(img).ellipse(P((bx - 25, yc - 25), (bx + 25, yc + 25)), fill=YEL)
        text(img, (bx, yc + 1), str(i + 1), 27, INK, PB, 'mm')
        if i < n - 1:
            ax = X0 + 64; ay = y0 + ch + gap / 2
            L(img).polygon(P((ax - 9, ay - 6), (ax + 9, ay - 6), (ax, ay + 7)), fill=GREEN)

def dg_cycle(img, d):
    """4 nodes around a centre. d: centre=(l1,l2), nodes=[(icon,t1,t2)x4] clockwise from top-left"""
    CX, CY, R = 540, 870, 160
    for a0, a1 in [(-135, -45), (-45, 45), (45, 135), (135, 225)]:
        arc_arrow(img, CX, CY, R, a0 + 22, a1 - 22, GREEN, w=4)
    L(img).ellipse(P((CX - 88, CY - 88), (CX + 88, CY + 88)), fill=WHITE, outline=YEL, width=5 * S)
    c1, c2 = d['centre']
    node_icon = d.get('cicon', 'store')
    tmp = Image.new('RGBA', (int(110 * S), int(110 * S)), (0, 0, 0, 0))
    icon(tmp, node_icon, 55, 55, DEEP, YEL, WHITE)
    sz = int(70 * S); tmp = tmp.resize((sz, sz), Image.LANCZOS)
    img.paste(tmp, (int(CX * S - sz / 2), int((CY - 36) * S - sz / 2)), tmp)
    text(img, (CX, CY + 22), c1, fit(c1, 18, PM, 150), SUB, PM, 'mm')
    text(img, (CX, CY + 48), c2, fit(c2, 22, PB, 150), INK, PB, 'mm')
    for i, (a, (ic, t1, t2)) in enumerate(zip([-135, -45, 45, 135], d['nodes'])):
        nx, ny = CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a))
        node(img, nx, ny, 48, ic, num=i + 1)
        if nx < CX:
            text(img, (nx - 66, ny - 16), t1, fit(t1, 25, PB, 290), INK, PB, 'rm')
            text(img, (nx - 66, ny + 18), t2, fit(t2, 20, PM, 290), SUB, PM, 'rm')
        else:
            text(img, (nx + 66, ny - 16), t1, fit(t1, 25, PB, 290), INK, PB, 'lm')
            text(img, (nx + 66, ny + 18), t2, fit(t2, 20, PM, 290), SUB, PM, 'lm')

def dg_hsteps(img, d):
    """heading + N (3-5) numbered nodes in a row + result card. d: head, steps=[(icon,t1,t2)], result"""
    heading(img, d['head'], 692)
    n = len(d['steps'])
    xs = [M + 90 + i * ((1080 - 2 * M - 180) / (n - 1)) for i in range(n)]
    y = 818
    L(img).line(P((xs[0], y), (xs[-1], y)), fill=LINEC, width=4 * S)
    for i, (x, (ic, a, b)) in enumerate(zip(xs, d['steps'])):
        node(img, x, y, 56 if n <= 4 else 50, ic, num=i + 1)
        cw = (1080 - 2 * M) / n - 8
        text(img, (x, y + 92), a, fit(a, 24, PB, cw), INK, PB, 'mm')
        text(img, (x, y + 124), b, fit(b, 19, PM, cw), SUB, PM, 'mm')
        if i < n - 1:
            mx = (x + xs[i + 1]) / 2
            L(img).polygon(P((mx - 8, y - 11), (mx + 10, y), (mx - 8, y + 11)), fill=GREEN)
    if d.get('result'):
        segs = segs_fit(parse(d['result'], 25), 900)
        w = rich_w(segs) + 90
        rrect(img, (540 - w / 2, 1000, 540 + w / 2, 1062), 31, fill=WHITE, outline=GREEN, width=3)
        check(img, 540 - w / 2 + 36, 1031, 15, GREEN, WHITE)
        rich2(img, 540 + 18, 1031, segs)

def dg_fanout(img, d):
    """idea -> poster -> approve -> 3 outputs. d: head, a=(icon,t1,t2) x3, outs=[(icon,label)x3]"""
    heading(img, d['head'], 692)
    ys = [770, 880, 990]; yc = 880
    xs = [130, 330, 530]
    for i, (x, (ic, t1, t2)) in enumerate(zip(xs, d['a'])):
        node(img, x, yc - 20, 54, ic, num=i + 1)
        text(img, (x, yc + 62), t1, fit(t1, 23, PB, 190), INK, PB, 'mm')
        text(img, (x, yc + 92), t2, fit(t2, 18, PM, 190), SUB, PM, 'mm')
        if i < 2:
            L(img).line(P((x + 58, yc - 20), (xs[i + 1] - 58, yc - 20)), fill=LINEC, width=4 * S)
            L(img).polygon(P((xs[i + 1] - 70, yc - 31), (xs[i + 1] - 56, yc - 20), (xs[i + 1] - 70, yc - 9)), fill=GREEN)
    for y, (ic, lab) in zip(ys, d['outs']):
        dashed(img, bez((588, yc - 20), (680, yc - 20), (760, y)), LINEC, w=3, dash=10, gap=8)
        rrect(img, (760, y - 44, 1080 - M, y + 44), 44, fill=WHITE, outline=CARD_OL, width=2)
        node(img, 806, y, 38, ic)
        text(img, (858, y), lab, fit(lab, 24, PB, 170), INK, PB, 'lm')

def dg_pipeline(img, d):
    """send -> safe -> phone with ticks -> reply back. d: head, stages=[(icon,t1,t2)x3], ticks=[...], back"""
    heading(img, d['head'], 692)
    xs = [150, 400, 650]; y = 812
    for i, (x, (ic, a, b)) in enumerate(zip(xs, d['stages'])):
        node(img, x, y, 56, ic, num=i + 1)
        text(img, (x, y + 88), a, fit(a, 23, PB, 220), INK, PB, 'mm')
        text(img, (x, y + 118), b, fit(b, 18, PM, 220), SUB, PM, 'mm')
        L(img).line(P((x + 62, y), (x + 250 - 62, y)), fill=LINEC, width=4 * S)
        L(img).polygon(P((x + 176, y - 11), (x + 190, y), (x + 176, y + 11)), fill=GREEN)
    # customer phone
    phone(img, 836, 676, 196, 300, 'wa', d.get('label', 'आपका ऑफर'))
    # ticks strip
    tks = d['ticks']
    ws = [tw(t, 20, PBD) + 54 for t in tks]
    x = 540 - (sum(ws) + 16 * (len(ws) - 1)) / 2
    for t, w in zip(tks, ws):
        rrect(img, (x, 990, x + w, 1032), 21, fill=WHITE, outline=GREEN, width=2)
        check(img, x + 22, 1011, 10, GREEN, WHITE)
        text(img, (x + 38, 1011), t, 20, INK, PBD, 'lm')
        x += w + 16
    dashed(img, bez((930, 990), (900, 1066), (540, 1066)), LINEC, w=3, dash=9, gap=7)
    text(img, (520, 1066), d['back'], fit(d['back'], 20, PBD, 460), GREEN, PBD, 'rm')

def dg_window(img, d):
    """24-hour reply window bar. d: head, open_t, open_b, closed_t, closed_b, tip"""
    heading(img, d['head'], 692)
    x0, x1, y = M + 30, 1080 - M - 30, 830
    rrect(img, (x0, y - 22, x0 + (x1 - x0) * 0.8, y + 22), 22, fill=GREEN)
    rrect(img, (x0 + (x1 - x0) * 0.8 - 22, y - 22, x1, y + 22), 22, fill=HL)
    rrect(img, (x0 + (x1 - x0) * 0.8 - 22, y - 22, x0 + (x1 - x0) * 0.8 + 4, y + 22), 0, fill=GREEN)
    text(img, (x0 + (x1 - x0) * 0.4, y), d['bar_open'], 22, WHITE, PB, 'mm')
    text(img, (x0 + (x1 - x0) * 0.9, y), d['bar_closed'], 18, INK, PB, 'mm')
    for i, lab in enumerate(d['marks']):
        x = x0 + (x1 - x0) * 0.8 * i / (len(d['marks']) - 1)
        L(img).line(P((x, y + 26), (x, y + 40)), fill=SUB, width=2 * S)
        text(img, (x, y + 56), lab, 18, SUB, PBD, 'mm')
    node(img, x0 + 4, y - 66, 30, 'chat')
    text(img, (x0 + 44, y - 66), d['start'], 21, INK, PBD, 'lm')
    cw = (1080 - 2 * M - 24) / 2
    for i, (ic, t1, t2) in enumerate([('chat', d['open_t'], d['open_b']), ('tmpl', d['closed_t'], d['closed_b'])]):
        cx0 = M + i * (cw + 24)
        rrect(img, (cx0, 914, cx0 + cw, 1080), 24, fill=WHITE, outline=CARD_OL if i else GREEN, width=2 if i else 3)
        node(img, cx0 + 60, 966, 36, ic)
        text(img, (cx0 + 110, 954), t1, fit(t1, 24, PB, cw - 130), INK, PB, 'lm')
        text(img, (cx0 + 110, 986), t2, fit(t2, 18, PM, cw - 130), SUB, PM, 'lm')
        text(img, (cx0 + 30, 1046), d['tips'][i], fit(d['tips'][i], 20, PBD, cw - 60), GREEN, PBD, 'lm')

def dg_beforeafter(img, d):
    """two columns: before (x) vs with Shri Tech (check). d: before=[3], after=[3], btitle, atitle"""
    cw = (1080 - 2 * M - 64) / 2
    for i in range(2):
        x0 = M + i * (cw + 64)
        rrect(img, (x0, 668, x0 + cw, 1076), 26, fill=WHITE, outline=(YEL if i == 0 else DEEP), width=3)
        hc = PALE if i == 0 else DEEP
        rrect(img, (x0, 668, x0 + cw, 736), 26, fill=hc)
        rrect(img, (x0, 710, x0 + cw, 736), 0, fill=hc)
        if i == 0:
            text(img, (x0 + cw / 2, 702), d['btitle'], fit(d['btitle'], 26, PB, cw - 40), INK, PB, 'mm')
        else:
            segs = segs_fit(parse(d['atitle'], 26, WHITE, YEL), cw - 40)
            rich2(img, x0 + cw / 2, 702, segs, dark=True)
        items = d['before'] if i == 0 else d['after']
        for k, it in enumerate(items):
            y = 790 + k * 92
            if i == 0:
                L(img).ellipse(P((x0 + 26, y - 18), (x0 + 62, y + 18)), fill=PALE, outline=YEL, width=2 * S)
                L(img).line(P((x0 + 36, y - 8), (x0 + 52, y + 8)), fill=SUB, width=4 * S)
                L(img).line(P((x0 + 52, y - 8), (x0 + 36, y + 8)), fill=SUB, width=4 * S)
                text(img, (x0 + 78, y), it, fit(it, 22, PM, cw - 100), SUB, PM, 'lm')
            else:
                check(img, x0 + 44, y, 18, GREEN, WHITE)
                text(img, (x0 + 78, y), it, fit(it, 22, PB, cw - 100), INK, PB, 'lm')
    # arrow between
    cx = M + cw + 32
    L(img).ellipse(P((cx - 28, 842), (cx + 28, 898)), fill=YEL)
    L(img).polygon(P((cx - 10, 856), (cx + 12, 870), (cx - 10, 884)), fill=DEEP)

def dg_tiles(img, d):
    """heading + N tiles (icon + 2 lines) + bottom note. d: head, tiles=[(icon,t1,t2)], note"""
    heading(img, d['head'], 692)
    n = len(d['tiles']); gap = 14
    tw_ = (1080 - 2 * M - gap * (n - 1)) / n
    for i, (ic, a, b) in enumerate(d['tiles']):
        x0 = M + i * (tw_ + gap)
        rrect(img, (x0, 740, x0 + tw_, 966), 24, fill=WHITE, outline=CARD_OL, width=2)
        node(img, x0 + tw_ / 2, 806, 44, ic, num=i + 1 if d.get('num') else None)
        text(img, (x0 + tw_ / 2, 880), a, fit(a, 23, PB, tw_ - 20), INK, PB, 'mm')
        text(img, (x0 + tw_ / 2, 914), b, fit(b, 17, PM, tw_ - 16), SUB, PM, 'mm')
        if d.get('b2') and i < len(d['b2']):
            text(img, (x0 + tw_ / 2, 938), d['b2'][i], fit(d['b2'][i], 17, PM, tw_ - 16), SUB, PM, 'mm')
    if d.get('note'):
        segs = segs_fit(parse(d['note'], 24), 900)
        w = rich_w(segs) + 64
        rrect(img, (540 - w / 2, 996, 540 + w / 2, 1056), 30, fill=HL)
        rich2(img, 540, 1026, segs)

def dg_dash(img, d):
    """phone dashboard left + numbered callouts right. d: head, items=[(t1,t2)x4]"""
    phone(img, M, 668, 252, 410, 'dash')
    X0, X1 = 330, 1080 - M
    heading(img, d['head'], 690, X0, 'l', 29)
    for i, (a, b) in enumerate(d['items']):
        y0 = 740 + i * 86; yc = y0 + 38
        rrect(img, (X0, y0, X1, y0 + 76), 22, fill=WHITE, outline=CARD_OL, width=2)
        L(img).ellipse(P((X0 + 20, yc - 22), (X0 + 64, yc + 22)), fill=GREEN)
        text(img, (X0 + 42, yc + 1), str(i + 1), 22, WHITE, PB, 'mm')
        text(img, (X0 + 84, yc - 13), a, fit(a, 24, PB, X1 - X0 - 110), INK, PB, 'lm')
        text(img, (X0 + 84, yc + 16), b, fit(b, 18, PM, X1 - X0 - 110), SUB, PM, 'lm')

def dg_tribute(img, d):
    """respectful message card, no selling. d: quote, by, lines"""
    y0, y1 = 672, 1180
    rrect(img, (M + 30, y0, 1080 - M - 30, y1), 30, fill=WHITE, outline=YEL, width=3)
    n = len(d['quote']); hq = n * 64 + (60 if d.get('by') else 0) + 46 * len(d.get('lines', [])) + 90
    y = (y0 + y1) / 2 - hq / 2
    text(img, (540, y + 30), '“', 96, YEL, PB, 'mm'); y += 100
    for ln_ in d['quote']:
        text(img, (540, y), ln_, fit(ln_, 42, PB, 840), INK, PB, 'mm'); y += 64
    if d.get('by'):
        y += 10; text(img, (540, y), d['by'], 26, GREEN, PBD, 'mm'); y += 50
    for ln_ in d.get('lines', []):
        y += 6; text(img, (540, y), ln_, fit(ln_, 24, PM, 840), SUB, PM, 'mm'); y += 40

DIAGRAMS = dict(hub=dg_hub, steps3=dg_steps3, cycle=dg_cycle, hsteps=dg_hsteps, fanout=dg_fanout, pipeline=dg_pipeline,
                window=dg_window, beforeafter=dg_beforeafter, tiles=dg_tiles, dash=dg_dash, tribute=dg_tribute)

def tribute_footer(img, line, y=1214):
    rrect(img, (0, y, 1080, 1350), 0, fill=DEEP)
    text(img, (540, y + 44), line, fit(line, 26, PBD, 980), (187, 247, 208), PBD, 'mm')
    size = 34; lw = logo_width(size)
    tot = lw + 40 + tw('9993615146', 34, PB) + 50
    x = 540 - tot / 2
    logo(img, x, y + 72, size, dark=True)
    phone_icon(img, x + lw + 60, y + 98, 30, YEL)
    text(img, (x + lw + 86, y + 98), '9993615146', 34, YEL, PB, 'lm')
