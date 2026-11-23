import React, { useEffect, useRef, useState, createContext, useContext, useCallback } from 'react';
import { Animated, Easing, Pressable, StyleSheet, Text, TextInput, View, ViewStyle, TextStyle, ActivityIndicator, Platform, ScrollView, RefreshControl } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { F, useTheme } from './theme';

const nd = Platform.OS !== 'web';
export const tap = () => { if (nd) Haptics.selectionAsync().catch(() => {}); };

export function T({ children, s, size = 14, w = 'r', c, style, lines }: { children: React.ReactNode; s?: 'mut'; size?: number; w?: keyof typeof F; c?: string; style?: TextStyle | TextStyle[]; lines?: number }) {
  const { t } = useTheme();
  return <Text numberOfLines={lines} style={[{ fontFamily: F[w], fontSize: size, color: c ?? (s === 'mut' ? t.mut : t.text), lineHeight: size * 1.45 }, style as any]}>{children}</Text>;
}

/** Fade + slide in, staggered by index */
export function Rise({ i = 0, children, style, from = 18 }: { i?: number; children: React.ReactNode; style?: ViewStyle; from?: number }) {
  const a = useRef(new Animated.Value(0)).current;
  useEffect(() => { Animated.timing(a, { toValue: 1, duration: 460, delay: 60 * i, easing: Easing.out(Easing.cubic), useNativeDriver: nd }).start(); }, []);
  return <Animated.View style={[style, { opacity: a, transform: [{ translateY: a.interpolate({ inputRange: [0, 1], outputRange: [from, 0] }) }] }]}>{children}</Animated.View>;
}

const pickOuter = (style: any): ViewStyle | undefined => { const f: any = StyleSheet.flatten(style) ?? {}; const o: any = {}; for (const k of ['flex', 'alignSelf', 'width', 'margin', 'marginTop', 'marginBottom', 'position', 'top', 'left', 'right', 'bottom', 'zIndex']) if (f[k] !== undefined) o[k] = f[k]; return o; };
/** Springy pressable */
export function Press({ onPress, children, style, disabled, haptic = true }: { onPress?: () => void; children: React.ReactNode; style?: ViewStyle | ViewStyle[]; disabled?: boolean; haptic?: boolean }) {
  const s = useRef(new Animated.Value(1)).current;
  const go = (v: number) => Animated.spring(s, { toValue: v, useNativeDriver: nd, speed: 40, bounciness: 8 }).start();
  return (
    <Pressable style={pickOuter(style)} disabled={disabled} onPressIn={() => go(0.96)} onPressOut={() => go(1)} onPress={() => { if (haptic) tap(); onPress?.(); }}>
      <Animated.View style={[style as any, (StyleSheet.flatten(style as any) as any)?.flex !== undefined ? { flex: undefined, flexGrow: 0, flexShrink: 0 } : null, { transform: [{ scale: s }], opacity: disabled ? 0.5 : 1 }, (StyleSheet.flatten(style as any) as any)?.position === 'absolute' ? { position: 'relative', top: 0, left: 0, right: undefined, bottom: undefined } : null]}>{children}</Animated.View>
    </Pressable>
  );
}

export function Btn({ title, onPress, kind = 'green', icon, loading, style, small, disabled }: { title: string; onPress?: () => void; kind?: 'green' | 'gold' | 'outline' | 'red' | 'ghost'; icon?: keyof typeof Ionicons.glyphMap; loading?: boolean; style?: ViewStyle; small?: boolean; disabled?: boolean }) {
  const { t } = useTheme();
  const bg = kind === 'green' ? t.green : kind === 'gold' ? t.gold : 'transparent';
  const fg = kind === 'green' ? t.onGreen : kind === 'gold' ? t.onGold : kind === 'red' ? t.red : t.green;
  const border = kind === 'outline' ? t.green : kind === 'red' ? t.red : 'transparent';
  return (
    <Press onPress={onPress} disabled={disabled || loading} style={[{ backgroundColor: bg, borderColor: border, borderWidth: kind === 'outline' || kind === 'red' ? 1.5 : 0, borderRadius: 14, paddingVertical: small ? 8 : 14, paddingHorizontal: small ? 14 : 20, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 }, (kind === 'green' || kind === 'gold') ? sh(t.mode === 'dark' ? '#000' : bg, 0.28) : {}, style ?? {}]}>
      {loading ? <ActivityIndicator color={fg} /> : icon ? <Ionicons name={icon} size={small ? 16 : 19} color={fg} /> : null}
      <T w="s" size={small ? 13 : 15} c={fg}>{title}</T>
    </Press>
  );
}

