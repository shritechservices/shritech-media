"""Line-art festival illustrations, light theme (green + yellow + white). Zone ~ y 100..410, centred at x 540."""
from kit import *

K = DEEP; SW = 5
def D(img): return ImageDraw.Draw(img)
def ln(img, pts, c=K, w=SW): D(img).line(P(*pts), fill=c, width=int(w * S), joint='curve')
def el(img, cx, cy, rx, ry=None, fill=None, out=K, w=SW):
    ry = ry or rx
    D(img).ellipse(P((cx - rx, cy - ry), (cx + rx, cy + ry)), fill=fill, outline=out, width=int(w * S) if out else 0)
def rect(img, x0, y0, x1, y1, fill=WHITE, out=K, w=SW, r=0):
    if r: D(img).rounded_rectangle(P((x0, y0), (x1, y1)), r * S, fill=fill, outline=out, width=int(w * S) if out else 0)
    else: D(img).rectangle(P((x0, y0), (x1, y1)), fill=fill, outline=out, width=int(w * S) if out else 0)
def poly(img, pts, fill=None, out=K, w=SW):
    if fill: D(img).polygon(P(*pts), fill=fill)
    if out: ln(img, pts + [pts[0]], out, w)

# ---------- primitives ----------
def rays(img, cx, cy, r0, r1, n=24, skip_below=None, col=YEL, w=6):
    for i in range(n):
        a = i * 2 * math.pi / n
        if skip_below is not None and math.sin(a) > skip_below: continue
        rr = r1 if i % 2 == 0 else r0 + (r1 - r0) * 0.6
        ln(img, [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + rr * math.cos(a), cy + rr * math.sin(a))], col, w)

def dots_arc(img, cx, cy, r, n, col, rd=4, a0=180, a1=360):
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n - 1))
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        D(img).ellipse(P((x - rd, y - rd), (x + rd, y + rd)), fill=col)

def diya(img, cx, by, s=1.0):
    glow(img, cx, by - 50 * s, 70 * s, (250, 204, 21), 0.45)
    fy = by - 16 * s
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.ellipse(P((cx - 16 * s, fy - 36 * s), (cx + 16 * s, fy)), fill=255)
    md.polygon(P((cx - 15 * s, fy - 22 * s), (cx, fy - 78 * s), (cx + 15 * s, fy - 22 * s)), fill=255)
    img.paste(Image.new('RGB', img.size, YEL), (0, 0), m)
    D(img).ellipse(P((cx - 7 * s, fy - 28 * s), (cx + 7 * s, fy - 4 * s)), fill=(255, 251, 225))
    D(img).chord(P((cx - 64 * s, by - 46 * s), (cx + 64 * s, by + 34 * s)), 0, 180, fill=YEL, outline=K, width=int(4 * S))
    ln(img, [(cx - 64 * s, by - 6 * s), (cx + 64 * s, by - 6 * s)], K, 4)
    for i in range(5):
        x = cx - 32 * s + i * 16 * s
        D(img).ellipse(P((x - 4 * s, by + 8 * s), (x + 4 * s, by + 16 * s)), fill=GREEN)

def toran(img, xa, xb, y=118, sag=30, n=8):
    pts = [(xa + (xb - xa) * i / 30, y + sag * math.sin(math.pi * i / 30)) for i in range(31)]
    ln(img, pts, GREEN, 3)
    for i in range(1, n):
        t = i / n; x = xa + (xb - xa) * t; yy = y + sag * math.sin(math.pi * t)
        D(img).polygon(P((x, yy), (x - 11, yy + 22), (x, yy + 44), (x + 11, yy + 22)), fill=GREEN if i % 2 else (34, 197, 94))
        if i % 2 == 0: D(img).ellipse(P((x - 9, yy + 46), (x + 9, yy + 64)), fill=YEL)

def lights(img, y=120, sag=36):
    pts = [(40 + 1000 * i / 40, y + sag * math.sin(math.pi * i / 40)) for i in range(41)]
    ln(img, pts, LINEC, 2)
    for i in range(1, 16):
        t = i / 16; x = 40 + 1000 * t; yy = y + sag * math.sin(math.pi * t)
        if 340 < x < 740: continue
        c = YEL if i % 2 else GREEN
        D(img).ellipse(P((x - 7, yy + 4), (x + 7, yy + 22)), fill=c)

def star5(img, cx, cy, r, fill=YEL, out=None):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(img, pts, fill, out, 3)

def crescent(img, cx, cy, r, col=YEL, bg=WHITE):
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.ellipse(P((cx - r, cy - r), (cx + r, cy + r)), fill=255)
    md.ellipse(P((cx - r * 0.55, cy - r * 1.05), (cx + r * 1.25, cy + r * 0.75)), fill=0)
    img.paste(Image.new('RGB', img.size, col), (0, 0), m)

def lantern(img, cx, top, s=1.0):
    ln(img, [(cx, 96), (cx, top)], K, 3)
    poly(img, [(cx - 18 * s, top + 10 * s), (cx + 18 * s, top + 10 * s), (cx + 10 * s, top)], fill=GREEN, out=None)
    rect(img, cx - 26 * s, top + 10 * s, cx + 26 * s, top + 78 * s, fill=PALE, out=K, w=4, r=10 * s)
    glow(img, cx, top + 44 * s, 30 * s, (250, 204, 21), 0.5)
    el(img, cx, top + 44 * s, 10 * s, 16 * s, fill=YEL, out=None)
    for x in (cx - 12 * s, cx + 12 * s): ln(img, [(x, top + 12 * s), (x, top + 76 * s)], K, 2)
    poly(img, [(cx - 18 * s, top + 78 * s), (cx + 18 * s, top + 78 * s), (cx, top + 96 * s)], fill=GREEN, out=None)

def kite(img, cx, cy, s=1.0, c1=YEL, c2=GREEN, rot=0):
    pts = [(0, -60), (44, 0), (0, 64), (-44, 0)]
    a = math.radians(rot)
    tp = [(cx + (x * math.cos(a) - y * math.sin(a)) * s, cy + (x * math.sin(a) + y * math.cos(a)) * s) for x, y in pts]
    D(img).polygon(P(tp[0], tp[1], tp[2]), fill=c1); D(img).polygon(P(tp[0], tp[3], tp[2]), fill=c2)
    poly(img, tp, None, K, 3); ln(img, [tp[0], tp[2]], K, 2); ln(img, [tp[1], tp[3]], K, 2)
    tail = [tp[2], (tp[2][0] - 10 * s, tp[2][1] + 30 * s), (tp[2][0] + 8 * s, tp[2][1] + 56 * s)]
    ln(img, tail, K, 2)
    return tp[2]

def chakra(img, cx, cy, r, col=K):
    el(img, cx, cy, r, fill=WHITE, out=col, w=4)
    el(img, cx, cy, r * 0.16, fill=col, out=None)
    for i in range(24):
        a = i * math.pi / 12
        ln(img, [(cx, cy), (cx + r * 0.92 * math.cos(a), cy + r * 0.92 * math.sin(a))], col, 2)

