"""Likeness check sheet: photo | 55% overlay | drawing.  Usage: python3 overlay_sheet.py <photo_crop.jpg> <portrait.png> <out.jpg>"""
import sys
from PIL import Image
ph = Image.open(sys.argv[1]).convert('RGBA'); dr = Image.open(sys.argv[2]).convert('RGBA')
bl = ph.copy(); a = dr.copy(); a.putalpha(a.getchannel('A').point(lambda v: int(v * 0.55))); bl.alpha_composite(a)
solo = Image.new('RGBA', (600, 620), (43, 47, 58, 255)); solo.alpha_composite(dr)
row = Image.new('RGB', (1800, 620)); [row.paste(im.convert('RGB'), (i * 600, 0)) for i, im in enumerate([ph, bl, solo])]
row.resize((1350, 465)).save(sys.argv[3], quality=85)
