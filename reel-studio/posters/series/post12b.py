"""Post 12 v3: Shivaji Jayanti hero (rider on hill at sunrise) + WhatsApp bulk messaging phone with customers ring
+ 'where to use' grid. Hindi + English mix, light theme."""
import sys
sys.path.insert(0, '/home/claude/posters/series')
import gloss, build2
from art2 import *
from gloss import grrect, gellipse, gshape, grad_mask_fill
from kit import rich2, segs_fit, ICONS

FD = '/home/claude/fonts2/'
def F2(name, size):
    f = ImageFont.truetype(FD + name, int(size * S), layout_engine=ImageFont.Layout.RAQM)
    try:
        if 'Playfair' in name: f.set_variation_by_name(b'Bold')
        if 'Montserrat' in name: f.set_variation_by_name(b'ExtraBold')
    except Exception: pass
    return f
def T2(img, xy, txt, font, color, anchor='mm'):
    ImageDraw.Draw(img).text((xy[0] * S, xy[1] * S), txt, font=font, fill=color, anchor=anchor)
def GT2(img, xy, txt, font, c1, c2, anchor='mm', shadow_=None):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).text((xy[0] * S, xy[1] * S), txt, font=font, fill=255, anchor=anchor)
    if shadow_:
        img.paste(Image.new('RGB', img.size, shadow_[0]), (0, int(4 * S)), m.filter(ImageFilter.GaussianBlur(5 * S)).point(lambda v: int(v * shadow_[1])))
    grad_mask_fill(img, m, c1, c2, sheen=0.0)

SUBC = (40, 62, 48)
img = gloss.base()

# ================= HERO: sunrise, hill, rider with flags =================
HX0, HY0, HX1, HY1 = M, 108, 1080 - M, 520
hero = Image.new('L', img.size, 0); ImageDraw.Draw(hero).rounded_rectangle(P((HX0, HY0), (HX1, HY1)), 36 * S, fill=255)
grad_mask_fill(img, hero, (255, 251, 225), (253, 214, 90), sheen=0.0)
# sun + rays (clipped to hero)
lay = img.copy()
glow(lay, 600, 330, 300, (255, 255, 230), 0.8)
for i in range(36):
    a = i * math.pi / 18; da = 0.05
    ImageDraw.Draw(lay).polygon(P((600, 330), (600 + 700 * math.cos(a - da), 330 + 700 * math.sin(a - da)), (600 + 700 * math.cos(a + da), 330 + 700 * math.sin(a + da))), fill=(255, 244, 190))
gellipse(lay, 600, 330, 92, 92, (255, 252, 230), (253, 224, 71), 0.4)
img.paste(lay, (0, 0), hero)
# clouds
for (cx, cy, w) in [(200, 200, 140), (880, 230, 170), (760, 160, 90)]:
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle(P((cx - w, cy - 12), (cx + w, cy + 12)), 12 * S, fill=150)
    img.paste(Image.new('RGB', img.size, WHITE), (0, 0), ImageChops.multiply(m.filter(ImageFilter.GaussianBlur(3 * S)), hero))

INK = ((40, 120, 66), (6, 46, 25))
sil = Image.new('L', img.size, 0); d = ImageDraw.Draw(sil)
def L_(pts, w): d.line(P(*pts), fill=255, width=int(w * S), joint='curve')
def E_(cx, cy, rx, ry): d.ellipse(P((cx - rx, cy - ry), (cx + rx, cy + ry)), fill=255)
def PG(pts): d.polygon(P(*pts), fill=255)
# hill
PG([(HX0, 470)] + bez((HX0, 470), (420, 360), (700, 430), 30) + bez((700, 430), (900, 470), (HX1, 440), 20) + [(HX1, HY1), (HX0, HY1)])
# flag poles + flags
for (px, py, h) in [(250, 330, 150), (820, 330, 150)]:
    L_([(px, py + 60), (px, py - h + 60)], 5)
    PG([(px, py - h + 62)] + bez((px, py - h + 62), (px + 50, py - h + 40), (px + 95, py - h + 74), 10) + [(px + 70, py - h + 96)] +
       bez((px + 95, py - h + 112), (px + 50, py - h + 90), (px, py - h + 112), 10))
