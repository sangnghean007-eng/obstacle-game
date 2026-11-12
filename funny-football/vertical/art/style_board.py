"""Render the reference head (CC BY-SA photo) in several graphic styles for comparison.
Usage: python3 style_board.py <reference.jpg> <out_dir>
"""
import sys, os, numpy as np, cv2
from sklearn.cluster import KMeans
ref, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
img = cv2.imread(ref)[120:1800, 400:1600]; H, W = img.shape[:2]
G = lambda p: (np.array(p, np.float32) * 2).astype(np.int32)
HEAD = G([(300,40),(360,45),(420,70),(470,100),(520,150),(555,200),(575,260),(580,320),(560,380),(540,410),(520,415),(555,430),(562,480),(556,540),(540,570),(510,582),(495,620),(480,680),(450,730),(400,770),(330,795),(290,802),(240,792),(190,762),(150,702),(120,622),(110,582),(90,586),(70,560),(55,500),(55,450),(70,430),(50,420),(30,380),(20,330),(30,270),(50,220),(90,150),(140,100),(200,60),(250,45)])
mask = np.zeros((H, W), np.uint8); cv2.fillPoly(mask, [HEAD], 255)
# mild caricature warp (bigger eyes, longer chin)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); sx, sy = xx.copy(), yy.copy()
def bulge(cx, cy, r, s):
    global sx, sy
    dx, dy = sx - cx, sy - cy; d2 = (dx * dx + dy * dy) / (r * r); f = np.where(d2 < 1, 1 - s * (1 - d2) ** 2, 1.0); sx, sy = cx + dx * f, cy + dy * f
bulge(415, 884, 200, 0.25); bulge(762, 870, 200, 0.25); bulge(582, 1250, 240, 0.15)
img = cv2.remap(img, sx, sy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
mask = cv2.remap(mask, sx, sy, cv2.INTER_LINEAR)
small = lambda im: cv2.resize(im, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
img, mask = small(img), small(mask); H, W = mask.shape
m = (cv2.GaussianBlur(mask, (0, 0), 3) > 127).astype(np.float32)
def save(name, rgb, bg=(245, 245, 245), outline=None):
    a = cv2.GaussianBlur(m, (0, 0), 0.8)[..., None]
    canvas = np.zeros_like(rgb, np.float32) + np.array(bg, np.float32)
    if outline is not None:
        ol = cv2.GaussianBlur(cv2.dilate(m, np.ones((11, 11), np.uint8)), (0, 0), 0.8)[..., None]
        canvas = canvas * (1 - ol) + np.array(outline, np.float32) * ol
    cv2.imwrite(f'{out}/{name}.jpg', (canvas * (1 - a) + rgb.astype(np.float32) * a).astype(np.uint8))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
def xdog(g, s=1.0, k=1.6, tau=0.98, eps=-1.0, phi=8):
    d = cv2.GaussianBlur(g, (0, 0), s) - tau * cv2.GaussianBlur(g, (0, 0), s * k)
    return np.where(d >= eps, 1.0, 1 + np.tanh(phi * (d - eps) / 10))

# 1) Low-poly
pts = [(x, y) for x in range(0, W, 40) for y in range(0, H, 40)]
edges = cv2.Canny(cv2.GaussianBlur(img, (5, 5), 0), 40, 110)
ys, xs = np.where((edges > 0) & (m > 0)); rnd = np.random.default_rng(1); sel = rnd.choice(len(xs), min(2600, len(xs)), replace=False)
pts += list(zip(xs[sel].tolist(), ys[sel].tolist()))
sub = cv2.Subdiv2D((0, 0, W, H))
for p in pts: sub.insert((float(min(p[0], W - 1)), float(min(p[1], H - 1))))
lp = np.zeros_like(img)
for t in sub.getTriangleList():
    tri = np.array(t, np.float32).reshape(3, 2)
    if (tri < 0).any() or (tri[:, 0] >= W).any() or (tri[:, 1] >= H).any(): continue
    c = tri.mean(0).astype(int); col = cv2.mean(img, mask=cv2.fillConvexPoly(np.zeros((H, W), np.uint8), tri.astype(np.int32), 255))[:3]
    cv2.fillConvexPoly(lp, tri.astype(np.int32), [int(v) for v in col], cv2.LINE_AA)
save('1_lowpoly', lp, (235, 200, 60))

# 2) Pop art (Warhol): 3-level posterize, bold colours
L = cv2.GaussianBlur(gray, (0, 0), 2.0)
q = np.digitize(L, np.percentile(L[m > 0], [28, 62]))
pal = np.array([[60, 20, 120], [40, 140, 255], [170, 230, 255]], np.uint8)      # BGR: purple, orange, light yellow
pop = pal[q]; pop = (pop * xdog(gray, 1.2)[..., None] ** 2).astype(np.uint8)
save('2_popart', pop, (200, 80, 230))

# 3) Comic halftone: flat colour + Ben-Day dots in shadows + ink
sm = img.copy()
for _ in range(3): sm = cv2.bilateralFilter(sm, 9, 30, 7)
lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
km = KMeans(6, n_init=3, random_state=0).fit(lab[(m.reshape(-1) > 0)][::15])
flat = cv2.cvtColor(km.cluster_centers_[km.predict(lab)].reshape(sm.shape).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
flat = np.clip((flat - 128) * 1.15 + 140, 0, 255)
dots = np.zeros((H, W), np.float32); dark = 1 - cv2.GaussianBlur(gray, (0, 0), 3) / 255
for y in range(0, H, 9):
    for x in range(0 if (y // 9) % 2 == 0 else 4, W, 9):
        r = dark[y, x] * 5.5 - 1.2
        if r > 0.6: cv2.circle(dots, (x, y), int(round(r)), 1, -1, cv2.LINE_AA)
comic = flat * (1 - 0.35 * dots[..., None]) * xdog(gray, 1.1)[..., None]
save('3_comic_halftone', comic, (70, 200, 255), outline=(20, 20, 20))

# 4) Ink sketch + watercolour wash
ink = xdog(gray, 0.9, tau=0.985, eps=-0.5, phi=12)
wash = cv2.stylization(img, sigma_s=40, sigma_r=0.45).astype(np.float32)
wash = 255 - (255 - wash) * 0.55
sketch = wash * ink[..., None]
save('4_ink_sketch', sketch, (250, 248, 240))

# 5) Pixel art (64 px wide, 14-colour palette)
pw = 72; ph = int(H * pw / W)
px = cv2.resize(cv2.bilateralFilter(img, 9, 40, 9), (pw, ph), interpolation=cv2.INTER_AREA)
pl = px.reshape(-1, 3).astype(np.float32); km2 = KMeans(14, n_init=3, random_state=0).fit(pl)
px = km2.cluster_centers_[km2.predict(pl)].reshape(px.shape).astype(np.uint8)
mpx = cv2.resize(m, (pw, ph), interpolation=cv2.INTER_NEAREST)
up = cv2.resize(px, (W, H), interpolation=cv2.INTER_NEAREST)
m_save = m.copy(); m[:] = cv2.resize(mpx, (W, H), interpolation=cv2.INTER_NEAREST)
save('5_pixel_art', up, (40, 30, 30)); m[:] = m_save

# 6) Oil painting
oil = cv2.xphoto.oilPainting(img, 7, 1) if hasattr(cv2, 'xphoto') else cv2.stylization(img, sigma_s=90, sigma_r=0.3)
oil = cv2.detailEnhance(oil, sigma_s=8, sigma_r=0.15)
save('6_painted', oil, (60, 50, 40))
print('done')
