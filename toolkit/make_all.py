#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "hfs")
import build, preprocess as pp
from collections import OrderedDict

U = "/mnt/user-data/uploads/"
OUT = "/mnt/user-data/outputs/operations/"
read = lambda p: open(p, encoding="utf-8").read()

# ---------- shared framework prose ----------
def structure(_=None):
    return ("Entries are grouped by calendar year and ordered by date of first major action; "
            "multi-year efforts are bracketed at their opening as campaign or programme brackets. "
            "Each entry follows the same three-field anatomy — Forces, Intent, Outcome — the skeleton "
            "the dossiers use, so the reference and the long-form briefs read in one register. Allied "
            "codenames carry the entry title; Axis codenames are set in italic where the scholarship "
            "attests them.")

def doctrine(_=None):
    return ("Inclusion is by consequence, not by drama: an action earns an entry if it changed the "
            "shape of the theater, whether or not it is famous. The through-line is the house argument "
            "— the gap between what gets remembered and what actually mattered — applied at theater "
            "scale. Treatment is evenhanded; Axis intent and outcome are stated as the Axis command "
            "understood them. Scope edges are deliberate: operations outside this theater appear only "
            "where they touch it directly.")

FW = {}
FW["european"] = [
("Framework", "This is the Western European and Atlantic volume of Heritage Fine Scale's operational reference: a chronological index of the campaigns, raids, programmes, and summits that set the shape of the war in Western Europe and on the Atlantic, from the diplomatic rupture of March 1939 to the German surrender in May 1945. It is a reference, not a narrative — entries are sorted by start date and stated in the terms an operation was planned and judged in, so a builder can place a subject in the actual record rather than in the box-art summary."),
 ("Structure", structure()),
 ("Doctrine", doctrine()),
 ("Operational Outcomes", "Read in order, the theater resolves into a recognizable shape. 1939 is the rupture and the Phoney War. 1940 is collapse and survival — Norway, France, Dunkirk, and the first blows struck to stay in the war at all. 1941 through 1943 is the stretch popular memory skips: the war was not held or lost on a beach but on the convoy routes, where the Atlantic was kept by inches while the cross-Channel force was built. 1944 is the return and the decisive year — Normandy, the breakout, the pursuit, and the costly autumn behind it. 1945 is the close, run at speed across the Rhine to surrender. For the modeler, that arc is the point: it tells you what a subject was actually doing in the war, the first thing an authentic build has to get right and the last thing the box will tell you."),
]
FW["pacific"] = [
("Framework", "This is the Pacific volume of Heritage Fine Scale's operational reference: a chronological index of the naval, air, and amphibious land operations of the Pacific and South-West Pacific, from Pearl Harbor in December 1941 to the surrender in Tokyo Bay in September 1945. It is a reference, not a narrative — entries are sorted by start date and stated in the terms an operation was planned and judged in."),
 ("Structure", structure()),
 ("Doctrine", doctrine()),
 ("Operational Outcomes", "Read in order, the theater resolves into a recognizable shape. 1941–42 is Japanese expansion and a run of Allied catastrophes — the Philippines, Malaya, the East Indies — checked at the Coral Sea and broken at Midway, the hinge of the whole war. 1942–43 is the attritional grind of Guadalcanal and New Guinea, where the initiative changed hands for good. 1943–44 is the two-axis advance — the Central Pacific island chain and MacArthur's South-West Pacific drive — converging on the Marianas and Leyte, where the Imperial Navy was destroyed as a fighting force. 1945 is the close at Iwo Jima and Okinawa, the bombing and blockade of the Home Islands, and the surrender. For the modeler, that arc places a subject in the war rather than on a shelf."),
]
FW["med"] = [
("Framework", "This is the Mediterranean and Middle East volume of Heritage Fine Scale's operational reference: the ground, naval, and air campaigns of the inland sea and its approaches — North Africa and the Western Desert, Malta and the convoy war, Greece, Crete, the Dodecanese, the Levant, Iraq and Iran, Sicily and the long Italian campaign — from 1940 to 1945. It is a reference, not a narrative; entries are sorted by start date and stated in the terms an operation was planned and judged in."),
 ("Structure", structure()),
 ("Doctrine", doctrine() + " This is the theater where Allied tactical air doctrine was forged and where the ‘periphery’ argument is most directly tested."),
 ("Operational Outcomes", "Read in order, the theater resolves into a recognizable shape. 1940 is Italian overreach and the first lopsided British victories in the desert and at Taranto. 1941 is the German intervention that changed the math — the loss of Greece and Crete, the arrival of the Afrikakorps, and the see-saw fighting in Cyrenaica. 1942 is the crisis at Gazala and Tobruk and the turn at El Alamein, then the clearing of Africa and the move to Sicily. 1943 through 1945 is the grinding Italian campaign — Salerno, Anzio, Cassino, the Gothic Line — that tied down German divisions to the end while the decision moved north. For the modeler, that arc explains why a desert or Italian-front subject looks and fought the way it did."),
]
FW["air"] = [
("Framework", "This is the European air-war volume of Heritage Fine Scale's operational reference: the strategic bombing offensive, the air-defense battles, tactical and maritime air, and the airborne lifts over Western Europe, from the opening sorties of 1939 to the final offensives of 1945. It is a reference, not a narrative. Markings here are shown as air-arm insignia rather than national flags — the air war's native idiom."),
 ("Structure", structure()),
 ("Doctrine", doctrine() + " The bomber-offensive argument — area against precision, and the cost of both — is treated evenhandedly."),
 ("Operational Outcomes", "Read in order, the campaign resolves into a recognizable shape. 1939–40 is the early probing and the Battle of Britain, the first defensive victory of the war. 1941–42 is the turn to night area bombing and the long build-up of force. 1943 is Pointblank and the crisis of unescorted daylight bombing, paid for over Schweinfurt and Regensburg. 1944 is the arrival of the long-range escort, air supremacy won before Overlord, and the tactical air war that followed the armies across France. 1945 is the final offensives against a collapsing defense. For the modeler, that arc fixes what a given airframe was doing, in what company, and against what."),
]

