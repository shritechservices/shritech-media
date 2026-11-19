import sys; sys.path.insert(0, '/home/claude/meme'); sys.path.insert(0, '/home/claude/reel')
import meme_yt2 as Z
from meme_yt import background, W, H
import meme as MM
from reel import GREEN, GOLD, WHITE, FSYM, text_img, pill, put, glow_sprite
from PIL import Image
base = background(3.0, accent=0.15)
# right: three phones fanned
for k, x, y, r, s in [('4e9d3978', 1300, 560, 10, 0.95), ('3c987a50', 1720, 560, -10, 0.95), ('173cd744', 1510, 520, 0, 1.12)]:
    put(base, Z.phone_img(k), x, y, rot=r, scale=s)
# left: hook
put(base, text_img('अरे भाई साहब!', 92, GOLD, glow=(180, 120, 0)), 520, 150, rot=-3)
put(base, text_img('Instagram पे', 120, WHITE), 520, 320)
put(base, text_img('नाम नहीं?!', 190, (255, 90, 90), glow=(239, 68, 68)), 520, 500, rot=-4)
put(base, MM.social_icon('ig', 170), 1060, 500, rot=8)
put(base, MM.mark(False, 58), 1110, 550)
put(base, pill('बिज़नेस ऑनलाइन लाइए, बात बनेगी!', 50, bg=(14, 36, 22), fg=GREEN, border=GREEN, icon=True), 520, 690)
# brand + number
l1 = text_img('Shri', 110, WHITE); l2 = text_img('Tech', 110, GREEN, glow=GREEN)
put(base, l1, 140 + (l1.width - 120) / 2, 860); put(base, l2, 140 + (l1.width - 120) + 18 + (l2.width - 120) / 2, 860)
p = pill('☎ 9993615146', 64, bg=(40, 32, 6), fg=GOLD, border=GOLD, path=FSYM)
put(base, p, 140 + p.width / 2 - 60, 1000)
for x, y in [(90, 600), (1000, 180), (1880, 120), (1150, 960)]: put(base, glow_sprite(GOLD, 14), x, y)
im = base.convert('RGB').resize((1280, 720), Image.LANCZOS)
im.save('/home/claude/meme/yt/ShriTech_Comedy_YouTube_Thumbnail.jpg', quality=90)
