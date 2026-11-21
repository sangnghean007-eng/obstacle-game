"""make_puppet.py — turn an AI full-body cut (cast/<name>/<view>.png) into a cut-out puppet:
torso, head, armL, armR, legL, legR PNGs + rig.json (pivots in body-image pixels, bust metrics for expression swaps).
    python3 cast/make_puppet.py            # builds every character in RIGS
Arm cuts are hand-placed polygons (AI arms touch the torso, so they cannot be found automatically); verify with the
contact sheet this script writes to cast/<name>/puppet_check.png (pivots red, cut lines yellow).
L / R = screen-left / screen-right."""
import json, os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
RIGS = {
    'mbappe': dict(view='threequarter', headY=150, neck=(120, 150), legY=420, legSplit=110, armSkinBelow=250,
                   armL=[(0, 135), (60, 140), (68, 255), (60, 300), (58, 330), (64, 400), (68, 452), (0, 452)], shL=(42, 172), hem=258,
                   armR=[(166, 160), (195, 168), (223, 300), (223, 452), (180, 452), (178, 330), (172, 255), (165, 205)], shR=(178, 186),
                   hipL=(70, 432), hipR=(145, 432)),
    'yamal': dict(view='front', headY=160, neck=(110, 160), legY=430, legSplit=110,
                  armL=[(0, 158), (50, 158), (60, 192), (52, 266), (40, 278), (42, 452), (0, 452)], shL=(46, 190), hem=266,
                  armR=[(167, 158), (217, 158), (217, 452), (175, 452), (177, 278), (165, 266), (157, 192)], shR=(172, 190),
                  hipL=(70, 440), hipR=(150, 440)),
    'messi': dict(view='front', headY=215, neck=(101, 215), legY=462, legSplit=101,
                  armL=[(0, 225), (40, 225), (50, 280), (46, 330), (42, 462), (0, 462)], shL=(40, 252), hem=330,
                  armR=[(162, 225), (202, 225), (202, 462), (160, 462), (156, 330), (152, 280)], shR=(162, 252),
                  hipL=(65, 472), hipR=(138, 472)),
    'ronaldo': dict(view='front', headY=148, neck=(120, 148), legY=430, legSplit=117,
                    armL=[(0, 148), (56, 148), (66, 200), (58, 258), (48, 266), (45, 425), (0, 425)], shL=(48, 180), hem=258,
                    armR=[(177, 148), (233, 148), (233, 425), (195, 425), (193, 266), (180, 258), (171, 200)], shR=(186, 180),
                    hipL=(70, 445), hipR=(165, 445)),
}
EXPR = ['smug', 'shock', 'angry', 'laugh', 'deadpan', 'cry']

def poly_mask(shape, pts):
    m = Image.new('L', (shape[1], shape[0]), 0); ImageDraw.Draw(m).polygon(pts, fill=255); return np.array(m) > 0

def bbox(a):
    ys, xs = np.where(a); return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]

def head_metrics(alpha, top_frac):
    """width and centre of the head (widest row in the top part = ears level) and the hair-top row"""
    ys, xs = np.where(alpha); y0, y1 = ys.min(), ys.max(); lim = int(y0 + (y1 - y0) * top_frac)
    best = (0, 0, 0)
    for y in range(y0, lim):
        r = np.where(alpha[y])[0]
        if len(r) and r.max() - r.min() > best[0]: best = (int(r.max() - r.min()), int((r.max() + r.min()) / 2), y)
    return dict(w=best[0], cx=best[1], top=int(y0), earY=best[2])