export const sh = (c: string, o = 0.12, r = 16, y = 8): ViewStyle => Platform.select({
  web: { boxShadow: `0px ${y}px ${r * 1.6}px ${c}${Math.round(o * 255).toString(16).padStart(2, '0')}` } as any,
  default: { shadowColor: c, shadowOpacity: o, shadowRadius: r, shadowOffset: { width: 0, height: y }, elevation: 4 },
})!;

export function Card({ children, style, pad = 16 }: { children: React.ReactNode; style?: ViewStyle | ViewStyle[]; pad?: number }) {
  const { t } = useTheme();
  return <View style={[{ backgroundColor: t.card, borderRadius: 22, padding: pad, borderWidth: 1, borderColor: t.line }, sh(t.shadow, t.mode === 'dark' ? 0.35 : 0.07), style as any]}>{children}</View>;
}

export function Pill({ label, color, bg, icon, size = 11 }: { label: string; color: string; bg: string; icon?: keyof typeof Ionicons.glyphMap; size?: number }) {
  return (
    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: bg, paddingHorizontal: 9, paddingVertical: 3, borderRadius: 99, alignSelf: 'flex-start' }}>
      {icon ? <Ionicons name={icon} size={size + 1} color={color} /> : null}
      <T w="s" size={size} c={color}>{label}</T>
    </View>
  );
}

export function useStatus() {
  const { t } = useTheme();
  return (s: string) => ({
    scheduled: { label: 'Scheduled', c: t.green, bg: t.chip, icon: 'time-outline' as const },
    publishing: { label: 'Publishing', c: t.blue, bg: t.blueSoft, icon: 'cloud-upload-outline' as const },
    posted: { label: 'Posted', c: t.green, bg: t.chip, icon: 'checkmark-circle' as const },
    partial: { label: 'Partly posted', c: t.gold, bg: t.goldSoft, icon: 'alert-circle-outline' as const },
    failed: { label: 'Not posted', c: t.red, bg: t.redSoft, icon: 'close-circle-outline' as const },
    cancelled: { label: 'Cancelled', c: t.mut, bg: t.card2, icon: 'remove-circle-outline' as const },
  } as any)[s] ?? { label: s, c: t.mut, bg: t.card2, icon: 'ellipse-outline' };
}

export function PlatformIcons({ list, size = 15 }: { list: string[]; size?: number }) {
  return (
    <View style={{ flexDirection: 'row', gap: 4 }}>
      {list.includes('facebook') && <View style={{ backgroundColor: '#1877F2', borderRadius: 99, padding: 3 }}><Ionicons name="logo-facebook" size={size - 3} color="#fff" /></View>}
      {list.includes('instagram') && <LinearGradient colors={['#F58529', '#DD2A7B', '#8134AF']} style={{ borderRadius: 99, padding: 3 }}><Ionicons name="logo-instagram" size={size - 3} color="#fff" /></LinearGradient>}
    </View>
  );
}

/** Count-up number */
export function CountUp({ to, size = 28, c }: { to: number; size?: number; c?: string }) {
  const [v, setV] = useState(0);
  useEffect(() => {
    const st = Date.now(); let raf: any;
    const step = () => { const k = Math.min(1, (Date.now() - st) / 900); setV(Math.round(to * (1 - Math.pow(1 - k, 3)))); if (k < 1) raf = requestAnimationFrame(step); };
    step(); return () => cancelAnimationFrame(raf);
  }, [to]);
  return <T w="b" size={size} c={c}>{v}</T>;
}

/** Brand wordmark: "Shri" + green "Tech" — always English */
export function Logo({ size = 24, light }: { size?: number; light?: boolean }) {
  const { t } = useTheme();
  return <Text style={{ fontFamily: F.x, fontSize: size }}><Text style={{ color: light ? '#fff' : t.text }}>Shri</Text><Text style={{ color: light ? '#FACC15' : t.green }}>Tech</Text></Text>;
}

