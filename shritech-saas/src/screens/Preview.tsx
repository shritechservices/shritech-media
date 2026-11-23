import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Image, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useVideoPlayer, VideoView } from 'expo-video';
import { useEvent } from 'expo';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Press, T, useWide } from '../ui';
import { previewUrl } from '../api';

/** Plays a reel from the library (auto-plays, loops, shows a spinner while loading). */
export function ReelPlayer({ url }: { url: string }) {
  const player = useVideoPlayer({ uri: previewUrl(url), contentType: 'progressive' } as any, (p) => { p.loop = true; p.muted = false; p.play(); });
  const { status } = useEvent(player, 'statusChange', { status: player.status });
  const [err, setErr] = useState(false);
  useEffect(() => { if (status === 'error') setErr(true); }, [status]);
  return (
    <View style={{ width: '100%', height: '100%', backgroundColor: '#000', alignItems: 'center', justifyContent: 'center' }}>
      <VideoView player={player} style={{ width: '100%', height: '100%' }} contentFit="contain" nativeControls />
      {status === 'loading' ? <View pointerEvents="none" style={{ position: 'absolute', alignItems: 'center', gap: 8 }}><ActivityIndicator color="#fff" size="large" /><T size={12} c="#fff">Loading reel…</T></View> : null}
      {err ? <View pointerEvents="none" style={{ position: 'absolute', alignItems: 'center', gap: 8, padding: 20 }}><Ionicons name="alert-circle" size={30} color="#FACC15" /><T size={13} c="#fff" style={{ textAlign: 'center' }}>This reel could not be played here. It will still post normally.</T></View> : null}
    </View>
  );
}

/** Full-screen preview of a library file. */
export default function Preview({ route, navigation }: any) {
  const m = route.params?.m; const ins = useSafeAreaInsets(); const wide = useWide();
  return (
    <View style={{ flex: 1, backgroundColor: '#000', alignItems: 'center', justifyContent: 'center' }}>
      <View style={wide ? { height: '92%', aspectRatio: 9 / 16, borderRadius: 20, overflow: 'hidden' } : { width: '100%', height: '100%' }}>
        {m?.kind === 'image' ? <Image source={m.local ?? { uri: m.public_url }} style={{ width: '100%', height: '100%' }} resizeMode="contain" /> : m ? <ReelPlayer url={m.public_url} /> : null}
      </View>
      <Press onPress={() => navigation.goBack()} style={{ position: 'absolute', top: ins.top + 12, left: 14, width: 44, height: 44, borderRadius: 22, backgroundColor: 'rgba(255,255,255,0.18)', alignItems: 'center', justifyContent: 'center' }}>
        <Ionicons name="close" size={26} color="#fff" />
      </Press>
      {m?.title ? <View pointerEvents="none" style={{ position: 'absolute', top: ins.top + 22, left: 70, right: 20 }}><T w="s" size={14} c="#fff" lines={1}>{m.title}</T></View> : null}
    </View>
  );
}
