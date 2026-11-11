"""Turn a CC BY-SA reference photo into a stylized caricature illustration.

Steps: crop the head, apply caricature warps (bigger hair/eyes, longer chin, narrower jaw),
then repaint it as flat cel-shaded colour with ink lines.
Usage: python3 caricature.py <reference.jpg> <out_dir>
"""
import sys, os
import numpy as np, cv2
from sklearn.cluster import KMeans

ref, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
img = cv2.imread(ref)[120:1800, 400:1600]          # head crop, 1200x1680
H, W = img.shape[:2]
# head outline (crop coords)
pts = np.array([(300,40),(360,45),(420,70),(470,100),(520,150),(555,200),(575,260),(580,320),(560,380),(540,410),(520,415),(555,430),(562,480),(556,540),(540,570),(510,582),(495,620),(480,680),(450,730),(400,770),(330,795),(290,802),(240,792),(190,762),(150,702),(120,622),(110,582),(90,586),(70,560),(55,500),(55,450),(70,430),(50,420),(30,380),(20,330),(30,270),(50,220),(90,150),(140,100),(200,60),(250,45)]) * 2
mask = np.zeros((H, W), np.uint8); cv2.fillPoly(mask, [pts.astype(np.int32)], 255)

# ---- caricature warp (backward mapping on a padded canvas) ----
PT, PB, PX = 220, 260, 120                        # extra room for taller hair / longer chin
OH, OW = H + PT + PB, W + 2 * PX
yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
sx, sy = xx - PX, yy - PT                          # start: identity into crop coords
def bulge(cx, cy, r, s):
    global sx, sy
    dx, dy = sx - cx, sy - cy; d2 = (dx * dx + dy * dy) / (r * r)
    f = np.where(d2 < 1, 1 - s * (1 - d2) ** 2, 1.0)
    sx, sy = cx + dx * f, cy + dy * f
# hair & skull: expand everything above the brow
k = np.clip((760 - sy) / 700, 0, 1) ** 1.2
sy = sy + (sy - 760) * (-0.16 * k) ; sx = sx + (sx - 600) * (-0.10 * k)
# long chin + narrow jaw below the mouth
k2 = np.clip((sy - 1180) / 500, 0, 1)
sy = sy - (sy - 1180) * 0.17 * k2; sx = sx + (sx - 585) * 0.10 * k2
bulge(410, 880, 190, 0.30); bulge(770, 870, 190, 0.30)    # bigger eyes
bulge(580, 1250, 230, 0.18)                               # bigger mouth
bulge(580, 1000, 150, -0.10)                              # slightly slimmer nose
warp = cv2.remap(img, sx, sy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
wmask = cv2.remap(mask, sx, sy, cv2.INTER_LINEAR, borderValue=0)
cv2.imwrite(f'{out}/warp.jpg', warp)

def ink(gray, sigma=1.4, k=1.6, tau=0.985, phi=12, eps=-2):
    g1 = cv2.GaussianBlur(gray, (0, 0), sigma); g2 = cv2.GaussianBlur(gray, (0, 0), sigma * k)
    d = g1 - tau * g2
    e = np.where(d >= eps, 1.0, 1.0 + np.tanh(phi * (d - eps) / 255 * 10))
    return np.clip(e, 0, 1)

def quantize(im, K):
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    sel = lab[wmask.reshape(-1) > 0]
    km = KMeans(K, n_init=3, random_state=0).fit(sel[::20])
    q = km.cluster_centers_[km.predict(lab)].reshape(im.shape).astype(np.uint8)
    return cv2.cvtColor(q, cv2.COLOR_LAB2BGR)

def boost(im, sat=1.35, val=1.05):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= sat; hsv[..., 2] *= val
    return cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)

def finish(col, lines, name, outline=10):
    col = col.astype(np.float32) * lines[..., None]
    a = cv2.GaussianBlur(wmask, (0, 0), 1.2)
    ol = cv2.dilate(wmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (outline * 2 + 1,) * 2))
    rgba = np.zeros((OH, OW, 4), np.float32); rgba[..., 3] = ol; rgba[..., :3] = 22
    m = (a / 255.0)[..., None]
    rgba[..., :3] = rgba[..., :3] * (1 - m) + col * m
    rgba[..., 3] = np.maximum(ol, a)
    ys, xs = np.where(rgba[..., 3] > 0); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    cv2.imwrite(f'{out}/{name}.png', rgba[y0:y1 + 1, x0:x1 + 1].astype(np.uint8))

base = warp.copy()
for _ in range(2): base = cv2.bilateralFilter(base, 9, 40, 9)
gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32)

# A) Comic ink: cel colours + detailed ink lines
smoothA = cv2.pyrMeanShiftFiltering(boost(base), 12, 28)
colA = quantize(smoothA, 9)
finish(colA, ink(gray, 1.6) * 0.85 + 0.15 * ink(gray, 3.0), 'style_A_comic')

# B) Flat vector: few colours, heavy smoothing, bold main lines only
smoothB = cv2.pyrMeanShiftFiltering(boost(base, 1.5), 22, 40)
colB = quantize(smoothB, 6); colB = cv2.medianBlur(colB, 9)
linesB = ink(cv2.GaussianBlur(gray, (0, 0), 2.5), 2.2, tau=0.98)
linesB = cv2.morphologyEx((linesB * 255).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) / 255.0
finish(colB, linesB, 'style_B_flat', 12)

# C) Painted: stylization + soft ink
colC = cv2.stylization(boost(warp, 1.25), sigma_s=60, sigma_r=0.35)
finish(colC, 0.6 + 0.4 * ink(gray, 1.8), 'style_C_painted', 8)
print('done')
