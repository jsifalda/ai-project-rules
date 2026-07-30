# Logo Usage Guidelines Template

The document to hand the user alongside the SVG files. Substitute real colors, sizes, and file names before delivering.

Contents of the template below:
- File formats provided, and SVG to PNG export (L16-38)
- Clear space and minimum sizes (L40-49)
- Color usage by context (L51-71)
- Incorrect usage (L73-81)
- File organization (L83-98)
- Technical specifications, web and responsive (L100-131)

````markdown
# Logo Usage Guidelines

## File Formats Provided

### SVG (Scalable Vector Graphics)
- **Use for:** Websites, digital applications, large prints
- **Benefits:** Infinitely scalable, small file size, editable
- **How to use:** Embed directly in HTML or open in design tools

### Exporting to PNG
If you need PNG format:

**Option 1: Using Inkscape (Free)**
```bash
inkscape logo.svg --export-png=logo.png --export-width=1000
```

**Option 2: Using ImageMagick**
```bash
convert -background none logo.svg logo.png
```

**Option 3: Online Converter**
- Visit: https://cloudconvert.com/svg-to-png
- Upload SVG, download PNG

## Clear Space

Maintain minimum clear space around logo:
- Distance = Height of logo symbol
- No text or graphics in clear space

## Minimum Sizes

- **Digital:** 100px width minimum
- **Print:** 1 inch width minimum

## Color Usage

### Primary Color Palette
- Use full color on white/light backgrounds
- Use monochrome white on dark backgrounds
- Use monochrome dark on light backgrounds

### Color Variations by Context

**Website Headers:**
- Full color version preferred
- Ensure 4.5:1 contrast with background

**Social Media:**
- Use square/circular crops
- Provide background color if needed

**Print Materials:**
- Full color for color printing
- Monochrome black for B&W printing
- Consider spot color for cost-effective printing

## Incorrect Usage

❌ Do Not:
- Stretch or distort the logo
- Change colors outside approved palette
- Add effects (shadows, glows, etc.)
- Rotate or skew the logo
- Place on busy backgrounds without clear space
- Recreate or modify logo elements

## File Organization

```
logos/
  concept-1/
    horizontal/
      full-color.svg
      monochrome-dark.svg
      monochrome-light.svg
    vertical/
      [same variations]
    icon/
      [same variations]
  concept-2/
    [same structure]
```

## Technical Specifications

### Web Usage
```html
<!-- Inline SVG (Recommended for control) -->
<svg><!-- SVG code --></svg>

<!-- Image tag (Simpler) -->
<img src="logo.svg" alt="Company Name Logo" />

<!-- CSS Background -->
.logo {
  background-image: url('logo.svg');
  background-size: contain;
}
```

### Responsive Implementation
```css
.logo {
  width: 100%;
  max-width: 200px;
  height: auto;
}

/* Mobile */
@media (max-width: 768px) {
  .logo {
    max-width: 150px;
  }
}
```
````
