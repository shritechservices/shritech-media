"""Christmas (25 Dec 2026) - dark theme, English. Audience: restaurants, cafes, bakeries. Diagram: growth cycle."""
import sys; sys.path.insert(0, '/home/claude/posters')
from v3 import *

T = DARK
img = Image.new('RGB', (W, H), BLACK)
glow(img, 540, 260, 300, (90, 70, 4), 0.55)
glow(img, 540, 880, 420, (10, 70, 36), 0.55)
d = L(img)
random.seed(3)

# snowflakes (line art)
def flake(x, y, r, col):
    for i in range(3):
        a = i * math.pi / 3
        d.line(P((x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))), fill=col, width=2 * S)
for _ in range(26):
    x, y = random.uniform(30, 1050), random.uniform(120, 430)
    if 330 < x < 750: continue
    flake(x, y, random.uniform(5, 11), random.choice([(200, 220, 205), (120, 160, 130), YEL]))

# Christmas tree: three tiers, line art
cx = 540
tiers = [(150, 245, 92), (210, 320, 122), (280, 398, 150)]
for top, bot, hw in tiers:
    d.polygon(P((cx, top), (cx - hw, bot), (cx + hw, bot)), fill=(12, 64, 34))
    d.line(P((cx, top), (cx - hw, bot), (cx + hw, bot), (cx, top)), fill=LGREEN, width=5 * S, joint='curve')
d.rectangle(P((cx - 20, 398), (cx + 20, 426)), fill=(120, 80, 4), outline=YEL, width=3 * S)
# garlands (dotted yellow)
for (y0, y1, x0, x1) in [(200, 232, -60, 70), (268, 300, -95, 100), (338, 380, -130, 130)]:
    pts = bez((cx + x0, y0), (cx, y1 + 30), (cx + x1, y1 - 10), 24)
    for i, (x, y) in enumerate(pts):
        if i % 2 == 0: d.ellipse(P((x - 3.5, y - 3.5), (x + 3.5, y + 3.5)), fill=YEL)
# ornaments
for (x, y, c) in [(cx - 40, 228, YEL), (cx + 34, 214, WHITE), (cx - 70, 300, WHITE), (cx + 64, 290, YEL),
                  (cx + 10, 270, LGREEN), (cx - 100, 372, YEL), (cx + 100, 368, WHITE), (cx - 20, 352, YEL)]:
    glow(img, x, y, 16, c, 0.3)
    d.ellipse(P((x - 9, y - 9), (x + 9, y + 9)), fill=c)
# star
glow(img, cx, 140, 60, (250, 204, 21), 0.6)
pts = []
for i in range(10):
    a = -math.pi / 2 + i * math.pi / 5
    r = 34 if i % 2 == 0 else 14
    pts.append((cx + r * math.cos(a), 140 + r * math.sin(a)))
d.polygon(P(*pts), fill=YEL)
# gifts
def gift(x, y, w, h, box, rib):
    d.rounded_rectangle(P((x, y), (x + w, y + h)), 6 * S, fill=box)
    d.rectangle(P((x - 4, y - 14), (x + w + 4, y + 4)), fill=box, outline=None)
    d.rectangle(P((x + w / 2 - 7, y - 14), (x + w / 2 + 7, y + h)), fill=rib)
    d.rectangle(P((x - 4, y - 4), (x + w + 4, y + 4)), fill=rib)
    d.ellipse(P((x + w / 2 - 22, y - 32), (x + w / 2 - 2, y - 14)), outline=rib, width=4 * S)
    d.ellipse(P((x + w / 2 + 2, y - 32), (x + w / 2 + 22, y - 14)), outline=rib, width=4 * S)
gift(330, 360, 76, 66, YEL, DEEP)
gift(674, 344, 90, 82, GREEN, YEL)
gift(770, 384, 56, 42, YEL, GREEN)
# a coffee cup + cake slice (cafe hint) on the left
d.rounded_rectangle(P((236, 378), (296, 426)), 10 * S, fill=WHITE)
d.arc(P((286, 388), (312, 414)), 270, 90, fill=WHITE, width=5 * S)
for x in (252, 268, 284):
    d.arc(P((x - 6, 344), (x + 6, 372)), 300, 60, fill=(200, 220, 205), width=3 * S)
