"""General Bulk WhatsApp post (no festival): hero phone with customers ring + where-to-use grid. Hindi + English. Light theme."""
import sys
sys.path.insert(0, '/home/claude/posters/series')
import gloss, build2
from art2 import *
from gloss import grrect, gellipse, gshape, grad_mask_fill
from kit import rich2, segs_fit

FD = '/home/claude/fonts2/'
def F2(name, size, var=None):
    f = ImageFont.truetype(FD + name, int(size * S), layout_engine=ImageFont.Layout.RAQM)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f
def GT2(img, xy, txt, font, c1, c2, anchor='mm'):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).text((xy[0] * S, xy[1] * S), txt, font=font, fill=255, anchor=anchor)
    img.paste(Image.new('RGB', img.size, GOLD), (0, int(4 * S)), m.filter(ImageFilter.GaussianBlur(5 * S)).point(lambda v: int(v * 0.22)))
    grad_mask_fill(img, m, c1, c2, sheen=0.0)
def flen(txt, font): return font.getlength(txt) / S

SUBC = (40, 62, 48)
img = gloss.base()

# ---- headline ----
fm = F2('Montserrat[wght].ttf', 58, b'ExtraBold')
w1, wb = flen('Send ', fm), flen('Bulk', fm)
x = 540 - (w1 + wb + 24) / 2
GT2(img, (x, 160), 'Send', fm, (21, 128, 61), (6, 52, 28), 'lm')
bx = x + w1
grrect(img, (bx - 6, 122, bx + wb + 18, 198), 18, (254, 240, 138), (234, 179, 8), 0.35)
ImageDraw.Draw(img).text(((bx + 6) * S, 160 * S), 'Bulk', font=fm, fill=DEEP, anchor='lm')
GT2(img, (540, 236), 'WhatsApp Messages Easily!', F2('Montserrat[wght].ttf', 50, b'ExtraBold'), (21, 128, 61), (6, 52, 28))
l2 = 'एक क्लिक में हज़ारों ग्राहकों तक आपका ऑफर'
w = tw(l2, 28, PB)
grrect(img, (540 - w / 2 - 24, 278, 540 + w / 2 + 24, 326), 24, (52, 211, 110), (21, 128, 61), 0.35)
text(img, (540, 302), l2, 28, WHITE, PB, 'mm')

# ---- hero: ring of customers + phone ----
cx, cy, rr = 540, 560, 250
dashed(img, [(cx + 360 * math.cos(a / 60 * 2 * math.pi), cy + 200 * math.sin(a / 60 * 2 * math.pi)) for a in range(61)], (134, 199, 157), w=3, dash=9, gap=8)
pals = [((254, 240, 138), (234, 179, 8)), ((187, 247, 208), (34, 160, 80)), ((255, 228, 200), (230, 160, 110)), ((209, 250, 223), (21, 128, 61))]
skins = [(241, 194, 150), (224, 172, 130), (198, 140, 100), (232, 185, 140)]
hair = [(40, 32, 28), (60, 40, 30), (30, 24, 22), (70, 50, 35)]
def avatar(ax, ay, i, r=44, fem=False):
    gellipse(img, ax, ay, r, r, *pals[i % 4], 0.3)
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse(P((ax - r, ay - r), (ax + r, ay + r)), fill=255)
    if fem:
        hb = Image.new('L', img.size, 0); ImageDraw.Draw(hb).rounded_rectangle(P((ax - r * .45, ay - r * .7), (ax + r * .45, ay + r * .45)), int(r * .4 * S), fill=255)
        img.paste(Image.new('RGB', img.size, hair[i % 4]), (0, 0), ImageChops.multiply(hb, m))
    sh = Image.new('L', img.size, 0); ds = ImageDraw.Draw(sh)
    ds.ellipse(P((ax - r * .34, ay - r * .62), (ax + r * .34, ay + r * .12)), fill=255)
    ds.chord(P((ax - r * .72, ay + r * .12), (ax + r * .72, ay + r * 1.45)), 180, 360, fill=255)
    img.paste(Image.new('RGB', img.size, skins[i % 4]), (0, 0), ImageChops.multiply(sh, m))
    hb = Image.new('L', img.size, 0); ImageDraw.Draw(hb).chord(P((ax - r * .37, ay - r * .68), (ax + r * .37, ay - r * .12)), 180, 360, fill=255)
    img.paste(Image.new('RGB', img.size, hair[i % 4]), (0, 0), ImageChops.multiply(hb, m))
    shirt = Image.new('L', img.size, 0); ImageDraw.Draw(shirt).chord(P((ax - r * .72, ay + r * .4), (ax + r * .72, ay + r * 1.6)), 180, 360, fill=255)
    gc = [((74, 222, 128), (21, 101, 52)), ((254, 240, 138), (217, 159, 6)), ((255, 255, 255), (210, 225, 218)), ((52, 160, 90), (6, 46, 25))][(i + 1) % 4]
    grad_mask_fill(img, ImageChops.multiply(shirt, m), gc[0], gc[1], sheen=0.2)
    ImageDraw.Draw(img).ellipse(P((ax - r, ay - r), (ax + r, ay + r)), outline=WHITE, width=int(5 * S))
    check(img, ax + r * .72, ay + r * .72, 12, GREEN, WHITE)
for i, a in enumerate([145, 180, 215, 325, 0, 35]):
    ax, ay = cx + 360 * math.cos(math.radians(a)), cy + 200 * math.sin(math.radians(a))
    avatar(ax, ay, i, 52, fem=(i % 2 == 1))
