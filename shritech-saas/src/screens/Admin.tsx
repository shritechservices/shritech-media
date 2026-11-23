import React, { useCallback, useEffect, useState } from 'react';
import { Linking, Platform, Share, View, Switch } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { Btn, Card, CountUp, Empty, Field, Hero, Logo, Pill, PlatformIcons, Press, Rise, Screen, Seg, SectionTitle, Skel, T, Thumb, useConfirm, useStatus, useToast, useWide } from '../ui';
import { ThemePref, useTheme } from '../theme';
import { api } from '../api';
import { dateStr, timeStr } from '../time';

const STATUS = ['pending', 'active', 'paused', 'closed'] as const;

/** Copy text (web) or open the share sheet (phone) so it can be sent on WhatsApp. */
async function copyOrShare(text: string): Promise<'copied' | 'shared'> {
  if (Platform.OS === 'web' && typeof navigator !== 'undefined' && (navigator as any).clipboard) { await (navigator as any).clipboard.writeText(text); return 'copied'; }
  await Share.share({ message: text }); return 'shared';
}
const CLIENT_GH_STEPS = (biz: string) => `Hello${biz ? ' ' + biz : ''} 🙏
To store your reels & images safely in your own free GitHub space, please do this once (about 5 minutes):

1️⃣ Go to https://github.com/signup and create a free account (or log in).
2️⃣ Click the + (top right) → "New repository".
   • Name: ${biz ? biz.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') + '-media' : 'yourbusiness-media'}
   • Choose "Public"  ✅ (needed so Facebook & Instagram can fetch your videos)
   • Tick "Add a README file"  → click "Create repository"
3️⃣ In that repository: Settings → Collaborators → "Add people" → type  shritechservices  → "Add to repository".
4️⃣ Send us your repository name on WhatsApp, like:  yourusername/yourbusiness-media

That's all — ShriTech will do the rest. 📞 99936 15146`;
const GH_STATUS: Record<string, { l: string; i: any }> = { ok: { l: 'CONNECTED', i: 'checkmark-circle' }, waiting: { l: 'WAITING FOR INVITE', i: 'time' }, error: { l: 'PROBLEM', i: 'alert-circle' } };

function Steps({ title, steps }: { title: string; steps: string[] }) {
  const { t } = useTheme();
  return (
    <View style={{ backgroundColor: t.card2, borderRadius: 14, padding: 12, gap: 8, borderWidth: 1, borderColor: t.line }}>
      <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}><Ionicons name="list-circle-outline" size={18} color={t.green} /><T w="b" size={13}>{title}</T></View>
      {steps.map((x, i) => (
        <View key={i} style={{ flexDirection: 'row', gap: 8 }}>
          <View style={{ width: 20, height: 20, borderRadius: 10, backgroundColor: t.chip, alignItems: 'center', justifyContent: 'center' }}><T w="b" size={11} c={t.green}>{i + 1}</T></View>
          <T size={12} style={{ flex: 1, lineHeight: 18 }}>{x}</T>
        </View>
      ))}
    </View>
  );
}
function useStatusColors() { const { t } = useTheme(); return (s: string) => (({ active: [t.green, t.chip, 'Active'], pending: [t.gold, t.goldSoft, 'Pending'], paused: [t.red, t.redSoft, 'Paused'], closed: [t.mut, t.card2, 'Closed'] } as any)[s] ?? [t.mut, t.card2, s]); }