# ---------- per-volume configs ----------
def cfg_common(marking):
    return {"marking": marking}

SCOPE = {
 "european": [
   ("Scope", "US / UK / Commonwealth and Allied (Polish, Free French, Norwegian, Belgian, Dutch, Czechoslovak) formations in Western Europe and on the Atlantic — ground campaigns and naval operations."),
   ("Period", "March 1939 – May 1945."),
   ("Sort", "By start date; range shown in each entry. Multi-year campaigns bracketed at their first major action."),
   ("Codenames", "Allied codenames in entry titles; Axis codenames italicized where commonly attested."),
 ],
 "pacific": [
   ("Scope", "Naval, air, and amphibious land operations across the Pacific and South-West Pacific, from the central ocean to the approaches to the Home Islands."),
   ("Period", "December 1941 – September 1945."),
   ("Sort", "By start date; range shown in each entry. Multi-year campaigns bracketed at their first major action."),
   ("Codenames", "Allied codenames in entry titles; Axis codenames italicized where commonly attested."),
 ],
 "med": [
   ("Scope", "The Mediterranean Theater (MTO), the Middle East Command theater, and the North African campaigns — ground, naval, and air operations."),
   ("Period", "June 1940 – May 1945."),
   ("Sort", "By start date; range shown in each entry."),
   ("Codenames", "Allied codenames in entry titles; Axis codenames italicized where commonly attested."),
 ],
 "air": [
   ("Scope", "Air operations over Western Europe — strategic bombing, air defense, tactical and maritime air, and the airborne lifts."),
   ("Period", "September 1939 – May 1945."),
   ("Sort", "By start date; range shown in each entry."),
   ("Codenames", "Allied codenames in entry titles; Axis codenames italicized where commonly attested."),
 ],
}

BANNERS = {
 "european": dict(
   banner_title="Belligerents — Western Europe &amp; the Atlantic",
   banner_note="National markings shown schematically; the German marking follows the period military cross used across this site rather than the era's national flag.",
   allied=[("us","United States"),("uk","United Kingdom"),("ca","Canada"),("fr","Free France"),
           ("pl","Poland"),("no","Norway"),("be","Belgium"),("nl","Netherlands"),
           ("cz","Czechoslovakia"),("su","Soviet Union")],
   axis=[("de","Germany")]),
 "pacific": dict(
   banner_title="Belligerents — Pacific &amp; South-West Pacific",
   banner_note="National markings shown schematically; Japan is shown by the wartime naval ensign.",
   allied=[("us","United States"),("uk","United Kingdom"),("ca","Canada"),("au","Australia"),
           ("nz","New Zealand"),("in","British India"),("nl","Netherlands"),("cn","China"),
           ("ph","Philippines"),("su","Soviet Union")],
   axis=[("jp","Japan"),("th","Thailand")]),
 "med": dict(
   banner_title="Belligerents — Mediterranean &amp; Middle East",
   banner_note="National markings shown schematically; the German marking follows the period military cross. Iraq and Iran appear as the venues of the 1941 Levant and Persian-corridor actions rather than as Axis members.",
   allied=[("us","United States"),("uk","United Kingdom"),("au","Australia"),("nz","New Zealand"),
           ("in","British India"),("za","South Africa"),("fr","Free France"),("pl","Poland"),
           ("gr","Greece")],
   axis=[("de","Germany"),("it","Italy"),("vichy","France (Vichy)"),("iq","Iraq"),("ir","Iran")]),
 "air": dict(
   banner_title="Air Arms — European Theater",
   banner_note="Air-arm insignia shown schematically; Commonwealth air forces (RCAF, RAAF, RNZAF, SAAF) and the Fleet Air Arm flew under the RAF roundel. The Luftwaffe marking is the period military cross.",
   allied=[("ins-us","USAAF"),("ins-raf","RAF / Commonwealth"),("ins-ff","Free French"),
           ("ins-polish","Polish Air Force"),("ins-soviet","Soviet VVS")],
   axis=[("ins-luftwaffe","Luftwaffe"),("ins-regia","Regia Aeronautica")]),
}

