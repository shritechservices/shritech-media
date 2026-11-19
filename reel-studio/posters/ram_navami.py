import sys; sys.path.insert(0, '/home/claude/posters')
from fest import *

SHOT = '/home/claude/manual/screens/p04-front-page-1.jpg'
img = vgrad((255, 255, 255), (255, 249, 214))
glow(img, 540, 300, 420, (254, 235, 120), 0.55)
glow(img, 80, 1150, 360, (187, 247, 208), 0.6)
glow(img, 1050, 900, 300, (254, 240, 160), 0.5)

# faint mandala rings behind the sun
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
for k, rr in enumerate([250, 300, 350]):
    d.ellipse([(540 - rr) * S, (300 - rr) * S, (540 + rr) * S, (300 + rr) * S], outline=GOLD + (60 - k * 15,), width=2 * S)
for i in range(36):
    a = i * math.pi / 18
    for rr in (300,):
        x, y = 540 + rr * math.cos(a), 300 + rr * math.sin(a)
        d.ellipse([(x - 6) * S, (y - 6) * S, (x + 6) * S, (y + 6) * S], fill=GREEN + (55,))
img.paste(lay, (0, 0), lay)

# sun rays
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
for i in range(32):
    a = i * math.pi / 16
    L = 235 if i % 2 == 0 else 195
    w = 0.07
    pts = [(540 + 150 * math.cos(a - w), 300 + 150 * math.sin(a - w)), (540 + L * math.cos(a), 300 + L * math.sin(a)),
           (540 + 150 * math.cos(a + w), 300 + 150 * math.sin(a + w))]
    d.polygon([(x * S, y * S) for x, y in pts], fill=(GOLD if i % 2 == 0 else YEL) + (230,))
img.paste(lay, (0, 0), lay)
# sun disc (glossy)
m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse([390 * S, 150 * S, 690 * S, 450 * S], fill=255)
sun = vgrad((254, 243, 160), (234, 170, 8)); img.paste(sun, (0, 0), m)
m2 = Image.new('L', img.size, 0); ImageDraw.Draw(m2).ellipse([420 * S, 166 * S, 660 * S, 300 * S], fill=90)
img.paste(Image.new('RGB', img.size, WHITE), (0, 0), m2.filter(ImageFilter.GaussianBlur(10 * S)))

# bow and arrow (dhanush-baan) in deep green over the sun
d = ImageDraw.Draw(img)
cx, cy = 540, 300
ex, ey, rx, ry = cx + 5, cy, 80, 128
d.arc([(ex - rx) * S, (ey - ry) * S, (ex + rx) * S, (ey + ry) * S], -72, 72, fill=DEEP, width=10 * S)
e1 = (ex + rx * math.cos(math.radians(72)), ey + ry * math.sin(math.radians(72)))
e2 = (e1[0], ey - (e1[1] - ey))
nock = (cx - 62, cy)
for e in (e1, e2):
    d.line([(e[0] * S, e[1] * S), (nock[0] * S, nock[1] * S)], fill=DEEP, width=3 * S)
d.line([((cx - 90) * S, cy * S), ((cx + 128) * S, cy * S)], fill=DEEP, width=7 * S)
d.polygon([((cx + 160) * S, cy * S), ((cx + 122) * S, (cy - 19) * S), ((cx + 130) * S, cy * S), ((cx + 122) * S, (cy + 19) * S)], fill=DEEP)
for k in range(3):
    x = cx - 84 + k * 13
    d.line([(x * S, cy * S), ((x - 18) * S, (cy - 18) * S)], fill=GREEN, width=5 * S)
    d.line([(x * S, cy * S), ((x - 18) * S, (cy + 18) * S)], fill=GREEN, width=5 * S)

# marigold toran garland at the top corners
def toran(x0, x1, y, sag):
    for i in range(15):
        t = i / 14
        x = x0 + (x1 - x0) * t
        yy = y + sag * 4 * t * (1 - t)
        c = GOLD if i % 2 else YEL
        d.ellipse([(x - 13) * S, (yy - 13) * S, (x + 13) * S, (yy + 13) * S], fill=c)
        d.ellipse([(x - 6) * S, (yy - 9) * S, (x + 2) * S, (yy - 3) * S], fill=LYEL)
        if i % 3 == 1:
            d.polygon([(x * S, (yy + 12) * S), ((x - 9) * S, (yy + 34) * S), (x * S, (yy + 46) * S), ((x + 9) * S, (yy + 34) * S)], fill=GREEN)
