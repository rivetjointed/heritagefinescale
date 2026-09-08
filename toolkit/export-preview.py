#!/usr/bin/env python3
"""Export the Ducceschi dossier pair as standalone pages for the Linden family preview.

The canonical pages live in this repo:

    site/dossiers/he-wrote-home-every-day.html
    site/dossiers/il-popolo-di-calamecca.html

They link /style.css, /dossier.css and /nav.js and use root-absolute paths, none of
which resolve on lindenstreetstudio.com. The family preview at
C:\\Work\\Sites\\linden\\preview\\heritage-fine-scale\\ is the same two pages made
self-contained: the two sheets inlined, the site nav dropped (its links are this
site's), paths made relative to the folder, the header lockup unlinked, and every
HTML comment removed (the audit flags studio-facing comments behind the gate).

    python toolkit/export-preview.py            # writes both pages
    python toolkit/export-preview.py --dry-run  # reports what would change

Idempotent. Edit the pages here and re-run; never edit the preview copies by hand.
The preview's images/dossiers/ducceschi/ folder is a copy of site/images/dossiers/ducceschi/
and is refreshed on every run too.
"""
import os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
DEST = r"C:\Work\Sites\linden\preview\heritage-fine-scale"

PAGES = {  # source in site/dossiers -> name in the preview folder
    "he-wrote-home-every-day.html": "index.html",
    "il-popolo-di-calamecca.html": "ducceschi-calamecca.html",
}
LINKS = {  # root-absolute page links -> preview-relative
    "/dossiers/he-wrote-home-every-day.html": "index.html",
    "/dossiers/il-popolo-di-calamecca.html": "ducceschi-calamecca.html",
}
DROP_HEAD = (
    '  <link rel="icon" href="/favicon.ico" sizes="any" />\n'
    '  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />\n'
    '  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />\n'
    '  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />\n'
    '  <link rel="manifest" href="/site.webmanifest" />\n'
    '  <meta name="theme-color" content="#16110A" />\n'
    '\n'
)
# No banner and no HTML comments at all in the export: the family can read View
# Source, and site-audit.py flags any studio-facing comment behind the preview gate.


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def must(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f"export-preview: anchor found {n}x, expected {count}: {old[:60]!r}")
    return text.replace(old, new)


def convert(src_name, html, css):
    html = must(html, DROP_HEAD, "")
    html = must(html,
        '  <link rel="stylesheet" href="/style.css" />\n  <link rel="stylesheet" href="/dossier.css" />\n',
        "  <style>\n" + css + "\n  </style>\n")
    html = must(html, '      <a href="/" aria-label="Heritage Fine Scale home">',
                      '      <span aria-label="Heritage Fine Scale">')
    html = must(html, '        </div>\n      </a>\n    </div>\n  </header>\n\n  <div id="site-nav"></div>',
                      '        </div>\n      </span>\n    </div>\n  </header>')
    html = must(html, '  <script src="/nav.js" defer></script>\n\n</body>', "</body>")
    html = html.replace('"/images/dossiers/ducceschi/', '"images/dossiers/ducceschi/')
    for a, b in LINKS.items():
        html = html.replace(f'href="{a}"', f'href="{b}"')
    assert 'href="/' not in html.replace('href="https://', ""), "a root-absolute link survived"
    html = re.sub(r"[ \t]*<!--.*?-->[ \t]*\n?", "", html, flags=re.S)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


def main():
    dry = "--dry-run" in sys.argv
    css = read(os.path.join(SITE, "style.css")) + "\n\n" + read(os.path.join(SITE, "dossier.css"))
    for src_name, dst_name in PAGES.items():
        out = convert(src_name, read(os.path.join(SITE, "dossiers", src_name)), css)
        dst = os.path.join(DEST, dst_name)
        same = os.path.exists(dst) and read(dst) == out
        print(("unchanged " if same else ("would write " if dry else "wrote ")) + dst)
        if not same and not dry:
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
    src_img = os.path.join(SITE, "images", "dossiers", "ducceschi")
    dst_img = os.path.join(DEST, "images", "dossiers", "ducceschi")
    copied = 0
    for name in sorted(os.listdir(src_img)):
        s, d = os.path.join(src_img, name), os.path.join(dst_img, name)
        if not os.path.exists(d) or os.path.getsize(d) != os.path.getsize(s):
            copied += 1
            if not dry:
                os.makedirs(dst_img, exist_ok=True)
                shutil.copy2(s, d)
    print(f"images: {copied} {'to copy' if dry else 'copied'}, {len(os.listdir(src_img)) - copied} already current")


if __name__ == "__main__":
    main()
