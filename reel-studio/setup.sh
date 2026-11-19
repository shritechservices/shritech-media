#!/usr/bin/env bash
# Restores the reel-making workspace exactly as it was used to make the ShriTech reels.
# Usage (Linux, Python 3 + ffmpeg):  bash setup.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
pip install --quiet pillow numpy 2>/dev/null || pip install --quiet --break-system-packages pillow numpy

# Scripts expect these absolute paths
mkdir -p /home/claude/{reel,meme,salon/fonts,salon/src,salon/st,salon/out,clinic/src,clinic/st,clinic/out} /mnt/user-data/uploads
cp "$HERE"/reel/*.py /home/claude/reel/
for d in vo vo_en vo_hi2; do
  mkdir -p /home/claude/reel/$d
  cp "$HERE/reel/$d/info.json" /home/claude/reel/$d/
  for f in "$HERE"/reel/$d/*.flac; do ffmpeg -v error -y -i "$f" "/home/claude/reel/$d/$(basename "${f%.flac}").wav"; done
done
cp "$HERE/meme/meme.py" /home/claude/meme/
cp "$HERE"/salon/*.py /home/claude/salon/
cp "$HERE"/assets/fonts/*.ttf /home/claude/salon/fonts/
cp "$HERE"/clinic/*.py /home/claude/clinic/
cp "$HERE"/assets/screenshots/dark/*.jpg /mnt/user-data/uploads/
mkdir -p /home/claude/manual/screens && cp "$HERE"/assets/screenshots/light-manual/*.jpg /home/claude/manual/screens/
# Source audio as in.mp4-compatible inputs for the final mux step
cp "$HERE/salon/source-audio.m4a" /home/claude/salon/src/in.m4a
cp "$HERE/clinic/source-audio.m4a" /home/claude/clinic/src/in.m4a
echo "Workspace restored. See README.md for render commands."
