// Demo mode: realistic sample data kept in memory only. Never touches the live system — safe for client demos.
import type { Media, Post, Rule, LogItem } from './types';
const DAY = 86400000;
const OFF = 330 * 60000;
const at = (days: number, hh: number, mm = 0) => { const n = new Date(Date.now() + OFF); return new Date(Date.UTC(n.getUTCFullYear(), n.getUTCMonth(), n.getUTCDate() + days, hh, mm) - OFF).toISOString(); };
const IMGS = [require('../assets/demo/img0.jpg'), require('../assets/demo/img1.jpg'), require('../assets/demo/img2.jpg'), require('../assets/demo/img3.jpg'), require('../assets/demo/img4.jpg'), require('../assets/demo/img5.jpg')];
const REELS = [require('../assets/demo/reel0.jpg'), require('../assets/demo/reel1.jpg'), require('../assets/demo/reel2.jpg'), require('../assets/demo/reel3.jpg'), require('../assets/demo/reel4.jpg')];
const IMG = (_: number) => 'demo://local';
let ri = 0, ii = 0;
let mid = 0, pid = 0, rid = 0;
const M = (kind: 'video' | 'image', title: string, seed: number): Media => ({ id: 'm' + ++mid, kind, title, public_url: IMG(seed), created_at: new Date(Date.now() - seed * 3600000).toISOString(), ...(kind === 'image' ? { local: IMGS[ii++ % IMGS.length] } : { poster: REELS[ri++ % REELS.length] }) });

const media: Media[] = [
  M('video', 'Wedding web invitation reel', 3), M('video', '90% businesses skip ads', 7), M('image', 'Auto posting for shops', 11),
  M('video', 'Business ka hero reel', 15), M('image', 'Bulk WhatsApp offer poster', 19), M('video', 'New Year reel – funny', 23),
  M('image', 'Website for your business', 27), M('video', 'English invitation reel', 31), M('image', 'Lead generation post', 35),
];
const CAP = 'नया ऑफ़र आ गया है! 🎉 आज ही विज़िट करें।\n📞 9993615146\n#ShriTech #SmallBusiness';
const P = (m: Media, when: string, status: Post['status'], extra: Partial<Post> = {}): Post => ({
  id: 'p' + ++pid, title: m.title, caption: CAP, scheduled_at: when, status, platforms: ['facebook', 'instagram'], media: m, media_id: m.id,
  collaborators: ['shreebalaji.digital_'], fb_status: status === 'posted' ? 'posted' : null, ig_status: status === 'posted' ? 'posted' : null,
  fb_link: status === 'posted' ? 'https://facebook.com' : null, ig_link: status === 'posted' ? 'https://instagram.com' : null, ...extra,
});
let posts: Post[] = [
  P(media[0], at(-9, 18), 'posted'), P(media[2], at(-7, 17, 30), 'posted'), P(media[1], at(-5, 19), 'posted'),
  P(media[6], at(-3, 17, 30), 'failed', { error: 'Instagram is busy right now', fb_status: 'posted', ig_status: 'failed' }),
  P(media[3], at(-1, 18), 'posted'), P(media[4], at(0, 21), 'scheduled'), P(media[5], at(2, 18), 'scheduled'), P(media[7], at(4, 18), 'scheduled'),
  P(media[8], at(6, 17, 30), 'scheduled'), P(media[0], at(9, 18), 'scheduled'), P(media[1], at(13, 18), 'scheduled'), P(media[2], at(17, 17, 30), 'scheduled'),
  P(media[5], at(22, 18), 'scheduled'), P(media[3], at(27, 18), 'scheduled'), P(media[6], at(33, 17, 30), 'scheduled'), P(media[7], at(38, 18), 'scheduled'),
];
let rules: Rule[] = [
  { id: 'r' + ++rid, platform: 'instagram', trigger: 'comment', keywords: ['price', 'details', 'info'], message: 'नमस्ते! 🙏 हमारी सर्विस की पूरी जानकारी यहाँ है। कॉल करें: 9993615146', reply_public: true, public_reply: 'आपको DM भेज दिया है ✅', active: true, active_till: null },
  { id: 'r' + ++rid, platform: 'instagram', trigger: 'comment', keywords: ['demo'], message: 'Demo के लिए यह लिंक खोलें, हम आपको कॉल करेंगे।', reply_public: true, public_reply: null, active: false, active_till: null },
  { id: 'r' + ++rid, platform: 'facebook', trigger: 'comment', keywords: ['offer'], message: 'आज का ऑफ़र आपके इनबॉक्स में भेज दिया है 🎁', reply_public: true, public_reply: null, active: true, active_till: null },
  { id: 'r' + ++rid, platform: 'instagram', trigger: 'story', keywords: [], message: 'Story पर reply के लिए धन्यवाद! 💚 हम जल्दी संपर्क करेंगे।', reply_public: false, public_reply: null, active: true, active_till: null, story_mentions: true },
];
const names = ['rahul.sweets', 'priya_boutique', 'fitzone.indore', 'gupta_store', 'cafe.aroma', 'royal.jewels'];
const log: LogItem[] = names.map((n, i) => ({ id: 'l' + i, platform: i % 3 === 2 ? 'facebook' : 'instagram', from_username: n, comment_text: ['Price?', 'details please', 'info', 'offer?', 'Price kya hai', 'details'][i], matched: ['price', 'details', 'info', 'offer', 'price', 'details'][i], dm_status: 'sent', public_status: i === 3 ? 'off' : 'sent', created_at: new Date(Date.now() - (i + 1) * 5400000).toISOString() }));
const wait = (ms = 350) => new Promise((r) => setTimeout(r, ms));

