import sys, os, re
sys.path.insert(0, '/home/claude/posters/series')
from art import *
from data import POSTS

OUT = '/home/claude/posters/series/out'
os.makedirs(OUT, exist_ok=True)

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def render(p):
    img = base()
    ART[p['art']](img)
    header(img)
    greeting(img, p['title'], p.get('line2'))
    story_pill(img, p['pill'])
    DIAGRAMS[p['dg']](img, p['d'])
    if p.get('tone') == 'tribute':
        tribute_footer(img, p['foot'])
    else:
        ribbon(img, p['rib'], p['chips'])
        cta(img, p['cta'])
    path = f"{OUT}/{p['n']:02d}-{p['date']}-{slug(p['occ'])}.jpg"
    finish3(img, path, f"{p['occ']} {p['date']} - Shri Tech")
    return path

if __name__ == '__main__':
    only = [int(a) for a in sys.argv[1:]]
    for p in POSTS:
        if only and p['n'] not in only: continue
        try: print(render(p))
        except Exception as e:
            import traceback; traceback.print_exc(); print('FAIL', p['n'])
