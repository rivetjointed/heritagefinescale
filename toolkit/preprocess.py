#!/usr/bin/env python3
"""Markdown preprocessing for HFS volumes — operates in markdown space,
then hands clean markdown to build.py.

Capabilities:
  parse_list(md)            -> structured dict
  emit_md(struct)           -> markdown (years + notes + frontmatter; no Framework)
  year_of(heading)          -> first 4-digit year (for bucketing)
  split_med(struct)         -> (european_struct, med_entries[list])
  fold_entries(struct, entries) -> struct with entries merged into year buckets
"""
import re
from collections import OrderedDict

def parse_list(md):
    lines = md.split("\n")
    h1 = ""; frontmatter = []; framework = None; fw_title = ""
    years = OrderedDict(); notes = []
    section = None; cur = None; in_fw = False
    def flush():
        nonlocal cur, framework
        if in_fw and cur is not None:
            framework = {"title": cur["heading"], "fields": cur["fields"]}
        elif cur is not None and section in years:
            years[section].append(cur)
        cur = None
    for ln in lines:
        s = ln.rstrip()
        if s.startswith("# ") and not s.startswith("## "):
            h1 = s[2:].strip(); continue
        if s.startswith("## "):
            flush()
            name = s[3:].strip(); section = name
            in_fw = (name == "Framework")
            if re.fullmatch(r"\d{4}", name) and name not in years:
                years[name] = []
            continue
        if s.startswith("### "):
            flush()
            heading = s[4:].strip()
            if in_fw:
                fw_title = heading; cur = {"heading": heading, "fields": []}
            elif section in years:
                cur = {"heading": heading, "fields": []}
            else:
                cur = {"heading": heading, "fields": []}
            continue
        m = re.match(r"^\*\*([^:]+):\*\*\s*(.*)$", s)
        if m:
            lab, val = m.group(1).strip(), m.group(2).strip()
            if in_fw and cur is not None:
                cur["fields"].append((lab, val))
            elif section is None or section in ("Table of Contents", "Scope"):
                frontmatter.append((lab, val))
            elif section in years and cur is not None:
                cur["fields"].append((lab, val))
            continue
        if section and section.startswith("Notes") and s.startswith("* "):
            notes.append(s[2:].strip()); continue
        if section and section.startswith("Notes") and s.strip() and notes:
            notes[-1] += " " + s.strip()
    flush()
    return {"h1": h1, "frontmatter": frontmatter, "framework": framework,
            "years": years, "notes": notes}

def year_of(heading):
    m = re.search(r"\b(19\d{2})\b", heading)
    return m.group(1) if m else "1940"

def emit_entry(e):
    out = ["### " + e["heading"]]
    for k, v in e["fields"]:
        out.append("**{}:** {}".format(k, v))
    return "\n".join(out)

def emit_md(struct):
    parts = ["# " + struct["h1"], ""]
    for k, v in struct["frontmatter"]:
        parts.append("**{}:** {}".format(k, v))
    parts.append("")
    for y in sorted(struct["years"].keys(), key=lambda x: int(x)):
        parts.append("## " + y); parts.append("")
        for e in struct["years"][y]:
            parts.append(emit_entry(e)); parts.append("")
    parts.append("## Notes on Scope Edges"); parts.append("")
    for n in struct["notes"]:
        parts.append("* " + n)
    return "\n".join(parts)

# Mediterranean / Middle East entries currently carried in the European list.
MED_TITLES = [
    "Mers-el-Kébir", "Operation Catapult", "Battle of Taranto", "Operation Compass",
    "SAS / LRDG Desert", "Greek Campaign", "Battle of Cape Matapan", "Siege of Tobruk",
    "Anglo-Iraqi War", "Battle of Crete", "Operation Exporter", "Operation Battleaxe",
    "Operation Countenance", "Operation Crusader", "Battle of Gazala",
    "First Battle of El Alamein", "Second Battle of El Alamein", "Capture of U-559",
    "Operation Torch", "Tunisian Campaign", "Operation Husky",
    "Italian Mainland Landings", "Dodecanese Campaign", "Volturno and Bernhardt",
    "Operation Shingle", "Battles of Monte Cassino", "Operation Diadem",
    "Operation Olive", "Operation Dragoon", "Liberation of Greece", "Operation Grapeshot",
]

def is_med(heading):
    return any(t in heading for t in MED_TITLES)

def split_med(struct):
    """Return (european_struct_without_med, list_of_med_entries_with_year)."""
    med = []
    for y, entries in struct["years"].items():
        keep = []
        for e in entries:
            if is_med(e["heading"]):
                med.append({"year": y, "entry": e})
            else:
                keep.append(e)
        struct["years"][y] = keep
    return struct, med

def fold_entries(struct, entries):
    """Merge a list of {'year':y,'entry':e} into struct's year buckets (front of year)."""
    for item in entries:
        y = item["year"]; e = item["entry"]
        if y not in struct["years"]:
            struct["years"][y] = []
        struct["years"][y].insert(0, e)
    return struct