/** Gradient hero header with floating animated glow blobs */
export function Hero({ children, height }: { children: React.ReactNode; height?: number }) {
  const { t } = useTheme(); const ins = useSafeAreaInsets();
  const a = useRef(new Animated.Value(0)).current;
  useEffect(() => { Animated.loop(Animated.sequence([Animated.timing(a, { toValue: 1, duration: 4200, easing: Easing.inOut(Easing.sin), useNativeDriver: nd }), Animated.timing(a, { toValue: 0, duration: 4200, easing: Easing.inOut(Easing.sin), useNativeDriver: nd })])).start(); }, []);
  const tx = a.interpolate({ inputRange: [0, 1], outputRange: [-20, 30] });
  return (
    <LinearGradient colors={t.grad as any} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ paddingTop: ins.top + 14, paddingHorizontal: 18, paddingBottom: 26, borderBottomLeftRadius: 30, borderBottomRightRadius: 30, overflow: 'hidden', minHeight: height }}>
      <Animated.View style={{ position: 'absolute', width: 220, height: 220, borderRadius: 110, backgroundColor: 'rgba(250,204,21,0.22)', top: -70, right: -50, transform: [{ translateX: tx }] }} />
      <Animated.View style={{ position: 'absolute', width: 160, height: 160, borderRadius: 80, backgroundColor: 'rgba(255,255,255,0.10)', bottom: -60, left: -30, transform: [{ translateY: tx }] }} />
      {children}
    </LinearGradient>
  );
}

export function Screen({ children, onRefresh, refreshing, header, pad = true }: { children: React.ReactNode; onRefresh?: () => void; refreshing?: boolean; header?: React.ReactNode; pad?: boolean }) {
  const { t } = useTheme();
  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 120 }} refreshControl={onRefresh ? <RefreshControl refreshing={!!refreshing} onRefresh={onRefresh} tintColor={t.green} colors={[t.green]} /> : undefined} showsVerticalScrollIndicator={false}>
        {header}
        <View style={pad ? { paddingHorizontal: 16, paddingTop: 16, gap: 14 } : undefined}>{children}</View>
      </ScrollView>
    </View>
  );
}

export function Field({ label, value, onChange, placeholder, multiline, secure, right, keyboard }: { label?: string; value: string; onChange: (v: string) => void; placeholder?: string; multiline?: boolean; secure?: boolean; right?: React.ReactNode; keyboard?: any }) {
  const { t } = useTheme(); const [f, setF] = useState(false);
  return (
    <View style={{ gap: 6 }}>
      {label ? <T s="mut" size={13} w="m">{label}</T> : null}
      <View style={{ flexDirection: 'row', alignItems: multiline ? 'flex-start' : 'center', backgroundColor: t.card2, borderRadius: 14, borderWidth: 1.5, borderColor: f ? t.green : t.line, paddingHorizontal: 14 }}>
        <TextInput value={value} onChangeText={onChange} placeholder={placeholder} placeholderTextColor={t.mut} secureTextEntry={secure} multiline={multiline} keyboardType={keyboard}
          onFocus={() => setF(true)} onBlur={() => setF(false)} autoCapitalize="none"
          style={{ flex: 1, fontFamily: F.r, fontSize: 15, color: t.text, paddingVertical: 12, minHeight: multiline ? 120 : undefined, textAlignVertical: multiline ? 'top' : 'center', outlineStyle: 'none' } as any} />
        {right}
      </View>
    </View>
  );
}

export function Seg<V extends string>({ items, value, onChange }: { items: { v: V; label: string; icon?: keyof typeof Ionicons.glyphMap }[]; value: V; onChange: (v: V) => void }) {
  const { t } = useTheme();
  return (
    <View style={{ flexDirection: 'row', backgroundColor: t.card2, borderRadius: 14, padding: 4, borderWidth: 1, borderColor: t.line }}>
      {items.map((it) => {
        const on = it.v === value;
        return (
          <Press key={it.v} onPress={() => onChange(it.v)} style={{ flex: 1 }}>
            <View style={{ flexDirection: 'row', gap: 6, alignItems: 'center', justifyContent: 'center', paddingVertical: 9, borderRadius: 11, backgroundColor: on ? t.green : 'transparent' }}>
              {it.icon ? <Ionicons name={it.icon} size={16} color={on ? t.onGreen : t.mut} /> : null}
              <T w="s" size={13} c={on ? t.onGreen : t.mut}>{it.label}</T>
            </View>
          </Press>
        );
      })}
    </View>
  );
}