def book(img, cx, cy, w=200, h=120, fill=WHITE):
    poly(img, [(cx, cy - h / 2 + 10), (cx - w / 2, cy - h / 2), (cx - w / 2, cy + h / 2), (cx, cy + h / 2 + 10)], fill=fill)
    poly(img, [(cx, cy - h / 2 + 10), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx, cy + h / 2 + 10)], fill=fill)
    for k in range(3):
        y = cy - h / 2 + 30 + k * 22
        ln(img, [(cx - w / 2 + 18, y), (cx - 18, y + 6)], LINEC, 3); ln(img, [(cx + 18, y + 6), (cx + w / 2 - 18, y)], LINEC, 3)

def gear(img, cx, cy, r, teeth=10, fill=WHITE, col=K):
    pts = []
    for i in range(teeth * 2):
        a0 = i * math.pi / teeth
        rr = r if i % 2 == 0 else r * 0.8
        for da in (-0.12, 0.12):
            pts.append((cx + rr * math.cos(a0 + da * 2.5 / teeth * 4), cy + rr * math.sin(a0 + da * 2.5 / teeth * 4)))
    poly(img, pts, fill, col, 4)
    el(img, cx, cy, r * 0.32, fill=YEL, out=col, w=4)

def gift(img, x, y, w, h, box=YEL, rib=GREEN):
    rect(img, x, y, x + w, y + h, fill=box, out=K, w=4, r=6)
    rect(img, x - 6, y - 16, x + w + 6, y + 4, fill=box, out=K, w=4, r=4)
    D(img).rectangle(P((x + w / 2 - 7, y - 14), (x + w / 2 + 7, y + h - 2)), fill=rib)
    el(img, x + w / 2 - 12, y - 26, 12, 9, fill=None, out=rib, w=4); el(img, x + w / 2 + 12, y - 26, 12, 9, fill=None, out=rib, w=4)

def balloon(img, cx, cy, s=1.0, col=YEL):
    el(img, cx, cy, 34 * s, 42 * s, fill=col, out=K, w=3)
    D(img).ellipse(P((cx - 18 * s, cy - 28 * s), (cx - 8 * s, cy - 12 * s)), fill=WHITE)
    poly(img, [(cx - 6 * s, cy + 44 * s), (cx + 6 * s, cy + 44 * s), (cx, cy + 36 * s)], fill=col, out=K, w=2)
    ln(img, [(cx, cy + 44 * s), (cx - 10 * s, cy + 80 * s), (cx + 6 * s, cy + 116 * s)], K, 2)

def burst(img, cx, cy, r, col=YEL, n=16):
    for i in range(n):
        a = i * 2 * math.pi / n
        ln(img, [(cx + r * 0.35 * math.cos(a), cy + r * 0.35 * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))], col if i % 2 else GREEN, 4)
        D(img).ellipse(P((cx + r * 1.12 * math.cos(a) - 4, cy + r * 1.12 * math.sin(a) - 4), (cx + r * 1.12 * math.cos(a) + 4, cy + r * 1.12 * math.sin(a) + 4)), fill=col)

def coin(img, cx, cy, r, sym='₹'):
    el(img, cx, cy, r, fill=YEL, out=K, w=4); el(img, cx, cy, r * 0.74, fill=None, out=GOLD, w=3)
    text(img, (cx, cy + 2), sym, r * 0.9, K, PB, 'mm')

def kalash(img, cx, by, s=1.0):
    D(img).ellipse(P((cx - 60 * s, by - 110 * s), (cx + 60 * s, by)), fill=YEL, outline=K, width=int(5 * S))
    rect(img, cx - 34 * s, by - 132 * s, cx + 34 * s, by - 104 * s, fill=YEL, out=K, w=5)
    for i, dx in enumerate((-40, -20, 0, 20, 40)):
        D(img).polygon(P((cx + dx * s, by - 130 * s), (cx + dx * s - 14 * s, by - 170 * s), (cx + dx * s + 14 * s, by - 170 * s)), fill=GREEN)
    el(img, cx, by - 178 * s, 26 * s, 24 * s, fill=(220, 252, 231), out=K, w=4)
    ln(img, [(cx - 50 * s, by - 60 * s), (cx + 50 * s, by - 60 * s)], GREEN, 5)
    text(img, (cx, by - 36 * s), 'शुभ', 22 * s, K, PB, 'mm')

def flower(img, cx, cy, r, col=YEL, center=GREEN):
    for i in range(8):
        a = i * math.pi / 4
        D(img).ellipse(P((cx + r * 0.6 * math.cos(a) - r * 0.42, cy + r * 0.6 * math.sin(a) - r * 0.42),
                         (cx + r * 0.6 * math.cos(a) + r * 0.42, cy + r * 0.6 * math.sin(a) + r * 0.42)), fill=col)
    el(img, cx, cy, r * 0.32, fill=center, out=None)

def lotus(img, cx, by, s=1.0):
    for dx, h, w_, col in [(-52, 70, 40, (220, 252, 231)), (52, 70, 40, (220, 252, 231)), (-26, 100, 40, (187, 247, 208)), (26, 100, 40, (187, 247, 208)), (0, 124, 44, YEL)]:
        x = cx + dx * s
        pts = bez((x - w_ * s, by), (x, by - h * s * 1.3), (x + w_ * s, by), 16)
        D(img).polygon(P(*pts), fill=col); ln(img, pts + [pts[0]], K, 3)
    ln(img, [(cx - 90 * s, by), (cx + 90 * s, by)], GREEN, 5)

def trophy(img, cx, by, s=1.0):
    pts = bez((cx - 60 * s, by - 190 * s), (cx, by - 40 * s), (cx + 60 * s, by - 190 * s), 20)
    D(img).polygon(P(*pts), fill=YEL); ln(img, pts + [pts[0]], K, 5)
    for sg in (-1, 1):
        D(img).arc(P((cx + sg * 58 * s - 26 * s, by - 186 * s), (cx + sg * 58 * s + 26 * s, by - 134 * s)), 270 if sg > 0 else 90, 90 if sg > 0 else 270, fill=K, width=int(5 * S))
    rect(img, cx - 10 * s, by - 100 * s, cx + 10 * s, by - 50 * s, fill=YEL, out=K, w=4)
    rect(img, cx - 48 * s, by - 50 * s, cx + 48 * s, by, fill=GREEN, out=K, w=5, r=6)
    star5(img, cx, by - 150 * s, 18 * s, WHITE)

def flag(img, x, top, bottom, col=YEL):
    ln(img, [(x, bottom), (x, top)], K, 5)
    poly(img, [(x, top + 4), (x + 66, top + 32), (x, top + 60)], col, K, 4)

def clock(img, cx, cy, r):
    el(img, cx, cy, r, fill=WHITE, out=K, w=6); el(img, cx, cy, r - 12, fill=None, out=LINEC, w=2)
    for i in range(12):
        a = i * math.pi / 6
        ln(img, [(cx + (r - 20) * math.cos(a), cy + (r - 20) * math.sin(a)), (cx + (r - 10) * math.cos(a), cy + (r - 10) * math.sin(a))], K, 4 if i % 3 == 0 else 2)
    ln(img, [(cx, cy), (cx, cy - r * 0.62)], K, 6); ln(img, [(cx, cy), (cx - r * 0.06, cy - r * 0.45)], GREEN, 6)
    el(img, cx, cy, 7, fill=YEL, out=K, w=2)

def snowflake(img, x, y, r, col=LINEC):
    for i in range(3):
        a = i * math.pi / 3
        ln(img, [(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))], col, 2)

def sparkles(img, pts):
    for x, y, r in pts: sparkle(img, x, y, r, GOLD)