// ================= Dashboard + business list =================
export function AdminHome({ navigation }: any) {
  const { t } = useTheme(); const sc = useStatusColors(); const wide = useWide();
  const [ov, setOv] = useState<any>(null); const [list, setList] = useState<any[]>([]); const [loading, setLoading] = useState(true); const [ref, setRef] = useState(false);
  const [filter, setFilter] = useState<'all' | 'pending' | 'active' | 'paused'>('all'); const [q, setQ] = useState('');
  const load = useCallback(async (pull = false) => { if (pull) setRef(true); try { const [o, l] = await Promise.all([api('admin_overview'), api<any[]>('admin_tenants')]); setOv(o); setList(l); } catch { } finally { setLoading(false); setRef(false); } }, []);
  useFocusEffect(useCallback(() => { load(); }, [load]));
  const shown = list.filter((x) => (filter === 'all' || x.status === filter) && (!q || (x.name + ' ' + x.users.map((u: any) => u.email).join(' ') + ' ' + (x.page_name ?? '')).toLowerCase().includes(q.toLowerCase())));
  const stats = ov ? [
    { n: ov.tenants, l: 'Businesses', i: 'storefront' as const, c: t.green, bg: t.chip },
    { n: ov.by_status?.pending ?? 0, l: 'Waiting setup', i: 'construct' as const, c: t.gold, bg: t.goldSoft },
    { n: ov.scheduled, l: 'Scheduled', i: 'calendar' as const, c: t.blue, bg: t.blueSoft },
    { n: ov.failed_30d, l: 'Not posted', i: 'alert-circle' as const, c: t.red, bg: t.redSoft },
  ] : [];
  return (
    <Screen onRefresh={() => load(true)} refreshing={ref} header={
      <Hero>
        <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', display: wide ? 'none' : 'flex' }}>
          <Logo size={26} light />
          <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}>
            <Pill label="ADMIN" color="#2A2000" bg="#FACC15" icon="shield-checkmark" />
            <Press onPress={() => navigation.navigate('AdminSettings')} style={{ width: 40, height: 40, borderRadius: 20, backgroundColor: 'rgba(255,255,255,0.16)', alignItems: 'center', justifyContent: 'center' }}><Ionicons name="settings-outline" size={21} color="#fff" /></Press>
          </View>
        </View>
        <Rise i={1}><T w="b" size={24} c="#fff" style={{ marginTop: wide ? 0 : 16 }}>Control centre</T></Rise>
        <Rise i={2}><T size={13} c="rgba(255,255,255,0.85)">{ov ? `${ov.users} users · ${ov.posted_30d} posted in 30 days · temp storage ${ov.temp_storage_mb} MB` : 'Loading…'}</T></Rise>
      </Hero>
    }>
      {ov && !ov.email_ready ? (
        <Rise><Press onPress={() => navigation.navigate('AdminSettings')}><Card style={{ flexDirection: 'row', gap: 10, alignItems: 'center', borderColor: t.gold, borderWidth: 1.5 }}>
          <Ionicons name="mail-unread-outline" size={22} color={t.gold} /><T size={13} style={{ flex: 1 }}>Email codes haven’t been confirmed yet. Tap to send yourself a test code.</T><Ionicons name="chevron-forward" size={18} color={t.mut} />
        </Card></Press></Rise>
      ) : null}
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10 }}>
        {loading ? [0, 1, 2, 3].map((i) => <View key={i} style={{ width: '48%' }}><Skel h={96} /></View>) : stats.map((s, i) => (
          <Rise key={s.l} i={i} style={{ width: wide ? '23%' : '48%', flexGrow: 1 }}>
            <Card pad={12} style={{ gap: 4 }}>
              <View style={{ width: 34, height: 34, borderRadius: 12, backgroundColor: s.bg, alignItems: 'center', justifyContent: 'center' }}><Ionicons name={s.i} size={18} color={s.c} /></View>
              <CountUp to={s.n} size={26} c={s.c} /><T s="mut" size={12}>{s.l}</T>
            </Card>
          </Rise>
        ))}
      </View>
      <SectionTitle title="Businesses" action="+ Add business" onAction={() => navigation.navigate('AdminTenant', { tenant: null })} />
      <Field value={q} onChange={setQ} placeholder="Search name, email or page…" right={<Ionicons name="search" size={18} color={t.mut} />} />
      <Seg items={[{ v: 'all', label: 'All' }, { v: 'pending', label: 'Pending' }, { v: 'active', label: 'Active' }, { v: 'paused', label: 'Paused' }]} value={filter} onChange={setFilter} />
      {loading ? <Skel h={90} /> : shown.length === 0 ? <Card><Empty icon="storefront-outline" title="No businesses yet" sub="When someone signs up with their email, they appear here as Pending." /></Card> : <View style={wide ? { flexDirection: 'row', flexWrap: 'wrap', gap: 16 } : { gap: 14 }}>{shown.map((x, i) => {
        const [c, bg, l] = sc(x.status);
        return (
          <Rise key={x.id} i={i} style={wide ? { width: '48.5%' } : undefined}>
            <Press onPress={() => navigation.navigate('AdminTenant', { tenant: x })}>
              <Card pad={14} style={{ gap: 8 }}>
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
                  <View style={{ width: 42, height: 42, borderRadius: 14, backgroundColor: t.chip, alignItems: 'center', justifyContent: 'center' }}><T w="b" size={17} c={t.green}>{x.name[0]?.toUpperCase()}</T></View>
                  <View style={{ flex: 1 }}><T w="b" size={15} lines={1}>{x.name}</T><T s="mut" size={12} lines={1}>{x.users.map((u: any) => u.email).join(', ') || 'No users'}</T></View>
                  <Pill label={l} color={c} bg={bg} size={11} />
                </View>
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
                  <PlatformIcons list={['facebook', 'instagram']} />
                  <T size={12} s="mut" style={{ flex: 1 }} lines={1}>{x.token_saved ? `${x.page_name ?? x.page_id}${x.ig_username ? ' · @' + x.ig_username : ''}` : 'Not connected'}</T>
                  <T size={12} w="s" c={t.green}>{x.scheduled} scheduled</T>
                </View>
              </Card>
            </Press>
          </Rise>
        );
      })}</View>}
    </Screen>
  );
}

