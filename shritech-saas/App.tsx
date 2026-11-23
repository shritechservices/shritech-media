import React, { useEffect, useRef, useState } from 'react';
import { Animated, Platform, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer, DefaultTheme, DarkTheme, createNavigationContainerRef } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useFonts, Poppins_400Regular, Poppins_500Medium, Poppins_600SemiBold, Poppins_700Bold, Poppins_800ExtraBold } from '@expo-google-fonts/poppins';
import { ThemeProvider, useTheme, F } from './src/theme';
import { ConfirmProvider, Logo, ToastProvider, tap, sh, useWide } from './src/ui';
import { DesktopShell, activeRoute } from './src/Desktop';
import { clearSession, restoreSession, setLogoutHandler } from './src/api';
import { resetMe, getMe } from './src/data';
import Login from './src/screens/Login';
import Landing from './src/screens/Landing';
import Home from './src/screens/Home';
import Calendar from './src/screens/Calendar';
import Compose from './src/screens/Compose';
import Library from './src/screens/Library';
import Replies from './src/screens/Replies';
import PostScreen from './src/screens/Post';
import RuleScreen from './src/screens/Rule';
import Account from './src/screens/Account';
import { AdminHome, AdminTenant, AdminSettings } from './src/screens/Admin';

const Tab = createBottomTabNavigator(); const Stack = createNativeStackNavigator();

function TabIcon({ name, focused, color }: { name: any; focused: boolean; color: string }) {
  const a = useRef(new Animated.Value(focused ? 1 : 0)).current;
  useEffect(() => { Animated.spring(a, { toValue: focused ? 1 : 0, useNativeDriver: Platform.OS !== 'web', bounciness: 12 }).start(); }, [focused]);
  return <Animated.View style={{ transform: [{ scale: a.interpolate({ inputRange: [0, 1], outputRange: [1, 1.18] }) }, { translateY: a.interpolate({ inputRange: [0, 1], outputRange: [0, -2] }) }] }}><Ionicons name={focused ? name : `${name}-outline`} size={23} color={color} /></Animated.View>;
}

function Tabs() {
  const { t } = useTheme(); const ins = useSafeAreaInsets(); const wide = useWide();
  return (
    <Tab.Navigator tabBar={wide ? () => null : undefined} screenOptions={{
      headerShown: false, tabBarActiveTintColor: t.green, tabBarInactiveTintColor: t.mut,
      tabBarStyle: { backgroundColor: t.tabBar, borderTopColor: t.line, height: 64 + ins.bottom, paddingTop: 6, paddingBottom: ins.bottom + 6, ...sh('#000', t.mode === 'dark' ? 0.4 : 0.08, 20, -4) },
      tabBarLabelStyle: { fontFamily: F.s, fontSize: 11 },
    }} screenListeners={{ tabPress: () => tap() }}>
      <Tab.Screen name="Home" component={Home} options={{ tabBarIcon: (p) => <TabIcon name="home" {...p} /> }} />
      <Tab.Screen name="Calendar" component={Calendar} options={{ tabBarIcon: (p) => <TabIcon name="calendar" {...p} /> }} />
      <Tab.Screen name="New" component={Compose} options={{
        tabBarLabel: () => null,
        tabBarIcon: ({ focused }) => (
          <LinearGradient colors={['#FACC15', '#EAB308']} style={{ width: 58, height: 58, borderRadius: 29, alignItems: 'center', justifyContent: 'center', marginTop: -22, borderWidth: 4, borderColor: t.tabBar, ...sh('#EAB308', 0.45, 14, 6) }}>
            <Ionicons name={focused ? 'create' : 'add'} size={30} color="#2A2000" />
          </LinearGradient>
        ),
      }} />
      <Tab.Screen name="Library" component={Library} options={{ title: 'Media', tabBarIcon: (p) => <TabIcon name="images" {...p} /> }} />
      <Tab.Screen name="Replies" component={Replies} options={{ title: 'Replies', tabBarIcon: (p) => <TabIcon name="chatbubbles" {...p} /> }} />
    </Tab.Navigator>
  );
}

