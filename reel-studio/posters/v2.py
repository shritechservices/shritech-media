"""ShriTech festival poster v2: clean, solid colours, line-art illustration + vector 'how it works' diagram."""
import sys; sys.path.insert(0, '/home/claude/posters')
from fest import *

LIGHT = dict(bg=WHITE, ink=DEEP, acc=GREEN, soft=MINT, hi=YEL, sub=(55, 80, 64), node=MINT, nodeic=DEEP,
             line=(134, 199, 157), card=WHITE, band=DEEP, bandtxt=WHITE, num=YEL, dark=False)
DARK = dict(bg=BLACK, ink=WHITE, acc=LGREEN, soft=(16, 30, 21), hi=YEL, sub=(190, 210, 197), node=(16, 32, 22), nodeic=YEL,
            line=(52, 120, 76), card=(14, 24, 17), band=YEL, bandtxt=BLACK, num=BLACK, dark=True)

def L(img):
    return ImageDraw.Draw(img)

def P(*pts):
    return [(x * S, y * S) for x, y in pts]

def dashed(img, pts, color, w=3, dash=12, gap=10):
    d = L(img)
    segs = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L_ = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L_ / (dash + gap)))
        for i in range(n):
            t0 = i * (dash + gap) / L_; t1 = min(1, t0 + dash / L_)
            d.line(P((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0), (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)), fill=color, width=int(w * S))

def bez(p0, p1, p2, n=40):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in [i / n for i in range(n + 1)]]

# ---------------- line icons (centre cx,cy; fits radius ~34) ----------------
def ic_ai(img, cx, cy, c, hi):
    def star(x, y, r, col):
        pts = []
        for i in range(8):
            a = i * math.pi / 4 - math.pi / 2; rr = r if i % 2 == 0 else r * 0.3
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        L(img).polygon(P(*pts), fill=col)
    star(cx - 6, cy + 4, 30, c); star(cx + 22, cy - 20, 13, hi); star(cx + 20, cy + 22, 8, hi)

def ic_social(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 38, cy - 22), (cx - 2, cy + 14)), 9 * S, outline=c, width=5 * S)
    text(img, (cx - 20, cy - 3), 'f', 30, c, PB, 'mm')
    d.rounded_rectangle(P((cx - 2, cy - 12), (cx + 36, cy + 26)), 11 * S, fill=bg, outline=c, width=5 * S)
    d.ellipse(P((cx + 7, cy - 3), (cx + 27, cy + 17)), outline=c, width=4 * S)
    d.ellipse(P((cx + 26, cy - 8), (cx + 31, cy - 3)), fill=hi)

def ic_wa(img, cx, cy, c, hi, bg):
    d = L(img)
    d.ellipse(P((cx - 30, cy - 30), (cx + 30, cy + 30)), outline=c, width=5 * S)
    d.polygon(P((cx - 22, cy + 16), (cx - 34, cy + 34), (cx - 10, cy + 26)), fill=c)
    # handset
    d.arc(P((cx - 14, cy - 14), (cx + 14, cy + 14)), 100, 260, fill=c, width=6 * S)
    d.ellipse(P((cx - 5, cy - 17), (cx + 5, cy - 9)), fill=c); d.ellipse(P((cx - 5, cy + 9), (cx + 5, cy + 17)), fill=c)
    # many-people badge
    d.ellipse(P((cx + 14, cy - 40), (cx + 44, cy - 10)), fill=hi)
    text(img, (cx + 29, cy - 25), '+', 26, DEEP, PB, 'mm')

def ic_lang(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 36, cy - 26), (cx + 4, cy + 14)), 9 * S, fill=c)
    text(img, (cx - 16, cy - 7), 'अ', 26, bg, PB, 'mm')
    d.rounded_rectangle(P((cx - 6, cy - 10), (cx + 36, cy + 30)), 9 * S, fill=bg, outline=c, width=5 * S)
    text(img, (cx + 15, cy + 10), 'A', 26, c, PB, 'mm')

# ---------------- vector phone ----------------
def vphone(img, x, y, w, h, T, poster_fn, lines):
    d = L(img)
    shadow(img, (x, y, x + w, y + h), 34, blur=20, alpha=0.25 if not T['dark'] else 0.5, off=10, color=DEEP if not T['dark'] else (0, 0, 0))
    d.rounded_rectangle(P((x, y), (x + w, y + h)), 34 * S, fill=(18, 30, 22) if not T['dark'] else (40, 52, 44))
    sx0, sy0, sx1, sy1 = x + 10, y + 10, x + w - 10, y + h - 10
    d.rounded_rectangle(P((sx0, sy0), (sx1, sy1)), 26 * S, fill=WHITE if not T['dark'] else (10, 16, 12))
    d.rounded_rectangle(P((x + w / 2 - 30, y + 18), (x + w / 2 + 30, y + 28)), 5 * S, fill=(18, 30, 22) if not T['dark'] else (40, 52, 44))
    # app bar
    text(img, (sx0 + 16, sy0 + 42), 'Shri', 17, DEEP if not T['dark'] else WHITE, PB, 'lm')
    text(img, (sx0 + 16 + tw('Shri ', 17, PB), sy0 + 42), 'Tech', 17, GREEN if not T['dark'] else LGREEN, PB, 'lm')
    d.rounded_rectangle(P((sx1 - 58, sy0 + 30), (sx1 - 12, sy0 + 54)), 12 * S, fill=GREEN)
    # poster
    px0, py0, px1, py1 = sx0 + 14, sy0 + 68, sx1 - 14, sy0 + 68 + (sx1 - sx0 - 28) * 1.0
    poster_fn(img, px0, py0, px1, py1)
    # status rows
    yy = py1 + 18
    for lab, col in lines:
        d.rounded_rectangle(P((sx0 + 14, yy), (sx1 - 14, yy + 34)), 10 * S, fill=MINT if not T['dark'] else (20, 36, 25))
        d.ellipse(P((sx0 + 22, yy + 7), (sx0 + 42, yy + 27)), fill=col)
        text(img, (sx0 + 50, yy + 17), lab, 14, DEEP if not T['dark'] else WHITE, PSB, 'lm')
        check(img, sx1 - 32, yy + 17, 10, GREEN, WHITE)
        yy += 42

