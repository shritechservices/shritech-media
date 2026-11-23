import { useCallback, useState } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import { api } from './api';
import type { Post } from './types';

export function useOverview(range: () => { from: string; to: string }, deps: any[] = []) {
  const [posts, setPosts] = useState<Post[]>([]); const [upcoming, setUp] = useState(0);
  const [loading, setLoading] = useState(true); const [refreshing, setRefreshing] = useState(false); const [failed, setFailed] = useState(false);
  const load = useCallback(async (pull = false) => {
    if (pull) setRefreshing(true);
    try { const r = await api<any>('overview', range()); setPosts(r.posts); setUp(r.upcoming); setFailed(false); }
    catch { setFailed(true); } finally { setLoading(false); setRefreshing(false); }
  }, deps);
  useFocusEffect(useCallback(() => { load(); const iv = setInterval(() => load(), 30000); return () => clearInterval(iv); }, [load]));
  return { posts, upcoming, loading, refreshing, failed, reload: () => load(true) };
}

export type Me = { user: { id: string; email: string; name: string | null; role: 'owner' | 'member' }; tenant: { id: string; name: string; status: string; plan: string; valid_till: string | null; post_quota: number; used_this_month: number; page_name: string | null; ig_username: string | null; connected: boolean; live: boolean; default_caption: string; contact_phone: string; request_note: string } };
let ME: Me | null = null;
export async function getMe(force = false) { if (!ME || force) ME = await api<Me>('me'); return ME; }
export const resetMe = () => { ME = null; };
// kept for screens that read the default caption
export async function getSettings(force = false) { const m = await getMe(force); return { default_caption: m.tenant.default_caption, page_name: m.tenant.page_name ?? '', ig_username: m.tenant.ig_username ?? '', token_saved: m.tenant.connected }; }
export const resetSettings = resetMe;
