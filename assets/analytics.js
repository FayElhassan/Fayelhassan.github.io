/* Visitor analytics for fayelhassan.github.io
 *
 * Configure on the <script> tag that loads this file:
 *   data-goatcounter="your-code"   -> https://your-code.goatcounter.com (cookie-free counts, always on)
 *   data-clarity="abcd1234ef"      -> Microsoft Clarity project ID (heatmaps/replays, only after consent)
 * Leave either empty to switch it off.
 *
 * GoatCounter also records which sections each visitor reaches (once per visit),
 * as events named "section/research", "section/journey", … so you can see where people stay.
 */
(function () {
  var me = document.currentScript;
  var GC = (me && me.getAttribute("data-goatcounter") || "").trim();
  var CLARITY = (me && me.getAttribute("data-clarity") || "").trim();
  var KEY = "fe-consent"; // "yes" | "no"
  var ar = document.documentElement.lang === "ar";
  var local = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  if (CLARITY) document.documentElement.classList.add("analytics-consent");

  function store(get, val) {
    try { return get ? localStorage.getItem(KEY) : localStorage.setItem(KEY, val); } catch (e) { return null; }
  }
  function addScript(src, attrs) {
    var s = document.createElement("script");
    s.async = true; s.src = src;
    for (var k in attrs) s.setAttribute(k, attrs[k]);
    document.head.appendChild(s);
    return s;
  }

  // ---- GoatCounter: no cookies, no personal data, so no consent needed ----
  if (GC && !local) {
    window.goatcounter = { no_onload: false };
    addScript("https://gc.zgo.at/count.js", { "data-goatcounter": "https://" + GC + ".goatcounter.com/count" });
  }
  // Section events: which parts of the page people actually reach
  if (GC && "IntersectionObserver" in window) {
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var id = e.target.id;
        if (!e.isIntersecting || seen[id]) return;
        seen[id] = true;
        var send = function () {
          if (window.goatcounter && window.goatcounter.count)
            window.goatcounter.count({ path: "section/" + id + (ar ? "-ar" : ""), title: "Section: " + id, event: true });
        };
        if (local) return console.info("[analytics] would count section/" + id);
        window.goatcounter && window.goatcounter.count ? send() : setTimeout(send, 1500);
      });
    }, { rootMargin: "-45% 0px -45% 0px" }); // counts a section once it crosses the middle of the screen, however tall it is
    document.querySelectorAll("main section[id]").forEach(function (s) { io.observe(s); });
  }

  // ---- Microsoft Clarity: uses cookies, so only after the visitor accepts ----
  function loadClarity() {
    if (!CLARITY || window.clarity) return;
    if (local) return console.info("[analytics] would load Clarity " + CLARITY);
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", CLARITY);
    window.clarity("consent");
  }

  var T = ar ? {
    text: "أستخدم ملفات تعريف الارتباط من Microsoft Clarity لفهم كيفية تصفّح الزوار للموقع (الخرائط الحرارية وإعادة الجلسات) وتحسينه. يُحصى عدد الزيارات دون ملفات تعريف ارتباط في كل الأحوال.",
    yes: "موافقة", no: "رفض", more: "اعرف المزيد"
  } : {
    text: "I use Microsoft Clarity cookies to understand how visitors move through this site (heatmaps and session replays) so I can improve it. Visits are counted without cookies either way.",
    yes: "Accept", no: "Decline", more: "Learn more"
  };

  function banner() {
    if (!CLARITY || document.getElementById("consent")) return;
    var d = document.createElement("div");
    d.id = "consent"; d.className = "consent"; d.setAttribute("role", "dialog");
    d.setAttribute("aria-live", "polite"); d.setAttribute("aria-label", ar ? "ملفات تعريف الارتباط" : "Cookies");
    d.innerHTML = '<p>' + T.text + ' <a href="https://learn.microsoft.com/en-us/clarity/setup-and-installation/privacy-disclosure" target="_blank" rel="noopener">' + T.more + '</a></p>' +
      '<div class="consent-actions"><button type="button" class="consent-no">' + T.no + '</button>' +
      '<button type="button" class="consent-yes">' + T.yes + '</button></div>';
    document.body.appendChild(d);
    requestAnimationFrame(function () { d.classList.add("show"); });
    function close(choice) {
      store(false, choice);
      d.classList.remove("show");
      setTimeout(function () { d.remove(); }, 300);
      if (choice === "yes") loadClarity();
      else if (window.clarity) window.clarity("consent", false);
    }
    d.querySelector(".consent-yes").addEventListener("click", function () { close("yes"); });
    d.querySelector(".consent-no").addEventListener("click", function () { close("no"); });
  }

  var choice = store(true);
  if (choice === "yes") loadClarity();
  else if (choice !== "no") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", banner); else banner();
  }

  // "Cookie settings" link in the footer reopens the banner
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-cookie-settings]");
    if (!a) return;
    e.preventDefault();
    if (!CLARITY) return;
    try { localStorage.removeItem(KEY); } catch (err) {}
    banner();
  });
})();
