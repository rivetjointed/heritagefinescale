/* ══════════════════════════════════════════════════════════════════════
   Full-bleed image carousel — Linden Street Studio
   Pairs with lightbox.css.

   USAGE, in full:
     <link rel="stylesheet" href="/assets/lightbox.css">
     <script src="/assets/lightbox.js" defer></script>
     <img class="zoomable" src="…" alt="…" data-cap="optional caption">

   The overlay builds itself from this file. Nothing to paste into the page,
   which is the point: a site that hand-copies overlay markup drifts from
   every other site the first time one of them is edited.

   Caption falls back to data-cap, then alt, then nothing.

   Optional data-full="…" names a larger file for the viewer, so a grid can
   carry light thumbnails while the overlay shows real detail. Without it the
   viewer shows the image the page already loaded, as it always has.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var imgs = [].slice.call(document.querySelectorAll("img.zoomable"));
  if (!imgs.length) return;

  // ---- build the overlay ------------------------------------------------
  var lb = document.createElement("div");
  lb.id = "lightbox";
  lb.setAttribute("role", "dialog");
  lb.setAttribute("aria-modal", "true");
  lb.setAttribute("aria-label", "Image viewer");
  lb.hidden = true;
  if (imgs.length === 1) lb.classList.add("single");

  lb.innerHTML =
    '<button class="lb-close" type="button" aria-label="Close image viewer">&#10005;</button>' +
    '<button class="lb-nav" id="lbPrev" type="button" aria-label="Previous image">&#8249;</button>' +
    '<button class="lb-nav" id="lbNext" type="button" aria-label="Next image">&#8250;</button>' +
    '<img class="lb-img" alt="">' +
    '<p class="lb-cap"></p>' +
    '<p class="lb-count"></p>';
  document.body.appendChild(lb);

  var img = lb.querySelector(".lb-img"),
      cap = lb.querySelector(".lb-cap"),
      count = lb.querySelector(".lb-count"),
      btnClose = lb.querySelector(".lb-close"),
      btnPrev = lb.querySelector("#lbPrev"),
      btnNext = lb.querySelector("#lbNext"),
      i = 0,
      lastFocused = null;

  function show(n) {
    i = (n + imgs.length) % imgs.length;
    var el = imgs[i];
    // currentSrc picks the resolution the browser actually chose for a
    // srcset image; src alone can hand back the wrong one.
    img.src = el.dataset.full || el.currentSrc || el.src;
    img.alt = el.alt || "";
    cap.textContent = el.dataset.cap || el.alt || "";
    count.textContent = (i + 1) + " / " + imgs.length;
    // Full-size files are heavy, so warm the neighbours while this one is
    // being looked at; paging then does not stall on a blank viewer.
    [i - 1, i + 1].forEach(function (k) {
      var nb = imgs[(k + imgs.length) % imgs.length];
      if (nb.dataset.full) new Image().src = nb.dataset.full;
    });
  }

  function open(n) {
    lastFocused = document.activeElement;
    show(n);
    lb.hidden = false;
    lb.classList.add("show");
    document.body.style.overflow = "hidden";
    btnClose.focus();
  }

  function close() {
    lb.classList.remove("show");
    lb.hidden = true;
    img.removeAttribute("src");   // stop a large image decoding in the background
    document.body.style.overflow = "";
    // Send focus back where it came from, or the keyboard user is dumped at
    // the top of the document with no idea where they were.
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  imgs.forEach(function (el, n) {
    el.addEventListener("click", function () { open(n); });

    // An image that opens a viewer is a control, and a plain <img> is not
    // reachable by keyboard at all, so without this the carousel simply does
    // not exist for anyone not using a mouse. Promoting it in script rather
    // than in markup means no host page has to remember to do it.
    el.setAttribute("tabindex", "0");
    el.setAttribute("role", "button");
    if (!el.getAttribute("aria-label")) {
      el.setAttribute("aria-label", "View larger: " + (el.dataset.cap || el.alt || "image"));
    }
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
        e.preventDefault();          // stop Space scrolling the page behind
        open(n);
      }
    });
  });

  btnPrev.addEventListener("click", function () { show(i - 1); });
  btnNext.addEventListener("click", function () { show(i + 1); });
  btnClose.addEventListener("click", close);

  // Backdrop click closes; a click on the image or caption must not.
  lb.addEventListener("click", function (e) {
    if (e.target === lb) close();
  });

  document.addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape") { close(); return; }
    if (e.key === "ArrowLeft") { show(i - 1); return; }
    if (e.key === "ArrowRight") { show(i + 1); return; }
    if (e.key !== "Tab") return;
    // Keep Tab inside the dialog. Without this, focus walks off into the page
    // behind the overlay, which is still scrolled and inert to the eye.
    var stops = [btnClose, btnPrev, btnNext].filter(function (b) {
      return b.offsetParent !== null;
    });
    if (!stops.length) return;
    var first = stops[0], last = stops[stops.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault(); last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault(); first.focus();
    }
  });

  // Swipe. 40px threshold, and horizontal only, so a vertical scroll gesture
  // on a tall image does not flick to the next one.
  var tx = 0, ty = 0;
  img.addEventListener("touchstart", function (e) {
    tx = e.touches[0].clientX;
    ty = e.touches[0].clientY;
  }, { passive: true });
  img.addEventListener("touchend", function (e) {
    var dx = e.changedTouches[0].clientX - tx,
        dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) show(dx > 0 ? i - 1 : i + 1);
  });
})();
