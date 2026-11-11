"""'Photo-comic' caricature: keeps the real photo detail (likeness) but repaints it
with smoothed skin, punchier colour, soft cel tones and ink lines, plus a mild caricature warp.
Usage: python3 photocomic.py <reference.jpg> <out.png> [exaggeration]
"""
import sys, numpy as np, cv2
ref, outp = sys.argv[1], sys.argv[2]; EX = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
img = cv2.imread(ref)[120:1800, 400:1600]; H, W = img.shape[:2]
G = lambda p: (np.array(p, np.float32) * 2).astype(np.int32)
head = G([(300,40),(360,45),(420,70),(470,100),(520,150),(555,200),(575,260),(580,320),(560,380),(540,410),(520,415),(555,430),(562,480),(556,540),(540,570),(510,582),(495,620),(480,680),(450,730),(400,770),(330,795),(290,802),(240,792),(190,762),(150,702),(120,622),(110,582),(90,586),(70,560),(55,500),(55,450),(70,430),(50,420),(30,380),(20,330),(30,270),(50,220),(90,150),(140,100),(200,60),(250,45)])
mask = np.zeros((H, W), np.uint8); cv2.fillPoly(mask, [head], 255)
PT, PB, PX = 200, 220, 110; OH, OW = H + PT + PB, W + 2 * PX
yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32); sx, sy = xx - PX, yy - PT
def bulge(cx, cy, r, s):
    global sx, sy
    dx, dy = sx - cx, sy - cy; d2 = (dx * dx + dy * dy) / (r * r)
    f = np.where(d2 < 1, 1 - s * EX * (1 - d2) ** 2, 1.0); sx, sy = cx + dx * f, cy + dy * f
k = np.clip((760 - sy) / 700, 0, 1) ** 1.2; sy = sy + (sy - 760) * (-0.2 * EX * k); sx = sx + (sx - 600) * (-0.12 * EX * k)
k2 = np.clip((sy - 1150) / 520, 0, 1); sy = sy - (sy - 1150) * 0.2 * EX * k2; sx = sx + (sx - 585) * 0.12 * EX * k2
bulge(415, 884, 200, 0.4); bulge(762, 870, 200, 0.4); bulge(582, 1250, 240, 0.25)
P = cv2.remap(img, sx, sy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
m = cv2.remap(mask, sx, sy, cv2.INTER_LINEAR, borderValue=0)
m = (cv2.GaussianBlur(m, (0, 0), 7) > 127).astype(np.float32)
# drop pink stadium background caught between curls near the outline (upper half only)
labP = cv2.cvtColor(cv2.GaussianBlur(P, (0, 0), 1.5), cv2.COLOR_BGR2LAB).astype(np.float32)
pink = ((labP[..., 1] - 128) > 1.1 * (labP[..., 2] - 128) + 4) & (labP[..., 1] > 140) & (labP[..., 0] > 70)
band = (m > 0) & (cv2.erode(m, np.ones((61, 61), np.uint8)) == 0) & (yy < PT + 900 * 1.0)
m[pink & band] = 0
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
m = (cv2.GaussianBlur(m, (0, 0), 2.5) > 0.5).astype(np.float32)

sm = P.copy()
for _ in range(4): sm = cv2.bilateralFilter(sm, 9, 30, 7)
# soft cel: blend smoothed photo with a quantized version of itself
lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).astype(np.float32)
Lq = np.round(lab[..., 0] / 22) * 22; Lq = cv2.GaussianBlur(Lq, (0, 0), 2.2)
lab[..., 0] = 0.55 * lab[..., 0] + 0.45 * Lq
lab[..., 1] = 128 + (lab[..., 1] - 128) * 1.25; lab[..., 2] = 128 + (lab[..., 2] - 128) * 1.3
col = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
col = np.clip((col - 128) * 1.08 + 136, 0, 255)                    # a bit brighter / punchier
gray = cv2.cvtColor(P, cv2.COLOR_BGR2GRAY).astype(np.float32)
g1 = cv2.GaussianBlur(gray, (0, 0), 1.5); g2 = cv2.GaussianBlur(gray, (0, 0), 2.6)
d = g1 - 0.98 * g2
ink = np.clip((-d - 1.5) / 5, 0, 1); ink = cv2.GaussianBlur(ink, (0, 0), 0.8)
col = col * (1 - 0.75 * ink[..., None]) + 18 * 0.75 * ink[..., None]
alpha = cv2.GaussianBlur(m, (0, 0), 1.2)
ol = cv2.GaussianBlur(cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))), (0, 0), 1.2)
rgb = col * alpha[..., None] + 20 * (1 - alpha[..., None])
A = np.maximum(alpha, ol)
rgba = np.dstack([rgb, A * 255]).clip(0, 255).astype(np.uint8)
ys, xs = np.where(A > 0.01); rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
rgba = cv2.resize(rgba, (rgba.shape[1] // 2, rgba.shape[0] // 2), interpolation=cv2.INTER_AREA)
cv2.imwrite(outp, rgba); print(rgba.shape)
