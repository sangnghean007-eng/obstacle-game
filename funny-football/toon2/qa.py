"""qa.py — machine QA gate before any video is sent (owner, Nov 20 2026: "always optimise everything before export").
Every number is measured from the final mp4, so "it looks fine to me" is never the check.

    python3 toon2/qa.py path/to/video.mp4 [out_dir]

Checks (FAIL = fix and re-render, WARN = look at it):
  length       15–30 s (DATA RULE 21 Nov 2026: our winners and outliers are 12–21 s; default 18–25 s)
  loudness     integrated -15..-13 LUFS, true peak <= -1.0 dBTP
  silence      no dead air >= 0.3 s (music bed must never drop out)
  still        no fully frozen picture >= 0.6 s (designed holds still need a pop, bob or particles)
  blank        no black frames
  safe zones   writes safezones.png: every second of the video with the Reels/TikTok/Shorts UI shaded red.
               Any name, stamp, score or face inside red is covered by the app on the phone.
"""
import json, re, subprocess, sys, os

def run(args):
    return subprocess.run(args, capture_output=True, text=True).stderr

def main(src, out):
    os.makedirs(out, exist_ok=True); res = []
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    res.append(('length', 'PASS' if 15 <= dur <= 30 else 'WARN', f'{dur:.1f} s'))
    e = run(['ffmpeg', '-hide_banner', '-i', src, '-af', 'ebur128=peak=true', '-f', 'null', '-'])
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]); TP = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])
    res.append(('loudness', 'PASS' if -15 <= I <= -13 and TP <= -1.0 else 'FAIL', f'{I} LUFS, true peak {TP} dBTP'))
    e = run(['ffmpeg', '-hide_banner', '-i', src, '-af', 'silencedetect=noise=-42dB:d=0.3', '-f', 'null', '-'])
    gaps = [(float(a), float(b)) for a, b in re.findall(r'silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)', e)]
    gaps = [g for g in gaps if g[0] < dur - 0.6]  # a fade-out tail is allowed
    res.append(('silence', 'PASS' if not gaps else 'FAIL', ', '.join(f'{a:.1f}-{b:.1f}s' for a, b in gaps) or 'none >= 0.3 s'))
    e = run(['ffmpeg', '-hide_banner', '-i', src, '-vf', 'freezedetect=n=0.002:d=0.6', '-map', '0:v', '-f', 'null', '-'])
    fr = re.findall(r'freeze_start: ([\d.]+)[\s\S]*?freeze_duration: ([\d.]+)', e)
    res.append(('still', 'PASS' if not fr else 'FAIL', ', '.join(f'{float(a):.1f}s for {float(d):.1f}s' for a, d in fr) or 'none >= 0.6 s'))
    e = run(['ffmpeg', '-hide_banner', '-i', src, '-vf', 'blackdetect=d=0.03:pix_th=0.08', '-map', '0:v', '-f', 'null', '-'])
    bl = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', e)
    res.append(('blank', 'PASS' if not bl else 'FAIL', ', '.join(f'{float(a):.2f}-{float(b):.2f}s' for a, b in bl) or 'none'))
    # music variation: no 3-s stretch may be a near-copy of the 3 s before it (owner: "sound must not be monotonous")
    try:
        import numpy as np, subprocess as sp
        raw = sp.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
        a = np.frombuffer(raw, dtype='<i2').astype(float); win = 3 * 8000; reps = []
        def fp(x):
            sp_ = np.abs(np.fft.rfft(x * np.hanning(len(x))))[: 2000]; return sp_ / (np.linalg.norm(sp_) + 1e-9)
        for i in range(win, len(a) - win, 8000):
            c = float(fp(a[i:i + win]) @ fp(a[i - win:i]))
            if c > 0.985: reps.append(i / 8000)
        res.append(('variation', 'PASS' if len(reps) < 3 else 'WARN', f'{len(reps)} near-identical 3-s stretches' + (f' at {", ".join(f"{r:.0f}s" for r in reps[:5])}' if reps else '')))
    except Exception as e: res.append(('variation', 'WARN', f'not measured ({e})'))
    # safe-zone sheet: shade the parts of a 1080x1920 frame that phone apps cover (worst case of Reels/TikTok/Shorts)
    shade = ("drawbox=x=0:y=0:w=1080:h=210:color=red@0.35:t=fill,"      # status bar + top tabs
             "drawbox=x=0:y=1520:w=1080:h=400:color=red@0.35:t=fill,"    # username, caption, music, comment bar
             "drawbox=x=930:y=980:w=150:h=540:color=red@0.35:t=fill")    # like / comment / share rail
    sheet = os.path.join(out, 'safezones.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f'fps=1,scale=1080:1920,{shade},scale=180:-1,tile=10x{int(dur // 10) + 1}', '-frames:v', '1', sheet])
    res.append(('safe zones', 'LOOK', sheet))
    w = max(len(r[0]) for r in res)
    for n, s, d in res: print(f'{n:<{w}}  {s:<4}  {d}')
    bad = [r for r in res if r[1] == 'FAIL']
    print('QA PASS' if not bad else f'QA FAIL ({len(bad)}) — fix and re-render')
    json.dump(res, open(os.path.join(out, 'qa.json'), 'w'), indent=1)
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(sys.argv[1]), 'qa')))
