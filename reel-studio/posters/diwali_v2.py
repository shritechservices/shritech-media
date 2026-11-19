import sys; sys.path.insert(0, '/home/claude/posters')
from v2 import *

T = DARK
img = Image.new('RGB', (W, H), BLACK)
glow(img, 540, 300, 300, (120, 92, 6), 0.55)
glow(img, 540, 900, 520, (10, 70, 36), 0.5)
d = L(img)

# string lights (line + bulbs)
pts = []
for i in range(41):
    t = i / 40; pts.append((40 + 1000 * t, 122 + 40 * math.sin(t * math.pi)))
d.line(P(*pts), fill=(70, 90, 76), width=2 * S)
for i in range(1, 16):
    t = i / 16; x = 40 + 1000 * t; y = 122 + 40 * math.sin(t * math.pi)
    if 470 < x < 610: continue
    c = YEL if i % 2 else LGREEN
    glow(img, x, y + 14, 24, c, 0.35)
    d.line(P((x, y), (x, y + 6)), fill=(70, 90, 76), width=2 * S)
    d.ellipse(P((x - 7, y + 6), (x + 7, y + 24)), fill=c)

# line rangoli behind the diya
cx, cy = 540, 296
for rr, col, n in [(190, GREEN, 28), (150, YEL, 20)]:
    for i in range(n):
        a = math.pi + i * math.pi / (n - 1)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        d.ellipse(P((x - 4, y - 4), (x + 4, y + 4)), fill=col)
for i in range(9):
    a = math.pi + (i + 0.5) * math.pi / 9
    a1, a2 = a - 0.16, a + 0.16
    p = [(cx + 105 * math.cos(a1), cy + 105 * math.sin(a1)), (cx + 135 * math.cos(a), cy + 135 * math.sin(a)),
         (cx + 105 * math.cos(a2), cy + 105 * math.sin(a2))]
    d.line(P(*p), fill=LGREEN, width=3 * S, joint='curve')

def diya(cx, by, s, glow_a=0.5):
    glow(img, cx, by - 60 * s, 120 * s, (250, 204, 21), glow_a)
    d = L(img)
    # flame
    fx, fy = cx, by - 30 * s
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.ellipse(P((fx - 24 * s, fy - 52 * s), (fx + 24 * s, fy)), fill=255)
    md.polygon(P((fx - 23 * s, fy - 32 * s), (fx, fy - 112 * s), (fx + 23 * s, fy - 32 * s)), fill=255)
    img.paste(Image.new('RGB', img.size, YEL), (0, 0), m.filter(ImageFilter.GaussianBlur(1.5 * S)))
    d.ellipse(P((fx - 11 * s, fy - 40 * s), (fx + 11 * s, fy - 4 * s)), fill=(255, 251, 225))
    # bowl
    d.chord(P((cx - 100 * s, by - 72 * s), (cx + 100 * s, by + 52 * s)), 0, 180, fill=YEL)
    d.polygon(P((cx + 92 * s, by - 10 * s), (cx + 132 * s, by - 34 * s), (cx + 84 * s, by + 10 * s)), fill=YEL)
    d.ellipse(P((cx - 100 * s, by - 24 * s), (cx + 100 * s, by)), fill=GOLD)
    d.ellipse(P((cx - 88 * s, by - 19 * s), (cx + 88 * s, by - 5 * s)), fill=(120, 80, 4))
    d.arc(P((cx - 72 * s, by - 6 * s), (cx + 72 * s, by + 36 * s)), 15, 165, fill=DEEP, width=int(5 * s * S))
    for i in range(5):
        x = cx - 40 * s + i * 20 * s
        d.ellipse(P((x - 5 * s, by + 18 * s), (x + 5 * s, by + 28 * s)), fill=DEEP)
diya(296, 358, 0.58, 0.35)
diya(784, 358, 0.58, 0.35)
diya(540, 338, 1.0)
for sx, sy, r in [(190, 250, 14), (890, 240, 16), (160, 400, 8), (930, 400, 9)]:
    sparkle(img, sx, sy, r, YEL)

# greeting (one clean line)
h1, h2 = 'Happy', 'Diwali'
w1, w2 = tw(h1, 92, PF), tw(h2, 100, PB)
x = 540 - (w1 + 22 + w2) / 2
text(img, (x, 500), h1, 92, YEL, PF, 'ls')
text(img, (x + w1 + 22, 500), h2, 100, WHITE, PB, 'ls')
text(img, (540, 542), 'Light, joy and growth for your home and business', 27, (187, 247, 208), PM, 'mm')

s = 'This Diwali, light up your business'
w = tw(s, 28, PB) + 64
rrect(img, (540 - w / 2, 582, 540 + w / 2, 634), 26, fill=YEL)
text(img, (540, 607), s, 28, BLACK, PB, 'mm')

def mini_poster(img, x0, y0, x1, y1):
    d = L(img)
    d.rounded_rectangle(P((x0, y0), (x1, y1)), 14 * S, fill=(12, 60, 32))
    c = ((x0 + x1) / 2, y0 + 82)
    glow(img, c[0], c[1] - 20, 50, (250, 204, 21), 0.35)
    d.chord(P((c[0] - 36, c[1] - 26), (c[0] + 36, c[1] + 20)), 0, 180, fill=YEL)
    m = [(c[0] - 9, c[1] - 6), (c[0], c[1] - 44), (c[0] + 9, c[1] - 6)]
    d.polygon(P(*m), fill=YEL); d.ellipse(P((c[0] - 9, c[1] - 18), (c[0] + 9, c[1] - 2)), fill=YEL)
    text(img, ((x0 + x1) / 2, y0 + 130), 'Diwali Offer', 19, YEL, PB, 'mm')
    d.rounded_rectangle(P((x0 + 30, y1 - 40), (x1 - 30, y1 - 16)), 12 * S, fill=LGREEN)
    text(img, ((x0 + x1) / 2, y1 - 28), 'Your Shop', 13, BLACK, PB, 'mm')

hub(img, T, mini_poster,
    [('ai', 'AI Posts', 'Ready in 1 minute'), ('wa', 'WhatsApp', 'Reach 1000s at once'),
     ('soc', '1-Click Post', 'Facebook + Instagram'), ('lang', '8+ Languages', 'Hindi, English...')],
    [('Facebook', GREEN), ('Instagram', YEL), ('WhatsApp', LGREEN)], top=664)

plans(img, T, 1112, [('Start Free', '₹0', ''), ('Growth', '₹1,799', ''), ('Pro', '₹3,999', '')], 'Popular')
topbar(img, T)
cta(img, T, 'Call / WhatsApp now', 'Team Shri Tech')
finish(img, '/home/claude/posters/diwali-english-dark-v2.jpg')
