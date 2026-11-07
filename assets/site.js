(function () {
  var root = document.documentElement;

  // Theme toggle (remembers choice when storage is available)
  try { var saved = localStorage.getItem("theme"); if (saved) root.setAttribute("data-theme", saved); } catch (e) {}
  var themeBtn = document.querySelector(".theme");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var cur = root.getAttribute("data-theme") ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    var next = cur === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) {}
  });

  // Mobile menu
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open);
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { links.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  // Nav border on scroll + active section
  var nav = document.querySelector(".nav");
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  function onScroll() { nav.classList.toggle("scrolled", window.scrollY > 8); }
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });

  if ("IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) navLinks.forEach(function (a) {
          a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id);
        });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    navLinks.forEach(function (a) { var s = document.querySelector(a.getAttribute("href")); if (s) spy.observe(s); });

    // Gentle reveal
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".theme-card, .pub, .project, .timeline li, .roles li, .talks li").forEach(function (el) {
      el.classList.add("reveal"); io.observe(el);
    });
  }

  // Publication filters
  var chips = document.querySelectorAll(".chip");
  var pubs = document.querySelectorAll(".pub");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.classList.toggle("is-on", c === chip); c.setAttribute("aria-pressed", c === chip); });
      pubs.forEach(function (p) {
        p.hidden = !(f === "all" || p.getAttribute("data-topic").split(" ").indexOf(f) !== -1);
      });
    });
  });

  var yr = document.getElementById("yr"); if (yr) yr.textContent = new Date().getFullYear();
})();

// TEDx: load the YouTube player only when asked (privacy-enhanced domain)
document.querySelectorAll(".tedx-player").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var id = btn.getAttribute("data-yt");
    var f = document.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
    f.title = "Women's Identity in Sudan | Fay Elhassan | TEDxUniversityofKhartoum";
    f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    f.allowFullscreen = true;
    var wrap = document.createElement("div");
    wrap.className = "tedx-player";
    wrap.appendChild(f);
    btn.replaceWith(wrap);
  }, { once: true });
});

// "Show more" for long lists: <el data-collapse="N" data-label="talks">
(function () {
  var lists = document.querySelectorAll("[data-collapse]");
  lists.forEach(function (list) {
    var n = parseInt(list.getAttribute("data-collapse"), 10);
    var items = Array.prototype.slice.call(list.children);
    if (items.length <= n) return;
    var label = list.getAttribute("data-label") || "items";
    var extra = items.slice(n);
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "show-more";
    if (!list.id) list.id = "list-" + label;
    btn.setAttribute("aria-controls", list.id);
    function set(open) {
      extra.forEach(function (el) { el.classList.toggle("is-collapsed", !open); });
      btn.setAttribute("aria-expanded", open);
      btn.innerHTML = open ? "Show less <span aria-hidden=\"true\">↑</span>"
        : (list.getAttribute("data-more") ? list.getAttribute("data-more") + " (" + extra.length + ")" : "Show " + extra.length + " more " + label) + " <span aria-hidden=\"true\">↓</span>";
    }
    list._setCollapsed = function (collapsed) { set(!collapsed); btn.hidden = false; };
    list._expandForFilter = function () { extra.forEach(function (el) { el.classList.remove("is-collapsed"); }); btn.hidden = true; };
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") !== "true";
      set(open);
      if (!open) list.scrollIntoView({ block: "nearest" });
    });
    list.insertAdjacentElement("afterend", btn);
    set(false);
  });

  // Publication filters show every match; "All" returns to the collapsed list
  var pubs = document.querySelector(".pubs");
  document.querySelectorAll(".chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      if (!pubs || !pubs._setCollapsed) return;
      if (chip.getAttribute("data-filter") === "all") pubs._setCollapsed(true);
      else pubs._expandForFilter();
    });
  });
})();

