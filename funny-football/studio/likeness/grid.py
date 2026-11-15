"""Crop a reference photo to the 600x620 design box and draw a labelled 50 px grid for reading landmarks.
Usage: python3 grid.py <photo> <out_prefix> <left> <top> <right> <bottom>   (crop box as fractions 0..1)
Writes <out_prefix>_crop.jpg (clean, used by overlay) and <out_prefix>_grid.jpg (for measuring)."""
import sys
from PIL import Image, ImageDraw
src, pre = sys.argv[1], sys.argv[2]; l, t, r, b = map(float, sys.argv[3:7])
im = Image.open(src).convert('RGB'); w, h = im.size
c = im.crop((int(w * l), int(h * t), int(w * r), int(h * b))).resize((600, 620)); c.save(pre + '_crop.jpg')
d = ImageDraw.Draw(c)
for y in range(0, 620, 50): d.line([(0, y), (600, y)], fill=(255, 0, 0) if y % 100 == 0 else (255, 150, 150)); d.text((2, y + 1), str(y), fill=(255, 255, 0))
for x in range(0, 600, 50): d.line([(x, 0), (x, 620)], fill=(255, 0, 0) if x % 100 == 0 else (255, 150, 150)); d.text((x + 2, 2), str(x), fill=(255, 255, 0))
c.save(pre + '_grid.jpg')
