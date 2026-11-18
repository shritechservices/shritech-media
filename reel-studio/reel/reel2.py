import os, sys, math, subprocess
os.environ['REEL_LANG'] = 'hi2'
sys.path.insert(0, '/home/claude/reel')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import reel as R
from reel import (W, H, FPS, GREEN, GOLD, WHITE, FB, FM, FSYM, text_img, pill, put, _paste, phone, crop_card,
                  shadowed, rrect_mask, glow_sprite, background, sweep, eo, eio, eback, prog, clamp, side_pills, _cache)
from captions import draw_caption, WORDS

B = [5.19, 13.29, 17.54, 22.43, 34.62, 41.78, 47.63, 52.36]
SC = [0] + B + [60]

def wt(word_prefix, default):
    for w, t0, t1, _ in WORDS:
        if w.startswith(word_prefix): return t0
    return default

def headline(base, t, t0, lines, y0, exit_t):
    R.headline(base, t, t0, lines, y0=y0, exit_t=exit_t)

def pmo(t, t0, t1, cy):
    p = prog(t, t0, 0.8); e = prog(t, t1 - 0.35, 0.35)
    y = cy + 900 * (1 - eback(p, 1.2)) + 18 * math.sin(t * 1.7)
    rot = 8 * (1 - eo(p)) + 1.5 * math.sin(t * 1.3)
    return y, rot, (0.92 + 0.08 * eo(p)) * (1 - 0.15 * e), 1 - e

# ---------- scenes ----------
def s_hook(base, t, t0, t1):
    cards = [crop_card('dfd79390', (394, 885, 686, 1176), 380, glow=GOLD),
             crop_card('dfd79390', (78, 885, 370, 1176), 380),
             crop_card('dfd79390', (711, 885, 1001, 1176), 380, glow=GOLD)]
    e = prog(t, t1 - 0.4, 0.4)
    for i, c in enumerate(cards):
        p = prog(t, 0.6 + i * 0.25, 1.0)
        x = [250, 830, 540][i] + 50 * math.sin(t + i); y = [1180, 1250, 1380][i]
        put(base, c, x, y + 500 * (1 - eo(p)), scale=0.85 + 0.1 * eo(p), rot=[-12, 10, -3][i] + 3 * math.sin(t * 1.5 + i),
            alpha=eo(p) * (1 - e))
    headline(base, t, 0.2, [('छोटा बिज़नेस,', 104, 'w'), ('बड़ी मार्केटिंग!', 124, 'g')], 400, t1 - 0.4)
    p = prog(t, 1.6, 0.5)
    put(base, pill('AI पोस्ट  +  WhatsApp मार्केटिंग', 42, bg=(44, 34, 4), fg=GOLD, border=GOLD), W / 2, 740,
        scale=0.5 + 0.5 * eback(p), alpha=eo(p) * (1 - e))

def s_steps(base, t, t0, t1):
    headline(base, t, t0, [('कैसे काम करता है?', 80, 'g'), ('सिर्फ़ 4 आसान स्टेप्स', 56, 'w')], 300, t1 - 0.35)
    y, rot, sc, a = pmo(t, t0 + 0.2, t1, 1180)
    put(base, phone('89edf9c0', eio(prog(t, t0 + 1.2, t1 - t0 - 2))), W / 2, y, scale=sc * 0.86, rot=rot, alpha=a)
    steps = [('1  बिज़नेस बताइए', 210, 700, GREEN), ('2  AI बनाए पोस्ट', 870, 900, GOLD),
             ('3  एडिट कीजिए', 210, 1200, GOLD), ('4  एक क्लिक पोस्ट', 860, 1420, GREEN)]
    for i, (txt, x, yy, c) in enumerate(steps):
        p = prog(t, t0 + 1.0 + 1.4 * i, 0.5)
        a2 = eo(p) * (1 - prog(t, t1 - 0.35, 0.35))
        pl = pill(txt, 38, bg=(14, 36, 22) if c == GREEN else (44, 34, 4), fg=c, border=c)
        put(base, pl, x, yy + 10 * math.sin(t * 2 + i), scale=0.5 + 0.5 * eback(p), rot=3 * math.sin(t + i * 2), alpha=a2)

