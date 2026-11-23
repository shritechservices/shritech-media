import React, { useCallback, useEffect, useState } from 'react';
import { Linking, View, Switch } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { Btn, Card, CountUp, Empty, Field, Hero, Logo, Pill, PlatformIcons, Press, Rise, Screen, Seg, SectionTitle, Skel, T, Thumb, useConfirm, useStatus, useToast } from '../ui';
import { ThemePref, useTheme } from '../theme';
import { api } from '../api';
import { dateStr, timeStr } from '../time';

const STATUS = ['pending', 'active', 'paused', 'closed'] as const;
function useStatusColors() { const { t } = useTheme(); return (s: string) => (({ active: [t.green, t.chip, 'Active'], pending: [t.gold, t.goldSoft, 'Pending'], paused: [t.red, t.redSoft, 'Paused'], closed: [t.mut, t.card2, 'Closed'] } as any)[s] ?? [t.mut, t.card2, s]); }

// ================= Dashboard + business list =================
export function AdminHome({ navigation }: any) {
  const { t } = useTheme(); const sc = useStatusColors();
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
        <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
          <Logo size={26} light />
          <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}>
            <Pill label="ADMIN" color="#2A2000" bg="#FACC15" icon="shield-checkmark" />
            <Press onPress={() => navigation.navigate('AdminSettings')} style={{ width: 40, height: 40, borderRadius: 20, backgroundColor: 'rgba(255,255,255,0.16)', alignItems: 'center', justifyContent: 'center' }}><Ionicons name="settings-outline" size={21} color="#fff" /></Press>
          </View>
        </View>
        <Rise i={1}><T w="b" size={24} c="#fff" style={{ marginTop: 16 }}>Control centre</T></Rise>
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
          <Rise key={s.l} i={i} style={{ width: '48%', flexGrow: 1 }}>
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
      {loading ? <Skel h={90} /> : shown.length === 0 ? <Card><Empty icon="storefront-outline" title="No businesses yet" sub="When someone signs up with their email, they appear here as Pending." /></Card> : shown.map((x, i) => {
        const [c, bg, l] = sc(x.status);
        return (
          <Rise key={x.id} i={i}>
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
      })}
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
    <Screen header={
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
  const { t, pref, setPref } = useTheme(); const toast = useToast(); const confirm = useConfirm();
  const [st, setSt] = useState<any>(null); const [codes, setCodes] = useState<any[]>([]);
  const [old, setOld] = useState(''); const [nw, setNw] = useState(''); const [busy, setBusy] = useState('');
  const load = useCallback(async () => { try { const s = await api<any>('admin_settings_get'); setSt(s); setCodes(await api<any[]>('admin_codes')); } catch { } }, []);
  useFocusEffect(useCallback(() => { load(); const iv = setInterval(() => api<any[]>('admin_codes').then(setCodes).catch(() => {}), 8000); return () => clearInterval(iv); }, [load]));
  const testEmail = async () => { setBusy('test'); try { const r = await api<any>('admin_test_email'); toast(r.via === 'supabase' ? 'Test code sent — check your Gmail' : 'Supabase could not send the email. Check Auth email settings.', r.via === 'supabase'); load(); } catch { toast('Email could not be sent. Check the key and sender.', false); } finally { setBusy(''); } };
  const changePw = async () => { setBusy('pw'); try { await api('admin_change_password', { old, password: nw }); setOld(''); setNw(''); toast('Password changed'); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const out = async () => { if (await confirm({ title: 'Log out of admin?', ok: 'Log out' })) { try { await api('logout'); } catch { } onLogout(); } };
  return (
    <Screen header={<Hero><Press onPress={() => navigation.goBack()} style={{ marginBottom: 8 }}><Ionicons name="arrow-back" size={24} color="#fff" /></Press><T w="b" size={24} c="#fff">Admin settings</T></Hero>}>
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
          <T w="b" size={16}>Appearance</T>
          <Seg<ThemePref> items={[{ v: 'system', label: 'Auto', icon: 'phone-portrait-outline' }, { v: 'light', label: 'Light', icon: 'sunny-outline' }, { v: 'dark', label: 'Dark', icon: 'moon-outline' }]} value={pref} onChange={setPref} />
        </Card>
      </Rise>
      <Rise i={3}>
        <Card style={{ gap: 12 }}>
          <T w="b" size={16}>Change admin password</T>
          <Field label="Old password" value={old} onChange={setOld} secure />
          <Field label="New password (8+ characters)" value={nw} onChange={setNw} secure />
          <Btn title="Update password" kind="outline" icon="key-outline" onPress={changePw} loading={busy === 'pw'} />
        </Card>
      </Rise>
      <Rise i={4}><Btn title="Log out" kind="red" icon="log-out-outline" onPress={out} /></Rise>
    </Screen>
  );
}
