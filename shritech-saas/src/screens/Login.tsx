import React, { useEffect, useRef, useState } from 'react';
import { Animated, Easing, KeyboardAvoidingView, Linking, Platform, ScrollView, TextInput, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import QRCode from 'react-native-qrcode-svg';
import { Btn, Card, Field, Hero, Logo, Press, Rise, Seg, T } from '../ui';
import { useTheme, F } from '../theme';
import { adminLogin, adminSetup, adminStatus, adminTotp, AdminStep, enterDemo, requestCode, verifyCode } from '../api';

function CodeBoxes({ value, onChange, auto }: { value: string; onChange: (v: string) => void; auto?: boolean }) {
  const { t } = useTheme(); const ref = useRef<any>(null);
  return (
    <Press onPress={() => ref.current?.focus()} haptic={false}>
      <View style={{ flexDirection: 'row', gap: 8, justifyContent: 'center' }}>
        {Array.from({ length: 6 }).map((_, i) => {
          const on = i === value.length;
          return (
            <View key={i} style={{ width: 46, height: 56, borderRadius: 14, borderWidth: 2, borderColor: on ? t.green : t.line, backgroundColor: t.card2, alignItems: 'center', justifyContent: 'center' }}>
              <T w="b" size={24}>{value[i] ?? ''}</T>
            </View>
          );
        })}
      </View>
      <TextInput ref={ref} value={value} onChangeText={(v) => onChange(v.replace(/\D/g, '').slice(0, 6))} keyboardType="number-pad" autoFocus={auto} maxLength={6}
        textContentType="oneTimeCode" autoComplete="one-time-code" style={{ position: 'absolute', opacity: 0, width: 1, height: 1 }} />
    </Press>
  );
}

export default function Login({ onDone }: { onDone: (role: 'user' | 'admin') => void }) {
  const { t } = useTheme();
  const [mode, setMode] = useState<'user' | 'admin'>('user');
  const [err, setErr] = useState(''); const [busy, setBusy] = useState(false); const [info, setInfo] = useState('');
  // user
  const [email, setEmail] = useState(''); const [biz, setBiz] = useState(''); const [code, setCode] = useState(''); const [sent, setSent] = useState(false);
  // admin
  const [hasAdmin, setHasAdmin] = useState<boolean | null>(null); const [aEmail, setAEmail] = useState(''); const [aPw, setAPw] = useState(''); const [setupKey, setSetupKey] = useState('');
  const [step, setStep] = useState<AdminStep | null>(null); const [totp, setTotp] = useState('');
  const pop = useRef(new Animated.Value(0)).current; const spin = useRef(new Animated.Value(0)).current; const shake = useRef(new Animated.Value(0)).current;
  const nd = Platform.OS !== 'web';
  useEffect(() => {
    Animated.spring(pop, { toValue: 1, useNativeDriver: nd, bounciness: 14, speed: 6 }).start();
    Animated.loop(Animated.timing(spin, { toValue: 1, duration: 9000, easing: Easing.linear, useNativeDriver: nd })).start();
  }, []);
  useEffect(() => { if (mode === 'admin' && hasAdmin === null) adminStatus().then((r) => setHasAdmin(r.admin_exists)).catch(() => setHasAdmin(true)); setErr(''); setInfo(''); }, [mode]);
  const bad = (m: string) => { setErr(m); Animated.sequence([10, -10, 7, -7, 0].map((v) => Animated.timing(shake, { toValue: v, duration: 60, useNativeDriver: nd }))).start(); };
  const run = async (f: () => Promise<void>) => { setBusy(true); setErr(''); try { await f(); } catch (e: any) { bad(e.message); } finally { setBusy(false); } };

  const send = () => run(async () => {
    if (!/^\S+@\S+\.\S+$/.test(email.trim())) throw new Error('Please enter your email address');
    await requestCode(email.trim()); setSent(true); setCode('');
    setInfo(`We sent a 6-digit code to ${email.trim()}. Check your inbox (and spam).`);
  });
  const verify = () => run(async () => { if (code.length !== 6) throw new Error('Enter the 6-digit code'); await verifyCode(email.trim(), code, biz.trim()); onDone('user'); });
  useEffect(() => { if (sent && code.length === 6 && !busy) verify(); }, [code]);
  const aLogin = () => run(async () => {
    const r = hasAdmin === false ? await adminSetup(setupKey.trim(), aEmail.trim(), aPw) : await adminLogin(aEmail.trim(), aPw);
    setStep(r); setTotp('');
  });
  const aTotp = () => run(async () => { if (!step) return; await adminTotp(step.token, totp); onDone('admin'); });
  useEffect(() => { if (step && totp.length === 6 && !busy) aTotp(); }, [totp]);

  return (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={{ flex: 1, backgroundColor: t.bg }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 40 }} keyboardShouldPersistTaps="handled">
        <Hero height={330}>
          <View style={{ alignItems: 'center', marginTop: 20, gap: 12 }}>
            <Animated.View style={{ transform: [{ scale: pop }] }}>
              <View style={{ width: 100, height: 100, borderRadius: 50, backgroundColor: 'rgba(255,255,255,0.14)', alignItems: 'center', justifyContent: 'center' }}>
                <Animated.View style={{ position: 'absolute', width: 100, height: 100, borderRadius: 50, borderWidth: 3, borderColor: '#FACC15', borderStyle: 'dashed', transform: [{ rotate: spin.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '360deg'] }) }] }} />
                <Ionicons name={mode === 'admin' ? 'shield-checkmark' : 'rocket'} size={46} color="#FACC15" />
              </View>
            </Animated.View>
            <Rise i={2}><Logo size={36} light /></Rise>
            <Rise i={3}><T w="m" size={14} c="rgba(255,255,255,0.9)" style={{ textAlign: 'center' }}>AutoPost · Facebook + Instagram on autopilot</T></Rise>
          </View>
        </Hero>
        <View style={{ paddingHorizontal: 18, marginTop: -50, gap: 14 }}>
          <Rise i={4}>
            <Animated.View style={{ transform: [{ translateX: shake }] }}>
              <Card style={{ gap: 14, padding: 20 }}>
                <Seg items={[{ v: 'user', label: 'Business', icon: 'storefront-outline' }, { v: 'admin', label: 'Admin', icon: 'shield-outline' }]} value={mode} onChange={(v) => { setMode(v); setStep(null); }} />
                {mode === 'user' ? (!sent ? (
                  <>
                    <T w="b" size={20}>Log in or sign up 👋</T>
                    <T s="mut" size={13}>Enter your email. We’ll send you a 6-digit code — no password needed.</T>
                    <Field label="Email" value={email} onChange={setEmail} placeholder="yourname@gmail.com" keyboard="email-address" />
                    <Field label="Business name (new accounts only)" value={biz} onChange={setBiz} placeholder="e.g. Gupta Sweets" />
                    {err ? <T size={13} c={t.red}>{err}</T> : null}
                    <Btn title="Send code" icon="mail-outline" onPress={send} loading={busy} />
                  </>
                ) : (
                  <>
                    <T w="b" size={20}>Enter your code</T>
                    <T s="mut" size={13}>{info}</T>
                    <CodeBoxes value={code} onChange={setCode} auto />
                    {err ? <T size={13} c={t.red}>{err}</T> : null}
                    <Btn title="Log in" icon="log-in-outline" onPress={verify} loading={busy} />
                    <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                      <Press onPress={() => { setSent(false); setErr(''); }}><T w="s" size={13} c={t.green}>← Change email</T></Press>
                      <Press onPress={send}><T w="s" size={13} c={t.green}>Send again</T></Press>
                    </View>
                  </>
                )) : !step ? (
                  <>
                    <T w="b" size={20}>{hasAdmin === false ? 'Create admin account' : 'Admin login'}</T>
                    <T s="mut" size={13}>{hasAdmin === false ? 'One-time setup. Use the setup key ShriTech gave you.' : 'Password + Google Authenticator code.'}</T>
                    {hasAdmin === false ? <Field label="Setup key" value={setupKey} onChange={setSetupKey} placeholder="Paste setup key" /> : null}
                    <Field label="Admin email" value={aEmail} onChange={setAEmail} placeholder="admin@gmail.com" keyboard="email-address" />
                    <Field label={hasAdmin === false ? 'New password (8+ characters)' : 'Password'} value={aPw} onChange={setAPw} secure placeholder="••••••••" />
                    {err ? <T size={13} c={t.red}>{err}</T> : null}
                    <Btn title={hasAdmin === false ? 'Create admin' : 'Continue'} icon="arrow-forward" onPress={aLogin} loading={busy} />
                  </>
                ) : (
                  <>
                    {step.stage === 'totp_enroll' ? (
                      <>
                        <T w="b" size={20}>Turn on Google Authenticator</T>
                        <T s="mut" size={13}>1. Install “Google Authenticator”. 2. Tap the button below (or scan the QR from another phone). 3. Type the 6-digit code it shows.</T>
                        <View style={{ alignItems: 'center', gap: 10 }}>
                          <View style={{ padding: 12, backgroundColor: '#fff', borderRadius: 16 }}><QRCode value={step.otpauth!} size={170} color="#14532D" /></View>
                          <Btn small kind="outline" icon="key-outline" title="Open in Authenticator" onPress={() => Linking.openURL(step.otpauth!).catch(() => {})} />
                          <T s="mut" size={11} style={{ textAlign: 'center' }}>Or enter this key manually:</T>
                          <T w="b" size={13} style={{ letterSpacing: 1, textAlign: 'center' }} c={t.green}>{step.secret?.replace(/(.{4})/g, '$1 ')}</T>
                        </View>
                      </>
                    ) : (
                      <>
                        <T w="b" size={20}>Authenticator code</T>
                        <T s="mut" size={13}>Open Google Authenticator and type the 6-digit code for ShriTech AutoPost.</T>
                      </>
                    )}
                    <CodeBoxes value={totp} onChange={setTotp} auto={step.stage === 'totp'} />
                    {err ? <T size={13} c={t.red}>{err}</T> : null}
                    <Btn title="Verify" icon="shield-checkmark-outline" onPress={aTotp} loading={busy} />
                    <Press onPress={() => setStep(null)}><T w="s" size={13} c={t.green}>← Back</T></Press>
                  </>
                )}
              </Card>
            </Animated.View>
          </Rise>
          {mode === 'user' ? <Rise i={6}><Btn title="Try demo (sample data)" kind="outline" icon="sparkles-outline" onPress={async () => { await enterDemo(); onDone('user'); }} /></Rise> : null}
          <Rise i={7}><T s="mut" size={12} style={{ textAlign: 'center' }}>Shri Balaji Digital Services · 📞 99936 15146</T></Rise>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