def build(name, R):
    d = os.path.join(HERE, name); im = np.array(Image.open(os.path.join(d, R['view'] + '.png')).convert('RGBA'))
    A = im[:, :, 3] > 0; h, w = A.shape; Y = np.arange(h)[:, None]; X = np.arange(w)[None, :]
    armL = A & poly_mask(A.shape, R['armL']); armR = A & poly_mask(A.shape, R['armR'])
    # where the hands touch the shorts, keep only skin (warm: R well above B) and ink (dark) — kit slivers stay on the torso
    rgb = im[:, :, :3].astype(int); skin = rgb[:, :, 0] > rgb[:, :, 2] + 22
    skin_or_ink = skin | ((rgb.max(axis=2) < 60) & ndimage.binary_dilation(skin, iterations=3))  # ink only where it outlines skin
    kit = ~skin_or_ink & (Y >= R.get('armSkinBelow', 395))
    armL &= ~kit; armR &= ~kit
    def main_blob(m):  # an arm is one piece: stray kit slivers caught by the polygon go back to the torso
        lab, n = ndimage.label(m)
        if n <= 1: return m
        return lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
    armL, armR = main_blob(armL), main_blob(armR)
    rest = A & ~armL & ~armR
    hx = np.where((rest & (Y < R['headY'] - 12)).any(0))[0]   # head columns = ear to ear (shoulders excluded)
    head = rest & (Y < R['headY'] + 8) & (X >= hx.min()) & (X <= hx.max())  # 8 px overlap into the neck
    legs = rest & (Y >= R['legY'])
    legL = legs & (X < R['legSplit']); legR = legs & (X >= R['legSplit'])
    torso = rest & (Y >= R['headY'] - 4) & ~((Y >= R['legY'] + 30))  # torso keeps the shorts; legs start under the hem
    parts = dict(torso=torso, head=head, armL=armL, armR=armR, legL=legL, legR=legR); rig = dict(view=R['view'], size=[w, h], parts={})
    imgs = {k: im.copy() for k in parts}
    # JOINT REPAIR — arms are cut WITH their sleeves and turn at the top of the shoulder, drawn over the torso.
    # The torso gets the sleeve's area back as a plain shoulder (nearest shirt colour + ink edge), so a raised arm never leaves a hole.
    src = torso & ~skin & (im[:, :, :3].max(axis=2) > 110)                      # copy shirt colour only (not neck skin, not ink)
    dist, (iy, ix) = ndimage.distance_transform_edt(~src, return_indices=True)
    fill = (armL | armR) & (Y < R['hem'] + 6) & (dist <= 9)                      # a rounded shoulder, not the whole sleeve
    t = imgs['torso']; t[fill, :3] = im[iy[fill], ix[fill], :3]; t[fill, 3] = 255
    tor2 = torso | fill; edge = fill & ~ndimage.binary_erosion(tor2, iterations=2); t[edge, :3] = 30
    # armpit side under the sleeve: shirt in deep shadow cut by the polygon looks like a grey scrap when the arm lifts —
    # repaint it with the lit shirt colour and give the new side an ink edge
    pol = poly_mask(A.shape, R['armL']) | poly_mask(A.shape, R['armR'])
    zone = ndimage.binary_dilation(pol, iterations=10) & tor2 & (Y >= R['hem'] - 4) & (Y < R['hem'] + 70) & ~skin
    t[zone, :3] = im[iy[zone], ix[zone], :3]
    side = zone & ~ndimage.binary_erosion(tor2, iterations=3); t[side, :3] = 30
    # thin leftovers of the armpit (shadow/gap scraps) are dropped: keep only the solid body (opening removes 1-6 px slivers)
    solid = ndimage.binary_opening(tor2, iterations=4); lab, n = ndimage.label(solid)
    if n > 1: solid = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
    tor2 = tor2 & ndimage.binary_dilation(solid, iterations=4)
    parts['torso'] = tor2
    for k, m in parts.items():
        b = bbox(m); rgba = imgs[k]; rgba[:, :, 3] = np.where(m, rgba[:, :, 3], 0)
        Image.fromarray(rgba[b[1]:b[3], b[0]:b[2]]).save(os.path.join(d, f'p_{k}.png')); rig['parts'][k] = dict(box=b)
    rig['pivot'] = dict(neck=R['neck'], shL=R['shL'], shR=R['shR'], hipL=R['hipL'], hipR=R['hipR'])
    rig['head'] = head_metrics(head, 0.7)
    rig['busts'] = {}
    for e in EXPR:
        p = os.path.join(d, e + '.png')
        if os.path.exists(p):
            b = np.array(Image.open(p))[:, :, 3] > 0; m = head_metrics(b, 0.55); m['size'] = [b.shape[1], b.shape[0]]
            wid = [np.ptp(np.where(b[y])[0]) if b[y].any() else 999 for y in range(b.shape[0])]
            lo, hi = m["earY"] + 10, int(b.shape[0] * 0.80)
            m['neckY'] = int(lo + np.argmin(wid[lo:hi]))   # narrowest row under the ears = middle of the neck: busts are clipped here
            rig['busts'][e] = m
    json.dump(rig, open(os.path.join(d, 'rig.json'), 'w'), indent=1)
    open(os.path.join(d, 'rig.js'), 'w').write(f'(window.RIGS = window.RIGS || {{}})[{name!r}] = ' + json.dumps(rig) + ';\n')  # file:// pages cannot fetch json
    # check sheet: parts tinted, pivots, cut polygons
    chk = Image.new('RGBA', (w * 3, h), (60, 160, 90, 255)); chk.alpha_composite(Image.fromarray(im), (0, 0))
    tint = {'torso': (255, 255, 255), 'head': (255, 200, 0), 'armL': (255, 0, 0), 'armR': (0, 120, 255), 'legL': (255, 0, 255), 'legR': (0, 255, 255)}
    col = np.zeros((h, w, 4), np.uint8)
    for k, m in parts.items(): col[m] = list(tint[k]) + [255]
    chk.alpha_composite(Image.fromarray(col), (w, 0))
    ex = Image.fromarray(im); dr = ImageDraw.Draw(chk)
    for k in ('armL', 'armR'): dr.line([(x + 2 * w, y) for x, y in R[k]] + [(R[k][0][0] + 2 * w, R[k][0][1])], fill=(255, 255, 0, 255), width=2)
    chk.alpha_composite(ex, (2 * w, 0)); dr = ImageDraw.Draw(chk)
    for k in ('armL', 'armR'): dr.line([(x + 2 * w, y) for x, y in R[k]] + [(R[k][0][0] + 2 * w, R[k][0][1])], fill=(255, 255, 0, 255), width=2)
    for p in rig['pivot'].values(): dr.ellipse([p[0] + 2 * w - 4, p[1] - 4, p[0] + 2 * w + 4, p[1] + 4], fill=(255, 0, 0, 255))
    dr.line([(2 * w, R['headY']), (3 * w, R['headY'])], fill=(255, 0, 255, 255)); dr.line([(2 * w, R['legY']), (3 * w, R['legY'])], fill=(255, 0, 255, 255))
    chk.save(os.path.join(d, 'puppet_check.png')); print(name, 'ok', {k: rig['parts'][k]['box'] for k in parts})

if __name__ == '__main__':
    for n, R in RIGS.items(): build(n, R)
