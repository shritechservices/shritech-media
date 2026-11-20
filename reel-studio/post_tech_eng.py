"""English posts: #22 National Technology Day (tech hub + design package) and #35 Engineers' Day (engineer hub)."""
import sys, math
sys.path.insert(0, '/home/claude/posters/series')
import gloss, build2
from art2 import *
from gloss import grrect, gellipse
from kit import rich2, segs_fit

SUBC = (40, 62, 48)
LC = (134, 199, 157)
OUT = '/home/claude/posters/series/out2/'

def sat_pill(cx, cy, ic, t1, t2, w=222, h=72):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    shadow(img, (x0, y0, x1, y1), h / 2, blur=10, alpha=0.18, off=5, color=DEEP)
    grrect(img, (x0, y0, x1, y1), h / 2, (255, 255, 255), (236, 252, 243), 0.25)
    rrect(img, (x0, y0, x1, y1), h / 2, outline=(134, 239, 172), width=3)
    gloss.node(img, x0 + 38, cy, 30, ic)
    tx = x0 + 78; mw = x1 - tx - 14
    text(img, (tx, cy - 12), t1, fit(t1, 20, PB, mw), DEEP, PB, 'lm')
    text(img, (tx, cy + 15), t2, fit(t2, 14, PBD, mw), SUBC, PBD, 'lm')

def hub(cx, cy, rx, ry, items, centre_fn):
    n = len(items)
    angs = [-90 + i * 360 / n for i in range(n)]
    pos = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in angs]
    # orbit + spokes
    pts = [(cx + (rx - 20) * math.cos(t / 60 * 2 * math.pi), cy + (ry - 12) * math.sin(t / 60 * 2 * math.pi)) for t in range(61)]
    dashed(img, pts, LC, w=3, dash=10, gap=8)
    d = ImageDraw.Draw(img)
    for (x, y) in pos:
        a = math.atan2(y - cy, x - cx)
        sx, sy = cx + 112 * math.cos(a), cy + 112 * math.sin(a)
        ex, ey = x - 64 * math.cos(a) * (rx / max(rx, 1)), y - 42 * math.sin(a)
        d.line(P((sx, sy), (ex, ey)), fill=GREEN, width=4 * S)
        d.polygon(P((ex, ey), (ex - 16 * math.cos(a - 0.45), ey - 16 * math.sin(a - 0.45)), (ex - 16 * math.cos(a + 0.45), ey - 16 * math.sin(a + 0.45))), fill=GREEN)
    centre_fn(cx, cy)
    for (x, y), it in zip(pos, items):
        sat_pill(x, y, *it)

def centre_tech(cx, cy):
    glow(img, cx, cy, 170, (250, 204, 21), 0.35)
    r = 104
    shadow(img, (cx - r, cy - r, cx + r, cy + r), r, blur=16, alpha=0.3, off=8, color=DEEP)
    gellipse(img, cx, cy, r, r, (52, 211, 110), (6, 78, 40), 0.35)
    gellipse(img, cx, cy, r - 10, r - 10, (22, 128, 61), (6, 52, 28), 0.3)
    # chip icon
    d = ImageDraw.Draw(img)
    cw = 54
    for k in range(-2, 3):
        for (ax, ay, bx, by) in [(cx + k * 18, cy - cw - 6, cx + k * 18, cy - cw - 22), (cx + k * 18, cy - cw + 2 * cw + 6, cx + k * 18, cy + cw + 22),
                                 (cx - cw - 6, cy + k * 18, cx - cw - 22, cy + k * 18), (cx + cw + 6, cy + k * 18, cx + cw + 22, cy + k * 18)]:
            d.line(P((ax, ay - 34), (bx, by - 34)) if False else P((ax, ay), (bx, by)), fill=(254, 240, 138), width=4 * S)
    grrect(img, (cx - cw, cy - cw, cx + cw, cy + cw), 12, (254, 240, 138), (217, 150, 6), 0.4)
    text(img, (cx, cy - 12), 'TECH', 26, DEEP, PB, 'mm')
    text(img, (cx, cy + 16), 'for you', 15, DEEP, PBD, 'mm')

