"""Richer gradient art for the posts the owner found plain (#7, #8, #12, #16, #17, #18, #20)."""
from art import *
from gloss import gshape, gellipse, grrect, grad_mask_fill, lighten, darken

GOLDG = ((254, 240, 138), (217, 159, 6)); GREENG = ((74, 222, 128), (21, 101, 52)); MINTG = ((240, 253, 244), (167, 243, 208))

def gpoly(img, pts, g, out=K, w=4, sheen=0.3):
    gshape(img, lambda d: d.polygon(P(*pts), fill=255), g[0], g[1], sheen)
    if out: ln(img, pts + [pts[0]], out, w)

def gel(img, cx, cy, rx, ry, g, out=K, w=4, sheen=0.3):
    gellipse(img, cx, cy, rx, ry, g[0], g[1], sheen)
    if out: el(img, cx, cy, rx, ry, fill=None, out=out, w=w)

def sunburst(img, cx, cy, r0, r1, n=32, col=(250, 214, 60), alpha=0.55):
    lay = Image.new('L', img.size, 0); d = ImageDraw.Draw(lay)
    for i in range(n):
        a = i * 2 * math.pi / n; da = math.pi / n * 0.55
        d.polygon(P((cx + r0 * math.cos(a - da), cy + r0 * math.sin(a - da)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                    (cx + r0 * math.cos(a + da), cy + r0 * math.sin(a + da))), fill=int(255 * alpha))
    img.paste(Image.new('RGB', img.size, col), (0, 0), lay.filter(ImageFilter.GaussianBlur(2 * S)))

def wave_flag(img, x, top, h=60, w=80, g=GOLDG):
    pts = [(x, top)] + bez((x, top), (x + w * 0.5, top - 14), (x + w, top + h * 0.45), 12)[1:] + bez((x + w, top + h * 0.45), (x + w * 0.5, top + h + 6), (x, top + h), 12)[1:]
    gpoly(img, pts, g, K, 3)

def a_gurugobind(img):
    sunburst(img, 540, 230, 120, 330)
    gel(img, 540, 230, 120, 120, ((255, 251, 225), (253, 224, 71)), out=None, sheen=0.4)
    # gurdwara: hall + three domes
    gpoly(img, [(380, 300), (700, 300), (700, 390), (380, 390)], MINTG, K, 5)
    gpoly(img, [(350, 390), (730, 390), (730, 408), (350, 408)], GOLDG, K, 4)
    for x0 in (410, 480, 550, 620):
        grrect(img, (x0, 320, x0 + 50, 390), 25, (254, 249, 195), (250, 214, 60), 0.2); rect(img, x0, 320, x0 + 50, 390, fill=None, out=K, w=4, r=25)
    for cx, s in [(540, 1.0), (420, 0.55), (660, 0.55)]:
        l_ = bez((cx - 66 * s, 300), (cx - 104 * s, 220 * s + 300 * (1 - s) - 0), (cx, 300 - 170 * s), 24)
        r_ = bez((cx, 300 - 170 * s), (cx + 104 * s, 220 * s + 300 * (1 - s)), (cx + 66 * s, 300), 24)
        gpoly(img, l_ + r_, GOLDG, K, 4)
        el(img, cx, 300 - 176 * s, 8 * s + 3, fill=YEL, out=K, w=3)
    for x in (250, 830):
        ln(img, [(x, 408), (x, 120)], K, 6)
        gpoly(img, [(x, 104), (x - 10, 126), (x + 10, 126)], GOLDG, K, 3)
        wave_flag(img, x + 3, 132, 64, 86 if x > 540 else 86)
    for x in (170, 300, 780, 910): diya(img, x, 400, 0.42)
    sparkles(img, [(150, 180, 14), (930, 200, 14)])

def a_army(img):
    # Himalaya at sunrise + medal + wreath
    sunburst(img, 540, 250, 90, 300, 28, (250, 214, 60), 0.45)
    gpoly(img, [(120, 404), (330, 220), (430, 310), (560, 180), (700, 300), (800, 240), (960, 404)], ((209, 250, 223), (34, 160, 80)), K, 5)
    for (px, py) in [(330, 220), (560, 180), (800, 240)]:
        gpoly(img, [(px, py), (px + 30, py + 28), (px - 30, py + 28)], ((255, 255, 255), (230, 240, 235)), None)
    cx = 540
    gpoly(img, [(cx - 66, 120), (cx - 8, 120), (cx + 22, 236), (cx - 36, 236)], GREENG, K, 4)
    gpoly(img, [(cx + 66, 120), (cx + 8, 120), (cx - 22, 236), (cx + 36, 236)], GOLDG, K, 4)
    glow(img, cx, 300, 120, (250, 204, 21), 0.4)
    gel(img, cx, 300, 82, 82, GOLDG, K, 6, 0.45)
    el(img, cx, 300, 62, fill=None, out=(180, 120, 5), w=3)
    star5(img, cx, 300, 46, WHITE, K)
    for sg in (-1, 1):
        for i in range(10):
            t = i / 9; y = 180 + 210 * t; x = cx + sg * (190 + 30 * math.sin(math.pi * t))
            gel(img, x, y, 15, 8, GREENG, None, sheen=0.4)
            if i % 3 == 1: gel(img, x + sg * 8, y + 10, 6, 6, GOLDG, None)

def a_shivaji(img):
    sunburst(img, 540, 300, 100, 320, 30, (250, 214, 60), 0.5)
    gel(img, 540, 300, 96, 96, ((255, 251, 225), (253, 224, 71)), out=None, sheen=0.4)
    ln(img, [(120, 406), (960, 406)], LINEC, 3)
    for x0, x1, top in [(200, 420, 300), (420, 660, 240), (660, 880, 310)]:
        gpoly(img, [(x0, top), (x1, top), (x1, 404), (x0, 404)], ((254, 249, 195), (240, 200, 70)), K, 5)
        for x in range(int(x0) + 6, int(x1) - 10, 40):
            gpoly(img, [(x, top - 22), (x + 22, top - 22), (x + 22, top), (x, top)], ((254, 249, 195), (240, 200, 70)), K, 3)
    gpoly(img, [(500, 404)] + bez((500, 360), (540, 320), (580, 360), 12) + [(580, 404)], GREENG, K, 5)
    ln(img, [(540, 240), (540, 120)], K, 5)
    wave_flag(img, 543, 122, 60, 90)
    # curved talwar + dhal
    ln(img, bez((160, 380), (150, 250), (240, 140), 20), (120, 130, 125), 9); ln(img, bez((160, 380), (150, 250), (240, 140), 20), WHITE, 3)
    ln(img, [(140, 372), (186, 384)], K, 7); gel(img, 150, 400, 10, 10, GOLDG, K, 3)
    gel(img, 900, 200, 58, 58, GOLDG, K, 5, 0.45)
    for a in (45, 135, 225, 315): gel(img, 900 + 28 * math.cos(math.radians(a)), 200 + 28 * math.sin(math.radians(a)), 7, 7, ((80, 90, 85), (20, 30, 25)), None)

def a_holi(img):
    random.seed(9)
    for cx, cy, r, g in [(300, 220, 110, GOLDG), (780, 210, 120, GREENG), (540, 300, 90, ((254, 249, 195), (250, 204, 21))),
                         (200, 350, 70, ((187, 247, 208), (34, 197, 94))), (890, 350, 70, GOLDG)]:
        for k in range(16):
            a = random.uniform(0, 6.28); rr = random.uniform(0.3, 1.0) * r; s = random.uniform(12, 32)
            gel(img, cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.8, s, s, g, None, 0.3)
        gel(img, cx, cy, r * 0.6, r * 0.5, g, None, 0.4)
    # pichkari
    grrect(img, (400, 160, 600, 204), 18, (74, 222, 128), (21, 101, 52), 0.4); rect(img, 400, 160, 600, 204, fill=None, out=K, w=4, r=18)
    grrect(img, (600, 174, 690, 190), 6, (254, 240, 138), (217, 159, 6)); rect(img, 600, 174, 690, 190, fill=None, out=K, w=3)
    rect(img, 360, 174, 400, 190, fill=YEL, out=K, w=3); rect(img, 350, 156, 366, 208, fill=K, out=None)
    for i in range(6): gel(img, 712 + i * 24, 182 - i * 7, 7 - i * 0.6, 7 - i * 0.6, GREENG, None)
    # gulal bowls with colour mounds
    for x, g in [(410, GOLDG), (540, GREENG), (670, ((187, 247, 208), (34, 197, 94)))]:
        gshape(img, lambda d, x=x: d.chord(P((x - 46, 300), (x + 46, 368)), 180, 360, fill=255), g[0], g[1], 0.45)
        gshape(img, lambda d, x=x: d.chord(P((x - 62, 296), (x + 62, 398)), 0, 180, fill=255), (255, 255, 255), (200, 215, 208), 0.2)
        D(img).arc(P((x - 62, 296), (x + 62, 398)), 0, 180, fill=K, width=int(3 * S)); ln(img, [(x - 62, 347), (x + 62, 347)], K, 3)
    # water balloons
    for (x, y, g) in [(160, 160, GOLDG), (930, 150, GREENG)]:
        gel(img, x, y, 26, 32, g, K, 3, 0.45)

def a_goodfriday(img):
    glow(img, 540, 230, 260, (254, 243, 170), 0.6)
    sunburst(img, 540, 220, 110, 300, 36, (250, 222, 90), 0.4)
    gpoly(img, [(250, 404)] + bez((250, 404), (540, 300), (830, 404), 30)[1:], ((220, 252, 231), (34, 160, 80)), K, 4)
    gpoly(img, [(522, 110), (558, 110), (558, 360), (522, 360)], ((255, 251, 225), (217, 170, 40)), K, 5)
    gpoly(img, [(450, 170), (630, 170), (630, 204), (450, 204)], ((255, 251, 225), (217, 170, 40)), K, 5)
    # lilies
    for x, sg in [(330, 1), (750, -1)]:
        ln(img, bez((x, 404), (x + sg * 10, 330), (x + sg * 30, 290), 12), (21, 128, 61), 5)
        for a in (-30, 0, 30):
            ar = math.radians(a - 90 + sg * 20)
            tip = (x + sg * 30 + 46 * math.cos(ar), 290 + 46 * math.sin(ar))
            gpoly(img, [(x + sg * 30, 290), (tip[0] - 14, tip[1] + 6), tip, (tip[0] + 14, tip[1] + 6)], ((255, 255, 255), (254, 240, 138)), K, 3)
    # dove
    cx, cy = 760, 150
    gpoly(img, bez((cx - 50, cy + 10), (cx - 10, cy - 50), (cx + 10, cy - 4), 12) + bez((cx + 10, cy - 4), (cx + 60, cy - 30), (cx + 50, cy + 20), 12)
          + [(cx - 30, cy + 26)], ((255, 255, 255), (220, 235, 228)), K, 3)
    el(img, cx + 44, cy + 2, 3, fill=K, out=None)

def a_ambedkar(img):
    sunburst(img, 540, 170, 70, 230, 28, (250, 214, 60), 0.45)
    # chakra glowing
    gel(img, 540, 170, 66, 66, ((255, 255, 255), (220, 252, 231)), K, 5)
    for i in range(24):
        a = i * math.pi / 12; ln(img, [(540, 170), (540 + 58 * math.cos(a), 170 + 58 * math.sin(a))], (21, 101, 52), 2)
    gel(img, 540, 170, 10, 10, GREENG, None)
    # open constitution book with gradient cover
    gpoly(img, [(540, 262), (330, 248), (320, 392), (540, 408)], ((255, 255, 255), (236, 252, 243)), K, 5)
    gpoly(img, [(540, 262), (750, 248), (760, 392), (540, 408)], ((255, 255, 255), (236, 252, 243)), K, 5)
    gpoly(img, [(318, 392), (540, 408), (762, 392), (762, 404), (540, 420), (318, 404)], GREENG, K, 3)
    text(img, (432, 300), 'भारत का', 24, (21, 101, 52), PB, 'mm'); text(img, (432, 340), 'संविधान', 34, K, PB, 'mm')
    for k in range(4): ln(img, [(580, 300 + k * 24), (720, 296 + k * 24)], LINEC, 3)
    # pen
    gpoly(img, [(840, 390), (920, 200), (944, 210), (864, 400)], GREENG, K, 4); gpoly(img, [(840, 390), (864, 400), (838, 418)], GOLDG, K, 3)
    sparkles(img, [(220, 220, 16), (860, 140, 14)])

def a_labour(img):
    sunburst(img, 540, 260, 120, 300, 26, (250, 214, 60), 0.35)
    # big gear (gradient)
    teeth = 12; cx, cy, r = 540, 270, 120
    pts = []
    for i in range(teeth * 2):
        a0 = i * math.pi / teeth; rr = r if i % 2 == 0 else r * 0.82
        for da in (-0.11, 0.11): pts.append((cx + rr * math.cos(a0 + da), cy + rr * math.sin(a0 + da)))
    gpoly(img, pts, GREENG, K, 4)
    gel(img, cx, cy, 70, 70, ((255, 255, 255), (220, 252, 231)), K, 4)
    # hard hat inside
    gshape(img, lambda d: d.chord(P((cx - 52, cy - 40), (cx + 52, cy + 50)), 180, 360, fill=255), GOLDG[0], GOLDG[1], 0.45)
    D(img).arc(P((cx - 52, cy - 40), (cx + 52, cy + 50)), 180, 360, fill=K, width=int(4 * S))
    gpoly(img, [(cx - 66, cy + 4), (cx + 66, cy + 4), (cx + 66, cy + 18), (cx - 66, cy + 18)], GOLDG, K, 3)
    ln(img, [(cx, cy - 40), (cx, cy + 4)], K, 3)
    # crossed hammer and wrench below/sides
    gpoly(img, [(190, 400), (205, 410), (330, 210), (315, 200)], ((180, 120, 60), (110, 70, 30)), K, 3)
    gpoly(img, [(290, 180), (370, 220), (356, 246), (276, 206)], ((200, 210, 205), (110, 125, 118)), K, 4)
    gpoly(img, [(890, 400), (875, 410), (760, 220), (775, 210)], ((200, 210, 205), (110, 125, 118)), K, 3)
    gel(img, 762, 204, 30, 30, ((220, 228, 224), (120, 135, 128)), K, 4)
    gel(img, 750, 190, 14, 14, ((255, 255, 255), (240, 245, 242)), None)
    # bricks
    for (x, y) in [(640, 380), (700, 380), (670, 352)]:
        grrect(img, (x, y, x + 56, y + 26), 3, (254, 220, 120), (217, 159, 6)); rect(img, x, y, x + 56, y + 26, fill=None, out=K, w=3, r=3)

ART.update(gurugobind=a_gurugobind, army=a_army, shivaji=a_shivaji, holi=a_holi, goodfriday=a_goodfriday,
           ambedkar=a_ambedkar, labour=a_labour)

# ---- give every shape in all illustrations a rich gradient fill ----
import art as _art
_rect0, _el0, _poly0 = _art.rect, _art.el, _art.poly
YELF = {YEL, GOLD, HL, (250, 222, 90), (253, 224, 71), (254, 240, 138)}
PALEF = {PALE, (254, 249, 195), (255, 251, 225)}
MINTF = {(220, 252, 231), (187, 247, 208), (240, 253, 244), (209, 250, 223), MINT}
def gmap(c):
    if c is None: return None
    c = tuple(c)
    if c == WHITE: return ((255, 255, 255), (222, 236, 229))
    if c in YELF: return ((254, 243, 160), (214, 150, 4))
    if c in PALEF: return ((255, 251, 225), (240, 198, 70))
    if c in MINTF: return ((236, 253, 243), (96, 205, 140))
    if c == GREEN or c == (34, 197, 94) or c == LGREEN: return ((110, 231, 160), (21, 110, 55))
    if c == DEEP or c == (22, 101, 52) or c == (12, 64, 34): return ((40, 140, 75), (6, 46, 25))
    return (lighten(c, 0.3), darken(c, 0.25))

def rect_g(img, x0, y0, x1, y1, fill=WHITE, out=K, w=SW, r=0):
    g = gmap(fill)
    if g:
        if r: grrect(img, (x0, y0, x1, y1), r, g[0], g[1], 0.3)
        else: gshape(img, lambda d: d.rectangle(P((x0, y0), (x1, y1)), fill=255), g[0], g[1], 0.3)
    if out: _rect0(img, x0, y0, x1, y1, fill=None, out=out, w=w, r=r)

def el_g(img, cx, cy, rx, ry=None, fill=None, out=K, w=SW):
    ry = ry or rx; g = gmap(fill)
    if g: gellipse(img, cx, cy, rx, ry, g[0], g[1], 0.35)
    if out: _el0(img, cx, cy, rx, ry, fill=None, out=out, w=w)

def poly_g(img, pts, fill=None, out=K, w=SW):
    g = gmap(fill)
    if g: gshape(img, lambda d: d.polygon(P(*pts), fill=255), g[0], g[1], 0.3)
    if out: _poly0(img, pts, None, out, w)

_art.rect, _art.el, _art.poly = rect_g, el_g, poly_g
