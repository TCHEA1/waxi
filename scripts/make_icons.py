# Génère l'icône Waxi (motifs wax sur fond indigo) et l'écran de démarrage
from PIL import Image, ImageDraw
import math, os, sys

BG = (18, 21, 58)
SLOT = (38, 43, 99)
S = 1024

def block(size, kind):
    im = Image.new('RGB', (size, size))
    d = ImageDraw.Draw(im)
    c = size / 2
    if kind == 0:  # cercles concentriques rouge/jaune
        d.rectangle([0, 0, size, size], fill=(216, 52, 44))
        for r, col in [(0.62, (255, 201, 60)), (0.48, (216, 52, 44)), (0.34, (255, 201, 60)), (0.18, (216, 52, 44))]:
            d.ellipse([c - r * size / 2 * 1.4, c - r * size / 2 * 1.4, c + r * size / 2 * 1.4, c + r * size / 2 * 1.4], fill=col)
    elif kind == 1:  # rayures vert/crème
        d.rectangle([0, 0, size, size], fill=(31, 157, 85))
        step = size / 4
        for k in range(-8, 12):
            x = k * step
            d.polygon([(x, 0), (x + step * 0.3, 0), (x + step * 0.3 + size, size), (x + size, size)], fill=(251, 244, 230))
            d.polygon([(x + step * 0.6, 0), (x + step * 0.72, 0), (x + step * 0.72 + size, size), (x + step * 0.6 + size, size)], fill=(255, 201, 60))
    elif kind == 2:  # pois blancs sur bleu
        d.rectangle([0, 0, size, size], fill=(47, 95, 208))
        for i in range(2):
            for j in range(2):
                cx, cy = (i + .5) * size / 2, (j + .5) * size / 2
                r = size * 0.11
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(251, 244, 230))
    elif kind == 3:  # losange orange/jaune
        d.rectangle([0, 0, size, size], fill=(255, 122, 26))
        d.polygon([(c, 0), (size, c), (c, size), (0, c)], fill=(255, 201, 60))
        d.polygon([(c, size * .28), (size * .72, c), (c, size * .72), (size * .28, c)], fill=(255, 122, 26))
    elif kind == 4:  # violet, feuille crème
        d.rectangle([0, 0, size, size], fill=(138, 47, 158))
        d.ellipse([c - size * .15, c - size * .3, c + size * .15, c + size * .3], fill=(251, 244, 230))
        d.ellipse([-size * .3, -size * .3, size * .3, size * .3], fill=(224, 90, 182))
    else:  # carrés emboîtés sarcelle
        d.rectangle([0, 0, size, size], fill=(15, 138, 138))
        d.rectangle([size * .15, size * .15, size * .85, size * .85], fill=(251, 244, 230))
        d.rectangle([size * .27, size * .27, size * .73, size * .73], fill=(15, 138, 138))
    return im

def rounded(im, rad):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], rad, fill=255)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    return out

# grille 3x3 : None = case vide
LAYOUT = [[0, 1, None], [2, 3, 0], [None, 4, 5]]

def art(total, grid_frac, transparent=False):
    im = Image.new('RGBA', (total, total), (0, 0, 0, 0) if transparent else BG + (255,))
    g = total * grid_frac
    gap = g * 0.05
    cell = (g - 2 * gap) / 3
    ox = (total - g) / 2
    for r in range(3):
        for c in range(3):
            x, y = ox + c * (cell + gap), ox + r * (cell + gap)
            k = LAYOUT[r][c]
            if k is None:
                tile = Image.new('RGB', (int(cell), int(cell)), SLOT)
            else:
                tile = block(int(cell), k)
            im.alpha_composite(rounded(tile, int(cell * .16)), (int(x), int(y)))
    return im

res = sys.argv[1]
full = art(S, 0.78)
# icône carrée classique + ronde
for folder, px in [('mdpi', 48), ('hdpi', 72), ('xhdpi', 96), ('xxhdpi', 144), ('xxxhdpi', 192)]:
    sq = rounded(full.convert('RGB'), int(S * .18)).resize((px, px), Image.LANCZOS)
    sq.save(os.path.join(res, f'mipmap-{folder}', 'ic_launcher.png'))
    m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).ellipse([0, 0, S - 1, S - 1], fill=255)
    rd = Image.new('RGBA', (S, S), (0, 0, 0, 0)); rd.paste(art(S, 0.62).convert('RGB'), (0, 0), m)
    rd.resize((px, px), Image.LANCZOS).save(os.path.join(res, f'mipmap-{folder}', 'ic_launcher_round.png'))
# icône adaptative (premier plan transparent, zone sûre ~ 61 %)
fg = art(S, 0.56, transparent=True)
for folder, px in [('mdpi', 108), ('hdpi', 162), ('xhdpi', 216), ('xxhdpi', 324), ('xxxhdpi', 432)]:
    fg.resize((px, px), Image.LANCZOS).save(os.path.join(res, f'mipmap-{folder}', 'ic_launcher_foreground.png'))
# écran de démarrage : fond indigo + grille au centre
for d in os.listdir(res):
    if d.startswith('drawable'):
        p = os.path.join(res, d, 'splash.png')
        if os.path.exists(p):
            w, h = Image.open(p).size
            sp = Image.new('RGB', (w, h), BG)
            s = int(min(w, h) * 0.42)
            sp.paste(art(s, 1.0, transparent=True), ((w - s) // 2, (h - s) // 2), art(s, 1.0, transparent=True))
            sp.save(p)
# icône Play Store 512
out = sys.argv[2] if len(sys.argv) > 2 else None
if out:
    full.convert('RGB').resize((512, 512), Image.LANCZOS).save(out)
print('ok')
