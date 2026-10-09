# Watercolor engine

`scripts/watercolor.py` paints with masks. Draw a shape with PIL, then `wash()` uses OpenCV to warp its edge, pool pigment at the rim, settle pigment into the paper tooth, and glaze it onto the canvas with a subtractive multiply. Start from `scripts/scene_example.py` (a road at dusk with a hanging traffic light).

## API

```python
from watercolor import *          # Painting, hexrgb, fbm, smooth_noise, np, cv2
p = Painting(W, H, paper='#fbfaf6', seed=11)   # 1400x860 to 1600x900 works well
img, d = p.mask()                  # PIL L image + ImageDraw. Draw shapes with fill=255
p.wash(img, '#7aa3c4', alpha=0.6,  # main tool
       wobble=5,      # edge warp in px. 0 for flat skies, 2-4 objects, 10-20 clouds, foliage
       soft=2.5,      # blur sigma of the edge
       edge=0.55,     # wet-edge darkening at the rim. 0.3 soft, 0.8 crisp
       gran=0.35,     # granulation into paper tooth. 0.6-0.8 for earth, asphalt
       bloom=0.0,     # backrun blooms, 0.3-0.6 for skies, foliage
       gradient=None, # array 0..1, e.g. p.flat_grad(1, 0, y0, y1) for graded skies
       color2=None, mix=0.5)  # wet-in-wet second pigment
p.pencil(lambda d, w: d.line(pts, fill=255, width=w), color='#3a3631', width=3, alpha=0.6)
p.splatter('#6b5a3a', n=50, region=(x0, y0, x1, y1), alpha=0.4)
full = np.ones((H, W), np.float32)  # whole-canvas mask for skies and walls
p.save('out.jpg')                   # applies paper emboss, vignette, edge-preserving finish
```

## Lessons from real scenes

- **Paint light to dark.** Glazes only darken. A light shape painted on top of a dark one does not show. Paint the light area first, or cut it out of the dark mask (`d.ellipse(inner, fill=0)`).
- **Rings for frames.** Clock faces, mirrors, dials: draw the frame as outer shape minus inner shape. Otherwise the frame color floods the glass.
- **Light sources are additive.** Flames, lamps, glowing signals: build a blurred mask and add color (`p.canvas = np.clip(p.canvas + glow[..., None] * rgb * k, 0, 1)`), then paint the flame body by mixing toward a bright color. A wash cannot make anything brighter.
- **Clip shapes to their zone.** A road triangle that runs under a dashboard still darkens it. End shapes where the next layer begins.
- **Symbolic beats literal.** Pick one object from the story per scene (a wall phone with the clock at the exact time mentioned, footprints circling one pothole, 100 seeds with 8 sprouts). Encode a number from the story in the picture when you can, and point to it in the caption.
- **People as anonymous silhouettes only.** Never an identifiable real person.
- **Avoid gimmicky shapes.** Big diagonal limbs, stiff hands and gloves read badly. Remove them rather than fix them.
- **Review a contact sheet.** Render all scenes, tile thumbnails into one image with OpenCV, view it, fix the weakest two, render again.

## Size budget

Render at 1400 to 1600 px wide. `scripts/assemble.py` downsizes to 1100 px (hero 1400 px) at JPEG quality 76 and inlines them. Fifteen scenes come to about 1.1 MB, well under the 16 MB page limit.
