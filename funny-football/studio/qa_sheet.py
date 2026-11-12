"""Studio QA: build a review contact sheet with the phone UI danger zones painted on every frame,
and flag frames where bright caption-like pixels fall inside those zones.
Usage: python3 qa_sheet.py <frames_dir> <fps> <out.jpg> <t1,t2,...>
Danger zones (1080x1920, conservative mix of TikTok/Reels/Shorts estimates):
  top 120 px, bottom 380 px, right 150 px (buttons column above the bottom bar).
"""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
frames, fps, out, times = sys.argv[1], float(sys.argv[2]), sys.argv[3], [float(x) for x in sys.argv[4].split(',')]
TOP, BOTTOM, RIGHT = 120, 380, 150
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
tiles, report = [], []
for t in times:
    im = Image.open(f'{frames}/f{int(round(t * fps)):05d}.jpg').convert('RGB'); W, H = im.size
    a = np.asarray(im).astype(int)
    # caption-like pixels: very bright white or saturated yellow
    white = (a[..., 0] > 235) & (a[..., 1] > 235) & (a[..., 2] > 235)
    yellow = (a[..., 0] > 230) & (a[..., 1] > 190) & (a[..., 2] < 90)
    cap = white | yellow
    zone = np.zeros(cap.shape, bool); zone[:TOP] = True; zone[H - BOTTOM:] = True; zone[TOP:H - BOTTOM, W - RIGHT:] = True
    score = (cap & zone).sum() / zone.sum()
    flag = score > 0.02
    report.append((t, round(float(score) * 100, 2), flag))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for box in [(0, 0, W, TOP), (0, H - BOTTOM, W, H), (W - RIGHT, TOP, W, H - BOTTOM)]: d.rectangle(box, fill=(255, 0, 0, 70))
    im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); d = ImageDraw.Draw(im)
    d.text((20, 140), f'{t:.1f}s' + ('  CHECK' if flag else ''), fill=(255, 60, 60) if flag else (255, 255, 0), font=font)
    tiles.append(im.resize((W // 3, H // 3)))
cols = min(8, len(tiles)); rows = (len(tiles) + cols - 1) // cols; w, h = tiles[0].size
sheet = Image.new('RGB', (cols * w, rows * h), (20, 20, 20))
for i, tl in enumerate(tiles): sheet.paste(tl, ((i % cols) * w, (i // cols) * h))
sheet.save(out, quality=85)
for t, s, f in report: print(f'{t:6.1f}s  caption-pixels-in-danger-zone {s:5.2f}%  {"<-- CHECK" if f else ""}')