META = {
 "european": dict(kicker="Operations Reference &middot; European Theater",
   h1="Western Europe &amp; the Atlantic", years="1939&ndash;1945",
   deck="Ground campaigns and Atlantic naval operations &mdash; the operational record a build's subject is drawn from. Each entry gives forces, intent, and outcome.",
   title="Western Europe &amp; the Atlantic, 1939&ndash;1945 &mdash; Operations Reference &mdash; Heritage Fine Scale",
   meta_desc="A curated operational reference for Western Europe and the Atlantic, 1939-1945: ground campaigns and naval operations with forces, intent, and outcome for each. Heritage Fine Scale.",
   out=OUT+"european-theater-1939-1945.html"),
 "pacific": dict(kicker="Operations Reference &middot; Pacific Theater",
   h1="The Pacific War", years="1941&ndash;1945",
   deck="Naval, air, and amphibious land operations from Pearl Harbor to Tokyo Bay. Each entry gives forces, intent, and outcome.",
   title="The Pacific War, 1941&ndash;1945 &mdash; Operations Reference &mdash; Heritage Fine Scale",
   meta_desc="A curated operational reference for the Pacific War, 1941-1945: naval, air, and amphibious operations with forces, intent, and outcome. Heritage Fine Scale.",
   out=OUT+"pacific-theater-1941-1945.html"),
 "med": dict(kicker="Operations Reference &middot; Mediterranean &amp; Middle East",
   h1="The Mediterranean &amp; Middle East", years="1940&ndash;1945",
   deck="The desert, the inland sea, and the long Italian campaign &mdash; ground, naval, and air operations. Each entry gives forces, intent, and outcome.",
   title="The Mediterranean &amp; Middle East, 1940&ndash;1945 &mdash; Operations Reference &mdash; Heritage Fine Scale",
   meta_desc="A curated operational reference for the Mediterranean and Middle East, 1940-1945: ground, naval, and air operations with forces, intent, and outcome. Heritage Fine Scale.",
   out=OUT+"mediterranean-middle-east-1940-1945.html"),
 "air": dict(kicker="Operations Reference &middot; European Air War",
   h1="The Air War over Europe", years="1939&ndash;1945",
   deck="Strategic bombing, air defense, tactical and maritime air, and the airborne lifts. Each entry gives forces, intent, and outcome.",
   title="The Air War over Europe, 1939&ndash;1945 &mdash; Operations Reference &mdash; Heritage Fine Scale",
   meta_desc="A curated operational reference for the air war over Europe, 1939-1945: strategic bombing, air defense, tactical air, and airborne operations. Heritage Fine Scale.",
   out=OUT+"european-air-war-1939-1945.html"),
}

def make_cfg(key, marking, md_text, framework, addendum=None, scope=None):
    c = dict(META[key]); c.update(BANNERS[key])
    c["marking"] = marking; c["md_text"] = md_text
    c["framework"] = framework; c["addendum"] = addendum
    c["scope"] = scope
    return c

results = {}

# ===== EUROPEAN =====
l1 = pp.parse_list(read(U+"WWII-List1-Europe-Ground-Naval.md"))
eu_addendum = {"title": l1["framework"]["title"].split(" — ",1)[-1],
               "fields": l1["framework"]["fields"]} if l1["framework"] else None
