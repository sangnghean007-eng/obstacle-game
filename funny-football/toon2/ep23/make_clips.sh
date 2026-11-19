#!/bin/bash
# one combo per video: render clip N at 60 fps, audio = master slice + pitched-down replay slice + end sting
set -e; cd "$(dirname "$0")"; S=${SCRATCH:-/tmp}; mkdir -p release
python3 audio.py $S/master.wav
python3 - "$S" <<'PY'
import sys; sys.path.insert(0, '../sfx'); from fx2 import *
m = Mix2(2.4, ep=2399); m.kazoo(.1, ['C5', 'E5', 'G5', 'C6'], .14, .12); m.crowd(.3, 'cheer', 1.6, .25); m.pop(.4, .3); m.write(sys.argv[1] + '/sting.wav')
PY
A=(0 0 3.0 5.6 8.4 11.2 14.2); D=(0 3.0 2.6 2.8 2.8 3.0 3.4); P0=(0 1.2 0.2 1.0 1.4 0.6 0.8); P1=(0 2.6 1.9 2.2 2.4 2.2 2.0)
NAMES=(x bicycle one-twos dominoes headers swirl tower)
for N in 1 2 3 4 5 6; do
  a=${A[$N]}; d=${D[$N]}; p0=$(python3 -c "print($a+${P0[$N]})"); p1=$(python3 -c "print($a+${P1[$N]})"); e=$(python3 -c "print($a+$d)")
  rm -rf $S/fr$N; CLIP=$N node render.js $S/fr$N 60
  if [ $N = 6 ]; then THIRD="[1:a]atrim=17.6:21.6,asetpts=PTS-STARTPTS[c]"; else THIRD="[2:a]asetpts=PTS-STARTPTS[c]"; fi
  ffmpeg -v error -y -framerate 60 -i $S/fr$N/f%05d.jpg -i $S/master.wav -i $S/sting.wav -filter_complex "[1:a]atrim=$a:$e,asetpts=PTS-STARTPTS[m];[1:a]atrim=$p0:$p1,asetpts=PTS-STARTPTS,asetrate=22050,aresample=44100[r];$THIRD;[m][r][c]concat=n=3:v=0:a=1,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-14:TP=-1.5:LRA=11[aa];[0:v]tmix=frames=2:weights='1 1',fps=30,split[x][y];[y]gblur=sigma=22,eq=brightness=-0.18:contrast=1.3[bl];[x][bl]blend=all_mode=screen:all_opacity=0.14,eq=contrast=1.05:saturation=1.08[v]" \
   -map "[v]" -map "[aa]" -c:v libx264 -crf 20 -preset slow -maxrate 10M -bufsize 20M -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart release/dream-duo-$N-${NAMES[$N]}-9x16.mp4
  rm -rf $S/fr$N; echo "clip $N done"
done
