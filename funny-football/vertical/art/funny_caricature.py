"""Strong, funny caricature from the CC BY-SA reference photo: heavy feature warps (likeness comes from
the real face), repainted as a flat cartoon (soft cel tones, rosy cheeks/nose, brown ink, thick outline),
plus drawn comic expressions. Usage: python3 funny_caricature.py <reference.jpg> <out_dir>
"""
import sys, os, numpy as np, cv2
ref, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
img = cv2.imread(ref)[120:1800, 400:1600]; H, W = img.shape[:2]
G = lambda p: (np.array(p, np.float32) * 2).astype(np.int32)
HEAD = G([(300,40),(360,45),(420,70),(470,100),(520,150),(555,200),(575,260),(580,320),(560,380),(540,410),(520,415),(555,430),(562,480),(556,540),(540,570),(510,582),(495,620),(480,680),(450,730),(400,770),(330,795),(290,802),(240,792),(190,762),(150,702),(120,622),(110,582),(90,586),(70,560),(55,500),(55,450),(70,430),(50,420),(30,380),(20,330),(30,270),(50,220),(90,150),(140,100),(200,60),(250,45)])
mask = np.zeros((H, W), np.uint8); cv2.fillPoly(mask, [HEAD], 255)
PT, PB, PX = 120, 520, 200; OH, OW = H + PT + PB, W + 2 * PX
yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
def build(p):
    sx, sy = xx - PX, yy - PT
    def bulge(cx, cy, r, s):
        nonlocal sx, sy
        dx, dy = sx - cx, sy - cy; d2 = (dx * dx + dy * dy) / (r * r); f = np.where(d2 < 1, 1 - s * (1 - d2) ** 2, 1.0); sx, sy = cx + dx * f, cy + dy * f
    # long chin + narrow jaw
    k2 = np.clip((sy - 1100) / 700, 0, 1); sy = sy - (sy - 1100) * p['chin'] * k2; sx = sx + (sx - 585) * p['jaw'] * k2
    # smaller cranium squeeze above brows
    k = np.clip((800 - sy) / 760, 0, 1); sx = sx + (sx - 600) * p['skull'] * k
    bulge(582, 1035, 260, p['nose']); bulge(582, 1255, 270, p['lips'])
    bulge(415, 884, 150, p['eyes']); bulge(762, 870, 150, p['eyes'])
    bulge(170, 1000, 170, p['ears']); bulge(1090, 980, 170, p['ears'])
    return sx, sy
def fwd(sx, sy, x, y):
    d = (sx - x) ** 2 + (sy - y) ** 2; i = int(np.argmin(d)); return i % OW, i // OW

def paint(P, m):
    sm = P.copy()
    for _ in range(4): sm = cv2.bilateralFilter(sm, 9, 28, 7)
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0]; Lq = np.round(L / 26) * 26; Lq = cv2.GaussianBlur(Lq, (0, 0), 1.6)
    lab[..., 0] = 0.35 * L + 0.65 * Lq + 6
    lab[..., 1] = 128 + (lab[..., 1] - 128) * 1.35 + 3; lab[..., 2] = 128 + (lab[..., 2] - 128) * 1.25
    col = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
    g = cv2.cvtColor(P, cv2.COLOR_BGR2GRAY).astype(np.float32)
    d = cv2.GaussianBlur(g, (0, 0), 1.8) - 0.98 * cv2.GaussianBlur(g, (0, 0), 3.0)
    ink = np.clip((-d - 1.8) / 4, 0, 1); ink = cv2.GaussianBlur(ink, (0, 0), 0.9)
    col = col * (1 - 0.8 * ink[..., None]) + np.array([16, 29, 59], np.float32) * 0.8 * ink[..., None]
    return col

def ellipse(c, ax, col, a=1.0, img=None):
    layer = np.zeros(img.shape[:2], np.float32); cv2.ellipse(layer, c, ax, 0, 0, 360, 1.0, -1, cv2.LINE_AA); layer = cv2.GaussianBlur(layer, (0, 0), ax[0] * 0.35) * a
    return img * (1 - layer[..., None]) + np.array(col, np.float32) * layer[..., None]

