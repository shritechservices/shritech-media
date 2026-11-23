import React, { useEffect, useRef, useState } from 'react';
import { Animated, Platform, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer, DefaultTheme, DarkTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useFonts, Poppins_400Regular, Poppins_500Medium, Poppins_600SemiBold, Poppins_700Bold, Poppins_800ExtraBold } from '@expo-google-fonts/poppins';
import { ThemeProvider, useTheme, F } from './src/theme';
import { ConfirmProvider, Logo, ToastProvider, tap, sh } from './src/ui';
import { clearSession, restoreSession, setLogoutHandler } from './src/api';
import { resetSettings } from './src/data';
import Login from './src/screens/Login';
import Home from './src/screens/Home';
import Calendar from './src/screens/Calendar';
import Compose from './src/screens/Compose';
import Library from './src/screens/Library';
import Replies from './src/screens/Replies';
import PostScreen from './src/screens/Post';
import RuleScreen from './src/screens/Rule';
import Settings from './src/screens/Settings';

const Tab = createBottomTabNavigator(); const Stack = createNativeStackNavigator();

function TabIcon({ name, focused, color }: { name: any; focused: boolean; color: string }) {
  const a = useRef(new Animated.Value(focused ? 1 : 0)).current;
  useEffect(() => { Animated.spring(a, { toValue: focused ? 1 : 0, useNativeDriver: Platform.OS !== 'web', bounciness: 12 }).start(); }, [focused]);
  return <Animated.View style={{ transform: [{ scale: a.interpolate({ inputRange: [0, 1], outputRange: [1, 1.18] }) }, { translateY: a.interpolate({ inputRange: [0, 1], outputRange: [0, -2] }) }] }}><Ionicons name={focused ? name : `${name}-outline`} size={23} color={color} /></Animated.View>;
}

function Tabs() {
  const { t } = useTheme(); const ins = useSafeAreaInsets();
  return (
    <Tab.Navigator screenOptions={{
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

function Splash() {
  const { t } = useTheme(); const a = useRef(new Animated.Value(0)).current;
  useEffect(() => { Animated.loop(Animated.sequence([Animated.timing(a, { toValue: 1, duration: 700, useNativeDriver: Platform.OS !== 'web' }), Animated.timing(a, { toValue: 0, duration: 700, useNativeDriver: Platform.OS !== 'web' })])).start(); }, []);
  return <View style={{ flex: 1, backgroundColor: t.bg, alignItems: 'center', justifyContent: 'center' }}><Animated.View style={{ opacity: a.interpolate({ inputRange: [0, 1], outputRange: [0.5, 1] }), transform: [{ scale: a.interpolate({ inputRange: [0, 1], outputRange: [0.95, 1.05] }) }] }}><Logo size={40} /></Animated.View></View>;
}

function Root() {
  const { t } = useTheme();
  const [state, setState] = useState<'boot' | 'out' | 'in'>('boot');
  const logout = async () => { await clearSession(); resetSettings(); setState('out'); };
  useEffect(() => { setLogoutHandler(() => setState('out')); restoreSession().then((ok) => setState(ok ? 'in' : 'out')); }, []);
  const navTheme = { ...(t.mode === 'dark' ? DarkTheme : DefaultTheme), colors: { ...(t.mode === 'dark' ? DarkTheme : DefaultTheme).colors, background: t.bg, card: t.card, primary: t.green, text: t.text, border: t.line } };
  return (
    <>
      <StatusBar style={state === 'in' || state === 'out' ? 'light' : t.mode === 'dark' ? 'light' : 'dark'} />
      {state === 'boot' ? <Splash /> : state === 'out' ? <Login onDone={() => { resetSettings(); setState('in'); }} /> : (
        <NavigationContainer theme={navTheme as any}>
          <Stack.Navigator screenOptions={{ headerShown: false, animation: 'slide_from_right' }}>
            <Stack.Screen name="Tabs" component={Tabs} />
            <Stack.Screen name="Post" component={PostScreen} options={{ presentation: 'modal', animation: 'slide_from_bottom' }} />
            <Stack.Screen name="Rule" component={RuleScreen} />
            <Stack.Screen name="Settings">{(p) => <Settings {...p} onLogout={logout} />}</Stack.Screen>
            <Stack.Screen name="New" component={Compose} />
          </Stack.Navigator>
        </NavigationContainer>
      )}
    </>
  );
}

export default function App() {
  const [ok] = useFonts({ Poppins_400Regular, Poppins_500Medium, Poppins_600SemiBold, Poppins_700Bold, Poppins_800ExtraBold });
  if (!ok) return null;
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <ToastProvider>
          <ConfirmProvider>
            <Root />
          </ConfirmProvider>
        </ToastProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
