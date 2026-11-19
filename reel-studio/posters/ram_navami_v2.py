import sys; sys.path.insert(0, '/home/claude/posters')
from v2 import *

T = LIGHT
img = Image.new('RGB', (W, H), WHITE)
glow(img, 540, 250, 330, (254, 243, 170), 0.55)
glow(img, 540, 900, 520, (220, 252, 231), 0.6)
d = L(img)

# mango-leaf toran at the two top corners (line art)
def toran(xa, xb):
    pts = []
    for i in range(31):
        t = i / 30; pts.append((xa + (xb - xa) * t, 118 + 30 * math.sin(t * math.pi)))
    d.line(P(*pts), fill=GREEN, width=3 * S)
    for i in range(1, 8):
        t = i / 8; x = xa + (xb - xa) * t; y = 118 + 30 * math.sin(t * math.pi)
        d.polygon(P((x, y), (x - 11, y + 22), (x, y + 44), (x + 11, y + 22)), fill=GREEN if i % 2 else (34, 197, 94))
        d.line(P((x, y + 4), (x, y + 40)), fill=(187, 247, 208), width=2 * S)
        if i % 2 == 0:
            d.ellipse(P((x - 9, y + 46), (x + 9, y + 64)), fill=YEL)
toran(20, 380); toran(700, 1060)

# sun with line rays
cx, cy = 540, 268
for i in range(24):
    a = i * math.pi / 12
    if math.sin(a) > 0.45: continue
    r0, r1 = 128, 150 if i % 2 else 168
    d.line(P((cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))), fill=YEL, width=6 * S)
d.ellipse(P((cx - 112, cy - 112), (cx + 112, cy + 112)), fill=(254, 240, 138), outline=YEL, width=5 * S)

# temple (line art)
k = DEEP; sw = 5 * S
d.rectangle(P((392, 362), (688, 384)), fill=WHITE, outline=k, width=sw)
d.rectangle(P((422, 346), (658, 362)), fill=WHITE, outline=k, width=sw)
d.rectangle(P((448, 254), (632, 346)), fill=WHITE, outline=k, width=sw)
d.rounded_rectangle(P((513, 282), (567, 352)), 26 * S, fill=GREEN, outline=k, width=sw)
d.rectangle(P((513, 318), (567, 352)), fill=GREEN)
d.line(P((513, 318), (513, 346)), fill=k, width=sw); d.line(P((567, 318), (567, 346)), fill=k, width=sw)
for x in (474, 606):
    d.line(P((x, 268), (x, 340)), fill=k, width=4 * S)
    d.line(P((x - 10, 268), (x + 10, 268)), fill=k, width=4 * S)
# shikhara
left = bez((456, 254), (468, 172), (540, 140), 30)
right = bez((540, 140), (612, 172), (624, 254), 30)
d.polygon(P(*(left + right)), fill=(254, 249, 195))
d.line(P(*left), fill=k, width=sw, joint='curve'); d.line(P(*right), fill=k, width=sw, joint='curve')
d.line(P((450, 254), (630, 254)), fill=k, width=sw)
for yy in (222, 192, 166):
    t = (254 - yy) / 114
    hw = 84 * (1 - t ** 1.6)
    d.line(P((540 - hw, yy), (540 + hw, yy)), fill=GOLD, width=3 * S)
d.ellipse(P((524, 126), (556, 146)), fill=YEL, outline=k, width=4 * S)
d.ellipse(P((532, 108), (548, 128)), fill=YEL, outline=k, width=3 * S)
d.line(P((540, 108), (540, 60)), fill=k, width=4 * S)
d.polygon(P((540, 60), (598, 74), (540, 92)), fill=YEL, outline=k)
d.line(P((540, 60), (598, 74), (540, 92)), fill=k, width=4 * S)
# side bow & arrow (line art)
for sgn in (-1, 1):
    bx = 540 + sgn * 250
    d.arc(P((bx - 40, 220), (bx + 40, 360)), 90 if sgn < 0 else 270, 270 if sgn < 0 else 90, fill=GREEN, width=5 * S)
    d.line(P((bx, 220), (bx, 360)), fill=GREEN, width=2 * S)
    d.line(P((bx - sgn * 10, 290), (bx + sgn * 70, 290)), fill=GREEN, width=4 * S)
    tip = bx + sgn * 70
    d.polygon(P((tip + sgn * 18, 290), (tip, 280), (tip, 300)), fill=GREEN)

# greeting
text(img, (540, 452), 'राम नवमी', 96, DEEP, PB, 'mm')
hl = 'की हार्दिक शुभकामनाएँ'
w = tw(hl, 50, PB)
rrect(img, (540 - w / 2 - 18, 516, 540 + w / 2 + 18, 548), 10, fill=(254, 240, 138))
text(img, (540, 528), hl, 50, GREEN, PB, 'mm')

# story pill
s = 'इस राम नवमी, अपने बिज़नेस को दें नई शुरुआत'
w = tw(s, 27, PB) + 64
rrect(img, (540 - w / 2, 582, 540 + w / 2, 634), 26, fill=GREEN)
text(img, (540, 607), s, 27, WHITE, PB, 'mm')

def mini_poster(img, x0, y0, x1, y1):
    d = L(img)
    d.rounded_rectangle(P((x0, y0), (x1, y1)), 14 * S, fill=(254, 249, 195))
    c = ((x0 + x1) / 2, y0 + 62)
    for i in range(12):
        a = i * math.pi / 6
        d.line(P((c[0] + 34 * math.cos(a), c[1] + 34 * math.sin(a)), (c[0] + 44 * math.cos(a), c[1] + 44 * math.sin(a))), fill=YEL, width=4 * S)
    d.ellipse(P((c[0] - 28, c[1] - 28), (c[0] + 28, c[1] + 28)), fill=YEL)
    text(img, ((x0 + x1) / 2, y0 + 130), 'शुभ राम नवमी', 19, DEEP, PB, 'mm')
    d.rounded_rectangle(P((x0 + 30, y1 - 40), (x1 - 30, y1 - 16)), 12 * S, fill=GREEN)
    text(img, ((x0 + x1) / 2, y1 - 28), 'Your Shop', 13, WHITE, PB, 'mm')

hub(img, T, mini_poster,
    [('ai', 'AI पोस्ट', 'सिर्फ 1 मिनट में'), ('wa', 'WhatsApp', 'हज़ारों ग्राहकों तक'),
     ('soc', '1-क्लिक पोस्ट', 'Facebook + Instagram'), ('lang', '8+ भाषाएँ', 'हिंदी, English...')],
    [('Facebook', GREEN), ('Instagram', YEL), ('WhatsApp', LGREEN)], top=664)

plans(img, T, 1112, [('फ्री शुरुआत', '₹0', ''), ('Growth', '₹1,799', ''), ('Pro', '₹3,999', '')], 'लोकप्रिय')
topbar(img, T)
cta(img, T, 'अभी कॉल / WhatsApp करें', 'टीम श्री टेक')
finish(img, '/home/claude/posters/ram-navami-hindi-light-v2.jpg')
