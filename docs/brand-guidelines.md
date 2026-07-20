# Brand guidelines

A short guide to the project's visual identity so it stays consistent as the
repository grows.

## Name and tagline

- **Name:** Practical Python Projects
- **Tagline:** _Learn Python by building practical, tested, and
  production-minded projects._

Write the name in full on first use. "PPP" is acceptable as a short form in
internal notes but not in public headings.

## Tone

Friendly, direct, and honest. Explain value plainly, avoid hype ("best",
"ultimate", "enterprise-grade"), and be clear about what is and is not
production-ready.

## Colors

| Role | Hex | Use |
|---|---|---|
| Ink (background) | `#0B1220` → `#152449` | Dark gradient backgrounds |
| Tile | `#0F172A` → `#1E3A8A` | The logo tile |
| Sky (primary accent) | `#38BDF8` | The prompt chevron, highlights |
| Teal (secondary accent) | `#2DD4BF` | The progression bars |
| Text light | `#F8FAFC` | Headings on dark backgrounds |
| Text muted | `#93C5FD` | Supporting text on dark backgrounds |

## The mark

The logo combines a terminal-style **chevron** (you build it yourself) with
**three ascending bars** (steady learning progression) on a rounded tile. It is
an original, geometric mark — no third-party logos or stock artwork.

## Assets

All assets live in [`assets/brand/`](../assets/brand/):

| File | Purpose |
|---|---|
| `logo.svg` | Square mark (256×256). |
| `banner.svg` | README banner (1280×320) with its own dark background, so it stays readable in both light and dark themes. |
| `social-preview.svg` | Source for the social preview (1280×640). |
| `social-preview.png` | Exported social preview for GitHub (1280×640, under 1 MB). |

## Reuse and regeneration

- The SVGs contain no scripts or external references and can be edited in any
  vector editor or a text editor.
- To regenerate `social-preview.png` from the SVG, render it at 1280×640 with any
  SVG renderer (for example a headless browser screenshot of the SVG sized to
  1280×640).
- Keep every image's alt text meaningful when embedding it in documentation.

## Accessibility

- The banner and social preview carry their own dark background, so they do not
  depend on the reader's theme.
- Text over the background meets a comfortable contrast ratio.
- Never rely on color alone to convey meaning.
