"""YouTube landscape 1920x1080 version of the Hindi comedy reel. Same audio, scenes, subtitles, dark theme."""
import os, sys, math, random, subprocess
sys.path.insert(0, '/home/claude/meme'); sys.path.insert(0, '/home/claude/reel')
import numpy as np
from PIL import Image, ImageDraw
import meme as MM
from reel import GREEN, GOLD, WHITE, FSYM, text_img, pill, put, _paste, glow_sprite, eo, prog
import reel2 as R2

W, H, FPS = 1920, 1080, 30
PW, PH = 1080, 1920
CROP = (300, 1430)          # portrait y-range holding the scene content
CROP_CTA = (320, 1520)
ZONE = (112, 935)           # landscape y-range for content

LW, LH = 240, 135
yy, xx = np.mgrid[0:LH, 0:LW].astype(np.float32)
rng = random.Random(7)
PARTS = [(rng.random() * W, rng.random() * H, rng.uniform(2, 6), rng.uniform(20, 60), rng.random() * 6.28, rng.choice([GREEN, GOLD, WHITE])) for _ in range(60)]
_grid = None
def background(t, accent=0.0):
    global _grid
    arr = np.zeros((LH, LW, 3), np.float32); arr[:] = (6, 12, 9)
    blobs = [(0.22 + 0.12 * math.sin(t * 0.4), 0.3 + 0.12 * math.cos(t * 0.33), 70, (34, 197, 94), 0.55),
             (0.8 + 0.1 * math.cos(t * 0.37), 0.68 + 0.12 * math.sin(t * 0.29), 80, (250, 180, 21), 0.38),
             (0.5 + 0.3 * math.sin(t * 0.21 + 2), 0.95 + 0.05 * math.sin(t * 0.5), 60, (16, 120, 70), 0.5)]
    for bx, by, r, c, a in blobs:
        d2 = ((xx - bx * LW) ** 2 + (yy - by * LH) ** 2) / (r * r)
        arr += (np.exp(-d2 * 2.2)[..., None] * a) * np.array(c, np.float32)
    v = 1 - 0.55 * (((xx / LW - 0.5) ** 2 + (yy / LH - 0.5) ** 2) * 2.2)
    arr *= np.clip(v, 0.25, 1)[..., None]
    if accent > 0: arr += accent * 60
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).convert('RGBA')
    if _grid is None:
        _grid = Image.new('RGBA', (W + 60, H + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(_grid)
        for x in range(0, W + 60, 60):
            for y in range(0, H + 60, 60): d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(120, 200, 150, 38))
    off = int((t * 18) % 60)
    img.alpha_composite(_grid.crop((off, off, off + W, off + H)))
    for (px, py, r, sp, ph, c) in PARTS:
        y = (py - t * sp) % (H + 100) - 50; x = px + 20 * math.sin(t * 0.8 + ph)
        tw = 0.5 + 0.5 * math.sin(t * 2 + ph)
        s = glow_sprite(c, int(r)); a = s.getchannel('A').point(lambda v, k=0.35 + 0.5 * tw: int(v * k))
        s2 = s.copy(); s2.putalpha(a); _paste(img, s2, int(x - s.width / 2), int(y - s.height / 2))
    return img

def topbar(base, t):
    a = eo(prog(t, 0.3, 0.5)) * (1 - eo(prog(t, MM.AUDIO_END, 0.4)))
    if a <= 0: return
    l1 = text_img('Shri', 44, WHITE); l2 = text_img('Tech', 44, GREEN, glow=GREEN)
    put(base, l1, 60 + l1.width / 2 - 60, 62, alpha=a)
    put(base, l2, 60 + l1.width - 120 - 60 + l2.width / 2 + 4, 62, alpha=a)
    p = pill('☎ 9993615146', 32, bg=(40, 32, 6), fg=GOLD, border=GOLD, path=FSYM)
    put(base, p, W - 60 - p.width / 2 + 60, 62, scale=1 + 0.04 * math.sin(t * 6), alpha=a)

def frame(t):
    flash = max([max(0, 1 - abs(t - b) / 0.12) for b in MM.CUTS] + [0])
    base = background(t * 1.6, accent=flash * 0.6)
    canvas = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    MM.scenes(canvas, t)
    y0, y1 = CROP_CTA if t >= MM.AUDIO_END else CROP
    part = canvas.crop((0, y0, PW, y1))
    sc = (ZONE[1] - ZONE[0]) / (y1 - y0)
    part = part.resize((int(PW * sc), int((y1 - y0) * sc)), Image.BILINEAR)
    _paste(base, part, int(W / 2 - part.width / 2), ZONE[0])
    topbar(base, t)
    for ci, (s0, s1) in enumerate(MM.SPANS):
        if s0 <= t < s1:
            active = None
            for j, (_, wt) in enumerate(MM.CHUNKS[ci]):
                if wt - 0.03 <= t: active = j
            p = min(1, (t - s0) / 0.15)
            put(base, MM.cap_img(ci, active), W / 2, 992 + 14 * (1 - p), scale=0.82 + 0.1 * eo(p))
            break
    for b in [24.5, MM.AUDIO_END]:
        pp = (t - (b - 0.3)) / 0.6
        if 0 < pp < 1:
            bw = 520; x = -bw + (W + bw * 2) * pp
            m = Image.new('L', (bw, 1), 0)
            for i in range(bw): m.putpixel((i, 0), int(130 * math.sin(math.pi * i / bw) ** 2))
            sw = Image.new('RGBA', (bw, H * 2), (210, 255, 225, 0)); sw.putalpha(m.resize((bw, H * 2)))
            sw = sw.rotate(-20, Image.BICUBIC, expand=True)
            _paste(base, sw, int(x - sw.width / 2), int(H / 2 - sw.height / 2))
    out = base.convert('RGB')
    if t < 0.15: out = Image.blend(Image.new('RGB', (W, H)), out, t / 0.15)
    return out

def render(a, b, path):
    tmp = path + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-crf', '21', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(round(a * FPS)), int(round(min(b, MM.DUR) * FPS))):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, path)

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]: frame(float(ts)).save(f'/home/claude/meme/yt/st_{ts}.jpg', quality=85)
    else:
        render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
