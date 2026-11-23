import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { useColorScheme } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Same palette as the web portal (dark) + ShriTech light brand (green / yellow / white)
export const palettes = {
  light: {
    mode: 'light' as const,
    bg: '#F6FBF4', bg2: '#FFFDF2', card: '#FFFFFF', card2: '#F3FAF1', line: '#E2EFE0',
    text: '#0B2A17', mut: '#5E7566', green: '#16A34A', green2: '#22C55E', deep: '#14532D',
    gold: '#EAB308', goldSoft: '#FEF9C3', red: '#DC2626', redSoft: '#FEE2E2', blue: '#2563EB', blueSoft: '#DBEAFE',
    pink: '#DB2777', chip: '#ECFDF3', onGreen: '#FFFFFF', onGold: '#2A2000',
    grad: ['#14532D', '#16A34A', '#22C55E'] as const, glowA: 'rgba(250,204,21,0.35)', glowB: 'rgba(34,197,94,0.25)',
    shadow: '#14532D', tabBar: '#FFFFFF',
  },
  dark: {
    mode: 'dark' as const,
    bg: '#07100B', bg2: '#0A140E', card: '#111A15', card2: '#16221B', line: '#22352A',
    text: '#E8F2EC', mut: '#94A89B', green: '#22C55E', green2: '#4ADE80', deep: '#0F2A1A',
    gold: '#FACC15', goldSoft: '#2A2408', red: '#F87171', redSoft: '#2A1111', blue: '#60A5FA', blueSoft: '#0D1A2E',
    pink: '#F472B6', chip: '#0F2A1A', onGreen: '#06210F', onGold: '#2A2000',
    grad: ['#06210F', '#0F3B22', '#166534'] as const, glowA: 'rgba(250,204,21,0.18)', glowB: 'rgba(34,197,94,0.22)',
    shadow: '#000000', tabBar: '#0B140F',
  },
};
export type Theme = typeof palettes.light | typeof palettes.dark;
export type ThemePref = 'system' | 'light' | 'dark';

const Ctx = createContext<{ t: Theme; pref: ThemePref; setPref: (p: ThemePref) => void }>({ t: palettes.light, pref: 'system', setPref: () => {} });

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const sys = useColorScheme();
  const [pref, setPrefState] = useState<ThemePref>('system');
  useEffect(() => { AsyncStorage.getItem('st_theme').then((v) => { if (v === 'light' || v === 'dark' || v === 'system') setPrefState(v); }); }, []);
  const setPref = (p: ThemePref) => { setPrefState(p); AsyncStorage.setItem('st_theme', p); };
  const t = useMemo(() => (pref === 'system' ? (sys === 'dark' ? palettes.dark : palettes.light) : palettes[pref]), [pref, sys]);
  return <Ctx.Provider value={{ t, pref, setPref }}>{children}</Ctx.Provider>;
}
export const useTheme = () => useContext(Ctx);

export const F = { r: 'Poppins_400Regular', m: 'Poppins_500Medium', s: 'Poppins_600SemiBold', b: 'Poppins_700Bold', x: 'Poppins_800ExtraBold' };
