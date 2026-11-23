import React, { useEffect, useRef, useState } from 'react';
import { Animated, Easing, KeyboardAvoidingView, Linking, Platform, ScrollView, TextInput, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import QRCode from 'react-native-qrcode-svg';
import { Btn, Card, Field, Hero, Logo, Press, Rise, Seg, T, useWide } from '../ui';
import { LinearGradient } from 'expo-linear-gradient';
import { useTheme, F } from '../theme';
import { userForgot, userReset, adminForgot, adminLogin, adminReset, adminSetup, adminStatus, adminTotp, AdminStep, enterDemo, loginPassword, requestCode, verifyCode } from '../api';

function CodeBoxes({ value, onChange, auto, max = 6 }: { value: string; onChange: (v: string) => void; auto?: boolean; max?: number }) {
  const { t } = useTheme(); const ref = useRef<any>(null);
  return (
    <Press onPress={() => ref.current?.focus()} haptic={false}>
      <View style={{ flexDirection: 'row', gap: max > 6 ? 6 : 8, justifyContent: 'center' }}>
        {Array.from({ length: max }).map((_, i) => {
          const on = i === value.length;
          return (
            <View key={i} style={{ width: max > 6 ? 34 : 46, height: 54, borderRadius: 14, borderWidth: 2, borderColor: on ? t.green : t.line, backgroundColor: t.card2, alignItems: 'center', justifyContent: 'center' }}>
              <T w="b" size={24}>{value[i] ?? ''}</T>
            </View>
          );
        })}
      </View>
      <TextInput ref={ref} value={value} onChangeText={(v) => onChange(v.replace(/\D/g, '').slice(0, max))} keyboardType="number-pad" autoFocus={auto} maxLength={max}
        textContentType="oneTimeCode" autoComplete="one-time-code" style={{ position: 'absolute', opacity: 0, width: 1, height: 1 }} />
    </Press>
  );
}

export default function Login({ onDone, onBack }: { onDone: (role: 'user' | 'admin') => void; onBack?: () => void }) {
  const { t } = useTheme(); const wide = useWide();
  const [mode, setMode] = useState<'user' | 'admin'>('user');
  const [err, setErr] = useState(''); const [busy, setBusy] = useState(false); const [info, setInfo] = useState('');
  // user
  const [how, setHow] = useState<'code' | 'pw'>('code'); const [uPw, setUPw] = useState('');
  const [email, setEmail] = useState(''); const [biz, setBiz] = useState(''); const [code, setCode] = useState(''); const [sent, setSent] = useState(false);
  // admin
  const [hasAdmin, setHasAdmin] = useState<boolean | null>(null); const [aEmail, setAEmail] = useState(''); const [aPw, setAPw] = useState(''); const [setupKey, setSetupKey] = useState('');
  const [step, setStep] = useState<AdminStep | null>(null); const [totp, setTotp] = useState('');
  const [forgot, setForgot] = useState<0 | 1 | 2>(0); const [rCode, setRCode] = useState(''); const [rPw, setRPw] = useState('');
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
    setInfo(`We sent a login code to ${email.trim()}. Check your inbox (and spam), then type the code here.`);
  });
  const pwLogin = () => run(async () => { if (!/^\S+@\S+\.\S+$/.test(email.trim())) throw new Error('Please enter your email address'); await loginPassword(email.trim(), uPw); onDone('user'); });
  const verify = () => run(async () => { if (code.length < 6) throw new Error('Enter the code from your email'); await verifyCode(email.trim(), code, biz.trim()); onDone('user'); });
  const aLogin = () => run(async () => {
    const r = hasAdmin === false ? await adminSetup(setupKey.trim(), aEmail.trim(), aPw) : await adminLogin(aEmail.trim(), aPw);
    setStep(r); setTotp('');
  });
  const fEmail = mode === 'admin' ? aEmail : email; const setFEmail = mode === 'admin' ? setAEmail : setEmail;
  const fSend = () => run(async () => { const e = fEmail.trim(); if (!/^\S+@\S+\.\S+$/.test(e)) throw new Error('Please enter your email'); if (mode === 'admin') await adminForgot(e); else await userForgot(e); setForgot(2); setRCode(''); setRPw(''); });
  const fReset = () => run(async () => {
    if (rCode.length < 6) throw new Error('Enter the code from your email'); if (rPw.length < 8) throw new Error('Use at least 8 characters for the new password');
    if (mode === 'admin') { await adminReset(fEmail.trim(), rCode, rPw); setAPw(''); setInfo('Password changed ✅ Log in with the new password + Authenticator code.'); }
    else { await userReset(fEmail.trim(), rCode, rPw); setHow('pw'); setUPw(''); setInfo('Password changed ✅ Log in with your new password.'); }
    setForgot(0);
  });
  const aTotp = () => run(async () => { if (!step) return; await adminTotp(step.token, totp); onDone('admin'); });
  useEffect(() => { if (step && totp.length === 6 && !busy) aTotp(); }, [totp]);

  const formBody = (<>
          <Rise i={4}>
            <Animated.View style={{ transform: [{ translateX: shake }] }}>
              <Card style={{ gap: 14, padding: 20 }}>
                <Seg items={[{ v: 'user', label: 'Business', icon: 'storefront-outline' }, { v: 'admin', label: 'Admin', icon: 'shield-outline' }]} value={mode} onChange={(v) => { setMode(v); setStep(null); setForgot(0); }} />
                {info && !forgot && !(mode === 'user' && sent) ? <View style={{ backgroundColor: t.chip, borderRadius: 12, padding: 10 }}><T w="m" size={13} c={t.green}>{info}</T></View> : null}
                {forgot ? (
                  <>
                    <T w="b" size={20}>Reset password 🔑</T>
                    {forgot === 1 ? (
                      <>
                        <T s="mut" size={13}>Enter your {mode === 'admin' ? 'admin ' : ''}email. We’ll send an 8-digit code to reset your password.</T>
                        <Field label="Email" value={fEmail} onChange={setFEmail} placeholder="yourname@gmail.com" keyboard="email-address" />
                        {err ? <T size={13} c={t.red}>{err}</T> : null}
                        <Btn title="Send reset code" icon="mail-outline" onPress={fSend} loading={busy} />
                      </>
                    ) : (
                      <>
                        <T s="mut" size={13}>We sent a code to {fEmail.trim()}. Check Inbox and Spam.</T>
                        <CodeBoxes value={rCode} onChange={setRCode} auto max={8} />
                        <Field label="New password (8+ characters)" value={rPw} onChange={setRPw} secure placeholder="••••••••" />
                        {err ? <T size={13} c={t.red}>{err}</T> : null}
                        <Btn title="Change password" icon="checkmark-circle-outline" onPress={fReset} loading={busy} />
                        <Press onPress={fSend}><T w="s" size={13} c={t.green} style={{ textAlign: 'center' }}>Send code again</T></Press>
                      </>
                    )}
                    <Press onPress={() => { setForgot(0); setErr(''); }}><T w="s" size={13} c={t.green} style={{ textAlign: 'center' }}>← Back to login</T></Press>
                  </>
                ) : mode === 'user' ? (!sent ? (
                  <>
                    <T w="b" size={20}>Log in or sign up 👋</T>
                    <View style={{ flexDirection: 'row', gap: 8 }}>
                      {([['code', 'Email code', 'mail-outline'], ['pw', 'Password', 'key-outline']] as const).map(([k, l, i]) => (
                        <Press key={k} onPress={() => { setHow(k); setErr(''); }} style={{ flexDirection: 'row', gap: 6, alignItems: 'center', paddingHorizontal: 12, paddingVertical: 7, borderRadius: 99, backgroundColor: how === k ? t.chip : 'transparent', borderWidth: 1, borderColor: how === k ? t.green : t.line }}>
                          <Ionicons name={i} size={14} color={how === k ? t.green : t.mut} /><T w="s" size={12} c={how === k ? t.green : t.mut}>{l}</T>
                        </Press>
                      ))}
                    </View>
                    <T s="mut" size={13}>{how === 'code' ? 'Enter your Gmail. We’ll email you a login code — no password needed.' : 'Log in with the email and password ShriTech set for you.'}</T>
                    <Field label="Email" value={email} onChange={setEmail} placeholder="yourname@gmail.com" keyboard="email-address" />
                    {how === 'code' ? <Field label="Business name (new accounts only)" value={biz} onChange={setBiz} placeholder="e.g. Gupta Sweets" /> : <Field label="Password" value={uPw} onChange={setUPw} secure placeholder="••••••••" />}
                    {err ? <T size={13} c={t.red}>{err}</T> : null}
                    {how === 'code' ? <Btn title="Send code" icon="mail-outline" onPress={send} loading={busy} /> : <Btn title="Log in" icon="log-in-outline" onPress={pwLogin} loading={busy} />}
                    {how === 'pw' ? <Press onPress={() => { setForgot(1); setErr(''); }}><T w="s" size={13} c={t.green} style={{ textAlign: 'center' }}>Forgot password?</T></Press> : null}
                  </>
                ) : (
                  <>
                    <T w="b" size={20}>Enter your code</T>
                    <T s="mut" size={13}>{info}</T>
                    <CodeBoxes value={code} onChange={setCode} auto max={8} />
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
                    {hasAdmin ? <Press onPress={() => { setForgot(1); setErr(''); }}><T w="s" size={13} c={t.green} style={{ textAlign: 'center' }}>Forgot password?</T></Press> : null}
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
          {onBack ? <Press onPress={onBack}><T w="s" size={13} c={t.green} style={{ textAlign: 'center' }}>← Back to home</T></Press> : null}
          <Rise i={7}><T s="mut" size={12} style={{ textAlign: 'center' }}>Shri Balaji Digital Services · 📞 99936 15146</T></Rise>
  </>);
  if (wide) return (
    <View style={{ flex: 1, flexDirection: 'row', backgroundColor: t.bg }}>
      <LinearGradient colors={t.grad as any} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ flex: 1.1, paddingHorizontal: 64, paddingVertical: 48, justifyContent: 'center', overflow: 'hidden' }}>
        <View style={{ position: 'absolute', width: 420, height: 420, borderRadius: 210, backgroundColor: 'rgba(250,204,21,0.16)', top: -120, right: -120 }} />
        <View style={{ position: 'absolute', width: 300, height: 300, borderRadius: 150, backgroundColor: 'rgba(255,255,255,0.07)', bottom: -100, left: -80 }} />
        <View style={{ maxWidth: 520, gap: 18 }}>
          <Logo size={44} light />
          <T w="b" size={38} c="#fff" style={{ lineHeight: 48 }}>Facebook & Instagram on autopilot.</T>
          <T size={16} c="rgba(255,255,255,0.85)" style={{ lineHeight: 26 }}>Plan a whole month of reels, post on time automatically, and reply to every comment in DM — all from one place.</T>
          <View style={{ gap: 12, marginTop: 8 }}>
            {([['calendar', 'Schedule posts and reels for the whole month'], ['logo-instagram', 'Facebook Page + Instagram together, with collabs'], ['chatbubbles', 'Auto DM replies to comments and story replies'], ['shield-checkmark', 'Secure login · your data stays private']] as const).map(([i, l]) => (
              <View key={l} style={{ flexDirection: 'row', alignItems: 'center', gap: 12 }}>
                <View style={{ width: 36, height: 36, borderRadius: 12, backgroundColor: 'rgba(255,255,255,0.14)', alignItems: 'center', justifyContent: 'center' }}><Ionicons name={i as any} size={18} color="#FACC15" /></View>
                <T w="m" size={15} c="#fff">{l}</T>
              </View>
            ))}
          </View>
        </View>
      </LinearGradient>
      <ScrollView style={{ flex: 1 }} contentContainerStyle={{ flexGrow: 1, justifyContent: 'center', alignItems: 'center', padding: 40 }} keyboardShouldPersistTaps="handled">
        <View style={{ width: '100%', maxWidth: 460, gap: 14 }}>{formBody}</View>
      </ScrollView>
    </View>
  );
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
          {formBody}
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