def centre_engineer(cx, cy):
    glow(img, cx, cy, 170, (250, 204, 21), 0.35)
    r = 104
    shadow(img, (cx - r, cy - r, cx + r, cy + r), r, blur=16, alpha=0.3, off=8, color=DEEP)
    gellipse(img, cx, cy, r, r, (52, 211, 110), (6, 78, 40), 0.35)
    gellipse(img, cx, cy, r - 10, r - 10, (240, 253, 244), (209, 250, 223), 0.2)
    d = ImageDraw.Draw(img)
    # gear behind
    gx, gy, gr = cx - 58, cy - 46, 20
    for k in range(8):
        a = k * math.pi / 4
        d.rectangle(P((gx + (gr + 2) * math.cos(a) - 6, gy + (gr + 2) * math.sin(a) - 6), (gx + (gr + 2) * math.cos(a) + 6, gy + (gr + 2) * math.sin(a) + 6)), fill=(134, 199, 157))
    d.ellipse(P((gx - gr, gy - gr), (gx + gr, gy + gr)), fill=(134, 199, 157)); d.ellipse(P((gx - 9, gy - 9), (gx + 9, gy + 9)), fill=(240, 253, 244))
    # body (shirt) clipped to circle
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.ellipse(P((cx - r + 10, cy - r + 10), (cx + r - 10, cy + r - 10)), fill=255)
    body = Image.new('L', img.size, 0); ImageDraw.Draw(body).rounded_rectangle(P((cx - 62, cy + 38), (cx + 62, cy + 140)), 40 * S, fill=255)
    body = Image.fromarray(np.minimum(np.array(body), np.array(m)))
    grad_mask_fill(img, body, (34, 197, 94), (21, 110, 52), sheen=0.2)
    d.polygon(P((cx - 20, cy + 38), (cx, cy + 66), (cx + 20, cy + 38)), fill=WHITE)              # collar
    d.rectangle(P((cx - 44, cy + 56), (cx - 36, cy + 100)), fill=(254, 240, 138))                 # vest stripes
    d.rectangle(P((cx + 36, cy + 56), (cx + 44, cy + 100)), fill=(254, 240, 138))
    # neck + face
    d.rectangle(P((cx - 12, cy + 22), (cx + 12, cy + 42)), fill=(232, 190, 150))
    d.ellipse(P((cx - 34, cy - 30), (cx + 34, cy + 38)), fill=(244, 205, 165))
    d.ellipse(P((cx - 15, cy + 2), (cx - 7, cy + 10)), fill=DEEP); d.ellipse(P((cx + 7, cy + 2), (cx + 15, cy + 10)), fill=DEEP)
    d.arc(P((cx - 12, cy + 10), (cx + 12, cy + 26)), 20, 160, fill=DEEP, width=3 * S)
    # hard hat
    hat = Image.new('L', img.size, 0); hd = ImageDraw.Draw(hat)
    hd.pieslice(P((cx - 40, cy - 52), (cx + 40, cy + 18)), 180, 360, fill=255)
    hd.rounded_rectangle(P((cx - 50, cy - 20), (cx + 50, cy - 8)), 6 * S, fill=255)
    grad_mask_fill(img, hat, (254, 240, 138), (217, 150, 6), sheen=0.45)
    d.rectangle(P((cx - 5, cy - 52), (cx + 5, cy - 20)), fill=(234, 170, 8))

