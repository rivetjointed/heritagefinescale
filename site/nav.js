/* ============================================================================
   Heritage Fine Scale — site navigation, single source of truth.
   Injects the primary nav into <div id="site-nav"></div> on every page.

   STYLES TRAVEL WITH THE NAV: this file also injects a <style> block
   (NAV_CSS below) appended to <head>, so it cascades after each page's
   baked-in stylesheet and wins ties. Pages built against older copies of
   style.css can never strand the nav again. Edit nav styling HERE, not in
   style.css.

   TO ADD A PAGE: add one entry to OPERATIONS (a theater volume), REFERENCE
   (a reference page), DOSSIERS (a long-form brief), or TOP (a top-level
   item). Nothing else, anywhere, needs to change — toolkit/build.py renders
   an empty <div id="site-nav"></div> and leaves the nav to this file.

   Active state is derived from the current path, so pages never hard-code it.
   On the homepage, section links stay as bare #anchors; elsewhere they point
   back to /#anchor.
   ============================================================================ */
(function () {
  "use strict";

  // ---- Nav stylesheet (canonical; formerly the nav block of style.css) -------
  var NAV_CSS = '' +
    'nav { background-color: var(--ink-mid); border-bottom: 1px solid var(--field); }\n' +
    'nav ul { list-style: none; display: flex; justify-content: center; flex-wrap: wrap; max-width: 900px; margin: 0 auto; }\n' +
    'nav ul li a {\n' +
    '  display: block; padding: 0.8rem 1.6rem; color: var(--bone); text-decoration: none;\n' +
    "  font-family: 'Barlow Condensed', 'Roboto Condensed', 'Noto Sans JP', sans-serif; font-weight: 500; font-size: 0.84rem;\n" +
    '  letter-spacing: 0.2em; text-transform: uppercase; transition: background 0.18s, color 0.18s;\n' +
    '}\n' +
    'nav ul li a:hover, nav ul li a.active { background-color: var(--field); color: #fff; }\n' +
    '\n' +
    '/* Dropdowns (Operations / Reference) */\n' +
    'nav ul li.has-sub { position: relative; }\n' +
    'nav ul li.has-sub > a::after { content: " \\25BE"; font-size: 0.72em; opacity: 0.65; }\n' +
    'nav .subnav {\n' +
    '  display: none; position: absolute; left: 0; top: 100%; z-index: 50;\n' +
    '  flex-direction: column; min-width: 230px; max-width: none; margin: 0;\n' +
    '  background: var(--field); border: 1px solid var(--ink);\n' +
    '  box-shadow: 0 8px 22px rgba(0,0,0,0.35);\n' +
    '}\n' +
    'nav ul li.has-sub:hover .subnav,\n' +
    'nav ul li.has-sub:focus-within .subnav { display: flex; }\n' +
    'nav .subnav li a {\n' +
    '  padding: 0.6rem 1.2rem; font-size: 0.76rem; letter-spacing: 0.14em; white-space: nowrap;\n' +
    '}\n' +
    'nav .subnav li a:hover, nav .subnav li a.active { background: var(--ink-mid); color: #fff; }\n' +
    'nav .subnav li .soon {\n' +
    "  display: block; padding: 0.6rem 1.2rem; font-family: 'Barlow Condensed', 'Roboto Condensed', 'Noto Sans JP', sans-serif;\n" +
    '  font-weight: 500; font-size: 0.76rem; letter-spacing: 0.14em; text-transform: uppercase;\n' +
    '  color: var(--ink-light); white-space: nowrap;\n' +
    '}\n' +
    'nav .subnav li .soon em {\n' +
    '  font-style: normal; color: var(--oxblood); margin-left: 0.45rem; font-size: 0.82em;\n' +
    '  letter-spacing: 0.1em;\n' +
    '}\n' +
    '\n' +
    '/* Section headers inside a dropdown (e.g. Charts) */\n' +
    'nav .subnav li.subnav-head {\n' +
    "  padding: 0.55rem 1.2rem 0.3rem; font-family: 'Barlow Condensed', 'Roboto Condensed', 'Noto Sans JP', sans-serif;\n" +
    '  font-weight: 600; font-size: 0.64rem; letter-spacing: 0.22em; text-transform: uppercase;\n' +
    '  color: var(--ink-light); white-space: nowrap; pointer-events: none;\n' +
    '}\n' +
    'nav .subnav li.subnav-head:not(:first-child) {\n' +
    '  margin-top: 0.3rem; border-top: 1px solid rgba(196,184,154,0.18);\n' +
    '}\n' +
    '\n' +
    '@media (max-width: 600px) {\n' +
    '  nav ul li a { padding: 0.7rem 1rem; font-size: 0.76rem; }\n' +
    '}\n';

  // ---- Operations dropdown (theater volumes), in series order ----------------
  var OPERATIONS = [
    { href: "/operations/european-theater-1939-1945.html",          label: "European Theater" },
    { href: "/operations/eastern-front-1938-1945.html",             label: "Eastern Front" },
    { href: "/operations/pacific-theater-1941-1945.html",           label: "Pacific Theater" },
    { href: "/operations/mediterranean-middle-east-1940-1945.html", label: "Mediterranean &amp; Middle East" },
    { href: "/operations/european-air-war-1939-1945.html",          label: "European Air War" }
  ];

  // First operations link doubles as the Operations parent target.
  var OPERATIONS_PARENT = OPERATIONS[0].href;

  // ---- Reference dropdown ----------------------------------------------------
  // Items with `group` render as a non-link section header inside the dropdown.
  var REFERENCE = [
    { group: "Charts" },
    { href: "/reference/aircraft-production.html", label: "Aircraft Production" },
    { href: "/reference/armor-production.html",    label: "Armor Production" },
    { href: "/reference/naval-tonnage.html",       label: "Naval Tonnage" },
    { group: "Terms &amp; Sources" },
    { href: "/reference/glossary.html",            label: "Glossary" },
    { href: "/reference/bibliography.html",        label: "Bibliography" }
  ];

  // First reference link doubles as the Reference parent target.
  var REFERENCE_PARENT = REFERENCE.filter(function (o) { return o.href; })[0].href;

  // ---- Dossiers dropdown (long-form briefs), in series order -----------------
  // Labelled by subject, matching the filename — not by the brief's title.
  var DOSSIERS = [
    { href: "/dossiers/ju87-picchiatello.html",        label: "Ju 87 Picchiatello" },
    { href: "/dossiers/your-cooking-is-the-best.html", label: "Your Cooking Is The Best" }
  ];

  // First dossier link doubles as the Dossiers parent target.
  var DOSSIERS_PARENT = DOSSIERS[0].href;

  // ---- Top-level items. `anchor` => homepage section link --------------------
  var TOP = [
    { kind: "anchor", frag: "services", label: "Services" },
    { kind: "ops",    label: "Operations" },
    { kind: "ref",    label: "Reference" },
    { kind: "dsr",    label: "Dossiers" },
    { kind: "anchor", frag: "about",    label: "About" },
    { kind: "anchor", frag: "contact",  label: "Get in Touch" }
  ];

  // ---- Path helpers ----------------------------------------------------------
  var path = window.location.pathname.replace(/index\.html$/, "").replace(/\/$/, "");
  if (path === "") path = "/";
  var onHome = (path === "/");

  function norm(href) { return href.replace(/index\.html$/, "").replace(/\/$/, "") || "/"; }
  function isActive(href) { return norm(href) === path; }
  function anchorHref(frag) { return onHome ? ("#" + frag) : ("/#" + frag); }

  // Is any item within a dropdown the current page? (drives parent active state)
  var opsActive = OPERATIONS.some(function (o) { return isActive(o.href); });
  var refActive = REFERENCE.some(function (o) { return o.href && isActive(o.href); });
  var dsrActive = DOSSIERS.some(function (o) { return isActive(o.href); });

  // ---- Build markup ----------------------------------------------------------
  function li(href, label, active) {
    return '<li><a href="' + href + '"' + (active ? ' class="active"' : '') + '>' + label + '</a></li>';
  }

  function dropdownItem(label, parentHref, list, active) {
    var sub = list.map(function (o) {
      if (o.group) return '          <li class="subnav-head">' + o.group + '</li>';
      return '          ' + li(o.href, o.label, isActive(o.href));
    }).join("\n");
    return '' +
      '      <li class="has-sub">\n' +
      '        <a href="' + parentHref + '"' + (active ? ' class="active"' : '') +
      ' aria-haspopup="true">' + label + '</a>\n' +
      '        <ul class="subnav">\n' + sub + '\n' +
      '        </ul>\n' +
      '      </li>';
  }

  var items = TOP.map(function (it) {
    if (it.kind === "ops")    return dropdownItem("Operations", OPERATIONS_PARENT, OPERATIONS, opsActive);
    if (it.kind === "ref")    return dropdownItem("Reference", REFERENCE_PARENT, REFERENCE, refActive);
    if (it.kind === "dsr")    return dropdownItem("Dossiers", DOSSIERS_PARENT, DOSSIERS, dsrActive);
    if (it.kind === "anchor") return '      ' + li(anchorHref(it.frag), it.label, false);
    return '      ' + li(it.href, it.label, isActive(it.href));
  }).join("\n");

  var html =
    '  <nav aria-label="Primary navigation">\n' +
    '    <ul>\n' + items + '\n' +
    '    </ul>\n' +
    '  </nav>';

  // ---- Inject ----------------------------------------------------------------
  function injectStyles() {
    if (document.getElementById("hfs-nav-style")) return; // idempotent
    var s = document.createElement("style");
    s.id = "hfs-nav-style";
    s.textContent = NAV_CSS;
    document.head.appendChild(s); // appended last in <head> => wins cascade ties
  }

  function mount() {
    injectStyles();
    var slot = document.getElementById("site-nav");
    if (slot) slot.outerHTML = html;
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
