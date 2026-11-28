// Small site-wide behaviour, loaded with defer on every page.
(function () {
  // Header: turn into a floating pill once the page is scrolled (styles in style.css, header.site.is-scrolled).
  var h = document.querySelector('header.site');
  if (h) {
    var on = false;
    var check = function () {
      var s = window.scrollY > 24;
      if (s !== on) { on = s; h.classList.toggle('is-scrolled', s); }
    };
    check();
    window.addEventListener('scroll', check, { passive: true });
  }
  // Client logo strip: pause / play button (moving content needs a way to stop it).
  document.querySelectorAll('.clients').forEach(function (c) {
    var b = c.querySelector('.clients-toggle');
    if (!b) return;
    b.addEventListener('click', function () {
      var p = c.classList.toggle('paused');
      b.setAttribute('aria-pressed', p ? 'true' : 'false');
    });
  });
})();
