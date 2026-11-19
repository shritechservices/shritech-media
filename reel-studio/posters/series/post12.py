"""Post 12 Shivaji Maharaj Jayanti redo: centre circle (festival ~35%), left = time-wasting old ways (X), right = Shri Tech digital (check)."""
import sys
sys.path.insert(0, '/home/claude/posters/series')
import gloss, build2
from art2 import *
from gloss import grrect, gellipse, gshape
from kit import rich2, segs_fit

SUBC = (40, 62, 48); RED1, RED2 = (248, 113, 113), (185, 28, 28)
img = gloss.base()

# title
s = fit('छत्रपति शिवाजी महाराज जयंती', 62, PB, 980)
grad_text(img, (540, 150), 'छत्रपति शिवाजी महाराज जयंती', s, (21, 128, 61), (6, 52, 28), PB, 'mm', shadow=(GOLD, 0.22), gloss=False)
l2 = 'स्वराज्य के प्रेरणास्रोत को कोटि-कोटि नमन'
w = tw(l2, 32, PB)
grrect(img, (540 - w / 2 - 20, 196, 540 + w / 2 + 20, 244), 12, (254, 243, 160), (250, 214, 60), 0.35)
text(img, (540, 220), l2, 32, (21, 110, 52), PB, 'mm')

# centre circle with the festival art
tmp = gloss.base(); gloss.glossy_art(tmp, ART['shivaji'], y1=520)
crop = tmp.crop((int(250 * S), int(20 * S), int(830 * S), int(600 * S)))
R = 185; CX, CY = 540, 468
gellipse(img, CX, CY, R + 34, R + 34, (254, 240, 138), (202, 138, 4), 0.4)
gellipse(img, CX, CY, R + 14, R + 14, (52, 211, 110), (21, 101, 52), 0.3)
cr = crop.resize((int(2 * R * S), int(2 * R * S)), Image.LANCZOS)
m = Image.new('L', cr.size, 0); ImageDraw.Draw(m).ellipse((0, 0, cr.width - 1, cr.height - 1), fill=255)
img.paste(cr, (int((CX - R) * S), int((CY - R) * S)), m)
sh = Image.new('L', cr.size, 0); ImageDraw.Draw(sh).ellipse((cr.width * 0.12, cr.height * 0.03, cr.width * 0.88, cr.height * 0.4), fill=45)
img.paste(Image.new('RGB', cr.size, WHITE), (int((CX - R) * S), int((CY - R) * S)), ImageChops.multiply(sh.filter(ImageFilter.GaussianBlur(14 * S)), m))
pl = 'जय भवानी, जय शिवाजी!'
w = tw(pl, 26, PB) + 60
shadow(img, (540 - w / 2, CY + R + 22, 540 + w / 2, CY + R + 72), 25, blur=10, alpha=0.25, off=5, color=DEEP)
grrect(img, (540 - w / 2, CY + R + 22, 540 + w / 2, CY + R + 72), 25, (52, 211, 110), (21, 128, 61), 0.35)
text(img, (540, CY + R + 47), pl, 26, WHITE, PB, 'mm')

# side quotes beside the circle
for x, a in ((150, ['साहस', 'स्वाभिमान']), (930, ['रणनीति', 'सुशासन'])):
    for i, t in enumerate(a):
        yy = 400 + i * 120
        gellipse(img, x, yy, 50, 50, (255, 255, 255), (236, 252, 243), 0)
        ImageDraw.Draw(img).ellipse(P((x - 50, yy - 50), (x + 50, yy + 50)), outline=YEL, width=int(3 * S))
        star5(img, x, yy - 14, 13, YEL, None)
        text(img, (x, yy + 20), t, fit(t, 20, PB, 84), DEEP, PB, 'mm')

# heading of the comparison
yh = 760
rich2(img, 540, yh, segs_fit([('शिवाजी महाराज की तरह', 30, DEEP, PB), ('सही रणनीति अपनाइए:', 30, (21, 128, 61), PB)], 980))