# horse (rearing, facing left) + rider
HCX, HCY, hs = 560, 318, 1.25
def H(x, y): return (HCX + x * hs, HCY + y * hs)
def HL(pts, w): L_([H(*p) for p in pts], w * hs)
bodym = Image.new('L', (int(260 * hs * S), int(120 * hs * S)), 0)
ImageDraw.Draw(bodym).ellipse((int(70 * hs * S), int(35 * hs * S), int(190 * hs * S), int(85 * hs * S)), fill=255)
bodym = bodym.rotate(-35, resample=Image.BICUBIC)
sil.paste(255, (int(H(-130, -60)[0] * S), int(H(-130, -60)[1] * S)), bodym)
HL([(-36, -36), (-50, -70), (-62, -100)], 30)               # neck
HL([(-62, -102), (-80, -96), (-94, -84)], 20)               # head
PG([H(-58, -112), H(-52, -128), H(-50, -108)])              # ear
PG([H(-30, -40), H(-48, -96), H(-40, -92), H(-20, -36)])   # mane
HL([(-44, -24), (-74, -34), (-80, -8)], 11)                 # foreleg 1 (raised)
HL([(-36, -12), (-62, -2), (-70, 20)], 11)                  # foreleg 2
HL([(36, 30), (30, 74), (42, 108)], 14)                     # hind leg 1
HL([(50, 22), (58, 70), (50, 106)], 13)                     # hind leg 2
HL([(56, 22), (88, 30), (96, 64), (84, 86)], 8)             # tail
# rider
HL([(-4, -28), (0, -80)], 26)                               # torso
E_(*H(4, -98), 12 * hs, 13 * hs)                            # head
PG([H(-10, -104), H(18, -106), H(14, -122), H(-4, -124), H(-12, -114)])   # pagdi
HL([(12, -120), (24, -134), (20, -148)], 3)                 # kalgi
HL([(-4, -30), (-14, 0), (-22, 8)], 11)                     # leg
HL([(6, -70), (24, -90), (30, -108)], 8)                    # arm raised
HL([(30, -80), (40, -165)], 4)                              # flag pole
PG([H(40, -165), H(90, -153), H(74, -141), H(94, -125), H(38, -127)])    # flag
HL([(-8, -66), (-30, -60), (-44, -74)], 8)                  # arm with sword
HL([(-44, -74), (-66, -118)], 4)                            # sword
sil = ImageChops.multiply(sil, hero)
shadow_m = sil.filter(ImageFilter.GaussianBlur(8 * S)).point(lambda v: int(v * 0.25))
img.paste(Image.new('RGB', img.size, (120, 80, 0)), (0, int(6 * S)), shadow_m)
grad_mask_fill(img, sil, INK[0], INK[1], sheen=0.0)
# gold rim on the hill top
rim = Image.new('L', img.size, 0)
ImageDraw.Draw(rim).line(P(*(bez((HX0, 470), (420, 360), (700, 430), 30) + bez((700, 430), (900, 470), (HX1, 440), 20))), fill=255, width=int(4 * S))
img.paste(Image.new('RGB', img.size, (234, 179, 8)), (0, 0), ImageChops.multiply(rim, hero))
rrect(img, (HX0, HY0, HX1, HY1), 36, outline=YEL, width=3)
# titles inside hero (bottom over hill)
GT2(img, (540, 455), 'Shivaji Jayanti', F2('GreatVibes-Regular.ttf', 74), (254, 240, 138), (234, 179, 8), shadow_=(DEEP, 0.5))
for sg in (-1, 1):  # crossed swords hint
    ImageDraw.Draw(img).arc(P((540 + sg * 230 - 40, 470), (540 + sg * 230 + 40, 520)), 200 if sg < 0 else 250, 290 if sg < 0 else 340, fill=(254, 240, 138), width=int(5 * S))

