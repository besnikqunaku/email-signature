# Email Signature — Besnik Qunaku

Hand-coded HTML email signatures. No generator, no framework, no web fonts.
Built to render in Outlook Classic (Windows/Word engine), Outlook New, Gmail
(web + iOS/Android), Apple Mail and Thunderbird.

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

## The LinkedIn icon and Outlook Classic

By default `build.py` embeds the icon as a base64 `data:` URI, which keeps each
signature a single self-contained file. That works in Gmail (which re-hosts
pasted images on its own CDN), Outlook New, and Apple Mail.

**Outlook Classic cannot render `data:` URIs at all** — the Word engine only
accepts an absolute `http(s)` image URL. There the icon falls back to its
`alt="LinkedIn"` text, which is why a visible "LinkedIn" text link sits next to
it regardless.

To support Outlook Classic properly, host `assets/linkedin.png` and set the URL
in `build.py`:

```python
HOSTED_ICON_URL = "https://your-domain.com/linkedin.png"
```

then re-run `python3 build.py`.

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

## TODO

- [x] Real phone number — `+383 48 666 762`
- [x] Job title — Software Developer
- [ ] Host `linkedin.png` and set `HOSTED_ICON_URL` (required for Outlook Classic)
- [ ] Confirm surname spelling: Qunaku (per email + LinkedIn) vs Cunaku
