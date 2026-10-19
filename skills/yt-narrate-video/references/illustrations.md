# Illustration guide

## Rules

- Draw each scene as inline SVG in the page. Use simple editorial shapes: silhouettes, maps, diagrams, objects. No raster images.
- Color only through the theme classes in the template. Never put a hex color in a scene. Light and dark mode then both work.
  - Fills: `f-ink`, `f-ink2`, `f-paper`, `f-paper2`, `f-card`, `f-rule`, `f-sky`, `f-go`, `f-yield`, `f-stop`, `f-none`.
  - Strokes: `s-ink`, `s-ink2`, `s-rule`, `s-paper`, `s-sky`, `s-go`, `s-yield`, `s-stop`.
  - Effects: `o2`, `o3`, `o6` for opacity, `dash` for a dashed stroke.
- Give each SVG `role="img"` and a real `aria-label` that says what the scene shows. The hero uses `{{HERO_ALT}}` as its label.
- Put a `<figcaption>` under each chapter figure. The caption adds meaning. It does not describe the picture.
- Make repeated elements (dot grids, windows, crowds, seeds) with the `rep()` helper in the scenes section of the template. Do not write them by hand.
- Give each repeated-shape group a unique id per scene, with its own `rep()` call. `rep()` fills only the first match.
- Replace each sample scene in the template and delete its `data-sample` attribute. `assemble.py` fails while one is left.
- Use deterministic positions. Do not use `Math.random`, so screenshots stay stable.
- Show no real person's face or likeness. Use anonymous silhouettes only. Use no logos and no remote images.
- Symbolic beats literal. Draw one object from the story per scene.
- Encode a number from the story in the picture when you can. Point to it in the caption.
- Keep a scene to about 10 to 30 elements.
- Use the viewBox sizes of the template: hero `0 0 1600 900` with `preserveAspectRatio="xMidYMid slice"`, chapter `0 0 1200 640`.

## Examples

A chapter figure with its caption. The empty `<g>` receives generated shapes.

```html
<figure class="art"><svg viewBox="0 0 1200 640" role="img" aria-label="A tall office block at dusk with twelve windows, most of them lit.">
  <rect width="1200" height="640" class="f-sky o2"/>
  <circle cx="170" cy="150" r="46" class="f-yield o6"/>
  <rect y="520" width="1200" height="120" class="f-paper2"/>
  <rect x="360" y="170" width="480" height="360" class="f-ink2"/>
  <g id="scene1Windows"></g>
  <rect y="518" width="1200" height="4" class="f-ink"/>
</svg><figcaption>Eight of twelve windows stay lit after midnight. That is the real cost.</figcaption></figure>
```

A `rep()` call. It fills the group above with a grid of windows. Every third window is dark.

```js
rep('#scene1Windows',12,i=>['rect',{x:392+(i%6)*72,y:210+Math.floor(i/6)*110,width:40,height:64,class:i%3?'f-yield':'f-paper'}]);
```

A small diagram with the same classes. A dashed line links two boxes, and the number is shown as filled dots.

```html
<figure class="art"><svg viewBox="0 0 1200 640" role="img" aria-label="Two boxes, client and server, linked by a dashed line with five dots on it.">
  <rect x="140" y="240" width="260" height="160" class="f-card s-ink" stroke-width="4"/>
  <rect x="800" y="240" width="260" height="160" class="f-ink2"/>
  <path d="M400 320 L800 320" class="f-none s-go dash" stroke-width="6"/>
  <g id="scene2Dots"></g>
</svg><figcaption>Five round trips before the page draws. Each one is a wait.</figcaption></figure>
```

```js
rep('#scene2Dots',5,i=>['circle',{cx:480+i*60,cy:320,r:10,class:'f-go'}]);
```
