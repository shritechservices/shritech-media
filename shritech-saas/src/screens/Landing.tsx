import React, { useEffect, useRef } from 'react';
import { Animated, Easing, Image, Linking, ScrollView, View, useWindowDimensions } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { Btn, Card, Logo, Press, Rise, T, sh } from '../ui';
import { useTheme } from '../theme';

const FEATURES: { i: any; t: string; d: string; c: string }[] = [
  { i: 'calendar', t: 'Plan a whole month', d: 'Drag your reels and posts onto a calendar. We publish them on time, even when your phone is off.', c: '#16A34A' },
  { i: 'logo-instagram', t: 'Facebook + Instagram together', d: 'One upload goes to your Facebook Page and Instagram as a Reel or post, with collab tags.', c: '#DB2777' },
  { i: 'chatbubbles', t: 'Auto replies & DMs', d: 'Someone comments “price”? They get your message in DM instantly, plus a public reply.', c: '#EAB308' },
  { i: 'images', t: 'Media library', d: 'Keep every reel and creative in one place. Re-use them anytime in one tap.', c: '#2563EB' },
  { i: 'people', t: 'Your team', d: 'Add staff with their Gmail. No passwords to share — they log in with an email code.', c: '#7C3AED' },
  { i: 'shield-checkmark', t: 'Done-for-you setup', d: 'ShriTech connects your accounts for you. Secure login, your data stays private.', c: '#0F766E' },
];
const STEPS = [
  { n: '1', t: 'Sign up with Gmail', d: 'Enter your email, type the code we send. That’s it.' },
  { n: '2', t: 'We connect your Page', d: 'Send your Facebook Page & Instagram. ShriTech sets everything up.' },
  { n: '3', t: 'Post on autopilot', d: 'Upload, pick a time, relax. We post and reply for you.' },
];

