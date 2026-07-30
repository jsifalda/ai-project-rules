---
name: create-svg-logo
description: Create professional SVG logos from descriptions and design specifications. Generates multiple logo variations with different layouts, styles, and concepts. Produces scalable vector graphics that can be used directly or exported to PNG. Use this skill when users ask to create logos, brand identities, icons, or visual marks for their designs. Do NOT use for general-purpose images like banners, cards, OG images, hero graphics, or posters, and not for raster formats or photo editing.
---

# SVG Logo Designer

This skill creates professional, scalable vector graphic (SVG) logos from design specifications, offering multiple variations and layout options.

## When to Use This Skill

Activate this skill when the user requests:
- Create a logo from a description or specification
- Design a brand identity or visual mark
- Generate logo variations and concepts
- Create icons or symbols
- Design wordmarks or lettermarks
- Produce scalable graphics for branding
- Export logos in different layouts and styles

## Bundled References

Load each one at the point in the workflow where it is needed, not upfront:

- [references/color-psychology.md](references/color-psychology.md) — color to meaning to industry mapping. Read during Phase 1 when choosing or proposing a palette.
- [references/svg-patterns.md](references/svg-patterns.md) — starter markup for wordmark, geometric icon, abstract mark, and combination mark. Read during Phase 4.
- [references/presentation-template.md](references/presentation-template.md) — the output format for presenting concepts. Read during Phase 5.
- [references/usage-guidelines.md](references/usage-guidelines.md) — the usage-guidelines document to deliver with the files. Read during Phase 7.

## Core Workflow

### Phase 1: Requirements Gathering

When a user requests a logo, gather comprehensive design requirements:

1. **Brand Information**
   - Company/product name
   - Industry and market
   - Target audience
   - Brand personality (modern, classic, playful, serious, etc.)
   - Brand values and messaging
   - Competitors (for differentiation)

2. **Design Preferences**
   - Logo type:
     - **Wordmark**: Text-based logo (Google, Coca-Cola style)
     - **Lettermark**: Initials/abbreviation (IBM, HBO style)
     - **Pictorial Mark**: Icon/symbol (Apple, Twitter style)
     - **Abstract Mark**: Abstract geometric form (Pepsi, Adidas style)
     - **Mascot**: Character-based (KFC Colonel, Michelin Man style)
     - **Combination Mark**: Icon + text (Burger King, Lacoste style)
     - **Emblem**: Text inside symbol (Starbucks, Harley-Davidson style)

3. **Style Guidelines**
   - Color palette (specific colors or let AI choose) — consult [references/color-psychology.md](references/color-psychology.md)
   - Color psychology considerations
   - Font preferences (if text-based)
   - Visual style:
     - Minimalist
     - Geometric
     - Organic/flowing
     - Bold/strong
     - Elegant/refined
     - Playful/friendly
     - Tech/modern
     - Vintage/retro

4. **Technical Requirements**
   - Size constraints (will it be used small? large?)
   - Application contexts (website, print, merchandise, etc.)
   - Color vs monochrome versions needed
   - Background usage (light, dark, transparent)
   - Scalability requirements

5. **Number of Variations**
   - How many different concepts? (Recommend 3-5)
   - How many layouts per concept? (Horizontal, vertical, square, circular)
   - Color variations needed?

### Phase 2: Design Concept Development

Create multiple logo concepts based on requirements:

#### Concept 1: Primary Direction

Develop the main design direction:

**Design Thinking:**
- Research visual metaphors related to brand
- Consider negative space opportunities
- Ensure memorability and uniqueness
- Balance simplicity with distinctiveness
- Consider cultural appropriateness

**SVG Structure:**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <!-- Gradients, patterns, filters -->
    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4F46E5;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Logo elements -->
  <g id="logo-symbol">
    <!-- Symbol/icon elements -->
  </g>

  <g id="logo-text">
    <!-- Text elements (if applicable) -->
  </g>
</svg>
```

#### Concept 2-5: Alternative Directions

Create variations exploring different visual approaches:
- Different visual metaphors
- Different style treatments
- Different layouts and compositions
- Different color applications

### Phase 3: Layout Variations

For each concept, create multiple layout options:

#### Layout A: Horizontal Lockup
- Icon on left, text on right
- Best for website headers, business cards
- Wider aspect ratio

#### Layout B: Vertical Lockup
- Icon on top, text below
- Best for social media profiles, app icons
- Taller aspect ratio

#### Layout C: Square/Centered
- Icon and text centered
- Best for favicon, app icon, profile picture
- 1:1 aspect ratio

#### Layout D: Icon Only
- Symbol without text
- Best for small sizes, watermarks
- Compact, recognizable

#### Layout E: Text Only
- Wordmark without icon
- Best for minimal applications
- Typography-focused

### Phase 4: SVG Generation

Create professional, optimized SVG code. Start from the constructions in [references/svg-patterns.md](references/svg-patterns.md) — wordmark, geometric icon, abstract mark, and combination mark.

**Best Practices:**

1. **Clean, Semantic Code**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">
  <!-- Use groups for organization -->
  <g id="icon">
    <!-- Icon elements -->
  </g>
  <g id="wordmark">
    <!-- Text elements -->
  </g>
</svg>
```

