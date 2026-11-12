"""Trace flat-colour regions of the CC BY-SA reference photo into smooth vector outlines (grid space 600x840),
exported as point lists for neymar_vector.js (hair silhouette, hair clumps, blond streaks, beard, face shadow, brows).
Usage: python3 trace_vectors.py <reference.jpg> <out.js>
"""
import sys, json, numpy as np, cv2
ref, outjs = sys.argv[1], sys.argv[2]
S = 2  # trace at 2x grid for smoother curves
ph = cv2.resize(cv2.imread(ref)[120:1800, 400:1600], (600 * S, 840 * S), interpolation=cv2.INTER_AREA)
lab = cv2.cvtColor(ph, cv2.COLOR_BGR2LAB).astype(np.float32); L, A, B = lab[..., 0], lab[..., 1] - 128, lab[..., 2] - 128
def poly(pts):
    m = np.zeros(L.shape, np.uint8); cv2.fillPoly(m, [(np.array(pts) * S).astype(np.int32)], 255); return m
FACE = [(95,330),(100,400),(100,470),(100,560),(110,622),(130,682),(165,732),(215,772),(270,796),(300,799),(345,791),(400,766),(440,726),(470,670),(478,600),(482,520),(485,450),(480,380),(470,300),(400,250),(290,232),(180,250),(110,300)]
HAIRZ = [(60,445),(100,415),(118,360),(140,318),(180,290),(235,268),(300,258),(370,262),(430,278),(478,300),(505,345),(515,380),(525,425),(560,430),(620,300),(600,0),(0,0),(0,300),(30,445)]
BEARDZ = [(103,470),(100,560),(110,622),(130,682),(165,732),(215,772),(270,796),(300,799),(345,791),(400,766),(440,726),(470,670),(478,600),(481,520),(479,470),(455,540),(420,580),(385,590),(290,575),(200,590),(160,580),(125,540)]
face, hz, bz = poly(FACE), poly(HAIRZ), poly(BEARDZ)
def smooth(m, blur):
    return ((cv2.GaussianBlur(m.astype(np.float32), (0, 0), blur * S) > 0.5) * 255).astype(np.uint8)
def contours(m, min_area, eps=1.6):
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    res = []
    for i, c in enumerate(cs):
        if cv2.contourArea(c) < min_area * S * S: continue
        c = cv2.approxPolyDP(c, eps * S, True)[:, 0, :] / S
        hole = hier is not None and hier[0][i][3] >= 0
        res.append({'hole': bool(hole), 'pts': [[round(float(x), 1), round(float(y), 1)] for x, y in c]})
    return res
# hair silhouette (dark or blond pixels inside the hair zone), largest blob, holes filled
blond = (B - A > 6) & (B > 14) & (L < 80)
hm = (((L < 52) | blond) & (hz > 0)).astype(np.uint8) * 255
hm = cv2.morphologyEx(hm, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21 * S, 21 * S)))
n, lbl, st, _ = cv2.connectedComponentsWithStats(hm); hm = ((lbl == 1 + np.argmax(st[1:, 4])) * 255).astype(np.uint8)
ff = hm.copy(); cv2.floodFill(ff, np.zeros((ff.shape[0] + 2, ff.shape[1] + 2), np.uint8), (0, 0), 255); hm = hm | cv2.bitwise_not(ff)
hair = smooth(hm, 2.5)
Lb = cv2.GaussianBlur(L, (0, 0), 2.5 * S)
clump = smooth((Lb > 30) & (hair > 0), 2.0)
bl = smooth((cv2.GaussianBlur(blond.astype(np.float32), (0, 0), 3 * S) > 0.3) & (hair > 0), 1.6)
# beard: traced zone, chin denser
Lbig = cv2.GaussianBlur(L, (0, 0), 30 * S); dens = cv2.GaussianBlur(np.clip((Lbig - L) / 30 + 0.15, 0, 1), (0, 0), 14 * S)
beard = smooth(bz > 0, 6)
chin = smooth((bz > 0) & (dens > 0.27), 8)
# face shadow (one cel tone) + brows
Ls = cv2.GaussianBlur(cv2.bilateralFilter(L, 0, 22, 10), (0, 0), 12 * S)
shade = smooth((Ls < np.percentile(Ls[face > 0], 32)) & (face > 0), 4)
light = smooth((Ls > np.percentile(Ls[face > 0], 86)) & (face > 0), 5)
BROWZ = np.zeros(L.shape, np.uint8)
for c, ax in [((206, 411), (68, 22)), ((389, 403), (75, 22))]: cv2.ellipse(BROWZ, (c[0] * S, c[1] * S), (ax[0] * S, ax[1] * S), 0, 0, 360, 255, -1)
brows = smooth(((Lbig - cv2.GaussianBlur(L, (0, 0), 2 * S)) > 14) & (BROWZ > 0), 1.5)
V = {'hair': contours(hair, 2000), 'clump': contours(clump, 25, 1.2), 'blond': contours(bl, 20, 1.2), 'beard': contours(beard, 500),
     'chin': contours(chin, 300), 'shade': contours(shade, 150), 'light': contours(light, 150), 'brows': contours(brows, 150, 1.0)}
open(outjs, 'w').write('// Vector outlines traced by trace_vectors.py from the CC BY-SA reference photo (Granada, Wikimedia Commons).\nwindow.NEY_VEC = ' + json.dumps(V, separators=(',', ':')) + ';\n')
print({k: (len(v), sum(len(c['pts']) for c in v)) for k, v in V.items()})