def ground(img, y=402, x0=150, x1=930):
    ln(img, [(x0, y), (x1, y)], LINEC, 3)

def sun(img, cx, cy, r=90, skip=0.5):
    glow(img, cx, cy, r * 2, (254, 236, 140), 0.5)
    rays(img, cx, cy, r + 16, r + 54, 28, skip, YEL, 6)
    el(img, cx, cy, r, fill=HL, out=YEL, w=6)

# ---------- occasions ----------
def a_gurunanak(img):
    cx = 540
    for i in range(30):
        a = math.pi + i * math.pi / 29
        for rr in (150, 175, 200):
            x, y = cx + rr * math.cos(a), 250 + rr * math.sin(a)
            r = 4 if rr != 175 else 3
            D(img).ellipse(P((x - r, y - r), (x + r, y + r)), fill=YEL if rr != 175 else GREEN)
    rect(img, 360, 366, 720, 388); rect(img, 410, 268, 670, 366)
    for x0 in (432, 512, 592):
        rect(img, x0, 296, x0 + 56, 366, fill=PALE, w=4, r=28); D(img).rectangle(P((x0 + 2, 340), (x0 + 54, 364)), fill=PALE)
    l_ = bez((470, 268), (436, 200), (540, 128), 30); r_ = bez((540, 128), (644, 200), (610, 268), 30)
    D(img).polygon(P(*(l_ + r_)), fill=HL); ln(img, l_); ln(img, r_); ln(img, [(466, 268), (614, 268)])
    el(img, 540, 116, 9, 10, fill=YEL, out=K, w=3); ln(img, [(540, 106), (540, 88)], K, 4)
    for x in (425, 655):
        rect(img, x - 16, 238, x + 16, 268, w=4)
        dl = bez((x - 18, 238), (x - 16, 214), (x, 204), 12); dr = bez((x, 204), (x + 16, 214), (x + 18, 238), 12)
        D(img).polygon(P(*(dl + dr)), fill=HL); ln(img, dl + dr, K, 4)
    flag(img, 780, 128, 388)
    for x in (300, 780 + 0):
        pass
    diya(img, 300, 392, 0.55); diya(img, 860, 392, 0.55)
    sparkles(img, [(150, 200, 13), (930, 250, 12), (220, 320, 8)])

def a_maths(img):
    # chalk-board with formulas + compass + ruler
    rect(img, 330, 120, 750, 380, fill=(240, 253, 244), out=K, w=6, r=18)
    text(img, (540, 190), 'π  ∞  √  ∑', 64, K, 'DejaVuSans-Bold', 'mm') if False else None
    for (t, x, y, sz, c) in [('1729', 430, 190, 54, GREEN), ('π', 650, 190, 70, K), ('a² + b² = c²', 540, 270, 40, K), ('∞', 420, 335, 48, GOLD), ('√2', 650, 335, 44, GREEN)]:
        f = PB if t not in ('π', '∞') else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        text(img, (x, y), t, sz, c, f, 'mm')
    # compass
    ln(img, [(220, 150), (180, 380)], K, 6); ln(img, [(220, 150), (262, 380)], K, 6); el(img, 220, 146, 12, fill=YEL, out=K, w=4)
    D(img).arc(P((150, 330), (290, 420)), 200, 340, fill=GREEN, width=int(4 * S))
    # ruler / triangle
    poly(img, [(830, 380), (930, 380), (830, 200)], HL, K, 5)
    for k in range(6): ln(img, [(830, 220 + k * 28), (846, 220 + k * 28)], K, 3)
    sparkles(img, [(290, 120, 12), (800, 140, 14)])

def a_christmas(img, variant=0):
    cx = 540
    for top, bot, hw in [(140, 228, 86), (194, 296, 112), (252, 364, 138)]:
        poly(img, [(cx, top), (cx - hw, bot), (cx + hw, bot)], (187, 247, 208), GREEN, 5)
    rect(img, cx - 18, 364, cx + 18, 388, fill=YEL, out=K, w=3)
    for (y0, y1, x0, x1) in [(188, 214, -56, 64), (250, 276, -88, 92), (314, 346, -120, 120)]:
        for i, (x, y) in enumerate(bez((cx + x0, y0), (cx, y1 + 30), (cx + x1, y1 - 10), 24)):
            if i % 2 == 0: D(img).ellipse(P((x - 3.5, y - 3.5), (x + 3.5, y + 3.5)), fill=GOLD)
    for (x, y, c) in [(cx - 36, 212, YEL), (cx + 32, 200, GREEN), (cx - 64, 276, GREEN), (cx + 58, 268, YEL), (cx - 92, 342, YEL), (cx + 92, 338, GREEN)]:
        el(img, x, y, 9, fill=c, out=K, w=2)
    glow(img, cx, 132, 50, (250, 204, 21), 0.5); star5(img, cx, 132, 30, YEL, K)
    if variant == 0:
        gift(img, 330, 330, 76, 58, YEL, GREEN); gift(img, 672, 316, 90, 72, GREEN, YEL); gift(img, 776, 350, 54, 38, YEL, GREEN)
    else:
        # snowman + bells
        el(img, 250, 340, 46, fill=WHITE, out=K, w=4); el(img, 250, 270, 32, fill=WHITE, out=K, w=4)
        for dx in (-10, 10): el(img, 250 + dx, 264, 3, fill=K, out=None)
        poly(img, [(250, 272), (276, 276), (250, 280)], YEL, None)
        rect(img, 222, 230, 278, 238, fill=K, out=None); rect(img, 232, 194, 268, 232, fill=K, out=None)
        ln(img, [(222, 310), (286, 310)], GREEN, 8)
        for bx in (800, 860):
            pts = bez((bx - 34, 300), (bx, 180), (bx + 34, 300), 16)
            D(img).polygon(P(*pts), fill=YEL); ln(img, pts + [pts[0]], K, 4); el(img, bx, 306, 8, fill=GREEN, out=K, w=2)
        ln(img, [(800, 200), (830, 160), (860, 200)], GREEN, 5)
        D(img).ellipse(P((818, 150), (842, 172)), fill=GREEN)
    for x, y, r in [(150, 180, 9), (920, 170, 10), (200, 270, 7), (900, 260, 8), (120, 360, 8), (960, 360, 7)]:
        snowflake(img, x, y, r)

def a_newyear(img, year='2027'):
    burst(img, 230, 200, 70); burst(img, 850, 190, 64, GREEN); burst(img, 330, 340, 40); burst(img, 760, 330, 44)
    text(img, (540, 262), year, 150, GREEN, PB, 'mm')
    s = tw(year, 150, PB)
    rrect(img, (540 - s / 2, 330, 540 + s / 2, 348), 9, fill=YEL)
    clock(img, 540 + s / 2 + 10, 150, 44) if False else None
    for i, x in enumerate((420, 470, 520, 560, 610, 660)):
        D(img).ellipse(P((x - 5, 380), (x + 5, 390)), fill=YEL if i % 2 else GREEN)

def a_youth(img):
    sun(img, 540, 330, 100, 0.2)
    # mountains
    poly(img, [(220, 400), (400, 230), (520, 330), (640, 210), (860, 400)], (220, 252, 231), K, 5)
    poly(img, [(400, 230), (430, 258), (370, 258)], WHITE, None)
    poly(img, [(640, 210), (674, 242), (606, 242)], WHITE, None)
    # flag on peak
    flag(img, 640, 130, 212)
    ground(img, 402, 160, 920)
    sparkles(img, [(240, 170, 12), (880, 180, 12)])

