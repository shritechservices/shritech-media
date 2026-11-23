import { useCallback, useState } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import { api } from './api';
import type { Post, Settings } from './types';

/** Overview of posts for a time window (same call the website uses). */
export function useOverview(range: () => { from: string; to: string }, deps: any[] = []) {
  const [posts, setPosts] = useState<Post[]>([]); const [upcoming, setUp] = useState(0); const [lastAt, setLast] = useState<string | null>(null);
  const [loading, setLoading] = useState(true); const [refreshing, setRefreshing] = useState(false); const [failed, setFailed] = useState(false);
  const load = useCallback(async (pull = false) => {
    if (pull) setRefreshing(true);
    try { const r = await api<any>('overview', range()); setPosts(r.posts); setUp(r.upcoming); setLast(r.last_at); setFailed(false); }
    catch { setFailed(true); } finally { setLoading(false); setRefreshing(false); }
  }, deps);
  useFocusEffect(useCallback(() => { load(); const iv = setInterval(() => load(), 30000); return () => clearInterval(iv); }, [load]));
  return { posts, upcoming, lastAt, loading, refreshing, failed, reload: () => load(true) };
}

let SETTINGS: Settings | null = null;
export async function getSettings(force = false) { if (!SETTINGS || force) SETTINGS = await api<Settings>('get_settings'); return SETTINGS; }
export const resetSettings = () => { SETTINGS = null; };
