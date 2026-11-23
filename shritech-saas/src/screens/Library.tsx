import React, { useCallback, useState } from 'react';
import { View, useWindowDimensions } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { useFocusEffect } from '@react-navigation/native';
import { Btn, Card, Empty, Field, Hero, Press, Rise, Screen, Seg, Skel, T, Thumb, useConfirm, useToast } from '../ui';
import { useTheme } from '../theme';
import { api, uploadFile } from '../api';
import type { Media } from '../types';

export default function Library({ navigation }: any) {
  const { t } = useTheme(); const toast = useToast(); const confirm = useConfirm(); const { width } = useWindowDimensions();
  const [all, setAll] = useState<'month' | 'all'>('month'); const [items, setItems] = useState<Media[]>([]); const [loading, setLoading] = useState(true); const [ref, setRef] = useState(false);
  const [title, setTitle] = useState(''); const [up, setUp] = useState(0);
  const load = useCallback(async (pull = false) => { if (pull) setRef(true); try { setItems(await api<Media[]>('list_media', { all: all === 'all' })); } catch { } finally { setLoading(false); setRef(false); } }, [all]);
  useFocusEffect(useCallback(() => { load(); }, [load]));
  const pick = async () => {
    const r = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images', 'videos'], quality: 1 });
    if (r.canceled || !r.assets?.[0]) return;
    const a = r.assets[0]; const isVid = a.type === 'video';
    if ((a.fileSize ?? 0) > 50 * 1048576) { toast('Please choose a file under 50 MB', false); return; }
    setUp(0.01);
    try { await uploadFile({ uri: a.uri, name: a.fileName ?? (isVid ? 'reel.mp4' : 'image.jpg'), mime: a.mimeType ?? (isVid ? 'video/mp4' : 'image/jpeg'), size: a.fileSize }, title, setUp); setTitle(''); toast('Uploaded ✨'); load(); }
    catch (e: any) { toast(e.message, false); } finally { setUp(0); }
  };
  const remove = async (m: Media) => {
    if (!(await confirm({ title: 'Remove this file?', msg: 'It will be removed from your library.', ok: 'Remove', danger: true }))) return;
    try { await api('delete_media', { id: m.id }); toast('Removed'); load(); } catch (e: any) { toast(e.message, false); }
  };
  const col = Math.floor((Math.min(width, 700) - 32 - 12) / 2);
  return (
    <Screen onRefresh={() => load(true)} refreshing={ref} header={
      <Hero><T w="b" size={24} c="#fff">Media library</T><T size={13} c="rgba(255,255,255,0.85)">Your reels and images, ready to schedule</T></Hero>
    }>
      <Rise>
        <Card style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', gap: 12, alignItems: 'center' }}>
            <View style={{ width: 48, height: 48, borderRadius: 16, backgroundColor: t.goldSoft, alignItems: 'center', justifyContent: 'center' }}><Ionicons name="cloud-upload" size={24} color={t.gold} /></View>
            <View style={{ flex: 1 }}><T w="b" size={15}>Upload from your phone</T><T s="mut" size={12}>Reels (MP4, 9:16, up to 50 MB) or JPG / PNG</T></View>
          </View>
          <Field value={title} onChange={setTitle} placeholder="Title (optional) e.g. Diwali reel" />
          {up > 0 ? (
            <View style={{ gap: 6 }}>
              <View style={{ height: 10, borderRadius: 5, backgroundColor: t.card2, overflow: 'hidden' }}><View style={{ height: 10, width: `${Math.round(up * 100)}%`, backgroundColor: t.green, borderRadius: 5 }} /></View>
              <T s="mut" size={12}>Uploading… {Math.round(up * 100)}%</T>
            </View>
          ) : <Btn title="Choose video or image" icon="images-outline" onPress={pick} />}
        </Card>
      </Rise>
      <Rise i={1}><Seg items={[{ v: 'month', label: 'This month', icon: 'calendar-outline' }, { v: 'all', label: 'All files', icon: 'albums-outline' }]} value={all} onChange={(v) => { setAll(v); setLoading(true); }} /></Rise>
      {loading ? <View style={{ flexDirection: 'row', gap: 12 }}><View style={{ flex: 1 }}><Skel h={240} /></View><View style={{ flex: 1 }}><Skel h={240} /></View></View>
        : items.length === 0 ? <Card><Empty icon="images-outline" title="No files here yet" sub={all === 'month' ? 'Older files are under “All files”.' : 'Upload your first reel above.'} /></Card>
          : (
            <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 12 }}>
              {items.map((m, i) => (
                <Rise key={m.id} i={i % 8} style={{ width: col }}>
                  <Card pad={0} style={{ overflow: 'hidden' }}>
                    <Thumb m={m} w="100%" h={col * 1.3} r={0} />
                    <View style={{ padding: 10, gap: 8 }}>
                      <T w="s" size={13} lines={1}>{m.title || 'Untitled'}</T>
                      <View style={{ flexDirection: 'row', gap: 8 }}>
                        <Btn small title="Schedule" icon="paper-plane" onPress={() => navigation.navigate('New', { mediaId: m.id })} style={{ flex: 1, paddingHorizontal: 6 }} />
                        <Press onPress={() => remove(m)} style={{ width: 36, borderRadius: 12, alignItems: 'center', justifyContent: 'center', backgroundColor: t.redSoft }}><Ionicons name="trash-outline" size={17} color={t.red} /></Press>
                      </View>
                    </View>
                  </Card>
                </Rise>
              ))}
            </View>
          )}
    </Screen>
  );
}
