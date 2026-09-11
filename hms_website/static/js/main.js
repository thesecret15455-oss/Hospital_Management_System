// Makes the sidebar nav in the Patient / Doctor / Admin dashboards interactive:
// clicking a link marks it active (color change) and briefly highlights the
// section it points to, so it's obvious something happened.
document.addEventListener("DOMContentLoaded", function () {
  var navLinks = document.querySelectorAll(".pdash-nav a, .adash-nav a");

  navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      var href = this.getAttribute("href") || "";

      // Always update which link looks "active", even for links that
      // navigate to a different page.
      navLinks.forEach(function (l) { l.classList.remove("active"); });
      this.classList.add("active");

      // Only intercept same-page anchor links (e.g. "#billing"); real
      // page navigations (like "Book New Visit") are left alone.
      if (href.charAt(0) === "#" && href.length > 1) {
        var target = document.querySelector(href);
        if (target) {
          target.classList.add("section-highlight");
          setTimeout(function () {
            target.classList.remove("section-highlight");
          }, 1400);
        }
      }
    });
  });

  // If the page was loaded with a #hash already in the URL (e.g. after a
  // redirect from a form submit), highlight that section and mark its
  // sidebar link active on load too.
  if (window.location.hash) {
    var initialTarget = document.querySelector(window.location.hash);
    if (initialTarget) {
      initialTarget.classList.add("section-highlight");
      setTimeout(function () { initialTarget.classList.remove("section-highlight"); }, 1400);
    }
    navLinks.forEach(function (l) {
      if (l.getAttribute("href") === window.location.hash) {
        navLinks.forEach(function (x) { x.classList.remove("active"); });
        l.classList.add("active");
      }
    });
  }
});

// Mobile off-canvas sidebar for the Patient / Admin / Doctor dashboards.
// Injects a hamburger button + dimming overlay so the fixed sidebar can be
// slid in/out on small screens instead of squeezing the layout.
document.addEventListener("DOMContentLoaded", function () {
  var sidebar = document.querySelector(".pdash-sidebar, .adash-sidebar");
  var root = document.querySelector(".pdash, .adash");
  if (!sidebar || !root) return;

  var toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "sidebar-toggle";
  toggle.setAttribute("aria-label", "Toggle menu");
  toggle.textContent = "☰";
  root.appendChild(toggle);

  var overlay = document.createElement("div");
  overlay.className = "sidebar-overlay";
  root.appendChild(overlay);

  function closeSidebar() {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
  }

  toggle.addEventListener("click", function () {
    var isOpen = sidebar.classList.toggle("open");
    overlay.classList.toggle("show", isOpen);
  });

  overlay.addEventListener("click", closeSidebar);

  sidebar.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", closeSidebar);
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 880) closeSidebar();
  });
});