# phone
pw, ph = 250, 440
px0, py0 = cx - pw / 2, cy - ph / 2 + 10
shadow(img, (px0, py0, px0 + pw, py0 + ph), 34, blur=20, alpha=0.32, off=12, color=DEEP)
grrect(img, (px0, py0, px0 + pw, py0 + ph), 34, (50, 60, 55), (10, 18, 13), 0.15)
sx0, sy0, sx1, sy1 = px0 + 10, py0 + 10, px0 + pw - 10, py0 + ph - 10
grrect(img, (sx0, sy0, sx1, sy1), 26, (240, 250, 244), (225, 240, 232), 0)
grrect(img, (sx0, sy0, sx1, sy0 + 48), 26, (37, 160, 100), (21, 110, 70), 0)
ImageDraw.Draw(img).rectangle(P((sx0, sy0 + 26), (sx1, sy0 + 48)), fill=(21, 110, 70))
gellipse(img, sx0 + 26, sy0 + 26, 13, 13, (254, 240, 138), (234, 179, 8), 0.3)
text(img, (sx0 + 48, sy0 + 26), 'Your Business', 16, WHITE, PB, 'lm')
grrect(img, (sx0 + 12, sy0 + 62, sx1 - 12, sy0 + 196), 12, (254, 240, 138), (234, 150, 8), 0.45)
text(img, ((sx0 + sx1) / 2, sy0 + 102), 'FESTIVE', 22, DEEP, PB, 'mm')
text(img, ((sx0 + sx1) / 2, sy0 + 140), 'OFFER', 34, DEEP, PB, 'mm')
text(img, ((sx0 + sx1) / 2, sy0 + 176), 'ख़ास ऑफर', 18, DEEP, PB, 'mm')
sparkle(img, sx0 + 34, sy0 + 82, 10, WHITE); sparkle(img, sx1 - 30, sy0 + 178, 9, WHITE)
for k, t in enumerate(['नमस्ते {{नाम}} जी! 🙏'[:-2], 'आपके लिए त्योहार का', 'ख़ास ऑफर — आज ही आइए']):
    text(img, (sx0 + 16, sy0 + 220 + k * 24), t, 15, (30, 50, 38), PBD, 'lm')
text(img, (sx1 - 14, sy0 + 290), '✓✓', 14, (59, 130, 246), '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'rm')
for k, t in enumerate(['Shop Now', 'Call']):
    yy = sy0 + 310 + k * 44
    rrect(img, (sx0 + 12, yy, sx1 - 12, yy + 36), 10, fill=WHITE, outline=(187, 247, 208), width=2)
    text(img, ((sx0 + sx1) / 2, yy + 18), t, 17, (21, 110, 70), PB, 'mm')
# whatsapp bubble badge
bxc, byc = sx1 + 6, sy0 + 2
gellipse(img, bxc, byc, 38, 38, (80, 230, 140), (21, 140, 70), 0.35)
ImageDraw.Draw(img).ellipse(P((bxc - 38, byc - 38), (bxc + 38, byc + 38)), outline=WHITE, width=int(5 * S))
ImageDraw.Draw(img).ellipse(P((bxc - 20, byc - 20), (bxc + 20, byc + 20)), outline=WHITE, width=int(5 * S))
ImageDraw.Draw(img).polygon(P((bxc - 16, byc + 12), (bxc - 24, byc + 26), (bxc - 6, byc + 18)), fill=WHITE)
ImageDraw.Draw(img).arc(P((bxc - 10, byc - 10), (bxc + 10, byc + 10)), 100, 250, fill=WHITE, width=int(5 * S))
# click arrow
ar = [(300, 330), (380, 392)]
ImageDraw.Draw(img).line(P(*ar), fill=DEEP, width=int(12 * S))
ImageDraw.Draw(img).polygon(P((396, 405), (360, 398), (386, 368)), fill=DEEP)

# ---- where to use ----
top = 830
fp = F2('PlayfairDisplay[wght].ttf', 34, b'Bold'); e1 = 'Where can you use it?  •'; h1 = 'कहाँ काम आएगा?'
tot = flen(e1, fp) + 14 + tw(h1, 32, PB)
GT2(img, (540 - tot / 2, top), e1, fp, (21, 128, 61), (6, 52, 28), 'lm')
grad_text(img, (540 - tot / 2 + flen(e1, fp) + 14, top), h1, 32, (21, 128, 61), (6, 52, 28), PB, 'lm', gloss=False)
uses = [('send', 'Marketing', 'मार्केटिंग कैंपेन'), ('store', 'Real Estate', 'प्रॉपर्टी की सूचना'), ('heart', 'Wedding', 'शादी का निमंत्रण'),
        ('photo', 'Products', 'प्रोडक्ट का प्रचार'), ('book', 'Reminders', 'अपॉइंटमेंट रिमाइंडर'), ('star', 'Festive', 'त्योहार की शुभकामनाएँ')]
g = 14; cw = (1080 - 2 * M - 2 * g) / 3; chh = 104
for i, (ic, en, hi) in enumerate(uses):
    x = M + (i % 3) * (cw + g); y = top + 36 + (i // 3) * (chh + g)
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
rich2(img, 540, ys + 32, segs_fit([('Official WhatsApp API •', 23, DEEP, PB), ('Excel से कॉन्टैक्ट •', 23, DEEP, PB), ('Delivery & Read रिपोर्ट', 23, (21, 128, 61), PB)], 950))

gloss.cta(img, 'Bulk WhatsApp शुरू करें — Call / WhatsApp करें')
build2.header(img)
finish3(img, '/home/claude/posters/series/out2/bulk-whatsapp-general.jpg', 'Bulk WhatsApp - Shri Tech')