/** On wide web screens, keep the app a comfortable width (landing page stays full width). */
function WebFrame({ children }: { children: React.ReactNode }) {
  const { t } = useTheme();
  if (Platform.OS !== 'web') return <>{children}</>;
  return <View style={{ flex: 1, backgroundColor: t.bg2 }}>{children}</View>;
}

function AppWidth({ children }: { children: React.ReactNode }) {
  const { t } = useTheme(); const wide = useWide();
  if (Platform.OS !== 'web' || wide) return <>{children}</>;
  return <View style={{ flex: 1, alignItems: 'center', backgroundColor: t.bg2 }}><View style={{ flex: 1, width: '100%', maxWidth: 760, ...sh('#000', 0.08, 30, 0) }}>{children}</View></View>;
}

function LoginWidth({ children }: { children: React.ReactNode }) {
  const { t } = useTheme(); const wide = useWide();
  if (Platform.OS !== 'web' || wide) return <>{children}</>;
  return <View style={{ flex: 1, alignItems: 'center', backgroundColor: t.bg2 }}><View style={{ flex: 1, width: '100%', maxWidth: 520 }}>{children}</View></View>;
}

const userNav = createNavigationContainerRef<any>();
const adminNav = createNavigationContainerRef<any>();

/** Desktop sidebar for business users (only on wide browser screens). */
function UserFrame({ children, route, onLogout }: { children: React.ReactNode; route: string; onLogout: () => void }) {
  const wide = useWide(); const [me, setMe] = useState<any>(null);
  useEffect(() => { if (wide) getMe().then(setMe).catch(() => {}); }, [wide, route]);
  if (!wide) return <>{children}</>;
  const go = (k: string) => { if (!userNav.isReady()) return; if (k === 'Account') userNav.navigate('Account'); else userNav.navigate('Tabs', { screen: k }); };
  return (
    <DesktopShell active={route} onNav={go} onLogout={onLogout} onAccount={() => go('Account')}
      title={me?.tenant?.name} subtitle={me?.user?.email}
      primary={{ label: 'New post', icon: 'add-circle', onPress: () => userNav.isReady() && userNav.navigate('New') }}
      items={[
        { key: 'Home', label: 'Dashboard', icon: 'grid' },
        { key: 'Calendar', label: 'Calendar', icon: 'calendar', match: ['Post'] },
        { key: 'Library', label: 'Media library', icon: 'images' },
        { key: 'Replies', label: 'Auto replies', icon: 'chatbubbles', match: ['Rule'] },
        { key: 'Account', label: 'Account & team', icon: 'person-circle' },
      ]}>{children}</DesktopShell>
  );
}
function AdminFrame({ children, route, onLogout, email }: { children: React.ReactNode; route: string; onLogout: () => void; email?: string }) {
  const wide = useWide();
  if (!wide) return <>{children}</>;
  return (
    <DesktopShell active={route} onNav={(k) => adminNav.isReady() && adminNav.navigate(k)} onLogout={onLogout} onAccount={() => adminNav.isReady() && adminNav.navigate('AdminSettings')}
      title="ShriTech Admin" subtitle="Super admin"
      items={[{ key: 'AdminHome', label: 'Businesses', icon: 'storefront', match: ['AdminTenant'] }, { key: 'AdminSettings', label: 'Settings', icon: 'settings' }]}>{children}</DesktopShell>
  );
}

function Splash() {
  const { t } = useTheme(); const a = useRef(new Animated.Value(0)).current;
  useEffect(() => { Animated.loop(Animated.sequence([Animated.timing(a, { toValue: 1, duration: 700, useNativeDriver: Platform.OS !== 'web' }), Animated.timing(a, { toValue: 0, duration: 700, useNativeDriver: Platform.OS !== 'web' })])).start(); }, []);
  return <View style={{ flex: 1, backgroundColor: t.bg, alignItems: 'center', justifyContent: 'center' }}><Animated.View style={{ opacity: a.interpolate({ inputRange: [0, 1], outputRange: [0.5, 1] }), transform: [{ scale: a.interpolate({ inputRange: [0, 1], outputRange: [0.95, 1.05] }) }] }}><Logo size={40} /></Animated.View></View>;
}