2. **Scalable Design**
   - Use viewBox for scalability
   - Avoid pixel-specific sizes
   - Use relative units
   - Design at multiple sizes to test

3. **Color Management**
```xml
<!-- Define colors once, reuse throughout -->
<defs>
  <style>
    .primary { fill: #4F46E5; }
    .secondary { fill: #10B981; }
    .text { fill: #1F2937; }
  </style>
</defs>

<rect class="primary" x="0" y="0" width="100" height="100" />
```

4. **Optimization**
   - Remove unnecessary attributes
   - Combine paths where possible
   - Use symbols for repeated elements
   - Minimize decimal precision
   - Remove invisible elements

5. **Accessibility**
```xml
<svg role="img" aria-labelledby="logo-title logo-desc">
  <title id="logo-title">Company Name Logo</title>
  <desc id="logo-desc">A blue circular icon with the company name</desc>
  <!-- Logo content -->
</svg>
```

### Phase 5: Presentation

Present logos in an organized, professional manner. Use the concept-block format in [references/presentation-template.md](references/presentation-template.md): design rationale, then each layout with its SVG code, usage note, and dimensions, then the color variations.

### Phase 6: File Generation

Save SVG files with proper naming:

```javascript
// File naming convention
company-name-logo-concept1-horizontal.svg
company-name-logo-concept1-vertical.svg
company-name-logo-concept1-icon.svg
company-name-logo-concept2-horizontal.svg
// etc.
```

Use the Write tool to save each variation:
```javascript
// Example
Write({
  file_path: "./logos/acme-logo-concept1-horizontal.svg",
  content: svgCode
});
```

### Phase 7: Usage Guidelines

Provide comprehensive usage documentation. Fill in the template in [references/usage-guidelines.md](references/usage-guidelines.md) — file formats and PNG export, clear space, minimum sizes, color usage by context, incorrect usage, file organization, and web/responsive implementation.

## Iteration Process

After presenting initial concepts:

1. **Gather Feedback**
   - Which concept resonates most?
   - What elements to keep/change?
   - Any concerns or issues?

2. **Refine Selected Concept**
   - Adjust colors if needed
   - Tweak proportions
   - Refine details
   - Test at different sizes

3. **Create Final Variations**
   - All layout options
   - All color variations
   - Special use cases

4. **Deliver Final Package**
   - All SVG files
   - Usage guidelines
   - Technical specs
   - Export instructions

## Communication Style

When working with users:

1. **Understand the Brand**
   - Ask about brand personality
   - Understand target audience
   - Research industry context

2. **Explain Design Choices**
   - Share rationale for visual metaphors
   - Explain color psychology
   - Justify composition decisions

3. **Provide Options**
   - Offer multiple concepts
   - Show layout variations
   - Demonstrate color options

4. **Be Flexible**
   - Accept feedback gracefully
   - Iterate based on input
   - Explain limitations when necessary

5. **Educate**
   - Explain SVG benefits
   - Guide on proper usage
   - Share best practices

## Deliverables

Provide complete logo package:

1. **SVG Files**
   - All concepts (3-5)
   - All layouts per concept (3-5)
   - All color variations (3-4)
   - Total: 30-75 files typically

2. **Documentation**
   - Usage guidelines
   - Color specifications
   - Size recommendations
   - Do's and don'ts

3. **Technical Info**
   - File organization structure
   - Export instructions (SVG to PNG)
   - Web implementation examples
   - Print specifications

4. **Optional: Mockups**
   - Logo on business card
   - Logo on website header
   - Logo on product
   - Logo on signage

## Example Workflow

**User Request:**
> "Create a logo for my tech startup called 'CloudSync'. We provide cloud storage solutions. Looking for something modern and trustworthy."

**Your Response:**

1. **Clarify:**
   - "I'll create a modern, tech-focused logo for CloudSync. A few questions:
     - Preferred colors? (Suggesting blue for trust, or let me propose a palette)
     - Logo type preference? (I'm thinking combination mark - icon + text)
     - Any visual elements to avoid or include? (clouds, sync symbols, etc.)
     - How many concepts would you like to see? (I recommend 3-4)"

2. **Develop Concepts:**
   - **Concept 1**: Abstract cloud with sync arrows, modern geometric style
   - **Concept 2**: Minimalist wordmark with stylized 'C' incorporating cloud
   - **Concept 3**: Circular badge with cloud and connection nodes
   - **Concept 4**: Bold lettermark 'CS' with cloud integration

3. **Create Variations:**
   - For each concept: horizontal, vertical, icon-only layouts
   - Color variations: full color, monochrome, reversed

4. **Present:**
   - Show all concepts with rationale
   - Provide SVG code for each
   - Include usage guidelines
   - Offer iteration based on feedback

5. **Refine:**
   - User selects favorite concept
   - Make requested adjustments
   - Finalize all variations
   - Deliver complete package

Remember: Great logos are simple, memorable, timeless, versatile, and appropriate. Focus on creating designs that will work across all applications and stand the test of time!
