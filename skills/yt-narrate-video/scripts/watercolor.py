"""Tiny watercolor engine.
Shapes are drawn as masks with PIL, then OpenCV does the physics-ish part:
noise warping (hand-drawn edges), wet-edge pigment pooling, granulation,
glazing (subtractive multiply), backruns (blooms) and cold-press paper.
"""
import numpy as np, cv2
from PIL import Image, ImageDraw

RNG = np.random.default_rng(7)


def hexrgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


def smooth_noise(h, w, scale, rng=RNG):
    sh, sw = max(2, int(h / scale)), max(2, int(w / scale))
    n = rng.random((sh, sw)).astype(np.float32)
    n = cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def fbm(h, w, scales=(160, 60, 20, 6), weights=(0.5, 0.25, 0.15, 0.1), rng=RNG):
    out = np.zeros((h, w), np.float32)
    for s, wt in zip(scales, weights):
        out += wt * smooth_noise(h, w, s, rng)
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


class Painting:
    def __init__(self, w, h, paper='#fbfaf6', seed=7):
        self.w, self.h = w, h
        self.rng = np.random.default_rng(seed)
        self.canvas = np.ones((h, w, 3), np.float32) * hexrgb(paper)
        # paper texture: cold-press tooth used for granulation and final emboss
        tooth = fbm(h, w, (40, 9, 3, 1.5), (0.2, 0.35, 0.3, 0.15), self.rng)
        self.tooth = tooth

    # ---------- mask helpers ----------
    def mask(self):
        img = Image.new('L', (self.w, self.h), 0)
        return img, ImageDraw.Draw(img)

    def warp(self, m, amp=6, scale=40):
        h, w = m.shape
        dx = (smooth_noise(h, w, scale, self.rng) - 0.5) * 2 * amp
        dy = (smooth_noise(h, w, scale, self.rng) - 0.5) * 2 * amp
        gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
        return cv2.remap(m, gx + dx, gy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    # ---------- the wash ----------
    def wash(self, mask, color, alpha=0.6, wobble=5, soft=2.5, edge=0.55,
             gran=0.35, bloom=0.0, gradient=None, wet=1.0, color2=None, mix=0.5):
        """mask: PIL L image or float array 0..1. color hex. gradient: array 0..1 multiplier."""
        m = np.asarray(mask, np.float32) / (255.0 if not isinstance(mask, np.ndarray) else 1.0)
        if wobble:
            m = self.warp(m, wobble, 30 + wobble * 6)
            m = self.warp(m, wobble * 0.4, 8)
        if soft:
            k = int(soft * 2) * 2 + 1
            m = cv2.GaussianBlur(m, (k, k), soft)
        m = np.clip(m, 0, 1)
        # wet edge: pigment migrates to the border of a drying puddle
        big = cv2.GaussianBlur(m, (0, 0), 6 * wet + 1)
        rim = np.clip(m - big, 0, 1) * 2.2
        dens = m * (0.62 + 0.38 * fbm(self.h, self.w, (90, 30, 10), (0.5, 0.3, 0.2), self.rng)) + edge * rim
        # granulation: pigment settles into paper valleys
        dens *= (1 - gran) + gran * (1.4 * (1 - self.tooth))
        if bloom:
            # backrun / cauliflower bloom: lighter blotch with dark fringe
            b = smooth_noise(self.h, self.w, 70, self.rng)
            b = (b > 0.72).astype(np.float32)
            b = cv2.GaussianBlur(self.warp(b, 10, 14), (0, 0), 3)
            fringe = np.clip(b - cv2.GaussianBlur(b, (0, 0), 4), 0, 1)
            dens = dens * (1 - bloom * b * 0.6) + bloom * fringe * m * 1.5
        if gradient is not None:
            dens *= gradient
        a = np.clip(dens * alpha, 0, 1)[..., None]
        c = hexrgb(color)
        if color2 is not None:
            # wet-in-wet: a second pigment dropped into the puddle
            t = np.clip((fbm(self.h, self.w, (120, 40, 12), (0.55, 0.3, 0.15), self.rng) - (1 - mix)) * 2.2 + 0.5, 0, 1)
            t = self.warp(t, 12, 30)[..., None]
            c = c * (1 - t) + hexrgb(color2) * t
        self.canvas *= (1 - a * (1 - c))  # glaze: subtractive multiply

    def flat_grad(self, top=1.0, bottom=0.0, y0=0, y1=None):
        y1 = self.h if y1 is None else y1
        g = np.zeros((self.h, self.w), np.float32)
        ys = np.arange(self.h)
        t = np.clip((ys - y0) / max(1, (y1 - y0)), 0, 1)
        g[:] = (top + (bottom - top) * t)[:, None]
        return g

    # ---------- line work ----------
    def pencil(self, draw_fn, color='#3a3631', alpha=0.55, width=2, wobble=2.0):
        img, d = self.mask()
        draw_fn(d, width)
        m = np.asarray(img, np.float32) / 255
        m = self.warp(m, wobble, 10)
        m = cv2.GaussianBlur(m, (3, 3), 0.7)
        m *= 0.55 + 0.45 * (1 - self.tooth)  # broken stroke on tooth
        a = np.clip(m * alpha, 0, 1)[..., None]
        self.canvas *= (1 - a * (1 - hexrgb(color)))

    def splatter(self, color, n=60, rmin=1, rmax=4, alpha=0.5, region=None):
        img, d = self.mask()
        x0, y0, x1, y1 = region or (0, 0, self.w, self.h)
        for _ in range(n):
            x = self.rng.uniform(x0, x1); y = self.rng.uniform(y0, y1)
            r = self.rng.uniform(rmin, rmax)
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        self.wash(img, color, alpha, wobble=1, soft=0.8, edge=0.8, gran=0.2)

    # ---------- finish ----------
    def finish(self, vignette=0.06):
        c = self.canvas.copy()
        # paper emboss lighting
        t = self.tooth
        gx = cv2.Sobel(t, cv2.CV_32F, 1, 0, ksize=3)
        light = 1 + 0.06 * np.clip(gx, -1, 1)
        c *= light[..., None]
        # deckle-ish vignette, very gentle
        yy, xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        r = np.sqrt(((xx - self.w / 2) / self.w) ** 2 + ((yy - self.h / 2) / self.h) ** 2)
        c *= (1 - vignette * np.clip(r * 1.6 - 0.3, 0, 1))[..., None]
        c = np.clip(c, 0, 1)
        out = (c * 255).astype(np.uint8)
        # a whisper of edge-preserving smoothing unifies the pigment
        out = cv2.edgePreservingFilter(out[..., ::-1], flags=1, sigma_s=8, sigma_r=0.12)[..., ::-1]
        return out

    def save(self, path, q=82):
        out = self.finish()
        cv2.imwrite(path, out[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, q, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
        return path
