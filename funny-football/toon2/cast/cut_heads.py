"""cut_heads.py — cut a caricature head sheet (any grid of heads on white) into cast/<name>/caric/<expr>.png
    python3 cast/cut_heads.py cast/<name>/caric_sheet.png smug,shock,angry,laugh,deadpan,cry   (names in reading order)"""
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage

def cut(src, names):
    im = np.array(Image.open(src).convert('RGB')); out = os.path.join(os.path.dirname(src), 'caric'); os.makedirs(out, exist_ok=True)
    white = im.min(axis=2) > 232; lab, _ = ndimage.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fg = ndimage.binary_erosion(~np.isin(lab, list(border)), iterations=1)
    blobs, n = ndimage.label(ndimage.binary_dilation(fg, iterations=2)); sl = ndimage.find_objects(blobs)
    big = sorted(range(n), key=lambda i: -(blobs[sl[i]] == i + 1).sum())[:len(names)]
    cy = np.array([(sl[i][0].start + sl[i][0].stop) / 2 for i in big]); mid = (cy.min() + cy.max()) / 2
    big.sort(key=lambda i: ((sl[i][0].start + sl[i][0].stop) / 2 > mid, sl[i][1].start))   # rows, then left→right
    for name, i in zip(names, big):
        s = sl[i]; a = ((blobs[s] == i + 1) & fg[s]).astype(np.uint8) * 255
        rgba = np.dstack([im[s], a]); ys, xs = np.where(a > 0); rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        Image.fromarray(rgba).save(os.path.join(out, name + '.png')); print(name, rgba.shape[1], 'x', rgba.shape[0])

if __name__ == '__main__': cut(sys.argv[1], sys.argv[2].split(','))
