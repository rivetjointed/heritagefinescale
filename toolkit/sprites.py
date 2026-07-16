"""HFS master marking library — national flags (60x40) and air insignia (40x40).

Auto-assembled by build_sprites.py. Edit there, not here.

Public API:
  SPRITE_DEFS            -> str: the inner <defs> markup (all <symbol>s)
  defs_svg()             -> str: a hidden <svg><defs>...</defs></svg> sprite block
  marker(id, label, kind)-> str: a <figure> with <use> for one marking
  sheet_svg(ids=None)    -> str: QA contact sheet of every (or given) marking
"""

SPRITE_DEFS = """<symbol id="star5w" viewBox="0 0 10 10"><polygon points="5,0 6.18,3.6 10,3.6 6.9,5.9 8.1,9.5 5,7.3 1.9,9.5 3.1,5.9 0,3.6 3.82,3.6" fill="#f2ecdf"/></symbol>
<symbol id="star5r" viewBox="0 0 10 10"><polygon points="5,0 6.18,3.6 10,3.6 6.9,5.9 8.1,9.5 5,7.3 1.9,9.5 3.1,5.9 0,3.6 3.82,3.6" fill="#c8102e"/></symbol>
<symbol id="star5g" viewBox="0 0 10 10"><polygon points="5,0 6.18,3.6 10,3.6 6.9,5.9 8.1,9.5 5,7.3 1.9,9.5 3.1,5.9 0,3.6 3.82,3.6" fill="#e0c068"/></symbol>
<symbol id="uj" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#1f3a93"/>
      <g stroke="#f2ecdf" stroke-width="8"><line x1="0" y1="0" x2="60" y2="40"/><line x1="60" y1="0" x2="0" y2="40"/></g>
      <g stroke="#c8102e" stroke-width="3"><line x1="0" y1="0" x2="60" y2="40"/><line x1="60" y1="0" x2="0" y2="40"/></g>
      <rect x="25" width="10" height="40" fill="#f2ecdf"/><rect y="15" width="60" height="10" fill="#f2ecdf"/>
      <rect x="27" width="6" height="40" fill="#c8102e"/><rect y="17" width="60" height="6" fill="#c8102e"/>
    </symbol>
<symbol id="us" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#f2ecdf"/>
      <g fill="#b22234">
        <rect y="0" width="60" height="3.08"/><rect y="6.15" width="60" height="3.08"/><rect y="12.3" width="60" height="3.08"/>
        <rect y="18.46" width="60" height="3.08"/><rect y="24.6" width="60" height="3.08"/><rect y="30.77" width="60" height="3.08"/><rect y="36.9" width="60" height="3.08"/>
      </g>
      <rect width="24" height="21.5" fill="#3c3b6e"/>
      <g fill="#f2ecdf">
        <circle cx="4" cy="4" r="1"/><circle cx="10" cy="4" r="1"/><circle cx="16" cy="4" r="1"/><circle cx="22" cy="4" r="1" transform="translate(-1.5,0)"/>
        <circle cx="7" cy="8" r="1"/><circle cx="13" cy="8" r="1"/><circle cx="19" cy="8" r="1"/>
        <circle cx="4" cy="12" r="1"/><circle cx="10" cy="12" r="1"/><circle cx="16" cy="12" r="1"/><circle cx="20.5" cy="12" r="1"/>
        <circle cx="7" cy="16" r="1"/><circle cx="13" cy="16" r="1"/><circle cx="19" cy="16" r="1"/>
        <circle cx="4" cy="19.5" r="1"/><circle cx="10" cy="19.5" r="1"/><circle cx="16" cy="19.5" r="1"/><circle cx="20.5" cy="19.5" r="1"/>
      </g>
    </symbol>
<symbol id="uk" viewBox="0 0 60 40"><use href="#uj"/></symbol>
<symbol id="ca" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#c8102e"/>
      <use href="#uj" width="24" height="16"/>
      <g transform="translate(44,20)">
        <path d="M0,-7 L6,-2 L4.5,6 L-4.5,6 L-6,-2 Z" fill="#f2ecdf" stroke="#7a5a2a" stroke-width="0.7"/>
        <path d="M0,-3 l1,2 2,0 -1.5,1.5 .6,2.2 -2.1,-1.3 -2.1,1.3 .6,-2.2 -1.5,-1.5 2,0 z" fill="#c8102e"/>
      </g>
    </symbol>
<symbol id="au" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#1f3a93"/>
      <use href="#uj" width="24" height="16"/>
      <use href="#star5w" x="8" y="18" width="9" height="9"/>
      <use href="#star5w" x="48" y="6"  width="6" height="6"/>
      <use href="#star5w" x="52" y="18" width="6" height="6"/>
      <use href="#star5w" x="44" y="26" width="6" height="6"/>
      <use href="#star5w" x="40" y="14" width="5" height="5"/>
      <use href="#star5w" x="49" y="30" width="4" height="4"/>
    </symbol>
<symbol id="nz" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#1f3a93"/>
      <use href="#uj" width="24" height="16"/>
      <use href="#star5r" x="48" y="6"  width="6" height="6"/>
      <use href="#star5r" x="52" y="18" width="6" height="6"/>
      <use href="#star5r" x="42" y="22" width="6" height="6"/>
      <use href="#star5r" x="47" y="30" width="6" height="6"/>
    </symbol>
<symbol id="in" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#9b1b1b"/>
      <use href="#uj" width="24" height="16"/>
      <use href="#star5g" x="40" y="13" width="14" height="14"/>
    </symbol>
<symbol id="za" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#ff7e00"/>
      <rect y="13.3" width="60" height="13.4" fill="#f2ecdf"/>
      <rect y="26.7" width="60" height="13.3" fill="#152484"/>
      <use href="#uj" x="24" y="14" width="12" height="8"/>
    </symbol>
<symbol id="pl" viewBox="0 0 60 40"><rect width="60" height="20" fill="#f2ecdf"/><rect y="20" width="60" height="20" fill="#dc143c"/></symbol>
<symbol id="fr" viewBox="0 0 60 40">
      <rect width="20" height="40" fill="#1f3a93"/><rect x="20" width="20" height="40" fill="#f2ecdf"/><rect x="40" width="20" height="40" fill="#ce1126"/>
      <g fill="#ce1126"><rect x="29" y="9" width="2" height="22"/><rect x="25" y="14" width="10" height="2"/><rect x="27" y="22" width="6" height="2"/></g>
    </symbol>
<symbol id="su" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#c8102e"/>
      <use href="#star5g" x="6" y="4" width="9" height="9"/>
      <g fill="none" stroke="#e0c068" stroke-width="1.4">
        <path d="M9,17 q7,1 5,8" /><line x1="9" y1="17" x2="15" y2="25"/>
      </g>
      <rect x="10.5" y="16.5" width="1.6" height="9" fill="#e0c068" transform="rotate(33 11 21)"/>
    </symbol>
<symbol id="gr" viewBox="0 0 60 40">
      <g fill="#1f5fb0">
        <rect y="0" width="60" height="4.44"/><rect y="8.9" width="60" height="4.44"/><rect y="17.8" width="60" height="4.44"/>
        <rect y="26.7" width="60" height="4.44"/><rect y="35.5" width="60" height="4.5"/>
      </g>
      <rect width="22.2" height="22.2" fill="#1f5fb0"/>
      <rect x="8.9" width="4.44" height="22.2" fill="#f2ecdf"/><rect y="8.9" width="22.2" height="4.44" fill="#f2ecdf"/>
    </symbol>
<symbol id="no" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#c8102e"/>
      <rect x="16" width="10" height="40" fill="#f2ecdf"/><rect y="15" width="60" height="10" fill="#f2ecdf"/>
      <rect x="18.5" width="5" height="40" fill="#1f3a93"/><rect y="17.5" width="60" height="5" fill="#1f3a93"/>
    </symbol>
<symbol id="cz" viewBox="0 0 60 40">
      <rect width="60" height="20" fill="#f2ecdf"/><rect y="20" width="60" height="20" fill="#d7141a"/>
      <polygon points="0,0 30,20 0,40" fill="#11457e"/>
    </symbol>
<symbol id="be" viewBox="0 0 60 40"><rect width="20" height="40" fill="#16110A"/><rect x="20" width="20" height="40" fill="#f3c300"/><rect x="40" width="20" height="40" fill="#c8102e"/></symbol>
<symbol id="nl" viewBox="0 0 60 40"><rect width="60" height="13.3" fill="#ae1c28"/><rect y="13.3" width="60" height="13.4" fill="#f2ecdf"/><rect y="26.7" width="60" height="13.3" fill="#21468b"/></symbol>
<symbol id="de" viewBox="0 0 60 40">
      <rect width="60" height="40" fill="#3a3631"/>
      <path d="M24,6 H36 V16 H50 V24 H36 V34 H24 V24 H10 V16 H24 Z" fill="#f2ecdf"/>
      <path d="M27,9 H33 V18.5 H47 V21.5 H33 V31 H27 V21.5 H13 V18.5 H27 Z" fill="#1c1813"/>
    </symbol>
<symbol id="it" viewBox="0 0 60 40">
      <rect width="20" height="40" fill="#0a8a3f"/><rect x="20" width="20" height="40" fill="#f2ecdf"/><rect x="40" width="20" height="40" fill="#ce1126"/>
      <rect x="26" y="13" width="8" height="13" fill="#c8102e" stroke="#11457e" stroke-width="0.9"/>
      <rect x="29" y="13" width="2" height="13" fill="#f2ecdf"/><rect x="26" y="18.5" width="8" height="2" fill="#f2ecdf"/>
    </symbol>
<symbol id="vichy" viewBox="0 0 60 40">
      <rect width="20" height="40" fill="#1f3a93"/><rect x="20" width="20" height="40" fill="#f2ecdf"/><rect x="40" width="20" height="40" fill="#ce1126"/>
      <g fill="#8a6a2a">
        <rect x="29.3" y="10" width="1.4" height="20"/>
        <path d="M30,11 l5,2 -5,3 z"/><path d="M30,11 l-5,2 5,3 z"/>
      </g>
    </symbol>
    <symbol id="jp" viewBox="0 0 60 40"><rect width="60" height="40" fill="#f2ecdf"/><polygon points="26,20 63.8,16.4 63.8,23.6" fill="#bc002d"/><polygon points="26,20 62.3,31.1 59.6,37.8" fill="#bc002d"/><polygon points="26,20 55.3,44.2 50.2,49.3" fill="#bc002d"/><polygon points="26,20 43.8,53.6 37.1,56.3" fill="#bc002d"/><polygon points="26,20 29.6,57.8 22.4,57.8" fill="#bc002d"/><polygon points="26,20 14.9,56.3 8.2,53.6" fill="#bc002d"/><polygon points="26,20 1.8,49.3 -3.3,44.2" fill="#bc002d"/><polygon points="26,20 -7.6,37.8 -10.3,31.1" fill="#bc002d"/><polygon points="26,20 -11.8,23.6 -11.8,16.4" fill="#bc002d"/><polygon points="26,20 -10.3,8.9 -7.6,2.2" fill="#bc002d"/><polygon points="26,20 -3.3,-4.2 1.8,-9.3" fill="#bc002d"/><polygon points="26,20 8.2,-13.6 14.9,-16.3" fill="#bc002d"/><polygon points="26,20 22.4,-17.8 29.6,-17.8" fill="#bc002d"/><polygon points="26,20 37.1,-16.3 43.8,-13.6" fill="#bc002d"/><polygon points="26,20 50.2,-9.3 55.3,-4.2" fill="#bc002d"/><polygon points="26,20 59.6,2.2 62.3,8.9" fill="#bc002d"/><circle cx="26" cy="20" r="9" fill="#bc002d"/></symbol>
    <symbol id="cn" viewBox="0 0 60 40"><rect width="60" height="40" fill="#de2910"/><rect width="26" height="18" fill="#1f3a93"/><polygon points="19.2,9.0 15.7,9.7 18.4,12.1 15.0,11.0 16.1,14.4 13.7,11.7 13.0,15.2 12.3,11.7 9.9,14.4 11.0,11.0 7.6,12.1 10.3,9.7 6.8,9.0 10.3,8.3 7.6,5.9 11.0,7.0 9.9,3.6 12.3,6.3 13.0,2.8 13.7,6.3 16.1,3.6 15.0,7.0 18.4,5.9 15.7,8.3" fill="#f2ecdf"/><circle cx="13" cy="9" r="2.4" fill="#1f3a93"/></symbol>
    <symbol id="th" viewBox="0 0 60 40"><rect width="60" height="6.67" fill="#a51931"/><rect y="6.67" width="60" height="6.67" fill="#f2ecdf"/><rect y="13.34" width="60" height="13.33" fill="#2d2a4a"/><rect y="26.67" width="60" height="6.66" fill="#f2ecdf"/><rect y="33.33" width="60" height="6.67" fill="#a51931"/></symbol>
    <symbol id="ph" viewBox="0 0 60 40"><rect width="60" height="20" fill="#0038a8"/><rect y="20" width="60" height="20" fill="#ce1126"/><polygon points="0,0 30,20 0,40" fill="#f2ecdf"/><polygon points="11,20 20.0,19.4 20.0,20.6" fill="#fcd116"/><polygon points="11,20 17.8,25.9 16.9,26.8" fill="#fcd116"/><polygon points="11,20 11.6,29.0 10.4,29.0" fill="#fcd116"/><polygon points="11,20 5.1,26.8 4.2,25.9" fill="#fcd116"/><polygon points="11,20 2.0,20.6 2.0,19.4" fill="#fcd116"/><polygon points="11,20 4.2,14.1 5.1,13.2" fill="#fcd116"/><polygon points="11,20 10.4,11.0 11.6,11.0" fill="#fcd116"/><polygon points="11,20 16.9,13.2 17.8,14.1" fill="#fcd116"/><circle cx="11" cy="20" r="3.2" fill="#fcd116"/><use href="#star5g" x="2" y="4" width="5" height="5"/><use href="#star5g" x="2" y="31" width="5" height="5"/><use href="#star5g" x="19" y="17.5" width="5" height="5"/></symbol>
    <symbol id="iq" viewBox="0 0 60 40"><rect width="60" height="13.33" fill="#16110A"/><rect y="13.33" width="60" height="13.34" fill="#f2ecdf"/><rect y="26.67" width="60" height="13.33" fill="#0a7d3f"/><polygon points="0,0 26,20 0,40" fill="#c8102e"/><use href="#star5w" x="6" y="12" width="6" height="6"/><use href="#star5w" x="13" y="23" width="6" height="6"/></symbol>
    <symbol id="ir" viewBox="0 0 60 40"><rect width="60" height="13.33" fill="#0a7d3f"/><rect y="13.33" width="60" height="13.34" fill="#f2ecdf"/><rect y="26.67" width="60" height="13.33" fill="#c8102e"/><polygon points="30,20 36.0,19.5 36.0,20.5" fill="#c89b2a"/><polygon points="30,20 35.4,22.5 34.9,23.4" fill="#c89b2a"/><polygon points="30,20 33.4,24.9 32.5,25.4" fill="#c89b2a"/><polygon points="30,20 30.5,26.0 29.5,26.0" fill="#c89b2a"/><polygon points="30,20 27.5,25.4 26.6,24.9" fill="#c89b2a"/><polygon points="30,20 25.1,23.4 24.6,22.5" fill="#c89b2a"/><polygon points="30,20 24.0,20.5 24.0,19.5" fill="#c89b2a"/><polygon points="30,20 24.6,17.5 25.1,16.6" fill="#c89b2a"/><polygon points="30,20 26.6,15.1 27.5,14.6" fill="#c89b2a"/><polygon points="30,20 29.5,14.0 30.5,14.0" fill="#c89b2a"/><polygon points="30,20 32.5,14.6 33.4,15.1" fill="#c89b2a"/><polygon points="30,20 34.9,16.6 35.4,17.5" fill="#c89b2a"/><circle cx="30" cy="20" r="3.4" fill="#c89b2a"/></symbol>
    <symbol id="fi" viewBox="0 0 60 40"><rect width="60" height="40" fill="#f2ecdf"/><rect x="16" width="9" height="40" fill="#003580"/><rect y="15.5" width="60" height="9" fill="#003580"/></symbol>
    <symbol id="ro" viewBox="0 0 60 40"><rect width="20" height="40" fill="#002b7f"/><rect x="20" width="20" height="40" fill="#fcd116"/><rect x="40" width="20" height="40" fill="#ce1126"/></symbol>
    <symbol id="hu" viewBox="0 0 60 40"><rect width="60" height="13.33" fill="#ce2939"/><rect y="13.33" width="60" height="13.34" fill="#f2ecdf"/><rect y="26.67" width="60" height="13.33" fill="#477050"/></symbol>
    <symbol id="mn" viewBox="0 0 60 40"><rect width="20" height="40" fill="#c8313e"/><rect x="20" width="20" height="40" fill="#1c5fa8"/><rect x="40" width="20" height="40" fill="#c8313e"/><polygon points="10,8 11.6,12.2 16,12.2 12.5,14.9 13.8,19.2 10,16.6 6.2,19.2 7.5,14.9 4,12.2 8.4,12.2" fill="#c89b2a"/><rect x="6.5" y="22" width="7" height="2.2" fill="#c89b2a"/><circle cx="10" cy="28" r="2.6" fill="#c89b2a"/><rect x="6.5" y="32" width="7" height="2.2" fill="#c89b2a"/></symbol>
    <symbol id="sk" viewBox="0 0 60 40"><rect width="60" height="13.33" fill="#f2ecdf"/><rect y="13.33" width="60" height="13.33" fill="#0b4ea2"/><rect y="26.66" width="60" height="13.34" fill="#ce2939"/><path d="M23,9 H37 V25 C37,30 30,33 30,33 C30,33 23,30 23,25 Z" fill="#ce2939" stroke="#f2ecdf" stroke-width="1.1"/><path d="M28.9,12 H31.1 V15 H34 V17.2 H31.1 V19.5 H35 V21.7 H31.1 V26 H28.9 V21.7 H25 V19.5 H28.9 V17.2 H26 V15 H28.9 Z" fill="#f2ecdf"/><path d="M24.5,27.5 C26,25.8 28,25.8 30,27.5 C32,25.8 34,25.8 35.5,27.5 C35,30 32.5,31.6 30,32.4 C27.5,31.6 25,30 24.5,27.5 Z" fill="#0b4ea2"/></symbol>
    <symbol id="es" viewBox="0 0 60 40"><rect width="60" height="10" fill="#aa151b"/><rect y="10" width="60" height="20" fill="#e3b438"/><rect y="30" width="60" height="10" fill="#aa151b"/></symbol>
    <symbol id="bg" viewBox="0 0 60 40"><rect width="60" height="13.33" fill="#f2ecdf"/><rect y="13.33" width="60" height="13.33" fill="#00805f"/><rect y="26.66" width="60" height="13.34" fill="#c8313e"/></symbol>
    <symbol id="hr" viewBox="0 0 60 40"><rect width="60" height="13.33" fill="#c8313e"/><rect y="13.33" width="60" height="13.33" fill="#f2ecdf"/><rect y="26.66" width="60" height="13.34" fill="#1c5fa8"/><g stroke="#5a4a3a" stroke-width="0.5"><rect x="24" y="10" width="3" height="3.75" fill="#c8313e"/><rect x="27" y="10" width="3" height="3.75" fill="#f2ecdf"/><rect x="30" y="10" width="3" height="3.75" fill="#c8313e"/><rect x="33" y="10" width="3" height="3.75" fill="#f2ecdf"/><rect x="24" y="13.75" width="3" height="3.75" fill="#f2ecdf"/><rect x="27" y="13.75" width="3" height="3.75" fill="#c8313e"/><rect x="30" y="13.75" width="3" height="3.75" fill="#f2ecdf"/><rect x="33" y="13.75" width="3" height="3.75" fill="#c8313e"/><rect x="24" y="17.5" width="3" height="3.75" fill="#c8313e"/><rect x="27" y="17.5" width="3" height="3.75" fill="#f2ecdf"/><rect x="30" y="17.5" width="3" height="3.75" fill="#c8313e"/><rect x="33" y="17.5" width="3" height="3.75" fill="#f2ecdf"/><rect x="24" y="21.25" width="3" height="3.75" fill="#f2ecdf"/><rect x="27" y="21.25" width="3" height="3.75" fill="#c8313e"/><rect x="30" y="21.25" width="3" height="3.75" fill="#f2ecdf"/><rect x="33" y="21.25" width="3" height="3.75" fill="#c8313e"/></g></symbol>
    <symbol id="ins-us" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#15346b"/><polygon points="20,5 23.4,15.4 34.3,15.4 25.4,21.8 28.8,32.1 20,25.7 11.2,32.1 14.6,21.8 5.7,15.4 16.6,15.4" fill="#f2ecdf"/></symbol>
    <symbol id="ins-raf" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#1f4ea1"/><circle cx="20" cy="20" r="12" fill="#f2ecdf"/><circle cx="20" cy="20" r="6" fill="#c8102e"/></symbol>
    <symbol id="ins-soviet" viewBox="0 0 40 40"><polygon points="20,3 24.7,16.5 39,16.5 27.4,24.8 32.1,38.3 20,30 7.9,38.3 12.6,24.8 1,16.5 15.3,16.5" fill="#c8102e" stroke="#4a1414" stroke-width="0.6"/></symbol>
    <symbol id="ins-luftwaffe" viewBox="0 0 40 40"><path d="M16,4 H24 V16 H36 V24 H24 V36 H16 V24 H4 V16 H16 Z" fill="#f2ecdf"/><path d="M18.4,7 H21.6 V18.4 H33 V21.6 H21.6 V33 H18.4 V21.6 H7 V18.4 H18.4 Z" fill="#16110A"/></symbol>
    <symbol id="ins-regia" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#0a8a3f"/><circle cx="20" cy="20" r="12" fill="#f2ecdf"/><circle cx="20" cy="20" r="6" fill="#c8102e"/></symbol>
    <symbol id="ins-polish" viewBox="0 0 40 40"><rect x="4" y="4" width="32" height="32" fill="#f2ecdf" stroke="#16110A" stroke-width="1.2"/><rect x="4" y="4" width="16" height="16" fill="#c8102e"/><rect x="20" y="20" width="16" height="16" fill="#c8102e"/><rect x="4" y="4" width="32" height="32" fill="none" stroke="#16110A" stroke-width="1.2"/></symbol>
    <symbol id="ins-ff" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#c8102e"/><circle cx="20" cy="20" r="12" fill="#f2ecdf"/><circle cx="20" cy="20" r="6" fill="#1f3a93"/><g fill="#c8102e"><rect x="19" y="14" width="2" height="12"/><rect x="15.5" y="17.5" width="9" height="1.6"/><rect x="17" y="22" width="6" height="1.6"/></g></symbol>"""

