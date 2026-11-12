"""Hand-drawn-style caricature (flat colour + one shadow tone + brown ink outline),
built by tracing regions of a CC BY-SA reference photo and exaggerating them.
Usage: python3 hamid_style.py <reference.jpg> <out.png>
"""
import sys, numpy as np, cv2
ref, outp = sys.argv[1], sys.argv[2]
img = cv2.imread(ref)[120:1800, 400:1600]; H, W = img.shape[:2]
G = lambda p: (np.array(p, np.float32) * 2).astype(np.int32)
def poly(p, h=H, w=W):
    m = np.zeros((h, w), np.uint8); cv2.fillPoly(m, [p], 255); return m
HEAD = G([(300,40),(360,45),(420,70),(470,100),(520,150),(555,200),(575,260),(580,320),(560,380),(540,410),(520,415),(555,430),(562,480),(556,540),(540,570),(510,582),(495,620),(480,680),(450,730),(400,770),(330,795),(290,802),(240,792),(190,762),(150,702),(120,622),(110,582),(90,586),(70,560),(55,500),(55,450),(70,430),(50,420),(30,380),(20,330),(30,270),(50,220),(90,150),(140,100),(200,60),(250,45)])
HAIRZONE = G([(60,445),(100,415),(118,360),(140,318),(180,290),(235,268),(300,258),(370,262),(430,278),(478,300),(505,345),(515,380),(525,425),(600,400),(600,0),(0,0),(0,445)])
BEARDZONE = G([(112,530),(140,585),(178,632),(205,602),(232,590),(290,582),(350,587),(392,602),(412,632),(452,585),(486,525),(500,620),(485,690),(455,740),(400,780),(330,805),(290,812),(240,800),(185,768),(145,705),(115,622)])
BROWZONE = np.zeros((H, W), np.uint8)
for c, ax in [((412, 822), (130, 42)), ((778, 806), (140, 42))]: cv2.ellipse(BROWZONE, c, ax, 0, 0, 360, 255, -1)
MOUTHZONE = np.zeros((H, W), np.uint8); cv2.ellipse(MOUTHZONE, (582, 1252), (140, 58), 0, 0, 360, 255, -1)

# ---------------- caricature warp ----------------
PT, PB, PX = 240, 280, 140; OH, OW = H + PT + PB, W + 2 * PX
yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32); sx, sy = xx - PX, yy - PT
def bulge(cx, cy, r, s):
    global sx, sy
    dx, dy = sx - cx, sy - cy; d2 = (dx * dx + dy * dy) / (r * r)
    f = np.where(d2 < 1, 1 - s * (1 - d2) ** 2, 1.0); sx, sy = cx + dx * f, cy + dy * f
