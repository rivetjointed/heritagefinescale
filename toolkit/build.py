#!/usr/bin/env python3
"""HFS reference-page generator. One template, one CSS, config-driven.

build(cfg) -> writes cfg['out'] and returns stats.

cfg keys:
  md_text     str  preprocessed markdown (years + Notes; no ## Framework/## Scope)
  out         str  output path
  title,kicker,deck,meta_desc   str
  series_label str   e.g. "European Theater"
  marking     "flags" | "insignia"
  allied,axis [(id,label),...]
  banner_title,banner_note      str
  framework   [(label,value),...] | None   (top block)
  addendum    {"title":str,"fields":[(label,value),...]} | None  (before Notes)
  scope       [(label,value),...] | None   (overrides md frontmatter)
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sprites

# ---------- inline markdown ----------
def inline(text):
    text = text.strip()
    text = (text.replace("\\~", "~").replace("\\[", "[").replace("\\]", "]")
                .replace("\\&", "&").replace("\\-", "-").replace("\\.", "."))
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text

def is_year(s):
    return re.fullmatch(r"\d{4}", s.strip()) is not None

# ---------- parse markdown ----------
def parse(md):
    lines = md.split("\n")
    frontmatter, years, year_order, notes = [], {}, [], []
    named, named_order = {}, []   # non-year chronology sections, in source order
    section, cur = None, None
    skip = {"Table of Contents", "Framework", "Scope"}

    def bucket(sec):
        if sec in years: return years[sec]
        if sec in named: return named[sec]["entries"]
        return None

    for ln in lines:
        s = ln.rstrip()
        if s.startswith("# ") and not s.startswith("## "):
            continue
        if s.startswith("## "):
            b = bucket(section)
            if cur is not None and b is not None:
                b.append(cur)
            cur = None
            name = s[3:].strip()
            section = name
            if is_year(name):
                if name not in years:
                    years[name] = []; year_order.append(name)
            elif name not in skip and not name.startswith("Notes"):
                if name not in named:
                    named[name] = {"preamble": "", "entries": []}
                    named_order.append(name)
            continue
        if s.startswith("### "):
            b = bucket(section)
            if cur is not None and b is not None:
                b.append(cur)
            cur = None
            heading = s[4:].strip()
            if bucket(section) is not None:
                if " — " in heading:
                    d, t = heading.split(" — ", 1)
                else:
                    d, t = "", heading
                cur = {"date": d.strip(), "title": t.strip(), "fields": []}
            continue
        # italic section preamble: *...* paragraph before first entry of a named section
        if (section in named and cur is None and s.startswith("*") and s.endswith("*")
                and not s.startswith("**")):
            named[section]["preamble"] = s.strip("*").strip()
            continue
        m = re.match(r"^\*\*([^:]+):\*\*\s*(.*)$", s)
        if m:
            lab, val = m.group(1).strip(), m.group(2).strip()
            if section is None or section in skip:
                frontmatter.append((lab, val))
            elif bucket(section) is not None and cur is not None:
                cur["fields"].append([lab, val])
            continue
        if section == "Notes on Scope Edges" and s.startswith("* "):
            notes.append(s[2:].strip()); continue
        if section == "Notes on Scope Edges" and s.startswith("- "):
            notes.append(s[2:].strip()); continue
        if section == "Notes on Scope Edges" and s.strip() and notes:
            notes[-1] += " " + s.strip()
    b = bucket(section)
    if cur is not None and b is not None:
        b.append(cur)
    # numeric year ordering (so 1939 sorts before 1940 even if appended later)
    year_order = sorted(set(year_order), key=lambda y: int(y))
    return frontmatter, years, year_order, notes, named, named_order

# ---------- render helpers ----------
def field_rows(fields):
    return "\n".join(
        '<div class="fld"><span class="fld-k">{}</span><span class="fld-v">{}</span></div>'
        .format(inline(k), inline(v)) for k, v in fields)

def render_years(years, year_order):
    out = []
    for y in year_order:
        eh = []
        for e in years[y]:
            eh.append(
"""    <article class="entry">
      <p class="entry-date">{date}</p>
      <h3 class="entry-title">{title}</h3>
      <div class="entry-fields">
{rows}
      </div>
    </article>""".format(date=inline(e["date"]), title=inline(e["title"]),
                         rows=field_rows(e["fields"])))
        out.append(
"""  <section class="year" id="y{y}">
    <div class="year-head"><h2>{y}</h2><span class="rivet-rule"></span>{tt}</div>
{entries}
  </section>""".format(y=y, entries="\n".join(eh), tt=TOTOP))
    return "\n\n".join(out)

def slug(name):
    t = re.sub(r"\(.*?\)", "", name)
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t or "section"

def short_label(name):
    # nav-pill label: text before any em-dash/slash/parenthetical, tightened
    t = re.sub(r"\(.*?\)", "", name).strip()
    return t

def render_named(named, named_order, labels=None):
    labels = labels or {}
    out = []
    for name in named_order:
        sec = named[name]
        pre = ('    <p class="section-preamble">%s</p>\n' % inline(sec["preamble"])) if sec["preamble"] else ""
        eh = []
        for e in sec["entries"]:
            eh.append(
"""    <article class="entry">
      <p class="entry-date">{date}</p>
      <h3 class="entry-title">{title}</h3>
      <div class="entry-fields">
{rows}
      </div>
    </article>""".format(date=inline(e["date"]), title=inline(e["title"]),
                         rows=field_rows(e["fields"])))
        out.append(
"""  <section class="year named-section" id="{sid}">
    <div class="year-head"><h2 class="named-h2">{name}</h2><span class="rivet-rule"></span>{tt}</div>
{pre}{entries}
  </section>""".format(sid=labels.get(name, (slug(name), None))[0], name=inline(name),
                       pre=pre, entries="\n".join(eh), tt=TOTOP))
    return "\n\n".join(out)

def marker_rows(items, kind, per=5):
    rows = []
    for i in range(0, len(items), per):
        inner = "\n".join("          " + sprites.marker(sid, lab, kind)
                          for sid, lab in items[i:i+per])
        rows.append('        <div class="flag-row">\n' + inner + '\n        </div>')
    return "\n".join(rows)

def render_banner(cfg):
    kind = "flag" if cfg["marking"] == "flags" else "insignia"
    return """  <section class="belligerents" aria-labelledby="bel-title">
    <div class="bel-inner">
      <div class="rivet-rule bel-eyebrow"></div>
      <p class="bel-title" id="bel-title">{bt}</p>
      <div class="bel-group">
        <p class="bel-side">Allied &amp; Co-Belligerent</p>
        <div class="flag-rows">
{a}
        </div>
      </div>
      <div class="bel-divider"></div>
      <div class="bel-group">
        <p class="bel-side">Axis &amp; Aligned</p>
        <div class="flag-rows">
{x}
        </div>
      </div>
      <p class="bel-note">{note}</p>
    </div>
  </section>""".format(bt=cfg["banner_title"], a=marker_rows(cfg["allied"], kind),
                       x=marker_rows(cfg["axis"], kind), note=cfg["banner_note"])

TOTOP = '<a class="totop" href="#top" aria-label="Back to top">&uarr; Top</a>'

# Operations series — order: European, Eastern (coming), Pacific, Med/ME, European Air.
THEATERS = [
    ("/operations/european-theater-1939-1945.html", "European Theater"),
    ("/operations/eastern-front-1938-1945.html", "Eastern Front"),
    ("/operations/pacific-theater-1941-1945.html", "Pacific Theater"),
    ("/operations/mediterranean-middle-east-1940-1945.html", "Mediterranean &amp; Middle East"),
    ("/operations/european-air-war-1939-1945.html", "European Air War"),
]

def render_topnav(active_file):
    items = []
    for href, label in THEATERS:
        if href is None:
            items.append('        <li><span class="soon">{} <em>Soon</em></span></li>'.format(label))
        else:
            cls = ' class="active"' if os.path.basename(href) == active_file else ""
            items.append('        <li><a href="{}"{}>{}</a></li>'.format(href, cls, label))
    return """  <nav aria-label="Primary navigation">
    <ul>
      <li><a href="/#services">Services</a></li>
      <li class="has-sub">
        <a href="/operations/european-theater-1939-1945.html" aria-haspopup="true">Operations</a>
        <ul class="subnav">
{theaters}
        </ul>
      </li>
      <li><a href="/dossiers/ju87-picchiatello.html">Dossiers</a></li>
      <li><a href="/#about">About</a></li>
      <li><a href="/#contact">Get in Touch</a></li>
    </ul>
  </nav>""".format(theaters="\n".join(items))

def render_framework(fw):
    if not fw: return ""
    return """
  <section class="cblock riveted" id="about">
    <span class="rvt tl"></span><span class="rvt tr"></span>
    <span class="rvt bl"></span><span class="rvt br"></span>
    <div class="cblock-head"><p class="cblock-kicker">About This Reference</p>{tt}</div>
    <div class="cblock-body">
{rows}
    </div>
  </section>""".format(rows=field_rows(fw), tt=TOTOP)

def render_addendum(ad):
    if not ad: return ""
    ads = ad if isinstance(ad, list) else [ad]
    out = []
    for i, a in enumerate(ads):
        aid = "addendum" if i == 0 else "addendum-%d" % (i + 1)
        out.append("""
  <section class="cblock riveted" id="{aid}">
    <span class="rvt tl"></span><span class="rvt tr"></span>
    <span class="rvt bl"></span><span class="rvt br"></span>
    <div class="cblock-head"><p class="cblock-kicker">Addendum</p>{tt}</div>
    <h2 class="cblock-title">{title}</h2>
    <div class="cblock-body">
{rows}
    </div>
  </section>""".format(aid=aid, title=inline(a["title"]), rows=field_rows(a["fields"]), tt=TOTOP))
    return "".join(out)

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css"),
           encoding="utf-8").read()

SHIELD = '''<svg class="shield" viewBox="0 0 120 144" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Heritage Fine Scale">
          <path d="M24,14 L96,14 L106,24 L106,72 C106,102 86,126 60,138 C34,126 14,102 14,72 L14,24 Z" fill="#16110A" stroke="#CFC4AA" stroke-width="1.4"/>
          <path d="M28,19 L92,19 L101,28 L101,71 C101,98 83,120 60,131 C37,120 19,98 19,71 L19,28 Z" fill="none" stroke="#CFC4AA" stroke-width="0.7" opacity="0.45"/>
          <text x="42" y="60" text-anchor="middle" font-family="'Barlow Condensed', sans-serif" font-weight="700" font-size="31" fill="#F2ECDF">H</text>
          <text x="60" y="83" text-anchor="middle" font-family="'Barlow Condensed', sans-serif" font-weight="700" font-size="31" fill="#F2ECDF">F</text>
          <text x="78" y="106" text-anchor="middle" font-family="'Barlow Condensed', sans-serif" font-weight="700" font-size="31" fill="#F2ECDF">S</text>
          <g fill="#6A2429"><circle cx="29" cy="21" r="2.3"/><circle cx="60" cy="19" r="2.3"/><circle cx="91" cy="21" r="2.3"/><circle cx="99" cy="50" r="2.3"/><circle cx="84" cy="104" r="2.3"/><circle cx="60" cy="127" r="2.3"/><circle cx="36" cy="104" r="2.3"/><circle cx="21" cy="50" r="2.3"/></g>
        </svg>'''

import re as _re
_DROP = _re.compile(
    r"(eastern front|\bl[123]\b|list [123]|when developed|out of scope per|"
    r"parent list|organi[sz]ational decision|formerly carried|now carried|"
    r"assembled from|belongs to the .*list|remain.* out of scope|these lists|this list)",
    _re.I)

def _clean_notes(notes):
    return [n for n in notes if not _DROP.search(n)]

def build(cfg):
    fm, years, year_order, notes, named, named_order = parse(cfg["md_text"])
    if not cfg.get("keep_notes"):
        notes = _clean_notes(notes)
    scope = cfg.get("scope") or fm
    scope_rows = "\n".join("        <dt>{}</dt><dd>{}</dd>".format(inline(k), inline(v))
                           for k, v in scope)
    sec_labels = cfg.get("section_labels") or {}
    labels = {}
    for name in named_order:
        labels[name] = sec_labels.get(name) or (slug(name), short_label(name))
    nav_named = "".join('<a href="#{0}">{1}</a>'.format(labels[n][0], labels[n][1])
                        for n in named_order)
    nav_years = "".join('<a href="#y{0}">{0}</a>'.format(y) for y in year_order)
    yearnav = ('<nav class="yearnav" aria-label="Section navigation">'
               '<a href="#about">About</a>' + nav_named + nav_years
               + ('<a href="#addendum">Addendum</a>' if cfg.get("addendum") else "")
               + ('<a href="#notes">Notes</a>' if notes else "")
               + '</nav>')
    notes_html = ""
    if notes:
        notes_items = "\n".join("      <li>{}</li>".format(inline(n)) for n in notes)
        notes_html = """
  <section class="notes" id="notes">
    <div class="year-head"><h2>Notes on Scope Edges</h2><span class="rivet-rule"></span>{tt}</div>
    <ul class="notes-list">
{items}
    </ul>
  </section>""".format(items=notes_items, tt=TOTOP)

    h1 = cfg["h1"]
    if cfg.get("years"):
        h1 = '{}<span class="h1-range">{}</span>'.format(h1, cfg["years"])

    page = PAGE.format(
        css=CSS, defs=sprites.defs_svg(), shield=SHIELD,
        topnav=render_topnav(os.path.basename(cfg["out"])),
        title=cfg["title"], meta_desc=cfg["meta_desc"],
        kicker=cfg["kicker"], h1=h1, deck=cfg["deck"],
        banner=render_banner(cfg), yearnav=yearnav,
        scope_rows=scope_rows, framework=render_framework(cfg.get("framework")),
        years=(render_named(named, named_order, labels) + ("\n\n" if named_order else "")
               + render_years(years, year_order)),
        addendum=render_addendum(cfg.get("addendum")), notes=notes_html)
    page = _re.sub(r'<use href="#([^"]+)"(?![^>]*xlink)',
                   r'<use href="#\1" xlink:href="#\1"', page)
    os.makedirs(os.path.dirname(cfg["out"]), exist_ok=True)
    open(cfg["out"], "w", encoding="utf-8").write(page)
    named_n = sum(len(named[n]["entries"]) for n in named_order)
    return {"out": cfg["out"], "years": {y: len(years[y]) for y in year_order},
            "named": {n: len(named[n]["entries"]) for n in named_order},
            "entries": sum(len(years[y]) for y in year_order) + named_n, "notes": len(notes)}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{meta_desc}" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#16110A" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;0,500;0,600;1,400&family=Barlow+Condensed:wght@400;500;600;700&family=Roboto+Condensed:ital,wght@0,400;0,500;0,600;0,700&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@400;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet" />
  <style>{css}</style>
</head>
<body>

{defs}

  <header class="riveted" id="top">
    <span class="rvt tl"></span><span class="rvt tr"></span>
    <span class="rvt bl"></span><span class="rvt br"></span>
    <div class="lockup">
      <a href="/" aria-label="Heritage Fine Scale home">
        {shield}
        <div class="lockup-text">
          <div class="wordmark">Heritage Fine Scale</div>
          <div class="rivet-rule wordmark-rule"></div>
          <div class="subline">Portland, Oregon &middot; U.S.A.</div>
        </div>
      </a>
    </div>
  </header>

{topnav}

  <main class="article intro">
    <p class="kicker">{kicker}</p>
    <h1>{h1}</h1>
    <p class="deck">{deck}</p>
  </main>

{banner}

  {yearnav}

  <main class="article">
    <div class="scope">
      <p class="scope-title">Scope &amp; Conventions</p>
      <dl>
{scope_rows}
      </dl>
    </div>
{framework}

{years}
{addendum}
{notes}
  </main>

  <a href="#top" class="to-top" id="toTop" aria-label="Back to top" title="Back to top">&uarr;</a>

  <footer>
    <p>&copy; 2026 Heritage Fine Scale &nbsp;&middot;&nbsp; Portland, Oregon</p>
  </footer>

  <script>
    (function () {{
      var b = document.getElementById('toTop');
      if (!b) return;
      var t = function () {{
        if (window.pageYOffset > 600) b.classList.add('show');
        else b.classList.remove('show');
      }};
      window.addEventListener('scroll', t, {{ passive: true }});
      t();
    }})();
  </script>

</body>
</html>
"""