# Hindi title + English line
s = fit('छत्रपति शिवाजी महाराज जयंती', 58, PB, 980)
grad_text(img, (540, 572), 'छत्रपति शिवाजी महाराज जयंती', s, (21, 128, 61), (6, 52, 28), PB, 'mm', shadow=(GOLD, 0.22), gloss=False)
l2 = 'Jai Bhavani, Jai Shivaji!  •  स्वराज्य के प्रेरणास्रोत को नमन'
w = tw(l2, 25, PB)
grrect(img, (540 - w / 2 - 22, 610, 540 + w / 2 + 22, 652), 21, (52, 211, 110), (21, 128, 61), 0.35)
text(img, (540, 631), l2, 25, WHITE, PB, 'mm')

# ================= MIDDLE: phone with customers ring (left) + where-to-use grid (right) =================
top = 676
GT2(img, (M + 236, top + 26), 'Send Bulk WhatsApp', F2('Montserrat[wght].ttf', 30), (21, 128, 61), (6, 52, 28))
text(img, (M + 236, top + 64), 'एक क्लिक में हज़ारों ग्राहकों तक', 23, DEEP, PB, 'mm')
# ring + avatars
cx, cy, rr = M + 236, top + 270, 180
dashed(img, [(cx + rr * math.cos(a / 40 * 2 * math.pi), cy + rr * math.sin(a / 40 * 2 * math.pi)) for a in range(41)], (134, 199, 157), w=3, dash=8, gap=8)
pals = [((254, 240, 138), (234, 179, 8)), ((187, 247, 208), (34, 160, 80)), ((255, 228, 200), (230, 160, 110)), ((209, 250, 223), (21, 128, 61))]
skins = [(241, 194, 150), (224, 172, 130), (198, 140, 100), (232, 185, 140)]
for i, a in enumerate([145, 180, 215, 325, 0, 35]):
    ax, ay = cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a))
    gellipse(img, ax, ay, 34, 34, *pals[i % 4], 0.3)
    m = Image.new('L', img.size, 0); dd = ImageDraw.Draw(m)
    dd.ellipse(P((ax - 34, ay - 34), (ax + 34, ay + 34)), fill=255)
    sh = Image.new('L', img.size, 0); ds = ImageDraw.Draw(sh)
    ds.ellipse(P((ax - 12, ay - 22), (ax + 12, ay + 4)), fill=255); ds.chord(P((ax - 24, ay + 4), (ax + 24, ay + 50)), 180, 360, fill=255)
    img.paste(Image.new('RGB', img.size, skins[i % 4]), (0, 0), ImageChops.multiply(sh, m))
    hb = Image.new('L', img.size, 0); ImageDraw.Draw(hb).chord(P((ax - 13, ay - 24), (ax + 13, ay - 4)), 180, 360, fill=255)
    img.paste(Image.new('RGB', img.size, (40, 32, 28)), (0, 0), ImageChops.multiply(hb, m))
    ImageDraw.Draw(img).ellipse(P((ax - 34, ay - 34), (ax + 34, ay + 34)), outline=WHITE, width=int(4 * S))
    check(img, ax + 24, ay + 24, 10, GREEN, WHITE)
# phone
px0, py0, pw, ph = cx - 92, top + 100, 184, 340
shadow(img, (px0, py0, px0 + pw, py0 + ph), 26, blur=16, alpha=0.3, off=10, color=DEEP)
grrect(img, (px0, py0, px0 + pw, py0 + ph), 26, (50, 60, 55), (10, 18, 13), 0.15)
sx0, sy0, sx1, sy1 = px0 + 8, py0 + 8, px0 + pw - 8, py0 + ph - 8
grrect(img, (sx0, sy0, sx1, sy1), 20, (240, 250, 244), (225, 240, 232), 0)
grrect(img, (sx0, sy0, sx1, sy0 + 36), 20, (37, 160, 100), (21, 110, 70), 0); ImageDraw.Draw(img).rectangle(P((sx0, sy0 + 20), (sx1, sy0 + 36)), fill=(21, 110, 70))
text(img, (sx0 + 14, sy0 + 22), 'Your Shop', 13, WHITE, PB, 'lm')
grrect(img, (sx0 + 8, sy0 + 46, sx1 - 8, sy0 + 156), 10, (254, 240, 138), (234, 150, 8), 0.4)
text(img, (sx0 + 84, sy0 + 82), 'FESTIVE', 18, DEEP, PB, 'mm'); text(img, (sx0 + 84, sy0 + 110), 'OFFER', 26, DEEP, PB, 'mm')
sparkle(img, sx0 + 30, sy0 + 62, 9, WHITE); sparkle(img, sx1 - 26, sy0 + 140, 8, WHITE)
for k, t in enumerate(['नमस्ते {{नाम}} जी!', 'त्योहार का ख़ास ऑफर', 'आज ही आइए 🙏'[:-2]]):
    text(img, (sx0 + 12, sy0 + 176 + k * 20), t, 12, (30, 50, 38), PBD, 'lm')