k = np.clip((760 - sy) / 700, 0, 1) ** 1.2; sy = sy + (sy - 760) * (-0.14 * k); sx = sx + (sx - 600) * (-0.06 * k)
k2 = np.clip((sy - 1120) / 560, 0, 1); sy = sy - (sy - 1120) * 0.24 * k2; sx = sx + (sx - 585) * 0.10 * k2
bulge(582, 1040, 210, 0.30)                          # bigger nose (signature of this style)
bulge(582, 1255, 220, 0.25)                          # bigger mouth
bulge(415, 884, 170, 0.22); bulge(762, 870, 170, 0.22)
Rm = lambda m: cv2.remap(m, sx, sy, cv2.INTER_LINEAR, borderValue=0)
P = cv2.remap(img, sx, sy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
def clean(m, blur=6, th=127):
    return (cv2.GaussianBlur(m, (0, 0), blur) > th).astype(np.uint8) * 255

lab = cv2.cvtColor(P, cv2.COLOR_BGR2LAB).astype(np.float32); L = lab[..., 0]
Ls = cv2.GaussianBlur(cv2.bilateralFilter(L, 0, 20, 8), (0, 0), 3)
head = clean(Rm(poly(HEAD)), 8)
hz, bz, brz, mz = [Rm(m) for m in (poly(HAIRZONE), poly(BEARDZONE), BROWZONE, MOUTHZONE)]

# hair: dark mass in hair zone, organic outline from the photo's curls
hair = ((cv2.GaussianBlur(L, (0, 0), 5) < 92) & (hz > 0) & (head > 0)).astype(np.uint8) * 255
hair = cv2.morphologyEx(hair, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
hair = clean(hair, 7)
n, lbl, st, _ = cv2.connectedComponentsWithStats(hair); hair = ((lbl == 1 + np.argmax(st[1:, 4])) * 255).astype(np.uint8)
# beard: darker than local skin inside beard zone
Lbig = cv2.GaussianBlur(L, (0, 0), 40)
dark = (Lbig - cv2.GaussianBlur(L, (0, 0), 4))
beard = clean(((dark > 6) & (bz > 0)).astype(np.uint8) * 255, 9)
beard = cv2.morphologyEx(beard, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
brows = clean(((dark > 14) & (brz > 0)).astype(np.uint8) * 255, 3)
lips = clean((((lab[..., 1] - 128) > np.median(lab[..., 1][head > 0]) - 128 + 6) & (mz > 0)).astype(np.uint8) * 255, 5)
mouthless_beard = cv2.bitwise_and(beard, cv2.bitwise_not(cv2.dilate(lips, np.ones((15, 15), np.uint8))))
skin_sh = clean(((Ls < np.percentile(Ls[(head > 0) & (hair == 0)], 33)) & (head > 0)).astype(np.uint8) * 255, 10)

# ---------------- paint ----------------
def hexc(h): h = h.lstrip('#'); return np.array([int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)], np.float32)
C = dict(line=hexc('#3a1d10'), skin=hexc('#dd9b70'), shade=hexc('#bb7650'), blush=hexc('#e8776a'), hair=hexc('#2b1a12'),
         hair2=hexc('#4a2e1d'), tip=hexc('#d7a648'), beard=hexc('#55331f'), lip=hexc('#c26a5a'), lip2=hexc('#9c4d42'))
canvas = np.zeros((OH, OW, 3), np.float32) + 255
def fill(mask, col, a=1.0):
    global canvas
    m = (mask.astype(np.float32) / 255 * a)[..., None]; canvas = canvas * (1 - m) + col * m
fill(head, C['skin']); fill(cv2.bitwise_and(skin_sh, head), C['shade'])
bl = np.zeros((OH, OW), np.uint8)
for c, ax in [((PX + 582, PT + 1015), (70, 55)), ((PX + 330, PT + 1010), (85, 45)), ((PX + 840, PT + 1000), (85, 45))]: cv2.ellipse(bl, c, ax, 0, 0, 360, 255, -1)
fill(cv2.GaussianBlur(Rm(cv2.resize(bl[PT:PT + H, PX:PX + W], (W, H))) if False else bl, (0, 0), 18), C['blush'], 0.45)
fill(mouthless_beard, C['beard'], 0.92)
fill(lips, C['lip'])
# hair with tonal clumps + blond tips
fill(hair, C['hair'])
clump = clean(((cv2.GaussianBlur(L, (0, 0), 3) > 55) & (hair > 0)).astype(np.uint8) * 255, 2)
fill(clump, C['hair2'])
hsv = cv2.cvtColor(P, cv2.COLOR_BGR2HSV)
tips = clean(((cv2.GaussianBlur(L, (0, 0), 1.5) > 95) & (hsv[..., 1] > 70) & (hair > 0)).astype(np.uint8) * 255, 1.5)
fill(tips, C['tip'])
fill(brows, C['hair'])

# ---------------- ink ----------------
def edge(mask, w):
    e = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (w, w)))
    return cv2.GaussianBlur(e, (0, 0), 1)
