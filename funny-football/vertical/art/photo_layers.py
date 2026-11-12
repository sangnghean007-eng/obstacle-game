"""Derive flat-colour shading + beard density layers from the CC BY-SA reference photo,
warped through the same caricature transform T used in neymar_vector.js, and export them
as data-URI PNGs (neymar_layers.js) that the vector drawing composites under its ink lines.
Usage: python3 photo_layers.py <reference.jpg> <out.js> [ex]
"""
import sys, base64, numpy as np, cv2
ref, outjs = sys.argv[1], sys.argv[2]; EX = float(sys.argv[3]) if len(sys.argv) > 3 else 1.1
photo = cv2.imread(ref)[120:1800, 400:1600]
photo = cv2.resize(photo, (600, 840), interpolation=cv2.INTER_AREA)      # grid space 1:1
S, X0, Y0, OW, OH = 2, -60, -120, 720, 1080                               # output: grid [-60,660]x[-120,960] at 2x

def bulge(x, y, cx, cy, r, s):
    dx, dy = x - cx, y - cy; d2 = (dx * dx + dy * dy) / (r * r)
    f = np.where(d2 < 1, 1 + s * (1 - d2) ** 2, 1.0); return cx + dx * f, cy + dy * f
def T(x, y, ex=EX):
    k = np.clip((380 - y) / 330, 0, 1); m = y < 380
    y = np.where(m, 380 - (380 - y) * (1 + 0.05 * ex * k), y); x = np.where(m, 290 + (x - 290) * (1 + 0.03 * ex * k), x)
    k2 = np.clip((y - 590) / 210, 0, 1); m2 = y > 590
    yn = np.where(m2, 590 + (y - 590) * (1 + 0.10 * ex * k2), y); x = np.where(m2, 290 + (x - 290) * (1 - 0.08 * ex * k2), x); y = yn
    x, y = bulge(x, y, 290, 525, 95, 0.28 * ex); x, y = bulge(x, y, 292, 622, 115, 0.08 * ex)
    x, y = bulge(x, y, 172, 425, 60, 0.10 * ex); x, y = bulge(x, y, 348, 418, 60, 0.10 * ex)
    return x, y
gy, gx = np.mgrid[0:OH * S, 0:OW * S].astype(np.float32)
px, py = gx / S + X0, gy / S + Y0
qx, qy = px.copy(), py.copy()
for _ in range(25):                                   # invert T by fixed-point iteration
    tx, ty = T(qx, qy); qx += (px - tx) * 0.8; qy += (py - ty) * 0.8
