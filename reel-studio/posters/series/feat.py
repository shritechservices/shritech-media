# -*- coding: utf-8 -*-
"""v2.1: each post explains ONE real Shri Tech feature with a light-theme website screenshot (from the User Manual).
Crops avoid prices, sample footer contact details, 'failed' rows, LinkedIn (locked) and admin screens."""
import sys
sys.path.insert(0, '/home/claude/posters/series')
from kit import *
import gloss
from gloss import grrect, gellipse

SCR = '/home/claude/manual/screens/'
# key: (file, y0, y1) in screenshot pixels (780 x 1688)
SHOT = {
    'hero':      ('p04-front-page-1.jpg', 60, 640),
    'how':       ('p04-front-page-2.jpg', 0, 1180),
    'flow':      ('p04-front-page-3.jpg', 380, 1688),
    'reports':   ('p05-front-pricing-whatsapp-1.jpg', 380, 1450),
    'login':     ('p06-login-1.jpg', 60, 820),
    'dash':      ('p07-dashboard-1.jpg', 120, 1500),
    'dash2':     ('p07-dashboard-2.jpg', 0, 930),
    'form':      ('p09-create-ai-image-1.jpg', 120, 1500),
    'brand':     ('p09-create-ai-image-2.jpg', 0, 1100),
    'own':       ('p10-create-own-image-1.jpg', 120, 1100),
    'review':    ('p11-review-approve-post-1.jpg', 150, 1420),
    'history':   ('p12-history-1.jpg', 150, 1300),
    'history2':  ('p12-history-2.jpg', 0, 950),
    'pages':     ('p14-account-1.jpg', 120, 760),
    'tour':      ('p15-whatsapp-tour-1.jpg', 180, 1620),
    'tour2':     ('p15-whatsapp-tour-2.jpg', 0, 700),
    'wahome':    ('p16-whatsapp-home-1.jpg', 150, 980),
    'wachart':   ('p16-whatsapp-home-2.jpg', 0, 1000),
    'excel':     ('p17-whatsapp-contacts-1.jpg', 150, 1500),
    'contacts':  ('p17-whatsapp-contacts-2.jpg', 200, 1350),
    'templates': ('p18-whatsapp-templates-1.jpg', 150, 1480),
    'newtmpl':   ('p18-whatsapp-templates-2.jpg', 250, 1600),
    'campaign':  ('p19-whatsapp-campaigns-1.jpg', 700, 1688),
    'campstat':  ('p19-whatsapp-campaigns-3.jpg', 0, 900),
    'inbox':     ('p20-whatsapp-chat-replies-1.jpg', 600, 1600),
    'chat':      ('p20-whatsapp-chat-replies-2.jpg', 1000, 1660),
    'seen':      ('p21-whatsapp-seen-liked-1.jpg', 700, 1688),
    'howwa':     ('p22-whatsapp-help-costs-1.jpg', 740, 1350),
    'safe':      ('p22-whatsapp-help-costs-2.jpg', 150, 740),
}

