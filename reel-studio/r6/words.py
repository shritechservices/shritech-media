# Hindi subtitles for reel 6; phrase spans from the voice loudness profile, word times spread by length.
PHR = [
    (0.30, 2.10, ['AI|g', 'से', '100|y', 'पोस्ट', 'बन', 'गयीं?']),
    (3.00, 4.40, ['फिर', 'भी', 'कोई', 'रुका|y', 'नहीं।']),
    (5.40, 6.60, ['स्पीड|g', 'AI', 'की', 'है।']),
    (7.10, 8.70, ['बात|y', 'आपकी', 'होनी', 'चाहिए।']),
    (9.60, 11.40, ['AI|g', 'टेक्स्ट', 'जल्दी', 'लिख', 'देता', 'है।']),
    (12.20, 14.20, ['AI|g', 'इमेज', 'जल्दी', 'बना', 'देता', 'है।']),
    (15.00, 16.30, ['पर', 'किसे', 'क्या', 'कहना|y', 'है,']),
    (16.40, 18.20, ['ये', 'आप|g', 'जानते', 'हैं।']),
    (19.00, 20.30, ['जब', 'बात|y', 'आपकी', 'हो']),
    (20.50, 21.70, ['और', 'स्पीड|g', 'AI', 'की,']),
    (21.80, 23.30, ['तब', 'लोग', 'रुकते|y', 'हैं।']),
    (24.10, 26.20, ['यही', 'है', 'AI', 'का', 'सही|y', 'उपयोग।|g']),
]
GROUPS = []
for a, b, ws in PHR:
    lens = [len(w.split('|')[0]) + 2 for w in ws]
    tot = sum(lens); t = a; items = []
    for w, l in zip(ws, lens):
        txt, _, st = w.partition('|')
        items.append((round(t, 2), txt, st) if st else (round(t, 2), txt))
        t += (b - a) * l / tot
    # split long phrases into chunks of <= 4 words
    while items:
        GROUPS.append(items[:4] if len(items) != 5 else items[:3]); items = items[len(GROUPS[-1]):]
SPANS = []
for i, g in enumerate(GROUPS):
    s = g[0][0] - 0.06
    nxt = GROUPS[i + 1][0][0] - 0.06 if i + 1 < len(GROUPS) else 26.6
    SPANS.append((s, min(nxt, g[-1][0] + 0.9)))

# snap estimated word starts to nearby energy onsets in the voice
def _snap():
    import wave, numpy as np
    w = wave.open('/home/claude/r6/src/a.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768
    hop = 160; n = len(a) // hop
    e = np.array([np.sqrt((a[i*hop:(i+1)*hop]**2).mean()) + 1e-9 for i in range(n)])
    db = 20 * np.log10(e)
    sm = np.convolve(db, np.ones(3) / 3, 'same')
    on = [i * 0.01 for i in range(5, n - 1) if sm[i] - sm[i - 5] > 6 and sm[i] > -30]
    on = np.array(on)
    for gi, g in enumerate(GROUPS):
        ng = []
        for it in g:
            t = it[0]; c = on[np.abs(on - t) < 0.14] if len(on) else []
            if len(c): t = float(c[np.argmin(np.abs(c - t))]) - 0.03
            ng.append((round(t, 2),) + tuple(it[1:]))
        for k in range(1, len(ng)):
            if ng[k][0] <= ng[k-1][0] + 0.08: ng[k] = (round(ng[k-1][0] + 0.1, 2),) + ng[k][1:]
        GROUPS[gi] = ng
_snap()
SPANS = []
for i, g in enumerate(GROUPS):
    s = g[0][0] - 0.06
    nxt = GROUPS[i + 1][0][0] - 0.06 if i + 1 < len(GROUPS) else 26.6
    SPANS.append((s, min(nxt, g[-1][0] + 0.9)))