src = cv2.remap(photo, qx.astype(np.float32), qy.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def polymask(pts):
    m = np.zeros((840, 600), np.uint8); cv2.fillPoly(m, [np.array(pts, np.int32)], 255)
    return cv2.remap(m, qx.astype(np.float32), qy.astype(np.float32), cv2.INTER_LINEAR, borderValue=0).astype(np.float32) / 255
FACE = [(95,330),(100,400),(100,470),(100,560),(110,622),(130,682),(165,732),(215,772),(270,796),(300,799),(345,791),(400,766),(440,726),(470,670),(478,600),(482,520),(485,450),(480,380),(470,300),(400,250),(290,232),(180,250),(110,300)]
BEARD = [(103,470),(100,560),(110,622),(130,682),(165,732),(215,772),(270,796),(300,799),(345,791),(400,766),(440,726),(470,670),(478,600),(481,520),(479,470),(455,540),(420,580),(385,590),(290,575),(200,590),(160,580),(125,540)]
LIPS = [(200,616),(230,596),(290,596),(352,596),(384,613),(362,640),(292,654),(222,640)]
face, beardz, lips = polymask(FACE), polymask(BEARD), polymask(LIPS)
face = cv2.erode(face, np.ones((5, 5), np.uint8))
L = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
Ls = cv2.GaussianBlur(cv2.bilateralFilter(L, 0, 22, 10), (0, 0), 7)
vals = Ls[face > 0.5]
def cel(mask_soft):
    return np.clip((mask_soft - 0.5) * 3 + 0.5, 0, 1)
sh1 = cel(cv2.GaussianBlur((Ls < np.percentile(vals, 30)).astype(np.float32), (0, 0), 4)) * face
sh2 = cel(cv2.GaussianBlur((Ls < np.percentile(vals, 9)).astype(np.float32), (0, 0), 4)) * face
hi = cel(cv2.GaussianBlur((Ls > np.percentile(vals, 88)).astype(np.float32), (0, 0), 5)) * face
# beard density: darkness relative to local skin, inside beard zone, stylised into 3 levels
Lbig = cv2.GaussianBlur(L, (0, 0), 30)
dens = np.clip((Lbig - cv2.GaussianBlur(L, (0, 0), 2.5)) / 30 + 0.15, 0, 1) * cv2.GaussianBlur(beardz, (0, 0), 6) * (1 - cv2.GaussianBlur(lips, (0, 0), 3))
dens = cv2.GaussianBlur(dens, (0, 0), 9)
zone = cv2.GaussianBlur(beardz, (0, 0), 10) * (1 - cv2.GaussianBlur(lips, (0, 0), 4))
beard = np.clip(zone * 1.3, 0, 1) * (0.34 + 0.3 * np.clip(dens * 2.2, 0, 1))
beard = cv2.GaussianBlur(beard, (0, 0), 2)
rng = np.random.default_rng(2); dots = cv2.GaussianBlur((rng.random(beard.shape) < 0.06).astype(np.float32), (0, 0), 0.9) * 3
beard = np.clip(beard + dots * (beard > 0.25) * 0.22, 0, 0.9)

HAIRZ = [(60,445),(100,415),(118,360),(140,318),(180,290),(235,268),(300,258),(370,262),(430,278),(478,300),(505,345),(515,380),(525,425),(560,430),(620,300),(600,0),(0,0),(0,300),(30,445)]
hz = polymask(HAIRZ)
lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(np.float32); Lh, A, B = lab[..., 0], lab[..., 1] - 128, lab[..., 2] - 128
dark = Lh < 52; blond = (B - A > 6) & (B > 14) & (Lh < 80)
hm = ((dark | blond) & (hz > 0.5)).astype(np.uint8) * 255
hm = cv2.morphologyEx(hm, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
hm = cv2.morphologyEx(hm, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
n_, lbl, st, _ = cv2.connectedComponentsWithStats(hm); hm = ((lbl == 1 + np.argmax(st[1:, 4])) * 255).astype(np.uint8)
hm = cv2.morphologyEx(hm, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
ff = hm.copy(); h_, w_ = ff.shape; cv2.floodFill(ff, np.zeros((h_ + 2, w_ + 2), np.uint8), (0, 0), 255)
hm = hm | cv2.bitwise_not(ff)                                   # fill interior holes
hm = (cv2.GaussianBlur(hm, (0, 0), 2.2) > 127).astype(np.float32)
hm = np.maximum(hm, (cv2.GaussianBlur(hz, (0, 0), 2) > 0.5).astype(np.float32) * cv2.erode(hm, np.ones((25, 25), np.uint8)))
Lq = cv2.bilateralFilter(Lh, 0, 18, 3)
hcol = np.zeros(src.shape, np.float32) + np.array([8, 13, 22], np.float32)                 # BGR '#160d08'
hcol[Lq > 26] = [24, 38, 59]                                                               # '#3b2618'
yb = cv2.GaussianBlur(blond.astype(np.float32), (0, 0), 1.2) > 0.45
hcol[yb] = [69, 154, 201]                                                                  # '#c99a45'
hcol[yb & (Lq > 62)] = [120, 205, 238]                                                     # '#eecd78'
ink = cv2.GaussianBlur(Lq, (0, 0), 1.0) - 0.96 * cv2.GaussianBlur(Lq, (0, 0), 2.0)
hcol[(ink < -3.5) & ~yb] = [6, 10, 16]
edge = cv2.morphologyEx((hm * 255).astype(np.uint8), cv2.MORPH_GRADIENT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
hcol[edge] = [15, 28, 58]                                                                  # '#3a1c0f' outline
hrgba = np.dstack([hcol, np.maximum(hm, edge.astype(np.float32)) * 255]).astype(np.uint8)
HAIRPNG = 'data:image/png;base64,' + base64.b64encode(cv2.imencode('.png', hrgba)[1]).decode()

def png(col, a):
    bgr = np.zeros((OH * S, OW * S, 4), np.uint8); bgr[..., :3] = col[::-1]; bgr[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    return 'data:image/png;base64,' + base64.b64encode(cv2.imencode('.png', bgr)[1]).decode()
hexc = lambda h: [int(h[i:i + 2], 16) for i in (1, 3, 5)]
js = "// Generated by photo_layers.py from the CC BY-SA reference photo (Granada, Wikimedia Commons).\n"
js += f"window.NEY_LAYERS = {{ x0: {X0}, y0: {Y0}, w: {OW}, h: {OH},\n"
js += f"  shade: '{png(hexc('#b8744f'), sh1)}',\n  shade2: '{png(hexc('#9a5a3c'), sh2)}',\n  light: '{png(hexc('#eab088'), hi * 0.85)}',\n  beard: '{png(hexc('#3d2416'), beard)}',\n  hair: '{HAIRPNG}' }};\n"
open(outjs, 'w').write(js)
cv2.imwrite('/tmp/claude-0/-home-user-obstacle-game/e66590ac-2a10-5a33-8fcb-c33592167d49/scratchpad/layers_dbg.jpg', np.hstack([(sh1 * 255), (sh2 * 255), (hi * 255), (beard * 255)]).astype(np.uint8))
print('ok', len(js) // 1024, 'KB')
