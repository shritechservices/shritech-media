"""YouTube landscape v2: same video + side phones cycling real dark-theme Shri Tech screens."""
import sys, math, os, subprocess
sys.path.insert(0, '/home/claude/meme'); sys.path.insert(0, '/home/claude/reel')
import meme_yt as Y
from meme_yt import *
from PIL import Image, ImageDraw, ImageFilter
from reel import GREEN, GOLD, WHITE, text_img, pill, put, eo, prog, shadowed

UP = '/mnt/user-data/uploads/'
LEFT = ['173cd744', '89edf9c0', '21442f26', '3c987a50', '520416cf', 'beb50932']
RIGHT = ['4e9d3978', '8de181ef', '96a199dd', 'e5d0d48b', 'cedf721b']
PWID, PHGT, BZ = 340, 640, 12
SW, SH = PWID - 2 * BZ, PHGT - 2 * BZ
_c = {}

def phone_img(k):
    if k in _c: return _c[k]
    sc = Image.open(UP + k + '-image.jpg').convert('RGB')
    s = sc.resize((SW, int(sc.height * SW / sc.width)), Image.LANCZOS).crop((0, 0, SW, SH))
    im = Image.new('RGBA', (PWID, PHGT), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, PWID - 1, PHGT - 1), 42, fill=(22, 30, 26, 255), outline=(60, 160, 100, 255), width=3)
    m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 32, fill=255)
    im.paste(s, (BZ, BZ), m)
    d.rounded_rectangle((PWID / 2 - 40, BZ + 8, PWID / 2 + 40, BZ + 22), 7, fill=(0, 0, 0, 255))
    out = shadowed(im, radius=42, blur=26, off=16, glow=GREEN, glow_a=0.45)
    _c[k] = out
    return out

def side_phone(base, t, keys, cx, label, ph0, ta):
    a = eo(prog(t, ta, 0.6))
    if a <= 0: return
    per = 3.0
    i = int((t + ph0) // per) % len(keys); f = ((t + ph0) % per) / per
    j = (i + 1) % len(keys)
    cy = 500 + 10 * math.sin(t * 1.4 + cx)
    rot = 2.5 * math.sin(t * 0.9 + cx) + (-4 if cx < W / 2 else 4)
    put(base, phone_img(keys[i]), cx, cy, rot=rot, alpha=a, scale=0.9 + 0.1 * a)
    if f > 0.82:
        put(base, phone_img(keys[j]), cx, cy, rot=rot, alpha=a * eo((f - 0.82) / 0.18), scale=0.9 + 0.1 * a)
    p = pill(label, 30, bg=(14, 36, 22), fg=GREEN, border=GREEN, icon=True)
    put(base, p, cx, 905, alpha=a)

_frame0 = Y.frame
def frame(t):
    out = _frame0(t).convert('RGBA')
    side_phone(out, t, LEFT, 285, 'AI पोस्ट डिज़ाइन', 0.0, 0.8)
    side_phone(out, t, RIGHT, W - 285, 'WhatsApp मार्केटिंग', 1.5, 1.1)
    return out.convert('RGB')

def render(a, b, path):
    tmp = path + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-crf', '24', '-preset', 'medium', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(round(a * FPS)), int(round(min(b, MM.DUR) * FPS))):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, path)

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]: frame(float(ts)).save(f'/home/claude/meme/yt/s2_{ts}.jpg', quality=85)
    else: render(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
