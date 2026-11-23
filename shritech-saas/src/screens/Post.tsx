import React, { useState } from 'react';
import { Image, Linking, View, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useVideoPlayer, VideoView } from 'expo-video';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Btn, Card, PlatformIcons, Pill, Press, Rise, T, useConfirm, useStatus, useToast } from '../ui';
import { useTheme } from '../theme';
import { api, previewUrl } from '../api';
import { dateStr, timeStr } from '../time';
import type { Post } from '../types';

function Player({ url }: { url: string }) {
  const player = useVideoPlayer(url, (p) => { p.loop = true; p.muted = false; });
  return <VideoView player={player} style={{ width: '100%', height: '100%' }} contentFit="cover" nativeControls />;
}

export default function PostScreen({ route, navigation }: any) {
  const { t } = useTheme(); const ins = useSafeAreaInsets(); const stat = useStatus(); const toast = useToast(); const confirm = useConfirm();
  const [p, setP] = useState<Post>(route.params.post); const [busy, setBusy] = useState('');
  const s = stat(p.status); const m = p.media;
  const act = async (k: string, fn: () => Promise<any>, msg: string, after?: Partial<Post>) => {
    setBusy(k);
    try { await fn(); toast(msg); if (after) setP({ ...p, ...after }); } catch (e: any) { toast(e.message, false); } finally { setBusy(''); }
  };
  const postNow = async () => {
    if (!(await confirm({ title: 'Post right now?', msg: 'This will publish immediately on ' + p.platforms.map((x) => (x === 'facebook' ? 'Facebook' : 'Instagram')).join(' and ') + '.', ok: 'Post now' }))) return;
    act('now', () => api('post_now', { id: p.id }), 'Publishing started 🚀', { status: 'publishing', scheduled_at: new Date().toISOString() });
  };
  const cancel = async () => {
    if (!(await confirm({ title: 'Cancel this post?', msg: 'It will not be published. The file stays in your library.', ok: 'Cancel post', danger: true }))) return;
    act('cancel', () => api('cancel_post', { id: p.id }), 'Post cancelled', { status: 'cancelled' });
  };
  const retry = () => act('retry', () => api('retry_post', { id: p.id }), 'Will try again in a moment', { status: 'scheduled', error: null });

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 40 }}>
        <View style={{ height: 430, backgroundColor: '#000' }}>
          {m?.poster ? <Image source={m.poster} style={{ width: '100%', height: '100%' }} resizeMode="cover" /> : m?.kind === 'video' ? <Player url={previewUrl(m.public_url)} /> : m ? <Image source={m.local ?? { uri: m.public_url }} style={{ width: '100%', height: '100%' }} resizeMode="cover" /> : null}
          <Press onPress={() => navigation.goBack()} style={{ position: 'absolute', top: ins.top + 10, left: 14, width: 42, height: 42, borderRadius: 21, backgroundColor: 'rgba(0,0,0,0.45)', alignItems: 'center', justifyContent: 'center' }}>
            <Ionicons name="chevron-down" size={24} color="#fff" />
          </Press>
        </View>
        <View style={{ padding: 16, gap: 14, marginTop: -26 }}>
          <Rise>
            <Card style={{ gap: 10 }}>
              <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}><Pill label={s.label} color={s.c} bg={s.bg} icon={s.icon} size={12} /><PlatformIcons list={p.platforms} size={18} /></View>
              <T w="b" size={20}>{p.title || m?.title || 'Post'}</T>
              <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}>
                <Ionicons name="calendar-outline" size={16} color={t.green} /><T w="m" size={14}>{dateStr(p.scheduled_at, true)}</T>
                <Ionicons name="time-outline" size={16} color={t.green} style={{ marginLeft: 6 }} /><T w="m" size={14}>{timeStr(p.scheduled_at)} IST</T>
              </View>
              {p.collaborators?.length ? <View style={{ flexDirection: 'row', gap: 6, alignItems: 'center' }}><Ionicons name="people-outline" size={16} color={t.pink} /><T size={13}>Collab: {p.collaborators.map((c) => '@' + c).join(', ')}</T></View> : null}
              {p.status === 'failed' || p.status === 'partial' ? (
                <View style={{ backgroundColor: t.redSoft, borderRadius: 12, padding: 10, flexDirection: 'row', gap: 8 }}>
                  <Ionicons name="information-circle" size={18} color={t.red} /><T size={13} style={{ flex: 1 }}>This post couldn’t go out everywhere. Tap “Try again” and we’ll post it in a moment.</T>
                </View>
              ) : null}
            </Card>
          </Rise>
          {(p.fb_link || p.ig_link) ? (
            <Rise i={1}>
              <View style={{ flexDirection: 'row', gap: 10 }}>
                {p.fb_link ? <Btn small kind="outline" icon="logo-facebook" title="View on Facebook" onPress={() => Linking.openURL(p.fb_link!)} style={{ flex: 1 }} /> : null}
                {p.ig_link ? <Btn small kind="outline" icon="logo-instagram" title="View on Instagram" onPress={() => Linking.openURL(p.ig_link!)} style={{ flex: 1 }} /> : null}
              </View>
            </Rise>
          ) : null}
          <Rise i={2}>
            <Card style={{ gap: 8 }}>
              <T w="b" size={15}>Caption</T>
              <T size={14} style={{ lineHeight: 22 }}>{p.caption || '—'}</T>
            </Card>
          </Rise>
          {p.status === 'scheduled' ? (
            <Rise i={3} style={{ gap: 10 }}>
              <Btn title="Edit time, caption or collab" icon="create-outline" onPress={() => navigation.navigate('New', { edit: p })} />
              <View style={{ flexDirection: 'row', gap: 10 }}>
                <Btn title="Post now" kind="gold" icon="flash" onPress={postNow} loading={busy === 'now'} style={{ flex: 1 }} />
                <Btn title="Cancel" kind="red" icon="close" onPress={cancel} loading={busy === 'cancel'} style={{ flex: 1 }} />
              </View>
            </Rise>
          ) : null}
          {p.status === 'failed' || p.status === 'partial' ? <Rise i={3}><Btn title="Try again" icon="refresh" onPress={retry} loading={busy === 'retry'} /></Rise> : null}
        </View>
      </ScrollView>
    </View>
  );
}
