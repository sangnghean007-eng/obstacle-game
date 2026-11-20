#!/bin/bash
# render_par.sh <episode_dir> <audio.py> <out.mp4> [workers] : same look as render_pro.sh but renders frames in parallel
set -e; EP=$1; OUT=$3; NW=${4:-4}; S=${SCRATCH:-/tmp}; TMP=$(mktemp -d -p "$S"); mkdir -p $TMP/fr
RJ=$(dirname "$0")/range_render.js
TOTAL=$(node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+require('path').resolve('$EP/scene.html')+'?render');console.log(Math.round(await p.evaluate(()=>DURATION)*60));await b.close();})()")
STEP=$(( (TOTAL + NW - 1) / NW )); for ((w=0; w<NW; w++)); do a=$((w*STEP)); b=$(( (w+1)*STEP < TOTAL ? (w+1)*STEP : TOTAL )); node $RJ $TMP/fr 60 $a $b $EP/scene.html & done; wait
python3 "$EP/$2" "$TMP/a.wav"
ffmpeg -v error -y -framerate 60 -i "$TMP/fr/f%05d.jpg" -i "$TMP/a.wav" -filter_complex "[0:v]tmix=frames=2:weights='1 1',fps=30,split[a][b];[b]gblur=sigma=22,eq=brightness=-0.18:contrast=1.3[bl];[a][bl]blend=all_mode=screen:all_opacity=0.14,eq=contrast=1.05:saturation=1.08,unsharp=5:5:0.4[v];[1:a]acompressor=threshold=-18dB:ratio=3:attack=8:release=120,extrastereo=m=1.4,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.79:level=false[aa]" -map "[v]" -map "[aa]" -c:v libx264 -crf 20 -preset slow -maxrate 10M -bufsize 20M -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
rm -rf "$TMP"
