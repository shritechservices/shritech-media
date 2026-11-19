"""v3 build: python3 build3.py [n ...] -> out3/NN-hi.jpg + NN-en.jpg"""
import sys, os, re
sys.path.insert(0, '/home/claude/posters/series/v3'); sys.path.insert(0, '/home/claude/posters/series')
from layouts import *
import illus
from data3 import POSTS3

OUT = '/home/claude/posters/series/v3/out3'
os.makedirs(OUT, exist_ok=True)

def render(p, lang):
    L = p[lang]
    img = bg(p['n'] % 5)
    header(img)
    if p.get('tone') == 'tribute':
        lay_T(img, p, L, lang)
        gloss.tribute_footer(img, L['cta'])
    else:
        LAYOUTS[p['lay']](img, p, L, lang)
        footer(img, L['cta'])
    path = f"{OUT}/{p['n']:02d}-{lang}.jpg"
    finish3(img, path, f"{p['occ']} {p['date']} - Shri Tech")
    return path

if __name__ == '__main__':
    only = [int(a) for a in sys.argv[1:]]
    for p in POSTS3:
        if only and p['n'] not in only: continue
        for lang in ('hi', 'en'):
            try: print(render(p, lang))
            except Exception:
                import traceback; traceback.print_exc(); print('FAIL', p['n'], lang)
