#!/usr/bin/env python3
"""
Build the email signatures.

Reads src/signature-*.html, substitutes __LI__ with the base64 LinkedIn icon
(or a hosted URL, if one is configured below), and writes:

    dist/signature-*.html   copy-paste ready signatures
    dist/preview.html       side-by-side preview + one-click copy + install steps

Run:  python3 build.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC, DIST, ASSETS = ROOT / "src", ROOT / "dist", ROOT / "assets"

# ---------------------------------------------------------------------------
# Set this to an absolute https:// URL once the icon is hosted somewhere.
# A hosted URL is required for Outlook Classic, which cannot render data: URIs.
# Leave as None to embed the icon as base64.
HOSTED_ICON_URL = "https://besnikqunaku.github.io/email-signature/assets/linkedin.png"
# ---------------------------------------------------------------------------

VARIANTS = [
    ("signature-a-monogram-tile.html", "Variant A", "Monogram Tile"),
    ("signature-b-minimal.html",       "Variant B", "Minimal Editorial"),
    ("signature-c-card.html",          "Variant C", "Accent Card"),
]


def icon_src() -> str:
    if HOSTED_ICON_URL:
        return HOSTED_ICON_URL
    png = (ASSETS / "linkedin.png").read_bytes()
    return "data:image/png;base64," + base64.b64encode(png).decode()


def strip_leading_comment(html: str) -> str:
    return re.sub(r"^\s*<!--.*?-->\s*", "", html, count=1, flags=re.S)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Besnik Qunaku — Email Signature</title>
<style>
  :root{{--bg:#101214;--panel:#181B1F;--line:#2A2F35;--ink:#EDEEF0;--muted:#9AA1A9;--accent:#C9A227}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}}
  .wrap{{max-width:820px;margin:0 auto;padding:48px 20px 96px}}
  h1{{font-size:26px;margin:0 0 6px;letter-spacing:-.4px}}
  .sub{{color:var(--muted);margin:0 0 40px;font-size:14px}}
  .card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin:0 0 28px;overflow:hidden}}
  .card-head{{display:flex;align-items:center;justify-content:space-between;gap:12px;
    padding:14px 18px;border-bottom:1px solid var(--line);flex-wrap:wrap}}
  .label{{font-size:13px;font-weight:600;letter-spacing:.3px}}
  .label span{{color:var(--muted);font-weight:400;margin-left:8px}}
  button{{background:var(--accent);color:#15171C;border:0;border-radius:7px;padding:8px 15px;
    font:600 13px/1 inherit;cursor:pointer;white-space:nowrap}}
  button:hover{{filter:brightness(1.08)}}
  button.done{{background:#2E9E6B;color:#fff}}
  .stage{{background:#fff;padding:30px 26px;overflow-x:auto}}
  h2{{font-size:15px;margin:44px 0 12px;letter-spacing:.2px}}
  ol{{padding-left:20px;color:var(--muted);font-size:14px}}
  ol li{{margin:0 0 9px}}
  code{{background:#22262B;border:1px solid var(--line);border-radius:4px;padding:1px 6px;
    font:13px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:#E4D3A0}}
  .note{{border-left:3px solid var(--accent);background:#1C1F24;padding:12px 16px;
    border-radius:0 8px 8px 0;font-size:13.5px;color:#C6CCD3;margin:16px 0}}
</style>
</head>
<body>
<div class="wrap">
  <h1>Besnik Qunaku — Email Signature</h1>
  <p class="sub">Three hand-coded variants. Monogram and layout are pure HTML/CSS —
     only the LinkedIn icon is an image, and it falls back to the text
     &ldquo;LinkedIn&rdquo; when images are blocked.</p>
{cards}
  <h2>Install in Gmail</h2>
  <ol>
    <li>Click <strong>Copy signature</strong> above (it copies the rendered result, not the code).</li>
    <li>Gmail &rarr; <strong>Settings</strong> (gear) &rarr; <strong>See all settings</strong> &rarr; <strong>General</strong>.</li>
    <li>Scroll to <strong>Signature</strong> &rarr; <strong>Create new</strong> &rarr; name it <code>Main</code>.</li>
    <li>Click into the box and paste with <code>Cmd+V</code>. Do <em>not</em> use &ldquo;Paste as plain text&rdquo;.</li>
    <li>Under <strong>Signature defaults</strong>, set it for <em>FOR NEW EMAILS USE</em> and <em>ON REPLY/FORWARD USE</em>.</li>
    <li>Bottom of the page &rarr; <strong>Save Changes</strong>.</li>
  </ol>

  <h2>Install in Outlook (New / Web)</h2>
  <ol>
    <li>Copy the signature above.</li>
    <li><strong>Settings</strong> &rarr; <strong>Mail</strong> &rarr; <strong>Compose and reply</strong>.</li>
    <li>Paste, tick both &ldquo;new messages&rdquo; and &ldquo;replies/forwards&rdquo;, then <strong>Save</strong>.</li>
  </ol>

  <h2>Install in Outlook Classic (Windows)</h2>
  <ol>
    <li>Copy the signature above.</li>
    <li><strong>File</strong> &rarr; <strong>Options</strong> &rarr; <strong>Mail</strong> &rarr; <strong>Signatures&hellip;</strong> &rarr; <strong>New</strong>.</li>
    <li>Paste, set it for New messages and Replies/forwards, click <strong>OK</strong>.</li>
  </ol>

  <div class="note">
    <strong>Outlook Classic note:</strong> the LinkedIn icon is embedded as a
    <code>data:</code> URI, which Outlook Classic cannot render &mdash; it falls back to the
    text &ldquo;LinkedIn&rdquo; beside it. Host <code>assets/linkedin.png</code>, set
    <code>HOSTED_ICON_URL</code> in <code>build.py</code>, and re-run
    <code>python3 build.py</code> to fix that.
  </div>
</div>
<script>
function copySig(id, btn){{
  var el = document.getElementById(id);
  var range = document.createRange();
  range.selectNodeContents(el);
  var sel = window.getSelection();
  sel.removeAllRanges(); sel.addRange(range);
  var ok = false;
  try {{ ok = document.execCommand('copy'); }} catch(e) {{ ok = false; }}
  sel.removeAllRanges();
  btn.textContent = ok ? 'Copied \\u2713' : 'Select it manually';
  btn.className = ok ? 'done' : '';
  setTimeout(function(){{ btn.textContent = 'Copy signature'; btn.className = ''; }}, 2200);
}}
</script>
</body>
</html>
"""

