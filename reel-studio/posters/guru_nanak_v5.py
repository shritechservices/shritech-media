"""Guru Nanak Jayanti (24 Nov 2026) - light theme, Hindi. Audience: shopkeepers. Feature: WhatsApp bulk (4 steps)."""
import sys; sys.path.insert(0, '/home/claude/posters')
from v3 import *

T = LIGHT
img = Image.new('RGB', (W, H), WHITE)
glow(img, 540, 250, 320, (254, 243, 170), 0.6)
glow(img, 300, 900, 480, (220, 252, 231), 0.55)
d = L(img)
k = DEEP; sw = 5 * S

# prakash: dotted light rays behind the gurdwara
cx, cy = 540, 250
for i in range(30):
    a = math.pi + i * math.pi / 29
    for rr in (150, 175, 200):
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        r = 4 if rr != 175 else 3
        d.ellipse(P((x - r, y - r), (x + r, y + r)), fill=YEL if rr != 175 else GREEN)

# gurdwara line art
d.rectangle(P((360, 366), (720, 388)), fill=WHITE, outline=k, width=sw)          # plinth
d.rectangle(P((410, 268), (670, 366)), fill=WHITE, outline=k, width=sw)          # hall
for x0 in (432, 512, 592):                                                         # arches
    d.rounded_rectangle(P((x0, 296), (x0 + 56, 366)), 28 * S, fill=(254, 249, 195), outline=k, width=4 * S)
    d.rectangle(P((x0 + 2, 340), (x0 + 54, 364)), fill=(254, 249, 195))
d.line(P((410, 284), (670, 284)), fill=GOLD, width=3 * S)
# main onion dome
left = bez((470, 268), (436, 200), (540, 128), 30)
right = bez((540, 128), (644, 200), (610, 268), 30)
d.polygon(P(*(left + right)), fill=(254, 240, 138))
d.line(P(*left), fill=k, width=sw, joint='curve'); d.line(P(*right), fill=k, width=sw, joint='curve')
d.line(P((466, 268), (614, 268)), fill=k, width=sw)
for t in (0.35, 0.6):
    y = 268 - t * 110
    d.arc(P((540 - 70 * (1 - t * 0.7), y - 10), (540 + 70 * (1 - t * 0.7), y + 10)), 0, 180, fill=GOLD, width=3 * S)
d.ellipse(P((531, 106), (549, 126)), fill=YEL, outline=k, width=3 * S)
d.line(P((540, 106), (540, 88)), fill=k, width=4 * S)
# corner chhatris
for x in (425, 655):
    d.rectangle(P((x - 16, 238), (x + 16, 268)), fill=WHITE, outline=k, width=4 * S)
    dl = bez((x - 18, 238), (x - 16, 214), (x, 204), 12); dr = bez((x, 204), (x + 16, 214), (x + 18, 238), 12)
    d.polygon(P(*(dl + dr)), fill=(254, 240, 138)); d.line(P(*(dl + dr)), fill=k, width=4 * S)
    d.line(P((x, 204), (x, 192)), fill=k, width=3 * S)
# Nishan Sahib (flag pole) on the right
d.line(P((780, 388), (780, 150)), fill=k, width=5 * S)
d.polygon(P((780, 128), (772, 152), (788, 152)), fill=k)
d.polygon(P((780, 156), (842, 186), (780, 214)), fill=YEL)
d.line(P((780, 156), (842, 186), (780, 214)), fill=k, width=4 * S)
# diyas row on the plinth
for i, x in enumerate(range(300, 800, 50)):
    if 360 <= x <= 720: continue
for x in (330, 750):
    glow(img, x, 360, 30, (250, 204, 21), 0.5)
    d.chord(P((x - 22, 360), (x + 22, 392)), 0, 180, fill=YEL); d.line(P((x - 22, 376), (x + 22, 376)), fill=k, width=3 * S)
    d.polygon(P((x - 6, 374), (x, 346), (x + 6, 374)), fill=GOLD)
for sx, sy, r in [(150, 200, 13), (930, 260, 12), (220, 330, 8), (880, 360, 8)]:
    sparkle(img, sx, sy, r, GOLD)

# greeting
text(img, (540, 452), 'गुरु नानक जयंती', 84, DEEP, PB, 'mm')
hl = 'प्रकाश पर्व की लख-लख बधाइयाँ'
w = tw(hl, 44, PB)
rrect(img, (540 - w / 2 - 18, 514, 540 + w / 2 + 18, 544), 10, fill=(254, 240, 138))
text(img, (540, 522), hl, 44, GREEN, PB, 'mm')
s = 'वंड छको — खुशियाँ बाँटो, हर ग्राहक के साथ'
w = tw(s, 27, PB) + 64
rrect(img, (540 - w / 2, 580, 540 + w / 2, 632), 26, fill=GREEN)
text(img, (540, 605), s, 27, WHITE, PB, 'mm')

