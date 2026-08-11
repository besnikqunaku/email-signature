#!/usr/bin/env python3
"""
Build the email signatures.

Reads src/<set>/*.html, substitutes __LI__ with the LinkedIn icon source, and
writes:

    dist/<set>/*.html   copy-paste ready signatures
    dist/preview.html   showcase page (copy buttons + compatibility notes)
    index.html          same page at repo root, for GitHub Pages

Run:  python3 build.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC, DIST, ASSETS = ROOT / "src", ROOT / "dist", ROOT / "assets"

# An absolute https URL is required: `data:` URIs are stripped by the Gmail
# signature editor and cannot be rendered by Outlook Classic at all.
# Set to None to embed the icon as base64 instead.
HOSTED_ICON_URL = "https://besnikqunaku.github.io/email-signature/assets/linkedin.png"

SETS = [
    {
        "id": "personal",
        "title": "Personal",
        "lede": "Signatures for my own correspondence. No logo, so identity is "
                "carried by a typographic monogram set in Georgia — live text "
                "in a coloured table cell, not an image, so it survives with "
                "images disabled.",
        "variants": [
            ("signature-a-monogram-tile.html", "Monogram Tile",
             "Charcoal tile, gold accent. Strongest identity mark."),
            ("signature-b-minimal.html", "Minimal Editorial",
             "Single column — structurally incapable of breaking on narrow screens."),
            ("signature-c-card.html", "Accent Card",
             "Bordered card with a solid left bar."),
        ],
    },
    {
        "id": "cohax",
        "title": "Cohax L.L.C",
        "lede": "Concept work for a former employer, built to their existing brand: "
                "Manrope, navy <code>#0C111D</code>, electric blue <code>#028AFB</code>, "
                "all taken from cohax.co. The wordmark is live text rather than a "
                "logo image, for the same images-off reason.",
        "badge": "Concept — not an official Cohax asset",
        "variants": [
            ("cohax-corporate.html", "Corporate",
             "Brand band, labelled contact rows, footer strip. The full-dress version."),
            ("cohax-compact.html", "Compact",
             "No background fills, so it sits cleanly inside a reply chain."),
        ],
    },
]


def icon_src() -> str:
    if HOSTED_ICON_URL:
        return HOSTED_ICON_URL
    png = (ASSETS / "linkedin.png").read_bytes()
    return "data:image/png;base64," + base64.b64encode(png).decode()


def strip_leading_comment(html: str) -> str:
    return re.sub(r"^\s*<!--.*?-->\s*", "", html, count=1, flags=re.S)


CARD = """      <div class="card">
        <div class="card-head">
          <div>
            <div class="label">{name}</div>
            <div class="desc">{desc}</div>
          </div>
          <button onclick="copySig('{sid}',this)">Copy signature</button>
        </div>
        <div class="stage"><div id="{sid}">
{body}
        </div></div>
      </div>
"""

SECTION = """    <section>
      <h2>{title}{badge}</h2>
      <p class="lede">{lede}</p>
{cards}    </section>
"""

BADGE = ' <span class="badge">{}</span>'


def main() -> None:
    src_uri = icon_src()
    DIST.mkdir(exist_ok=True)
    sections, n = [], 0

    for spec in SETS:
        out_dir = DIST / spec["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        cards = []

        for fname, name, desc in spec["variants"]:
            raw = (SRC / spec["id"] / fname).read_text(encoding="utf-8")
            built = raw.replace("__LI__", src_uri)
            (out_dir / fname).write_text(built, encoding="utf-8")
            cards.append(CARD.format(
                name=name, desc=desc, sid="sig%d" % n,
                body=strip_leading_comment(built).rstrip(),
            ))
            n += 1
            print("wrote dist/%s/%s  (%d bytes)" % (spec["id"], fname, len(built)))

        sections.append(SECTION.format(
            title=spec["title"],
            badge=BADGE.format(spec["badge"]) if spec.get("badge") else "",
            lede=spec["lede"],
            cards="".join(cards),
        ))

    page = (ROOT / "page.template.html").read_text(encoding="utf-8")
    page = page.replace("<!--SECTIONS-->", "".join(sections))

    (DIST / "preview.html").write_text(page, encoding="utf-8")
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("wrote dist/preview.html and index.html")
    print("icon source: %s" % ("hosted URL" if HOSTED_ICON_URL else "embedded base64"))


if __name__ == "__main__":
    main()