export function Empty({ icon, title, sub }: { icon: keyof typeof Ionicons.glyphMap; title: string; sub?: string }) {
  const { t } = useTheme();
  const a = useRef(new Animated.Value(0)).current;
  useEffect(() => { Animated.loop(Animated.sequence([Animated.timing(a, { toValue: 1, duration: 1400, useNativeDriver: nd }), Animated.timing(a, { toValue: 0, duration: 1400, useNativeDriver: nd })])).start(); }, []);
  return (
    <View style={{ alignItems: 'center', paddingVertical: 26, gap: 6 }}>
      <Animated.View style={{ transform: [{ translateY: a.interpolate({ inputRange: [0, 1], outputRange: [0, -8] }) }] }}>
        <View style={{ width: 70, height: 70, borderRadius: 35, backgroundColor: t.chip, alignItems: 'center', justifyContent: 'center' }}><Ionicons name={icon} size={32} color={t.green} /></View>
      </Animated.View>
      <T w="s" size={15}>{title}</T>
      {sub ? <T s="mut" size={13} style={{ textAlign: 'center' }}>{sub}</T> : null}
    </View>
  );
}

/** Shimmer skeleton block */
export function Skel({ h = 70, r = 18 }: { h?: number; r?: number }) {
  const { t } = useTheme(); const a = useRef(new Animated.Value(0.4)).current;
  useEffect(() => { Animated.loop(Animated.sequence([Animated.timing(a, { toValue: 1, duration: 700, useNativeDriver: nd }), Animated.timing(a, { toValue: 0.4, duration: 700, useNativeDriver: nd })])).start(); }, []);
  return <Animated.View style={{ height: h, borderRadius: r, backgroundColor: t.card2, opacity: a }} />;
}

// ---------- toast ----------
const ToastCtx = createContext<(msg: string, ok?: boolean) => void>(() => {});
export const useToast = () => useContext(ToastCtx);
export function ToastProvider({ children }: { children: React.ReactNode }) {
  const { t } = useTheme(); const ins = useSafeAreaInsets();
  const [m, setM] = useState<{ msg: string; ok: boolean } | null>(null); const a = useRef(new Animated.Value(0)).current; const tm = useRef<any>(null);
  const show = useCallback((msg: string, ok = true) => {
    setM({ msg, ok }); clearTimeout(tm.current);
    Animated.spring(a, { toValue: 1, useNativeDriver: nd, bounciness: 10 }).start();
    if (nd) Haptics.notificationAsync(ok ? Haptics.NotificationFeedbackType.Success : Haptics.NotificationFeedbackType.Warning).catch(() => {});
    tm.current = setTimeout(() => Animated.timing(a, { toValue: 0, duration: 250, useNativeDriver: nd }).start(), 2600);
  }, []);
  return (
    <ToastCtx.Provider value={show}>
      {children}
      {m && (
        <Animated.View pointerEvents="none" style={{ position: 'absolute', left: 20, right: 20, top: ins.top + 10, opacity: a, transform: [{ translateY: a.interpolate({ inputRange: [0, 1], outputRange: [-40, 0] }) }] }}>
          <View style={[{ flexDirection: 'row', gap: 10, alignItems: 'center', backgroundColor: t.card, borderRadius: 16, padding: 14, borderWidth: 1.5, borderColor: m.ok ? t.green : t.gold }, sh('#000', 0.18)]}>
            <Ionicons name={m.ok ? 'checkmark-circle' : 'information-circle'} size={22} color={m.ok ? t.green : t.gold} />
            <T w="m" size={14} style={{ flex: 1 }}>{m.msg}</T>
          </View>
        </Animated.View>
      )}
    </ToastCtx.Provider>
  );
}

export const st = StyleSheet.create({ row: { flexDirection: 'row', alignItems: 'center' } });

