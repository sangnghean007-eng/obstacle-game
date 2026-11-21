"""cut_sheet.py — cut an AI turnaround sheet (3 full bodies left, 3x2 expression busts right) into transparent PNGs.
    python3 cast/cut_sheet.py cast/<name>/sheet.png
Figures are found automatically (connected non-white blobs), so layouts that shift a little still cut cleanly.
White background is removed by flood fill from the border only, so white eyes/teeth stay opaque."""
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage

BODIES = ['front', 'threequarter', 'side']; HEADS = ['smug', 'shock', 'angry', 'laugh', 'deadpan', 'cry']

def cut(src, out=None):
    im = np.array(Image.open(src).convert('RGB')); out = out or os.path.dirname(src); os.makedirs(out, exist_ok=True)
    white = im.min(axis=2) > 232
    lab, _ = ndimage.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fg = ~np.isin(lab, list(border))
    # NOTE: a white kit with no outline at the bottom of a bust (Mbappé's busts) fades into the background and cannot be
    # cut; puppet.js clips busts at the neck and draws the collar/shoulders instead (PUPPET.bust kit option).
    # enclosed holes (gap between arm and torso, between legs) are background too: the AI background is neutral
    # white (~251, B >= R) while white kit fabric is warmer (~246, R > B), so only true holes are removed.
    imf = im.astype(float)
    for i, s in enumerate(ndimage.find_objects(lab)):
        if i + 1 in border or s is None: continue
        m = lab[s] == i + 1
        if m.sum() < 250: continue
        px = imf[s][m]; mu = px.mean(0)
        if mu.mean() >= 248.5 and mu[2] >= mu[0] - 0.5: fg[s][m] = False
    fg = ndimage.binary_erosion(fg, iterations=1)                       # trim the white halo
    blobs, n = ndimage.label(ndimage.binary_dilation(fg, iterations=int(os.environ.get("DIL", 2))))  # join hair curls / loose bits
    sl = ndimage.find_objects(blobs)
    figs = sorted([(int((blobs == i + 1).sum()), s) for i, s in enumerate(sl)], key=lambda t: -t[0])
    tall = [s for _, s in figs if s[0].stop - s[0].start > im.shape[0] * 0.6]
    figs = [s for _, s in figs[:9 if tall else 6]]      # head-only sheets (caricature busts) have 6 figures and no bodies
    bodies = sorted([s for s in figs if s[0].stop - s[0].start > im.shape[0] * 0.6], key=lambda s: s[1].start)
    heads = [s for s in figs if s not in bodies]
    mid = np.median([(s[0].start + s[0].stop) / 2 for s in heads])
    heads = sorted(heads, key=lambda s: ((s[0].start + s[0].stop) / 2 > mid, s[1].start))
    assert len(bodies) in (0, 3) and len(heads) == 6, (len(bodies), len(heads))
    for name, s in list(zip(BODIES, bodies)) + list(zip(HEADS, heads)):
        lbl = np.bincount(blobs[s].ravel())[1:].argmax() + 1                # the blob that owns this box
        a = ((blobs[s] == lbl) & fg[s]).astype(np.uint8) * 255
        rgba = np.dstack([im[s], a]); ys, xs = np.where(a > 0)
        rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        Image.fromarray(rgba).save(os.path.join(out, name + '.png')); print(name, rgba.shape[1], 'x', rgba.shape[0])

if __name__ == '__main__': cut(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
