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

# ================= TOP: owner-supplied Shivaji Jayanti artwork (black recoloured to brand deep green) =================
import numpy as np
src = Image.open('/mnt/user-data/uploads/a0642ef1-image.jpg').convert('RGB')
art = src.crop((0, 52, src.width, 608))                    # artwork + calligraphy, English paragraph removed
arr = np.asarray(art).astype(np.float32)
lum = arr.mean(axis=2, keepdims=True)
k = np.clip((110 - lum) / 110, 0, 1)                        # dark pixels -> deep green
arr = arr * (1 - k) + np.array([10, 62, 34], np.float32) * k
art = Image.fromarray(arr.astype(np.uint8))
bgc = tuple(int(v) for v in np.asarray(src)[8:40, 8:40].reshape(-1, 3).mean(axis=0))
CX0, CY0, CX1, CY1 = M, 108, 1080 - M, 662
card = Image.new('L', img.size, 0); ImageDraw.Draw(card).rounded_rectangle(P((CX0, CY0), (CX1, CY1)), 36 * S, fill=255)
shadow(img, (CX0, CY0, CX1, CY1), 36, blur=16, alpha=0.2, off=8, color=GOLD)
img.paste(Image.new('RGB', img.size, bgc), (0, 0), card)
h = CY1 - CY0 - 8
sc = h / art.height
a2 = art.resize((int(art.width * sc * S), int(h * S)), Image.LANCZOS)
fm = Image.new('L', a2.size, 255)
fw = int(60 * S)
for i in range(fw):
    v = int(255 * i / fw)
    ImageDraw.Draw(fm).line([(i, 0), (i, a2.height)], fill=v); ImageDraw.Draw(fm).line([(a2.width - 1 - i, 0), (a2.width - 1 - i, a2.height)], fill=v)
img.paste(a2, (int((540 - art.width * sc / 2) * S), int((CY0 + 4) * S)), fm)
rrect(img, (CX0, CY0, CX1, CY1), 36, outline=YEL, width=3)

# ================= MIDDLE: phone with customers ring (left) + where-to-use grid (right) =================
top = 686
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
finish3(img, '/home/claude/posters/series/out2/12-2027-02-19-shivaji-jayanti-v4.jpg', 'Shivaji Maharaj Jayanti 2027 - Shri Tech')
