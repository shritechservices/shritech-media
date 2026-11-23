# ShriTech AutoPost — mobile app (Expo)

A light/dark, animated phone app for the same ShriTech AutoPost system as the website.

## How it connects (nothing new on the server)
- The app calls the **same** endpoint the website uses: `https://instaworld.sbdigital2001.workers.dev/api`
  (Cloudflare worker → Supabase `api` function → same database).
- Same admin password as the website. Whatever you schedule in the app shows on the website, and the other way round.
- Uploads go through the same signed-upload flow as the website. No Supabase keys, Meta tokens or GitHub tokens are inside the app.
- **Demo mode** ("Try demo" on the login screen) uses built-in sample data only — it never touches the live system. Use it for client demos.

## Screens
Home (live countdown to the next post, stats, next 7 days) · Calendar (month view, tap a day) · New post (pick media, caption, collab, Facebook/Instagram, date + time in IST) · Media library (upload from phone, schedule, remove) · Auto replies (comment & story rules, on/off, activity) · Post details (preview, edit, post now, cancel, try again) · Settings (Auto / Light / Dark theme, connection check, change password, log out).

## Run it on your phone (free)
1. Install **Expo Go** from the Play Store / App Store.
2. On a computer with Node 20+: `npm install` then `npx expo start`.
3. Scan the QR code with Expo Go (Android) or the Camera app (iPhone).

## Make an installable Android app (free)
1. Create a free account at expo.dev.
2. `npm install -g eas-cli` → `eas login` → `eas build:configure`
3. `eas build -p android --profile preview` → you get a link to download the **.apk** (free tier, queue may take a few minutes).

## Tech
Expo SDK 58 · React Navigation (tabs + stack) · expo-video · expo-image-picker · expo-linear-gradient · Poppins font · built-in Animated API (works in Expo Go and on web).
