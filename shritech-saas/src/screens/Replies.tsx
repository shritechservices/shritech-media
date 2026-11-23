import React, { useCallback, useState } from 'react';
import { Switch, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { Btn, Card, Empty, Hero, Pill, Press, Rise, Screen, Seg, SectionTitle, Skel, T, useToast } from '../ui';
import { useTheme } from '../theme';
import { api } from '../api';
import type { LogItem, Rule } from '../types';

const ago = (iso: string) => { const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000); return m < 60 ? `${m}m ago` : m < 1440 ? `${Math.round(m / 60)}h ago` : `${Math.round(m / 1440)}d ago`; };

export default function Replies({ navigation }: any) {
  const { t } = useTheme(); const toast = useToast();
  const [trig, setTrig] = useState<'comment' | 'story'>('comment'); const [plat, setPlat] = useState<'instagram' | 'facebook'>('instagram');
  const [rules, setRules] = useState<Rule[]>([]); const [log, setLog] = useState<LogItem[]>([]); const [loading, setLoading] = useState(true); const [ref, setRef] = useState(false);
  const load = useCallback(async (pull = false) => {
    if (pull) setRef(true);
    try { const [r, l] = await Promise.all([api<Rule[]>('list_rules', { platform: plat, trigger: trig }), api<LogItem[]>('comment_log', { platform: plat, trigger: trig })]); setRules(r); setLog(l); }
    catch { } finally { setLoading(false); setRef(false); }
  }, [plat, trig]);
  useFocusEffect(useCallback(() => { setLoading(true); load(); }, [load]));
  const toggle = async (r: Rule, v: boolean) => {
    setRules((x) => x.map((y) => (y.id === r.id ? { ...y, active: v } : y)));
    try { await api('toggle_rule', { id: r.id, active: v }); toast(v ? 'Auto reply is ON' : 'Auto reply paused'); } catch (e: any) { toast(e.message, false); load(); }
  };
  return (
    <Screen narrow onRefresh={() => load(true)} refreshing={ref} header={
      <Hero>
        <T w="b" size={24} c="#fff">Auto replies</T>
        <T size={13} c="rgba(255,255,255,0.85)">{trig === 'comment' ? 'Someone comments a keyword → we reply and send your message in DM' : 'Someone replies to your story → we send your message in DM'}</T>
      </Hero>
    }>
      <Rise><Seg items={[{ v: 'comment', label: 'Comments', icon: 'chatbubble-ellipses-outline' }, { v: 'story', label: 'Story replies', icon: 'albums-outline' }]} value={trig} onChange={setTrig} /></Rise>
      <Rise i={1}><Seg items={[{ v: 'instagram', label: 'Instagram', icon: 'logo-instagram' }, { v: 'facebook', label: 'Facebook', icon: 'logo-facebook' }]} value={plat} onChange={setPlat} /></Rise>
      <SectionTitle title="Your rules" action="+ Add rule" onAction={() => navigation.navigate('Rule', { platform: plat, trigger: trig })} />
      {loading ? <><Skel h={110} /><Skel h={110} /></> : rules.length === 0 ? (
        <Card><Empty icon="chatbubbles-outline" title="No rules yet" sub="Add a keyword like “price” and the message to send." /><Btn title="Add your first rule" icon="add" onPress={() => navigation.navigate('Rule', { platform: plat, trigger: trig })} /></Card>
      ) : rules.map((r, i) => (
        <Rise key={r.id} i={i}>
          <Press onPress={() => navigation.navigate('Rule', { rule: r, platform: plat, trigger: trig })}>
            <Card style={{ gap: 10, opacity: r.active ? 1 : 0.65 }}>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 6, flex: 1 }}>
                  {(r.keywords.length ? r.keywords : ['Any story reply']).map((k) => <Pill key={k} label={k} color={t.green} bg={t.chip} size={12} />)}
                </View>
                <Switch value={r.active} onValueChange={(v) => toggle(r, v)} trackColor={{ true: t.green, false: t.line }} thumbColor="#fff" />
              </View>
              <T size={13} lines={3}>{r.message}</T>
              <View style={{ flexDirection: 'row', gap: 12 }}>
                <View style={{ flexDirection: 'row', gap: 4, alignItems: 'center' }}><Ionicons name="mail-outline" size={14} color={t.mut} /><T s="mut" size={12}>Private message</T></View>
                {r.reply_public ? <View style={{ flexDirection: 'row', gap: 4, alignItems: 'center' }}><Ionicons name="chatbubble-outline" size={14} color={t.mut} /><T s="mut" size={12}>Public reply</T></View> : null}
                {r.active_till ? <T s="mut" size={12}>till {r.active_till}</T> : null}
              </View>
            </Card>
          </Press>
        </Rise>
      ))}
      <SectionTitle title="Recent activity" />
      {loading ? <Skel h={60} /> : log.length === 0 ? <Card><Empty icon="pulse-outline" title="No activity yet" sub="Matched comments will appear here." /></Card> : (
        <Card pad={6}>
          {log.slice(0, 15).map((l, i) => (
            <View key={l.id} style={{ flexDirection: 'row', gap: 10, alignItems: 'center', padding: 10, borderBottomWidth: i < Math.min(log.length, 15) - 1 ? 1 : 0, borderColor: t.line }}>
              <View style={{ width: 38, height: 38, borderRadius: 19, backgroundColor: t.chip, alignItems: 'center', justifyContent: 'center' }}><T w="b" size={15} c={t.green}>{(l.from_username ?? '?')[0]?.toUpperCase()}</T></View>
              <View style={{ flex: 1 }}>
                <T w="s" size={13} lines={1}>@{l.from_username ?? 'someone'}</T>
                <T s="mut" size={12} lines={1}>“{l.comment_text}” · {ago(l.created_at)}</T>
              </View>
              <Ionicons name={l.dm_status === 'sent' ? 'checkmark-done-circle' : 'time-outline'} size={22} color={l.dm_status === 'sent' ? t.green : t.gold} />
            </View>
          ))}
        </Card>
      )}
    </Screen>
  );
}