// ================= Characters & the Nile journey =================
(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SVGNS = "http://www.w3.org/2000/svg";

  // --- The confluence felucca (SMIL) pauses for reduced motion
  if (reduce) document.querySelectorAll(".confluence").forEach(function (s) { if (s.pauseAnimations) s.pauseAnimations(); });

  // --- Camel: walks the dune, jumps on click, and hops now and then on its own
  var camel = document.querySelector(".camel");
  var fig = document.querySelector(".hero-photo");
  function sizeWalk() { if (camel && fig) camel.style.setProperty("--walk", Math.max(60, fig.clientWidth - camel.offsetWidth) + "px"); }
  function jump() {
    if (!camel || camel.classList.contains("jump")) return;
    camel.classList.add("jump");
    setTimeout(function () { camel.classList.remove("jump"); }, 720);
  }
  if (camel) {
    sizeWalk(); addEventListener("resize", sizeWalk);
    camel.addEventListener("click", jump);
    if (!reduce) setInterval(function () { if (!document.hidden && Math.random() < .5) jump(); }, 6500);
  }

  // --- Section diamonds hop as each section arrives
  if ("IntersectionObserver" in window && !reduce) {
    var hopIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("hop"); hopIO.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -20% 0px" });
    document.querySelectorAll(".section .kicker").forEach(function (k) { hopIO.observe(k); });
  }

  // --- Project cards tilt toward the pointer (mouse only)
  if (!reduce && matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll(".project").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        card.style.transform = "perspective(800px) rotateY(" + (x * 6) + "deg) rotateX(" + (-y * 6) + "deg) translateY(-3px)";
      });
      card.addEventListener("mouseleave", function () { card.style.transform = ""; });
    });
  }

  // --- The Nile: a winding river through the journey; a felucca sails it as you scroll
  var nile = document.getElementById("nile");
  if (!nile) return;
  var svg = nile.querySelector(".nile-svg");
  var parts = ["bank", "water", "flow", "progress"].map(function (n) { return svg.querySelector(".nile-" + n); });
  var progress = parts[3];
  var nodesG = svg.querySelector(".nile-nodes"), decorG = svg.querySelector(".nile-decor");
  var boat = svg.querySelector(".nile-boat");
  var stops = Array.prototype.slice.call(nile.querySelectorAll(".stop"));
  var len = 0, nodeLens = [], nodeEls = [], boatScale = 1.3;

  function centerY(el) { var r = el.getBoundingClientRect(), n = nile.getBoundingClientRect(); return r.top - n.top + r.height / 2; }
  function lengthAtY(y) {               // river flows downward, so y grows with length
    var lo = 0, hi = len;
    for (var i = 0; i < 24; i++) { var mid = (lo + hi) / 2; if (progress.getPointAtLength(mid).y < y) lo = mid; else hi = mid; }
    return lo;
  }
  function build() {
    var W = nile.clientWidth, H = nile.clientHeight;
    if (!W || !H) return;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    var mobile = W < 700, cx = mobile ? 26 : W / 2, amp = mobile ? 10 : 64;
    boatScale = mobile ? .72 : 1.3;
    var pts = [centerY(nile.querySelector(".nile-source"))]
      .concat(stops.map(function (s) { return centerY(s.querySelector(".stop-card")); }))
      .concat([centerY(nile.querySelector(".nile-mouth"))]);
    var d = "M" + cx + " " + pts[0], dir = 1, mids = [];
    for (var i = 1; i < pts.length; i++) {
      var y0 = pts[i - 1], y1 = pts[i], dy = y1 - y0, sx = cx + amp * dir;
      d += " C" + sx + " " + (y0 + dy * .38) + " " + sx + " " + (y1 - dy * .38) + " " + cx + " " + y1;
      mids.push({ x: cx + amp * dir * .75, y: (y0 + y1) / 2, dir: dir });
      dir = -dir;
    }
    parts.forEach(function (p) { p.setAttribute("d", d); });
    len = progress.getTotalLength();
    progress.style.strokeDasharray = len;
    nodesG.innerHTML = ""; decorG.innerHTML = ""; nodeEls = [];
    nodeLens = stops.map(function (s, i) {
      var y = pts[i + 1];
      if (s.classList.contains("is-now")) {
        var ring = document.createElementNS(SVGNS, "circle");
        ring.setAttribute("class", "nile-node-ring"); ring.setAttribute("cx", cx); ring.setAttribute("cy", y); ring.setAttribute("r", 9);
        nodesG.appendChild(ring);
      }
      var c = document.createElementNS(SVGNS, "circle");
      c.setAttribute("class", "nile-node" + (s.classList.contains("is-now") ? " now" : ""));
      c.setAttribute("cx", cx); c.setAttribute("cy", y); c.setAttribute("r", 7);
      nodesG.appendChild(c); nodeEls.push(c);
      return lengthAtY(y);
    });
    if (!mobile) stops.forEach(function (s, i) {   // date palms on the empty bank opposite each card
      var side = i % 2 === 0 ? 1 : -1, y = pts[i + 1];
      [0, 1].forEach(function (k) {
        if (k && i % 2) return;
        var h = k ? 44 : 62, w = h * 2 / 3;
        var u = document.createElementNS(SVGNS, "use");
        u.setAttribute("href", "#palm"); u.setAttribute("width", w); u.setAttribute("height", h);
        u.setAttribute("x", cx + side * (120 + k * 46) - w / 2); u.setAttribute("y", y - h + 18 + k * 6);
        u.setAttribute("class", "palm-sway"); u.style.animationDelay = (-(i + k) * .8) + "s";
        decorG.appendChild(u);
      });
    });
    update();
  }
  function update() {
    if (!len) return;
    var r = nile.getBoundingClientRect();
    var t = Math.min(1, Math.max(0, (innerHeight * .55 - r.top) / r.height));
    var L = t * len;
    progress.style.strokeDashoffset = len - L;
    var p = progress.getPointAtLength(L), q = progress.getPointAtLength(Math.min(len, L + 2));
    var tilt = Math.max(-14, Math.min(14, Math.atan2(q.x - p.x, q.y - p.y) * -20));
    var face = q.x < p.x ? -1 : 1;
    boat.classList.add("on");
    boat.setAttribute("transform", "translate(" + p.x + " " + (p.y + 2) + ") rotate(" + tilt + ") scale(" + (face * boatScale) + " " + boatScale + ")");
    var current = -1;
    nodeLens.forEach(function (nl, i) {
      var reached = L >= nl - 4;
      stops[i].classList.toggle("reached", reached);
      nodeEls[i] && nodeEls[i].classList.toggle("reached", reached);
      if (reached) current = i;
    });
    stops.forEach(function (s, i) { s.classList.toggle("current", i === current); });
  }
  var ticking = false;
  addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; update(); }); } }, { passive: true });
  if ("ResizeObserver" in window) new ResizeObserver(function () { build(); }).observe(nile); else addEventListener("resize", build);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
  build();
})();