def a_sankranti(img):
    sun(img, 540, 230, 70, 0.6)
    t1 = kite(img, 300, 210, 1.1, YEL, GREEN, -12); t2 = kite(img, 800, 190, 1.0, GREEN, YEL, 14); kite(img, 660, 330, 0.7, YEL, GREEN, 6)
    ln(img, bez(t1, (260, 380), (180, 410)), LINEC, 2); ln(img, bez(t2, (860, 360), (930, 410)), LINEC, 2)
    # til-gud bowl
    D(img).chord(P((420, 330), (520, 410)), 0, 180, fill=YEL, outline=K, width=int(4 * S))
    for x, y in [(445, 360), (470, 352), (495, 360), (458, 340), (483, 340)]: el(img, x, y, 11, fill=(254, 249, 195), out=K, w=2)

def a_gurugobind(img):
    sun(img, 540, 250, 80, 0.4)
    # khanda-free respectful: Nishan Sahib pair + lamps + dome
    l_ = bez((470, 330), (440, 268), (540, 200), 30); r_ = bez((540, 200), (640, 268), (610, 330), 30)
    D(img).polygon(P(*(l_ + r_)), fill=HL); ln(img, l_); ln(img, r_)
    rect(img, 430, 330, 650, 396); rect(img, 400, 396, 680, 412)
    for x0 in (452, 512, 572): rect(img, x0, 350, x0 + 46, 396, fill=PALE, w=4, r=22)
    el(img, 540, 192, 8, fill=YEL, out=K, w=3); ln(img, [(540, 184), (540, 168)], K, 4)
    flag(img, 300, 140, 410); flag(img, 760, 140, 410)
    for x in (200, 880): diya(img, x, 388, 0.5)

def a_army(img):
    cx = 540
    # ribbon
    poly(img, [(cx - 70, 110), (cx - 10, 110), (cx + 20, 230), (cx - 40, 230)], GREEN, K, 4)
    poly(img, [(cx + 70, 110), (cx + 10, 110), (cx - 20, 230), (cx + 40, 230)], YEL, K, 4)
    # medal
    glow(img, cx, 300, 120, (250, 204, 21), 0.35)
    el(img, cx, 300, 84, fill=YEL, out=K, w=6); el(img, cx, 300, 64, fill=None, out=GOLD, w=3)
    star5(img, cx, 300, 48, WHITE, K)
    # wreath
    for sg in (-1, 1):
        for i in range(10):
            t = i / 9; y = 170 + 230 * t; x = cx + sg * (170 + 34 * math.sin(math.pi * t))
            D(img).ellipse(P((x - 14, y - 7), (x + 14, y + 7)), fill=GREEN if i % 2 else (34, 197, 94))
            if i % 3 == 1: el(img, x + sg * 8, y + 10, 6, fill=YEL, out=None)
    for x, y in [(250, 170), (830, 170), (240, 340), (840, 340)]: star5(img, x, y, 14, YEL, K)

def a_republic(img):
    cx = 540
    # India Gate line art
    rect(img, cx - 130, 170, cx + 130, 404, fill=WHITE, out=K, w=5)
    D(img).rectangle(P((cx - 52, 250), (cx + 52, 404)), fill=(240, 253, 244))
    pts = bez((cx - 52, 404), (cx - 52, 220), (cx, 220), 14) + bez((cx, 220), (cx + 52, 220), (cx + 52, 404), 14)
    D(img).polygon(P(*pts), fill=PALE); ln(img, pts, K, 5)
    rect(img, cx - 150, 150, cx + 150, 172, fill=YEL, out=K, w=4)
    rect(img, cx - 110, 120, cx + 110, 150, fill=WHITE, out=K, w=4)
    D(img).chord(P((cx - 50, 90), (cx + 50, 150)), 180, 360, fill=HL, outline=K, width=int(4 * S))
    for x in (cx - 100, cx + 100): rect(img, x - 14, 200, x + 14, 404, fill=PALE, out=K, w=3)
    chakra(img, 250, 270, 70); chakra(img, 830, 270, 70)
    ground(img, 406, 150, 930)

def a_ramzan(img):
    glow(img, 540, 230, 200, (254, 236, 140), 0.45)
    crescent(img, 520, 230, 110, YEL)
    star5(img, 620, 180, 26, YEL, K)
    lantern(img, 280, 150, 1.2); lantern(img, 800, 130, 1.0); lantern(img, 900, 200, 0.8); lantern(img, 180, 210, 0.8)
    for x, y in [(380, 330), (700, 330), (420, 150), (720, 120)]: star5(img, x, y, 10, GOLD)
    # mosque-free skyline of arches
    for i, x in enumerate(range(380, 720, 68)):
        rect(img, x, 360, x + 56, 406, fill=PALE, out=K, w=3, r=26)

def a_valentine(img):
    heart_shape(img, 540, 250, 110, GREEN); heart_shape(img, 540, 255, 70, YEL)
    text(img, (540, 240), '♥', 1, YEL, PB, 'mm')
    heart_shape(img, 330, 210, 40, YEL); heart_shape(img, 760, 200, 46, GREEN); heart_shape(img, 260, 340, 26, GREEN); heart_shape(img, 830, 330, 30, YEL)
    gift(img, 640, 340, 80, 60, YEL, GREEN)
    # rose
    el(img, 410, 330, 24, fill=YEL, out=K, w=3); D(img).arc(P((396, 316), (424, 344)), 0, 270, fill=K, width=int(3 * S))
    ln(img, [(410, 354), (406, 410)], GREEN, 5); D(img).ellipse(P((380, 372), (406, 386)), fill=GREEN)

def a_shivaji(img):
    # fort walls + flag + shield and sword
    ln(img, [(150, 404), (930, 404)], LINEC, 3)
    for x0, x1, top in [(220, 420, 290), (420, 660, 230), (660, 860, 300)]:
        rect(img, x0, top, x1, 404, fill=PALE, out=K, w=5)
        for x in range(int(x0), int(x1), 40): rect(img, x, top - 22, x + 22, top, fill=PALE, out=K, w=4)
    rect(img, 500, 320, 580, 404, fill=GREEN, out=K, w=5, r=40); D(img).rectangle(P((502, 364), (578, 402)), fill=GREEN)
    flag(img, 540, 110, 206)
    # shield
    el(img, 880, 220, 54, fill=YEL, out=K, w=5)
    for a in (45, 135, 225, 315): el(img, 880 + 26 * math.cos(math.radians(a)), 220 + 26 * math.sin(math.radians(a)), 6, fill=K, out=None)
    ln(img, [(150, 140), (290, 320)], K, 7); ln(img, [(170, 180), (205, 152)], K, 6)

