"""Clear English voice lines with SVOX Pico (generic voices; no imitation of real people).
Usage: python3 make_pico.py <out_dir> "<id>|<lang en-US/en-GB>|<pitch %>|<speed %>|<text>" ...
"""
import sys, subprocess, wave, tempfile, os, numpy as np
SR = 44100
out = sys.argv[1]
for spec in sys.argv[2:]:
    name, lang, pitch, speed, text = spec.split('|', 4)
    tmp = tempfile.mktemp(suffix='.wav')
    subprocess.run(['pico2wave', '-l', lang, '-w', tmp, f"<pitch level='{pitch}'><speed level='{speed}'>{text}</speed></pitch>"], check=True)
    w = wave.open(tmp); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768; os.remove(tmp)
    x = np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x)
    i = np.where(np.abs(x) > 0.01)[0]; x = x[i[0]:i[-1] + 1]
    x = x / (np.abs(x).max() + 1e-9) * 0.95
    o = wave.open(f'{out}/{name}.wav', 'wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((x * 32767).astype('<i2').tobytes()); o.close()
    print(name, round(len(x) / SR, 2))
