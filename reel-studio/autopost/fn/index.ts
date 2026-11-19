import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, {
  auth: { persistSession: false },
});
const DAY = 86400000;
const enc = new TextEncoder();

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } });

async function sha256(s: string) {
  const h = await crypto.subtle.digest("SHA-256", enc.encode(s));
  return [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
function randHex(n = 32) {
  const a = new Uint8Array(n); crypto.getRandomValues(a);
  return [...a].map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function pbkdf2(pw: string, salt: string) {
  const key = await crypto.subtle.importKey("raw", enc.encode(pw), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", salt: enc.encode(salt), iterations: 120000, hash: "SHA-256" }, key, 256);
  return [...new Uint8Array(bits)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function getSettings(): Promise<Record<string, string>> {
  const { data } = await db.from("settings").select("key,value");
  const o: Record<string, string> = {};
  for (const r of data ?? []) o[r.key] = r.value ?? "";
  return o;
}
async function setSetting(key: string, value: string) {
  await db.from("settings").upsert({ key, value, updated_at: new Date().toISOString() });
}

async function checkSession(token?: string) {
  if (!token) return false;
  const { data } = await db.from("sessions").select("expires_at").eq("token", await sha256(token)).maybeSingle();
  return !!data && new Date(data.expires_at).getTime() > Date.now();
}

// ---------------- Meta Graph helpers ----------------
async function graph(s: Record<string, string>, method: "GET" | "POST", path: string, params: Record<string, string> = {}) {
  const v = s.graph_version || "v23.0";
  const url = new URL(`https://graph.facebook.com/${v}/${path}`);
  const body = new URLSearchParams({ ...params, access_token: s.page_token });
  let res: Response;
  if (method === "GET") {
    for (const [k, val] of body) url.searchParams.set(k, val);
    res = await fetch(url);
  } else {
    res = await fetch(url, { method: "POST", body });
  }
  const j = await res.json().catch(() => ({}));
  if (!res.ok || j.error) throw new Error(j.error?.message || `Graph error ${res.status}`);
  return j;
}

function cleanCollabs(v: unknown): string[] {
  const arr = Array.isArray(v) ? v : String(v ?? "").split(",");
  return [...new Set(arr.map((x) => String(x).trim().replace(/^@/, "").toLowerCase()).filter((x) => /^[a-z0-9._]{1,30}$/.test(x)))].slice(0, 3);
}

async function finalize(id: string) {
  const { data: p } = await db.from("posts").select("*").eq("id", id).single();
  if (!p) return;
  const want = p.platforms as string[];
  const st = (pl: string) => (pl === "facebook" ? p.fb_status : p.ig_status);
  const done = want.every((pl) => st(pl) === "posted" || st(pl) === "failed");
  if (!done) return;
  const ok = want.filter((pl) => st(pl) === "posted").length;
  const status = ok === want.length ? "posted" : ok === 0 ? "failed" : "partial";
  await db.from("posts").update({ status, posted_at: new Date().toISOString() }).eq("id", id);
}

async function publishDue() {
  const s = await getSettings();
  const log: string[] = [];
  if (!s.page_token) return ["no Meta token configured"];
  const nowIso = new Date().toISOString();
  const { data: due } = await db.from("posts").select("*, media(*)").eq("status", "scheduled").lte("scheduled_at", nowIso).limit(5);
  for (const p of due ?? []) {
    await db.from("posts").update({ status: "publishing", attempts: (p.attempts ?? 0) + 1 }).eq("id", p.id);
    const m = p.media;
    const errs: string[] = [];
    if (!m) {
      await db.from("posts").update({ status: "failed", error: "Media missing" }).eq("id", p.id);
      continue;
    }
    if (p.platforms.includes("facebook") && !p.fb_status) {
      try {
        if (m.kind === "video") {
          const r = await graph(s, "POST", `${s.page_id}/videos`, { file_url: m.public_url, description: p.caption ?? "" });
          await db.from("posts").update({ fb_status: "posted", fb_id: r.id, fb_link: `https://www.facebook.com/${s.page_id}/videos/${r.id}` }).eq("id", p.id);
        } else {
          const r = await graph(s, "POST", `${s.page_id}/photos`, { url: m.public_url, caption: p.caption ?? "" });
          const pid = r.post_id || r.id;
          await db.from("posts").update({ fb_status: "posted", fb_id: pid, fb_link: `https://www.facebook.com/${pid}` }).eq("id", p.id);
        }
        log.push(`FB ok ${p.id}`);
      } catch (e) {
        errs.push(`Facebook: ${(e as Error).message}`);
        await db.from("posts").update({ fb_status: "failed" }).eq("id", p.id);
      }
    }
    if (p.platforms.includes("instagram") && !p.ig_status) {
      try {
        const params: Record<string, string> = { caption: p.caption ?? "" };
        if (m.kind === "video") Object.assign(params, { media_type: "REELS", video_url: m.public_url, share_to_feed: "true" });
        else params.image_url = m.public_url;
        if (Array.isArray(p.collaborators) && p.collaborators.length) params.collaborators = JSON.stringify(p.collaborators);
        const r = await graph(s, "POST", `${s.ig_user_id}/media`, params);
        await db.from("posts").update({ ig_status: "processing", ig_container: r.id }).eq("id", p.id);
        log.push(`IG container ${r.id}`);
      } catch (e) {
        errs.push(`Instagram: ${(e as Error).message}`);
        await db.from("posts").update({ ig_status: "failed" }).eq("id", p.id);
      }
    }
    if (errs.length) await db.from("posts").update({ error: errs.join(" | ") }).eq("id", p.id);
    await finalize(p.id);
  }
  // Instagram containers waiting to finish processing
  const { data: proc } = await db.from("posts").select("*").eq("ig_status", "processing").limit(10);
  for (const p of proc ?? []) {
    try {
      const st = await graph(s, "GET", p.ig_container, { fields: "status_code,status" });
      if (st.status_code === "FINISHED") {
        const pub = await graph(s, "POST", `${s.ig_user_id}/media_publish`, { creation_id: p.ig_container });
        let link = "";
        try { link = (await graph(s, "GET", pub.id, { fields: "permalink" })).permalink; } catch (_) { /* ignore */ }
        await db.from("posts").update({ ig_status: "posted", ig_id: pub.id, ig_link: link }).eq("id", p.id);
        log.push(`IG posted ${pub.id}`);
      } else if (st.status_code === "ERROR" || st.status_code === "EXPIRED" ||
        Date.now() - new Date(p.scheduled_at).getTime() > 60 * 60 * 1000) {
        await db.from("posts").update({ ig_status: "failed", error: [p.error, `Instagram: ${st.status || st.status_code}`].filter(Boolean).join(" | ") }).eq("id", p.id);
      }
    } catch (e) {
      await db.from("posts").update({ ig_status: "failed", error: [p.error, `Instagram: ${(e as Error).message}`].filter(Boolean).join(" | ") }).eq("id", p.id);
    }
    await finalize(p.id);
  }
  return log;
}


// ---------------- Comment Management (comment → public reply + private message) ----------------
const DEFAULT_PUBLIC_REPLY = "आपको DM भेज दिया है ✅";
function ruleLive(r: any) {
  if (!r.active) return false;
  if (!r.active_till) return true;
  return Date.now() <= new Date(`${r.active_till}T23:59:59+05:30`).getTime();
}
function cleanKeywords(v: unknown): string[] {
  const arr = Array.isArray(v) ? v : String(v ?? "").split(",");
  return [...new Set(arr.map((x) => String(x).trim()).filter(Boolean).map((x) => x.slice(0, 40)))].slice(0, 10);
}
function matchKeyword(text: string, kws: string[]) {
  const t = String(text ?? "").toLowerCase().replace(/\s+/g, " ");
  for (const k of kws) { const kk = String(k).toLowerCase().trim(); if (kk && t.includes(kk)) return k; }
  return null;
}
function dmText(r: any) {
  let s = String(r.message).trim();
  if (r.image_url) s += `\n\n🖼️ इमेज: ${r.image_url}`;
  if (r.file_url) s += `\n📄 ${r.file_name || "डॉक्यूमेंट"}: ${r.file_url}`;
  return s;
}
async function sendPrivate(s: Record<string, string>, platform: string, commentId: string, text: string) {
  const params = { recipient: JSON.stringify({ comment_id: commentId }), message: JSON.stringify({ text }) };
  if (platform === "facebook") return await graph(s, "POST", `${s.page_id}/messages`, params);
  try { return await graph(s, "POST", `${s.page_id}/messages`, params); }
  catch (_) { return await graph(s, "POST", `${s.ig_user_id}/messages`, params); }
}
async function processComments(s: Record<string, string>) {
  const out: string[] = [];
  if (!s.page_token) return out;
  const { data: rules } = await db.from("comment_rules").select("*");
  const live = (rules ?? []).filter(ruleLive);
  for (const platform of ["instagram", "facebook"]) {
    const rs = live.filter((r: any) => r.platform === platform);
    if (!rs.length) continue;
    const oldest = Math.min(...rs.map((r: any) => new Date(r.created_at).getTime()));
    const since = Math.max(oldest, Date.now() - 7 * DAY);
    const items: any[] = [];
    try {
      if (platform === "instagram") {
        const med = await graph(s, "GET", `${s.ig_user_id}/media`, { fields: "id,timestamp,comments_count", limit: "15" });
        for (const m of med.data ?? []) {
          if (!m.comments_count || new Date(m.timestamp).getTime() < Date.now() - 60 * DAY) continue;
          const cs = await graph(s, "GET", `${m.id}/comments`, { fields: "id,text,timestamp,username,from{id,username}", limit: "50" });
          for (const c of cs.data ?? []) items.push({ id: c.id, text: c.text, time: c.timestamp, from_id: c.from?.id, from_username: c.from?.username || c.username, media_id: m.id });
        }
      } else {
        const posts = await graph(s, "GET", `${s.page_id}/posts`, { fields: "id,created_time", limit: "15" });
        for (const p of posts.data ?? []) {
          if (new Date(p.created_time).getTime() < Date.now() - 60 * DAY) continue;
          const cs = await graph(s, "GET", `${p.id}/comments`, { fields: "id,message,created_time,from{id,name}", limit: "50", order: "reverse_chronological", filter: "stream" });
          for (const c of cs.data ?? []) items.push({ id: c.id, text: c.message, time: c.created_time, from_id: c.from?.id, from_username: c.from?.name, media_id: p.id });
        }
      }
    } catch (e) { out.push(`${platform} fetch: ${(e as Error).message}`); continue; }
    for (const c of items) {
      const t = new Date(c.time).getTime();
      if (!t || t < since) continue;
      const own = platform === "instagram"
        ? (c.from_id === s.ig_user_id || (!!c.from_username && c.from_username === s.ig_username))
        : c.from_id === s.page_id;
      if (own) continue;
      let rule: any = null, kw: string | null = null;
      for (const r of rs) {
        if (t < new Date(r.created_at).getTime()) continue;
        const k = matchKeyword(c.text, r.keywords);
        if (k) { rule = r; kw = k; break; }
      }
      if (!rule) continue;
      const { data: ins, error } = await db.from("comment_log").insert({
        platform, comment_id: c.id, media_id: c.media_id, rule_id: rule.id, from_id: c.from_id ?? null,
        from_username: c.from_username ?? null, comment_text: c.text, matched: kw, comment_time: c.time,
      }).select("id").maybeSingle();
      if (error || !ins) continue; // already handled once
      const patch: Record<string, unknown> = {}; const errs: string[] = [];
      try { await sendPrivate(s, platform, c.id, dmText(rule)); patch.dm_status = "sent"; }
      catch (e) { patch.dm_status = "failed"; errs.push(`Message: ${(e as Error).message}`); }
      if (rule.reply_public) {
        const txt = String(rule.public_reply ?? "").trim() || DEFAULT_PUBLIC_REPLY;
        try {
          if (platform === "instagram") await graph(s, "POST", `${c.id}/replies`, { message: txt });
          else await graph(s, "POST", `${c.id}/comments`, { message: txt });
          patch.public_status = "sent";
        } catch (e) { patch.public_status = "failed"; errs.push(`Reply: ${(e as Error).message}`); }
      } else patch.public_status = "off";
      if (errs.length) patch.error = errs.join(" | ");
      await db.from("comment_log").update(patch).eq("id", ins.id);
      out.push(`${platform} ${c.id} dm:${patch.dm_status} reply:${patch.public_status}`);
    }
  }
  return out;
}

async function cleanup() {
  const cutoff = new Date(Date.now() - 30 * DAY).toISOString();
  const { data: old } = await db.from("posts").select("id").lt("scheduled_at", cutoff).in("status", ["posted", "partial", "failed", "cancelled"]);
  if (old?.length) await db.from("posts").delete().in("id", old.map((o) => o.id));
  // media is never deleted automatically (files stay on GitHub; library shows current month only)
  const removed = 0;
  await db.from("sessions").delete().lt("expires_at", new Date().toISOString());
  return { posts_removed: old?.length ?? 0, media_removed: removed };
}

// ---------------- request handler ----------------
Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const s0 = await getSettings();
  const wk = req.headers.get("x-worker-key") ?? "";
  if (!s0.worker_key_hash || (await sha256(wk)) !== s0.worker_key_hash) return json({ error: "forbidden" }, 403);

  let body: Record<string, any> = {};
  try { body = await req.json(); } catch (_) { /* empty */ }
  const action = body.action as string;
  const token = req.headers.get("x-session") ?? "";

  try {
    // ---- no login needed ----
    if (action === "status") return json({ password_set: !!s0.admin_hash });
    if (action === "setup_password") {
      if (s0.admin_hash) return json({ error: "Password already set" }, 400);
      if (!body.password || String(body.password).length < 8) return json({ error: "Use at least 8 characters" }, 400);
      const salt = randHex(16);
      await setSetting("admin_salt", salt);
      await setSetting("admin_hash", await pbkdf2(body.password, salt));
      return json({ ok: true });
    }
    if (action === "login") {
      if (!s0.admin_hash || (await pbkdf2(body.password ?? "", s0.admin_salt)) !== s0.admin_hash)
        return json({ error: "Wrong password" }, 401);
      const t = randHex(32);
      await db.from("sessions").insert({ token: await sha256(t), expires_at: new Date(Date.now() + 7 * DAY).toISOString() });
      return json({ token: t });
    }
    if (action === "tick") {
      const log = await publishDue();
      let comments: string[] = [];
      try { comments = await processComments(await getSettings()); } catch (e) { comments = [`comments error: ${(e as Error).message}`]; }
      return json({ log, comments });
    }
    if (action === "cleanup") return json(await cleanup());

    // ---- login required ----
    if (!(await checkSession(token))) return json({ error: "login required" }, 401);

    switch (action) {
      case "logout":
        await db.from("sessions").delete().eq("token", await sha256(token));
        return json({ ok: true });
      case "change_password": {
        if ((await pbkdf2(body.old ?? "", s0.admin_salt)) !== s0.admin_hash) return json({ error: "Old password wrong" }, 400);
        if (!body.password || String(body.password).length < 8) return json({ error: "Use at least 8 characters" }, 400);
        const salt = randHex(16);
        await setSetting("admin_salt", salt);
        await setSetting("admin_hash", await pbkdf2(body.password, salt));
        await db.from("sessions").delete().neq("token", "");
        return json({ ok: true });
      }
      case "get_settings":
        return json({
          page_id: s0.page_id ?? "", ig_user_id: s0.ig_user_id ?? "", graph_version: s0.graph_version || "v23.0",
          default_caption: s0.default_caption ?? "", page_name: s0.page_name ?? "", ig_username: s0.ig_username ?? "",
          token_saved: !!s0.page_token, token_hint: s0.page_token ? "…" + s0.page_token.slice(-6) : "",
        });
      case "save_settings": {
        for (const k of ["page_id", "ig_user_id", "graph_version", "default_caption"]) {
          if (typeof body[k] === "string") await setSetting(k, body[k].trim());
        }
        if (typeof body.page_token === "string" && body.page_token.trim()) await setSetting("page_token", body.page_token.trim());
        return json({ ok: true });
      }
      case "test_connection": {
        const s = await getSettings();
        const out: Record<string, string> = {};
        try {
          const pg = await graph(s, "GET", s.page_id, { fields: "name" });
          out.facebook = `✅ Page: ${pg.name}`; await setSetting("page_name", pg.name);
        } catch (e) { out.facebook = `❌ ${(e as Error).message}`; }
        // Auto-detect the Instagram Business account linked to the Page
        try {
          const lk = await graph(s, "GET", s.page_id, { fields: "instagram_business_account{id,username}" });
          const iba = lk.instagram_business_account;
          if (iba?.id) {
            s.ig_user_id = iba.id;
            await setSetting("ig_user_id", iba.id);
            out.detected = `Instagram account auto-detected: ${iba.id}`;
          } else {
            out.detected = "No Instagram Business account is linked to this Page";
          }
        } catch (e) { out.detected = `Could not auto-detect Instagram: ${(e as Error).message}`; }
        await setSetting("ig_username", "");
        if (!s.ig_user_id || s.ig_user_id === s.page_id) {
          out.instagram = `❌ ${out.detected}. (The Instagram ID must be different from the Page ID.)`;
          return json(out);
        }
        try {
          const ig = await graph(s, "GET", s.ig_user_id, { fields: "username" });
          out.instagram = `✅ @${ig.username}`; await setSetting("ig_username", ig.username);
        } catch (e) { out.instagram = `❌ ${(e as Error).message}`; return json(out); }
        try {
          const lim = await graph(s, "GET", `${s.ig_user_id}/content_publishing_limit`, { fields: "quota_usage,config" });
          const q = lim.data?.[0];
          if (q) out.instagram += ` · used ${q.quota_usage}/${q.config?.quota_total ?? "?"} posts in 24h`;
        } catch (e) { out.instagram += ` (publishing check: ${(e as Error).message})`; }
        return json(out);
      }
      case "upload_url": {
        const kind = body.kind === "image" ? "image" : "video";
        const ext = String(body.filename ?? "").split(".").pop()?.toLowerCase().replace(/[^a-z0-9]/g, "") || (kind === "video" ? "mp4" : "jpg");
        const path = `${new Date().toISOString().slice(0, 10)}/${randHex(10)}.${ext}`;
        const { data, error } = await db.storage.from("media").createSignedUploadUrl(path);
        if (error) throw error;
        return json({ path, signed_url: data.signedUrl, token: data.token });
      }
      case "register_media": {
        const kind = body.kind === "image" ? "image" : "video";
        const { data: pub } = db.storage.from("media").getPublicUrl(body.path);
        const { data, error } = await db.from("media").insert({
          path: body.path, public_url: pub.publicUrl, kind, title: body.title ?? null, size_bytes: body.size ?? null,
        }).select().single();
        if (error) throw error;
        return json(data);
      }
      case "list_media": {
        let q = db.from("media").select("*").order("created_at", { ascending: false });
        if (!body.all) {
          const ist = new Date(Date.now() + 330 * 60000);
          const start = new Date(Date.UTC(ist.getUTCFullYear(), ist.getUTCMonth(), 1) - 330 * 60000).toISOString();
          q = q.gte("created_at", start);
        }
        const { data } = await q.limit(body.all ? 300 : 120);
        return json(data ?? []);
      }
      case "delete_media": {
        const { count } = await db.from("posts").select("id", { count: "exact", head: true }).eq("media_id", body.id).eq("status", "scheduled");
        if (count) return json({ error: "This file is used by a scheduled post" }, 400);
        const { data: m } = await db.from("media").select("path").eq("id", body.id).single();
        if (m) await db.storage.from("media").remove([m.path]);
        await db.from("media").delete().eq("id", body.id);
        return json({ ok: true });
      }
      case "list_rules": {
        let q = db.from("comment_rules").select("*").order("created_at", { ascending: false });
        if (body.platform) q = q.eq("platform", body.platform);
        const { data } = await q;
        return json(data ?? []);
      }
      case "save_rule": {
        const platform = body.platform === "facebook" ? "facebook" : body.platform === "instagram" ? "instagram" : "";
        if (!platform) return json({ error: "Pick Instagram or Facebook" }, 400);
        const keywords = cleanKeywords(body.keywords);
        if (!keywords.length) return json({ error: "Add at least one keyword" }, 400);
        if (!String(body.message ?? "").trim()) return json({ error: "Description is required" }, 400);
        const till = body.active_till ? String(body.active_till).slice(0, 10) : null;
        if (till && !/^\d{4}-\d{2}-\d{2}$/.test(till)) return json({ error: "Invalid date" }, 400);
        const row: Record<string, unknown> = {
          platform, keywords, message: String(body.message).trim(), reply_public: body.reply_public !== false,
          public_reply: String(body.public_reply ?? "").trim() || null, active: body.active !== false, active_till: till,
          image_url: body.image_url || null, image_path: body.image_path || null,
          file_url: body.file_url || null, file_path: body.file_path || null, file_name: body.file_name || null,
          updated_at: new Date().toISOString(),
        };
        if (body.id) {
          const { data, error } = await db.from("comment_rules").update(row).eq("id", body.id).select().single();
          if (error) throw error; return json(data);
        }
        const { data, error } = await db.from("comment_rules").insert(row).select().single();
        if (error) throw error; return json(data);
      }
      case "toggle_rule": {
        await db.from("comment_rules").update({ active: !!body.active, updated_at: new Date().toISOString() }).eq("id", body.id);
        return json({ ok: true });
      }
      case "delete_rule": {
        const { data: r } = await db.from("comment_rules").select("image_path,file_path").eq("id", body.id).maybeSingle();
        const paths = [r?.image_path, r?.file_path].filter((p) => typeof p === "string" && p.startsWith("dm/")) as string[];
        if (paths.length) await db.storage.from("media").remove(paths);
        await db.from("comment_rules").delete().eq("id", body.id);
        return json({ ok: true });
      }
      case "comment_log": {
        let q = db.from("comment_log").select("*").order("created_at", { ascending: false }).limit(60);
        if (body.platform) q = q.eq("platform", body.platform);
        const { data } = await q;
        return json(data ?? []);
      }
      case "dm_upload_url": {
        const ext = String(body.filename ?? "").split(".").pop()?.toLowerCase().replace(/[^a-z0-9]/g, "") || "bin";
        const path = `dm/${new Date().toISOString().slice(0, 10)}/${randHex(8)}.${ext}`;
        const { data, error } = await db.storage.from("media").createSignedUploadUrl(path);
        if (error) throw error;
        const { data: pub } = db.storage.from("media").getPublicUrl(path);
        return json({ path, signed_url: data.signedUrl, public_url: pub.publicUrl });
      }
      case "overview": {
        const minFrom = Date.now() - 31 * DAY;
        const f0 = body.from ? new Date(body.from).getTime() : Date.now() - 30 * DAY;
        const t0 = body.to ? new Date(body.to).getTime() : Date.now() + 31 * DAY;
        const from = new Date(Math.max(isNaN(f0) ? minFrom : f0, minFrom)).toISOString();
        const to = new Date(isNaN(t0) ? Date.now() + 31 * DAY : t0).toISOString();
        const { data } = await db.from("posts").select("*, media(id,kind,public_url,title)")
          .gte("scheduled_at", from).lte("scheduled_at", to).order("scheduled_at");
        const { count: upcoming } = await db.from("posts").select("id", { count: "exact", head: true }).eq("status", "scheduled");
        const { data: last } = await db.from("posts").select("scheduled_at").eq("status", "scheduled").order("scheduled_at", { ascending: false }).limit(1);
        return json({ posts: data ?? [], now: new Date().toISOString(), upcoming: upcoming ?? 0, last_at: last?.[0]?.scheduled_at ?? null });
      }
      case "create_post": {
        const when = new Date(body.scheduled_at);
        if (isNaN(when.getTime())) return json({ error: "Invalid date" }, 400);
        const platforms = (body.platforms ?? ["facebook", "instagram"]).filter((p: string) => ["facebook", "instagram"].includes(p));
        if (!platforms.length) return json({ error: "Pick at least one platform" }, 400);
        const { data, error } = await db.from("posts").insert({
          title: body.title ?? null, caption: body.caption ?? "", media_id: body.media_id, platforms,
          collaborators: cleanCollabs(body.collaborators),
          scheduled_at: (when.getTime() < Date.now() ? new Date() : when).toISOString(),
        }).select().single();
        if (error) throw error;
        return json(data);
      }
      case "update_post": {
        const patch: Record<string, unknown> = {};
        for (const k of ["title", "caption", "scheduled_at", "platforms", "media_id"]) if (k in body) patch[k] = body[k];
        if ("collaborators" in body) patch.collaborators = cleanCollabs(body.collaborators);
        await db.from("posts").update(patch).eq("id", body.id).eq("status", "scheduled");
        return json({ ok: true });
      }
      case "cancel_post":
        await db.from("posts").update({ status: "cancelled" }).eq("id", body.id).eq("status", "scheduled");
        return json({ ok: true });
      case "post_now":
        await db.from("posts").update({ scheduled_at: new Date().toISOString() }).eq("id", body.id).eq("status", "scheduled");
        return json({ log: await publishDue() });
      case "retry_post": {
        const { data: p } = await db.from("posts").select("*").eq("id", body.id).in("status", ["failed", "partial"]).maybeSingle();
        if (!p) return json({ error: "Only failed posts can be retried" }, 400);
        const patch: Record<string, unknown> = { status: "scheduled", scheduled_at: new Date().toISOString(), error: null };
        if (p.fb_status === "failed") patch.fb_status = null;
        if (p.ig_status === "failed") { patch.ig_status = null; patch.ig_container = null; }
        await db.from("posts").update(patch).eq("id", body.id);
        return json({ ok: true });
      }
      default:
        return json({ error: "unknown action" }, 400);
    }
  } catch (e) {
    return json({ error: (e as Error).message }, 500);
  }
});
