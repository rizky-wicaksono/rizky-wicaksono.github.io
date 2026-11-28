/* Fill-in-the-blank contact sentence (built by fill_cta in _src/build.py).
   Sizes each blank to its text, checks name + email, then opens an email (mailto:) with the sentence filled in,
   or copies it for people who use webmail. No data leaves the page: there is no server. */
(function () {
  "use strict";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function count(name) { // GoatCounter event, if the counter has loaded (it may be blocked)
    try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: "contact-" + name, title: "Contact sentence: " + name, event: true }); } catch (e) {}
  }

  document.querySelectorAll("form.fill-cta").forEach(function (form) {
    var cfg = JSON.parse(form.getAttribute("data-cta"));
    var f = { name: form.elements.name, intent: form.elements.intent, topic: form.elements.topic, email: form.elements.email };
    var status = form.querySelector(".fill-status");
    var copyBtn = form.querySelector("[data-copy]");
    // Browsers with CSS field-sizing size each blank to its text themselves (see .blank in the CSS).
    // The rest get a hidden twin of the blanks' text, used to measure how wide each blank should be.
    var cssSizing = window.CSS && CSS.supports && CSS.supports("field-sizing", "content");
    var ruler = document.createElement("span");
    ruler.setAttribute("aria-hidden", "true");
    ruler.style.cssText = "position:absolute;visibility:hidden;white-space:pre;left:-9999px;top:0";
    form.appendChild(ruler);

    // Size a blank to its value (or placeholder) so the sentence reads like a sentence.
    function fit(el) {
      if (cssSizing) return;
      var cs = getComputedStyle(el);
      ruler.style.font = cs.font;
      ruler.style.letterSpacing = cs.letterSpacing;
      ruler.textContent = el.tagName === "SELECT" ? el.options[el.selectedIndex].text : (el.value || el.placeholder);
      var pad = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight) + parseFloat(cs.borderLeftWidth) + parseFloat(cs.borderRightWidth);
      el.style.width = Math.ceil(ruler.getBoundingClientRect().width + pad + 2) + "px";
    }
    function fitAll() { Object.keys(f).forEach(function (k) { fit(f[k]); }); }
    Object.keys(f).forEach(function (k) {
      f[k].addEventListener(k === "intent" || k === "topic" ? "change" : "input", function () {
        fit(f[k]);
        if (f[k].getAttribute("aria-invalid")) check(true);
      });
    });
    if (!cssSizing) {
      fitAll();
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
      window.addEventListener("resize", fitAll);
    }

    function say(text, ok) { status.textContent = text; status.classList.toggle("ok", !!ok); }

    // quiet = re-check while typing: clear fixed errors without moving focus.
    function check(quiet) {
      var errors = [];
      var name = f.name.value.trim(), email = f.email.value.trim();
      f.name.setAttribute("aria-invalid", name ? "false" : "true");
      if (!name) errors.push([f.name, cfg.name_error]);
      var emailOk = EMAIL_RE.test(email);
      f.email.setAttribute("aria-invalid", emailOk ? "false" : "true");
      if (!emailOk) errors.push([f.email, email ? cfg.email_invalid : cfg.email_error]);
      say(errors.map(function (x) { return x[1]; }).join(" "));
      if (errors.length && !quiet) errors[0][0].focus();
      return !errors.length;
    }

    function fill(tpl, brackets) {
      var v = { name: f.name.value.trim(), intent: f.intent.value, topic: f.topic.value, email: f.email.value.trim() };
      return tpl.replace(brackets ? /\[(name|intent|topic|email)\]/g : /\{(name|intent|topic|email)\}/g, function (_, k) { return v[k]; });
    }
    function message() { return fill(cfg.sentence, true); }

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (!check(false)) return;
      // mailto: does nothing visible when no email app is set up, so always say what should happen.
      say(cfg.opening, true);
      count("send");
      window.location.href = "mailto:" + cfg.to + "?subject=" + encodeURIComponent(fill(cfg.subject, false)) + "&body=" + encodeURIComponent(message() + "\n");
    });

    if (copyBtn && navigator.clipboard && window.isSecureContext) {
      copyBtn.hidden = false;
      copyBtn.addEventListener("click", function () {
        if (!check(false)) return;
        navigator.clipboard.writeText(message()).then(function () {
          say(cfg.copied, true);
          count("copy");
        }, function () { say(cfg.copy_failed); });
      });
    }
  });
})();