# n: (style, [shots], feature title, [3 points])   style: L = shot left, R = shot right, D = two shots
FEAT = {
 1: ('L', ['campaign'], 'एक क्लिक में ऑफर, हर ग्राहक तक', ['सबको, अगला बैच या ग्रुप चुनें', 'अभी भेजें या बाद में', 'हर ग्राहक को उसके नाम से']),
 2: ('R', ['form'], 'एक बार जानकारी, हर दिन नया पोस्टर', ['नाम, नंबर, पता एक बार', 'इमेज टाइप: त्योहार, ऑफर', 'अगली बार सिर्फ ऑफर लाइन']),
 3: ('L', ['review'], 'देखें, बदलें, फिर पोस्ट करें', ['जो दिखे वही पोस्ट हो', 'कैप्शन आप बदल सकते हैं', 'FB, Instagram, WhatsApp चुनें']),
 4: ('R', ['chat'], 'ग्राहक से सीधी बात, एक ही जगह', ['सारे जवाब एक इनबॉक्स में', 'क्विक रिप्लाई से तुरंत जवाब', 'फ़ोटो और जानकारी भेजें']),
 5: ('D', ['brand', 'flow'], 'आपके रंग, आपका लोगो, आपका ब्रांड', ['दो ब्रांड रंग', 'अपना लोगो', 'हर पोस्टर ब्रांड जैसा']),
 6: ('L', ['flow'], 'आइडिया से पोस्ट, तीनों जगह', ['आप जानकारी दें', 'पोस्टर + कैप्शन तैयार', 'एक क्लिक: FB + Instagram']),
 7: ('R', ['contacts'], 'मेंबर्स की लिस्ट, ग्रुप के साथ', ['टैग से ग्रुप बनाएँ', 'नाम या नंबर से खोजें', 'STOP वाले अपने-आप अलग']),
 9: ('L', ['dash'], 'डैशबोर्ड: सब एक नज़र में', ['बचे क्रेडिट और आपका प्लान', 'इस महीने के पोस्ट', 'पिछले 7 दिन का चार्ट']),
 10: ('R', ['own'], 'अपनी फ़ोटो से पोस्ट', ['मोबाइल से फ़ोटो चुनें', '1-2 लाइन में बताएँ', 'कैप्शन अपनी भाषा में']),
 11: ('L', ['inbox'], 'किसने लिखा, सब एक जगह', ['पिछले 24 घंटे के जवाब', 'जवाब देना मुफ़्त', 'हर चैट पर नया मैसेज दिखे']),
 13: ('R', ['wachart'], 'हर कैंपेन की पूरी रिपोर्ट', ['14 दिन का मैसेज चार्ट', 'चल रहे और पूरे कैंपेन', 'शेड्यूल कैंपेन भी']),
 14: ('D', ['own', 'review'], 'घर बैठे: फ़ोटो डालें, पोस्ट करें', ['फ़ोटो चुनें', 'कैप्शन तैयार', 'मंज़ूर करें, पोस्ट']),
 15: ('L', ['tour'], 'ऑफर सीधे ग्राहक के WhatsApp में', ['Excel से कॉन्टैक्ट', 'सैकड़ों को एक साथ', 'पोस्टर + कैप्शन एक मैसेज में']),
 16: ('R', ['history'], 'हर पोस्ट का पूरा रिकॉर्ड', ['कब और कहाँ पोस्ट हुआ', 'आख़िरी 3 इमेज सेव', 'हर पोस्ट का स्टेटस']),
 18: ('L', ['templates'], 'मंज़ूर मैसेज टेम्पलेट', ['Meta से अप्रूवल यहीं से', 'ग्राहक का नाम अपने-आप', 'रिमाइंडर, ऑफर, धन्यवाद']),
 19: ('D', ['hero', 'how'], 'बिज़नेस बताइए, पोस्ट तैयार', ['बताइए', 'बनाइए', 'पोस्ट कीजिए']),
 20: ('R', ['own'], 'काम की फ़ोटो से शानदार पोस्ट', ['अपनी फ़ोटो अपलोड', 'काम के बारे में 1 लाइन', 'कैप्शन अपने-आप']),
 21: ('L', ['campstat'], 'शेड्यूल, रोकें, रिपोर्ट', ['तय समय पर अपने-आप', 'रोकें या कैंसिल करें', 'रिपोर्ट डाउनलोड करें']),
 22: ('D', ['hero', 'dash'], 'AI से पोस्ट, कंट्रोल आपके हाथ में', ['AI पोस्टर', 'डैशबोर्ड', 'आपकी मंज़ूरी']),
 23: ('D', ['own', 'history2'], 'फ़ोटो › कैप्शन › पोस्ट', ['फ़ोटो डालें', 'कैप्शन तैयार', 'हिस्ट्री में सेव']),
 24: ('L', ['excel'], 'Excel से सदस्य जोड़ें', ['नाम, नंबर और टैग', 'एक फाइल में ढेरों नंबर', 'सिर्फ सहमति वाले लोग']),
 25: ('R', ['chat'], 'फ़्री रिप्लाई विंडो में तुरंत जवाब', ['ग्राहक ने लिखा? 24 घंटे खुला', 'क्विक रिप्लाई', 'कॉल बटन भी']),
 26: ('L', ['seen'], 'किसने देखा, किसने लाइक किया', ['ऑफर पढ़ने वाले लोग', 'लाइक करने वाले लोग', 'उन्हें तुरंत जवाब']),
 27: ('R', ['brand'], 'अपनी भाषा, अपना ब्रांड', ['हिंदी या English', 'अपने ब्रांड रंग', 'अपना लोगो']),
 28: ('L', ['safe'], 'नंबर सुरक्षित रखने के नियम', ['सिर्फ सहमति वाले ग्राहक', 'STOP पर अपने-आप हटें', 'रोज़ की सीमा धीरे बढ़े']),
 29: ('D', ['tour', 'campaign'], 'त्योहार ऑफर, सीधे WhatsApp पर', ['ऑफर तैयार', 'कैंपेन', 'सबको एक साथ']),
 30: ('R', ['dash2'], 'स्कोरबोर्ड जैसा डैशबोर्ड', ['7 दिन का क्रेडिट चार्ट', 'हाल के पोस्ट', 'पोस्ट बनाएँ, एक बटन']),
 31: ('D', ['pages', 'review'], 'पेज जुड़े, एक क्लिक पोस्ट', ['FB + Instagram जुड़े', 'प्रीव्यू', 'एक क्लिक']),
 32: ('L', ['campaign'], 'हर अभिभावक तक एक साथ सूचना', ['पूरी लिस्ट या ग्रुप', 'अभी या बाद में', 'मंज़ूर टेम्पलेट से']),
 33: ('R', ['newtmpl'], 'हिंदी में भी मैसेज टेम्पलेट', ['नाम और भाषा चुनें', '{{1}} = ग्राहक का नाम', 'अप्रूवल के लिए भेजें']),
 34: ('D', ['contacts', 'campstat'], 'पुराने यात्रियों को नया ऑफर', ['यात्री लिस्ट', 'कैंपेन', 'रिपोर्ट']),
 35: ('L', ['howwa'], '4 स्टेप: एक बार सेटअप, फिर आसान', ['कॉन्टैक्ट › टेम्पलेट', 'कैंपेन › रिपोर्ट', 'नंबर सुरक्षित रखने के नियम']),
 36: ('R', ['seen'], 'किसने पढ़ा, उसे तुरंत जवाब', ['पढ़ने वाले किसान', 'फ़्री में जवाब', 'भरोसेमंद रिश्ता']),
 37: ('L', ['excel'], 'टैग से ग्रुप: सही ग्राहक, सही ऑफर', ['Excel में टैग कॉलम', 'हर ग्रुप अलग लिस्ट', 'ग्रुप को अलग कैंपेन']),
 38: ('R', ['reports'], 'भेजा, पहुँचा, पढ़ा: सब दिखे', ['डिलीवरी रिपोर्ट', 'STOP अपने-आप', 'अभी या बाद में भेजें']),
 39: ('D', ['campaign', 'tour'], 'धनतेरस ऑफर, पहले से हर फ़ोन पर', ['कैंपेन', 'ऑफर मैसेज', 'सबको']),
 40: ('D', ['hero', 'wahome'], 'पोस्ट + WhatsApp: एक प्लेटफ़ॉर्म', ['सोशल पोस्ट', 'WhatsApp', 'एक जगह']),
 41: ('L', ['chat'], 'मरीज़ से प्यार भरी बातचीत', ['सवाल का तुरंत जवाब', 'क्विक रिप्लाई', 'ज़रूरत हो तो कॉल']),
 42: ('R', ['login'], 'आसान शुरुआत, मोबाइल पर भी', ['ईमेल से लॉगिन', 'बिज़नेस का नाम डालें', 'मुफ़्त अकाउंट बनाएँ']),
 43: ('D', ['own', 'history2'], 'नया कलेक्शन, नई पोस्ट', ['फ़ोटो', 'कैप्शन', 'हिस्ट्री']),
 44: ('L', ['pages'], 'आपका FB और Instagram जुड़ा', ['पेज एक बार जुड़े', 'फिर हर पोस्ट एक क्लिक', 'WhatsApp भी साथ']),
 45: ('R', ['tour2'], 'रिपोर्ट और सुरक्षा, अपने-आप', ['डिलीवर और रीड रिपोर्ट', 'STOP / अनसब्सक्राइब अपने-आप', 'पूरे साल लगातार प्रचार']),
}

