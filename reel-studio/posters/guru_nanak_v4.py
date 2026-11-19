"""Guru Nanak Jayanti (24 Nov 2026) - light theme, Hindi. Audience: shopkeepers. Feature: WhatsApp bulk (4 steps)."""
import sys; sys.path.insert(0, '/home/claude/posters')
from v3 import *

T = LIGHT
img = Image.new('RGB', (W, H), WHITE)
glow(img, 540, 250, 320, (254, 243, 170), 0.6)
glow(img, 300, 900, 480, (220, 252, 231), 0.55)
d = L(img)
k = DEEP; sw = 5 * S

# ---- Ik Onkar in a glowing circle of light (prakash), with a row of diyas ----
cx, cy = 540, 232
glow(img, cx, cy, 230, (254, 236, 140), 0.65)
for i in range(36):
    a = i * math.pi / 18
    r0, r1 = 142, (196 if i % 2 == 0 else 172)
    if math.sin(a) > 0.5: continue
    d.line(P((cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))),
           fill=YEL if i % 2 == 0 else (250, 222, 90), width=5 * S)
for i in range(48):
    a = i * math.pi / 24
    x, y = cx + 214 * math.cos(a), cy + 214 * math.sin(a)
    if y > 330: continue
    d.ellipse(P((x - 3.5, y - 3.5), (x + 3.5, y + 3.5)), fill=GREEN)
d.ellipse(P((cx - 124, cy - 124), (cx + 124, cy + 124)), fill=WHITE, outline=YEL, width=7 * S)
d.ellipse(P((cx - 108, cy - 108), (cx + 108, cy + 108)), outline=(187, 247, 208), width=3 * S)
# the symbol, centred by its bounding box
gf = ImageFont.truetype('/home/claude/posters/NotoSansGurmukhi.ttf', int(118 * S)); gf.set_variation_by_name(b'Bold')
m = Image.new('L', (int(300 * S), int(300 * S)), 0)
ImageDraw.Draw(m).text((0, 0), '\u0A74', font=gf, fill=255)
bb = m.getbbox(); m = m.crop(bb)
img.paste(Image.new('RGB', m.size, DEEP), (int(cx * S - m.size[0] / 2), int(cy * S - m.size[1] / 2) + int(4 * S)), m)
# deepmala: diyas on a line under the circle
d.line(P((150, 394), (930, 394)), fill=(134, 199, 157), width=3 * S)
for x in range(170, 931, 76):
    if 400 < x < 680: continue
    glow(img, x, 368, 26, (250, 204, 21), 0.45)
    d.chord(P((x - 20, 362), (x + 20, 392)), 0, 180, fill=YEL)
    d.line(P((x - 20, 377), (x + 20, 377)), fill=DEEP, width=3 * S)
    d.polygon(P((x - 6, 375), (x, 344), (x + 6, 375)), fill=GOLD)
    d.ellipse(P((x - 3, 362), (x + 3, 372)), fill=(255, 251, 225))

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

# ---- right: 4-step cards filling the column (x 334..1040) ----
X0, X1 = 330, 1032
text(img, (X0, 684), 'WhatsApp से हर ग्राहक तक', 29, DEEP, PB, 'lm')
text(img, (X0, 722), '4 आसान स्टेप, सब एक ही प्लेटफॉर्म पर', 22, GREEN, PSB, 'lm')
steps = [('sheet', 'Excel से कॉन्टैक्ट जोड़ें', 'एक फाइल में ढेरों नंबर', '5,000 / फाइल'),
         ('tmpl', 'अपना मैसेज टेम्पलेट बनाएँ', 'Meta अप्रूवल यहीं से', 'अप्रूव्ड'),
         ('send', 'एक क्लिक में सबको भेजें', 'अभी या तय समय पर', '1 क्लिक'),
         ('chart', 'रिपोर्ट और लाइव चैट', 'किसने पढ़ा, किसने जवाब दिया', 'रिपोर्ट')]
top, ch, gap = 754, 72, 12
for i, (ic, a, b, tag) in enumerate(steps):
    y0 = top + i * (ch + gap); yc = y0 + ch / 2
    rrect(img, (X0, y0, X1, y0 + ch), 20, fill=WHITE, outline=(209, 250, 223), width=2)
    circ_node(img, X0 + 44, yc, 30, T, ic, num=None)
    text(img, (X0 + 92, yc - 14), a, 24, DEEP, PB, 'lm')
    text(img, (X0 + 92, yc + 17), b, 19, (55, 80, 64), PM, 'lm')
    tw_ = tw(tag, 18, PB) + 28
    rrect(img, (X1 - 18 - tw_, yc - 17, X1 - 18, yc + 17), 17, fill=(254, 240, 138))
    text(img, (X1 - 18 - tw_ / 2, yc), tag, 18, DEEP, PB, 'mm')

# ---- offer ribbon for shopkeepers (centred) ----
RY = 1098
rrect(img, (48, RY, 1032, RY + 92), 22, fill=(254, 249, 195), outline=YEL, width=3)
rich(img, 540, RY + 27, [('दुकानदारों के लिए WhatsApp मार्केटिंग', 24, DEEP, PB), ('सिर्फ ₹999/माह', 24, GREEN, PB)])
chips = ['किराना', 'कपड़ा', 'मिठाई', 'मोबाइल शॉप', 'मेडिकल स्टोर', 'हार्डवेयर']
ws = [tw(c, 18, PSB) + 26 for c in chips]
cx_ = 540 - (sum(ws) + 10 * (len(ws) - 1)) / 2
for chip, w in zip(chips, ws):
    rrect(img, (cx_, RY + 48, cx_ + w, RY + 75), 13, fill=WHITE, outline=(134, 199, 157), width=2)
    text(img, (cx_ + w / 2, RY + 61), chip, 18, DEEP, PSB, 'mm')
    cx_ += w + 10

logo(img, 48, 34, 44, dark=False)
num_pill(img, 1032, 36, False)
cta3(img, T, 'अपनी दुकान के लिए फ्री डेमो — कॉल / WhatsApp')
finish3(img, '/home/claude/posters/guru-nanak-jayanti-hindi-light-v4.jpg', 'Guru Nanak Jayanti 2026 - Shri Tech')