export async function demoApi(action: string, d: any): Promise<any> {
  await wait();
  switch (action) {
    case 'get_settings': return { page_name: 'Shree Balaji Digital (Demo)', ig_username: 'shritech.demo', token_saved: true, default_caption: '#ShriTech 📞 9993615146' };
    case 'overview': {
      const f = new Date(d.from ?? Date.now() - 30 * DAY).getTime(), t = new Date(d.to ?? Date.now() + 31 * DAY).getTime();
      const list = posts.filter((p) => { const x = new Date(p.scheduled_at).getTime(); return x >= f && x <= t; }).sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at));
      const up = posts.filter((p) => p.status === 'scheduled');
      return { posts: list, now: new Date().toISOString(), upcoming: up.length, last_at: up.map((p) => p.scheduled_at).sort().pop() ?? null };
    }
    case 'list_media': return [...media].sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)));
    case 'register_media': { const m: Media = { id: 'm' + ++mid, kind: d.kind, title: d.title, public_url: d.demo_uri ?? IMG(mid), created_at: new Date().toISOString(), ...(d.kind === 'image' && d.demo_uri ? { local: { uri: d.demo_uri } } : {}) }; media.unshift(m); return m; }
    case 'delete_media': { if (posts.some((p) => p.media_id === d.id && p.status === 'scheduled')) throw new Error('This file is used in a scheduled post, so it can’t be removed.'); const i = media.findIndex((m) => m.id === d.id); if (i >= 0) media.splice(i, 1); return { ok: true }; }
    case 'create_post': { const m = media.find((x) => x.id === d.media_id) ?? null; const p: Post = { id: 'p' + ++pid, title: d.title || m?.title || 'Post', caption: d.caption ?? '', scheduled_at: d.scheduled_at, status: 'scheduled', platforms: d.platforms, collaborators: d.collaborators ?? [], media: m, media_id: d.media_id }; posts.push(p); return p; }
    case 'update_post': { const p = posts.find((x) => x.id === d.id); if (p && p.status === 'scheduled') Object.assign(p, Object.fromEntries(Object.entries(d).filter(([k]) => k !== 'id' && k !== 'action'))); return { ok: true }; }
    case 'cancel_post': { const p = posts.find((x) => x.id === d.id); if (p && p.status === 'scheduled') p.status = 'cancelled'; return { ok: true }; }
    case 'post_now': { const p = posts.find((x) => x.id === d.id); if (p) Object.assign(p, { status: 'posted', scheduled_at: new Date().toISOString(), fb_status: 'posted', ig_status: 'posted', fb_link: 'https://facebook.com', ig_link: 'https://instagram.com' }); return { log: [] }; }
    case 'retry_post': { const p = posts.find((x) => x.id === d.id); if (p) Object.assign(p, { status: 'scheduled', error: null, scheduled_at: new Date(Date.now() + 120000).toISOString() }); return { ok: true }; }
    case 'list_rules': return rules.filter((r) => r.platform === d.platform && r.trigger === (d.trigger === 'story' ? 'story' : 'comment'));
    case 'save_rule': { if (d.id) { const r = rules.find((x) => x.id === d.id); if (r) Object.assign(r, d); return r; } const r = { ...d, id: 'r' + ++rid } as Rule; rules.unshift(r); return r; }
    case 'toggle_rule': { const r = rules.find((x) => x.id === d.id); if (r) r.active = !!d.active; return { ok: true }; }
    case 'delete_rule': rules = rules.filter((r) => r.id !== d.id); return { ok: true };
    case 'comment_log': return log.filter((l) => l.platform === d.platform);
    case 'test_connection': return { facebook: '✅ Page: Shree Balaji Digital (Demo)', instagram: '✅ @shritech.demo' };
    case 'change_password': case 'logout': return { ok: true };
    default: return {};
  }
}
