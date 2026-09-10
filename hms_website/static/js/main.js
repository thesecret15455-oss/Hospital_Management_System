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