def a_science(img):
    # atom + flask + microscope
    for a in (0, 60, 120):
        m = Image.new('RGBA', (int(300 * S), int(140 * S)), (0, 0, 0, 0))
        ImageDraw.Draw(m).ellipse((4 * S, 4 * S, 296 * S, 136 * S), outline=GREEN + (255,), width=int(5 * S))
        m = m.rotate(a, expand=True, resample=Image.BICUBIC)
        img.paste(m, (int(540 * S - m.size[0] / 2), int(250 * S - m.size[1] / 2)), m)
    el(img, 540, 250, 22, fill=YEL, out=K, w=4)
    for (x, y) in [(680, 250), (470, 140), (470, 360)]: el(img, x, y, 9, fill=K, out=None)
    # flask
    poly(img, [(230, 180), (270, 180), (270, 260), (320, 380), (180, 380), (230, 260)], WHITE, K, 5)
    poly(img, [(212, 320), (288, 320), (320, 380), (180, 380)], HL, None); ln(img, [(180, 380), (320, 380)], K, 5)
    for x, y in [(240, 350), (262, 336), (252, 300)]: el(img, x, y, 6, fill=GREEN, out=None)
    # microscope
    rect(img, 790, 380, 900, 404, fill=YEL, out=K, w=4, r=6)
    ln(img, [(840, 380), (840, 300), (880, 260)], K, 8)
    rect(img, 816, 170, 846, 270, fill=GREEN, out=K, w=4, r=6)
    rect(img, 806, 330, 880, 342, fill=K, out=None)

def a_women(img):
    # woman symbol + flowers + rising arrow
    el(img, 540, 220, 92, fill=WHITE, out=GREEN, w=14)
    ln(img, [(540, 312), (540, 400)], GREEN, 14); ln(img, [(500, 360), (580, 360)], GREEN, 14)
    flower(img, 540, 220, 52, YEL)
    for (x, y, r) in [(290, 230, 30), (800, 220, 34), (230, 350, 22), (860, 350, 24)]: flower(img, x, y, r, YEL if r > 25 else GREEN, GREEN if r > 25 else YEL)
    sparkles(img, [(380, 140, 12), (700, 130, 14)])

def a_eid(img):
    glow(img, 540, 220, 200, (254, 236, 140), 0.45)
    crescent(img, 540, 210, 96, YEL); star5(img, 626, 166, 22, YEL, K)
    lantern(img, 300, 130, 1.1); lantern(img, 780, 130, 1.1)
    # sevaiyan bowl
    D(img).chord(P((450, 306), (630, 396)), 0, 180, fill=YEL, outline=K, width=int(5 * S))
    for i in range(6): ln(img, bez((470 + i * 24, 348), (480 + i * 24, 326), (494 + i * 24, 348), 8), GOLD, 3)
    el(img, 506, 336, 7, fill=GREEN, out=None); el(img, 574, 336, 7, fill=GREEN, out=None)
    for x, y in [(180, 300), (900, 300), (420, 140), (660, 120)]: star5(img, x, y, 10, GOLD)

def a_holi(img):
    # colour splashes + pichkari + gulal bowls
    random.seed(4)
    for cx, cy, r, c in [(320, 220, 90, YEL), (720, 210, 100, (187, 247, 208)), (540, 300, 80, HL), (230, 340, 50, (187, 247, 208)), (860, 340, 56, YEL)]:
        for k in range(14):
            a = random.uniform(0, 6.28); rr = random.uniform(0.2, 1.0) * r
            el(img, cx + rr * math.cos(a), cy + rr * math.sin(a), random.uniform(10, 30), fill=c, out=None)
        el(img, cx, cy, r * 0.55, fill=c, out=None)
    # pichkari
    rect(img, 420, 180, 600, 220, fill=GREEN, out=K, w=4, r=12); rect(img, 600, 192, 680, 208, fill=YEL, out=K, w=3)
    rect(img, 380, 192, 420, 208, fill=YEL, out=K, w=3); rect(img, 370, 176, 386, 224, fill=K, out=None)
    for i in range(5): el(img, 700 + i * 22, 200 - i * 6, 6 - i * 0.6, fill=GREEN, out=None)
    for x, c in [(420, YEL), (540, GREEN), (660, (187, 247, 208))]:
        D(img).chord(P((x - 50, 314), (x + 50, 394)), 0, 180, fill=WHITE, outline=K, width=int(4 * S))
        D(img).chord(P((x - 40, 302), (x + 40, 366)), 180, 360, fill=c)

def a_goodfriday(img):
    glow(img, 540, 240, 220, (254, 243, 170), 0.5)
    rays(img, 540, 230, 120, 170, 32, 0.6, (250, 222, 90), 4)
    rect(img, 524, 120, 556, 404, fill=PALE, out=K, w=5, r=4); rect(img, 450, 180, 630, 212, fill=PALE, out=K, w=5, r=4)
    ground(img, 404, 300, 780)
    for x in (360, 720): lotus(img, x, 402, 0.5)

def a_ambedkar(img):
    book(img, 540, 300, 360, 170, WHITE)
    text(img, (450, 280), 'संविधान', 30, K, PB, 'mm')
    chakra(img, 630, 280, 44)
    # lamp of knowledge
    diya(img, 540, 196, 0.7)
    rays(img, 540, 160, 70, 110, 20, 0.0, YEL, 4)
    sparkles(img, [(250, 200, 14), (830, 200, 14)])
    # pen
    poly(img, [(820, 380), (900, 220), (920, 230), (840, 390)], GREEN, K, 4); poly(img, [(820, 380), (840, 390), (818, 404)], YEL, K, 3)

