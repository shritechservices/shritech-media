import sys; sys.path.insert(0, '/home/claude/posters')
from fest import *

SHOT = '/mnt/user-data/uploads/3c987a50-image.jpg'
img = vgrad((5, 8, 6), (9, 22, 13))
glow(img, 540, 380, 430, (120, 90, 4), 0.55)
glow(img, 540, 400, 220, (250, 204, 21), 0.22)
glow(img, 0, 1100, 380, (22, 120, 60), 0.45)
glow(img, 1080, 820, 320, (22, 120, 60), 0.35)

# bokeh
random.seed(7)
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
for _ in range(38):
    x, y = random.uniform(0, 1080), random.uniform(120, 760)
    if 300 < x < 780 and 230 < y < 460: continue
    r = random.uniform(5, 22)
    c = random.choice([YEL, GOLD, LGREEN, YEL])
    d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=c + (random.randint(35, 90),))
lay = lay.filter(ImageFilter.GaussianBlur(3 * S))
img.paste(lay, (0, 0), lay)

# rangoli half-mandala behind the diyas
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
cx, cy = 540, 420
for k, (rr, n, col) in enumerate([(300, 24, GOLD), (240, 18, GREEN), (180, 12, YEL)]):
    for i in range(n):
        a = math.pi + i * math.pi / (n - 1)
        a1, a2 = a - math.pi / n * 0.8, a + math.pi / n * 0.8
        pts = [(cx + (rr - 50) * math.cos(a1), cy + (rr - 50) * math.sin(a1)), (cx + rr * math.cos(a), cy + rr * math.sin(a)),
               (cx + (rr - 50) * math.cos(a2), cy + (rr - 50) * math.sin(a2)), (cx + (rr - 70) * math.cos(a), cy + (rr - 70) * math.sin(a))]
        d.polygon([(x * S, y * S) for x, y in pts], outline=col + (110,), width=2 * S)
    d.arc([(cx - rr - 10) * S, (cy - rr - 10) * S, (cx + rr + 10) * S, (cy + rr + 10) * S], 180, 360, fill=col + (60,), width=2 * S)
img.paste(lay, (0, 0), lay)

# string lights
d = ImageDraw.Draw(img)
def lights(x0, x1, y, sag, n):
    pts = []
    for i in range(n + 1):
        t = i / n; pts.append((x0 + (x1 - x0) * t, y + sag * 4 * t * (1 - t)))
    d.line([(x * S, yy * S) for x, yy in pts], fill=(60, 70, 62), width=2 * S)
    for i, (x, yy) in enumerate(pts[1:-1]):
        c = YEL if i % 2 == 0 else LGREEN
        glow(img, x, yy + 10, 26, c, 0.35)
        d.ellipse([(x - 7) * S, (yy + 2) * S, (x + 7) * S, (yy + 20) * S], fill=c)
        d.ellipse([(x - 3) * S, (yy + 5) * S, (x + 1) * S, (yy + 10) * S], fill=WHITE)
lights(-20, 1100, 116, 60, 18)

# diyas
def diya(cx, by, s):
    glow(img, cx, by - 70 * s, 110 * s, (250, 204, 21), 0.45)
    d = ImageDraw.Draw(img)
    # bowl
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.chord([(cx - 95 * s) * S, (by - 75 * s) * S, (cx + 95 * s) * S, (by + 45 * s) * S], 0, 180, fill=255)
    md.polygon([((cx + 95 * s) * S, (by - 15 * s) * S), ((cx + 135 * s) * S, (by - 40 * s) * S), ((cx + 90 * s) * S, (by + 0 * s) * S)], fill=255)
    img.paste(vgrad((250, 204, 21), (161, 98, 7)), (0, 0), m)
    d.ellipse([(cx - 95 * s) * S, (by - 26 * s) * S, (cx + 95 * s) * S, (by - 4 * s) * S], fill=(120, 72, 5))
    d.ellipse([(cx - 86 * s) * S, (by - 22 * s) * S, (cx + 86 * s) * S, (by - 8 * s) * S], fill=(250, 214, 80))
    for i in range(7):
        x = cx - 60 * s + i * 20 * s
        d.ellipse([(x - 5 * s) * S, (by + 12 * s) * S, (x + 5 * s) * S, (by + 22 * s) * S], fill=GREEN)
    d.arc([(cx - 70 * s) * S, (by - 8 * s) * S, (cx + 70 * s) * S, (by + 34 * s) * S], 20, 160, fill=DEEP, width=int(3 * s * S))
    # flame
    fx, fy = cx + 100 * s, by - 40 * s
    fx = cx; fy = by - 22 * s
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.ellipse([(fx - 22 * s) * S, (fy - 50 * s) * S, (fx + 22 * s) * S, (fy) * S], fill=255)
    md.polygon([((fx - 21 * s) * S, (fy - 30 * s) * S), (fx * S, (fy - 105 * s) * S), ((fx + 21 * s) * S, (fy - 30 * s) * S)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2 * S))
    img.paste(vgrad((255, 255, 230), (250, 180, 10)), (0, 0), m)
    d.ellipse([(fx - 9 * s) * S, (fy - 34 * s) * S, (fx + 9 * s) * S, (fy - 4 * s) * S], fill=(255, 255, 245))
