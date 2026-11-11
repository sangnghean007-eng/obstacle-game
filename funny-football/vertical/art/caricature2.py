"""Region-based caricature illustration from a CC BY-SA reference photo.
Usage: python3 caricature2.py <reference.jpg> <out_dir> [exaggeration=1.0]
"""
import sys, os
import numpy as np, cv2

ref, out = sys.argv[1], sys.argv[2]; EX = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
REAL_EYES = len(sys.argv) > 4 and sys.argv[4] == 'real'
os.makedirs(out, exist_ok=True)
img = cv2.imread(ref)[120:1800, 400:1600]; H, W = img.shape[:2]
G = lambda p: (np.array(p, np.float32) * 2).astype(np.int32)
head = G([(300,40),(360,45),(420,70),(470,100),(520,150),(555,200),(575,260),(580,320),(560,380),(540,410),(520,415),(555,430),(562,480),(556,540),(540,570),(510,582),(495,620),(480,680),(450,730),(400,770),(330,795),(290,802),(240,792),(190,762),(150,702),(120,622),(110,582),(90,586),(70,560),(55,500),(55,450),(70,430),(50,420),(30,380),(20,330),(30,270),(50,220),(90,150),(140,100),(200,60),(250,45)])
hair = G([(70,432),(100,410),(118,360),(140,318),(180,290),(235,268),(300,258),(370,262),(430,278),(478,300),(505,345),(515,380),(522,418),(540,410),(560,380),(580,320),(575,260),(555,200),(520,150),(470,100),(420,70),(360,45),(300,40),(250,45),(200,60),(140,100),(90,150),(50,220),(30,270),(20,330),(30,380),(50,420)])
def poly(p):
    m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [p], 255); return m
M_head, M_hair = poly(head), poly(hair)
M_mouth = np.zeros((H, W), np.uint8); cv2.ellipse(M_mouth, (582, 1250), (150, 62), 0, 0, 360, 255, -1)
M_eyes = np.zeros((H, W), np.uint8)
for c in [(415, 896), (762, 882)]: cv2.ellipse(M_eyes, c, (104, 40), 0, 0, 360, 255, -1)
M_lower = np.zeros((H, W), np.uint8); cv2.fillPoly(M_lower, [G([(112,530),(140,585),(178,632),(205,602),(232,590),(290,582),(350,587),(392,602),(412,632),(452,585),(486,525),(495,620),(480,680),(450,730),(400,770),(330,795),(290,802),(240,792),(190,762),(150,702),(120,622)])], 255)
M_brow = np.zeros((H, W), np.uint8)
for c, ax in [((412, 822), (140, 46)), ((778, 806), (150, 46))]: cv2.ellipse(M_brow, c, ax, 0, 0, 360, 255, -1)