d.rectangle(P((236, 392), (296, 400)), fill=GREEN)

# greeting
h1, h2 = 'Merry', 'Christmas'
w1, w2 = tw(h1, 86, PF), tw(h2, 90, PB)
x = 540 - (w1 + 22 + w2) / 2
text(img, (x, 510), h1, 86, YEL, PF, 'ls')
text(img, (x + w1 + 22, 510), h2, 90, WHITE, PB, 'ls')
text(img, (540, 550), 'Warm wishes for full tables and happy guests', 27, (187, 247, 208), PM, 'mm')
s = "Put your Christmas menu on every customer's phone"
w = tw(s, 26, PB) + 60
rrect(img, (540 - w / 2, 586, 540 + w / 2, 636), 25, fill=YEL)
text(img, (540, 611), s, 26, BLACK, PB, 'mm')

# ---- growth cycle diagram ----
CX, CY, R = 540, 870, 165
# ring arrows between the 4 nodes (NW=-135, NE=-45, SE=45, SW=135)
for a0, a1 in [(-135, -45), (-45, 45), (45, 135), (135, 225)]:
    arc_arrow(img, CX, CY, R, a0 + 22, a1 - 22, (74, 222, 128), w=4)
# centre: the restaurant
d.ellipse(P((CX - 92, CY - 92), (CX + 92, CY + 92)), fill=(14, 28, 19), outline=YEL, width=4 * S)
# cloche icon
d.chord(P((CX - 46, CY - 52), (CX + 46, CY + 26)), 180, 360, fill=YEL)
d.ellipse(P((CX - 7, CY - 62), (CX + 7, CY - 48)), fill=YEL)
d.rounded_rectangle(P((CX - 56, CY - 14), (CX + 56, CY - 4)), 5 * S, fill=WHITE)
text(img, (CX, CY + 22), 'Your', 20, (187, 247, 208), PSB, 'mm')
text(img, (CX, CY + 48), 'Restaurant', 22, WHITE, PB, 'mm')
nodes = [(-135, 'menu', 'Festive menu post', 'AI designs it in 1 minute', 'l'),
         (-45, 'soc', 'Post in 1 click', 'Facebook + Instagram', 'r'),
         (45, 'wa', 'Offer on WhatsApp', 'Reach 1000s of regulars', 'r'),
         (135, 'book', 'Bookings roll in', 'Reply in live chat', 'l')]
for i, (a, ic, t1, t2, side) in enumerate(nodes):
    nx, ny = CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a))
    circ_node(img, nx, ny, 50, T, ic, num=i + 1)
    if side == 'l':
        text(img, (nx - 70, ny - 16), t1, 26, WHITE, PB, 'rm'); text(img, (nx - 70, ny + 18), t2, 21, (190, 210, 197), PM, 'rm')
    else:
        text(img, (nx + 70, ny - 16), t1, 26, WHITE, PB, 'lm'); text(img, (nx + 70, ny + 18), t2, 21, (190, 210, 197), PM, 'lm')

# ---- start-free ribbon for food businesses ----
RY = 1100
rrect(img, (40, RY, 1040, RY + 98), 22, fill=(16, 30, 21), outline=YEL, width=3)
rich(img, 64, RY + 30, [('Start FREE today', 26, YEL, PB), ('· 10 credits every month · No card needed', 21, WHITE, PM)], anchor='l')
cx_ = 64
for chip in ['Restaurants', 'Cafes', 'Bakeries', 'Cloud kitchens', 'Sweet shops']:
    w = tw(chip, 18, PSB) + 26
    rrect(img, (cx_, RY + 56, cx_ + w, RY + 86), 15, fill=(12, 48, 27), outline=(52, 120, 76), width=2)
    text(img, (cx_ + w / 2, RY + 71), chip, 18, (187, 247, 208), PSB, 'mm')
    cx_ += w + 10

logo(img, 48, 34, 44, dark=True)
num_pill(img, 1032, 36, True)
cta3(img, T, 'Free demo for your restaurant — Call / WhatsApp')
finish3(img, '/home/claude/posters/christmas-english-dark-v4.jpg', 'Christmas 2026 - Shri Tech')
