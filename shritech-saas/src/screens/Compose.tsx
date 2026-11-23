import React, { useEffect, useRef, useState } from 'react';
import { Animated, Easing, Platform, ScrollView, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { Btn, Card, Field, Hero, Press, Rise, Screen, SectionTitle, Skel, T, Thumb, useToast, Empty, Cols, useWide } from '../ui';
import { useTheme } from '../theme';
import { api, uploadFile } from '../api';
import { getSettings } from '../data';
import { DOW, fromIST, ist, MON, timeStr, dateStr } from '../time';
import type { Media, Post } from '../types';

const PRESETS = [[9, 0], [12, 0], [15, 0], [17, 30], [18, 0], [19, 0], [21, 0]];

function Success({ onClose, when }: { onClose: () => void; when: string }) {
  const { t } = useTheme(); const a = useRef(new Animated.Value(0)).current; const r = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    Animated.spring(a, { toValue: 1, useNativeDriver: Platform.OS !== 'web', bounciness: 16, speed: 5 }).start();
    Animated.loop(Animated.timing(r, { toValue: 1, duration: 2400, easing: Easing.linear, useNativeDriver: Platform.OS !== 'web' })).start();
  }, []);
  return (
    <View style={{ flex: 1, backgroundColor: t.bg, alignItems: 'center', justifyContent: 'center', padding: 30, gap: 16 }}>
      <Animated.View style={{ transform: [{ scale: a }] }}>
        <View style={{ width: 150, height: 150, borderRadius: 75, backgroundColor: t.chip, alignItems: 'center', justifyContent: 'center' }}>
          <Animated.View style={{ position: 'absolute', width: 150, height: 150, borderRadius: 75, borderWidth: 3, borderColor: t.gold, borderStyle: 'dashed', transform: [{ rotate: r.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '360deg'] }) }] }} />
          <View style={{ width: 100, height: 100, borderRadius: 50, backgroundColor: t.green, alignItems: 'center', justifyContent: 'center' }}><Ionicons name="checkmark" size={60} color="#fff" /></View>
        </View>
      </Animated.View>
      <Rise i={3}><T w="b" size={24} style={{ textAlign: 'center' }}>Scheduled! 🎉</T></Rise>
      <Rise i={4}><T s="mut" size={15} style={{ textAlign: 'center' }}>It will go live on {dateStr(when, true)} at {timeStr(when)} — automatically.</T></Rise>
      <Rise i={5} style={{ alignSelf: 'stretch' }}><Btn title="Done" onPress={onClose} /></Rise>
    </View>
  );
}

