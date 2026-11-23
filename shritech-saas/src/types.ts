export type Platform = 'facebook' | 'instagram';
export type Media = { id: string; kind: 'video' | 'image'; public_url: string; title: string | null; created_at?: string; size_bytes?: number | null; local?: any; poster?: any };
export type Post = {
  id: string; title: string | null; caption: string | null; scheduled_at: string; status: 'scheduled' | 'publishing' | 'posted' | 'partial' | 'failed' | 'cancelled';
  platforms: Platform[]; collaborators?: string[] | null; media?: Media | null; media_id?: string;
  fb_status?: string | null; ig_status?: string | null; fb_link?: string | null; ig_link?: string | null; error?: string | null;
};
export type Rule = {
  id: string; platform: Platform; trigger: 'comment' | 'story'; keywords: string[]; message: string; reply_public: boolean; public_reply: string | null;
  active: boolean; active_till: string | null; created_at?: string; story_mentions?: boolean;
};
export type LogItem = { id: string; platform: Platform; from_username: string | null; comment_text: string | null; matched: string | null; dm_status: string | null; public_status: string | null; created_at: string };
export type Settings = { page_name: string; ig_username: string; token_saved: boolean; default_caption: string };