def node(img, cx, cy, T, icon, l1, l2):
    d = L(img)
    d.ellipse(P((cx - 60, cy - 60), (cx + 60, cy + 60)), fill=T['node'], outline=T['acc'], width=4 * S)
    if icon == 'ai': ic_ai(img, cx, cy, T['nodeic'], T['acc'] if not T['dark'] else LGREEN)
    elif icon == 'soc': ic_social(img, cx, cy, T['nodeic'], T['hi'] if not T['dark'] else LGREEN, T['node'])
    elif icon == 'wa': ic_wa(img, cx, cy, T['nodeic'], YEL if not T['dark'] else LGREEN, T['node'])
    else: ic_lang(img, cx, cy, T['nodeic'], T['hi'], T['node'])
    text(img, (cx, cy + 90), l1, 27, T['ink'], PB, 'mm')
    text(img, (cx, cy + 126), l2, 23, T['sub'], PM, 'mm')

def hub(img, T, poster_fn, labels, phone_lines, top=650):
    """Phone in the middle, 4 feature nodes linked with dashed curves."""
    px, pw, ph = 540 - 120, 240, 418
    py = top
    nodes = [(160, top + 72), (160, top + 282), (920, top + 72), (920, top + 282)]
    for (nx, ny) in nodes:
        side = px if nx < 540 else px + pw
        sx = nx + (62 if nx < 540 else -62)
        ty = py + 140 if ny < top + 200 else py + 330
        pts = bez((sx, ny), ((sx + side) / 2, ny), (side, ty))
        dashed(img, pts, T['line'], w=3, dash=10, gap=9)
        L(img).ellipse(P((side - 7, ty - 7), (side + 7, ty + 7)), fill=T['acc'])
    vphone(img, px, py, pw, ph, T, poster_fn, phone_lines)
    for (nx, ny), (ic, a, b) in zip(nodes, labels):
        node(img, nx, ny, T, ic, a, b)

def plans(img, T, y, items, mid_label):
    W3, gap = 300, 24
    x0 = 540 - (W3 * 3 + gap * 2) / 2
    for i, (name, price, per) in enumerate(items):
        x = x0 + i * (W3 + gap)
        star = i == 1
        if star:
            rrect(img, (x, y, x + W3, y + 96), 22, fill=GREEN)
            fg, sub = WHITE, (220, 252, 231)
        else:
            rrect(img, (x, y, x + W3, y + 96), 22, fill=T['card'], outline=T['line'], width=2)
            fg, sub = T['ink'], T['sub']
        text(img, (x + W3 / 2, y + 30), name, 22, sub, PSB, 'mm')
        text(img, (x + W3 / 2, y + 66), price, 34, fg, PB, 'mm')
        if star:
            w = tw(mid_label, 16, PB) + 24
            rrect(img, (x + W3 / 2 - w / 2, y - 14, x + W3 / 2 + w / 2, y + 14), 14, fill=YEL)
            text(img, (x + W3 / 2, y), mid_label, 16, DEEP, PB, 'mm')

def topbar(img, T):
    logo(img, 48, 34, 42, dark=T['dark'])
    pw = tw('9993615146', 28, PB) + 92
    if T['dark']:
        rrect(img, (1032 - pw, 36, 1032, 94), 29, fill=YEL); c = BLACK
    else:
        rrect(img, (1032 - pw, 36, 1032, 94), 29, fill=DEEP); c = YEL
    phone_icon(img, 1032 - pw + 34, 65, 26, c)
    text(img, (1032 - pw + 60, 65), '9993615146', 28, c, PB, 'lm')

def cta(img, T, l1, team, y=1214):
    if T['dark']:
        rrect(img, (0, y, 1080, 1350), 0, fill=YEL)
    else:
        rrect(img, (0, y, 1080, 1350), 0, fill=DEEP)
    tc = T['bandtxt']
    text(img, (52, y + 40), l1, 25, tc if T['dark'] else (187, 247, 208), PSB, 'lm')
    phone_icon(img, 78, y + 96, 44, T['num'])
    text(img, (116, y + 96), '9993615146', 60, T['num'], PB, 'lm')
    text(img, (1028, y + 46), team, 28, DEEP if T['dark'] else YEL, PB, 'rm')
    text(img, (1028, y + 88), 'Shri Balaji Digital Services', 22, tc, PM, 'rm')