// ================= Business detail / setup =================
export function AdminTenant({ navigation, route }: any) {
  const { t } = useTheme(); const toast = useToast(); const stat = useStatus(); const sc = useStatusColors();
  const x = route.params?.tenant; const isNew = !x;
  const [f, setF] = useState<any>({ name: x?.name ?? '', status: x?.status ?? 'pending', plan: x?.plan ?? 'starter', post_quota: String(x?.post_quota ?? 60), valid_till: x?.valid_till ?? '', page_id: x?.page_id ?? '', ig_user_id: x?.ig_user_id ?? '', page_token: '', graph_version: x?.graph_version ?? 'v25.0', default_caption: x?.default_caption ?? '', admin_note: x?.admin_note ?? '', contact_phone: x?.contact_phone ?? '', owner_email: '' });
  const [id, setId] = useState<string | null>(x?.id ?? null); const [hint, setHint] = useState<string>(x?.token_hint ?? ''); const [test, setTest] = useState<any>(null);
  const [busy, setBusy] = useState(''); const [posts, setPosts] = useState<any[]>([]); const [users, setUsers] = useState<any[]>(x?.users ?? []); const [newU, setNewU] = useState('');
  const [ghs, setGhs] = useState<any>({ gh_repo: x?.gh_repo ?? null, gh_branch: x?.gh_branch ?? null, gh_status: x?.gh_status ?? null, gh_note: x?.gh_note ?? null, gh_checked_at: x?.gh_checked_at ?? null });
  const [ghRepo, setGhRepo] = useState<string>(x?.gh_repo ?? ''); const [ghBranch, setGhBranch] = useState<string>(x?.gh_branch ?? '');
  const ghCheck = async () => { if (!id) return; setBusy('gh'); try { const r = await api<any>('admin_tenant_github', { id, repo: ghRepo, branch: ghBranch }); setGhs(r); setGhRepo(r.gh_repo ?? ghRepo); setGhBranch(r.gh_branch ?? ''); toast(r.gh_status === 'ok' ? 'GitHub storage connected ✅' : r.gh_status === 'waiting' ? 'Waiting for the client’s invite' : 'Please check the note below', r.gh_status === 'ok'); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const ghClear = async () => { if (!id) return; setBusy('ghc'); try { const r = await api<any>('admin_tenant_github_clear', { id }); setGhs(r); setGhRepo(''); setGhBranch(''); toast('Now using ShriTech storage'); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const ghShare = async () => { try { const how = await copyOrShare(CLIENT_GH_STEPS(f.name)); if (how === 'copied') toast('Steps copied — paste them in WhatsApp'); } catch { } };
  const set = (k: string) => (v: string) => setF((o: any) => ({ ...o, [k]: v }));
  useEffect(() => { if (id) api<any[]>('admin_tenant_posts', { id }).then(setPosts).catch(() => {}); }, [id]);
  const save = async (extra: any = {}) => {
    setBusy('save');
    try {
      const r = await api<any>('admin_tenant_save', { id, ...f, ...extra, owner_email: isNew ? f.owner_email : undefined });
      setId(r.id); setHint(r.token_hint); setF((o: any) => ({ ...o, page_token: '', status: r.status }));
      if (isNew && f.owner_email) setUsers([{ email: f.owner_email.trim().toLowerCase(), role: 'owner', active: true }]);
      toast('Saved ✅');
    } catch (e: any) { toast(e.message, false); } finally { setBusy(''); }
  };
  const runTest = async () => {
    if (f.page_token || f.page_id !== (x?.page_id ?? '')) await save();
    setBusy('test'); setTest(null);
    try { const r = await api<any>('admin_tenant_test', { id }); setTest(r); if (r.page_name) setF((o: any) => ({ ...o })); toast(r.facebook ? 'Connection checked' : 'Not connected yet', !!r.facebook); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); }
  };
  const addUser = async () => { try { const u = await api<any>('admin_user_save', { email: newU, tenant_id: id, role: users.length ? 'member' : 'owner' }); setUsers((o) => [...o.filter((y) => y.email !== u.email), u]); setNewU(''); toast('User added'); } catch (e: any) { toast(e.message, false); } };
  const toggleUser = async (u: any) => { try { const r = await api<any>('admin_user_save', { email: u.email, tenant_id: id, role: u.role, active: !u.active }); setUsers((o) => o.map((y) => (y.email === r.email ? r : y))); } catch (e: any) { toast(e.message, false); } };
  return (
    <Screen narrow header={
      <Hero>
        <Press onPress={() => navigation.goBack()} style={{ marginBottom: 8 }}><Ionicons name="arrow-back" size={24} color="#fff" /></Press>
        <T w="b" size={24} c="#fff">{isNew && !id ? 'Add business' : f.name || 'Business'}</T>
        {x?.request_note ? <T size={13} c="rgba(255,255,255,0.9)">Customer sent: {x.request_note.replace(/\n/g, ' · ')}</T> : null}
        {x?.contact_phone ? <Press onPress={() => Linking.openURL('https://wa.me/91' + x.contact_phone.replace(/\D/g, '').slice(-10))}><T w="s" size={13} c="#FACC15">📞 {x.contact_phone} · WhatsApp</T></Press> : null}
      </Hero>
    }>
      <Rise>
        <Card style={{ gap: 12 }}>
          <T w="b" size={16}>Account & plan</T>
          <Field label="Business name" value={f.name} onChange={set('name')} />
          {isNew && !id ? <Field label="Owner email (they log in with it)" value={f.owner_email} onChange={set('owner_email')} keyboard="email-address" /> : null}
          <T s="mut" size={13} w="m">Status</T>
          <View style={{ flexDirection: 'row', gap: 8, flexWrap: 'wrap' }}>
            {STATUS.map((s) => { const [c, bg, l] = sc(s); const on = f.status === s; return <Press key={s} onPress={() => set('status')(s)} style={{ paddingHorizontal: 14, paddingVertical: 8, borderRadius: 99, backgroundColor: on ? c : bg, borderWidth: 1, borderColor: c }}><T w="s" size={13} c={on ? '#fff' : c}>{l}</T></Press>; })}
          </View>
          <View style={{ flexDirection: 'row', gap: 10 }}>
            <View style={{ flex: 1 }}><Field label="Plan" value={f.plan} onChange={set('plan')} placeholder="starter" /></View>
            <View style={{ flex: 1 }}><Field label="Posts / month (0 = no limit)" value={f.post_quota} onChange={set('post_quota')} keyboard="number-pad" /></View>
          </View>
          <Field label="Valid till (YYYY-MM-DD, empty = no end)" value={f.valid_till} onChange={set('valid_till')} placeholder="2027-12-31" />
          <Field label="Contact phone" value={f.contact_phone} onChange={set('contact_phone')} keyboard="phone-pad" />
          <Field label="Private note (only admin sees)" value={f.admin_note} onChange={set('admin_note')} multiline />
        </Card>
      </Rise>
      <Rise i={1}>
        <Card style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}><T w="b" size={16}>Facebook + Instagram setup</T><PlatformIcons list={['facebook', 'instagram']} size={20} /></View>
          <Field label="Facebook Page ID" value={f.page_id} onChange={set('page_id')} keyboard="number-pad" placeholder="e.g. 104229451876137" />
          <Field label={`Page access token ${hint ? '(saved ' + hint + ')' : ''}`} value={f.page_token} onChange={set('page_token')} secure placeholder={hint ? 'Leave empty to keep the saved token' : 'Paste the Page token'} />
          <Field label="Instagram Business ID (auto-detected on check)" value={f.ig_user_id} onChange={set('ig_user_id')} keyboard="number-pad" />
          <View style={{ flexDirection: 'row', gap: 10 }}>
            <View style={{ flex: 1 }}><Field label="Graph API version" value={f.graph_version} onChange={set('graph_version')} /></View>
          </View>
          <Field label="Default caption / hashtags" value={f.default_caption} onChange={set('default_caption')} multiline />
          {test ? (
            <View style={{ gap: 6, backgroundColor: t.card2, borderRadius: 14, padding: 12 }}>
              <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}><Ionicons name={test.facebook ? 'checkmark-circle' : 'close-circle'} size={20} color={test.facebook ? t.green : t.red} /><T size={13}>Facebook {test.page_name ? '· ' + test.page_name : ''}</T></View>
              <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}><Ionicons name={test.instagram ? 'checkmark-circle' : 'close-circle'} size={20} color={test.instagram ? t.green : t.red} /><T size={13}>Instagram {test.ig_username ? '· @' + test.ig_username : ''}</T></View>
              {test.message ? <T s="mut" size={12}>{test.message}</T> : null}
            </View>
          ) : null}
          <View style={{ flexDirection: 'row', gap: 10 }}>
            <Btn title="Save" icon="save-outline" onPress={() => save()} loading={busy === 'save'} style={{ flex: 1 }} />
            <Btn title="Check" icon="pulse" kind="outline" onPress={runTest} loading={busy === 'test'} disabled={!id} style={{ flex: 1 }} />
          </View>
          {id && f.status !== 'active' ? <Btn title="Activate business" kind="gold" icon="rocket-outline" onPress={() => { set('status')('active'); save({ status: 'active' }); }} /> : null}
        </Card>
      </Rise>
      {id ? (
        <Rise i={2}>
          <Card style={{ gap: 12 }}>
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: 8 }}>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}><Ionicons name="logo-github" size={20} color={t.text} /><T w="b" size={16}>Storage (GitHub)</T></View>
              {ghs.gh_status && GH_STATUS[ghs.gh_status] ? <Pill label={GH_STATUS[ghs.gh_status].l} icon={GH_STATUS[ghs.gh_status].i} color={ghs.gh_status === 'ok' ? t.green : ghs.gh_status === 'waiting' ? t.gold : t.red} bg={ghs.gh_status === 'ok' ? t.chip : ghs.gh_status === 'waiting' ? t.goldSoft : t.redSoft} /> : <Pill label="SHRITECH STORAGE" color={t.mut} bg={t.card2} />}
            </View>
            <T s="mut" size={12}>{ghs.gh_status === 'ok' ? 'New reels and images of this business are saved in their own GitHub repository.' : 'Until connected, this business’s files are saved in ShriTech storage. Posting works either way.'}</T>
            <Field label="Client repository (username/repository-name)" value={ghRepo} onChange={setGhRepo} placeholder="e.g. guptastore/guptastore-media" />
            <Field label="Branch (leave empty for default)" value={ghBranch} onChange={setGhBranch} placeholder="main" />
            {ghs.gh_note ? (
              <View style={{ flexDirection: 'row', gap: 8, backgroundColor: ghs.gh_status === 'ok' ? t.chip : ghs.gh_status === 'waiting' ? t.goldSoft : t.redSoft, borderRadius: 12, padding: 10 }}>
                <Ionicons name={GH_STATUS[ghs.gh_status]?.i ?? 'information-circle'} size={18} color={ghs.gh_status === 'ok' ? t.green : ghs.gh_status === 'waiting' ? t.gold : t.red} />
                <View style={{ flex: 1 }}><T size={12}>{ghs.gh_note}</T>{ghs.gh_checked_at ? <T s="mut" size={11}>Checked {dateStr(ghs.gh_checked_at, true)} · {timeStr(ghs.gh_checked_at)}</T> : null}</View>
              </View>
            ) : null}
            <View style={{ flexDirection: 'row', gap: 10, flexWrap: 'wrap' }}>
              <Btn title="Check & connect" icon="git-network-outline" onPress={ghCheck} loading={busy === 'gh'} disabled={!ghRepo.trim()} style={{ flex: 1, minWidth: 240 }} />
              {ghs.gh_repo ? <Btn title="Use ShriTech storage" kind="outline" icon="arrow-undo-outline" onPress={ghClear} loading={busy === 'ghc'} style={{ flex: 1, minWidth: 240 }} /> : null}
            </View>
            <Steps title="What the client does (once)" steps={[
              'Create a free account at github.com/signup (or log in).',
              'Click + (top right) → New repository → give a name like “shopname-media” → choose PUBLIC → tick “Add a README file” → Create repository.',
              'In that repository: Settings → Collaborators → Add people → type  shritechservices  → Add.',
              'Send you the repository name on WhatsApp, e.g.  username/shopname-media.',
            ]} />
            <Btn small kind="outline" icon={Platform.OS === 'web' ? 'copy-outline' : 'share-social-outline'} title={Platform.OS === 'web' ? 'Copy steps for client (WhatsApp)' : 'Send steps to client'} onPress={ghShare} />
            <Steps title="What you do after they send the name" steps={[
              'Paste the repository name above (a full github.com link also works).',
              'Tap “Check & connect” — it accepts the invite and tests saving a file automatically.',
              'Green CONNECTED = done. Yellow WAITING = the client hasn’t added shritechservices yet. Red = read the note (usually: repository must be Public).',
            ]} />
          </Card>
        </Rise>
      ) : null}
      {id ? (
        <Rise i={3}>
          <Card style={{ gap: 10 }}>
            <T w="b" size={16}>Users</T>
            {users.map((u) => (
              <View key={u.email} style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
                <Ionicons name={u.role === 'owner' ? 'person' : 'people-outline'} size={18} color={t.green} />
                <View style={{ flex: 1 }}><T size={13} lines={1}>{u.email}</T><T s="mut" size={11}>{u.role}</T></View>
                <Switch value={u.active !== false} onValueChange={() => toggleUser(u)} trackColor={{ true: t.green, false: t.line }} thumbColor="#fff" />
              </View>
            ))}
            <Field value={newU} onChange={setNewU} placeholder="Add user email" keyboard="email-address" right={<Press onPress={addUser}><Ionicons name="person-add" size={22} color={t.green} /></Press>} />
          </Card>
        </Rise>
      ) : null}
      {id ? (
        <>
          <SectionTitle title="Recent posts" />
          {posts.length === 0 ? <Card><Empty icon="calendar-clear-outline" title="No posts yet" /></Card> : posts.slice(0, 20).map((p, i) => { const s = stat(p.status); return (
            <Rise key={p.id} i={i % 6}>
              <Card pad={10} style={{ flexDirection: 'row', gap: 10, alignItems: 'center' }}>
                <Thumb m={p.media} w={46} h={60} />
                <View style={{ flex: 1, gap: 3 }}>
                  <T w="s" size={13} lines={1}>{p.title || p.media?.title || 'Post'}</T>
                  <T s="mut" size={11}>{dateStr(p.scheduled_at, true)} · {timeStr(p.scheduled_at)}</T>
                  {p.error ? <T size={11} c={t.red} lines={2}>{p.error}</T> : null}
                </View>
                <Pill label={s.label} color={s.c} bg={s.bg} size={10} />
              </Card>
            </Rise>
          ); })}
        </>
      ) : null}
    </Screen>
  );
}

