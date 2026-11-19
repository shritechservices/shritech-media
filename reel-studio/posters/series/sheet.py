import glob,sys
from PIL import Image
fs=sorted(glob.glob('out/*.jpg'))
per=6
for k in range(0,len(fs),per):
    ims=[Image.open(f).resize((540,675)) for f in fs[k:k+per]]
    s=Image.new('RGB',(540*3,675*2),'white')
    for i,im in enumerate(ims): s.paste(im,((i%3)*540,(i//3)*675))
    s.save(f'/tmp/sh{k//per:02d}.jpg',quality=82)
print(len(fs))