CARD = """  <div class="card">
    <div class="card-head">
      <div class="label">{title} <span>{subtitle}</span></div>
      <button onclick="copySig('{sid}',this)">Copy signature</button>
    </div>
    <div class="stage"><div id="{sid}">
{body}
    </div></div>
  </div>
"""


def main() -> None:
    src_uri = icon_src()
    DIST.mkdir(exist_ok=True)
    cards = []

    for i, (fname, title, subtitle) in enumerate(VARIANTS):
        raw = (SRC / fname).read_text(encoding="utf-8")
        built = raw.replace("__LI__", src_uri)
        (DIST / fname).write_text(built, encoding="utf-8")
        cards.append(CARD.format(
            title=title, subtitle=subtitle, sid="sig%d" % i,
            body=strip_leading_comment(built).rstrip(),
        ))
        print("wrote dist/%s  (%d bytes)" % (fname, len(built)))

    page = PAGE.format(cards="\n".join(cards))
    (DIST / "preview.html").write_text(page, encoding="utf-8")
    print("wrote dist/preview.html")

    # Same page at the repo root, so GitHub Pages serves it as the landing page.
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("wrote index.html")
    print("icon source: %s" % ("hosted URL" if HOSTED_ICON_URL else "embedded base64"))


if __name__ == "__main__":
    main()