function Root() {
  const { t } = useTheme();
  const [state, setState] = useState<'boot' | 'out' | 'user' | 'admin'>('boot');
  const [showLogin, setShowLogin] = useState(Platform.OS !== 'web');
  const [route, setRoute] = useState('');
  const logout = async () => { await clearSession(); resetMe(); setState('out'); };
  useEffect(() => { setLogoutHandler(() => { resetMe(); setState('out'); }); restoreSession().then((r) => setState(r === 'admin' ? 'admin' : r ? 'user' : 'out')); }, []);
  const navTheme = { ...(t.mode === 'dark' ? DarkTheme : DefaultTheme), colors: { ...(t.mode === 'dark' ? DarkTheme : DefaultTheme).colors, background: t.bg, card: t.card, primary: t.green, text: t.text, border: t.line } };
  return (
    <>
      <StatusBar style={state === 'boot' ? (t.mode === 'dark' ? 'light' : 'dark') : 'light'} />
      {state === 'boot' ? <Splash /> : state === 'out' && !showLogin ? <Landing onStart={() => setShowLogin(true)} /> : state === 'out' ? <LoginWidth><Login onBack={Platform.OS === 'web' ? () => setShowLogin(false) : undefined} onDone={(r) => { resetMe(); setState(r); }} /></LoginWidth> : state === 'admin' ? (
        <AppWidth><AdminFrame route={route} onLogout={logout}><NavigationContainer ref={adminNav} onReady={() => setRoute(activeRoute(adminNav.getRootState()))} onStateChange={(st) => setRoute(activeRoute(st))} theme={navTheme as any}>
          <Stack.Navigator screenOptions={{ headerShown: false, animation: 'slide_from_right' }}>
            <Stack.Screen name="AdminHome" component={AdminHome} />
            <Stack.Screen name="AdminTenant" component={AdminTenant} />
            <Stack.Screen name="AdminSettings">{(p) => <AdminSettings {...p} onLogout={logout} />}</Stack.Screen>
          </Stack.Navigator>
        </NavigationContainer></AdminFrame></AppWidth>
      ) : (
        <AppWidth><UserFrame route={route} onLogout={logout}><NavigationContainer ref={userNav} onReady={() => setRoute(activeRoute(userNav.getRootState()))} onStateChange={(st) => setRoute(activeRoute(st))} theme={navTheme as any}>
          <Stack.Navigator screenOptions={{ headerShown: false, animation: 'slide_from_right' }}>
            <Stack.Screen name="Tabs" component={Tabs} />
            <Stack.Screen name="Post" component={PostScreen} options={{ presentation: 'modal', animation: 'slide_from_bottom' }} />
            <Stack.Screen name="Rule" component={RuleScreen} />
            <Stack.Screen name="Account">{(p) => <Account {...p} onLogout={logout} />}</Stack.Screen>
            <Stack.Screen name="New" component={Compose} />
          </Stack.Navigator>
        </NavigationContainer></UserFrame></AppWidth>
      )}
    </>
  );
}

export default function App() {
  const [ok, fontErr] = useFonts({ Poppins_400Regular, Poppins_500Medium, Poppins_600SemiBold, Poppins_700Bold, Poppins_800ExtraBold });
  const [late, setLate] = useState(false);
  useEffect(() => { const id = setTimeout(() => setLate(true), 4000); return () => clearTimeout(id); }, []);
  if (!ok && !fontErr && !late) return null; // never wait forever for fonts
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <WebFrame>
        <ToastProvider>
          <ConfirmProvider>
            <Root />
          </ConfirmProvider>
        </ToastProvider>
        </WebFrame>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
