# Email Signature — Besnik Qunaku

Hand-coded HTML email signatures. No generator, no framework, no web fonts.
Built to render in Outlook Classic (Windows/Word engine), Outlook New, Gmail
(web + iOS/Android), Apple Mail and Thunderbird.

**Live preview:** https://besnikqunaku.github.io/email-signature/

## Layout

```
src/          source signatures (contain the __LI__ icon token)
assets/       linkedin.png — 96px, generated procedurally, 800 bytes
dist/         build output: copy-paste ready signatures + preview.html
build.py      substitutes the icon and generates the preview page
```

## Build

```bash
python3 build.py
open dist/preview.html
```

`dist/preview.html` renders all three variants on a white background with a
one-click **Copy signature** button and install steps for each client.

## Variants

| File | Style |
|---|---|
| `signature-a-monogram-tile.html` | Charcoal monogram tile, gold accent |
| `signature-b-minimal.html` | Single-column editorial, terracotta accent |
| `signature-c-card.html` | Bordered card, teal left bar |

## The LinkedIn icon

The icon is served from GitHub Pages:

```
https://besnikqunaku.github.io/email-signature/assets/linkedin.png
```

It is generated procedurally by `tools/make-icon.py`, which writes the PNG
directly with `zlib` — no image library, no design tool. The rounded tile and
the `in` glyph are drawn as geometry and rasterised with 4× supersampling for
antialiased edges. Output is 96px, 800 bytes, displayed at 18px for a crisp 4×
retina result.

An absolute `https` URL is **required**: `data:` URIs are stripped by the Gmail
signature editor and cannot be rendered by Outlook Classic at all. To embed the
icon as base64 instead (self-contained files, but Gmail and Outlook Classic will
drop it), set `HOSTED_ICON_URL = None` in `build.py` and rebuild.

Because images can be blocked by the recipient, a text "LinkedIn" link always
sits beside the icon and the image carries `alt="LinkedIn"`.

## Techniques used

- Nested tables only, `role="presentation"`, `cellpadding/cellspacing/border=0`,
  `border-collapse:collapse`
- `mso-line-height-rule:exactly` on every text cell; `mso-table-lspace/rspace:0pt`
  on every table — removes Outlook's phantom spacing
- Dividers and accent bars are `bgcolor` table cells, not CSS borders
- Monogram is live text in a colored cell, not an image — survives images-off
- Web-safe stacks only: Georgia for the monogram, Segoe UI/Roboto/Helvetica/Arial
  for body text
- Links double-wrapped in `<a style>` + inner `<span style>` to stop Outlook and
  Gmail forcing blue underline
- `mailto:`, `tel:` (E.164, no spaces) and a Google Maps link on the address
- Widths declared as both HTML attributes and CSS

## Status

- [x] Contact details final
- [x] Icon hosted on GitHub Pages
- [ ] Screenshot set: Outlook Classic, Outlook New, Gmail, iOS Mail