# Convenience id groups (a volume's config names the ids it shows, in order).
FLAGS_ALL = ["us","uk","ca","au","nz","in","za","fr","pl","cz","no","gr","be","nl",
             "su","de","it","vichy","jp","cn","th","ph","iq","ir","fi","ro","hu",
             "sk","hr","bg","es","mn"]
INSIGNIA_ALL = ["ins-us","ins-raf","ins-soviet","ins-luftwaffe","ins-regia",
                "ins-polish","ins-ff"]

def defs_svg():
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" '
            'focusable="false" xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink"><defs>'
            + SPRITE_DEFS + "</defs></svg>")

def marker(sid, label, kind="flag"):
    vb = "0 0 60 40" if kind == "flag" else "0 0 40 40"
    cls = "flag" if kind == "flag" else "insignia"
    return ('<figure class="%s"><svg viewBox="%s" role="img" '
            'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'aria-label="%s"><use href="#%s" xlink:href="#%s"/></svg>'
            '<figcaption>%s</figcaption></figure>') % (cls, vb, label, sid, sid, label)

def sheet_svg(ids=None):
    ids = ids or (FLAGS_ALL + INSIGNIA_ALL)
    cols, cw, ch = 6, 130, 96
    rows = (len(ids) + cols - 1) // cols
    W, H = cols*cw, rows*ch
    tiles = []
    for i, sid in enumerate(ids):
        x = (i % cols)*cw + 30
        y = (i // cols)*ch + 10
        vb = "0 0 40 40" if sid.startswith("ins-") else "0 0 60 40"
        w = 48 if sid.startswith("ins-") else 60
        tiles.append(f'<g transform="translate({x},{y})"><rect x="-1" y="-1" width="{w+2}" height="42" fill="none" stroke="#888"/><use href="#{sid}" width="{w}" height="40"/></g>')
        tiles.append(f'<text x="{x+w/2:.0f}" y="{y+58}" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#CFC4AA">{sid}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="#16110A"/>'
            + SPRITE_DEFS + "".join(tiles) + "</svg>")