// ---------- confirm sheet ----------
import { Modal, Image } from 'react-native';
type ConfirmOpts = { title: string; msg?: string; ok?: string; danger?: boolean };
const ConfirmCtx = createContext<(o: ConfirmOpts) => Promise<boolean>>(async () => false);
export const useConfirm = () => useContext(ConfirmCtx);
export function ConfirmProvider({ children }: { children: React.ReactNode }) {
  const { t } = useTheme();
  const [o, setO] = useState<(ConfirmOpts & { res: (v: boolean) => void }) | null>(null);
  const a = useRef(new Animated.Value(0)).current;
  const ask = useCallback((x: ConfirmOpts) => new Promise<boolean>((res) => { setO({ ...x, res }); a.setValue(0); Animated.spring(a, { toValue: 1, useNativeDriver: nd, bounciness: 6 }).start(); }), []);
  const done = (v: boolean) => { o?.res(v); setO(null); };
  return (
    <ConfirmCtx.Provider value={ask}>
      {children}
      <Modal transparent visible={!!o} animationType="fade" onRequestClose={() => done(false)}>
        <Pressable style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.45)', justifyContent: 'flex-end' }} onPress={() => done(false)}>
          <Animated.View style={{ transform: [{ translateY: a.interpolate({ inputRange: [0, 1], outputRange: [300, 0] }) }] }}>
            <Pressable onPress={() => {}} style={{ backgroundColor: t.card, borderTopLeftRadius: 28, borderTopRightRadius: 28, padding: 22, paddingBottom: 38, gap: 12 }}>
              <View style={{ alignSelf: 'center', width: 44, height: 5, borderRadius: 3, backgroundColor: t.line, marginBottom: 6 }} />
              <T w="b" size={19}>{o?.title}</T>
              {o?.msg ? <T s="mut" size={14}>{o.msg}</T> : null}
              <View style={{ flexDirection: 'row', gap: 10, marginTop: 8 }}>
                <Btn title="Not now" kind="outline" onPress={() => done(false)} style={{ flex: 1 }} />
                <Btn title={o?.ok ?? 'Yes'} kind={o?.danger ? 'red' : 'green'} onPress={() => done(true)} style={{ flex: 1 }} />
              </View>
            </Pressable>
          </Animated.View>
        </Pressable>
      </Modal>
    </ConfirmCtx.Provider>
  );
}

/** Media tile: image preview, or a branded tile for videos */
export function Thumb({ m, w, h, r = 14 }: { m?: { kind: string; public_url: string; title?: string | null; local?: any; poster?: any } | null; w: number | `${number}%`; h: number; r?: number }) {
  const { t } = useTheme();
  if (m?.kind === 'image') return <Image source={m.local ?? { uri: m.public_url }} style={{ width: w as any, height: h, borderRadius: r, backgroundColor: t.card2 }} resizeMode="cover" />;
  if (m?.poster) return (
    <View style={{ width: w as any, height: h, borderRadius: r, overflow: 'hidden', backgroundColor: t.card2 }}>
      <Image source={m.poster} style={{ width: '100%', height: '100%' }} resizeMode="cover" />
      <View style={{ position: 'absolute', top: 6, left: 6, flexDirection: 'row', alignItems: 'center', gap: 3, backgroundColor: 'rgba(0,0,0,0.55)', borderRadius: 99, paddingHorizontal: 7, paddingVertical: 2 }}>
        <Ionicons name="play" size={10} color="#fff" /><T w="s" size={9} c="#fff">REEL</T>
      </View>
    </View>
  );
  return (
    <LinearGradient colors={t.mode === 'dark' ? ['#0F3B22', '#16221B'] : ['#DCFCE7', '#FEF9C3']} style={{ width: w as any, height: h, borderRadius: r, alignItems: 'center', justifyContent: 'center' }}>
      <View style={{ width: 38, height: 38, borderRadius: 19, backgroundColor: t.green, alignItems: 'center', justifyContent: 'center' }}><Ionicons name="play" size={18} color={t.onGreen} style={{ marginLeft: 2 }} /></View>
      <T w="s" size={10} c={t.green} style={{ marginTop: 6 }}>REEL</T>
    </LinearGradient>
  );
}

export function SectionTitle({ title, action, onAction }: { title: string; action?: string; onAction?: () => void }) {
  const { t } = useTheme();
  return (
    <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: 4 }}>
      <T w="b" size={17}>{title}</T>
      {action ? <Press onPress={onAction}><T w="s" size={13} c={t.green}>{action}</T></Press> : null}
    </View>
  );
}
