import React, { useEffect, useState } from 'react';
import { View, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { Btn, Card, CountUp, Empty, Hero, Logo, PlatformIcons, Press, Rise, Screen, SectionTitle, Skel, T, Thumb, Pill, useStatus, sh } from '../ui';
import { useTheme } from '../theme';
import { useOverview, getMe, Me } from '../data';
import { isDemo } from '../api';
import { dayKey, DOW, greet, ist, timeStr, dateStr } from '../time';
import type { Post } from '../types';

function Countdown({ to }: { to: string }) {
  const [n, setN] = useState(Date.now());
  useEffect(() => { const iv = setInterval(() => setN(Date.now()), 1000); return () => clearInterval(iv); }, []);
  let s = Math.max(0, Math.floor((new Date(to).getTime() - n) / 1000));
  const d = Math.floor(s / 86400); s %= 86400; const h = Math.floor(s / 3600); s %= 3600; const m = Math.floor(s / 60); s %= 60;
  const box = (v: number, l: string) => (
    <View style={{ alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.16)', borderRadius: 12, paddingVertical: 6, minWidth: 54 }}>
      <T w="b" size={20} c="#fff">{String(v).padStart(2, '0')}</T><T size={10} c="rgba(255,255,255,0.8)">{l}</T>
    </View>
  );
  return <View style={{ flexDirection: 'row', gap: 8 }}>{box(d, 'days')}{box(h, 'hrs')}{box(m, 'min')}{box(s, 'sec')}</View>;
}

export default function Home({ navigation }: any) {
  const { t } = useTheme(); const stat = useStatus();
  const { posts, upcoming, loading, refreshing, reload } = useOverview(() => ({ from: new Date(Date.now() - 30 * 86400000).toISOString(), to: new Date(Date.now() + 31 * 86400000).toISOString() }));
  const [me, setMe] = useState<Me | null>(null);
  useEffect(() => { const u = navigation.addListener('focus', () => getMe(true).then(setMe).catch(() => {})); getMe().then(setMe).catch(() => {}); return u; }, []);
  const conn = me?.tenant.connected ? (me.tenant.page_name || 'Connected') : '';
  const ten = me?.tenant;
  const now = Date.now();
  const next = posts.filter((p) => p.status === 'scheduled' && new Date(p.scheduled_at).getTime() >= now - 60000)[0];
  const past = posts.filter((p) => new Date(p.scheduled_at).getTime() < now && p.status !== 'scheduled').reverse();
  const posted = past.filter((p) => p.status === 'posted' || p.status === 'partial').length;
  const failed = past.filter((p) => p.status === 'failed').length;
  // next 7 days strip
  const week = Array.from({ length: 7 }, (_, i) => { const d = now + i * 86400000; const k = dayKey(d); return { d, k, list: posts.filter((p) => dayKey(p.scheduled_at) === k && p.status !== 'cancelled') }; });
  const open = (p: Post) => navigation.navigate('Post', { post: p });

  const stats = [
    { n: upcoming, l: 'Scheduled', icon: 'calendar' as const, c: t.green, bg: t.chip },
    { n: posted, l: 'Posted', icon: 'checkmark-done' as const, c: t.gold, bg: t.goldSoft },
    { n: failed, l: 'Not posted', icon: 'alert-circle' as const, c: t.red, bg: t.redSoft },
  ];
  return (
    <Screen onRefresh={reload} refreshing={refreshing} header={
      <Hero>
        <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
          <Logo size={26} light />
          <View style={{ flexDirection: 'row', gap: 10, alignItems: 'center' }}>
            {isDemo() ? <Pill label="DEMO" color="#2A2000" bg="#FACC15" icon="sparkles" /> : null}
            <Press onPress={() => navigation.navigate('Account')} style={{ width: 40, height: 40, borderRadius: 20, backgroundColor: 'rgba(255,255,255,0.16)', alignItems: 'center', justifyContent: 'center' }}>
              <Ionicons name="settings-outline" size={21} color="#fff" />
            </Press>
          </View>
        </View>
        <Rise i={1}><T w="m" size={15} c="rgba(255,255,255,0.85)" style={{ marginTop: 18 }}>{greet()} 👋</T></Rise>
        <Rise i={2}><T w="b" size={24} c="#fff">{ten?.name ?? 'Your posts are on autopilot'}</T></Rise>
        {next ? (
          <Rise i={3}>
            <Press onPress={() => open(next)} style={{ marginTop: 16, backgroundColor: 'rgba(0,0,0,0.18)', borderRadius: 20, padding: 14, gap: 10 }}>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                <Ionicons name="flash" size={15} color="#FACC15" /><T w="s" size={12} c="#FACC15">NEXT POST GOES LIVE IN</T>
              </View>
              <Countdown to={next.scheduled_at} />
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                <PlatformIcons list={next.platforms} />
                <T w="m" size={13} c="#fff" lines={1} style={{ flex: 1 }}>{next.title || next.media?.title || 'Post'} · {dateStr(next.scheduled_at)}, {timeStr(next.scheduled_at)}</T>
              </View>
            </Press>
          </Rise>
        ) : null}
      </Hero>
    }>
      {ten && !ten.live ? (
        <Rise>
          <Card style={{ gap: 10, borderColor: t.gold, borderWidth: 1.5 }}>
            <View style={{ flexDirection: 'row', gap: 10, alignItems: 'center' }}>
              <View style={{ width: 44, height: 44, borderRadius: 14, backgroundColor: t.goldSoft, alignItems: 'center', justifyContent: 'center' }}><Ionicons name={ten.status === 'pending' ? 'construct' : 'pause-circle'} size={22} color={t.gold} /></View>
              <View style={{ flex: 1 }}><T w="b" size={16}>{ten.status === 'pending' ? 'Setting up your account' : 'Your plan is paused'}</T><T s="mut" size={12}>{ten.status === 'pending' ? 'ShriTech will connect your Facebook Page & Instagram' : 'Contact ShriTech to continue posting'}</T></View>
            </View>
            {ten.status === 'pending' ? [
              ['checkmark-circle', 'Account created', true],
              [ten.request_note ? 'checkmark-circle' : 'ellipse-outline', 'Send your Facebook Page & Instagram details', !!ten.request_note],
              [ten.connected ? 'checkmark-circle' : 'ellipse-outline', 'ShriTech connects your accounts', ten.connected],
              ['ellipse-outline', 'Start posting 🚀', false],
            ].map(([i, l, ok]: any) => <View key={l} style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}><Ionicons name={i} size={18} color={ok ? t.green : t.mut} /><T size={13} c={ok ? t.text : t.mut}>{l}</T></View>) : null}
            <Btn small title={ten.status === 'pending' ? 'Send my details' : 'Call 99936 15146'} icon={ten.status === 'pending' ? 'paper-plane-outline' : 'call-outline'} kind="gold" onPress={() => ten.status === 'pending' ? navigation.navigate('Account') : require('react-native').Linking.openURL('tel:9993615146')} />
          </Card>
        </Rise>
      ) : null}
      <View style={{ flexDirection: 'row', gap: 10 }}>
        {stats.map((s, i) => (
          <Rise key={s.l} i={i} style={{ flex: 1 }}>
            <Card pad={12} style={{ gap: 6 }}>
              <View style={{ width: 34, height: 34, borderRadius: 12, backgroundColor: s.bg, alignItems: 'center', justifyContent: 'center' }}><Ionicons name={s.icon} size={18} color={s.c} /></View>
              {loading ? <Skel h={30} r={8} /> : <CountUp to={s.n} size={26} c={s.c} />}
              <T s="mut" size={11} lines={1}>{s.l}</T>
            </Card>
          </Rise>
        ))}
      </View>

      <Rise i={3}>
        <Card pad={14} style={{ flexDirection: 'row', alignItems: 'center', gap: 12 }}>
          <View style={{ width: 42, height: 42, borderRadius: 14, backgroundColor: conn ? t.chip : t.redSoft, alignItems: 'center', justifyContent: 'center' }}>
            <Ionicons name={conn ? 'link' : 'unlink'} size={20} color={conn ? t.green : t.red} />
          </View>
          <View style={{ flex: 1 }}>
            <T w="s" size={14}>{conn ? 'Facebook + Instagram connected' : 'Checking connection…'}</T>
            <T s="mut" size={12} lines={1}>{conn || 'Your Meta accounts'}</T>
          </View>
          <PlatformIcons list={['facebook', 'instagram']} size={20} />
        </Card>
      </Rise>

      <SectionTitle title="Next 7 days" action="Calendar" onAction={() => navigation.navigate('Calendar')} />
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 10, paddingRight: 10 }}>
        {week.map((w, i) => {
          const x = ist(w.d); const today = i === 0;
          return (
            <Rise key={w.k} i={i} from={10}>
              <Press onPress={() => navigation.navigate('Calendar', { day: w.k })}>
                {today ? (
                  <LinearGradient colors={[t.green, t.deep]} style={[{ width: 66, borderRadius: 18, paddingVertical: 12, alignItems: 'center', gap: 2 }, sh(t.green, 0.3)]}>
                    <T w="m" size={11} c="#fff">Today</T><T w="b" size={22} c="#fff">{x.getUTCDate()}</T>
                    <View style={{ flexDirection: 'row', gap: 3, height: 8 }}>{w.list.slice(0, 3).map((p) => <View key={p.id} style={{ width: 7, height: 7, borderRadius: 4, backgroundColor: '#FACC15' }} />)}</View>
                  </LinearGradient>
                ) : (
                  <View style={{ width: 66, borderRadius: 18, paddingVertical: 12, alignItems: 'center', gap: 2, backgroundColor: t.card, borderWidth: 1, borderColor: t.line }}>
                    <T s="mut" w="m" size={11}>{DOW[x.getUTCDay()]}</T><T w="b" size={22}>{x.getUTCDate()}</T>
                    <View style={{ flexDirection: 'row', gap: 3, height: 8 }}>{w.list.slice(0, 3).map((p) => <View key={p.id} style={{ width: 7, height: 7, borderRadius: 4, backgroundColor: p.media?.kind === 'image' ? t.gold : t.green }} />)}</View>
                  </View>
                )}
              </Press>
            </Rise>
          );
        })}
      </ScrollView>

      <View style={{ flexDirection: 'row', gap: 10 }}>
        {[{ l: 'New post', i: 'add-circle' as const, go: 'New', c: t.green }, { l: 'Upload', i: 'cloud-upload' as const, go: 'Library', c: t.gold }, { l: 'Auto replies', i: 'chatbubbles' as const, go: 'Replies', c: t.pink }].map((a, i) => (
          <Rise key={a.l} i={i + 2} style={{ flex: 1 }}>
            <Press onPress={() => navigation.navigate(a.go)}>
              <Card pad={14} style={{ alignItems: 'center', gap: 8 }}>
                <Ionicons name={a.i} size={28} color={a.c} /><T w="s" size={12}>{a.l}</T>
              </Card>
            </Press>
          </Rise>
        ))}
      </View>

      <SectionTitle title="Recent activity" />
      {loading ? <><Skel /><Skel /></> : past.length === 0 ? <Card><Empty icon="time-outline" title="Nothing posted yet" sub="Posted items from the last 30 days show here." /></Card> : past.slice(0, 6).map((p, i) => {
        const s = stat(p.status);
        return (
          <Rise key={p.id} i={i}>
            <Press onPress={() => open(p)}>
              <Card pad={10} style={{ flexDirection: 'row', gap: 12, alignItems: 'center' }}>
                <Thumb m={p.media} w={54} h={70} />
                <View style={{ flex: 1, gap: 4 }}>
                  <T w="s" size={14} lines={1}>{p.title || p.media?.title || 'Post'}</T>
                  <T s="mut" size={12}>{dateStr(p.scheduled_at)} · {timeStr(p.scheduled_at)}</T>
                  <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}><Pill label={s.label} color={s.c} bg={s.bg} icon={s.icon} /><PlatformIcons list={p.platforms} /></View>
                </View>
                <Ionicons name="chevron-forward" size={18} color={t.mut} />
              </Card>
            </Press>
          </Rise>
        );
      })}
    </Screen>
  );
}