def a_ramnavami(img):
    cx, cy = 540, 268
    toran(img, 20, 380); toran(img, 700, 1060)
    for i in range(24):
        a = i * math.pi / 12
        if math.sin(a) > 0.45: continue
        r1 = 150 if i % 2 else 168
        ln(img, [(cx + 128 * math.cos(a), cy + 128 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], YEL, 6)
    el(img, cx, cy, 112, fill=HL, out=YEL, w=5)
    rect(img, 392, 362, 688, 384); rect(img, 422, 346, 658, 362); rect(img, 448, 254, 632, 346)
    rect(img, 513, 282, 567, 352, fill=GREEN, w=5, r=26)
    for x in (474, 606): ln(img, [(x, 268), (x, 340)], K, 4)
    l_ = bez((456, 254), (468, 172), (540, 140), 30); r_ = bez((540, 140), (612, 172), (624, 254), 30)
    D(img).polygon(P(*(l_ + r_)), fill=(254, 249, 195)); ln(img, l_); ln(img, r_)
    for yy in (222, 192, 166):
        hw = 84 * (1 - ((254 - yy) / 114) ** 1.6); ln(img, [(540 - hw, yy), (540 + hw, yy)], GOLD, 3)
    el(img, 540, 136, 16, 10, fill=YEL, out=K, w=4); el(img, 540, 118, 8, 10, fill=YEL, out=K, w=3)
    ln(img, [(540, 108), (540, 60)], K, 4); poly(img, [(540, 60), (598, 74), (540, 92)], YEL, K, 4)
    for sg in (-1, 1):
        bx = 540 + sg * 250
        D(img).arc(P((bx - 40, 220), (bx + 40, 360)), 90 if sg < 0 else 270, 270 if sg < 0 else 90, fill=GREEN, width=int(5 * S))
        ln(img, [(bx, 220), (bx, 360)], GREEN, 2); ln(img, [(bx - sg * 10, 290), (bx + sg * 70, 290)], GREEN, 4)
        tip = bx + sg * 70; poly(img, [(tip + sg * 18, 290), (tip, 280), (tip, 300)], GREEN, None)

def a_labour(img):
    gear(img, 470, 250, 110, 12, WHITE); gear(img, 650, 330, 70, 9, PALE)
    # hammer + wrench crossed
    ln(img, [(200, 380), (320, 200)], K, 10); rect(img, 290, 170, 360, 205, fill=YEL, out=K, w=4, r=6)
    ln(img, [(880, 380), (760, 200)], K, 10)
    el(img, 752, 186, 30, fill=YEL, out=K, w=4); el(img, 744, 174, 12, fill=WHITE, out=None)
    # helmet
    D(img).chord(P((800, 290), (940, 400)), 180, 360, fill=YEL, outline=K, width=int(5 * S)); ln(img, [(790, 345), (950, 345)], K, 6)

def a_akshaya(img):
    kalash(img, 540, 404, 1.25)
    for x, y, r in [(310, 360, 34), (370, 330, 28), (250, 320, 24), (770, 360, 34), (710, 330, 28), (830, 320, 24)]: coin(img, x, y, r)
    sparkles(img, [(300, 170, 16), (780, 160, 16), (400, 120, 10), (680, 120, 10)])
    rays(img, 540, 200, 150, 190, 24, 0.3, (250, 222, 90), 4)

def a_tech(img):
    # chip + rocket
    rect(img, 430, 170, 650, 390, fill=WHITE, out=K, w=6, r=18)
    rect(img, 480, 220, 600, 340, fill=HL, out=K, w=4, r=10)
    for i in range(5):
        for (x0, y0, x1, y1) in [(450 + i * 40, 170, 450 + i * 40, 140), (450 + i * 40, 390, 450 + i * 40, 420), (430, 190 + i * 40, 400, 190 + i * 40), (650, 190 + i * 40, 680, 190 + i * 40)]:
            ln(img, [(x0, y0), (x1, y1)], GREEN, 5)
    text(img, (540, 280), 'AI', 54, K, PB, 'mm')
    # rocket left
    poly(img, [(250, 150), (280, 210), (280, 330), (220, 330), (220, 210)], WHITE, K, 5)
    el(img, 250, 240, 14, fill=YEL, out=K, w=3)
    poly(img, [(220, 290), (190, 340), (220, 330)], GREEN, K, 3); poly(img, [(280, 290), (310, 340), (280, 330)], GREEN, K, 3)
    poly(img, [(232, 334), (268, 334), (250, 390)], YEL, None)
    # circuit right
    for k, y in enumerate((200, 260, 320)):
        ln(img, [(700, y), (790, y), (820, y - 30 + k * 30), (900, y - 30 + k * 30)], GREEN, 4); el(img, 905, y - 30 + k * 30, 9, fill=YEL, out=K, w=3)

def a_father(img):
    # shirt + tie + mug + photo frame
    poly(img, [(420, 160), (480, 140), (540, 180), (600, 140), (660, 160), (700, 260), (650, 270), (650, 400), (430, 400), (430, 270), (380, 260)], WHITE, K, 5)
    poly(img, [(520, 180), (560, 180), (552, 205), (528, 205)], GREEN, K, 3)
    poly(img, [(528, 205), (552, 205), (570, 330), (540, 360), (510, 330)], GREEN, K, 4)
    for y in (240, 280, 320): ln(img, [(520, y), (560, y + 12)], YEL, 4)
    # mug
    rect(img, 200, 300, 290, 404, fill=YEL, out=K, w=5, r=10); D(img).arc(P((272, 320), (322, 380)), 270, 90, fill=K, width=int(5 * S))
    text(img, (245, 350), 'PAPA', 18, K, PB, 'mm') if False else heart_shape(img, 245, 346, 20, GREEN)
    # photo frame
    rect(img, 780, 180, 900, 300, fill=WHITE, out=K, w=5, r=8)
    poly(img, [(792, 288), (820, 250), (840, 270), (860, 244), (888, 288)], GREEN, None); el(img, 870, 210, 10, fill=YEL, out=None)
    sparkles(img, [(300, 180, 12), (760, 360, 10)])

def a_yoga(img):
    sun(img, 540, 230, 80, 0.5)
    # meditation figure (simple)
    el(img, 540, 250, 22, fill=GREEN, out=None)
    poly(img, [(540, 274), (580, 330), (500, 330)], GREEN, None)
    ln(img, [(510, 296), (470, 330), (500, 352)], GREEN, 10); ln(img, [(570, 296), (610, 330), (580, 352)], GREEN, 10)
    D(img).ellipse(P((440, 330), (640, 380)), fill=GREEN)
    rect(img, 380, 384, 700, 400, fill=YEL, out=K, w=3, r=8)
    lotus(img, 230, 400, 0.7); lotus(img, 850, 400, 0.7)

def a_gurupurnima(img):
    glow(img, 540, 200, 160, (254, 243, 170), 0.6)
    el(img, 540, 200, 92, fill=HL, out=YEL, w=6)
    for x, y, r in [(510, 180, 14), (570, 220, 10), (540, 160, 7)]: el(img, x, y, r, fill=(250, 222, 90), out=None)
    book(img, 540, 350, 280, 90, WHITE)
    diya(img, 280, 400, 0.6); diya(img, 800, 400, 0.6)
    for x, y in [(250, 170), (830, 160), (330, 260), (760, 250)]: star5(img, x, y, 9, GOLD)

def a_friendship(img):
    # friendship bands + two linked circles
    for i, (x, c) in enumerate([(430, YEL), (650, GREEN)]):
        el(img, x, 260, 110, 64, fill=None, out=c, w=18)
        for k in range(10):
            a = k * math.pi / 5
            el(img, x + 110 * math.cos(a), 260 + 64 * math.sin(a), 7, fill=WHITE, out=K, w=2)
    heart_shape(img, 540, 250, 30, GREEN)
    sparkles(img, [(250, 160, 14), (840, 160, 14), (250, 360, 10), (840, 360, 10)])

def a_independence(img):
    # Red Fort line art (green/yellow) + kites + chakra
    cx = 540
    rect(img, cx - 220, 300, cx + 220, 404, fill=PALE, out=K, w=5)
    for x in range(cx - 210, cx + 211, 30): rect(img, x, 286, x + 16, 300, fill=PALE, out=K, w=3)
    rect(img, cx - 60, 240, cx + 60, 300, fill=WHITE, out=K, w=5)
    rect(img, cx - 30, 340, cx + 30, 404, fill=GREEN, out=K, w=4, r=30); D(img).rectangle(P((cx - 28, 372), (cx + 28, 402)), fill=GREEN)
    for x in (cx - 200, cx + 200, cx - 40, cx + 40):
        D(img).chord(P((x - 22, 200), (x + 22, 250)), 180, 360, fill=HL, outline=K, width=int(3 * S))
        rect(img, x - 18, 225, x + 18, 240 if abs(x - cx) > 100 else 240, fill=WHITE, out=K, w=3)
        if abs(x - cx) > 100: rect(img, x - 18, 240, x + 18, 300, fill=WHITE, out=K, w=3)
    chakra(img, cx, 165, 42)
    kite(img, 230, 170, 0.8, YEL, GREEN, -10); kite(img, 860, 160, 0.8, GREEN, YEL, 12)

def a_rakhi(img):
    # rakhi
    ln(img, bez((180, 260), (360, 230), (440, 250)), GOLD, 6); ln(img, bez((640, 250), (720, 230), (900, 260)), GOLD, 6)
    flower(img, 540, 250, 110, YEL, GREEN)
    el(img, 540, 250, 52, fill=WHITE, out=K, w=5); el(img, 540, 250, 30, fill=GREEN, out=K, w=3); star5(img, 540, 250, 16, YEL)
    for x in (190, 890):
        ln(img, [(x, 260), (x - 10, 330)], GOLD, 4); el(img, x - 10, 338, 9, fill=YEL, out=K, w=2)
    # thali
    el(img, 540, 384, 150, 22, fill=YEL, out=K, w=4)
    diya(img, 470, 380, 0.4); el(img, 600, 370, 14, fill=GREEN, out=K, w=2)

def a_janmashtami(img):
    # flute + peacock feather + matki
    poly(img, [(220, 330), (850, 190), (856, 214), (226, 354)], YEL, K, 5)
    for k in range(6):
        x = 420 + k * 70; y = 330 - (x - 220) * 140 / 630 - 2
        el(img, x, y + 4, 6, fill=K, out=None)
    # feather
    fx, fy = 760, 160
    ln(img, bez((fx - 60, fy + 230), (fx - 40, fy + 100), (fx, fy)), GREEN, 4)
    el(img, fx, fy + 10, 46, 70, fill=(187, 247, 208), out=GREEN, w=3); el(img, fx, fy + 18, 26, 36, fill=YEL, out=None); el(img, fx, fy + 22, 12, 16, fill=DEEP, out=None)
    # matki
    el(img, 330, 210, 60, 52, fill=YEL, out=K, w=5); rect(img, 300, 150, 360, 168, fill=YEL, out=K, w=4, r=6)
    D(img).chord(P((296, 150), (364, 180)), 180, 360, fill=WHITE)
    ln(img, [(330, 100), (330, 150)], K, 3)

def a_sports(img):
    trophy(img, 540, 404, 1.35)
    # hockey stick + ball
    ln(img, [(220, 150), (280, 380)], K, 10); ln(img, bez((280, 380), (300, 404), (340, 390), 10), K, 10)
    el(img, 370, 390, 13, fill=YEL, out=K, w=3)
    # football
    el(img, 820, 330, 56, fill=WHITE, out=K, w=5)
    poly(img, [(820, 306), (842, 322), (834, 348), (806, 348), (798, 322)], K, None)
    for x, y in [(240, 140), (860, 170)]: star5(img, x, y, 14, YEL, K)

def a_ganesh(img):
    # modak plate + toran + umbrella-like chhatri + diyas (symbolic)
    toran(img, 60, 520, 120, 26, 8); toran(img, 560, 1020, 120, 26, 8)
    D(img).chord(P((360, 230), (720, 396)), 0, 180, fill=YEL, outline=K, width=int(5 * S))
    ln(img, [(360, 313), (720, 313)], K, 5)
    for (x, y, s) in [(450, 278, 1), (540, 248, 1.2), (630, 278, 1), (495, 296, 0.8), (585, 296, 0.8)]:
        pts = [(x, y - 48 * s)] + bez((x + 34 * s, y - 6 * s), (x + 30 * s, y + 24 * s), (x, y + 24 * s), 8) + bez((x, y + 24 * s), (x - 30 * s, y + 24 * s), (x - 34 * s, y - 6 * s), 8)
        D(img).polygon(P(*pts), fill=(254, 249, 195)); ln(img, pts + [pts[0]], K, 4)
        for k in (-1, 0, 1): ln(img, [(x, y - 44 * s), (x + k * 18 * s, y + 18 * s)], GOLD, 2)
    diya(img, 250, 400, 0.6); diya(img, 830, 400, 0.6)
    sparkles(img, [(540, 180, 16), (400, 200, 9), (680, 200, 9)])

def a_teachers(img):
    rect(img, 340, 140, 740, 360, fill=(22, 101, 52), out=K, w=8, r=10)
    text(img, (540, 210), 'ज्ञान', 56, WHITE, PB, 'mm')
    text(img, (540, 290), 'A B C  •  1 2 3', 34, YEL, PB, 'mm')
    rect(img, 360, 360, 720, 374, fill=YEL, out=K, w=3)
    # mortarboard
    poly(img, [(220, 220), (300, 190), (380, 220), (300, 250)], K, None); rect(img, 262, 232, 338, 262, fill=K, out=None, r=6)
    ln(img, [(360, 222), (360, 270)], YEL, 4); el(img, 360, 276, 7, fill=YEL, out=None)
    book(img, 860, 330, 150, 80, WHITE)
    ln(img, [(820, 160), (900, 260)], GREEN, 10); poly(img, [(900, 260), (912, 276), (894, 268)], YEL, None)

def a_hindi(img):
    rect(img, 410, 130, 670, 390, fill=WHITE, out=K, w=6, r=30)
    rrect(img, (426, 146, 654, 374), 22, fill=HL)
    text(img, (540, 255), 'अ', 170, K, PB, 'mm')
    # pen nib
    poly(img, [(780, 380), (820, 200), (860, 380), (820, 420)], YEL, K, 5); ln(img, [(820, 240), (820, 380)], K, 3); el(img, 820, 300, 8, fill=K, out=None)
    for (t, x, y) in [('क', 250, 200), ('ख', 300, 320), ('ग', 200, 330)]: text(img, (x, y), t, 50, GREEN, PB, 'mm')

def a_visarjan(img):
    # waves + flowers + diya boat
    for k, y in enumerate((340, 370, 400)):
        pts = [(80 + i * 23, y + 10 * math.sin(i * 0.7 + k)) for i in range(41)]
        ln(img, pts, GREEN if k % 2 else LINEC, 5)
    D(img).chord(P((440, 270), (640, 360)), 0, 180, fill=YEL, outline=K, width=int(5 * S))
    diya(img, 540, 300, 0.7)
    for x, y in [(300, 330), (760, 320), (220, 290), (860, 280)]: flower(img, x, y, 22, YEL)
    sparkles(img, [(380, 150, 12), (700, 150, 12), (540, 120, 9)])

def a_engineers(img):
    # bridge + gear + compass
    ln(img, [(120, 380), (960, 380)], K, 6)
    pts = bez((180, 380), (540, 120), (900, 380), 40)
    ln(img, pts, GREEN, 8)
    for i in range(1, 12):
        x = 180 + i * 60; y = [p for p in pts if abs(p[0] - x) < 12][0][1]
        ln(img, [(x, y), (x, 380)], K, 3)
    for x in (300, 780): rect(img, x - 14, 240, x + 14, 404, fill=YEL, out=K, w=4)
    gear(img, 540, 210, 40, 8, YEL)

def a_gandhi(img):
    # round glasses + charkha + wheat
    el(img, 450, 200, 54, fill=WHITE, out=K, w=7); el(img, 630, 200, 54, fill=WHITE, out=K, w=7)
    D(img).arc(P((500, 180), (580, 220)), 200, 340, fill=K, width=int(7 * S))
    ln(img, [(396, 196), (340, 180)], K, 6); ln(img, [(684, 196), (740, 180)], K, 6)
    # charkha wheel
    el(img, 540, 340, 56, fill=None, out=GREEN, w=6)
    for i in range(8):
        a = i * math.pi / 4; ln(img, [(540, 340), (540 + 56 * math.cos(a), 340 + 56 * math.sin(a))], GREEN, 3)
    rect(img, 470, 396, 700, 410, fill=YEL, out=K, w=3)
    # wheat (Jai Kisan)
    for x in (220, 860):
        ln(img, [(x, 404), (x, 260)], GOLD, 5)
        for k in range(5):
            y = 270 + k * 22
            D(img).ellipse(P((x - 18, y - 8), (x - 2, y + 8)), fill=YEL); D(img).ellipse(P((x + 2, y - 8), (x + 18, y + 8)), fill=YEL)

def a_durga(img):
    # trishul + lotus + drum (dhak)
    ln(img, [(540, 140), (540, 400)], K, 8)
    ln(img, bez((470, 160), (480, 250), (540, 250), 12), K, 8); ln(img, bez((610, 160), (600, 250), (540, 250), 12), K, 8)
    for x in (470, 540, 610): poly(img, [(x, 110 if x == 540 else 130), (x - 14, 160), (x + 14, 160)], YEL, K, 4)
    lotus(img, 540, 404, 0.9)
    # dhak
    el(img, 260, 300, 70, 44, fill=YEL, out=K, w=5); el(img, 220, 300, 18, 40, fill=WHITE, out=K, w=4)
    for k in range(4): ln(img, [(220 + k * 22, 262), (240 + k * 22, 338)], GREEN, 3)
    for i in range(5): ln(img, [(260 + i * 6, 256), (250 + i * 10, 200)], (187, 247, 208), 4)
    sun(img, 830, 250, 50, 0.6)

def a_dussehra(img):
    # bow & arrow aimed at a burning effigy silhouette
    D(img).arc(P((150, 140), (310, 400)), 270, 90, fill=GREEN, width=int(7 * S))
    ln(img, [(230, 140), (230, 400)], K, 2)
    ln(img, [(220, 270), (640, 270)], K, 6); poly(img, [(670, 270), (632, 254), (640, 270), (632, 286)], K, None)
    # victory bonfire
    glow(img, 820, 300, 110, (250, 204, 21), 0.4)
    for (dx, h, w_, col) in [(-50, 120, 40, YEL), (50, 120, 40, YEL), (0, 190, 56, (250, 222, 90)), (0, 120, 30, (255, 251, 225))]:
        x = 820 + dx; by = 380
        pts = bez((x - w_, by), (x - w_ * 0.6, by - h * 0.7), (x, by - h), 14) + bez((x, by - h), (x + w_ * 0.6, by - h * 0.7), (x + w_, by), 14)
        D(img).polygon(P(*pts), fill=col)
    for k in range(3): ln(img, [(740 + k * 20, 404), (900 - k * 20, 372)], K, 7)
    text(img, (480, 360), 'विजय', 44, GREEN, PB, 'mm')

def a_dhanteras(img):
    kalash(img, 400, 404, 1.0)
    for x, y, r in [(640, 380, 34), (700, 350, 30), (760, 380, 34), (700, 300, 26), (820, 340, 26)]: coin(img, x, y, r)
    diya(img, 900, 404, 0.5); diya(img, 200, 404, 0.5)
    sparkles(img, [(560, 150, 16), (760, 160, 12), (300, 140, 10)])

def a_diwali(img):
    lights(img)
    cx, cy = 540, 300
    dots_arc(img, cx, cy, 190, 28, GREEN, 4); dots_arc(img, cx, cy, 150, 20, YEL, 4)
    diya(img, 300, 380, 0.75); diya(img, 780, 380, 0.75); diya(img, 540, 370, 1.15)
    sparkles(img, [(190, 250, 14), (890, 240, 16), (170, 380, 8), (920, 380, 9)])

def a_bhaidooj(img):
    el(img, 540, 330, 220, 40, fill=YEL, out=K, w=5)
    diya(img, 420, 320, 0.6)
    el(img, 540, 300, 30, 18, fill=WHITE, out=K, w=3); el(img, 540, 296, 10, 6, fill=GREEN, out=None)
    gift(img, 610, 260, 90, 56, GREEN, YEL)
    # tilak symbol above
    el(img, 540, 170, 70, fill=PALE, out=YEL, w=5)
    poly(img, [(540, 120), (556, 170), (540, 214), (524, 170)], GREEN, None); el(img, 540, 176, 8, fill=YEL, out=None)
    for x, y in [(260, 200), (820, 200)]: flower(img, x, y, 30, YEL)

def a_mp(img):
    # Sanchi stupa + torana gate
    cx = 560
    D(img).chord(P((cx - 170, 220), (cx + 170, 520)), 180, 360, fill=PALE, outline=K, width=int(5 * S))
    rect(img, cx - 190, 366, cx + 190, 404, fill=WHITE, out=K, w=5)
    rect(img, cx - 34, 196, cx + 34, 220, fill=YEL, out=K, w=4); ln(img, [(cx, 196), (cx, 160)], K, 4)
    rect(img, cx - 40, 150, cx + 40, 162, fill=GREEN, out=K, w=3)
    for x in range(cx - 160, cx + 161, 20): ln(img, [(x, 366), (x, 404)], LINEC, 2)
    # torana
    tx = 230
    for x in (tx - 60, tx + 60): rect(img, x - 10, 230, x + 10, 404, fill=YEL, out=K, w=4)
    for y in (220, 260, 300): rect(img, tx - 100, y, tx + 100, y + 16, fill=WHITE, out=K, w=4, r=8)
    for x, y in [(870, 160), (930, 240)]: star5(img, x, y, 12, GOLD)

def a_children(img):
    balloon(img, 300, 180, 1.0, YEL); balloon(img, 380, 150, 0.9, GREEN); balloon(img, 230, 230, 0.8, (187, 247, 208))
    kite(img, 820, 180, 0.9, YEL, GREEN, 10)
    # toy blocks
    for (x, y, c, t) in [(470, 330, YEL, 'A'), (560, 330, GREEN, 'B'), (515, 250, (187, 247, 208), 'C')]:
        rect(img, x - 40, y - 40, x + 40, y + 40, fill=c, out=K, w=4, r=8); text(img, (x, y), t, 40, K, PB, 'mm')
    # rose
    el(img, 760, 340, 22, fill=YEL, out=K, w=3); ln(img, [(760, 362), (758, 404)], GREEN, 5)

# map art key -> function
ART = dict(gurunanak=a_gurunanak, maths=a_maths, christmas=a_christmas, christmas2=lambda i: a_christmas(i, 1),
           ny27=lambda i: a_newyear(i, '2027'), ny28=lambda i: a_newyear(i, '2028'), youth=a_youth, sankranti=a_sankranti,
           gurugobind=a_gurugobind, army=a_army, republic=a_republic, ramzan=a_ramzan, valentine=a_valentine, shivaji=a_shivaji,
           science=a_science, women=a_women, eid=a_eid, holi=a_holi, goodfriday=a_goodfriday, ambedkar=a_ambedkar,
           ramnavami=a_ramnavami, labour=a_labour, akshaya=a_akshaya, tech=a_tech, father=a_father, yoga=a_yoga,
           gurupurnima=a_gurupurnima, friendship=a_friendship, independence=a_independence, rakhi=a_rakhi,
           janmashtami=a_janmashtami, sports=a_sports, ganesh=a_ganesh, teachers=a_teachers, hindi=a_hindi,
           visarjan=a_visarjan, engineers=a_engineers, gandhi=a_gandhi, durga=a_durga, dussehra=a_dussehra,
           dhanteras=a_dhanteras, diwali=a_diwali, bhaidooj=a_bhaidooj, mp=a_mp, children=a_children)
