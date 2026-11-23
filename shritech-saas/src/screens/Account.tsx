import React, { useCallback, useState } from 'react';
import { Linking, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { Btn, Card, Field, Hero, Logo, Pill, PlatformIcons, Press, Rise, Screen, Seg, T, useConfirm, useToast } from '../ui';
import { ThemePref, useTheme } from '../theme';
import { api, isDemo } from '../api';
import { getMe, Me } from '../data';

export default function Account({ navigation, onLogout }: any) {
  const { t, pref, setPref } = useTheme(); const toast = useToast(); const confirm = useConfirm();
  const [me, setMe] = useState<Me | null>(null); const [team, setTeam] = useState<any[]>([]);
  const [name, setName] = useState(''); const [phone, setPhone] = useState(''); const [note, setNote] = useState(''); const [cap, setCap] = useState(''); const [newMem, setNewMem] = useState(''); const [busy, setBusy] = useState(''); const [pw, setPw] = useState('');
  const load = useCallback(async () => {
    try { const m = await getMe(true); setMe(m); setName(m.tenant.name); setPhone(m.tenant.contact_phone); setNote(m.tenant.request_note); setCap(m.tenant.default_caption); setTeam(await api<any[]>('list_team')); } catch { }
  }, []);
  useFocusEffect(useCallback(() => { load(); }, [load]));
  const owner = me?.user.role === 'owner'; const ten = me?.tenant;
  const save = async () => { setBusy('save'); try { await api('update_profile', { name, contact_phone: phone, request_note: note, default_caption: cap }); toast(ten?.status === 'pending' ? 'Sent to ShriTech ✅' : 'Saved'); load(); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const add = async () => { setBusy('add'); try { await api('add_member', { email: newMem }); setNewMem(''); toast('Team member added. They log in with their email.'); load(); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const remove = async (u: any) => { if (!(await confirm({ title: `Remove ${u.email}?`, msg: 'They will no longer be able to log in.', ok: 'Remove', danger: true }))) return; try { await api('remove_member', { id: u.id }); load(); } catch (e: any) { toast(e.message, false); } };
  const setPassword = async () => { setBusy('pw'); try { await api('user_set_password', { password: pw }); setPw(''); toast('Password saved. You can log in with email + password.'); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); } };
  const out = async () => { if (await confirm({ title: isDemo() ? 'Exit demo?' : 'Log out?', ok: isDemo() ? 'Exit' : 'Log out' })) { try { await api('logout'); } catch { } onLogout(); } };
  const statusPill = ten ? ({ active: [t.green, t.chip, 'Active'], pending: [t.gold, t.goldSoft, 'Setting up'], paused: [t.red, t.redSoft, 'Paused'], closed: [t.mut, t.card2, 'Closed'] } as any)[ten.status] ?? [t.mut, t.card2, ten.status] : null;
  const used = ten ? Math.min(1, ten.post_quota ? ten.used_this_month / ten.post_quota : 0) : 0;
  return (
    <Screen header={
      <Hero>
        <Press onPress={() => navigation.goBack()} style={{ marginBottom: 8 }}><Ionicons name="arrow-back" size={24} color="#fff" /></Press>
        <T w="b" size={24} c="#fff">My account</T>
        <T size={13} c="rgba(255,255,255,0.85)">{me?.user.email}</T>
      </Hero>
    }>
      {ten ? (
        <Rise>
          <Card style={{ gap: 12 }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
              <T w="b" size={17} style={{ flex: 1 }}>{ten.name}</T>
              {statusPill ? <Pill label={statusPill[2]} color={statusPill[0]} bg={statusPill[1]} size={12} /> : null}
            </View>
            <View style={{ flexDirection: 'row', gap: 10 }}>
              <View style={{ flex: 1, backgroundColor: t.card2, borderRadius: 14, padding: 10 }}><T s="mut" size={11}>Plan</T><T w="b" size={15} style={{ textTransform: 'capitalize' }}>{ten.plan}</T></View>
              <View style={{ flex: 1, backgroundColor: t.card2, borderRadius: 14, padding: 10 }}><T s="mut" size={11}>Valid till</T><T w="b" size={15}>{ten.valid_till ?? '—'}</T></View>
            </View>
            {ten.post_quota > 0 ? (
              <View style={{ gap: 6 }}>
                <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}><T s="mut" size={12}>Posts this month</T><T w="s" size={12}>{ten.used_this_month} / {ten.post_quota}</T></View>
                <View style={{ height: 10, borderRadius: 5, backgroundColor: t.card2, overflow: 'hidden' }}><View style={{ height: 10, width: `${Math.round(used * 100)}%`, backgroundColor: used > 0.9 ? t.red : t.green }} /></View>
              </View>
            ) : null}
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10, paddingTop: 4 }}>
              <PlatformIcons list={['facebook', 'instagram']} size={20} />
              <T size={13} style={{ flex: 1 }}>{ten.connected ? `${ten.page_name ?? 'Facebook Page'}${ten.ig_username ? ' · @' + ten.ig_username : ''}` : 'Not connected yet — ShriTech will connect it'}</T>
              <Ionicons name={ten.connected ? 'checkmark-circle' : 'time-outline'} size={20} color={ten.connected ? t.green : t.gold} />
            </View>
          </Card>
        </Rise>
      ) : null}
      {owner ? (
        <Rise i={1}>
          <Card style={{ gap: 12 }}>
            <T w="b" size={16}>{ten?.status === 'pending' ? 'Send your details to ShriTech' : 'Business details'}</T>
            <Field label="Business name" value={name} onChange={setName} />
            <Field label="WhatsApp / phone" value={phone} onChange={setPhone} keyboard="phone-pad" placeholder="98xxxxxxxx" />
            <Field label="Facebook Page link & Instagram username" value={note} onChange={setNote} multiline placeholder={'facebook.com/yourpage\n@yourinstagram'} />
            <Field label="Default caption / hashtags" value={cap} onChange={setCap} multiline placeholder="#YourBrand 📞 98xxxxxxxx" />
            <Btn title={ten?.status === 'pending' ? 'Send to ShriTech' : 'Save'} icon="checkmark" kind="gold" onPress={save} loading={busy === 'save'} />
          </Card>
        </Rise>
      ) : null}
      <Rise i={2}>
        <Card style={{ gap: 10 }}>
          <T w="b" size={16}>Team</T>
          {team.map((u) => (
            <View key={u.id} style={{ flexDirection: 'row', alignItems: 'center', gap: 10, opacity: u.active ? 1 : 0.5 }}>
              <View style={{ width: 36, height: 36, borderRadius: 18, backgroundColor: t.chip, alignItems: 'center', justifyContent: 'center' }}><T w="b" c={t.green}>{u.email[0].toUpperCase()}</T></View>
              <View style={{ flex: 1 }}><T w="s" size={13} lines={1}>{u.email}</T><T s="mut" size={11}>{u.role === 'owner' ? 'Owner' : u.active ? 'Team member' : 'Removed'}</T></View>
              {owner && u.role === 'member' && u.active ? <Press onPress={() => remove(u)}><Ionicons name="close-circle" size={22} color={t.red} /></Press> : null}
            </View>
          ))}
          {owner ? <Field value={newMem} onChange={setNewMem} placeholder="Add team member email" keyboard="email-address" right={<Press onPress={add}><Ionicons name="person-add" size={22} color={t.green} /></Press>} /> : null}
        </Card>
      </Rise>
      {!isDemo() ? (
        <Rise i={3}>
          <Card style={{ gap: 12 }}>
            <T w="b" size={16}>{me?.user.has_password ? 'Change password' : 'Set a password (optional)'}</T>
            <T s="mut" size={12}>You can always log in with an email code too.</T>
            <Field label="New password (8+ characters)" value={pw} onChange={setPw} secure />
            <Btn title="Save password" kind="outline" icon="key-outline" onPress={setPassword} loading={busy === 'pw'} />
          </Card>
        </Rise>
      ) : null}
      <Rise i={3}>
        <Card style={{ gap: 12 }}>
          <T w="b" size={16}>Appearance</T>
          <Seg<ThemePref> items={[{ v: 'system', label: 'Auto', icon: 'phone-portrait-outline' }, { v: 'light', label: 'Light', icon: 'sunny-outline' }, { v: 'dark', label: 'Dark', icon: 'moon-outline' }]} value={pref} onChange={setPref} />
        </Card>
      </Rise>
      <Rise i={4} style={{ gap: 10 }}>
        <Btn title="Talk to ShriTech" kind="outline" icon="logo-whatsapp" onPress={() => Linking.openURL('https://wa.me/919993615146')} />
        <Btn title={isDemo() ? 'Exit demo' : 'Log out'} kind="red" icon="log-out-outline" onPress={out} />
      </Rise>
      <View style={{ alignItems: 'center', gap: 4, marginTop: 6 }}><Logo size={20} /><T s="mut" size={12}>AutoPost for business · v2.0</T></View>
    </Screen>
  );
}
