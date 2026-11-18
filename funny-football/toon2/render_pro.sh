#!/bin/bash
# render_pro.sh <episode_dir> <audio.py> <out.mp4> — 60 fps render → 2-frame motion blur → 30 fps, bloom + grade, mastered audio.
set -e
EP=$1; OUT=$3; TMP=$(mktemp -d -p "${SCRATCH:-/tmp}")
node "$EP/render.js" "$TMP/fr" 60
python3 "$EP/$2" "$TMP/a.wav"
ffmpeg -v error -y -framerate 60 -i "$TMP/fr/f%05d.jpg" -i "$TMP/a.wav" -filter_complex "\
[0:v]tmix=frames=2:weights='1 1',fps=30,split[a][b];[b]gblur=sigma=22,eq=brightness=-0.18:contrast=1.3[bl];[a][bl]blend=all_mode=screen:all_opacity=0.14,eq=contrast=1.05:saturation=1.08,unsharp=5:5:0.4[v];\
[1:a]acompressor=threshold=-18dB:ratio=3:attack=8:release=120,extrastereo=m=1.4,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 20 -preset slow -maxrate 10M -bufsize 20M -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
rm -rf "$TMP"