for k, t in enumerate(['Shop Now', 'Call']):
    yy = sy0 + 240 + k * 34
    rrect(img, (sx0 + 8, yy, sx1 - 8, yy + 28), 8, fill=WHITE, outline=(187, 247, 208), width=2)
    text(img, ((sx0 + sx1) / 2, yy + 14), t, 14, (21, 110, 70), PB, 'mm')
ICONS['wa'](img, sx1 - 4, sy0 - 4, WHITE, YEL, (37, 160, 100)) if False else None

# right: where to use
X0, X1 = 520, 1080 - M
GT2(img, ((X0 + X1) / 2, top + 26), 'Where can you use it?', F2('PlayfairDisplay[wght].ttf', 30), (21, 128, 61), (6, 52, 28))
text(img, ((X0 + X1) / 2, top + 64), 'कहाँ काम आएगा?', 23, DEEP, PB, 'mm')
uses = [('send', 'Marketing', 'मार्केटिंग कैंपेन'), ('store', 'Real Estate', 'प्रॉपर्टी की सूचना'),
        ('heart', 'Wedding', 'शादी का निमंत्रण'), ('photo', 'Products', 'प्रोडक्ट का प्रचार'),
        ('book', 'Reminders', 'अपॉइंटमेंट रिमाइंडर'), ('star', 'Festive', 'त्योहार की शुभकामनाएँ')]
cw, chh, g = (X1 - X0 - 16) / 2, 106, 12
for i, (ic, en, hi) in enumerate(uses):
    x = X0 + (i % 2) * (cw + 16); y = top + 96 + (i // 2) * (chh + g)
    shadow(img, (x, y, x + cw, y + chh), 20, blur=10, alpha=0.12, off=5, color=DEEP)
    grrect(img, (x, y, x + cw, y + chh), 20, (255, 255, 255), (240, 253, 244), 0)
    rrect(img, (x, y, x + cw, y + chh), 20, outline=(187, 247, 208), width=2)
    gloss.node(img, x + 46, y + chh / 2, 32, ic)
    text(img, (x + 90, y + chh / 2 - 15), en, fit(en, 24, PB, cw - 100), DEEP, PB, 'lm')
    text(img, (x + 90, y + chh / 2 + 17), hi, fit(hi, 18, PBD, cw - 100), SUBC, PBD, 'lm')

# strip
ys = 1132
shadow(img, (M, ys, 1080 - M, ys + 64), 22, blur=12, alpha=0.15, off=6, color=GOLD)
grrect(img, (M, ys, 1080 - M, ys + 64), 22, (255, 251, 225), (254, 240, 138), 0.3)
rrect(img, (M, ys, 1080 - M, ys + 64), 22, outline=YEL, width=3)
rich2(img, 540, ys + 32, segs_fit([('Smart strategy, like a true leader —', 23, DEEP, PB), ('@ST', 26), ('WhatsApp CRM', 23, (21, 128, 61), PB)], 950))

gloss.cta(img, 'Bulk WhatsApp शुरू करें — Call / WhatsApp करें')
build2.header(img)
finish3(img, '/home/claude/posters/series/out2/12-2027-02-19-shivaji-jayanti-v3.jpg', 'Shivaji Maharaj Jayanti 2027 - Shri Tech')