# ---------- vector eyes (drawn in source space at 4x, then warped with the face) ----------
SS = 4
eyeL = np.zeros((H * SS // 2, W * SS // 2, 4), np.uint8)   # half-res crop *4 = 2x crop
def E(x, y): return (int(x * SS / 2), int(y * SS / 2))
def almond(c, w, h, tilt=0):
    cx, cy = c; up, lo = [], []
    for i in range(41):
        t = -1 + i / 20; x = cx + t * w
        up.append(E(x, cy - h * (1 - t * t) ** 0.8 - tilt * t - (6 if t > 0 else 0) * (1 - t * t)))
        lo.append(E(x, cy + h * 0.55 * (1 - t * t) ** 1.2 - tilt * t))
    return np.array(up), np.array(lo)
for (c, w, h, look) in ([] if REAL_EYES else [((415, 886), 76, 21, (5, -3)), ((762, 872), 82, 21, (1, -3))]):
    up, lo = almond(c, w, h)
    shape = np.vstack([up, lo[::-1]])
    m = np.zeros(eyeL.shape[:2], np.uint8); cv2.fillPoly(m, [shape], 255)
    layer = np.zeros_like(eyeL); cv2.fillPoly(layer, [shape], (232, 240, 246, 255), cv2.LINE_AA)
    ic = E(c[0] + look[0], c[1] + look[1] - 3)
    cv2.circle(layer, ic, int(21 * SS / 2), (40, 62, 98, 255), -1, cv2.LINE_AA)
    cv2.circle(layer, ic, int(16 * SS / 2), (28, 44, 74, 255), -1, cv2.LINE_AA)
    cv2.circle(layer, ic, int(8 * SS / 2), (8, 8, 10, 255), -1, cv2.LINE_AA)
    cv2.circle(layer, (ic[0] - 12, ic[1] - 12), int(4.5 * SS / 2), (255, 255, 255, 255), -1, cv2.LINE_AA)
    layer[m == 0] = 0
    cv2.polylines(layer, [up], False, (18, 12, 8, 255), int(7 * SS / 2), cv2.LINE_AA)   # heavy upper lid
    cv2.polylines(layer, [lo], False, (40, 30, 25, 200), int(2.5 * SS / 2), cv2.LINE_AA)
    crease = up.copy(); crease[:, 1] -= int(11 * SS / 2); crease = crease[6:-4]
    cv2.polylines(layer, [crease], False, (50, 70, 110, 170), int(2.5 * SS / 2), cv2.LINE_AA)
    eyeL = np.maximum(eyeL, layer) if False else np.where(layer[..., 3:] > 0, layer, eyeL)
# nose, lips, ears (vector ink, source space)
def pl(points, col, w, closed=False):
    global eyeL
    lay_ = np.zeros_like(eyeL); cv2.polylines(lay_, [np.array([E(*q) for q in points])], closed, col, int(w * SS / 2), cv2.LINE_AA)
    eyeL = np.where(lay_[..., 3:] > 0, lay_, eyeL)
def curve(p0, c, p1, n=24):
    return [((1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0], (1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1]) for t in np.linspace(0, 1, n)]
INK = (14, 18, 30, 255)
pl(curve((505, 1028), (462, 1062), (518, 1094)), INK, 5)
pl(curve((655, 1028), (700, 1060), (645, 1094)), INK, 5)
pl(curve((535, 1102), (582, 1116), (628, 1102)), (30, 40, 70, 220), 4)
for c in [(550, 1094), (612, 1094)]:
    l2 = np.zeros_like(eyeL); cv2.ellipse(l2, E(*c), (int(15 * SS / 2), int(7 * SS / 2)), 0, 0, 360, (20, 26, 45, 255), -1, cv2.LINE_AA); eyeL = np.where(l2[..., 3:] > 0, l2, eyeL)
pl(curve((468, 1250), (582, 1272), (697, 1246)), INK, 6)
pl(curve((480, 1236), (520, 1212), (580, 1222)) + curve((582, 1222), (640, 1210), (688, 1234)), (40, 50, 90, 170), 3)
pl(curve((505, 1276), (582, 1318), (660, 1272)), (40, 50, 90, 150), 3)
for (c, a0, a1) in [((168, 1010), 100, 260), ((1098, 984), -80, 80)]:
    l2 = np.zeros_like(eyeL); cv2.ellipse(l2, E(*c), (int(24 * SS / 2), int(46 * SS / 2)), 0, a0, a1, (30, 50, 90, 230), int(5 * SS / 2), cv2.LINE_AA); eyeL = np.where(l2[..., 3:] > 0, l2, eyeL)
l2 = np.zeros_like(eyeL); cv2.circle(l2, E(1072, 1106), int(10 * SS / 2), (250, 250, 255, 255), -1, cv2.LINE_AA); cv2.circle(l2, E(1072, 1106), int(10 * SS / 2), (20, 20, 20, 255), int(3 * SS / 2), cv2.LINE_AA); cv2.circle(l2, E(1068, 1102), int(3 * SS / 2), (255, 255, 255, 255), -1, cv2.LINE_AA)
eyeL = np.where(l2[..., 3:] > 0, l2, eyeL)
eyeL = cv2.resize(eyeL, (W, H), interpolation=cv2.INTER_AREA)
EYE_BOX = [(415, 884), (762, 870)]

# ---------- caricature warp ----------
PT, PB, PX = 260, 300, 140
OH, OW = H + PT + PB, W + 2 * PX
yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
sx, sy = xx - PX, yy - PT
def bulge(cx, cy, r, s):
    global sx, sy
    dx, dy = sx - cx, sy - cy; d2 = (dx * dx + dy * dy) / (r * r)
    f = np.where(d2 < 1, 1 - s * EX * (1 - d2) ** 2, 1.0); sx, sy = cx + dx * f, cy + dy * f
k = np.clip((760 - sy) / 700, 0, 1) ** 1.2
sy = sy + (sy - 760) * (-0.20 * EX * k); sx = sx + (sx - 600) * (-0.12 * EX * k)
k2 = np.clip((sy - 1150) / 520, 0, 1)
sy = sy - (sy - 1150) * 0.20 * EX * k2; sx = sx + (sx - 585) * 0.12 * EX * k2
bulge(410, 885, 200, 0.34); bulge(772, 872, 200, 0.34); bulge(582, 1250, 240, 0.2); bulge(585, 1010, 150, -0.08)
R = lambda a, interp=cv2.INTER_LINEAR: cv2.remap(a, sx, sy, interp, borderMode=cv2.BORDER_REPLICATE if a.ndim == 3 else cv2.BORDER_CONSTANT, borderValue=0)
P = R(img, cv2.INTER_CUBIC)
mh, mhair, mmouth, meyes, mlow, mbrow = [R(m).astype(np.float32) / 255 for m in (M_head, M_hair, M_mouth, M_eyes, M_lower, M_brow)]
mbrow = cv2.GaussianBlur(mbrow, (0, 0), 8)
mh = (cv2.GaussianBlur(mh, (0, 0), 9) > 0.5).astype(np.float32)
mhair = cv2.GaussianBlur(mhair, (0, 0), 3); mskin = np.clip(mh - mhair, 0, 1)

def hexc(h): h = h.lstrip('#'); return np.array([int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)], np.float32)  # BGR
def smoothstep(e0, e1, x): t = np.clip((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)
def lay(base, col, a): return base * (1 - a[..., None]) + col * a[..., None]

lab = cv2.cvtColor(P, cv2.COLOR_BGR2LAB).astype(np.float32); L = lab[..., 0]
Ls = cv2.bilateralFilter(L, 0, 18, 12); Ls = cv2.GaussianBlur(Ls, (0, 0), 14)
Lbig = cv2.GaussianBlur(L, (0, 0), 22)

# ---------- skin: 3-tone soft cel shading ----------
sk = Ls[mskin > 0.5]; lo, hi = np.percentile(sk, 22), np.percentile(sk, 78)
c_sh, c_mid, c_hi, c_spec = hexc('#9c5f3c'), hexc('#c98b5e'), hexc('#e2a97a'), hexc('#f6d2ad')
canvas = np.zeros((OH, OW, 3), np.float32) + c_mid
canvas = lay(canvas, c_sh, 1 - smoothstep(lo - 6, lo + 6, Ls))
canvas = lay(canvas, c_hi, smoothstep(hi - 6, hi + 6, Ls))
canvas = lay(canvas, c_spec, smoothstep(np.percentile(sk, 97) - 2, np.percentile(sk, 97) + 2, Ls) * 0.9 * (1 - cv2.GaussianBlur(R(M_mouth).astype(np.float32) / 255, (0, 0), 8)))
# cheek blush
blush = np.zeros((OH, OW), np.float32)
for c in [(PX + 330, PT + 1040), (PX + 860, PT + 1030)]: cv2.ellipse(blush, c, (90, 50), 0, 0, 360, 1, -1)
canvas = lay(canvas, hexc('#d9735a'), cv2.GaussianBlur(R(cv2.resize(blush[PT:PT+H, PX:PX+W], (W, H))), (0, 0), 25) * 0.25)

# ---------- dark details (brows, eyes, nostrils, beard stubble) ----------
dark = np.clip((Lbig - L) / 38, 0, 1)
dark = cv2.GaussianBlur(dark, (0, 0), 1.0)
meyes = cv2.GaussianBlur(meyes, (0, 0), 6)
if REAL_EYES:
    eyezone = meyes.copy(); meyes = meyes * 0
brow_eye = smoothstep(0.3, 0.45, cv2.GaussianBlur(dark, (0, 0), 1.5)) * mskin * (mbrow if not REAL_EYES else np.clip(mbrow + eyezone, 0, 1)) * (1 - meyes)
if REAL_EYES:
    # keep the real eye: stylized photo pixels (iris, lids, whites) inside the eye zone
    eyephoto = cv2.bilateralFilter(P, 0, 30, 4).astype(np.float32)
    eyephoto = cv2.convertScaleAbs(eyephoto, alpha=1.15, beta=8).astype(np.float32)
    canvas = lay(canvas, eyephoto, smoothstep(0.35, 0.8, eyezone))
beard = cv2.GaussianBlur(mlow * (1 - smoothstep(0.2, 0.5, cv2.GaussianBlur(mmouth, (0, 0), 4))), (0, 0), 16) * mskin
beard = smoothstep(0.2, 0.8, beard) * (0.45 + 0.55 * smoothstep(0.1, 0.4, cv2.GaussianBlur(dark, (0, 0), 5)))
canvas = lay(canvas, hexc('#3b2518'), beard * 0.55)
rng = np.random.default_rng(3); noise = cv2.GaussianBlur(rng.random((OH, OW)).astype(np.float32), (0, 0), 1.2)
canvas = lay(canvas, hexc('#21140c'), smoothstep(0.52, 0.6, noise) * beard * 0.35)
canvas = lay(canvas, hexc('#24160f'), brow_eye * (1 if not REAL_EYES else (1 - smoothstep(0.35, 0.8, eyezone))))

# ---------- eyes ----------
white = smoothstep(0.55, 0.75, (L - Lbig) / 40 + 0.6) * meyes * (1 - brow_eye)
pass

# ---------- lips ----------
a = lab[..., 1]; lips = smoothstep(4, 10, a - np.median(a[mskin > 0.5])) * mmouth
lips = cv2.GaussianBlur(lips, (0, 0), 2)
lipcol = lay(np.zeros_like(canvas) + hexc('#94574a'), hexc('#b0705f'), smoothstep(np.percentile(Ls[mmouth > .5], 50), np.percentile(Ls[mmouth > .5], 85), Ls))
canvas = lay(canvas, lipcol, smoothstep(0.3, 0.6, lips))

# ---------- hair: dark curls with blond tips ----------
Lh = cv2.bilateralFilter(L, 0, 25, 3)
core = cv2.GaussianBlur(cv2.erode((mhair > 0.5).astype(np.uint8), np.ones((31, 31), np.uint8)).astype(np.float32), (0, 0), 6)
hcol = lay(np.zeros_like(canvas) + hexc('#22160f'), hexc('#5a3b22'), smoothstep(45, 70, Lh) * core)
hsv = cv2.cvtColor(P, cv2.COLOR_BGR2HSV).astype(np.float32)
blond = smoothstep(80, 120, Lh) * smoothstep(40, 90, hsv[..., 1]) * core
hcol = lay(hcol, hexc('#e3b04b'), blond)
hcol = lay(hcol, hexc('#fbe08a'), smoothstep(125, 150, Lh) * blond)
canvas = lay(canvas, hcol, mhair)

# ---------- ink lines ----------
g = cv2.GaussianBlur(Ls, (0, 0), 1.6); d = g - 0.985 * cv2.GaussianBlur(Ls, (0, 0), 2.6)
inkface = smoothstep(-0.5, -2.0, d) * mskin * (1 - mlow * 0.8) * (1 - meyes)
gh = cv2.GaussianBlur(Lh, (0, 0), 1.1); dh = gh - 0.97 * cv2.GaussianBlur(Lh, (0, 0), 1.8)
inkhair = smoothstep(-1.0, -4.0, dh) * mhair
canvas = lay(canvas, hexc('#120b07'), np.clip(inkface * 0.9 + inkhair * 0.75, 0, 1))

eyeW = R(eyeL)
ea = eyeW[..., 3].astype(np.float32) / 255
canvas = lay(canvas, eyeW[..., :3].astype(np.float32), ea)

# ---------- outline + alpha, 2x supersample down ----------
alpha = cv2.GaussianBlur(mh, (0, 0), 1.2)
ol = cv2.dilate((mh > 0.5).astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))).astype(np.float32) / 255
ol = cv2.GaussianBlur(ol, (0, 0), 1.2)
rgb = lay(np.zeros_like(canvas) + hexc('#151515'), canvas, alpha)
A = np.maximum(ol, alpha)
rgba = np.dstack([rgb, A * 255]).clip(0, 255).astype(np.uint8)
ys, xs = np.where(A > 0.01); rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
rgba = cv2.resize(rgba, (rgba.shape[1] // 2, rgba.shape[0] // 2), interpolation=cv2.INTER_AREA)
cv2.imwrite(f'{out}/head_illustrated.png', rgba)
print(rgba.shape)