toran(-10, 330, 118, 70)
toran(750, 1090, 118, 70)

# top bar
logo(img, 48, 34, 44)
pw = tw('9993615146', 30, PB) + 98
grad_box(img, (1032 - pw, 34, 1032, 96), 31, (16, 120, 60), DEEP)
phone_icon(img, 1032 - pw + 36, 66, 28, YEL)
text(img, (1032 - pw + 64, 66), '9993615146', 30, YEL, PB, 'lm')

# greeting
pl = 'जय श्री राम'
w0 = tw(pl, 26, PSB) + 56
rrect(img, (540 - w0 / 2, 468, 540 + w0 / 2, 516), 24, fill=YEL)
text(img, (540, 491), pl, 26, DEEP, PSB, 'mm')
grad_text(img, (540, 572), 'राम नवमी की', 66, (22, 140, 64), DEEP, PB, 'mm', shadow=(GOLD, 0.2))
grad_text(img, (540, 656), 'हार्दिक शुभकामनाएँ', 70, (250, 204, 21), (190, 128, 4), PB, 'mm', shadow=(GOLD, 0.25))
text(img, (540, 722), 'मर्यादा, विश्वास और नई शुरुआत का पावन पर्व', 28, DEEP, PM, 'mm')

# business card
CX0, CY0, CX1, CY1 = 40, 768, 1040, 1184
shadow(img, (CX0, CY0, CX1, CY1), 36, blur=22, alpha=0.22, color=DEEP)
rrect(img, (CX0, CY0, CX1, CY1), 36, fill=WHITE)
rrect(img, (CX0, CY0, CX1, CY1), 36, outline=(187, 247, 208), width=3)
grad_box(img, (CX0, CY0, CX1, CY0 + 14), 7, YEL, GOLD, gloss=False)
# phone peeking out of the card
phone_mock(img, SHOT, 58, 792, 252, rot=-4, crop_top=0, crop_h=1120)
X = 352
text(img, (X, 822), 'इस राम नवमी, बिज़नेस की नई शुरुआत', 31, DEEP, PB, 'lm')
text(img, (X, 864), 'Shri Tech के साथ — आसान, तेज़ और स्मार्ट', 25, GREEN, PSB, 'lm')
items = ['AI से पोस्ट सिर्फ 1 मिनट में', 'Facebook + Instagram पर 1-क्लिक पोस्ट',
         'WhatsApp पर एक क्लिक में हज़ारों ग्राहक', 'हिंदी, English समेत 8+ भाषाएँ']
for i, s in enumerate(items):
    y = 920 + i * 50
    check(img, X + 16, y, 16, GREEN, WHITE)
    text(img, (X + 44, y), s, 26, (20, 40, 28), PM, 'lm')
# plan chips
chips = [('फ्री में शुरू करें', YEL, DEEP), ('Growth ₹1,799', MINT, DEEP), ('Pro ₹3,999', MINT, DEEP)]
x = X
for s, bg, fg in chips:
    w = tw(s, 22, PBD) + 36
    rrect(img, (x, 1136 - 22, x + w, 1136 + 22), 22, fill=bg, outline=(GREEN if bg == MINT else None), width=2)
    text(img, (x + w / 2, 1136), s, 22, fg, PBD, 'mm')
    x += w + 12

# bottom CTA band
grad_box(img, (0, 1206, 1080, 1350), 0, (18, 128, 62), DEEP)
glow(img, 860, 1280, 200, (34, 197, 94), 0.25)
text(img, (48, 1250), 'अभी कॉल / WhatsApp करें', 26, WHITE, PSB, 'lm')
phone_icon(img, 74, 1305, 46, YEL)
grad_text(img, (112, 1306), '9993615146', 58, (254, 240, 138), (234, 179, 8), PB, 'lm')
text(img, (1032, 1258), 'टीम श्री टेक', 28, YEL, PB, 'rm')
text(img, (1032, 1298), 'Shri Balaji Digital Services', 22, WHITE, PM, 'rm')
for sx, sy, r in [(990, 440, 16), (88, 400, 12), (968, 540, 9), (110, 600, 10)]:
    sparkle(img, sx, sy, r, GOLD)

finish(img, '/home/claude/posters/ram-navami-hindi-light.jpg')
