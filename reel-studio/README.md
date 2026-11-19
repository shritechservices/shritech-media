# ShriTech Reel Studio (backup)

Everything used to make the ShriTech reels, so they can be rebuilt **exactly** or used as a base for new ones.
Also contains a copy of the AutoPost website code (no secrets — keys live in Cloudflare/Supabase, not here).

## What's inside
| Folder | Contents |
|---|---|
| `reel/` | Reels 1–3 engine (`reel.py`, `reel2.py`, `captions.py`, scripts), voice-over clips (`vo*`, FLAC) |
| `meme/` | Comedy reel (`meme.py`) + its source audio |
| `salon/` | Salon reel (light theme) — `salon.py` is also the shared light-theme library (brand block, captions, thumbnail) |
| `clinic/` | Clinic reel (light theme) — reuses `salon.py` |
| `assets/screenshots/dark/` | Dark-theme ShriTech app screenshots (owner's phone) |
| `assets/screenshots/light-manual/` | Light-theme client screens from the User Manual (parts 1–19 only, no admin). Crop the footer: it has sample contact details |
| `assets/fonts/` | Poppins ExtraBold, Playfair Display Italic (OFL) |
| `audio/` | The **exact final audio track** of every published reel (.m4a) |
| `autopost/` | Website page, Cloudflare worker, Supabase edge function (backup copy) |

## Restore
```bash
bash setup.sh          # needs Linux, Python 3, ffmpeg; recreates /home/claude/... paths
```

## Rebuild a reel exactly (example: salon)
```bash
cd /home/claude/salon
python3 salon.py render 0 18.5 out/p1.mp4 & python3 salon.py render 18.5 36.7 out/p2.mp4 & wait
printf "file p1.mp4\nfile p2.mp4\n" > out/list.txt
ffmpeg -f concat -safe 0 -i out/list.txt -c copy out/v.mp4
ffmpeg -i out/v.mp4 -i <repo>/reel-studio/audio/reel4-salon.m4a -map 0:v -map 1:a -c copy -movflags +faststart out/final.mp4
python3 salon.py still thumb        # thumbnail -> out/ShriTech_Salon_Thumbnail.jpg
```
Clinic: same with `clinic.py`, ranges `0 24.5` and `24.5 48.9`, audio `reel5-clinic.m4a`.

Re-cutting from the source audio instead (rule: keep up to "फॉलो करो", drop the other creator's handle, add 0.5 s for the thumbnail):
- Salon: `-af "atrim=0:35.45,afade=t=out:st=35.25:d=0.2,adelay=500:all=1,apad=whole_dur=36.7"`
- Clinic: `-af "atrim=0:47.6,afade=t=out:st=47.45:d=0.15,adelay=500:all=1,apad=whole_dur=48.9"`

## House rules for new reels
- Light theme = green + yellow + white. Dark theme = green + yellow + black.
- Original visuals (don't copy the reference video), Hindi word-by-word subtitles.
- "Shri Tech" + ☎ 9993615146 under the subtitles for the whole video (animated), in the top bar and on the end card.
- A thumbnail for every reel (also the first 0.5 s of the video).
- Use ShriTech website screenshots in the visuals.

## Session handover
`ShriTech_Session_Handover.docx` — complete A-to-Z state of the project (upload it to a new Claude session to continue).
