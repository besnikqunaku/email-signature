#!/usr/bin/env python3
"""
Build the email signatures.

Reads src/<set>/*.html, resolves __ASSET:<file>__ tokens to hosted image URLs,
and writes:

    dist/<set>/*.html   copy-paste ready signatures
    dist/preview.html   the showcase page
    index.html          same page at repo root, for GitHub Pages

Run:  python3 build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"

# Absolute https URLs are required. `data:` URIs are stripped by the Gmail
# signature editor and cannot be rendered by Outlook Classic at all.
ASSET_BASE = "https://besnikqunaku.github.io/email-signature/assets/"

SETS = [
    {
        "id": "personal",
        "title": "Personal",
        "variants": [
            ("signature-a-monogram-tile.html", "Monogram Tile"),
            ("signature-b-minimal.html", "Minimal"),
            ("signature-c-card.html", "Accent Card"),
        ],
    },
    {
        "id": "lawfirm",
        "title": "Krasniqi & Dedaj",
        "note": "Fictional firm — design sample",
        "variants": [
            ("lawfirm-letterhead.html", "Letterhead"),
            ("lawfirm-compact.html", "Compact"),
        ],
    },
]

ASSET_RE = re.compile(r"__ASSET:([A-Za-z0-9._-]+)__")


def strip_leading_comment(html: str) -> str:
    return re.sub(r"^\s*<!--.*?-->\s*", "", html, count=1, flags=re.S)


CARD = """    <article class="card">
      <div class="bar">
        <span class="name">{name}</span>
        <span class="tag">{tag}</span>
        <button type="button" onclick="copySig('{sid}',this)">COPY</button>
      </div>
      <div class="stage"><div id="{sid}">
{body}
      </div></div>
    </article>
"""


def main() -> None:
    DIST.mkdir(exist_ok=True)
    cards, n = [], 0

    for spec in SETS:
        out_dir = DIST / spec["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        tag = spec.get("note") or spec["title"]

        for fname, name in spec["variants"]:
            raw = (SRC / spec["id"] / fname).read_text(encoding="utf-8")
            built = ASSET_RE.sub(lambda m: ASSET_BASE + m.group(1), raw)
            (out_dir / fname).write_text(built, encoding="utf-8")
            cards.append(CARD.format(
                name=name, tag=tag, sid="sig%d" % n,
                body=strip_leading_comment(built).rstrip(),
            ))
            n += 1
            print("wrote dist/%s/%s  (%d bytes)" % (spec["id"], fname, len(built)))

    page = (ROOT / "page.template.html").read_text(encoding="utf-8")
    page = page.replace("<!--CARDS-->", "".join(cards))
    page = page.replace("<!--COUNT-->", str(n))

    if ASSET_RE.search(page):
        raise SystemExit("unresolved __ASSET:__ token in output")

    (DIST / "preview.html").write_text(page, encoding="utf-8")
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("wrote dist/preview.html and index.html  (%d designs)" % n)


if __name__ == "__main__":
    main()