def package_card(y):
    x0, x1 = M, 1080 - M
    shadow(img, (x0, y, x1, y + 108), 24, blur=12, alpha=0.18, off=6, color=GOLD)
    grrect(img, (x0, y, x1, y + 108), 24, (255, 251, 225), (254, 240, 138), 0.3)
    rrect(img, (x0, y, x1, y + 108), 24, outline=YEL, width=3)
    # left badge
    bx0, bx1 = x0 + 14, x0 + 250
    grrect(img, (bx0, y + 12, bx1, y + 96), 18, (22, 128, 61), (6, 46, 25), 0.3)
    grad_text(img, ((bx0 + bx1) / 2, y + 44), '150', 44, (254, 240, 138), (234, 179, 8), PB, 'mm', gloss=True)
    text(img, ((bx0 + bx1) / 2, y + 78), 'DESIGNS / YEAR', 17, WHITE, PB, 'mm')
    tx = bx1 + 24; mw = x1 - tx - 20
    text(img, (tx, y + 30), 'Graphic Design Package', fit('Graphic Design Package', 28, PB, mw), DEEP, PB, 'lm')
    l2 = 'Designed with your brand  •  Scheduled  •  Posted for you'
    text(img, (tx, y + 66), l2, fit(l2, 19, PBD, mw), (21, 110, 52), PBD, 'lm')
    l3 = 'Facebook + Instagram  •  Logo & brand colours on every post'
    text(img, (tx, y + 92), l3, fit(l3, 16, PM, mw), SUBC, PM, 'lm')

def strip(y, segs):
    shadow(img, (M, y, 1080 - M, y + 68), 22, blur=12, alpha=0.15, off=6, color=GOLD)
    grrect(img, (M, y, 1080 - M, y + 68), 22, (255, 251, 225), (254, 240, 138), 0.3)
    rrect(img, (M, y, 1080 - M, y + 68), 22, outline=YEL, width=3)
    rich2(img, 540, y + 34, segs_fit(segs, 940))

# ---------------- #22 National Technology Day ----------------
img = gloss.base()
gloss.glossy_art(img, ART['tech'])
gloss.greeting(img, 'National Technology Day', 'Celebrating Innovation & Progress')
gloss.story_pill(img, 'How technology grows your business — all in one place')
hub(540, 860, 362, 166, [
    ('users', 'Customer CRM', 'All contacts, one list'),
    ('send', 'Bulk WhatsApp', 'Offers to all in 1 click'),
    ('soc', '1-Click Posting', 'Facebook + Instagram'),
    ('chat', 'Live Chat', 'Reply customers instantly'),
    ('clock', 'Smart Scheduling', 'Right time, every time'),
    ('chart', 'Reports', 'Sent, delivered, read'),
    ('lang', 'Multi-language', 'Hindi, English & more'),
    ('photo', 'Branding Videos', 'Reels for your brand'),
    ('palette', 'Branding Posts', 'Your logo & colours'),
], centre_tech)
package_card(1078)
gloss.cta(img, 'Take your business digital — Call / WhatsApp')
build2.header(img)
p1 = OUT + '22-2027-05-11-national-technology-day-en.jpg'
finish3(img, p1, 'National Technology Day 2027 - Shri Tech')

# ---------------- #35 Engineers' Day ----------------
img = gloss.base()
gloss.glossy_art(img, ART['engineers'])
gloss.greeting(img, "Engineers' Day", 'Tribute to Sir M. Visvesvaraya')
gloss.story_pill(img, 'Strong foundation, strong business — engineered by Shri Tech')
hub(540, 868, 362, 172, [
    ('sheet', 'Excel Import', 'Add contacts in bulk'),
    ('users', 'Groups & Tags', 'Right offer, right people'),
    ('tmpl', 'Approved Templates', 'Meta-approved messages'),
    ('eye', 'Read Tracking', 'See who read your offer'),
    ('shield', 'Safe Messaging', 'Auto opt-out on STOP'),
    ('bell', 'Reminders', 'Follow-ups on time'),
    ('check', 'Your Approval', 'Nothing posts without you'),
    ('store', 'Brand Kit', 'Logo, colours, details'),
    ('grow', 'Growth Dashboard', 'Track every campaign'),
], centre_engineer)
strip(1122, [('Engineered for your business:', 25, DEEP, PB), ('Set up once, grow every day', 25, (21, 128, 61), PB)])
gloss.cta(img, 'Build your digital system — Call / WhatsApp')
build2.header(img)
p2 = OUT + '35-2027-09-15-engineers-day-en.jpg'
finish3(img, p2, "Engineers' Day 2027 - Shri Tech")
print(p1, p2)
