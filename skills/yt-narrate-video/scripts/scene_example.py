"""Example scene. Copy, rename, edit shapes. Run: python3 scene_example.py out.jpg"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from watercolor import *

W, H = 1600, 900
p = Painting(W, H, seed=11)

# sky: blue to warm dusk, two glazes
full = np.ones((H, W), np.float32)
p.wash(full, '#7aa3c4', 0.55, wobble=0, soft=0, edge=0, gran=0.25, gradient=p.flat_grad(1.0, 0.0, 0, 560))
p.wash(full, '#f0b65e', 0.55, wobble=0, soft=0, edge=0, gran=0.2, gradient=p.flat_grad(0.0, 1.0, 180, 620))
p.wash(full, '#e58a6b', 0.25, wobble=0, soft=0, edge=0, gran=0.2, gradient=p.flat_grad(0.0, 1.0, 380, 600))

# clouds: soft lifted-looking strokes (darker undersides)
img, d = p.mask()
for (cx, cy, rx, ry) in [(260, 170, 230, 40), (520, 120, 160, 28), (1150, 200, 280, 46), (1390, 120, 150, 24), (850, 290, 210, 30)]:
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    d.ellipse([cx - rx * .6, cy - ry * 1.6, cx + rx * .4, cy + ry * .3], fill=255)
p.wash(img, '#8a7fa0', 0.35, wobble=14, soft=6, edge=0.6, gran=0.5, bloom=0.4)

# distant tree line
img, d = p.mask()
pts = [(0, 600)]
x = 0
while x < W:
    x += p.rng.uniform(18, 50)
    pts.append((x, 600 - p.rng.uniform(8, 40)))
pts += [(W, 640), (0, 640)]
d.polygon(pts, fill=255)
p.wash(img, '#55607a', 0.75, wobble=4, soft=1.5, edge=0.7, gran=0.5)

# fields
img, d = p.mask(); d.rectangle([0, 615, W, H], fill=255)
p.wash(img, '#b7a35a', 0.7, wobble=3, soft=2, edge=0.3, gran=0.55)
img, d = p.mask(); d.polygon([(0, 700), (W, 650), (W, H), (0, H)], fill=255)
p.wash(img, '#6f7a3a', 0.45, wobble=6, soft=4, edge=0.5, gran=0.6, bloom=0.3)

# road: vanishing point
vp = (820, 612)
img, d = p.mask(); d.polygon([(vp[0] - 6, vp[1]), (vp[0] + 6, vp[1]), (1250, H), (380, H)], fill=255)
p.wash(img, '#4b4a4f', 0.75, wobble=2, soft=1.2, edge=0.6, gran=0.65)
# center dashes
for i in range(9):
    t0 = (i / 9) ** 1.8; t1 = ((i + 0.45) / 9) ** 1.8
    y0 = vp[1] + (H - vp[1]) * t0; y1 = vp[1] + (H - vp[1]) * t1
    wd0 = 1 + 9 * t0; wd1 = 1 + 9 * t1
    img, d = p.mask(); d.polygon([(vp[0] - wd0, y0), (vp[0] + wd0, y0), (vp[0] + wd1, y1), (vp[0] - wd1, y1)], fill=255)
    p.wash(img, '#e8c85a', 0.9, wobble=1, soft=0.8, edge=0.3, gran=0.3)

# wire + hanging signal
p.pencil(lambda d, w: d.line([(-20, 250), (400, 290), (820, 305), (1240, 290), (1620, 248)], fill=255, width=w), width=3, alpha=0.7)
p.pencil(lambda d, w: d.line([(820, 305), (820, 330)], fill=255, width=w), width=3, alpha=0.7)
img, d = p.mask(); d.rounded_rectangle([780, 330, 860, 560], 14, fill=255)
p.wash(img, '#2d2f33', 0.85, wobble=2, soft=1, edge=0.6, gran=0.4)
# lenses
for i, col in enumerate(['#5a2a26', '#5e4a20', '#3fd58a']):
    cy = 375 + i * 68
    img, d = p.mask(); d.ellipse([796, cy - 26, 844, cy + 26], fill=255)
    p.wash(img, col, 0.9 if i == 2 else 0.6, wobble=1, soft=1, edge=0.4, gran=0.2)
# green glow
img, d = p.mask(); d.ellipse([700, 400, 940, 620], fill=255)
glow = cv2.GaussianBlur(np.asarray(img, np.float32) / 255, (0, 0), 40)
p.canvas = p.canvas * (1 - 0.0) + glow[..., None] * np.array([0.05, 0.22, 0.12], np.float32) * 0.9
p.canvas = np.clip(p.canvas, 0, 1)

# fence posts on left
for i in range(10):
    t = i / 10
    x = 330 - 330 * t ** 1.2 + 40
    y = 640 + 230 * t ** 1.3
    hh = 18 + 70 * t
    p.pencil(lambda d, w, x=x, y=y, hh=hh: d.line([(x, y), (x, y - hh)], fill=255, width=w), width=int(2 + 4 * t), alpha=0.6)
p.pencil(lambda d, w: d.line([(370, 625), (0, 820)], fill=255, width=w), width=2, alpha=0.4)

p.splatter('#6b5a3a', n=50, region=(0, 700, W, H), alpha=0.4)
p.save(sys.argv[1] if len(sys.argv) > 1 else 'hero.jpg')
print('ok')