export default function Compose({ route, navigation }: any) {
  const { t } = useTheme(); const toast = useToast(); const wide = useWide();
  const edit: Post | undefined = route?.params?.edit;
  const [media, setMedia] = useState<Media[]>([]); const [loadingM, setLoadingM] = useState(true);
  const [pick, setPick] = useState<string | null>(edit?.media_id ?? edit?.media?.id ?? null);
  const [title, setTitle] = useState(edit?.title ?? ''); const [cap, setCap] = useState(edit?.caption ?? '');
  const [plat, setPlat] = useState<string[]>(edit?.platforms ?? ['facebook', 'instagram']);
  const [collab, setCollab] = useState((edit?.collaborators ?? []).join(', '));
  const base = edit ? ist(edit.scheduled_at) : ist(Date.now() + 86400000);
  const [day, setDay] = useState({ y: base.getUTCFullYear(), m: base.getUTCMonth(), d: base.getUTCDate() });
  const [hm, setHm] = useState<[number, number]>(edit ? [base.getUTCHours(), base.getUTCMinutes()] : [18, 0]);
  const [busy, setBusy] = useState(false); const [up, setUp] = useState(0); const [done, setDone] = useState<string | null>(null);

  const loadMedia = async () => { setLoadingM(true); try { setMedia(await api<Media[]>('list_media', { all: true })); } catch { } finally { setLoadingM(false); } };
  useEffect(() => { loadMedia(); if (!edit) getSettings().then((s) => setCap((c) => c || (s.default_caption ?? ''))).catch(() => {}); }, []);
  useEffect(() => {
    const d = route?.params?.day as string | undefined;
    if (d) setDay({ y: +d.slice(0, 4), m: +d.slice(5, 7) - 1, d: +d.slice(8, 10) });
    if (route?.params?.mediaId) setPick(route.params.mediaId);
  }, [route?.params?.day, route?.params?.mediaId]);

  const days = Array.from({ length: 75 }, (_, i) => { const x = ist(Date.now() + i * 86400000); return { y: x.getUTCFullYear(), m: x.getUTCMonth(), d: x.getUTCDate(), w: x.getUTCDay() }; });
  const whenISO = fromIST(day.y, day.m, day.d, hm[0], hm[1]);
  const inPast = new Date(whenISO).getTime() < Date.now();

  const uploadNew = async () => {
    const r = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images', 'videos'], quality: 1 });
    if (r.canceled || !r.assets?.[0]) return;
    const a = r.assets[0]; const isVid = a.type === 'video';
    if ((a.fileSize ?? 0) > 50 * 1048576) { toast('Please choose a file under 50 MB', false); return; }
    setUp(0.01);
    try {
      const m: any = await uploadFile({ uri: a.uri, name: a.fileName ?? (isVid ? 'reel.mp4' : 'image.jpg'), mime: a.mimeType ?? (isVid ? 'video/mp4' : 'image/jpeg'), size: a.fileSize }, title, setUp);
      toast('Uploaded to your library'); await loadMedia(); if (m?.id) setPick(m.id);
    } catch (e: any) { toast(e.message, false); } finally { setUp(0); }
  };

  const save = async () => {
    if (!pick) { toast('Please choose a reel or image first', false); return; }
    if (!plat.length) { toast('Pick Facebook, Instagram or both', false); return; }
    if (inPast) { toast('Please pick a time in the future', false); return; }
    setBusy(true);
    try {
      const body = { media_id: pick, title: title || media.find((x) => x.id === pick)?.title || 'Post', caption: cap, platforms: plat, scheduled_at: whenISO, collaborators: collab };
      if (edit) { await api('update_post', { id: edit.id, ...body }); toast('Post updated'); navigation.goBack(); }
      else { await api('create_post', body); setDone(whenISO); }
    } catch (e: any) { toast(e.message, false); } finally { setBusy(false); }
  };
  if (done) return <Success when={done} onClose={() => { setDone(null); setPick(null); setTitle(''); navigation.navigate('Calendar'); }} />;

  const togglePlat = (p: string) => setPlat((x) => (x.includes(p) ? x.filter((y) => y !== p) : [...x, p]));
  return (
    <Screen header={
      <Hero>
        {edit ? <Press onPress={() => navigation.goBack()} style={{ marginBottom: 8 }}><Ionicons name="arrow-back" size={24} color="#fff" /></Press> : null}
        <T w="b" size={24} c="#fff">{edit ? 'Edit post' : 'New post'}</T>
        <T size={13} c="rgba(255,255,255,0.85)">Choose · write · pick a time. We post it for you.</T>
      </Hero>
    }>
      <Cols ratio={1.25} left={<>
      <Rise>
        <SectionTitle title="1 · Choose reel or image" />
      </Rise>
      <Rise i={1}>
        <ScrollView horizontal={!wide} showsHorizontalScrollIndicator={false} style={wide ? { maxHeight: 440 } : undefined} contentContainerStyle={{ gap: 10, paddingVertical: 4, ...(wide ? { flexWrap: 'wrap', flexDirection: 'row' } : {}) }}>
          {!edit ? (
            <Press onPress={uploadNew} style={{ width: 96, height: 132, borderRadius: 16, borderWidth: 2, borderStyle: 'dashed', borderColor: t.green, alignItems: 'center', justifyContent: 'center', gap: 6, backgroundColor: t.chip }}>
              {up > 0 ? <T w="b" size={18} c={t.green}>{Math.round(up * 100)}%</T> : <Ionicons name="cloud-upload" size={28} color={t.green} />}
              <T w="s" size={11} c={t.green}>{up > 0 ? 'Uploading' : 'Upload new'}</T>
            </Press>
          ) : null}
          {loadingM ? [0, 1, 2].map((i) => <View key={i} style={{ width: 96 }}><Skel h={132} r={16} /></View>) : media.map((m) => {
            const on = pick === m.id;
            return (
              <Press key={m.id} onPress={() => { setPick(m.id); if (!title) setTitle(m.title ?? ''); }} style={{ width: 96, gap: 4 }}>
                <View style={{ borderRadius: 18, borderWidth: 3, borderColor: on ? t.gold : 'transparent' }}>
                  <Thumb m={m} w={90} h={126} r={14} />
                  {on ? <View style={{ position: 'absolute', top: 6, right: 6, backgroundColor: t.gold, borderRadius: 12, padding: 2 }}><Ionicons name="checkmark" size={16} color="#2A2000" /></View> : null}
                </View>
                <T size={11} lines={1} s="mut">{m.title || 'Untitled'}</T>
              </Press>
            );
          })}
        </ScrollView>
        {!loadingM && media.length === 0 ? <Empty icon="images-outline" title="Library is empty" sub="Upload a reel or image to get started." /> : null}
      </Rise>

      <Rise i={2}><SectionTitle title="2 · Write" /></Rise>
      <Rise i={3}>
        <Card style={{ gap: 12 }}>
          <Field label="Title (only for you)" value={title} onChange={setTitle} placeholder="e.g. Diwali reel – sweets shop" />
          <Field label="Caption" value={cap} onChange={setCap} multiline placeholder="Write your caption, number and hashtags…" />
          <Field label="Collab with (Instagram usernames, max 3)" value={collab} onChange={setCollab} placeholder="e.g. shreebalaji.digital_" />
          {!collab.includes('shreebalaji.digital_') ? (
            <Press onPress={() => setCollab((c) => (c ? c + ', ' : '') + 'shreebalaji.digital_')} style={{ alignSelf: 'flex-start', flexDirection: 'row', gap: 5, alignItems: 'center', backgroundColor: t.chip, borderRadius: 99, paddingHorizontal: 12, paddingVertical: 6 }}>
              <Ionicons name="add" size={14} color={t.green} /><T w="s" size={12} c={t.green}>@shreebalaji.digital_</T>
            </Press>
          ) : null}
        </Card>
      </Rise>

      </>} right={<>
      <Rise i={4}><SectionTitle title="3 · Where" /></Rise>
      <Rise i={5}>
        <View style={{ flexDirection: 'row', gap: 10 }}>
          {[{ k: 'facebook', l: 'Facebook', i: 'logo-facebook' as const, c: '#1877F2' }, { k: 'instagram', l: 'Instagram', i: 'logo-instagram' as const, c: '#DD2A7B' }].map((x) => {
            const on = plat.includes(x.k);
            return (
              <Press key={x.k} onPress={() => togglePlat(x.k)} style={{ flex: 1 }}>
                <Card pad={14} style={{ flexDirection: 'row', alignItems: 'center', gap: 10, borderColor: on ? x.c : t.line, borderWidth: on ? 2 : 1 }}>
                  <Ionicons name={x.i} size={24} color={on ? x.c : t.mut} /><T w="s" size={14} style={{ flex: 1 }}>{x.l}</T>
                  <Ionicons name={on ? 'checkmark-circle' : 'ellipse-outline'} size={22} color={on ? x.c : t.mut} />
                </Card>
              </Press>
            );
          })}
        </View>
      </Rise>

      <Rise i={6}><SectionTitle title="4 · When (India time)" /></Rise>
      <Rise i={7}>
        <ScrollView horizontal={!wide} showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8, ...(wide ? { flexWrap: 'wrap', flexDirection: 'row' } : {}) }}>
          {days.map((d, i) => {
            const on = d.y === day.y && d.m === day.m && d.d === day.d;
            return (
              <Press key={i} onPress={() => setDay(d)} style={{ width: 58, paddingVertical: 10, borderRadius: 16, alignItems: 'center', backgroundColor: on ? t.green : t.card, borderWidth: 1, borderColor: on ? t.green : t.line }}>
                <T w="m" size={11} c={on ? t.onGreen : t.mut}>{i === 0 ? 'Today' : DOW[d.w]}</T>
                <T w="b" size={19} c={on ? t.onGreen : t.text}>{d.d}</T>
                <T size={10} c={on ? t.onGreen : t.mut}>{MON[d.m]}</T>
              </Press>
            );
          })}
        </ScrollView>
      </Rise>
      <Rise i={8}>
        <Card style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
            {PRESETS.map(([h, m]) => {
              const on = hm[0] === h && hm[1] === m;
              return <Press key={`${h}${m}`} onPress={() => setHm([h, m])} style={{ paddingHorizontal: 14, paddingVertical: 8, borderRadius: 99, backgroundColor: on ? t.gold : t.card2, borderWidth: 1, borderColor: on ? t.gold : t.line }}><T w="s" size={13} c={on ? t.onGold : t.text}>{timeStr(fromIST(2026, 0, 1, h, m))}</T></Press>;
            })}
          </View>
          <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 14 }}>
            {[{ l: 'Hour', v: hm[0], set: (k: number) => setHm(([h, m]) => [(h + k + 24) % 24, m]) }, { l: 'Minute', v: hm[1], set: (k: number) => setHm(([h, m]) => [h, (m + k * 5 + 60) % 60]) }].map((x) => (
              <View key={x.l} style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                <Press onPress={() => x.set(-1)} style={{ width: 36, height: 36, borderRadius: 18, backgroundColor: t.card2, alignItems: 'center', justifyContent: 'center' }}><Ionicons name="remove" size={18} color={t.text} /></Press>
                <View style={{ alignItems: 'center', minWidth: 44 }}><T w="b" size={20}>{String(x.v).padStart(2, '0')}</T><T s="mut" size={10}>{x.l}</T></View>
                <Press onPress={() => x.set(1)} style={{ width: 36, height: 36, borderRadius: 18, backgroundColor: t.card2, alignItems: 'center', justifyContent: 'center' }}><Ionicons name="add" size={18} color={t.text} /></Press>
              </View>
            ))}
          </View>
          <View style={{ backgroundColor: inPast ? t.redSoft : t.chip, borderRadius: 12, padding: 10, flexDirection: 'row', gap: 8, alignItems: 'center' }}>
            <Ionicons name={inPast ? 'alert-circle' : 'rocket'} size={18} color={inPast ? t.red : t.green} />
            <T w="m" size={13} style={{ flex: 1 }}>{inPast ? 'This time has already passed — pick a later time.' : `Goes live ${dateStr(whenISO, true)} at ${timeStr(whenISO)}`}</T>
          </View>
        </Card>
      </Rise>
      <Rise i={9}><Btn title={edit ? 'Save changes' : 'Schedule post'} icon={edit ? 'save-outline' : 'paper-plane'} kind="gold" onPress={save} loading={busy} /></Rise>
      </>} />
    </Screen>
  );
}
