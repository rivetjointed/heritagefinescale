# Heritage Fine Scale — Operations Reference Volumes · Handoff Brief

Purpose: a reusable toolkit that turns WWII operational-history markdown lists into
branded static HTML reference pages for the HFS site, in the established documentation
aesthetic (cream/parchment, oxblood rivets, Barlow Condensed + Source Serif 4, shield
lockup, dark belligerent banner, sticky section nav).

---

## What exists now (delivered, downloadable)

Four generated volumes + one QA asset:
- `european-theater-1939-1945.html` — 71 entries (Mediterranean stripped out, pre-war folded in)
- `pacific-theater-1941-1945.html` — 52 entries
- `mediterranean-middle-east-1940-1945.html` — 44 entries (30 ground/naval pulled from European + 14 air-addendum)
- `european-air-war-1939-1945.html` — 68 entries (insignia banner, not flags)
- `hfs-marking-library.png` — contact sheet of all 38 markings

## The toolkit (THE durable asset — was in /home/claude/, now exported here)

Re-upload these into the project to resume. Roles:
- `sprites.py` — master marking library. 38 SVG symbols = 27 national flags + 7 air
  insignia. API: `SPRITE_DEFS`, `FLAGS_ALL`, `INSIGNIA_ALL`, `defs_svg()`,
  `marker(id,label,kind)`, `sheet_svg()`. Flags viewBox 60x40; insignia 40x40.
  Conventions: Germany = Balkenkreuz; Japan = wartime naval ensign (rising sun);
  Canada = Red Ensign; South Africa = oranje-blanje-blou; Free France = Cross of Lorraine.
- `build.py` — config-driven page generator. `build(cfg)` parses markdown, renders
  banner (rows of 5) / framework / years / addendum / notes, writes HTML. Supports
  `marking="flags"|"insignia"`. Holds the page template, the dynamic top-nav
  (Operations dropdown w/ active-state), and a `_DROP` regex that filters internal
  housekeeping notes.
- `style.css` — shared stylesheet (single source of truth for branding).
- `preprocess.py` — markdown-space ops: `parse_list`, `emit_md`, `split_med`
  (uses `MED_TITLES` deny-list), `fold_entries`, `prewar_section_entries`.
- `make_all.py` — driver. Holds per-volume configs (FW framework text, SCOPE, BANNERS,
  META), orchestrates the Med-split + prewar-fold, and renders all four pages + sheet.

To regenerate everything: re-upload the five toolkit files + the source markdowns, then
run `python3 make_all.py`. Requires `cairosvg` (sprite-sheet PNG) and, for QA renders,
`wkhtmltoimage` (note its 32767px height cap on tall pages — not an HTML bug).

## Source inputs (your uploads — keep them)

- `WWII-List1-Europe-Ground-Naval.md` — European ground + Atlantic/Med naval (89 entries; Med gets split out)
- `WWII-List2-Pacific.md` — Pacific (53 incl. the Japanese-decision framework block)
- `WWII-List3-Europe-Air_1.md` — European air (62; no framework section)
- `WWII-List3-Mediterranean-Middle-East-Addendum.md` — Med/ME AIR ops addendum (14)
- `WWII-PreWar-EarlyWar-Addendum.md` — pre-sectioned: Section 1 → European, Section 3 → Air; Section 2 (Pacific) empty

---

## Decisions locked this session

- Volume series order: European / Eastern (to come) / Pacific / Mediterranean & Middle East / European Air.
- Med overlap: truly Med/ME entries stripped from European and folded into the Med volume (deny-list in `preprocess.MED_TITLES`). Dragoon classed as Med to match the air addendum.
- Med volume = Med ground/naval (from European) + Med air addendum, merged by year; flags banner.
- Air volume uses air-arm INSIGNIA, not flags.
- Japan rendered as the wartime naval ensign (accepted; unlike the hakenkreuz).
- Source "## Framework" context blocks (German High Command; Japanese decision-making) are NOT the page framework — relocated to a bottom "Addendum" before Notes. The top block is "About This Reference" with fields Framework / Structure / Doctrine / Operational Outcomes.
- Internal housekeeping removed from site copy: no "Eastern Front (to come)", "one of a set", cross-volume "carried in / cross-referenced", or "per L1's convention". Genuine *historical* Eastern Front mentions kept.
- Banner flags break into rows of 5 max.
- Title year-range drops to its own line at full title size.
- Intro (title/kicker/deck) block buffer halved.
- Section nav is sticky; "About" label (not "Framework"); each year/Addendum/Notes head has an "↑ Top" link; a floating back-to-top button fades in after scroll.
- Top nav carries an Operations dropdown (5 theaters, current page highlighted, Eastern Front shown as "Soon"). Theater links are RELATIVE — the four pages must deploy in the same directory.

## Master marking library — 38 symbols

Flags (id): us uk ca au nz in za fr pl cz no gr be nl su de it vichy jp cn th ph iq ir fi ro hu
Insignia (id): ins-us ins-raf ins-soviet ins-luftwaffe ins-regia ins-polish ins-ff
(fi/ro/hu already drawn for the Eastern Front; Slovakia, Croatia, Yugoslavia not yet.)

---

## Pending / next

- Eastern Front volume — awaiting source data (your usage trigger). Will pull Soviet + German + co-belligerents (Finland/Romania/Hungary done; Slovakia/Croatia/Yugoslavia to draw) and the 1945 Manchurian campaign. New config block in `make_all.py` + its markdown; toolkit otherwise ready.
- `index.html` — untouched. You are wiring the Operations nav + the flag swap (replacing the simple insignia on the home page and dossier pages with the master flag/insignia set) on your own pass. The `<nav>` markup the four reference pages now carry is the block to mirror onto the home page.
- Deployment: confirm the four pages live in one directory so the relative Operations links resolve.
