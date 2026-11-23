import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';
import { demoApi } from './demo';

// SaaS backend (separate from the live single-account system).
export const BASE = 'https://hnrhctlxreexefymfcct.supabase.co/functions/v1/saas-api';

export type Role = 'user' | 'admin';
let TOKEN = ''; let ROLE: Role = 'user'; let DEMO = false;
let onLogout: () => void = () => {};
export const setLogoutHandler = (f: () => void) => { onLogout = f; };
export const isDemo = () => DEMO;
export const role = () => ROLE;

export async function restoreSession(): Promise<Role | 'demo' | null> {
  const [t, r, d] = await Promise.all([AsyncStorage.getItem('sa_token'), AsyncStorage.getItem('sa_role'), AsyncStorage.getItem('sa_demo')]);
  if (d === '1') { DEMO = true; ROLE = 'user'; return 'demo'; }
  TOKEN = t ?? ''; ROLE = r === 'admin' ? 'admin' : 'user';
  return TOKEN ? ROLE : null;
}
export async function enterDemo() { DEMO = true; ROLE = 'user'; await AsyncStorage.setItem('sa_demo', '1'); }
export async function clearSession() { TOKEN = ''; DEMO = false; await AsyncStorage.multiRemove(['sa_token', 'sa_role', 'sa_demo']); }
async function saveSession(t: string, r: Role) { TOKEN = t; ROLE = r; DEMO = false; await AsyncStorage.multiSet([['sa_token', t], ['sa_role', r]]); await AsyncStorage.removeItem('sa_demo'); }

// Friendly messages only — raw server errors are never shown.
const KNOWN = ['not correct', 'expired', 'too many', 'wait a few', 'paused', 'being set up', 'not connected', 'used all', 'valid email', 'at least', 'already', 'only the owner', 'only failed', 'keyword', 'description is required', 'used by a scheduled', 'pick at least', 'choose a reel', 'setup key', 'log in again', 'contact shritech', 'wait a minute', 'enter the code'];
export class ApiError extends Error {}

export async function api<T = any>(action: string, data: Record<string, any> = {}, tok?: string): Promise<T> {
  if (DEMO) return demoApi(action, data) as Promise<T>;
  let r: Response;
  try { r = await fetch(BASE, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-session': tok ?? TOKEN }, body: JSON.stringify({ action, ...data }) }); }
  catch { throw new ApiError('No internet connection. Please try again.'); }
  const j: any = await r.json().catch(() => ({}));
  if (r.status === 401 && !tok && !['admin_login', 'admin_totp'].includes(action)) { await clearSession(); onLogout(); throw new ApiError('Please log in again.'); }
  if (!r.ok || j.error) {
    const m = String(j.error ?? '');
    throw new ApiError(KNOWN.some((k) => m.toLowerCase().includes(k)) ? m : 'Something didn’t work. Please try again in a moment.');
  }
  return j as T;
}

// ---- business users: email code ----
export const requestCode = (email: string) => api<{ sent: boolean; via: string }>('user_request_otp', { email }, '');
export async function verifyCode(email: string, code: string, business?: string) { const r = await api<{ token: string }>('user_verify_otp', { email, code, business }, ''); await saveSession(r.token, 'user'); }

export async function loginPassword(email: string, password: string) { const r = await api<{ token: string }>('user_login_password', { email, password }, ''); await saveSession(r.token, 'user'); }

// ---- admin: password + Google Authenticator ----
export type AdminStep = { token: string; stage: 'totp' | 'totp_enroll' | 'full'; secret?: string; otpauth?: string };
export const adminStatus = () => api<{ admin_exists: boolean }>('admin_status', {}, '');
export const adminSetup = (setup_key: string, email: string, password: string) => api<AdminStep>('admin_setup', { setup_key, email, password }, '');
export const adminLogin = (email: string, password: string) => api<AdminStep>('admin_login', { email, password }, '');
export const userForgot = (email: string) => api('user_forgot', { email }, '');
export const userReset = (email: string, code: string, password: string) => api('user_reset', { email, code, password }, '');
export const adminForgot = (email: string) => api('admin_forgot', { email }, '');
export const adminReset = (email: string, code: string, password: string) => api('admin_reset', { email, code, password }, '');
export async function adminTotp(stepToken: string, code: string) { const r = await api<AdminStep>('admin_totp', { code }, stepToken); await saveSession(r.token, 'admin'); }

/** Upload: signed URL → register. Files are later moved to GitHub automatically. */
export async function uploadFile(f: { uri: string; name: string; mime: string; size?: number }, title: string, onProgress?: (p: number) => void) {
  const kind = f.mime.startsWith('image') ? 'image' : 'video';
  if (DEMO) { for (let i = 1; i <= 10; i++) { await new Promise((res) => setTimeout(res, 120)); onProgress?.(i / 10); } return demoApi('register_media', { kind, title: title || f.name, demo_uri: f.uri }); }
  const u = await api<{ path: string; signed_url: string }>('upload_url', { filename: f.name, kind });
  const fd = new FormData(); fd.append('cacheControl', '3600');
  if (Platform.OS === 'web') { const blob = await (await fetch(f.uri)).blob(); fd.append('', blob, f.name); }
  else fd.append('', { uri: f.uri, name: f.name, type: f.mime } as any);
  await new Promise<void>((res, rej) => {
    const x = new XMLHttpRequest(); x.open('PUT', u.signed_url);
    x.upload.onprogress = (e) => { if (e.lengthComputable) onProgress?.(e.loaded / e.total); };
    x.onload = () => (x.status < 300 ? res() : rej(new ApiError('Upload didn’t finish. Please try again.')));
    x.onerror = () => rej(new ApiError('No internet connection. Please try again.'));
    x.send(fd);
  });
  return api('register_media', { path: u.path, kind, title: title || f.name.replace(/\.[^.]+$/, ''), size: f.size ?? null });
}

export const previewUrl = (u?: string | null) => {
  const m = String(u ?? '').match(/^https:\/\/raw\.githubusercontent\.com\/([^/]+)\/([^/]+)\/([^/]+)\/(.+)$/);
  return m ? `https://cdn.jsdelivr.net/gh/${m[1]}/${m[2]}@${m[3]}/${m[4]}` : (u ?? '');
};
