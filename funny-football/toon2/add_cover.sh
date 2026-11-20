#!/bin/bash
# add_cover.sh <video.mp4> <cover.jpg> : puts the cover as the first 0.1 s of the video (owner, Nov 20 2026),
# so every platform that takes the first frame as thumbnail shows the cover. Audio is delayed 0.1 s to stay in sync.
# Run it once per final export (it refuses a video that already starts with the cover: see the .cover marker).
set -e; V=$1; C=$2; M="${V%.mp4}.cover"
[ -f "$M" ] && [ "$M" -nt "$V" ] && { echo "already has the cover: $V"; exit 0; }
T=$(mktemp --suffix=.mp4)
ffmpeg -v error -y -i "$V" -loop 1 -t 0.1 -framerate 30 -i "$C" -filter_complex \
 "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p[c];[0:v]fps=30,format=yuv420p,setsar=1[m];[c][m]concat=n=2:v=1:a=0[v];[0:a]adelay=100:all=1[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 20 -preset slow -maxrate 10M -bufsize 20M -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$T"
mv "$T" "$V"; touch "$M"; echo "cover added: $V"