# two cards
top, bot = 800, 1112
cw = (1080 - 2 * M - 40) / 2
L0, R0 = M, M + cw + 40
for x0, good in ((L0, False), (R0, True)):
    shadow(img, (x0, top, x0 + cw, bot), 26, blur=14, alpha=0.18, off=8, color=DEEP)
    gloss.grrect(img, (x0, top, x0 + cw, bot), 26, (255, 255, 255), (240, 253, 244) if good else (255, 247, 237), 0)
    rrect(img, (x0, top, x0 + cw, bot), 26, outline=(GREEN if good else (252, 165, 165)), width=3)
    hb = (x0, top, x0 + cw, top + 64)
    if good: grrect(img, hb, 26, (52, 211, 110), (21, 128, 61), 0.35)
    else: grrect(img, hb, 26, RED1, RED2, 0.3)
    ImageDraw.Draw(img).rectangle(P((x0, top + 40), (x0 + cw, top + 64)), fill=(21, 128, 61) if good else RED2)
    head = 'डिजिटल अपनाइए' if good else 'फ़ालतू काम हटाइए'
    text(img, (x0 + cw / 2, top + 32), head, 28, WHITE, PB, 'mm')

bad = ['पर्चे बाँटे, पता नहीं किसने देखे', 'एक-एक ग्राहक को कॉल-मैसेज', 'हर पोस्टर पर डिज़ाइनर का इंतज़ार', 'ग्राहकों का कोई रिकॉर्ड नहीं', 'अंदाज़े से प्रचार, नतीजा शून्य']
good = ['WhatsApp CRM: सारे ग्राहक एक जगह', 'एक क्लिक में बल्क मैसेज', 'मिनटों में ब्रांडेड पोस्टर', 'किसने पढ़ा, पूरी रिपोर्ट', 'चैट में तुरंत जवाब, पक्का ग्राहक']
d = ImageDraw.Draw(img)
for i, (b, g) in enumerate(zip(bad, good)):
    y = top + 100 + i * 45
    gellipse(img, L0 + 34, y, 15, 15, RED1, RED2, 0.3)
    d.line(P((L0 + 28, y - 6), (L0 + 40, y + 6)), fill=WHITE, width=int(4 * S)); d.line(P((L0 + 40, y - 6), (L0 + 28, y + 6)), fill=WHITE, width=int(4 * S))
    text(img, (L0 + 60, y), b, fit(b, 21, PBD, cw - 76), (120, 60, 50), PBD, 'lm')
    gellipse(img, R0 + 34, y, 15, 15, (74, 222, 128), (21, 128, 61), 0.3)
    d.line(P((R0 + 27, y), (R0 + 32, y + 6), (R0 + 42, y - 6)), fill=WHITE, width=int(4 * S), joint='curve')
    text(img, (R0 + 60, y), g, fit(g, 21, PB, cw - 76), DEEP, PB, 'lm')

# sword divider between the cards
cx = 540
ln(img, [(cx, top + 10), (cx, bot - 50)], (170, 180, 175), 8)
ln(img, [(cx, top + 10), (cx, bot - 50)], WHITE, 2)
poly(img, [(cx - 8, top + 14), (cx, top - 14), (cx + 8, top + 14)], (220, 228, 224), K, 2)
gloss.grrect(img, (cx - 26, bot - 54, cx + 26, bot - 42), 5, (254, 240, 138), (202, 138, 4), 0.3)
gloss.grrect(img, (cx - 7, bot - 42, cx + 7, bot - 6), 4, (120, 80, 40), (70, 45, 25), 0.2)
gellipse(img, cx, bot - 2, 10, 10, (254, 240, 138), (202, 138, 4), 0.3)

# strip
ys = 1132
shadow(img, (M, ys, 1080 - M, ys + 64), 22, blur=12, alpha=0.15, off=6, color=GOLD)
grrect(img, (M, ys, 1080 - M, ys + 64), 22, (255, 251, 225), (254, 240, 138), 0.3)
rrect(img, (M, ys, 1080 - M, ys + 64), 22, outline=YEL, width=3)
rich2(img, 540, ys + 32, segs_fit([('समय बचाइए, ग्राहक बढ़ाइए —', 24, DEEP, PB), ('@ST', 26), ('के साथ', 24, DEEP, PB)], 940))

gloss.cta(img, 'अपने बिज़नेस को डिजिटल बनाइए — कॉल / WhatsApp करें')
build2.header(img)
finish3(img, '/home/claude/posters/series/out2/12-2027-02-19-shivaji-jayanti-digital.jpg', 'Shivaji Maharaj Jayanti 2027 - Shri Tech')
