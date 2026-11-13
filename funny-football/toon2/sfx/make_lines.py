"""Short, clear English voice lines using espeak-ng + MBROLA voices (generic voices, no imitation of real people).
Usage: python3 make_lines.py <out_dir> "<id>|<voice>|<pitch>|<speed>|<text>" ...
"""
import sys, subprocess, wave, io, numpy as np
SR = 44100
out = sys.argv[1]
for spec in sys.argv[2:]:
    name, voice, pitch, speed, text = spec.split('|', 4)
    raw = subprocess.run(['espeak-ng', '-v', voice, '-p', pitch, '-s', speed, '-a', '180', '--stdout', text], capture_output=True, check=True).stdout
    w = wave.open(io.BytesIO(raw)); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    x = np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x)
    i = np.where(np.abs(x) > 0.01)[0]; x = x[i[0]:i[-1] + 1]
    x = x / (np.abs(x).max() + 1e-9) * 0.95
    o = wave.open(f'{out}/{name}.wav', 'wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((x * 32767).astype('<i2').tobytes()); o.close()
    print(name, round(len(x) / SR, 2))