def s_dash(base, t, t0, t1):
    headline(base, t, t0, [('आपका डैशबोर्ड', 84, 'g'), ('सब कुछ एक नज़र में', 56, 'w')], 300, t1 - 0.35)
    y, rot, sc, a = pmo(t, t0 + 0.2, t1, 1200)
    k = eio(prog(t, t0 + 1.2, 0.6))
    put(base, phone('520416cf', 0.15 * eio(prog(t, t0 + 0.8, 2))), W / 2 - 170 * k, y, scale=sc * 0.86 * (1 - 0.1 * k), rot=rot - 3 * k, alpha=a * (1 - 0.35 * k))
    e = prog(t, t1 - 0.35, 0.35)
    c1 = crop_card('520416cf', (38, 350, 1042, 585), 520)
    c2 = crop_card('520416cf', (38, 1405, 1042, 1880), 560, glow=GOLD)
    p = prog(t, t0 + 1.3, 0.6)
    put(base, c1, W / 2 + 170 + 300 * (1 - eo(p)), 880 + 10 * math.sin(t * 2), scale=0.6 + 0.4 * eback(p), rot=-3, alpha=eo(p) * (1 - e))
    p = prog(t, t0 + 1.9, 0.6)
    put(base, c2, W / 2 + 150 + 300 * (1 - eo(p)), 1260 + 12 * math.sin(t * 1.7), scale=0.6 + 0.4 * eback(p), rot=3, alpha=eo(p) * (1 - e))

