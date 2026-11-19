# Subtitles for reel 7 (Digital Power) — phrase starts read from the source video's own captions.
CAPS = [
 (0.0, 'Social|g Media|g'), (1.1, 'के इस दौर में'), (2.4, 'भारत में'), (3.3, '500|y Million|y से अधिक'),
 (6.1, 'YouTube|g Users हैं'), (7.8, '500|y Million|y से ज़्यादा'), (10.4, 'Instagram|g Users हैं'),
 (12.1, 'हमारे यहां'), (13.1, 'अलग अलग'), (14.2, 'मुद्दों पर'), (15.4, 'खुलकर'), (15.9, 'बहस होती है'),
 (17.1, 'अलग अलग'), (18.0, 'दृष्टिकोण पर'), (19.3, 'जनता'), (19.9, 'चर्चा|y करती है'),
 (21.2, 'और इसमें जिसने'), (22.8, 'एक बड़ी'), (23.5, 'भूमिका निभाई है'), (25.1, 'वह है'),
 (26.0, 'Digital|g Power|g'), (27.2, '12-13 साल पहले'), (28.9, 'तक Mobile|y'), (30.1, 'और Internet|y तक'),
 (31.2, 'पहुंच भी'), (32.2, 'अपने'), (32.7, 'आप में एक शक्ति|g हुआ'), (34.1, 'करती थी'), (34.9, 'जिसके पास'),
 (36.0, 'Access|y था,'), (37.1, 'उसके पास'), (37.6, 'Opportunities|g थीं'), (39.2, '2014|y के बाद'),
 (41.3, 'भारत ने'), (42.2, 'Mobile data को'), (43.9, 'Affordable|y'), (44.8, 'बनाने पर'), (45.5, 'ज़ोर दिया'),
 (46.4, 'आज एक छोटे'), (47.8, 'शहर का'), (48.5, 'विद्यार्थी भी'), (49.8, 'Digital|g Learning|g'),
 (51.0, 'से जुड़ सकता है'), (52.5, 'किसी गांव'), (53.3, 'में छोटा'), (54.0, 'दुकानदार|y भी नए'),
 (55.8, 'Customers|g'), (56.6, 'तक पहुंच सकता है'), (58.2, 'एक युवा भी'), (59.5, 'Online नए'),
 (60.6, 'Courses'), (61.4, 'Join कर सकता है'), (62.9, 'यही Power to'), (64.2, 'Empower|y है'),
 (65.7, 'हमारे यहां'), (66.8, 'एक Street|y Vendor|y'), (68.3, 'और एक बड़े'), (69.1, 'Car|g Showroom|g'),
 (70.2, 'का कारोबार'), (71.2, 'अलग अलग है'), (72.3, 'उनका scale'), (73.1, 'अलग है,'), (73.9, 'लेकिन भारत में'),
 (75.0, 'यह दोनों'), (76.3, 'Digital|g Payments|g'), (77.7, 'के एक ही'), (78.8, 'Ecosystem|y का'),
 (79.8, 'इस्तेमाल कर रहे हैं'), (81.5, 'यही'), (82.2, 'Inclusive|g Technology|g'), (83.9, 'की ताकत|y है'),
]
END_SPEECH = 85.1
GROUPS = []; SPANS = []
for i, (a, txt) in enumerate(CAPS):
    b = CAPS[i + 1][0] if i + 1 < len(CAPS) else END_SPEECH
    ws = txt.split(' ')
    dur = min(b - a, 0.35 * len(ws) + 0.4)
    lens = [len(w.split('|')[0]) + 2 for w in ws]; tot = sum(lens); t = a + 0.05; items = []
    for w, l in zip(ws, lens):
        t0, _, st = w.partition('|')
        items.append((round(t, 2), t0, st) if st else (round(t, 2), t0))
        t += dur * l / tot
    GROUPS.append(items); SPANS.append((a - 0.02, b - 0.02))