eu, med_entries = pp.split_med(l1)
prewar = read(U+"WWII-PreWar-EarlyWar-Addendum.md")
# Remove author asides that reference the internal list structure / not-yet-built Eastern Front volume.
prewar = prewar.replace(
  "Eastern Front operations remain out of scope per L1's convention; the Soviet entry is recorded here as a chronology marker because the Polish partition was the joint German-Soviet act the M-R secret protocol had specified.",
  "The Soviet entry is recorded here because the Polish partition was the joint German-Soviet act the M-R secret protocol had specified.")
prewar = prewar.replace(
  " Soviet operations against Finland and the Finnish defense itself are out of scope as Eastern Front material — the Mannerheim Line, the *motti* tactics, *Mannerheim*'s campaign — handled in a separate Eastern Front list when developed.",
  "")
eu = pp.fold_entries(eu, pp.prewar_section_entries(prewar, "List 1"))
results["european"] = build.build(make_cfg(
    "european","flags", pp.emit_md(eu), FW["european"], addendum=eu_addendum, scope=SCOPE["european"]))

# ===== MEDITERRANEAN / MIDDLE EAST =====
medair = pp.parse_list(read(U+"WWII-List3-Mediterranean-Middle-East-Addendum.md"))
med_years = OrderedDict()
for item in med_entries:
    med_years.setdefault(item["year"], []).append(item["entry"])
for y, entries in medair["years"].items():
    for e in entries:
        med_years.setdefault(y, []).append(e)
med_struct = {"h1":"Mediterranean / Middle East", "frontmatter":[],
              "framework":None, "years":med_years, "notes": medair["notes"]}
results["med"] = build.build(make_cfg(
    "med","flags", pp.emit_md(med_struct), FW["med"], scope=SCOPE["med"]))

# ===== PACIFIC =====
l2 = pp.parse_list(read(U+"WWII-List2-Pacific.md"))
pac_addendum = {"title": l2["framework"]["title"].split(" — ",1)[-1],
                "fields": l2["framework"]["fields"]} if l2["framework"] else None
results["pacific"] = build.build(make_cfg(
    "pacific","flags", pp.emit_md(l2), FW["pacific"], addendum=pac_addendum, scope=None))

# ===== EUROPEAN AIR =====
l3 = pp.parse_list(read(U+"WWII-List3-Europe-Air_1.md"))
l3 = pp.fold_entries(l3, pp.prewar_section_entries(prewar, "List 3"))
results["air"] = build.build(make_cfg(
    "air","insignia", pp.emit_md(l3), FW["air"], scope=SCOPE["air"]))