def shot_card(img, key, x, y, w, maxh, rot=0):
    """screenshot inside a phone-style frame; returns drawn height"""
    f, y0, y1 = SHOT[key]
    sc = Image.open(SCR + f).convert('RGB').crop((0, y0, 780, y1))
    bez_ = 12
    iw = w - 2 * bez_
    ih = sc.height * iw / sc.width
    if ih + 2 * bez_ > maxh:
        ih = maxh - 2 * bez_; iw = sc.width * ih / sc.height
    fw, fh = iw + 2 * bez_, ih + 2 * bez_
    card = Image.new('RGBA', (int(fw * S), int(fh * S)), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, card.width - 1, card.height - 1), int(30 * S), fill=(18, 30, 22, 255))
    s2 = sc.resize((int(iw * S), int(ih * S)), Image.LANCZOS)
    m = Image.new('L', s2.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s2.width - 1, s2.height - 1), int(20 * S), fill=255)
    card.paste(s2, (int(bez_ * S), int(bez_ * S)), m)
    sh = Image.new('L', card.size, 0)
    ImageDraw.Draw(sh).polygon([(0, 0), (card.width * 0.6, 0), (0, card.height * 0.45)], fill=34)
    sh = ImageChops.multiply(sh.filter(ImageFilter.GaussianBlur(12 * S)), card.getchannel('A'))
    card.paste(Image.new('RGBA', card.size, (255, 255, 255, 255)), (0, 0), sh)
    if rot: card = card.rotate(rot, resample=Image.BICUBIC, expand=True)
    px = int((x + (w - fw) / 2) * S - (card.width - fw * S) / 2); py = int(y * S - (card.height - fh * S) / 2)
    PAD = int(40 * S)
    a = Image.new('L', (card.width + 2 * PAD, card.height + 2 * PAD), 0); a.paste(card.getchannel('A'), (PAD, PAD))
    a = a.filter(ImageFilter.GaussianBlur(14 * S)).point(lambda v: int(v * 0.32))
    img.paste(Image.new('RGB', a.size, DEEP), (px - PAD, py - PAD + int(12 * S)), a)
    img.paste(card, (px, py), card)
    return fh

