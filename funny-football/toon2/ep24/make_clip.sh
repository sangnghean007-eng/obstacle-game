#!/bin/bash
# make_clip.sh N main_end p0 p1 name : main + slow-mo replay (pitched audio) + card sting
set -e; cd "$(dirname "$0")"; S=${SCRATCH:-/tmp}; N=$1; E=$2; P0=$3; P1=$4; NAME=$5
python3 audio.py $S/m$N.wav
python3 - "$S" <<'PY'
import sys; sys.path.insert(0, '../sfx'); from fx2 import *
m = Mix2(2.4, ep=2499); m.kazoo(.1, ['C5', 'E5', 'G5', 'C6'], .14, .12); m.crowd(.3, 'cheer', 1.6, .25); m.pop(.4, .3); m.write(sys.argv[1] + '/sting.wav')
PY
rm -rf $S/fr$N; CLIP=$N node render.js $S/fr$N 60
ffmpeg -v error -y -framerate 60 -i $S/fr$N/f%05d.jpg -i $S/m$N.wav -i $S/sting.wav -filter_complex "[1:a]atrim=0:$E,asetpts=PTS-STARTPTS[m];[1:a]atrim=$P0:$P1,asetpts=PTS-STARTPTS,asetrate=22050,aresample=44100[r];[2:a]asetpts=PTS-STARTPTS[c];[m][r][c]concat=n=3:v=0:a=1,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-14:TP=-1.5:LRA=11[aa];[0:v]tmix=frames=2:weights='1 1',fps=30,split[x][y];[y]gblur=sigma=22,eq=brightness=-0.18:contrast=1.3[bl];[x][bl]blend=all_mode=screen:all_opacity=0.14,eq=contrast=1.05:saturation=1.08[v]" \
 -map "[v]" -map "[aa]" -c:v libx264 -crf 20 -preset slow -maxrate 10M -bufsize 20M -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart release/$NAME
rm -rf $S/fr$N