export default function Landing({ onStart }: { onStart: () => void }) {
  const { t } = useTheme(); const { width } = useWindowDimensions(); const wide = width >= 900; const mid = width >= 640;
  const float = useRef(new Animated.Value(0)).current;
  useEffect(() => { Animated.loop(Animated.sequence([Animated.timing(float, { toValue: 1, duration: 2600, easing: Easing.inOut(Easing.sin), useNativeDriver: false }), Animated.timing(float, { toValue: 0, duration: 2600, easing: Easing.inOut(Easing.sin), useNativeDriver: false })])).start(); }, []);
  const ty = float.interpolate({ inputRange: [0, 1], outputRange: [0, -14] });
  const W = Math.min(1180, width - 32);
  const phone = (src: any, rot: string, sc = 1) => (
    <Animated.View style={[{ transform: [{ translateY: ty }, { rotate: rot }, { scale: sc }] }]}>
      <View style={[{ width: 250, height: 540, borderRadius: 40, backgroundColor: '#0B1410', padding: 9 }, sh('#000', 0.35, 30, 18)]}>
        <Image source={src} style={{ width: '100%', height: '100%', borderRadius: 32 }} resizeMode="cover" />
      </View>
    </Animated.View>
  );
  return (
    <ScrollView style={{ flex: 1, backgroundColor: t.bg }} contentContainerStyle={{ alignItems: 'center' }}>
      {/* nav */}
      <View style={{ width: W, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 18 }}>
        <Logo size={28} />
        <View style={{ flexDirection: 'row', gap: 10, alignItems: 'center' }}>
          {mid ? <Press onPress={() => Linking.openURL('https://wa.me/919993615146')}><T w="s" size={14} c={t.green}>Talk to us</T></Press> : null}
          <Btn small title="Log in" kind="outline" onPress={onStart} />
          {mid ? <Btn small title="Start free" kind="gold" onPress={onStart} /> : null}
        </View>
      </View>
      {/* hero */}
      <LinearGradient colors={t.grad as any} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ width: W, borderRadius: 36, padding: wide ? 56 : 26, flexDirection: wide ? 'row' : 'column', alignItems: 'center', gap: 30, overflow: 'hidden' }}>
        <View style={{ position: 'absolute', width: 420, height: 420, borderRadius: 210, backgroundColor: 'rgba(250,204,21,0.18)', top: -160, right: -120 }} />
        <View style={{ flex: wide ? 1.1 : undefined, gap: 18 }}>
          <Rise><View style={{ alignSelf: 'flex-start', backgroundColor: 'rgba(250,204,21,0.2)', borderRadius: 99, paddingHorizontal: 14, paddingVertical: 6 }}><T w="s" size={13} c="#FACC15">🚀 Social media on autopilot for Indian businesses</T></View></Rise>
          <Rise i={1}><T w="x" size={wide ? 52 : 34} c="#fff" style={{ lineHeight: wide ? 62 : 42 }}>Post to Facebook & Instagram — automatically.</T></Rise>
          <Rise i={2}><T size={wide ? 18 : 15} c="rgba(255,255,255,0.88)" style={{ lineHeight: wide ? 28 : 23 }}>Schedule reels and posts for the whole month, reply to comments in DM, and grow your business while you focus on customers.</T></Rise>
          <Rise i={3}>
            <View style={{ flexDirection: 'row', gap: 12, flexWrap: 'wrap' }}>
              <Btn title="Start with Gmail" icon="mail" kind="gold" onPress={onStart} />
              <Press onPress={() => Linking.openURL('https://wa.me/919993615146')} style={{ flexDirection: 'row', gap: 8, alignItems: 'center', borderWidth: 1.5, borderColor: '#fff', borderRadius: 14, paddingVertical: 13, paddingHorizontal: 20 }}><Ionicons name="logo-whatsapp" size={19} color="#fff" /><T w="s" size={15} c="#fff">WhatsApp us</T></Press>
            </View>
          </Rise>
          <Rise i={4}><View style={{ flexDirection: 'row', gap: 18, flexWrap: 'wrap' }}>{['No password', 'Light & dark mode', 'Works on phone & web'].map((x) => <View key={x} style={{ flexDirection: 'row', gap: 6, alignItems: 'center' }}><Ionicons name="checkmark-circle" size={16} color="#FACC15" /><T size={13} c="#fff">{x}</T></View>)}</View></Rise>
        </View>
        <View style={{ flex: wide ? 1 : undefined, flexDirection: 'row', justifyContent: 'center', alignItems: 'center', height: wide ? 560 : 470 }}>
          {mid ? <View style={{ marginRight: -70, zIndex: 0, opacity: 0.95 }}>{phone(require('../../assets/web/hero_dark.jpg'), '-8deg', 0.86)}</View> : null}
          <View style={{ zIndex: 2 }}>{phone(require('../../assets/web/hero_light.jpg'), '3deg', wide ? 1 : 0.85)}</View>
        </View>
      </LinearGradient>
      {/* features */}
      <View style={{ width: W, paddingVertical: 50, gap: 26 }}>
        <View style={{ alignItems: 'center', gap: 8 }}>
          <T w="x" size={wide ? 36 : 26} style={{ textAlign: 'center' }}>Everything your page needs</T>
          <T s="mut" size={15} style={{ textAlign: 'center', maxWidth: 620 }}>One simple app for planning, posting and replying — made for shops, clinics, gyms, salons and every local business.</T>
        </View>
        <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 16, justifyContent: 'center' }}>
          {FEATURES.map((f, i) => (
            <Rise key={f.t} i={i} style={{ width: wide ? (W - 32) / 3 : mid ? (W - 16) / 2 : W }}>
              <Card style={{ gap: 10, minHeight: 170 }} pad={22}>
                <View style={{ width: 50, height: 50, borderRadius: 16, backgroundColor: f.c + '22', alignItems: 'center', justifyContent: 'center' }}><Ionicons name={f.i} size={26} color={f.c} /></View>
                <T w="b" size={18}>{f.t}</T>
                <T s="mut" size={14} style={{ lineHeight: 21 }}>{f.d}</T>
              </Card>
            </Rise>
          ))}
        </View>
      </View>
      {/* steps */}
      <View style={{ width: W, backgroundColor: t.card2, borderRadius: 32, padding: wide ? 44 : 22, gap: 24, borderWidth: 1, borderColor: t.line }}>
        <T w="x" size={wide ? 32 : 24} style={{ textAlign: 'center' }}>Start in 3 easy steps</T>
        <View style={{ flexDirection: wide ? 'row' : 'column', gap: 16 }}>
          {STEPS.map((s) => (
            <View key={s.n} style={{ flex: 1, flexDirection: 'row', gap: 14, alignItems: 'flex-start' }}>
              <LinearGradient colors={['#FACC15', '#EAB308']} style={{ width: 46, height: 46, borderRadius: 23, alignItems: 'center', justifyContent: 'center' }}><T w="x" size={20} c="#2A2000">{s.n}</T></LinearGradient>
              <View style={{ flex: 1, gap: 4 }}><T w="b" size={17}>{s.t}</T><T s="mut" size={14}>{s.d}</T></View>
            </View>
          ))}
        </View>
      </View>
      {/* CTA */}
      <View style={{ width: W, paddingVertical: 50 }}>
        <LinearGradient colors={['#FACC15', '#EAB308']} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 32, padding: wide ? 44 : 24, flexDirection: wide ? 'row' : 'column', alignItems: 'center', gap: 18, justifyContent: 'space-between' }}>
          <View style={{ gap: 6, flex: wide ? 1 : undefined }}>
            <T w="x" size={wide ? 30 : 23} c="#2A2000">Ready to put your page on autopilot?</T>
            <T size={15} c="#3F3200">Sign up with your Gmail. ShriTech will call you and set everything up.</T>
          </View>
          <View style={{ flexDirection: 'row', gap: 10, flexWrap: 'wrap' }}>
            <Btn title="Start now" icon="arrow-forward" onPress={onStart} />
            <Btn title="Call 99936 15146" icon="call" kind="outline" onPress={() => Linking.openURL('tel:9993615146')} style={{ borderColor: '#14532D' }} />
          </View>
        </LinearGradient>
      </View>
      <View style={{ width: W, paddingBottom: 40, alignItems: 'center', gap: 6 }}>
        <Logo size={22} />
        <T s="mut" size={13} style={{ textAlign: 'center' }}>Shri Balaji Digital Services · 📞 99936 15146 · AutoPost for Facebook & Instagram</T>
      </View>
    </ScrollView>
  );
}
