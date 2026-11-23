import React, { useState } from 'react';
import { Switch, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Btn, Card, Field, Hero, Pill, Press, Rise, Screen, T, useConfirm, useToast } from '../ui';
import { useTheme } from '../theme';
import { api } from '../api';
import { dayKey } from '../time';
import type { Rule } from '../types';

export default function RuleScreen({ route, navigation }: any) {
  const { t } = useTheme(); const toast = useToast(); const confirm = useConfirm();
  const r: Rule | undefined = route.params.rule; const platform = r?.platform ?? route.params.platform; const trigger = r?.trigger ?? route.params.trigger;
  const [kws, setKws] = useState<string[]>(r?.keywords ?? []); const [kw, setKw] = useState('');
  const [msg, setMsg] = useState(r?.message ?? ''); const [pub, setPub] = useState(r?.reply_public ?? true); const [pubTxt, setPubTxt] = useState(r?.public_reply ?? '');
  const [till, setTill] = useState<string | null>(r?.active_till ?? null); const [busy, setBusy] = useState(false);
  const addKw = () => { const k = kw.trim(); if (k && !kws.includes(k) && kws.length < 10) setKws([...kws, k]); setKw(''); };
  const save = async () => {
    setBusy(true);
    try {
      await api('save_rule', { id: r?.id, platform, trigger, keywords: kw.trim() ? [...kws, kw.trim()] : kws, message: msg, reply_public: trigger === 'story' ? false : pub, public_reply: pubTxt, active_till: till, active: r?.active ?? true, story_mentions: true });
      toast('Rule saved'); navigation.goBack();
    } catch (e: any) { toast(e.message, false); } finally { setBusy(false); }
  };
  const del = async () => {
    if (!r || !(await confirm({ title: 'Delete this rule?', ok: 'Delete', danger: true }))) return;
    try { await api('delete_rule', { id: r.id }); toast('Rule deleted'); navigation.goBack(); } catch (e: any) { toast(e.message, false); }
  };
  const tillOpts = [{ l: 'No end date', v: null }, { l: '7 days', v: dayKey(Date.now() + 7 * 86400000) }, { l: '30 days', v: dayKey(Date.now() + 30 * 86400000) }];
  return (
    <Screen narrow header={
      <Hero>
        <Press onPress={() => navigation.goBack()} style={{ marginBottom: 8 }}><Ionicons name="arrow-back" size={24} color="#fff" /></Press>
        <T w="b" size={24} c="#fff">{r ? 'Edit rule' : 'New auto reply'}</T>
        <T size={13} c="rgba(255,255,255,0.85)">{platform === 'instagram' ? 'Instagram' : 'Facebook'} · {trigger === 'story' ? 'Story replies' : 'Comments'}</T>
      </Hero>
    }>
      <Rise>
        <Card style={{ gap: 10 }}>
          <T w="b" size={15}>{trigger === 'story' ? 'Keywords (optional)' : 'When a comment contains…'}</T>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 6 }}>
            {kws.map((k) => <Press key={k} onPress={() => setKws(kws.filter((x) => x !== k))}><Pill label={k + '  ✕'} color={t.green} bg={t.chip} size={13} /></Press>)}
          </View>
          <Field value={kw} onChange={setKw} placeholder="Type a keyword, e.g. price"
            right={<Press onPress={addKw}><Ionicons name="add-circle" size={26} color={t.green} /></Press>} />
        </Card>
      </Rise>
      <Rise i={1}>
        <Card style={{ gap: 12 }}>
          <Field label="Message we send in DM" value={msg} onChange={setMsg} multiline placeholder="नमस्ते! पूरी जानकारी… 📞 9993615146" />
          {trigger === 'comment' ? (
            <>
              <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                <T w="m" size={14}>Also reply under the comment</T>
                <Switch value={pub} onValueChange={setPub} trackColor={{ true: t.green, false: t.line }} thumbColor="#fff" />
              </View>
              {pub ? <Field value={pubTxt} onChange={setPubTxt} placeholder="आपको DM भेज दिया है ✅" /> : null}
            </>
          ) : null}
        </Card>
      </Rise>
      <Rise i={2}>
        <Card style={{ gap: 10 }}>
          <T w="b" size={15}>Keep it on for</T>
          <View style={{ flexDirection: 'row', gap: 8, flexWrap: 'wrap' }}>
            {tillOpts.map((o) => { const on = till === o.v || (o.v && till && o.l !== 'No end date' && till === o.v); return (
              <Press key={o.l} onPress={() => setTill(o.v)} style={{ paddingHorizontal: 14, paddingVertical: 8, borderRadius: 99, backgroundColor: on ? t.green : t.card2, borderWidth: 1, borderColor: on ? t.green : t.line }}><T w="s" size={13} c={on ? t.onGreen : t.text}>{o.l}</T></Press>
            ); })}
          </View>
          {till && !tillOpts.some((o) => o.v === till) ? <T s="mut" size={12}>Currently till {till}</T> : null}
        </Card>
      </Rise>
      <Rise i={3} style={{ gap: 10 }}>
        <Btn title="Save rule" icon="checkmark" kind="gold" onPress={save} loading={busy} />
        {r ? <Btn title="Delete rule" icon="trash-outline" kind="red" onPress={del} /> : null}
      </Rise>
    </Screen>
  );
}
