import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';
import { demoApi } from './demo';

// The app talks to the SAME backend as the website (Cloudflare worker → Supabase "api" function).
// Nothing new is deployed: same password, same data, both sides always in sync.
export const BASE = 'https://instaworld.sbdigital2001.workers.dev';

let TOKEN = '';
let DEMO = false;
let onLogout: () => void = () => {};
export const setLogoutHandler = (f: () => void) => { onLogout = f; };
export const isDemo = () => DEMO;

export async function restoreSession() {
  const [t, d] = await Promise.all([AsyncStorage.getItem('st_token'), AsyncStorage.getItem('st_demo')]);
  TOKEN = t ?? ''; DEMO = d === '1';
  return DEMO || !!TOKEN;
}
export async function enterDemo() { DEMO = true; await AsyncStorage.setItem('st_demo', '1'); }
export async function clearSession() { TOKEN = ''; DEMO = false; await AsyncStorage.multiRemove(['st_token', 'st_demo']); }

// Friendly messages only — raw server errors are never shown.
const friendly = (raw: string, status: number) => {
  const r = raw.toLowerCase();
  if (r.includes('wrong password')) return 'That password is not correct.';
  if (r.includes('used by a scheduled post')) return 'This file is used in a scheduled post, so it can’t be removed.';
  if (r.includes('at least 8')) return 'Please use at least 8 characters.';
  if (r.includes('old password')) return 'The old password is not correct.';
  if (r.includes('only failed')) return 'Only failed posts can be retried.';
  if (r.includes('keyword')) return 'Please add at least one keyword.';
  if (r.includes('description is required')) return 'Please write the message to send.';
  if (status === 0) return 'No internet connection. Please try again.';
  return 'Something didn’t work. Please try again in a moment.';
};
export class ApiError extends Error {}

export async function api<T = any>(action: string, data: Record<string, any> = {}): Promise<T> {
  if (DEMO) return demoApi(action, data) as Promise<T>;
  let r: Response;
  try {
    r = await fetch(`${BASE}/api`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-session': TOKEN }, body: JSON.stringify({ action, ...data }) });
  } catch { throw new ApiError(friendly('', 0)); }
  const j = await r.json().catch(() => ({}));
  if (r.status === 401 && action !== 'login') { await clearSession(); onLogout(); throw new ApiError('Please log in again.'); }
  if (!r.ok || (j as any).error) throw new ApiError(friendly(String((j as any).error ?? ''), r.status));
  return j as T;
}

export async function login(password: string) {
  const r = await api<{ token: string }>('login', { password });
  TOKEN = r.token; DEMO = false;
  await AsyncStorage.setItem('st_token', TOKEN); await AsyncStorage.removeItem('st_demo');
}

/** Upload a picked file the same way the website does: signed URL → register in library. */
export async function uploadFile(f: { uri: string; name: string; mime: string; size?: number }, title: string, onProgress?: (p: number) => void) {
  const kind = f.mime.startsWith('image') ? 'image' : 'video';
  if (DEMO) { for (let i = 1; i <= 10; i++) { await new Promise((res) => setTimeout(res, 120)); onProgress?.(i / 10); } return demoApi('register_media', { kind, title: title || f.name, demo_uri: f.uri }); }
  const u = await api<{ path: string; signed_url: string }>('upload_url', { filename: f.name, kind });
  const fd = new FormData();
  fd.append('cacheControl', '3600');
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

/** Videos on raw.githubusercontent play better through jsDelivr (correct video type); posting still uses the raw link. */
export const previewUrl = (u?: string | null) => {
  const m = String(u ?? '').match(/^https:\/\/raw\.githubusercontent\.com\/([^/]+)\/([^/]+)\/([^/]+)\/(.+)$/);
  return m ? `https://cdn.jsdelivr.net/gh/${m[1]}/${m[2]}@${m[3]}/${m[4]}` : (u ?? '');
};