diya(380, 400, 0.72)
diya(700, 400, 0.72)
diya(540, 400, 1.0)

# top bar
logo(img, 48, 34, 44, dark=True)
pw = tw('9993615146', 30, PB) + 98
grad_box(img, (1032 - pw, 34, 1032, 96), 31, (253, 224, 71), (234, 179, 8))
phone_icon(img, 1032 - pw + 36, 66, 28, BLACK)
text(img, (1032 - pw + 64, 66), '9993615146', 30, BLACK, PB, 'lm')

# greeting
grad_text(img, (540, 512), 'Happy', 74, (254, 240, 138), (234, 179, 8), PF, 'mm')
grad_text(img, (540, 612), 'DIWALI', 132, (254, 240, 138), (202, 138, 4), PB, 'mm', shadow=(YEL, 0.25))
text(img, (540, 712), 'May your home and business shine brighter', 29, WHITE, PM, 'mm')

# business card (dark glass)
CX0, CY0, CX1, CY1 = 40, 768, 1040, 1184
shadow(img, (CX0, CY0, CX1, CY1), 36, blur=26, alpha=0.6, color=(0, 0, 0))
rrect(img, (CX0, CY0, CX1, CY1), 36, fill=(16, 27, 20))
glow(img, 860, 860, 240, (22, 120, 60), 0.18)
rrect(img, (CX0, CY0, CX1, CY1), 36, outline=(34, 120, 64), width=2)
grad_box(img, (CX0, CY0, CX1, CY0 + 14), 7, YEL, GOLD, gloss=False)
phone_mock(img, SHOT, 54, 800, 284, rot=-4, dark=True, crop_top=0, crop_h=1262, frame=(52, 60, 55))
X = 362
text(img, (X, 822), 'This Diwali, light up your business', 30, WHITE, PB, 'lm')
text(img, (X, 864), 'with Shri Tech — fast, simple, smart', 25, LGREEN, PSB, 'lm')
items = ['Diwali offer posts in 1 minute with AI', '1-click post on Facebook & Instagram',
         'Send offers to 1000s on WhatsApp', '8+ languages, your logo & colours']
for i, s in enumerate(items):
    y = 920 + i * 50
    check(img, X + 16, y, 16, YEL, BLACK)
    text(img, (X + 44, y), s, 26, (226, 236, 229), PM, 'lm')
chips = [('Start FREE', YEL, BLACK, None), ('Growth ₹1,799', (16, 27, 20), YEL, GREEN), ('Pro ₹3,999', (16, 27, 20), YEL, GREEN)]
x = X
for s, bg, fg, ol in chips:
    w = tw(s, 22, PBD) + 40
    rrect(img, (x, 1136 - 22, x + w, 1136 + 22), 22, fill=bg, outline=ol, width=2)
    text(img, (x + w / 2, 1136), s, 22, fg, PBD, 'mm')
    x += w + 12

# bottom CTA band (yellow, glossy)
grad_box(img, (0, 1206, 1080, 1350), 0, (253, 224, 71), (234, 170, 8))
text(img, (48, 1250), 'Call / WhatsApp now', 26, DEEP, PSB, 'lm')
phone_icon(img, 74, 1305, 46, BLACK)
text(img, (112, 1306), '9993615146', 58, BLACK, PB, 'lm')
text(img, (1032, 1258), 'Team Shri Tech', 28, DEEP, PB, 'rm')
text(img, (1032, 1298), 'Shri Balaji Digital Services', 22, BLACK, PM, 'rm')
for sx, sy, r in [(170, 560, 14), (920, 540, 16), (110, 440, 9), (980, 420, 10)]:
    sparkle(img, sx, sy, r, YEL)

finish(img, '/home/claude/posters/diwali-english-dark.jpg')