# ---- left: vector phone showing a WhatsApp campaign ----
x, y, w_, h_ = 48, 668, 252, 410
shadow(img, (x, y, x + w_, y + h_), 34, blur=20, alpha=0.22, off=10, color=DEEP)
d.rounded_rectangle(P((x, y), (x + w_, y + h_)), 34 * S, fill=(18, 30, 22))
sx0, sy0, sx1, sy1 = x + 10, y + 10, x + w_ - 10, y + h_ - 10
d.rounded_rectangle(P((sx0, sy0), (sx1, sy1)), 26 * S, fill=(240, 253, 244))
d.rounded_rectangle(P((sx0, sy0), (sx1, sy0 + 64)), 26 * S, fill=WHITE)
d.rectangle(P((sx0, sy0 + 34), (sx1, sy0 + 64)), fill=WHITE)
wordmark(img, sx0 + 16, sy0 + 40, 17)
text(img, (sx1 - 14, sy0 + 40), 'WhatsApp', 13, GREEN, PSB, 'rm')
bx0, by0, bx1 = sx0 + 12, sy0 + 78, sx1 - 12
d.rounded_rectangle(P((bx0, by0), (bx1, by0 + 190)), 14 * S, fill=WHITE, outline=(209, 250, 223), width=2 * S)
d.rounded_rectangle(P((bx0 + 8, by0 + 8), (bx1 - 8, by0 + 108)), 10 * S, fill=(254, 249, 195))
c = ((bx0 + bx1) / 2, by0 + 54)
glow(img, c[0], c[1] - 6, 40, (250, 204, 21), 0.4)
d.chord(P((c[0] - 26, c[1] - 6), (c[0] + 26, c[1] + 24)), 0, 180, fill=YEL)
d.polygon(P((c[0] - 7, c[1] + 6), (c[0], c[1] - 26), (c[0] + 7, c[1] + 6)), fill=GOLD)
text(img, (c[0], by0 + 94), 'प्रकाश पर्व ऑफर', 15, DEEP, PB, 'mm')
text(img, (bx0 + 12, by0 + 128), 'नमस्ते {{नाम}} जी,', 13, DEEP, PSB, 'lm')
text(img, (bx0 + 12, by0 + 150), 'आज सभी सामान पर 10% छूट', 13, (55, 80, 64), PM, 'lm')
text(img, (bx1 - 12, by0 + 174), '✓✓', 14, GREEN, SYM, 'rm')
yy = by0 + 204
d.rounded_rectangle(P((bx0, yy), (bx1, yy + 44)), 10 * S, fill=WHITE)
text(img, (bx0 + 12, yy + 22), '1,200 ग्राहकों को भेजा', 14, DEEP, PB, 'lm')
yy += 54
d.rounded_rectangle(P((bx0, yy), (bx1, yy + 52)), 10 * S, fill=WHITE)
text(img, (bx0 + 12, yy + 16), 'पढ़ा', 13, (55, 80, 64), PSB, 'lm'); text(img, (bx1 - 12, yy + 16), '87%', 14, GREEN, PB, 'rm')
d.rounded_rectangle(P((bx0 + 12, yy + 32), (bx1 - 12, yy + 40)), 4 * S, fill=(209, 250, 223))
d.rounded_rectangle(P((bx0 + 12, yy + 32), (bx0 + 12 + (bx1 - bx0 - 24) * 0.87, yy + 40)), 4 * S, fill=GREEN)

# ---- right: 3 simple steps (big icons, short words) ----
X0, X1 = 330, 1032
rich(img, X0, 690, [('सिर्फ', 30, DEEP, PB), ('3 स्टेप', 30, GREEN, PB), ('में हर ग्राहक तक', 30, DEEP, PB)], anchor='l')
steps = [('sheet', 'ग्राहकों की लिस्ट डालें'), ('tmpl', 'ऑफर का मैसेज चुनें'), ('send', 'एक क्लिक में सबको भेजें')]
top, ch, gap = 742, 96, 22
for i, (ic, a) in enumerate(steps):
    y0 = top + i * (ch + gap); yc = y0 + ch / 2
    rrect(img, (X0, y0, X1, y0 + ch), 24, fill=WHITE, outline=(209, 250, 223), width=2)
    circ_node(img, X0 + 70, yc, 36, T, ic, num=None)
    text(img, (X0 + 130, yc), a, 28, DEEP, PB, 'lm')
    bx = X1 - 52
    L(img).ellipse(P((bx - 26, yc - 26), (bx + 26, yc + 26)), fill=YEL)
    text(img, (bx, yc + 1), str(i + 1), 28, DEEP, PB, 'mm')
    if i < 2:   # down arrow between cards
        ax = X0 + 70; ay = y0 + ch + gap / 2
        L(img).polygon(P((ax - 9, ay - 6), (ax + 9, ay - 6), (ax, ay + 7)), fill=GREEN)

# ---- ribbon: who it is for (no prices) ----
RY = 1098
rrect(img, (48, RY, 1032, RY + 92), 22, fill=(254, 249, 195), outline=YEL, width=3)
rich(img, 540, RY + 27, [('हर दुकान के लिए', 24, DEEP, PB), ('WhatsApp मार्केटिंग', 24, GREEN, PB)])
chips = ['किराना', 'कपड़ा', 'मिठाई', 'मोबाइल शॉप', 'मेडिकल स्टोर', 'हार्डवेयर']
ws = [tw(c, 18, PSB) + 26 for c in chips]
cx_ = 540 - (sum(ws) + 10 * (len(ws) - 1)) / 2
for chip, w in zip(chips, ws):
    rrect(img, (cx_, RY + 48, cx_ + w, RY + 75), 13, fill=WHITE, outline=(134, 199, 157), width=2)
    text(img, (cx_ + w / 2, RY + 61), chip, 18, DEEP, PSB, 'mm')
    cx_ += w + 10

logo(img, 48, 34, 44, dark=False)
num_pill(img, 1032, 36, False)
cta3(img, T, 'अपनी दुकान की ग्रोथ के लिए — कॉल / WhatsApp करें')
finish3(img, '/home/claude/posters/guru-nanak-jayanti-hindi-light-v5.jpg', 'Guru Nanak Jayanti 2026 - Shri Tech')