def render(name, p, face):
    sx, sy = build(p)
    P = cv2.remap(img, sx, sy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    m = cv2.remap(mask, sx, sy, cv2.INTER_LINEAR, borderValue=0); m = (cv2.GaussianBlur(m, (0, 0), 6) > 127).astype(np.uint8)
    col = paint(P, m)
    eL, eR, mo, no = fwd(sx, sy, 415, 884), fwd(sx, sy, 762, 870), fwd(sx, sy, 582, 1250), fwd(sx, sy, 582, 1050)
    # rosy cheeks + nose (style of the reference)
    for c in (fwd(sx, sy, 330, 1010), fwd(sx, sy, 850, 1000)): col = ellipse(c, (110, 60), (90, 90, 235), 0.35, col)
    col = ellipse(no, (85, 60), (100, 110, 240), 0.3, col)
    INK = (16, 29, 59)
    if face in ('cry', 'grin'):
        skin = cv2.mean(col[eL[1] + 90:eL[1] + 160, eL[0]:eR[0]].astype(np.float32))[:3]
        if face == 'cry':
            for (c, dd) in ((eL, 1), (eR, -1)):          # squeezed > < eyes
                col = ellipse(c, (95, 46), skin, 1.0, col)
                cv2.polylines(col, [np.array([[c[0] - dd * 60, c[1] - 30], [c[0] + dd * 30, c[1] + 4], [c[0] - dd * 60, c[1] + 38]], np.int32)], False, INK, 16, cv2.LINE_AA)
            # giant wailing mouth
            mx, my = mo; my -= 30; w, h = 170, 175
            cv2.ellipse(col, (mx, my + 50), (w, h), 0, 0, 360, (28, 22, 110), -1, cv2.LINE_AA)
            cv2.rectangle(col, (mx - 120, my - 110), (mx + 120, my - 70), (250, 252, 255), -1)
            cv2.ellipse(col, (mx, my + 50 + h - 60), (100, 55), 0, 0, 360, (110, 100, 235), -1, cv2.LINE_AA)
            cv2.ellipse(col, (mx, my + 50), (w, h), 0, 0, 360, INK, 12, cv2.LINE_AA)
            # fountain tears
            for (c, dd) in ((eL, -1), (eR, 1)):
                for i in range(12):
                    k = i / 12; tx, ty = int(c[0] + dd * (60 + k * 520)), int(c[1] - k * 280 + k * k * 900)
                    cv2.ellipse(col, (tx, ty), (20, 28), 0, 0, 360, (255, 215, 130), -1, cv2.LINE_AA); cv2.ellipse(col, (tx, ty), (20, 28), 0, 0, 360, (176, 111, 31), 5, cv2.LINE_AA)
                    cv2.ellipse(m, (tx, ty), (24, 32), 0, 0, 360, 1, -1)
        else:  # huge toothy grin
            mx, my = mo; w = 230
            my -= 40; pts = np.array([[mx - w, my - 50], [mx - w // 2, my - 15], [mx, my - 5], [mx + w // 2, my - 15], [mx + w, my - 50], [mx + int(w * 0.7), my + 110], [mx, my + 170], [mx - int(w * 0.7), my + 110]], np.int32)
            cv2.fillPoly(col, [pts], (30, 25, 110), cv2.LINE_AA)
            mk = np.zeros(col.shape[:2], np.uint8); cv2.fillPoly(mk, [pts], 1)
            teeth = np.zeros_like(mk); cv2.rectangle(teeth, (mx - w, my - 80), (mx + w, my + 70), 1, -1); teeth &= mk
            col[teeth > 0] = (246, 250, 255)
            for i in range(-4, 5): cv2.line(col, (mx + i * 52, my - 10), (mx + i * 50, my + 68 - abs(i) * 8), (150, 160, 180), 4, cv2.LINE_AA)
            cv2.polylines(col, [pts], True, INK, 12, cv2.LINE_AA)
    alpha = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)
    ol = cv2.GaussianBlur(cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))).astype(np.float32), (0, 0), 1.2)
    rgb = col * alpha[..., None] + np.array(INK, np.float32) * (1 - alpha[..., None])
    rgba = np.dstack([rgb, np.maximum(alpha, ol) * 255]).clip(0, 255).astype(np.uint8)
    ys, xs = np.where(rgba[..., 3] > 3); rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    rgba = cv2.resize(rgba, (rgba.shape[1] // 2, rgba.shape[0] // 2), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'{out}/{name}.png', rgba); return rgba

STRONG = dict(chin=0.22, jaw=0.14, skull=0.06, nose=0.42, lips=0.30, eyes=-0.12, ears=0.28)
for face in ('neutral', 'grin', 'cry'): render(f'ney_{face}', STRONG, face)
print('ok')