# ===== EASTERN FRONT =====
FW["eastern"] = [
 ("Framework", "This is the Eastern Front volume of Heritage Fine Scale's operational reference: a chronological index of the German–Soviet war — the largest land war ever fought and the theater where the German army was destroyed — together with the Soviet Far East operations that bracket it, from Lake Khasan in 1938 to the Manchurian offensive of August 1945. It is a reference, not a narrative — entries are sorted by start date and stated in the terms an operation was planned and judged in, so a builder can place a subject in the actual record rather than in the box-art summary."),
 ("Structure", "Entries are grouped by calendar year and ordered by date of first major action; multi-year efforts are bracketed at their opening as campaign or programme brackets. Two discrete sections precede the chronology by design — the Soviet–Japanese Far East unit, held together because its two border wars, its pact, and its 1945 offensive are one story; and the Soviet expansion of 1939–41, because the 1941 campaign reads incoherently without the Red Army's deployment posture explained. Each entry follows the same three-field anatomy — Forces, Intent, Outcome — the skeleton the dossiers use, so the reference and the long-form briefs read in one register. Soviet codenames are transliterated in entry titles with Cyrillic in parentheses; Axis codenames are set in italic where the scholarship attests them."),
 ("Doctrine", "Inclusion is by consequence, not by drama: an action earns an entry if it changed the shape of the theater, whether or not it is famous. The through-line is the house argument — the gap between what gets remembered and what actually mattered — applied here in every direction at once: Soviet constructed memory, the German memoir literature's clean-Wehrmacht and lost-victories constructions, and the national memories of the lands between. Treatment is evenhanded; Axis intent and outcome are stated as the Axis command understood them. The war's criminal dimension is carried structurally, in-chronology, where it belongs — not as adjunct but as planning premise; the second addendum below frames the pattern."),
 ("Operational Outcomes", "Read in order, the theater resolves into a recognizable shape. 1938–39 is the Far East proving ground — Khasan and Khalkhin Gol — that turned Japanese expansion south and auditioned Zhukov. 1939–41 is the expansion: Poland partitioned, the Winter War's costly verdict, the Baltic and Bessarabian annexations that set the 1941 start line. 1941 is catastrophe and survival — the frontier disasters, Kyiv and Vyazma, and the counteroffensive before Moscow that broke the campaign's premise. 1942 runs from the Kharkov and Crimean failures through Blau to Stalingrad, the war's hinge. 1943 is Kursk and the race to the Dnieper — the initiative changing hands for good. 1944 is the year of the ten blows: Bagration destroying Army Group Center, the Balkan collapse, the satellites changing sides. 1945 is Vistula–Oder, Berlin, and — three months after the German surrender, almost to the day — Manchuria. For the modeler, that arc is the point: it tells you what a subject was actually doing in the war, the first thing an authentic build has to get right and the last thing the box will tell you."),
]
SCOPE["eastern"] = [
 ("Scope", "Soviet forces and their co-belligerents against Germany and the Axis eastern coalition (Finland, Romania, Hungary, Slovakia, Italy's ARMIR, Spain's *División Azul*), plus the Soviet–Japanese Far East operations. Eastern naval (Baltic, Black Sea, Arctic coastal, river flotillas) and air operations folded in wholesale."),
 ("Period", "July 1938 – September 1945."),
 ("Sort", "By start date; range shown in each entry. Two discrete sections — the Far East unit and the Soviet Expansion of 1939–41 — precede the main chronology."),
 ("Codenames", "Soviet codenames transliterated in entry titles with Cyrillic in parentheses; Axis codenames italicized where commonly attested."),
]
BANNERS["eastern"] = dict(
 banner_title="Belligerents &mdash; Eastern Front &amp; Soviet Far East",
 banner_note=("National markings shown schematically; the German marking follows the period military cross "
              "used across this site and Japan is shown by the wartime naval ensign. Romania appears in both "
              "columns &mdash; Axis until the 23 August 1944 coup, co-belligerent after; Bulgaria entered the "
              "Allied column in September 1944; Finland fought as a German co-belligerent until its separate "
              "exit in September 1944, then &mdash; per the Moscow Armistice &mdash; expelled the Wehrmacht from Lapland by force into April 1945, hence its place in both columns; the Spanish <em>Divisi&oacute;n Azul</em> was withdrawn in October 1943."),
 allied=[("su","Soviet Union"),("mn","Mongolia"),("pl","Poland (LWP)"),
         ("cz","Czechoslovak Corps"),("ro","Romania (from Aug 1944)"),("bg","Bulgaria (from Sep 1944)"),
         ("fi","Finland (from Sep 1944)")],
 axis=[("de","Germany"),("fi","Finland (to Sep 1944)"),("ro","Romania (to Aug 1944)"),
       ("hu","Hungary"),("sk","Slovakia"),("it","Italy (ARMIR)"),
       ("es","Spain (Divisi&oacute;n Azul)"),("hr","Croatia"),("jp","Japan (Far East)")])
META["eastern"] = dict(kicker="Operations Reference &middot; Eastern Front",
 h1="The Eastern Front", years="1938&ndash;1945",
 deck="The German&ndash;Soviet war and the Soviet Far East &mdash; ground, naval, and air operations folded into one chronology. Each entry gives forces, intent, and outcome.",
 title="The Eastern Front, 1938&ndash;1945 &mdash; Operations Reference &mdash; Heritage Fine Scale",
 meta_desc="A curated operational reference for the Eastern Front, 1938-1945: the German-Soviet war and the Soviet Far East operations, with forces, intent, and outcome for each. Heritage Fine Scale.",
 out=OUT+"eastern-front-1938-1945.html")

ef_md = pp.rewrite_series_refs(read(U+"WWII-List4-Eastern-Front.md"))
ef_md, ef_blocks = pp.extract_framework_blocks(ef_md)
ef_cfg = make_cfg("eastern", "flags", ef_md, FW["eastern"],
                  addendum=[{"title": b["title"], "fields": b["fields"]} for b in ef_blocks],
                  scope=SCOPE["eastern"])
ef_cfg["keep_notes"] = True
ef_cfg["section_labels"] = {
    "Soviet\u2013Japanese / Far East (1938\u20131945)": ("far-east", "Far East"),
    "Soviet Expansion 1939\u20131941": ("expansion", "Expansion"),
}
results["eastern"] = build.build(ef_cfg)

# ===== sprite sheet to outputs =====
import sprites
import cairosvg
cairosvg.svg2png(bytestring=sprites.sheet_svg().encode(),
                 write_to=OUT+"hfs-marking-library.png", output_width=1560)

for k, r in results.items():
    print(k, "->", os.path.basename(r["out"]), "| entries", r["entries"], "| years", r["years"])