def prewar_section_entries(prewar_md, section_substr):
    """Extract entries from a named '## Section ...' of the prewar addendum,
    bucketed by start-year, returns list of {'year','entry'}."""
    lines = prewar_md.split("\n")
    out = []; in_sec = False; cur = None
    def flush():
        nonlocal cur
        if cur is not None:
            out.append({"year": year_of(cur["heading"]), "entry": cur})
        cur = None
    for ln in lines:
        s = ln.rstrip()
        if s.startswith("## "):
            flush(); in_sec = section_substr in s; continue
        if not in_sec: continue
        if s.startswith("### "):
            flush(); cur = {"heading": s[4:].strip(), "fields": []}; continue
        m = re.match(r"^\*\*([^:]+):\*\*\s*(.*)$", s)
        if m and cur is not None:
            cur["fields"].append((m.group(1).strip(), m.group(2).strip()))
    flush()
    return out


# ---------- List-4 era helpers ----------
SERIES_REWRITES = [
    # most-specific first
    ("per L1/L2/L3 convention", "per the series convention"),
    ("the L1 precedent", "the European volume's precedent"),
    ("(cross-ref L1 Framework)", "(see the European volume's command addendum)"),
    ("Cross-ref L2 (\u201cJapanese Strategic Decision-Making and the Road to War\u201d framework)",
     "See the Pacific volume's strategic-decision addendum"),
    ('Cross-ref L2 ("Japanese Strategic Decision-Making and the Road to War" framework)',
     "See the Pacific volume's strategic-decision addendum"),
    ("Excludes Western Allied operations (L1/L3) and the Pacific War proper (L2)",
     "Excludes Western Allied operations (European and Air volumes) and the Pacific War proper (Pacific volume)"),
    ("Arctic convoys remain L1 per RN scope", "Arctic convoys remain in the European volume per RN scope"),
    ("RN operations per L1's naval scope", "RN operations per the European volume's naval scope"),
    ("without duplicating L1's convoy entries", "without duplicating the European volume's convoy entries"),
    ("the German air defense are L3's scope", "the German air defense are the Air volume's scope"),
    ("remains L1's Holocaust bracket", "remains the European volume's Holocaust bracket"),
    ("remain in L1 per the all-summits-in-one-document convention",
     "remain in the European volume per the all-summits-in-one-document convention"),
    ("The Winter War's Allied-planning dimension remains in L1",
     "The Winter War's Allied-planning dimension remains in the European volume"),
    ("L2 carries cross-references only", "the Pacific volume carries cross-references only"),
    ("same convention as Potsdam in L1", "same convention as Potsdam in the European volume"),
    ("the Pre-War Addendum's scope", "the European volume's pre-war section"),
    ("the Pre-War Addendum (M-R Pact entry)", "the European volume's pre-war section (M-R Pact entry)"),
    ("per the Addendum's explicit deferral", "per that section's explicit deferral"),
    ("the operations the Addendum deferred here", "the operations deferred here"),
    ("*Fall Weiss* (Addendum)", "*Fall Weiss* (European volume, pre-war section)"),
    ("the German campaign is the Pre-War Addendum's scope",
     "the German campaign is covered in the European volume's pre-war section"),
    ("per organizational decision", "by design"),
    ("per existing convention", "per the series convention"),
    ("the list reads incoherently", "the chronology reads incoherently"),
    ("per the list's spine", "per the volume's spine"),
    ("this list's", "this volume's"),
    ("this list", "this volume"),
    ("Cross-ref L2 (Endgame", "Cross-ref: Pacific volume (Endgame"),
    ("Cross-ref L2.", "Cross-ref: Pacific volume."),
    ("Allied intervention planning dimension in L1 (Winter War",
     "Allied intervention planning dimension in the European volume (Winter War"),
    ("the L1 Framework's rule", "the European volume command addendum's rule"),
    ("(L1 Framework)", "(European volume, command addendum)"),
    ("cross-ref L1, Sicily/Italian collapse", "cross-ref: Mediterranean volume, Sicily/Italian collapse"),
    ("(cross-ref L1)", "(cross-ref: European volume)"),
    ("(L1 cross-ref,", "(European volume cross-ref,"),
    ("(L3 cross-ref)", "(Air volume cross-ref)"),
    # bare fallbacks last
    ("(L1)", "(European volume)"),
    ("(L2)", "(Pacific volume)"),
    ("(L3)", "(Air volume)"),
    ("L1's", "the European volume's"),
    ("L2's", "the Pacific volume's"),
    ("L3's", "the Air volume's"),
]

def rewrite_series_refs(md):
    """Map internal L1/L2/L3 list nomenclature to public theater-volume names."""
    for a, b in SERIES_REWRITES:
        md = md.replace(a, b)
    return md

def leftover_series_refs(md):
    return re.findall(r"[^\w]L[123][^\w]", md)

def extract_framework_blocks(md):
    """Pull '## Framework — Title' blocks (fields directly under ##, no ###).
    Returns (md_without_blocks, [{'title','fields'}...])."""
    lines = md.split("\n")
    out_lines, blocks, cur = [], [], None
    for ln in lines:
        s = ln.rstrip()
        if s.startswith("## Framework"):
            title = s[3:].strip()
            if " \u2014 " in title:
                title = title.split(" \u2014 ", 1)[1]
            elif " — " in title:
                title = title.split(" — ", 1)[1]
            cur = {"title": title, "fields": []}
            blocks.append(cur)
            continue
        if s.startswith("## ") and cur is not None:
            cur = None
            out_lines.append(ln); continue
        if cur is not None:
            m = re.match(r"^\*\*([^:]+):\*\*\s*(.*)$", s)
            if m:
                cur["fields"].append((m.group(1).strip(), m.group(2).strip()))
            continue
        out_lines.append(ln)
    return "\n".join(out_lines), blocks
