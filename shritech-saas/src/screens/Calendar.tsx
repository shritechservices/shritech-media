import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Animated, Platform, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Card, Empty, Hero, PlatformIcons, Pill, Press, Rise, Screen, Skel, T, Thumb, useStatus, Btn, Cols, useWide } from '../ui';
import { useTheme } from '../theme';
import { useOverview } from '../data';
import { dayKey, MONTHS, monthStartISO, nowYM, timeStr, ist, dateStr } from '../time';

const W7 = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
const W7L = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export default function Calendar({ navigation, route }: any) {
  const { t } = useTheme(); const stat = useStatus(); const wide = useWide(); const CH = wide ? 96 : 52;
  const [ym, setYm] = useState(nowYM());
  const todayK = dayKey(Date.now());
  const [sel, setSel] = useState<string>(route?.params?.day ?? todayK);
  useEffect(() => { if (route?.params?.day) { const d = route.params.day as string; setSel(d); setYm({ y: +d.slice(0, 4), m: +d.slice(5, 7) - 1 }); } }, [route?.params?.day]);
  const ov = useOverview(() => {
    const from = new Date(Math.min(new Date(monthStartISO(ym.y, ym.m)).getTime(), Date.now() - 30 * 86400000)).toISOString();
    const to = monthStartISO(ym.m === 11 ? ym.y + 1 : ym.y, (ym.m + 1) % 12);
    return { from, to: new Date(Math.max(new Date(to).getTime(), Date.now())).toISOString() };
  }, [ym.y, ym.m]);
  const byDay = useMemo(() => { const o: Record<string, typeof ov.posts> = {}; ov.posts.forEach((p) => { (o[dayKey(p.scheduled_at)] ??= []).push(p); }); return o; }, [ov.posts]);
  const fade = useRef(new Animated.Value(1)).current;
  const move = (k: number) => {
    Animated.timing(fade, { toValue: 0, duration: 120, useNativeDriver: Platform.OS !== 'web' }).start(() => {
      setYm(({ y, m }) => { let mm = m + k, yy = y; if (mm < 0) { mm = 11; yy--; } if (mm > 11) { mm = 0; yy++; } return { y: yy, m: mm }; });
      Animated.timing(fade, { toValue: 1, duration: 220, useNativeDriver: Platform.OS !== 'web' }).start();
    });
  };
  const first = new Date(Date.UTC(ym.y, ym.m, 1)); const lead = (first.getUTCDay() + 6) % 7; const nd = new Date(Date.UTC(ym.y, ym.m + 1, 0)).getUTCDate();
  const cells: (number | null)[] = [...Array(lead).fill(null), ...Array.from({ length: nd }, (_, i) => i + 1)];
  while (cells.length % 7) cells.push(null);
  const key = (d: number) => `${ym.y}-${String(ym.m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
  const list = (byDay[sel] ?? []).filter((p) => p.status !== 'cancelled' || true);
  const monthCount = ov.posts.filter((p) => { const x = ist(p.scheduled_at); return x.getUTCFullYear() === ym.y && x.getUTCMonth() === ym.m && p.status === 'scheduled'; }).length;
  const isPast = sel < todayK;

  return (
    <Screen onRefresh={ov.reload} refreshing={ov.refreshing} header={
      <Hero>
        <T w="b" size={24} c="#fff">Calendar</T>
        <T size={13} c="rgba(255,255,255,0.85)">{monthCount} scheduled this month · {ov.upcoming} in total · India time</T>
      </Hero>
    }>
      <Cols ratio={2.1} left={<>
      <Rise>
        <Card pad={wide ? 20 : 14}>
          <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
            <Press onPress={() => move(-1)} style={{ width: 38, height: 38, borderRadius: 12, backgroundColor: t.card2, alignItems: 'center', justifyContent: 'center' }}><Ionicons name="chevron-back" size={20} color={t.text} /></Press>
            <Press onPress={() => { setYm(nowYM()); setSel(todayK); }}><T w="b" size={17}>{MONTHS[ym.m]} {ym.y}</T></Press>
            <Press onPress={() => move(1)} style={{ width: 38, height: 38, borderRadius: 12, backgroundColor: t.card2, alignItems: 'center', justifyContent: 'center' }}><Ionicons name="chevron-forward" size={20} color={t.text} /></Press>
          </View>
          <View style={{ flexDirection: 'row' }}>{(wide ? W7L : W7).map((d, i) => <T key={i} s="mut" w="s" size={12} style={{ flex: 1, textAlign: 'center' }}>{d}</T>)}</View>
          <Animated.View style={{ opacity: fade, flexDirection: 'row', flexWrap: 'wrap', marginTop: 6 }}>
            {cells.map((d, i) => {
              if (!d) return <View key={i} style={{ width: `${100 / 7}%`, height: CH }} />;
              const k = key(d); const ps = (byDay[k] ?? []).filter((p) => p.status !== 'cancelled'); const on = k === sel; const today = k === todayK; const past = k < todayK;
              return (
                <View key={i} style={{ width: `${100 / 7}%`, height: CH, padding: wide ? 3 : 2 }}>
                  <Press onPress={() => setSel(k)} haptic style={{ flex: 1, borderRadius: 14, alignItems: wide ? 'flex-start' : 'center', justifyContent: wide ? 'flex-start' : 'center', padding: wide ? 8 : 0, ...(wide && !on && !today ? { borderWidth: 1, borderColor: t.line } : {}), backgroundColor: on ? t.green : today ? t.goldSoft : 'transparent', borderWidth: today && !on ? 1.5 : 0, borderColor: t.gold }}>
                    <T w={on || today ? 'b' : 'm'} size={14} c={on ? t.onGreen : past ? t.mut : t.text}>{d}</T>
                    {wide ? (
                      <View style={{ gap: 3, marginTop: 4, width: '100%' }}>
                        {ps.slice(0, 2).map((p) => <View key={p.id} style={{ flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: on ? 'rgba(255,255,255,0.2)' : p.status === 'failed' ? t.redSoft : p.media?.kind === 'image' ? t.goldSoft : t.chip, borderRadius: 6, paddingHorizontal: 5, paddingVertical: 2 }}><T w="s" size={10} c={on ? '#fff' : p.status === 'failed' ? t.red : p.media?.kind === 'image' ? t.gold : t.green} lines={1} style={{ flex: 1 }}>{timeStr(p.scheduled_at)} {p.title || p.media?.title || ''}</T></View>)}
                        {ps.length > 2 ? <T size={10} c={on ? '#fff' : t.mut}>+{ps.length - 2} more</T> : null}
                      </View>
                    ) : (
                    <View style={{ flexDirection: 'row', gap: 2, height: 6, marginTop: 1 }}>
                      {ps.slice(0, 3).map((p) => <View key={p.id} style={{ width: 5, height: 5, borderRadius: 3, backgroundColor: on ? '#fff' : p.status === 'failed' ? t.red : p.media?.kind === 'image' ? t.gold : t.green }} />)}
                    </View>
                    )}
                  </Press>
                </View>
              );
            })}
          </Animated.View>
          <View style={{ flexDirection: 'row', gap: 14, marginTop: 8, justifyContent: 'center' }}>
            {[{ c: t.green, l: 'Reel' }, { c: t.gold, l: 'Image' }, { c: t.red, l: 'Not posted' }].map((x) => (
              <View key={x.l} style={{ flexDirection: 'row', gap: 5, alignItems: 'center' }}><View style={{ width: 8, height: 8, borderRadius: 4, backgroundColor: x.c }} /><T s="mut" size={11}>{x.l}</T></View>
            ))}
          </View>
        </Card>
      </Rise>

      </>} right={<>
      <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
        <T w="b" size={17}>{sel === todayK ? 'Today' : dateStr(sel + 'T06:30:00Z')}</T>
        {!isPast ? <Btn small title="Add post" icon="add" kind="gold" onPress={() => navigation.navigate('New', { day: sel })} /> : null}
      </View>
      {ov.loading ? <Skel h={90} /> : list.length === 0 ? (
        <Card><Empty icon="calendar-clear-outline" title={isPast ? 'No posts on this day' : 'Free day'} sub={isPast ? undefined : 'Tap “Add post” to schedule something here.'} /></Card>
      ) : list.map((p, i) => {
        const s = stat(p.status);
        return (
          <Rise key={p.id + sel} i={i}>
            <Press onPress={() => navigation.navigate('Post', { post: p })}>
              <Card pad={10} style={{ flexDirection: 'row', gap: 12, alignItems: 'center' }}>
                <Thumb m={p.media} w={62} h={82} />
                <View style={{ flex: 1, gap: 5 }}>
                  <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}><Ionicons name="time-outline" size={14} color={t.green} /><T w="b" size={14} c={t.green}>{timeStr(p.scheduled_at)}</T></View>
                  <T w="s" size={14} lines={2}>{p.title || p.media?.title || 'Post'}</T>
                  <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}><Pill label={s.label} color={s.c} bg={s.bg} icon={s.icon} /><PlatformIcons list={p.platforms} /></View>
                </View>
                <Ionicons name="chevron-forward" size={18} color={t.mut} />
              </Card>
            </Press>
          </Rise>
        );
      })}
      </>} />
    </Screen>
  );
}
