import numpy as np, wave
SR=44100; D=60.0; N=int(SR*D); out=np.zeros((N,2))
bpm=120; beat=60/bpm
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def add(x,start,g=1.0,pan=0.0):
    i=int(start*SR); x=x[:max(0,N-i)]
    out[i:i+len(x),0]+=x*g*(1-pan); out[i:i+len(x),1]+=x*g*(1+pan)
rng=np.random.default_rng(1)
def kick():
    n=int(.45*SR); t=np.arange(n)/SR; f=50+110*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
def hat(): n=int(.06*SR); x=rng.standard_normal(n); x=np.diff(x,prepend=0); return x*env(n,.001,.015)
def clap(): n=int(.25*SR); x=rng.standard_normal(n); return x*env(n,.002,.06)*.6
def tone(f,dur,kind='saw',d=.3):
    n=int(dur*SR); t=np.arange(n)/SR
    if kind=='saw': x=sum(np.sin(2*np.pi*f*k*t)/k for k in range(1,8))
    else: x=np.sin(2*np.pi*f*t)+.3*np.sin(4*np.pi*f*t)
    return x*env(n,.01,d)
# Indian-flavoured progression in A minor: Am F G Em
roots=[220.0,174.61,196.0,164.81]; KICK,HAT,CLAP=kick(),hat(),clap()
scale=[440,493.88,523.25,587.33,659.25,698.46,783.99,880]
mel=[0,2,4,2,5,4,2,1, 4,5,7,5,4,2,1,0]
for b in range(int(D/beat)):
    t=b*beat; bar=b//4; r=roots[bar%4]
    intro = t<5; outro=t>57.5
    if not intro: add(KICK,t,.9)
    elif b%2==0: add(KICK,t,.5)
    if b%2==1 and t>5: add(CLAP,t,.35)
    for h in range(2): add(HAT,t+h*beat/2,.12 if h else .07,pan=.3)
    # bass 8ths
    for h in range(2): add(tone(r/2,beat/2*.95,'saw',.12),t+h*beat/2,.11)
    # pad on bar start
    if b%4==0:
        for iv in (1,1.189,1.498):
            add(tone(r*iv,beat*4,'sine',2.0),t,.05,pan=-.2)
    # pluck melody from 5s
    if t>=5 and t<57:
        for h in range(2):
            k=mel[(b*2+h)%16]; add(tone(scale[k],.3,'sine',.12),t+h*beat/2,.09,pan=.25)
# whooshes at scene boundaries
for s in [5,11,19,26,33,40,47,53]:
    n=int(.7*SR); x=rng.standard_normal(n); t=np.arange(n)/SR
    e=np.sin(np.pi*t/.7)**2; x=np.convolve(x,np.ones(8)/8,'same')*e
    add(x,s-.45,.25)
# riser before CTA
n=int(2*SR); t=np.arange(n)/SR; add(np.sin(2*np.pi*np.cumsum(200+600*t/2)/SR)*(t/2)**2*.3,51)
# fade out
fo=np.ones(N); k=int(2*SR); fo[-k:]=np.linspace(1,0,k); out*=fo[:,None]
out=np.tanh(out*1.2); out/=np.abs(out).max()/0.89
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