// ================= Admin settings =================
export function AdminSettings({ navigation, onLogout }: any) {
  const wide = useWide();
  const { t, pref, setPref } = useTheme(); const toast = useToast(); const confirm = useConfirm();
  const [st, setSt] = useState<any>(null); const [codes, setCodes] = useState<any[]>([]);
  const [old, setOld] = useState(''); const [nw, setNw] = useState(''); const [busy, setBusy] = useState('');
  const [gh, setGh] = useState<any>(null); const [ghTok, setGhTok] = useState('');
  useEffect(() => { api<any>('admin_github_get').then(setGh).catch(() => {}); }, []);
  const [defRepo, setDefRepo] = useState(''); const [defNote, setDefNote] = useState<string | null>(null);
  const saveDef = async () => { setBusy('def'); setDefNote(null); try { const r = await api<any>('admin_github_default', { repo: defRepo }); if (r.ok) { setDefRepo(''); setGh(await api<any>('admin_github_get')); toast('Default storage updated ✅'); } else { setDefNote(r.note); toast('Not changed — see the note', false); } } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const resetDef = async () => { if (!(await confirm({ title: 'Use the built-in storage?', msg: 'New files of businesses without their own GitHub will go to shritechservices/shritech-media again.', ok: 'Yes, reset' }))) return; setBusy('defr'); try { await api('admin_github_default_clear'); setGh(await api<any>('admin_github_get')); toast('Back to built-in storage'); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const saveGh = async () => { setBusy('gh'); try { const r = await api<any>('admin_github_save', { token: ghTok }); setGhTok(''); setGh(await api<any>('admin_github_get')); toast(`GitHub key saved ✅ (${r.login})`); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const load = useCallback(async () => { try { const s = await api<any>('admin_settings_get'); setSt(s); setCodes(await api<any[]>('admin_codes')); } catch { } }, []);
  useFocusEffect(useCallback(() => { load(); const iv = setInterval(() => api<any[]>('admin_codes').then(setCodes).catch(() => {}), 8000); return () => clearInterval(iv); }, [load]));
  const testEmail = async () => { setBusy('test'); try { const r = await api<any>('admin_test_email'); toast(r.via === 'supabase' ? 'Test code sent — check your Gmail' : 'Supabase could not send the email. Check Auth email settings.', r.via === 'supabase'); load(); } catch { toast('Email could not be sent. Check the key and sender.', false); } finally { setBusy(''); } };
  const changePw = async () => { setBusy('pw'); try { await api('admin_change_password', { old, password: nw }); setOld(''); setNw(''); toast('Password changed'); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const out = async () => { if (await confirm({ title: 'Log out of admin?', ok: 'Log out' })) { try { await api('logout'); } catch { } onLogout(); } };
  return (
    <Screen narrow header={<Hero>{!wide ? <Press onPress={() => navigation.goBack()} style={{ marginBottom: 8 }}><Ionicons name="arrow-back" size={24} color="#fff" /></Press> : null}<T w="b" size={24} c="#fff">Admin settings</T></Hero>}>
      <Rise>
        <Card style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}><T w="b" size={16}>Login code emails</T>{st ? <Pill label={st.email_ready ? 'WORKING' : 'CHECK'} color={st.email_ready ? t.green : t.gold} bg={st.email_ready ? t.chip : t.goldSoft} /> : null}</View>
          <T s="mut" size={12}>Codes are sent by Supabase Auth (your project’s email settings). If Supabase can’t send, the code appears below so you can share it.</T>
          {st?.last_ok ? <T size={12}>Last email sent: {new Date(st.last_ok).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}</T> : null}
          <Btn title="Send me a test code" kind="outline" icon="mail-outline" onPress={testEmail} loading={busy === 'test'} />
        </Card>
      </Rise>
      <Rise i={1}>
        <Card style={{ gap: 10 }}>
          <T w="b" size={16}>Login codes waiting</T>
          <T s="mut" size={12}>Only shown while email is off. Read the code to the customer on call/WhatsApp.</T>
          {codes.length === 0 ? <T s="mut" size={13}>No codes right now.</T> : codes.map((c) => (
            <View key={c.email} style={{ flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: t.card2, borderRadius: 12, padding: 10 }}>
              <T size={13} style={{ flex: 1 }} lines={1}>{c.email}</T><T w="b" size={20} c={t.green} style={{ letterSpacing: 3 }}>{c.code_plain}</T>
            </View>
          ))}
        </Card>
      </Rise>
      <Rise i={2}>
        <Card style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}><Ionicons name="logo-github" size={20} color={t.text} /><T w="b" size={16}>GitHub key (client storage)</T></View>
            {gh ? <Pill label={gh.saved ? 'SAVED' : 'NOT SET'} color={gh.saved ? t.green : t.gold} bg={gh.saved ? t.chip : t.goldSoft} /> : null}
          </View>
          <T s="mut" size={12}>Used to connect each client’s own GitHub repository and save their reels there. Saved only on the server — never shown again.</T>
          {gh?.saved ? <T size={12}>Account: <T w="b" size={12}>{gh.login}</T> · key {gh.hint}{gh.saved_at ? ' · saved ' + dateStr(gh.saved_at, true) : ''}</T> : null}
          <Field label={gh?.saved ? 'Replace key (optional)' : 'Paste GitHub key'} value={ghTok} onChange={setGhTok} secure placeholder="ghp_…" />
          <Btn title="Save & check key" icon="key-outline" onPress={saveGh} loading={busy === 'gh'} disabled={ghTok.trim().length < 20} />
          <Steps title="How to make the key (once)" steps={[
            'Log in to GitHub as shritechservices → profile photo → Settings.',
            'Left menu (bottom): Developer settings → Personal access tokens → Tokens (classic).',
            'Generate new token → Generate new token (classic).',
            'Note: “ShriTech AutoPost” · Expiration: No expiration · tick the “repo” box.',
            'Click Generate token, copy it (starts with ghp_), paste it above and tap “Save & check key”.',
          ]} />
        </Card>
      </Rise>
      <Rise i={3}>
        <Card style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}><Ionicons name="server-outline" size={20} color={t.text} /><T w="b" size={16}>Default storage</T></View>
          <T s="mut" size={12}>Where new reels & images go for businesses that have NOT connected their own GitHub. Businesses with their own GitHub always use theirs.</T>
          <View style={{ backgroundColor: t.chip, borderRadius: 12, padding: 12, gap: 4 }}>
            <T s="mut" size={11}>Currently used</T>
            <T w="b" size={15} c={t.green}>{gh?.default_repo || 'shritechservices/shritech-media'}</T>
            <T s="mut" size={11}>{gh?.default_repo ? `branch ${gh.default_branch || 'main'}${gh.default_set_at ? ' · set ' + dateStr(gh.default_set_at, true) : ''}` : 'Built-in storage'}</T>
          </View>
          <Field label="Change to (username/repository-name)" value={defRepo} onChange={setDefRepo} placeholder="e.g. shritechservices/shritech-media-3" />
          {defNote ? <View style={{ backgroundColor: t.goldSoft, borderRadius: 12, padding: 10 }}><T size={12}>{defNote}</T></View> : null}
          <View style={{ flexDirection: 'row', gap: 10, flexWrap: 'wrap' }}>
            <Btn title="Check & set as default" icon="swap-horizontal-outline" onPress={saveDef} loading={busy === 'def'} disabled={!gh?.saved || defRepo.trim().length < 3} style={{ flex: 1, minWidth: 240 }} />
            {gh?.default_repo ? <Btn title="Reset to built-in" kind="outline" icon="arrow-undo-outline" onPress={resetDef} loading={busy === 'defr'} style={{ flex: 1, minWidth: 240 }} /> : null}
          </View>
          <Steps title="When a storage repository gets full (~1–2 GB)" steps={[
            'On GitHub (shritechservices): + → New repository → name like shritech-media-3 → Public → tick “Add a README file” → Create.',
            'Come here, type  shritechservices/shritech-media-3  above and tap “Check & set as default”.',
            'For your own business: Businesses → Shri Balaji Digital → Storage (GitHub) → enter the same name → Check & connect.',
            'Old files stay where they are and keep working — only new uploads go to the new repository.',
          ]} />
        </Card>
      </Rise>
      <Rise i={4}>
        <Card style={{ gap: 12 }}>
          <T w="b" size={16}>Appearance</T>
          <Seg<ThemePref> items={[{ v: 'system', label: 'Auto', icon: 'phone-portrait-outline' }, { v: 'light', label: 'Light', icon: 'sunny-outline' }, { v: 'dark', label: 'Dark', icon: 'moon-outline' }]} value={pref} onChange={setPref} />
        </Card>
      </Rise>
      <Rise i={5}>
        <Card style={{ gap: 12 }}>
          <T w="b" size={16}>Change admin password</T>
          <Field label="Old password" value={old} onChange={setOld} secure />
          <Field label="New password (8+ characters)" value={nw} onChange={setNw} secure />
          <Btn title="Update password" kind="outline" icon="key-outline" onPress={changePw} loading={busy === 'pw'} />
        </Card>
      </Rise>
      <Rise i={6}><Btn title="Log out" kind="red" icon="log-out-outline" onPress={out} /></Rise>
    </Screen>
  );
}