def ring(r, a, c=GREEN, w=6):
    im = Image.new('RGBA', (int(r * 2 + 12), int(r * 2 + 12)), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((6, 6, r * 2 + 6, r * 2 + 6), outline=c + (int(255 * a),), width=w)
    return im

def s_free(base, t, t0, t1):
    e = prog(t, t1 - 0.35, 0.35)
    headline(base, t, t0, [('शुरुआत बिल्कुल फ़्री!', 92, 'g')], 360, t1 - 0.35)
    p = prog(t, t0 + 0.8, 0.6)
    n = int(round(10 * eio(prog(t, t0 + 0.9, 1.0))))
    for k in range(3):
        ph = ((t - t0) * 0.7 + k / 3) % 1
        put(base, ring(150 + 260 * ph, (1 - ph) * eo(p) * (1 - e), GOLD if k % 2 else GREEN), W / 2, 880)
    put(base, text_img(str(n), 330, grad=(GREEN, GOLD), glow=GREEN), W / 2, 870, scale=(0.4 + 0.6 * eback(p, 2)) * (1 + 0.03 * math.sin(t * 5)), alpha=eo(p) * (1 - e))
    p2 = prog(t, t0 + 1.4, 0.5)
    put(base, text_img('फ़्री क्रेडिट्स हर महीने', 70, WHITE), W / 2, 1150, scale=0.8 + 0.2 * eo(p2), alpha=eo(p2) * (1 - e))
    for i, (txt, c) in enumerate([('कोई कार्ड नहीं चाहिए', GOLD), ('आज ही शुरू करें', GREEN)]):
        pp = prog(t, t0 + 2.0 + 0.35 * i, 0.5)
        put(base, pill(txt, 42, bg=(14, 36, 22) if c == GREEN else (44, 34, 4), fg=c, border=c, icon=True),
            W / 2, 1300 + 115 * i, scale=0.5 + 0.5 * eback(pp), alpha=eo(pp) * (1 - e))

def plan_card(name, price, per, credits, color, tag=None):
    key = ('plan', name)
    if key in _cache: return _cache[key]
    cw, ch = 880, 230
    bg = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    arr = np.zeros((ch, cw, 4), np.uint8)
    gx = np.linspace(0, 1, cw)[None, :, None]
    col = np.array((16, 26, 20)) * (1 - gx) + np.array(color) * 0.18 * gx + np.array((10, 16, 12)) * gx
    arr[..., :3] = np.broadcast_to(col, (ch, cw, 3)); arr[..., 3] = 245
    bg = Image.fromarray(arr, 'RGBA'); bg.putalpha(rrect_mask(cw, ch, 36))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((0, 0, cw - 1, ch - 1), 36, outline=color + (255,), width=4)
    nm = text_img(name, 58, WHITE, shadow=False)
    _paste(bg, nm, 50 - 60, 60 - nm.height // 2 + 10)
    cr = text_img(credits, 40, color, path=FM, shadow=False)
    _paste(bg, cr, 50 - 60, 150 - cr.height // 2 + 10)
    pr = text_img(price, 96, grad=(GREEN, GOLD), shadow=False)
    pe = text_img(per, 36, (200, 210, 204), path=FM, shadow=False)
    px = cw - 40 - (pe.width - 120) - (pr.width - 120) - 10
    _paste(bg, pr, px - 60, ch // 2 - pr.height // 2 + 5)
    _paste(bg, pe, px + (pr.width - 120) + 10 - 60, ch // 2 - pe.height // 2 + 30)
    out = shadowed(bg, radius=36, blur=24, off=18, glow=color, glow_a=0.55)
    if tag:
        tg = pill(tag, 30, bg=(44, 34, 4), fg=GOLD, border=GOLD)
        _paste(out, tg, out.width // 2 + cw // 2 - tg.width + 20, out.height // 2 - ch // 2 - tg.height // 2 + 10)
    _cache[key] = out
    return out

def s_plans(base, t, t0, t1):
    headline(base, t, t0, [('प्लान्स और प्राइस', 88, 'g'), ('हर बिज़नेस के लिए', 56, 'w')], 290, t1 - 0.35)
    e = prog(t, t1 - 0.4, 0.4)
    cards = [(plan_card('Growth', '₹1,799', '/30 दिन', '400 क्रेडिट्स', GREEN), wt('Growth', t0 + 0.4) - 0.2, 720),
             (plan_card('Pro', '₹3,999', '/30 दिन', '1000 क्रेडिट्स', GOLD, tag='बेस्ट वैल्यू'), wt('Pro', t0 + 5) - 0.2, 1000),
             (plan_card('टॉप-अप', '₹399', '', '+50 क्रेडिट्स', GREEN), wt('टॉप-अप', t0 + 9) - 0.2, 1280)]
    for i, (c, ta, y) in enumerate(cards):
        p = prog(t, ta, 0.6)
        side = -1 if i % 2 == 0 else 1
        # highlight the card being talked about
        nxt = cards[i + 1][1] if i + 1 < len(cards) else t1
        hl = 1.0 if ta <= t < nxt else 0.0
        sc = (0.7 + 0.3 * eback(p)) * (1 + 0.04 * hl * (0.5 + 0.5 * math.sin(t * 6)))
        put(base, c, W / 2 + side * 700 * (1 - eo(p)), y + 8 * math.sin(t * 1.8 + i), scale=sc * (1 - 0.15 * e),
            rot=side * 4 * (1 - eo(p)), alpha=eo(p) * (1 - e) * (1 if hl or t < ta else 0.75))

def s_addon(base, t, t0, t1):
    headline(base, t, t0, [('WhatsApp मार्केटिंग', 80, 'g'), ('ऐड-ऑन', 64, 'w')], 300, t1 - 0.35)
    e = prog(t, t1 - 0.35, 0.35)
    card = crop_card('4e0475b8', (38, 1245, 1042, 2040), 840)
    p = prog(t, t0 + 0.5, 0.7)
    put(base, card, W / 2, 1060 + 12 * math.sin(t * 1.6) + 400 * (1 - eo(p)), scale=(0.6 + 0.4 * eback(p)) * (1 + 0.015 * math.sin(t * 3)),
        rot=-2 + 1.5 * math.sin(t), alpha=eo(p) * (1 - e))
    for k in range(5):
        ph = t * 2.5 + k * 1.3
        a = max(0, math.sin(ph)) * eo(p) * (1 - e)
        put(base, glow_sprite(GOLD, 9), 120 + k * 210, 640 + 60 * (k % 2), scale=0.7 + 0.6 * a, alpha=a)
    pp = prog(t, wt('सेटअप', t0 + 4) - 0.2, 0.5)
    put(base, pill('सेटअप में पूरी मदद', 42, bg=(44, 34, 4), fg=GOLD, border=GOLD, icon=True), W / 2, 1480,
        scale=0.5 + 0.5 * eback(pp), alpha=eo(pp) * (1 - e))

def s_charge(base, t, t0, t1):
    e = prog(t, t1 - 0.35, 0.35)
    headline(base, t, t0, [('मैसेज चार्ज', 84, 'g'), ('सीधे Meta को, लगभग', 56, 'w')], 300, t1 - 0.35)
    p = prog(t, t0 + 0.6, 0.6)
    v = 0.86 * eio(prog(t, t0 + 0.7, 1.2))
    put(base, text_img(f'₹{v:.2f}', 230, grad=(GREEN, GOLD), glow=GREEN), W / 2, 780, scale=(0.5 + 0.5 * eback(p)), alpha=eo(p) * (1 - e))
    put(base, text_img('प्रति मार्केटिंग मैसेज', 56, WHITE, path=FM), W / 2, 960, alpha=eo(prog(t, t0 + 1.0, 0.5)) * (1 - e))
    # stamp
    ps = prog(t, wt('कोई', t0 + 3) - 0.15, 0.45)
    if ps > 0:
        if 'stamp0' not in _cache:
            sw, sh = 640, 220
            im = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((6, 6, sw - 7, sh - 7), 40, outline=GOLD + (255,), width=10)
            d.rounded_rectangle((22, 22, sw - 23, sh - 23), 30, outline=GOLD + (160,), width=3)
            tx = text_img('0% मार्कअप', 100, GOLD, shadow=False)
            _paste(im, tx, sw // 2 - tx.width // 2, sh // 2 - tx.height // 2 + 6)
            _cache['stamp0'] = shadowed(im, radius=40, blur=18, off=12, glow=GOLD, glow_a=0.5)
        put(base, _cache['stamp0'], W / 2, 1230, scale=2.2 - 1.2 * eback(ps, 2.5), rot=-7, alpha=eo(ps) * (1 - e))
    pp = prog(t, t0 + 1.4, 0.5)
    put(base, pill('सिर्फ़ सहमति वाले ग्राहकों को मैसेज', 36, icon=True), W / 2, 1450, scale=0.5 + 0.5 * eback(pp), alpha=eo(pp) * (1 - e))

def s_report(base, t, t0, t1):
    headline(base, t, t0, [('लाइव रिपोर्ट', 88, 'g'), ('डिलीवरी • रीड • कैंपेन', 56, 'w')], 300, t1 - 0.35)
    y, rot, sc, a = pmo(t, t0 + 0.2, t1, 1200)
    k = eio(prog(t, t0 + 1.0, 0.6))
    put(base, phone('cedf721b', 0.5 * eio(prog(t, t0 + 0.6, 3))), W / 2 - 160 * k, y, scale=sc * 0.86 * (1 - 0.1 * k), rot=rot - 3 * k, alpha=a * (1 - 0.35 * k))
    c = crop_card('cedf721b', (38, 797, 1042, 1450), 600)
    p = prog(t, t0 + 1.1, 0.6); e = prog(t, t1 - 0.35, 0.35)
    put(base, c, W / 2 + 130 + 300 * (1 - eo(p)), 1130 + 12 * math.sin(t * 1.8), scale=0.6 + 0.4 * eback(p), rot=3 - 1.5 * math.sin(t), alpha=eo(p) * (1 - e))

def s_cta(base, t, t0, t1):
    headline(base, t, t0, [('अधिक जानकारी के लिए', 76, 'w'), ('संपर्क करें', 110, 'g')], 360, None)
    p = prog(t, t0 + 0.8, 0.7)
    if p > 0:
        # reuse the call button built by reel.s_cta
        if 'callbtn' not in _cache:
            R.s_cta(Image.new('RGBA', (W, H)), 60.0)
        for k in range(3):
            ph = ((t - t0) * 0.8 + k / 3) % 1
            r = Image.new('RGBA', (1100, 400), (0, 0, 0, 0))
            w2, h2 = 450 + 120 * ph, 100 + 90 * ph
            ImageDraw.Draw(r).rounded_rectangle((550 - w2, 200 - h2, 550 + w2, 200 + h2), int(h2), outline=GREEN + (int(200 * (1 - ph) * eo(p)),), width=5)
            put(base, r, W / 2, 800)
        put(base, _cache['callbtn'], W / 2, 800, scale=(0.3 + 0.7 * eback(p, 2.2)) * (1 + 0.035 * math.sin((t - t0) * 7)), alpha=eo(p))
    feats = [('10 फ़्री क्रेडिट्स हर महीने', 1010, GREEN), ('प्लान्स ₹1,799 से', 1115, GOLD), ('WhatsApp ऐड-ऑन ₹999/महीना', 1220, GREEN)]
    for i, (txt, y, c) in enumerate(feats):
        pp = prog(t, t0 + 1.5 + 0.25 * i, 0.5)
        put(base, pill(txt, 40, bg=(14, 36, 22) if c == GREEN else (44, 34, 4), fg=c, border=c, icon=True),
            W / 2 + 500 * (1 - eo(pp)) * (1 if i % 2 else -1), y, scale=0.9 + 0.1 * eo(pp), alpha=eo(pp))
    pp = prog(t, t0 + 2.6, 0.6)
    l1 = text_img('Shri', 100, WHITE); l2 = text_img('Tech', 100, GREEN, glow=GREEN)
    sc = 0.6 + 0.4 * eback(pp); tw = (l1.width - 120 + l2.width - 120) * sc
    put(base, l1, W / 2 - tw / 2 + (l1.width - 120) * sc / 2, 1350, scale=sc, alpha=eo(pp))
    put(base, l2, W / 2 + tw / 2 - (l2.width - 120) * sc / 2, 1350, scale=sc, alpha=eo(pp))
    pp = prog(t, t0 + 3.3, 0.5)
    put(base, text_img('आज ही कॉल करें!', 64, GOLD, glow=(180, 120, 0)), W / 2, 1460, scale=0.7 + 0.3 * eback(pp) + 0.03 * math.sin(t * 5), alpha=eo(pp))

SCENES = [s_hook, s_steps, s_dash, s_free, s_plans, s_addon, s_charge, s_report, s_cta]

def topbar(base, t):
    a = eo(prog(t, B[0] + 0.3, 0.6)) * (1 - eo(prog(t, B[-1], 0.5)))
    if a <= 0: return
    logo1 = text_img('Shri', 46, WHITE); logo2 = text_img('Tech', 46, GREEN, glow=GREEN)
    y = 150 - 30 * (1 - a)
    put(base, logo1, 70 + logo1.width / 2 - 60, y, alpha=a)
    put(base, logo2, 70 + logo1.width - 120 - 60 + logo2.width / 2 + 4, y, alpha=a)
    p = pill('☎ 9993615146', 34, bg=(40, 32, 6), fg=GOLD, border=GOLD, path=FSYM)
    put(base, p, W - 70 - p.width / 2 + 60, y, scale=1 + 0.04 * math.sin(t * 6), alpha=a)

def frame(t):
    acc = max([max(0, 1 - abs(t - b) / 0.15) for b in B] + [0])
    base = background(t, accent=acc * 0.5)
    for i, fn in enumerate(SCENES):
        if SC[i] - 0.01 <= t < SC[i + 1] + 0.01:
            fn(base, t, SC[i], SC[i + 1])
    topbar(base, t)
    draw_caption(base, t)
    for b in B: sweep(base, (t - (b - 0.35)) / 0.7)
    out = base.convert('RGB')
    if t < 0.3: out = Image.blend(Image.new('RGB', (W, H)), out, t / 0.3)
    return out

def render(a, b, path):
    tmp = path + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-crf', '19', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, path)

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            frame(float(ts)).save(f'/home/claude/reel/still_hi2_{ts}.jpg', quality=85)
    else:
        render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