ink = np.zeros((OH, OW), np.float32)
for m, w in [(skin_sh, 3), (lips, 5), (brows, 3)]: ink = np.maximum(ink, edge(cv2.bitwise_and(m, head), w).astype(np.float32) / 255 * 0.55)
# feature lines from the photo (nose, ears, eyes, mouth) as brown ink
g = cv2.GaussianBlur(Ls, (0, 0), 1.8); d = g - 0.975 * cv2.GaussianBlur(Ls, (0, 0), 3.4)
feat = np.clip((-d - 1.5) / 3.5, 0, 1) * (hair == 0) * (head > 0) * (1 - (mouthless_beard > 0) * 0.85)
ink = np.maximum(ink, feat)
curl = cv2.GaussianBlur(L, (0, 0), 1.2) - 0.97 * cv2.GaussianBlur(L, (0, 0), 2.2)
ink = np.maximum(ink, np.clip((-curl - 3) / 6, 0, 1) * (hair > 0) * 0.8)
ink = np.maximum(ink, edge(hair, 7).astype(np.float32) / 255 * (head > 0))
ink = np.maximum(ink, edge(head, 13).astype(np.float32) / 255)
canvas = canvas * (1 - ink[..., None]) + C['line'] * ink[..., None]

# eyes: flat white + brown iris + heavy lid (drawn at the traced eye positions)
def to_out(x, y):  # forward-map a source point
    d = (sx - x) ** 2 + (sy - y) ** 2; i = np.argmin(d); return int(i % OW), int(i // OW)
for (x, y, w, h) in [(415, 886, 70, 20), (762, 872, 76, 20)]:
    cx, cy = to_out(x, y); wx = int(w * 1.15); hy = int(h * 1.2)
    eye = np.zeros((OH, OW), np.uint8); cv2.ellipse(eye, (cx, cy), (wx, hy), 0, 0, 360, 255, -1, cv2.LINE_AA)
    lid = np.zeros((OH, OW), np.uint8); cv2.ellipse(lid, (cx, cy - hy - 4), (wx + 6, hy + 2), 0, 0, 360, 255, -1)
    eye = cv2.bitwise_and(eye, cv2.bitwise_not(lid))
    fill(eye, hexc('#fbf7f2'))
    iris = np.zeros((OH, OW), np.uint8); cv2.circle(iris, (cx + 4, cy - 2), int(hy * 1.15), 255, -1, cv2.LINE_AA); iris = cv2.bitwise_and(iris, eye)
    fill(iris, hexc('#6a4326')); pup = np.zeros((OH, OW), np.uint8); cv2.circle(pup, (cx + 4, cy - 2), int(hy * 0.55), 255, -1, cv2.LINE_AA); fill(cv2.bitwise_and(pup, eye), hexc('#1c0f08'))
    hl = np.zeros((OH, OW), np.uint8); cv2.circle(hl, (cx - 4, cy - 9), 5, 255, -1, cv2.LINE_AA); fill(hl, hexc('#ffffff'))
    lidline = np.zeros((OH, OW), np.uint8); cv2.ellipse(lidline, (cx, cy + 2), (wx + 4, hy + 4), 0, 190, 350, 255, 7, cv2.LINE_AA)
    fill(lidline, C['line']); lo = np.zeros((OH, OW), np.uint8); cv2.ellipse(lo, (cx, cy - 2), (wx - 6, hy + 2), 0, 20, 160, 255, 3, cv2.LINE_AA); fill(lo, C['line'], 0.7)

alpha = cv2.dilate(head, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))).astype(np.float32)
rgba = np.dstack([canvas, alpha]).clip(0, 255).astype(np.uint8)
ys, xs = np.where(alpha > 0); rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
rgba = cv2.resize(rgba, (rgba.shape[1] // 2, rgba.shape[0] // 2), interpolation=cv2.INTER_AREA)
cv2.imwrite(outp, rgba); print(rgba.shape)
