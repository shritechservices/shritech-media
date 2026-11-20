"""Post 17 (Good Friday) redo: same top; quote box replaced by two step flows - Bulk WhatsApp + Live chat."""
import sys
sys.path.insert(0, '/home/claude/posters/series')
import gloss, build2
from art2 import *
from gloss import grrect, gellipse
from kit import rich2, segs_fit

SUBC = (40, 62, 48)
LC = (134, 199, 157)
img = gloss.base()
gloss.glossy_art(img, ART['goodfriday'])
gloss.greeting(img, 'गुड फ्राइडे', 'प्रेम, क्षमा और त्याग का संदेश')
gloss.story_pill(img, 'शांति और करुणा के साथ — हर ग्राहक से अपनापन')

def panel(x0, x1, y0, y1, head, sub, steps, dark_head):
    shadow(img, (x0, y0, x1, y1), 28, blur=14, alpha=0.16, off=8, color=DEEP)
    grrect(img, (x0, y0, x1, y1), 28, (255, 255, 255), (240, 253, 244), 0.0)
    rrect(img, (x0, y0, x1, y1), 28, outline=(187, 247, 208), width=3)
    # head bar
    hb = (x0 + 14, y0 + 14, x1 - 14, y0 + 82)
    if dark_head: grrect(img, hb, 22, (22, 110, 56), (6, 46, 25), 0.3)
    else: grrect(img, hb, 22, (254, 243, 160), (250, 204, 21), 0.35)
    cx = (x0 + x1) / 2
    text(img, (cx, y0 + 38), head, fit(head, 27, PB, x1 - x0 - 50), (254, 240, 138) if dark_head else DEEP, PB, 'mm')
    text(img, (cx, y0 + 66), sub, fit(sub, 17, PBD, x1 - x0 - 50), WHITE if dark_head else (21, 110, 52), PBD, 'mm')
    # vertical steps
    n = len(steps); top = y0 + 134; gap = (y1 - 50 - top) / (n - 1)
    nx = x0 + 66
    for i in range(n - 1):
        ya, yb = top + i * gap + 36, top + (i + 1) * gap - 36
        dashed(img, [(nx, ya), (nx, yb)], LC, w=4, dash=10, gap=7)
        my = (ya + yb) / 2
        ImageDraw.Draw(img).polygon(P((nx - 8, my - 5), (nx + 8, my - 5), (nx, my + 7)), fill=GREEN)
    for i, (ic, a, b) in enumerate(steps):
        y = top + i * gap
        gloss.node(img, nx, y, 33, ic, num=i + 1)
        tx = nx + 56; mw = x1 - tx - 22
        text(img, (tx, y - 14), a, fit(a, 24, PB, mw), DEEP, PB, 'lm')
        text(img, (tx, y + 18), b, fit(b, 18, PBD, mw), SUBC, PBD, 'lm')

y0, y1 = 664, 1108
mid = 540
panel(M, mid - 12, y0, y1, 'WhatsApp बल्क मैसेज', 'एक साथ सभी ग्राहकों तक', [
    ('sheet', 'कॉन्टैक्ट जोड़ें', 'Excel से एक साथ'),
    ('tmpl', 'मैसेज तैयार', 'Meta से मंज़ूर टेम्पलेट'),
    ('send', 'एक क्लिक में भेजें', 'सबको या चुने ग्रुप को'),
    ('eye', 'रिपोर्ट देखें', 'पहुँचा, पढ़ा — सब दिखे')], True)
panel(mid + 12, 1080 - M, y0, y1, 'ग्राहक से लाइव चैट', 'जवाब वहीं, उसी ऐप में', [
    ('chat', 'ग्राहक का जवाब आए', 'सीधे आपके चैट में'),
    ('bell', 'तुरंत सूचना', 'नया मैसेज, तुरंत पता'),
    ('heart', 'प्यार से जवाब दें', 'मोबाइल से ही'),
    ('check', 'ऑर्डर / बुकिंग पक्का', 'भरोसेमंद ग्राहक')], False)

# strip
ys = 1128
shadow(img, (M, ys, 1080 - M, ys + 68), 22, blur=12, alpha=0.15, off=6, color=GOLD)
grrect(img, (M, ys, 1080 - M, ys + 68), 22, (255, 251, 225), (254, 240, 138), 0.3)
rrect(img, (M, ys, 1080 - M, ys + 68), 22, outline=YEL, width=3)
rich2(img, 540, ys + 34, segs_fit([('@ST', 26), ('के साथ: मैसेज भेजें और जवाब दें —', 24, DEEP, PB), ('सब एक ही जगह', 24, (21, 128, 61), PB)], 940))

gloss.cta(img, 'अपने ग्राहकों से अपनापन बढ़ाएँ — कॉल / WhatsApp करें')
build2.header(img)
finish3(img, '/home/claude/posters/series/out2/17-2027-03-26-good-friday-v2.jpg', 'Good Friday 2027 - Shri Tech')
