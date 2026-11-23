import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { Logo, Press, T, SIDEBAR_W, useConfirm, sh } from './ui';
import { useTheme } from './theme';

export type NavItem = { key: string; label: string; icon: keyof typeof Ionicons.glyphMap; match?: string[] };

/** Desktop browser frame: fixed left sidebar + wide content area. */
export function DesktopShell({ items, active, onNav, primary, title, subtitle, onAccount, onLogout, children }: {
  items: NavItem[]; active: string; onNav: (k: string) => void;
  primary?: { label: string; icon: keyof typeof Ionicons.glyphMap; onPress: () => void };
  title?: string; subtitle?: string; onAccount?: () => void; onLogout: () => void; children: React.ReactNode;
}) {
  const { t, pref, setPref } = useTheme(); const confirm = useConfirm();
  const dark = t.mode === 'dark';
  const out = async () => { if (await confirm({ title: 'Log out?', ok: 'Log out' })) onLogout(); };
  const initials = (title || 'S').trim().split(/\s+/).slice(0, 2).map((w) => w[0]?.toUpperCase()).join('');
  return (
    <View style={{ flex: 1, flexDirection: 'row', backgroundColor: t.bg }}>
      <View style={{ width: SIDEBAR_W, backgroundColor: t.card, borderRightWidth: 1, borderRightColor: t.line, paddingVertical: 22, paddingHorizontal: 16 }}>
        <View style={{ paddingHorizontal: 8, marginBottom: 6 }}><Logo size={26} /></View>
        <T s="mut" size={11} style={{ paddingHorizontal: 8, marginBottom: 22 }}>AutoPost for Facebook & Instagram</T>
        {primary ? (
          <Press onPress={primary.onPress} style={{ marginBottom: 18 }}>
            <LinearGradient colors={['#FACC15', '#EAB308']} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={[{ borderRadius: 14, paddingVertical: 12, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 }, sh('#EAB308', 0.3, 14, 6)]}>
              <Ionicons name={primary.icon} size={19} color="#2A2000" /><T w="b" size={14} c="#2A2000">{primary.label}</T>
            </LinearGradient>
          </Press>
        ) : null}
        <View style={{ gap: 4 }}>
          {items.map((it) => {
            const on = active === it.key || !!it.match?.includes(active);
            return (
              <Press key={it.key} onPress={() => onNav(it.key)} haptic={false} style={{ flexDirection: 'row', alignItems: 'center', gap: 12, paddingVertical: 11, paddingHorizontal: 12, borderRadius: 12, backgroundColor: on ? t.chip : 'transparent' }}>
                <Ionicons name={on ? it.icon : (`${it.icon}-outline` as any)} size={20} color={on ? t.green : t.mut} />
                <T w={on ? 's' : 'm'} size={14} c={on ? t.green : t.text}>{it.label}</T>
                {on ? <View style={{ marginLeft: 'auto', width: 6, height: 6, borderRadius: 3, backgroundColor: t.green }} /> : null}
              </Press>
            );
          })}
        </View>
        <View style={{ flex: 1 }} />
        <View style={{ flexDirection: 'row', backgroundColor: t.card2, borderRadius: 12, padding: 4, marginBottom: 12 }}>
          {([['light', 'sunny'], ['dark', 'moon'], ['system', 'phone-portrait']] as const).map(([k, i]) => (
            <Press key={k} haptic={false} onPress={() => setPref(k)} style={{ flex: 1, paddingVertical: 7, borderRadius: 9, alignItems: 'center', backgroundColor: pref === k ? t.card : 'transparent' }}>
              <Ionicons name={(pref === k ? i : `${i}-outline`) as any} size={16} color={pref === k ? t.green : t.mut} />
            </Press>
          ))}
        </View>
        <Press onPress={onAccount} haptic={false} style={{ flexDirection: 'row', alignItems: 'center', gap: 10, padding: 10, borderRadius: 14, borderWidth: 1, borderColor: t.line, backgroundColor: active === 'Account' ? t.chip : 'transparent' }}>
          <LinearGradient colors={t.grad as any} style={{ width: 38, height: 38, borderRadius: 19, alignItems: 'center', justifyContent: 'center' }}><T w="b" size={14} c="#fff">{initials}</T></LinearGradient>
          <View style={{ flex: 1, minWidth: 0 }}><T w="s" size={13} lines={1}>{title || 'ShriTech'}</T><T s="mut" size={11} lines={1}>{subtitle || ''}</T></View>
          <Press onPress={out} haptic={false} style={{ width: 32, height: 32, borderRadius: 10, alignItems: 'center', justifyContent: 'center', backgroundColor: t.redSoft }}><Ionicons name="log-out-outline" size={17} color={t.red} /></Press>
        </Press>
        <T s="mut" size={10} style={{ textAlign: 'center', marginTop: 10 }}>{dark ? '🌙' : '☀️'} ShriTech · 99936 15146</T>
      </View>
      <View style={{ flex: 1, minWidth: 0 }}>{children}</View>
    </View>
  );
}

/** Name of the screen currently showing, from a navigation state. */
export function activeRoute(state: any): string {
  let s = state; let name = '';
  while (s && s.routes) { const r = s.routes[s.index ?? 0]; name = r.name; s = r.state; }
  return name;
}

export function useLatest<T>(get: () => Promise<T>, deps: any[] = []) {
  const [v, setV] = useState<T | null>(null);
  useEffect(() => { get().then(setV).catch(() => {}); }, deps);
  return v;
}
