# Heritage Fine Scale

Client site, live at **heritagefinescale.com**. Research and build reference for scale
modelers: WWII operational history, dossiers on individual subjects, and reference tables.
Built and maintained by Linden Street Studio.

Plain static HTML and CSS, no framework. `site/` is the publish directory
(`netlify.toml`), so nothing outside it ever ships, this file included. The only generated
pages are the operations volumes (see below). Tooling in `toolkit/` is Python.

The studio's house rules live at
`C:\Work\Business\Linden Street Studio LLC\04-playbooks\production-standards.md`, and the
studio-wide client-site rules (attribution credit, shared carousel, audit) are in
`C:\Work\Sites\linden\CLAUDE.md`. Read those rather than re-deciding a rule here.

## Deploying

Netlify project `snazzy-eclair-186bcf`, production branch `master`, remote
`github.com/rivetjointed/heritagefinescale`. **Treat a push to `master` as a deploy and ask
before pushing.**

Check `git branch -vv` before assuming what is live. Work in progress sits on its own
branch: Dossier No. 003 (the Ducceschi pair) was merged to `master` and reverted on
2026-09-08, and continues on `dossier-003` while the family reviews it.

Gate before anything goes live or to the client:

```bash
python C:\Work\Sites\linden\tools\site-audit.py site
```

Client mode, every `.html` under `site/`. It exits 1 on any ERROR.

The contact form on `index.html` is a Netlify form (`name="contact"`) that posts to
`/success`. `success.html` is noindexed.

## Navigation

`site/nav.js` is the single source of truth for the primary nav **and its CSS**. Pages
carry an empty `<div id="site-nav"></div>` and the script fills it. To add a page, add one
entry to `OPERATIONS`, `REFERENCE`, `DOSSIERS` or `TOP` in that file; its header documents
the structure. Never hard-code a nav into a page, and edit nav styling in `nav.js`, not
`style.css`.

## Operations volumes are generated

The five theater pages in `site/operations/` come from `toolkit/make_all.py`. **Never
hand-edit them.** Prose belongs in the source lists; a hand edit is silently overwritten
the next time anyone runs `--write`.

```bash
python toolkit/make_all.py           # build to toolkit/_rebuild/ and report drift from live
python toolkit/make_all.py --write   # overwrite site/operations/
```

The default run is the regression test: a rebuild is meant to be a no-op, so read its
drift report before ever passing `--write`. The docstrings in `make_all.py` and `build.py`
explain what is load-bearing.

**Broken as of 2026-09-27.** The script reads its sources from `other/`, which does not
exist. The lists now sit in `toolkit/sources/` (untracked, dated 2026-09-16), and one name
differs: the script wants `WWII-List3-Europe-Air_1.md`, the folder has
`WWII-List3-Europe-Air.md`. Do not simply repoint it: first confirm those lists still
rebuild the published pages with no drift. Fix this before touching the operations pages.

The operations volumes use British spelling on purpose (programme, armoured, theatre,
-ise endings). Those were judgement calls lifted into the sources. Do not Americanise them.

`toolkit/HFS-operations-reference-HANDOFF.md` and `toolkit/toolkit.txt` are history from
when the toolkit lived in a chat sandbox. They predate the Eastern Front volume and name
paths that no longer exist. Read them for background, not instructions.

## Dossiers

Long-form pages in `site/dossiers/`, styled by `dossier.css`. Pages that a family has not
yet cleared for publication carry `noindex`; delete the meta when they go public.

The Ducceschi pair is reviewed on the studio's preview portal. `toolkit/export-preview.py`
regenerates the self-contained copies in
`C:\Work\Sites\linden\preview\heritage-fine-scale\`. Edit the pages here and re-run it;
never edit the preview copies by hand.

## Unlisted pages

`sourdough/` and `ham-and-bean-soup/` are personal hobby pages: unlisted, noindexed, and
disallowed for most crawlers in `robots.txt` (ClaudeBot is deliberately allowed). Neither
is linked from the nav or the homepage; keep it that way.

The sourdough page keeps its own carousel. That is a sanctioned exception to the studio's
shared carousel (reasons in `linden/CLAUDE.md`). The dossier pages also carry their own
lightbox markup. Do not convert either to the shared carousel without asking.

## Attribution credit

Every page carries the Linden Street Studio footer credit, except `ham-and-bean-soup/`
(as of 2026-09-27; not recorded whether that is deliberate). Its canonical source is
`C:\Work\Sites\linden\tools\attribution.py`, and its CSS lives in `site/style.css`.
`toolkit/build.py` inlines a byte-identical copy because it cannot import across repos: if
the credit changes in `attribution.py`, change it in `build.py` too, or every rebuild
produces a diff.

## This file

Lives at the repo root, outside `site/`, so it never deploys. The root `.gitignore` is a
whitelist; `!/CLAUDE.md` is what lets this file be tracked.
