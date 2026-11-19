"""Post 8 (Indian Army Day) redo: same top, CRM 7-step line diagram instead of the quote."""
import sys
sys.path.insert(0, '/home/claude/posters/series')
import gloss, build2
from art2 import *
from gloss import grrect, gellipse
from kit import rich2, segs_fit

SUBC = (40, 62, 48)
img = gloss.base()
gloss.glossy_art(img, ART['army'])
gloss.greeting(img, 'भारतीय सेना दिवस', 'हमारे वीर जवानों को सलाम')
gloss.story_pill(img, 'जय हिंद! सेना जैसा अनुशासन, हर ग्राहक के साथ')

# heading bar
y0 = 662
shadow(img, (M, y0, 1080 - M, y0 + 72), 36, blur=12, alpha=0.25, off=6, color=DEEP)
grrect(img, (M, y0, 1080 - M, y0 + 72), 36, (22, 110, 56), (6, 46, 25), 0.3)
rich2(img, 540, y0 + 36, segs_fit([('@ST', 30), ('WhatsApp CRM:', 28, WHITE, PB), ('7 स्टेप', 30, (254, 240, 138), PB), ('में पूरा सिस्टम', 28, WHITE, PB)], 940), dark=True)

steps = [('sheet', 'कॉन्टैक्ट जोड़ें', 'Excel से एक साथ'),
         ('users', 'ग्रुप बनाएँ', 'टैग से अलग लिस्ट'),
         ('tmpl', 'टेम्पलेट बनाएँ', 'ऑफर, रिमाइंडर'),
         ('shield', 'Meta मंज़ूरी', 'प्लेटफ़ॉर्म से ही'),
         ('send', 'कैंपेन भेजें', 'अभी या तय समय'),
         ('chart', 'रिपोर्ट देखें', 'भेजा, पहुँचा, पढ़ा'),
         ('chat', 'चैट में जवाब', 'ग्राहक से सीधी बात')]
# snake: row1 left->right (4), row2 right->left (3)
r1 = 806; r2 = 990
x1 = [M + 100 + i * ((1080 - 2 * M - 260) / 3) for i in range(4)]
x2 = [x1[3] - 0.5 * (x1[1] - x1[0]) - i * (x1[1] - x1[0]) for i in range(3)]
pos = [(x, r1) for x in x1] + [(x, r2) for x in x2]
d = ImageDraw.Draw(img)
LC = (134, 199, 157)
for i in range(6):
    (ax, ay), (bx, by) = pos[i], pos[i + 1]
    if ay == by:
        dashed(img, [(ax, ay), (bx, by)], LC, w=4, dash=12, gap=8)
        mx = (ax + bx) / 2; sg = 1 if bx > ax else -1
        d.polygon(P((mx - 10 * sg, ay - 12), (mx + 12 * sg, ay), (mx - 10 * sg, ay + 12)), fill=GREEN)
    else:   # U-turn on the right
        pts = bez((ax + 48, ay), (1052, (ay + by) / 2), (bx + 48, by), 30)
        dashed(img, pts, LC, w=4, dash=12, gap=8)
for i, ((x, y), (ic, a, b)) in enumerate(zip(pos, steps)):
    gloss.node(img, x, y, 46, ic, num=i + 1)
    text(img, (x, y + 70), a, fit(a, 23, PB, 210), DEEP, PB, 'mm')
    text(img, (x, y + 98), b, fit(b, 18, PBD, 210), SUBC, PBD, 'mm')

# strip
ys = 1128
shadow(img, (M, ys, 1080 - M, ys + 68), 22, blur=12, alpha=0.15, off=6, color=GOLD)
grrect(img, (M, ys, 1080 - M, ys + 68), 22, (255, 251, 225), (254, 240, 138), 0.3)
rrect(img, (M, ys, 1080 - M, ys + 68), 22, outline=YEL, width=3)
rich2(img, 540, ys + 34, segs_fit([('अनुशासन और भरोसा —', 24, DEEP, PB), ('हर ग्राहक तक सही समय पर सही संदेश', 24, (21, 128, 61), PB)], 940))

gloss.cta(img, 'अपने बिज़नेस को WhatsApp CRM से जोड़ें — कॉल / WhatsApp करें')
build2.header(img)
finish3(img, '/home/claude/posters/series/out2/08-2027-01-15-indian-army-day-crm.jpg', 'Indian Army Day 2027 - Shri Tech')