def feature_points(img, x, y, title, pts, maxw):
    lab = 'Shri Tech फ़ीचर'
    w = tw(lab, 19, PB) + 34
    grrect(img, (x, y, x + w, y + 38), 19, (254, 240, 138), (234, 179, 8), 0.3)
    text(img, (x + w / 2, y + 19), lab, 19, DEEP, PB, 'mm')
    y += 70
    s = 34
    for ln_ in _wrap(title, s, PB, maxw):
        grad_text(img, (x, y), ln_, s, (21, 128, 61), (6, 52, 28), PB, 'lm', gloss=False); y += s * 1.25
    y += 14
    for p in pts:
        gellipse(img, x + 17, y, 17, 17, (74, 222, 128), (21, 128, 61), 0.3)
        ImageDraw.Draw(img).line(P((x + 9, y), (x + 15, y + 7), (x + 26, y - 7)), fill=WHITE, width=int(4 * S), joint='curve')
        text(img, (x + 48, y + 1), p, fit(p, 26, PBD, maxw - 50), (30, 50, 38), PBD, 'lm'); y += 54
    return y

def _wrap(txt, size, path, maxw):
    out, cur = [], ''
    for w in txt.split(' '):
        t = (cur + ' ' + w).strip()
        if tw(t, size, path) <= maxw or not cur: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def showcase(img, n):
    style, shots, title, pts = FEAT[n]
    top, bot = 662, 1086
    if style in ('L', 'R'):
        sw = 330
        sx = M if style == 'L' else 1080 - M - sw
        shot_card(img, shots[0], sx, top, sw, bot - top)
        tx = M + sw + 40 if style == 'L' else M
        feature_points(img, tx, top + 14, title, pts, 1080 - 2 * M - sw - 40)
    else:
        # two screens, slightly tilted, with numbered step chips under the title
        segs = _wrap(title, 32, PB, 980)
        grad_text(img, (540, top + 22), segs[0], fit(segs[0], 32, PB, 980), (21, 128, 61), (6, 52, 28), PB, 'mm', gloss=False)
        sw = 300
        shot_card(img, shots[0], 120, top + 56, sw, bot - top - 60, rot=4)
        shot_card(img, shots[1], 660, top + 56, sw, bot - top - 60, rot=-4)
        # centre steps
        for i, p in enumerate(pts):
            cy = top + 130 + i * 110
            gellipse(img, 540, cy, 34, 34, (254, 240, 138), (217, 159, 6), 0.35)
            text(img, (540, cy + 1), str(i + 1), 30, DEEP, PB, 'mm')
            text(img, (540, cy + 52), p, fit(p, 20, PBD, 200), DEEP, PBD, 'mm')

PATH = dict(hero='Home', how='Home', flow='Home', reports='WhatsApp', login='Login', dash='Home', dash2='Home',
            form='Create › New image', brand='Create › New image', own='Create › Existing image', review='Create › Approve and post',
            history='History', history2='History', pages='Account', tour='WhatsApp', tour2='WhatsApp', wahome='WhatsApp › Home',
            wachart='WhatsApp › Home', excel='WhatsApp › Contacts', contacts='WhatsApp › Contacts', templates='WhatsApp › Templates',
            newtmpl='WhatsApp › Templates', campaign='WhatsApp › Campaigns', campstat='WhatsApp › Campaigns', inbox='WhatsApp › Chat',
            chat='WhatsApp › Chat', seen='WhatsApp › Chat › Seen and liked', howwa='WhatsApp › Help', safe='WhatsApp › Help')

_show0 = showcase
def showcase(img, n):
    _show0(img, n)
    style, shots, title, pts = FEAT[n]
    if style in ('L', 'R'):
        sw = 330
        x = M + sw + 40 if style == 'L' else M
        w = 1080 - 2 * M - sw - 40
        y = 1018
        lab = 'कहाँ मिलेगा:'; pth = PATH[shots[0]]
        gloss.grrect(img, (x, y, x + w, y + 56), 28, (255, 255, 255), (236, 252, 243), 0)
        rrect(img, (x, y, x + w, y + 56), 28, outline=(134, 199, 157), width=2)
        text(img, (x + 24, y + 28), lab, 21, (180, 120, 5), PBD, 'lm')
        lw = tw(lab, 21, PBD)
        text(img, (x + 34 + lw, y + 28), pth, fit(pth, 21, PB, w - lw - 60), DEEP, PB, 'lm')
