import React, { useEffect, useRef, useState } from 'react';
import { Animated, Easing, KeyboardAvoidingView, Platform, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Btn, Card, Field, Hero, Logo, Press, Rise, T } from '../ui';
import { useTheme } from '../theme';
import { enterDemo, login } from '../api';

export default function Login({ onDone }: { onDone: () => void }) {
  const { t } = useTheme();
  const [pw, setPw] = useState(''); const [show, setShow] = useState(false); const [busy, setBusy] = useState(false); const [err, setErr] = useState('');
  const pop = useRef(new Animated.Value(0)).current; const spin = useRef(new Animated.Value(0)).current; const shake = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    Animated.spring(pop, { toValue: 1, useNativeDriver: Platform.OS !== 'web', bounciness: 14, speed: 6 }).start();
    Animated.loop(Animated.timing(spin, { toValue: 1, duration: 9000, easing: Easing.linear, useNativeDriver: Platform.OS !== 'web' })).start();
  }, []);
  const doShake = () => Animated.sequence([10, -10, 7, -7, 0].map((v) => Animated.timing(shake, { toValue: v, duration: 60, useNativeDriver: Platform.OS !== 'web' }))).start();
  const go = async () => {
    if (!pw) { setErr('Please enter your password.'); doShake(); return; }
    setBusy(true); setErr('');
    try { await login(pw); onDone(); } catch (e: any) { setErr(e.message); doShake(); } finally { setBusy(false); }
  };
  const demo = async () => { await enterDemo(); onDone(); };
  return (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={{ flex: 1, backgroundColor: t.bg }}>
      <Hero height={390}>
        <View style={{ alignItems: 'center', marginTop: 30, gap: 14 }}>
          <Animated.View style={{ transform: [{ scale: pop }] }}>
            <View style={{ width: 112, height: 112, borderRadius: 56, backgroundColor: 'rgba(255,255,255,0.14)', alignItems: 'center', justifyContent: 'center' }}>
              <Animated.View style={{ position: 'absolute', width: 112, height: 112, borderRadius: 56, borderWidth: 3, borderColor: '#FACC15', borderStyle: 'dashed', transform: [{ rotate: spin.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '360deg'] }) }] }} />
              <Ionicons name="rocket" size={50} color="#FACC15" />
            </View>
          </Animated.View>
          <Rise i={2}><Logo size={38} light /></Rise>
          <Rise i={3}><T w="m" size={15} c="rgba(255,255,255,0.9)" style={{ textAlign: 'center' }}>AutoPost · Facebook + Instagram on autopilot</T></Rise>
        </View>
      </Hero>
      <View style={{ paddingHorizontal: 18, marginTop: -50 }}>
        <Rise i={4}>
          <Animated.View style={{ transform: [{ translateX: shake }] }}>
            <Card style={{ gap: 14, padding: 20 }}>
              <T w="b" size={21}>Welcome back 👋</T>
              <T s="mut" size={13}>Use the same password as your ShriTech website.</T>
              <Field label="Password" value={pw} onChange={setPw} secure={!show} placeholder="Enter password"
                right={<Press onPress={() => setShow(!show)} haptic={false}><Ionicons name={show ? 'eye-off' : 'eye'} size={20} color={t.mut} /></Press>} />
              {err ? <T size={13} c={t.red}>{err}</T> : null}
              <Btn title="Log in" icon="log-in-outline" onPress={go} loading={busy} />
              <Btn title="Try demo (sample data)" kind="outline" icon="sparkles-outline" onPress={demo} />
            </Card>
          </Animated.View>
        </Rise>
        <Rise i={6}><T s="mut" size={12} style={{ textAlign: 'center', marginTop: 18 }}>Shri Balaji Digital Services · 📞 99936 15146</T></Rise>
      </View>
    </KeyboardAvoidingView>
  );
}
