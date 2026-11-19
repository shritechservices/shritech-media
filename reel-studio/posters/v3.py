"""ShriTech poster kit v3: brand-safe (watermark, in-art branding, copyright metadata), rich text with the
English 'Shri Tech' wordmark (Shri dark green + Tech light green), extra icons and diagram types."""
import sys; sys.path.insert(0, '/home/claude/posters')
from v2 import *

TECHG = (34, 197, 94)   # light green for 'Tech'

# ---------- brand ----------
def wordmark_w(size): return tw('Shri', size, PB) + size * 0.22 + tw('Tech', size, PB)

def wordmark(img, x, cy, size, shri=DEEP, tech=TECHG):
    text(img, (x, cy), 'Shri', size, shri, PB, 'lm')
    text(img, (x + tw('Shri', size, PB) + size * 0.22, cy), 'Tech', size, tech, PB, 'lm')

def logo_pill(img, x, y, size=40, align='l'):
    """White pill with S-mark + Shri Tech wordmark (always readable on any background)."""
    r = size * 0.6
    w = 2 * r + size * 0.3 + wordmark_w(size) + size * 0.9
    h = size * 1.55
    if align == 'r': x = x - w
    rrect(img, (x, y, x + w, y + h), h / 2, fill=WHITE, outline=(209, 250, 223), width=2)
    cx, cy = x + size * 0.45 + r, y + h / 2
    grad_box(img, (cx - r, cy - r, cx + r, cy + r), r * 0.42, LGREEN, GREEN)
    text(img, (cx, cy + size * 0.02), 'S', size * 0.92, WHITE, PB, 'mm')
    L(img).ellipse(P((cx + r * 0.55, cy - r * 1.05), (cx + r * 1.0, cy - r * 0.6)), fill=YEL)
    wordmark(img, cx + r + size * 0.3, cy, size)
    return w, h

def num_pill(img, xr, y, dark):
    pw = tw('9993615146', 28, PB) + 92
    fill, c = (YEL, BLACK) if dark else (DEEP, YEL)
    rrect(img, (xr - pw, y, xr, y + 60), 30, fill=fill)
    phone_icon(img, xr - pw + 34, y + 30, 26, c)
    text(img, (xr - pw + 60, y + 30), '9993615146', 28, c, PB, 'lm')

def rich(img, cx, cy, segs, anchor='m'):
    """segs: list of (text, size, color, font) or ('@SHRITECH', size). Drawn on one baseline, centred at cx."""
    parts = []
    for s in segs:
        if s[0] == '@SHRITECH': parts.append(('wm', s[1], wordmark_w(s[1])))
        else: parts.append(('t', s, tw(s[0], s[1], s[3])))
    gap = 10
    total = sum(p[2] for p in parts) + gap * (len(parts) - 1)
    x = cx - total / 2 if anchor == 'm' else cx
    for p in parts:
        if p[0] == 'wm': wordmark(img, x, cy, p[1])
        else: text(img, (x, cy), p[1][0], p[1][1], p[1][2], p[1][3], 'lm')
        x += p[2] + gap

def watermark(img, dark):
    """Faint diagonal brand pattern over the whole image so crops/edits still carry the brand."""
    tile = Image.new('L', (W * 2, H * 2), 0)
    d = ImageDraw.Draw(tile)
    f = F(PB, 24)
    s = 'Shri Tech  •  9993615146'
    for j, y in enumerate(range(0, H * 2, int(190 * S))):
        off = (j % 2) * 230 * S
        for x in range(-int(400 * S), W * 2, int(470 * S)):
            d.text((x + off, y), s, font=f, fill=255)
    tile = tile.rotate(28, resample=Image.BICUBIC).crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
    a = tile.point(lambda v: int(v * (0.065 if dark else 0.07)))
    img.paste(Image.new('RGB', img.size, WHITE if dark else DEEP), (0, 0), a)

def finish3(img, path, title):
    out = img.resize((W // S, H // S), Image.LANCZOS)
    ex = Image.Exif()
    ex[0x8298] = '(c) 2026 Shri Tech - Shri Balaji Digital Services, 9993615146. All rights reserved.'
    ex[0x013B] = 'Shri Tech (Shri Balaji Digital Services)'
    ex[0x010E] = title
    out.save(path, quality=95, subsampling=0, exif=ex.tobytes())
    return out

# ---------- extra line icons ----------
def ic_sheet(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 30, cy - 34), (cx + 30, cy + 34)), 8 * S, fill=bg, outline=c, width=5 * S)
    for yy in (cy - 12, cy + 8):
        d.line(P((cx - 30, yy), (cx + 30, yy)), fill=c, width=3 * S)
    d.line(P((cx - 6, cy - 34), (cx - 6, cy + 34)), fill=c, width=3 * S)
    d.rectangle(P((cx - 28, cy - 32), (cx + 28, cy - 13)), fill=hi)

def ic_template(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 34, cy - 28), (cx + 30, cy + 18)), 12 * S, fill=bg, outline=c, width=5 * S)
    d.polygon(P((cx - 18, cy + 16), (cx - 26, cy + 34), (cx - 2, cy + 16)), fill=c)
    for i, yy in enumerate((cy - 12, cy + 2)):
        d.line(P((cx - 20, yy), (cx + (14 if i else 16), yy)), fill=c, width=4 * S)
    d.ellipse(P((cx + 14, cy + 4), (cx + 42, cy + 32)), fill=hi)
    d.line(P((cx + 21, cy + 18), (cx + 26, cy + 24), (cx + 35, cy + 12)), fill=DEEP, width=4 * S)

