import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Btn, Card, Field, Hero, Logo, Press, Rise, Screen, Seg, T, useConfirm, useToast, PlatformIcons } from '../ui';
import { ThemePref, useTheme, palettes } from '../theme';
import { api, isDemo } from '../api';
import { getSettings } from '../data';

export default function Settings({ navigation, onLogout }: any) {
  const { t, pref, setPref } = useTheme(); const toast = useToast(); const confirm = useConfirm();
  const [s, setS] = useState<any>(null); const [test, setTest] = useState<any>(null); const [testing, setTesting] = useState(false);
  const [old, setOld] = useState(''); const [nw, setNw] = useState(''); const [pwBusy, setPwBusy] = useState(false);
  useEffect(() => { getSettings(true).then(setS).catch(() => {}); }, []);
  const runTest = async () => {
    setTesting(true); setTest(null);
    try { const r = await api<any>('test_connection'); setTest({ fb: String(r.facebook ?? '').startsWith('✅'), ig: String(r.instagram ?? '').startsWith('✅') }); }
    catch { setTest({ fb: false, ig: false }); } finally { setTesting(false); }
  };
  const changePw = async () => {
    setPwBusy(true);
    try { await api('change_password', { old, password: nw }); toast('Password changed. Please log in again.'); setTimeout(onLogout, 1000); }
    catch (e: any) { toast(e.message, false); } finally { setPwBusy(false); }
  };
  const out = async () => { if (await confirm({ title: 'Log out?', msg: 'You can log in again anytime with your password.', ok: 'Log out' })) { try { await api('logout'); } catch { } onLogout(); } };
  const swatch = (k: 'light' | 'dark') => (
    <View style={{ flex: 1, height: 76, borderRadius: 16, backgroundColor: palettes[k].bg, borderWidth: 2, borderColor: (pref === k) ? t.green : t.line, padding: 8, gap: 5 }}>
      <View style={{ height: 14, borderRadius: 6, backgroundColor: palettes[k].green, width: '60%' }} />
      <View style={{ height: 22, borderRadius: 8, backgroundColor: palettes[k].card, borderWidth: 1, borderColor: palettes[k].line }} />
      <View style={{ height: 8, borderRadius: 4, backgroundColor: palettes[k].gold, width: '35%' }} />
    </View>
  );
  const Row = ({ ok, label, icon }: { ok: boolean | null; label: string; icon: any }) => (
    <View style={{ flexDirection: 'row', gap: 10, alignItems: 'center' }}>
      <Ionicons name={icon} size={20} color={t.mut} /><T w="m" size={14} style={{ flex: 1 }}>{label}</T>
      {ok === null ? null : <Ionicons name={ok ? 'checkmark-circle' : 'close-circle'} size={22} color={ok ? t.green : t.red} />}
    </View>
  );
  return (
    <Screen header={
      <Hero>
        <Press onPress={() => navigation.goBack()} style={{ marginBottom: 8 }}><Ionicons name="arrow-back" size={24} color="#fff" /></Press>
        <T w="b" size={24} c="#fff">Settings</T>
      </Hero>
    }>
      <Rise>
        <Card style={{ gap: 12 }}>
          <T w="b" size={16}>Appearance</T>
          <View style={{ flexDirection: 'row', gap: 10 }}>
            <Press onPress={() => setPref('light')} style={{ flex: 1, gap: 6 }}>{swatch('light')}<T w="s" size={12} style={{ textAlign: 'center' }}>☀️ Light</T></Press>
            <Press onPress={() => setPref('dark')} style={{ flex: 1, gap: 6 }}>{swatch('dark')}<T w="s" size={12} style={{ textAlign: 'center' }}>🌙 Dark</T></Press>
          </View>
          <Seg<ThemePref> items={[{ v: 'system', label: 'Auto', icon: 'phone-portrait-outline' }, { v: 'light', label: 'Light', icon: 'sunny-outline' }, { v: 'dark', label: 'Dark', icon: 'moon-outline' }]} value={pref} onChange={setPref} />
        </Card>
      </Rise>
      <Rise i={1}>
        <Card style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}><T w="b" size={16}>Connected accounts</T><PlatformIcons list={['facebook', 'instagram']} size={20} /></View>
          <Row icon="logo-facebook" label={s?.page_name || 'Facebook Page'} ok={test ? test.fb : null} />
          <Row icon="logo-instagram" label={s?.ig_username ? '@' + s.ig_username : 'Instagram account'} ok={test ? test.ig : null} />
          <Btn title={testing ? 'Checking…' : 'Check connection'} icon="pulse" kind="outline" onPress={runTest} loading={testing} />
          <T s="mut" size={12}>Account keys stay safely on the server and are never shown in the app.</T>
        </Card>
      </Rise>
      {!isDemo() ? (
        <Rise i={2}>
          <Card style={{ gap: 12 }}>
            <T w="b" size={16}>Change password</T>
            <T s="mut" size={12}>This also changes the website password.</T>
            <Field label="Old password" value={old} onChange={setOld} secure />
            <Field label="New password (8+ characters)" value={nw} onChange={setNw} secure />
            <Btn title="Update password" kind="outline" icon="key-outline" onPress={changePw} loading={pwBusy} />
          </Card>
        </Rise>
      ) : null}
      <Rise i={3}><Btn title={isDemo() ? 'Exit demo' : 'Log out'} kind="red" icon="log-out-outline" onPress={out} /></Rise>
      <Rise i={4}>
        <View style={{ alignItems: 'center', gap: 4, marginTop: 10 }}>
          <Logo size={22} />
          <T s="mut" size={12}>AutoPost app · v1.0</T>
          <T s="mut" size={12}>Shri Balaji Digital Services · 📞 99936 15146</T>
        </View>
      </Rise>
    </Screen>
  );
}