def ic_send(img, cx, cy, c, hi, bg):
    d = L(img)
    d.polygon(P((cx - 34, cy - 4), (cx + 34, cy - 30), (cx + 10, cy + 32), (cx - 2, cy + 6)), outline=c, fill=bg)
    d.line(P((cx - 34, cy - 4), (cx + 34, cy - 30), (cx + 10, cy + 32), (cx - 2, cy + 6), (cx - 34, cy - 4)), fill=c, width=5 * S, joint='curve')
    d.line(P((cx - 2, cy + 6), (cx + 34, cy - 30)), fill=c, width=4 * S)
    for k in range(3):
        d.line(P((cx - 40, cy + 14 + k * 9), (cx - 24 + k * 4, cy + 14 + k * 9)), fill=hi, width=4 * S)

def ic_chart(img, cx, cy, c, hi, bg):
    d = L(img)
    d.line(P((cx - 34, cy - 32), (cx - 34, cy + 30), (cx + 36, cy + 30)), fill=c, width=5 * S)
    for i, hh in enumerate((22, 38, 30, 52)):
        x = cx - 24 + i * 15
        d.rounded_rectangle(P((x, cy + 24 - hh), (x + 10, cy + 24)), 3 * S, fill=hi if i == 3 else c)

def ic_menu(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 28, cy - 36), (cx + 28, cy + 36)), 8 * S, fill=bg, outline=c, width=5 * S)
    sparkle(img, cx, cy - 16, 10, hi)
    for i, yy in enumerate((cy + 4, cy + 16)):
        d.line(P((cx - 16, yy), (cx + 16, yy)), fill=c, width=4 * S)
    d.line(P((cx - 10, cy + 28), (cx + 10, cy + 28)), fill=c, width=3 * S)

def ic_booking(img, cx, cy, c, hi, bg):
    d = L(img)
    d.rounded_rectangle(P((cx - 32, cy - 26), (cx + 32, cy + 32)), 8 * S, fill=bg, outline=c, width=5 * S)
    d.rectangle(P((cx - 30, cy - 24), (cx + 30, cy - 10)), fill=c)
    for x in (cx - 16, cx + 16): d.line(P((x, cy - 36), (x, cy - 18)), fill=c, width=5 * S)
    d.line(P((cx - 14, cy + 10), (cx - 4, cy + 20), (cx + 16, cy - 2)), fill=hi, width=6 * S)

ICONS = dict(ai=ic_ai, soc=ic_social, wa=ic_wa, lang=ic_lang, sheet=ic_sheet, tmpl=ic_template, send=ic_send,
             chart=ic_chart, menu=ic_menu, book=ic_booking)

def icon(img, name, cx, cy, c, hi, bg):
    f = ICONS[name]
    if name == 'ai': f(img, cx, cy, c, hi)
    else: f(img, cx, cy, c, hi, bg)

def circ_node(img, cx, cy, r, T, name, num=None):
    d = L(img)
    d.ellipse(P((cx - r, cy - r), (cx + r, cy + r)), fill=T['node'], outline=T['acc'], width=4 * S)
    tmp = Image.new('RGBA', (int(110 * S), int(110 * S)), (0, 0, 0, 0))
    icon(tmp, name, 55, 55, T['nodeic'], YEL if not T['dark'] else LGREEN, T['node'])
    sz = int(r * 1.5 * S)
    tmp = tmp.resize((sz, sz), Image.LANCZOS)
    img.paste(tmp, (int(cx * S - sz / 2), int(cy * S - sz / 2)), tmp)
    if num:
        bx, by = cx + r * 0.72, cy - r * 0.72
        d.ellipse(P((bx - 17, by - 17), (bx + 17, by + 17)), fill=YEL, outline=T['bg'], width=3 * S)
        text(img, (bx, by + 1), str(num), 20, DEEP, PB, 'mm')

def arc_arrow(img, cx, cy, r, a0, a1, color, w=4):
    """Dashed arc from angle a0 to a1 (degrees, clockwise) with an arrowhead."""
    n = 30
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    dashed(img, pts, color, w=w, dash=11, gap=8)
    a = math.radians(a1); ta = a + math.pi / 2
    tip = (cx + r * math.cos(a), cy + r * math.sin(a))
    back = (tip[0] - 18 * math.cos(ta), tip[1] - 18 * math.sin(ta))
    nx, ny = math.cos(a), math.sin(a)
    L(img).polygon(P(tip, (back[0] + 10 * nx, back[1] + 10 * ny), (back[0] - 10 * nx, back[1] - 10 * ny)), fill=color)

def logo_width(size):
    return 2 * size * 0.62 + size * 0.28 + tw('Shri', size, PB) + size * 0.16 + tw('Tech', size, PB)

def cta3(img, T, l1, y=1214, M=48):
    rrect(img, (0, y, 1080, 1350), 0, fill=YEL if T['dark'] else DEEP)
    tc = BLACK if T['dark'] else (187, 247, 208)
    text(img, (M, y + 40), l1, 25, tc, PSB, 'lm')
    phone_icon(img, M + 26, y + 96, 44, BLACK if T['dark'] else YEL)
    text(img, (M + 64, y + 96), '9993615146', 60, BLACK if T['dark'] else YEL, PB, 'lm')
    # original logo, no box, right aligned
    size = 38
    lw = logo_width(size)
    if T['dark']:   # yellow band: dark green Shri + green Tech
        logo(img, 1080 - M - lw, y + 26, size, dark=False)
    else:           # deep green band: white Shri + light green Tech
        logo(img, 1080 - M - lw, y + 26, size, dark=True)
    text(img, (1080 - M, y + 104), 'Shri Balaji Digital Services', 20, BLACK if T['dark'] else WHITE, PM, 'rm')
