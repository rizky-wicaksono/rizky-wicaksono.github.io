#!/usr/bin/env python3
"""Builds the static site into _site/ (or the folder given as the first argument).

All editable text lives in content/ (home page, case studies, tools, guides; edited with Pages CMS) and is read by
content.py. Interface labels are in i18n.py, layout and CSS here. Static files (assets/, share-v2.png) are copied from the repo root."""
import html, json, os, re, shutil
from data import *  # noqa: F401,F403  (ROOT, BASE, LINKEDIN, NOTION, CASES, EXPERIENCE, e, logo_tile ...)

HERE = os.path.dirname(os.path.abspath(__file__))
# IMAGES (coverage preview images by article URL) comes from the case files via data.py

ICONS = {  # simple geometric marks, one per service, drawn in currentColor
    "media": '<circle cx="36" cy="36" r="30" fill="none" stroke="currentColor" stroke-width="8"/><circle cx="36" cy="36" r="10" fill="currentColor"/>',
    "marcomm": '<circle cx="24" cy="36" r="20" fill="currentColor"/><circle cx="48" cy="36" r="20" fill="none" stroke="currentColor" stroke-width="8"/>',
    "story": '<path d="M6 66V36a30 30 0 0 1 60 0v30z" fill="currentColor"/>',
    "corp": '<rect x="6" y="6" width="26" height="26" fill="currentColor"/><rect x="40" y="40" width="26" height="26" fill="currentColor"/><circle cx="53" cy="19" r="13" fill="none" stroke="currentColor" stroke-width="7"/>',
    "event": '<path d="M36 4 68 66H4z" fill="currentColor"/>',
    "content": '<path d="M6 36a30 30 0 0 1 60 0z" fill="currentColor"/><path d="M66 42a30 30 0 0 1-60 0z" fill="none" stroke="currentColor" stroke-width="8"/>',
}

CSS = """\
:root { --ink:#0a0a0a; --paper:#ffffff; --soft:#f4f2ee; --muted:#5f5f5b; --line:#e2dfd8; --accent:#14307a; --accent-d:#6cc4ff; --accent-hover:#94d6ff; --btn-ink:#0a0a0a;
  --dark:#0a0a0a; --dark-line:#2b2b2b; --dark-muted:#a9a9a4; --focus:#1a5cff; }
* { box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { margin:0; background:var(--paper); color:var(--ink); font:17px/1.65 "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; -webkit-font-smoothing:antialiased; }
a { color:inherit; text-underline-offset:3px; }
:focus-visible { outline:3px solid var(--focus); outline-offset:3px; border-radius:4px; }
.dark :focus-visible { outline-color:#ffd24a; }
.skip { position:absolute; left:16px; top:-60px; background:var(--accent-d); color:var(--btn-ink); padding:8px 14px; border-radius:6px; z-index:20; font-weight:700; }
.skip:focus { top:12px; }
.wrap { width:min(1200px, 100% - 48px); margin-inline:auto; }

.dark { background:var(--dark); color:#fff; }
header.site .wrap { display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; padding-block:22px; }
.brand { font-weight:800; font-size:20px; text-decoration:none; letter-spacing:-0.01em; display:inline-flex; align-items:center; gap:10px; }
.brand i { width:14px; height:14px; border-radius:50%; background:var(--accent-d); display:inline-block; }
nav ul { display:flex; flex-wrap:wrap; gap:8px 30px; list-style:none; margin:0; padding:0; }
nav a { text-decoration:none; font-size:16px; font-weight:600; color:#d8d8d3; }
nav a:hover, nav a[aria-current] { color:#fff; text-decoration:underline; text-decoration-color:var(--accent-d); text-decoration-thickness:2px; }

h1 { font-size:clamp(42px, 7vw, 96px); line-height:1.02; letter-spacing:-0.035em; font-weight:800; margin:0 0 28px; }
h2 { font-size:clamp(30px, 3.6vw, 46px); line-height:1.12; letter-spacing:-0.025em; font-weight:800; margin:0 0 28px; }
h3 { font-size:20px; line-height:1.3; margin:0 0 10px; font-weight:800; letter-spacing:-0.01em; }
p { margin:0 0 16px; }
.lead { font-size:clamp(18px, 2vw, 22px); color:var(--dark-muted); max-width:34em; }
.label { font-size:14px; font-weight:700; color:var(--muted); margin:0 0 14px; }

.btn { display:inline-block; padding:14px 26px; border-radius:999px; background:var(--accent-d); color:var(--btn-ink); text-decoration:none; font-weight:800; font-size:16px; border:2px solid var(--accent-d); transition:transform .15s, background .15s; }
.btn:hover { transform:translateY(-2px); background:var(--accent-hover); border-color:var(--accent-hover); }
.btn.ghost { background:transparent; color:#fff; border-color:#4a4a4a; }
.btn.ghost:hover { border-color:#fff; background:transparent; }
.actions { display:flex; gap:12px; flex-wrap:wrap; margin-top:36px; }

.hero { padding-block:clamp(48px, 9vw, 120px) clamp(64px, 10vw, 128px); }
.hero .wrap { display:grid; grid-template-columns:1.35fr 1fr; gap:48px; align-items:center; }
.hero-art { width:100%; max-width:440px; justify-self:end; }
.hero-art .blob { display:block; position:relative; aspect-ratio:1; border-radius:50%; background:var(--accent-d); overflow:hidden; }
.hero-art .blob img { position:absolute; left:50%; bottom:-2%; width:86%; height:auto; transform:translateX(-50%); }

section.block { padding-block:clamp(64px, 9vw, 112px); }
section.soft { background:var(--soft); }
.about { display:grid; grid-template-columns:1fr 1.3fr; gap:56px; }
.about p { font-size:18px; color:#2a2a28; }
.about .stats { grid-template-columns:1fr 1fr; gap:24px; margin-top:44px; padding-top:28px; }
.about .stats .stat b { font-size:clamp(48px, 5.4vw, 72px); }

.stats { display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:32px; margin-top:64px; padding-top:40px; border-top:2px solid var(--ink); }
.stat b { display:block; font-size:clamp(44px, 6vw, 80px); line-height:1; letter-spacing:-0.04em; font-weight:800; color:var(--accent); }
.dark .stat b { color:var(--accent-d); }
.stat span { display:block; margin-top:12px; font-size:15px; color:var(--muted); max-width:16em; }

.chip { display:inline-block; margin:6px 0 0; padding:6px 14px; border:2px solid var(--accent); color:var(--accent); border-radius:999px; font-size:14px; font-weight:800; text-decoration:none; }
a.chip:hover { background:var(--accent); color:#fff; }
.plain { margin:0 0 16px; padding-left:20px; font-size:18px; color:#2a2a28; }
.plain li { margin-bottom:6px; }
.marcomm { display:grid; grid-template-columns:1fr 1.15fr; gap:56px; align-items:center; }
.marcomm h2 { color:#fff; }
.mc-stats { display:grid; grid-template-columns:repeat(3, 1fr); gap:36px 24px; }
.mc-stats .stat b { font-size:clamp(36px, 4.4vw, 60px); }
.mc-stats .stat span { color:var(--dark-muted); }
.services { display:grid; grid-template-columns:repeat(3, 1fr); gap:56px 40px; }
.service svg { width:72px; height:72px; color:var(--ink); display:block; margin-bottom:22px; }
.service p { font-size:16px; color:#3b3b38; }
.more { font-weight:800; font-size:15px; text-decoration:none; border-bottom:2px solid var(--accent); padding-bottom:2px; }
.more:hover { background:var(--accent); }

.cards { display:grid; grid-template-columns:repeat(3, 1fr); gap:32px; }
.card { display:flex; flex-direction:column; text-decoration:none; background:var(--paper); border:1px solid var(--line); border-radius:6px; overflow:hidden; transition:transform .18s, box-shadow .18s; }
.card:hover { transform:translateY(-4px); box-shadow:0 12px 28px rgba(0,0,0,.10); }
.card .body { padding:22px 24px 26px; display:flex; flex-direction:column; flex:1; }
.card .meta { color:var(--muted); font-size:14px; margin:0 0 6px; }
.card .name { font-size:22px; line-height:1.25; font-weight:800; letter-spacing:-0.015em; margin:0 0 8px; }
.card .teaser { color:#3b3b38; font-size:16px; margin:0 0 18px; }
.card .go { margin-top:auto; font-weight:800; font-size:15px; }
.card .go::after { content:" →"; color:var(--accent); }
.card.notion { background:var(--ink); color:#fff; border-color:var(--ink); }
.card.notion .meta, .card.notion .teaser { color:var(--dark-muted); }
.card.notion .body { justify-content:flex-end; min-height:260px; }
.card .meta, .card .name, .card .teaser, .card .go { display:block; }

.thumb { position:relative; aspect-ratio:16/10; background:var(--ink); overflow:hidden; display:block; }
.thumb .fb { position:absolute; inset:0; display:flex; align-items:flex-end; padding:16px 18px; color:var(--accent-d); font-weight:800; font-size:clamp(28px, 4vw, 44px); letter-spacing:-0.03em; line-height:1; }
.thumb img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; transition:transform .35s; }
.card:hover .thumb img, a.cov:hover .thumb img { transform:scale(1.03); }
.logo-thumb { aspect-ratio:16/10; display:grid; place-items:center; padding:14%; overflow:hidden; background:var(--soft); isolation:isolate; border-bottom:1px solid var(--line); }
.logo-thumb img { max-width:78%; max-height:62%; width:auto; height:auto; object-fit:contain; mix-blend-mode:multiply; transition:transform .3s; }
.logo-thumb .fb { font-weight:800; font-size:clamp(28px,4vw,44px); color:var(--accent); letter-spacing:-0.03em; }
.card:hover .logo-thumb img { transform:scale(1.04); }
.case-hero .logo-thumb { border:0; }
.logo-tile { position:absolute; left:14px; top:14px; z-index:2; display:flex; align-items:center; justify-content:center; width:112px; height:44px; background:#fff; border-radius:6px; padding:6px 10px; margin:0; }
.logo-tile img { position:static; max-width:100%; max-height:100%; object-fit:contain; transform:none !important; }

.rows { list-style:none; margin:0; padding:0; }
.rows li { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(0,1.2fr) 200px; gap:8px 32px; padding-block:22px; border-bottom:1px solid var(--line); align-items:baseline; }
.rows li b { font-weight:800; letter-spacing:-0.01em; }
.rows li:first-child { border-top:2px solid var(--ink); }
.rows .when { color:var(--muted); font-variant-numeric:tabular-nums; text-align:right; }
.edu { color:var(--muted); margin-top:20px; }

.talk { padding-block:clamp(72px, 10vw, 128px); }
.muted-d { color:var(--dark-muted); margin-top:28px; font-size:16px; }
.muted-d a { color:#fff; }
.talk h2 { font-size:clamp(40px, 7vw, 88px); line-height:1.02; letter-spacing:-0.035em; margin-bottom:24px; }

footer.site { background:var(--dark); color:var(--dark-muted); border-top:1px solid var(--dark-line); padding-block:44px 56px; font-size:15px; }
footer.site .cols3 { display:grid; grid-template-columns:2fr 1fr 1fr; gap:32px; }
footer.site h4 { color:#fff; margin:0 0 12px; font-size:15px; }
footer.site ul { list-style:none; margin:0; padding:0; }
footer.site li { margin-bottom:8px; }
footer.site a { text-decoration:none; }
footer.site a:hover { color:#fff; text-decoration:underline; }
footer.site .note { font-size:13px; max-width:34em; }

.crumb { display:inline-block; color:var(--dark-muted); text-decoration:none; font-size:15px; font-weight:600; margin-bottom:28px; }
.crumb:hover { color:#fff; }
.case-hero { padding-block:24px clamp(48px, 7vw, 88px); }
.case-hero .wrap { display:grid; grid-template-columns:1.1fr 1fr; gap:48px; align-items:center; }
.case-hero h1 { font-size:clamp(36px, 5.4vw, 72px); }
.case-meta { display:flex; gap:32px; flex-wrap:wrap; color:var(--dark-muted); font-size:14px; margin:0; padding:0; list-style:none; }
.case-meta b { display:block; color:#fff; font-weight:700; font-size:16px; }
.cols { display:grid; grid-template-columns:repeat(3, 1fr); gap:48px; }
.cols h2 { font-size:28px; margin-bottom:18px; }
.cols p, .cols li { font-size:16px; color:#2a2a28; }
.cols ul { padding-left:20px; margin:16px 0 0; }
.cols li { margin-bottom:10px; }
.cov-grid { display:grid; grid-template-columns:repeat(4, 1fr); gap:24px; margin:0; padding:0; list-style:none; }
.cov { display:flex; flex-direction:column; text-decoration:none; height:100%; }
.cov .src { display:block; margin:14px 0 4px; color:var(--muted); font-size:14px; font-weight:700; }
.cov .hl { display:block; font-size:16px; line-height:1.4; font-weight:700; }
a.cov:hover .hl { text-decoration:underline; text-decoration-color:var(--accent); text-decoration-thickness:2px; }
.pager { display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; padding-block:40px; }
.pager a { text-decoration:none; font-weight:800; }
.pager small { display:block; color:var(--muted); font-weight:600; font-size:14px; }

.prose { max-width:720px; }
.prose h2 { font-size:28px; margin:44px 0 14px; }
.prose p, .prose li { font-size:18px; line-height:1.7; color:#2a2a28; }
.prose ul { padding-left:22px; margin:0 0 16px; }
.prose li { margin-bottom:8px; }
.takeaway { background:var(--soft); border-left:4px solid var(--accent); border-radius:0 10px 10px 0; padding:20px 24px; margin:0 0 8px; }
.takeaway b { display:block; font-size:14px; color:var(--accent); margin-bottom:6px; }
.takeaway p { margin:0; }
.faq h3 { font-size:19px; margin:26px 0 6px; }
.prose ol.steps { list-style:none; counter-reset:step; padding:0; margin:0 0 16px; }
.prose ol.steps li { counter-increment:step; position:relative; padding-left:48px; margin-bottom:18px; }
.prose ol.steps li::before { content:counter(step); position:absolute; left:0; top:2px; width:32px; height:32px; border-radius:50%; background:var(--ink); color:#fff; font-size:15px; font-weight:800; display:grid; place-items:center; }
.prose ol.steps b { display:block; }
.prose a { color:var(--accent); }
.tool-cta { display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:16px 24px; background:var(--ink); color:#fff; border-radius:12px; padding:22px 24px; margin:28px 0 8px; }
.tool-cta p { color:var(--dark-muted); margin:4px 0 0; font-size:16px; line-height:1.5; }
.tool-cta b { font-size:18px; }
.tool-cta div { flex:1 1 280px; }
.prose .tool-cta a.btn { color:var(--btn-ink); }
.related { margin-top:44px; padding-top:8px; border-top:1px solid var(--line); }
.related h2 { font-size:24px; }
.guide-links { font-size:14px; font-weight:700; margin:-10px 0 22px; color:var(--muted); }
.guide-links a { color:var(--accent); }
.meta-line { color:var(--dark-muted); font-size:15px; margin:0; display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
.avatar { border-radius:50%; object-fit:cover; display:block; flex:none; }
.wlist { list-style:none; margin:0; padding:0; }
.wlist li { border-top:2px solid var(--ink); }
.wlist li:last-child { border-bottom:1px solid var(--line); }
.wlist a { display:grid; grid-template-columns:1fr auto; gap:8px 32px; padding:26px 0; text-decoration:none; }
.wlist a:hover h3 { text-decoration:underline; text-decoration-color:var(--accent); text-decoration-thickness:2px; }
.wlist h3 { font-size:24px; margin:0 0 6px; letter-spacing:-0.015em; }
.wlist p { margin:0; color:#3b3b38; font-size:16px; }
.wlist .when { color:var(--muted); font-size:14px; white-space:nowrap; }
.tool-list { list-style:none; margin:0; padding:0; }
.tool-card .body { gap:0; }
.tool-card h2.name { font-size:24px; margin:0 0 8px; }
.tool-art { display:grid; place-items:center; aspect-ratio:16/9; background:var(--ink); overflow:hidden; }
.tool-icons { display:flex; gap:14px; }
.tool-icons svg { width:64px; height:64px; padding:16px; border-radius:50%; background:var(--accent-d); color:var(--btn-ink); transition:transform .25s; }
.tool-card:hover .tool-icons svg { transform:translateY(-3px); }
.tags { display:flex; flex-wrap:wrap; gap:6px; list-style:none; margin:0 0 22px; padding:0; }
.tags li { font-size:13px; font-weight:700; padding:3px 10px; border-radius:999px; background:var(--soft); color:#3b3b38; }
.tool-card .btn { align-self:flex-start; margin-top:auto; }
.sr { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
.tools-more { margin-top:64px; padding-top:28px; border-top:2px solid var(--ink); max-width:720px; }
.tools-more h2 { font-size:28px; margin-bottom:12px; }
.tools-more p { color:#3b3b38; }
.hd-right { display:flex; align-items:center; gap:28px; flex-wrap:wrap; }
.lang { display:flex; gap:4px; font-size:13px; font-weight:800; }
.lang a, .lang span { padding:5px 9px; border-radius:6px; text-decoration:none; }
.lang a { color:#a9a9a4; border:1px solid #3a3a3a; }
.lang a:hover { color:#fff; border-color:#fff; }
.lang span { background:#fff; color:#0a0a0a; border:1px solid #fff; }
.sources { margin-top:44px; padding-top:8px; border-top:1px solid var(--line); }
.sources h2 { font-size:24px; }
.sources li { font-size:16px; line-height:1.55; }
.sources a { color:var(--accent); }
@media (max-width: 960px) {
  .hero .wrap, .case-hero .wrap { grid-template-columns:1fr; }
  .hero-art { justify-self:start; max-width:220px; margin-top:8px; }
  .about, .cols, .marcomm { grid-template-columns:1fr; gap:32px; }
  .stats { grid-template-columns:1fr 1fr; }
  .services, .cards { grid-template-columns:1fr 1fr; }
  .cov-grid { grid-template-columns:1fr 1fr; }
  .rows li { grid-template-columns:1fr; gap:2px; }
  .rows .when { text-align:left; }
  .wlist a { grid-template-columns:1fr; }
  footer.site .cols3 { grid-template-columns:1fr 1fr; }
}
@media (max-width: 600px) {
  body { font-size:16px; }
  .services, .cards, .cov-grid { grid-template-columns:1fr; }
  .stats { grid-template-columns:1fr 1fr; }
  .mc-stats { grid-template-columns:1fr 1fr; gap:28px 16px; }
  .logo-thumb { aspect-ratio:16/9; }
  .service svg { width:56px; height:56px; margin-bottom:16px; }
  .stats { gap:28px; }
  nav ul { gap:4px 18px; }
  nav a { font-size:15px; }
  footer.site .cols3 { grid-template-columns:1fr; }
}
@media (prefers-reduced-motion: reduce) { * { transition:none !important; scroll-behavior:auto !important; } }
"""

# Privacy-friendly traffic counter (GoatCounter): no cookies, no personal data.
# Dashboard: https://rizky-wicaksono.goatcounter.com
GOATCOUNTER = '<script data-goatcounter="https://rizky-wicaksono.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'


def img_for(url):
    """The article's own preview image (hotlinked, never copied), or None."""
    return (IMAGES.get(url) or {}).get("image") if url else None


def cover_of(c):
    for _src, _hl, url in c["coverage"]:
        i = img_for(url)
        if i:
            return i
    return None


MARKS = {"JAFF Market": "JM", "DAIKIN Indonesia": "DAIKIN", "PT DFI Retail Nusantara Tbk": "DFI", "Guardian Indonesia": "G",
         "PT CRIF Lembaga Informasi Keuangan (CLIK)": "CLIK", "Trinity Entertainment Group": "TEG", "CropLife Indonesia": "CLID"}


def initials(name):
    return MARKS.get(name, name[:2].upper())


def short(s):
    return s if len(s) <= 14 else s.split()[0]


def thumb(src, fallback, extra="", pre=""):
    if src and not src.startswith("http"):
        src = pre + src.lstrip("/")  # local image: assets/img/x.jpg (the CMS may write /assets/img/x.jpg)
    img = f'<img src="{e(src)}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">' if src else ""
    return f'<span class="thumb">{extra}<span class="fb" aria-hidden="true">{e(fallback)}</span>{img}</span>'


def logo_thumb(c, pre="", radius=""):
    """Client logo, centred on a plain tile. Falls back to the client's initials when no logo file exists."""
    p = logo_path(c["slug"])
    st = f' style="{radius}"' if radius else ""
    if not p:
        return f'<span class="logo-thumb"{st}><span class="fb" aria-hidden="true">{e(initials(c["name"]))}</span></span>'
    return f'<span class="logo-thumb"{st}><img src="{pre}{p}" alt="{e(c["name"])} logo"></span>'


# DESCS and TITLE_NAME (case page descriptions and short names) come from the case files via data.py


import posixpath
import re
from i18n import NAV, CHROME, MONTHS, HOME, CASE_ID, EXPERIENCE_ID, TOOLS
from content import load_articles

ARTICLES = load_articles()

LANGS = ("en", "id")


def rel(cur, target):
    """Relative link from page `cur` (a public directory path such as /work/x/) to file `target` (+ optional #fragment)."""
    frag = ""
    if "#" in target:
        target, frag = target.split("#", 1)
        frag = "#" + frag
    cur_dir = cur if cur.endswith("/") else posixpath.dirname(cur)
    cur_dir = cur_dir.rstrip("/") or "/"
    r = posixpath.relpath(target, cur_dir)
    return r + frag


def home_file(lang):
    return "/index.html" if lang == "en" else "/id/index.html"


def guides_file(lang):
    return "/guides/index.html" if lang == "en" else "/id/guides/index.html"


def tools_file(lang):
    return "/tools/index.html" if lang == "en" else "/id/tools/index.html"


def article_file(a, lang):
    base = "/guides" if lang == "en" else "/id/guides"
    return f"{base}/{a['slug'][lang]}/index.html"


def arts(lang, tool=None):
    """Articles that exist in this language; tool=False only PR guides, tool=True only tool how-tos."""
    return [a for a in ARTICLES if lang in a and (tool is None or bool(a.get("tool")) == tool)]


def hl(al, lang):
    return "" if al == lang else ' hreflang="en"'


def slug_article(slug):
    return next(a for a in ARTICLES if a["slug"]["en"] == slug)


def public(file):
    """Public URL of a built file: index.html becomes its folder."""
    return BASE + file[: -len("index.html")]


def dir_of(file):
    return file[: -len("index.html")]


def nice_date(iso, lang="en"):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[lang][int(m) - 1]} {y}"


def cur_attr(path, file):
    return ' aria-current="page"' if path == dir_of(file) else ""


def head(title, desc, path, extra="", pre=None, lang="en", alt=None, gsv=False):
    """path is the public folder path of the page. alt maps language -> built file for the translated pair."""
    C = CHROME[lang]
    N = NAV[lang]
    url = BASE + path
    pre = rel(path, "/index.html")[: -len("index.html")] if pre is None else pre
    GSV = '<meta name="google-site-verification" content="tG3gmLb30_hhg8Ap8CPv2WYpMAD_VgxuqS5mDeFNg74">' if gsv else ""
    hreflang = ""
    locale_alt = ""
    if alt:
        hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{public(f)}">\n' for l, f in alt.items())
        hreflang += f'<link rel="alternate" hreflang="x-default" href="{public(alt["en"])}">\n'
        other = "id" if lang == "en" else "en"
        locale_alt = f'<meta property="og:locale:alternate" content="{CHROME[other]["locale"]}">\n'
    # language switcher: pair if there is one, otherwise the other language's home page
    def target(l):
        if alt:
            return alt[l]
        return home_file(l)
    sw = []
    for l in LANGS:
        if l == lang:
            sw.append(f'<span lang="{l}" aria-current="true">{l.upper()}</span>')
        else:
            sw.append(f'<a lang="{l}" hreflang="{l}" href="{rel(path, target(l))}" aria-label="{"Bahasa Indonesia" if l == "id" else "English"}">{l.upper()}</a>')
    home = home_file(lang)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{hreflang}<meta name="author" content="Rizky Wicaksono">
{GSV}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Rizky Wicaksono">
<meta property="og:locale" content="{C['locale']}">
{locale_alt}<meta property="og:image" content="{BASE}/share-v2.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/share-v2.png">
<meta name="theme-color" content="#0a0a0a">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
{FONTS}<link rel="stylesheet" href="{pre}style.css">
{extra}{GOATCOUNTER}</head>
<body>
<a class="skip" href="#main">{C['skip']}</a>
<div class="dark">
<header class="site"><div class="wrap">
  <a class="brand" href="{rel(path, home)}"><i aria-hidden="true"></i>Rizky Wicaksono</a>
  <div class="hd-right">
    <nav aria-label="Main"><ul>
      <li><a href="{rel(path, home + '#work')}">{N['work']}</a></li>
      <li><a href="{rel(path, tools_file(lang))}"{cur_attr(path, tools_file(lang))}>{N['tools']}</a></li>
      <li><a href="{rel(path, guides_file(lang))}"{cur_attr(path, guides_file(lang))}>{N['guides']}</a></li>
      <li><a href="{rel(path, home + '#contact')}">{N['contact']}</a></li>
    </ul></nav>
    <div class="lang" role="group" aria-label="Language">{''.join(sw)}</div>
  </div>
</div></header>
"""


def foot(path, lang="en"):
    C = CHROME[lang]
    home = home_file(lang)
    return f"""<footer class="site"><div class="wrap">
  <div class="cols3">
    <div>
      <img class="avatar" src="{rel(path, '/assets/img/rizky-wicaksono.jpg')}" alt="Rizky Wicaksono" width="48" height="48" loading="lazy" style="width:48px;height:48px;margin-bottom:14px">
      <a class="brand" href="{rel(path, home)}" style="color:#fff"><i aria-hidden="true"></i>Rizky Wicaksono</a>
      <p style="margin-top:14px">{C['tag']}</p>
      <p class="note">{C['note']}</p>
    </div>
    <div><h4>{C['site']}</h4><ul>
      <li><a href="{rel(path, home + '#about')}">{C['about']}</a></li>
      <li><a href="{rel(path, home + '#work')}">{C['work']}</a></li>
      <li><a href="{rel(path, tools_file(lang))}">{C['tools']}</a></li>
      <li><a href="{rel(path, guides_file(lang))}">{C['guides']}</a></li>
      <li><a href="{rel(path, home + '#contact')}">{C['contact']}</a></li></ul></div>
    <div><h4>{C['elsewhere']}</h4><ul>
      <li><a href="{LINKEDIN}" rel="me noopener">LinkedIn</a></li>
      <li><a href="mailto:rizky.wcaksono@gmail.com">{C['email']}</a></li></ul></div>
  </div>
  <p style="margin:28px 0 0"><small>&copy; 2026 Rizky Wicaksono</small></p>
</div></footer>
</body>
</html>
"""


PERSON = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Rizky Wicaksono", "inLanguage": ["en", "id"]},
        {"@type": "ProfilePage", "@id": BASE + "/#profilepage", "url": BASE + "/", "inLanguage": "en", "isPartOf": {"@id": BASE + "/#website"}, "mainEntity": {"@id": BASE + "/#person"}, "dateModified": "2026-11-25"},
        {"@type": "ProfilePage", "@id": BASE + "/id/#profilepage", "url": BASE + "/id/", "inLanguage": "id", "isPartOf": {"@id": BASE + "/#website"}, "mainEntity": {"@id": BASE + "/#person"}, "dateModified": "2026-11-25"},
        {"@type": "Person", "@id": BASE + "/#person", "name": "Rizky Wicaksono", "givenName": "Rizky", "familyName": "Wicaksono",
         "jobTitle": "Public Relations Consultant",
         "image": BASE + "/assets/img/rizky-wicaksono.jpg",
         "worksFor": {"@type": "Organization", "name": "Image Dynamics PR"},
         "description": "Public Relations Consultant in Jakarta specialising in media relations, brand storytelling and integrated campaigns.",
         "url": BASE + "/", "address": {"@type": "PostalAddress", "addressLocality": "Jakarta", "addressCountry": "ID"},
         "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universitas Sriwijaya"},
         "knowsAbout": ["Public Relations", "Media Relations", "Marketing Communications", "Corporate Communications", "Integrated Campaigns", "Integrated Marketing Communications", "Brand Storytelling", "Entertainment PR", "AI-assisted public relations"],
         "sameAs": [LINKEDIN, NOTION, "https://www.instagram.com/rizkyow_", "https://github.com/rizky-wicaksono", "https://rizky-wicaksono.medium.com/"]},
    ],
}


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + "\n</script>\n"


def home(lang="en"):
    T = HOME[lang]
    C = CHROME[lang]
    cur = dir_of(home_file(lang))
    pre = rel(cur, "/index.html")[: -len("index.html")]
    by_slug = {c["slug"]: c for c in CASES}
    link_case = lambda slug: rel(cur, f"/work/{slug}/index.html")
    services = "\n".join(
        f"""    <article class="service">
      <svg viewBox="0 0 72 72" aria-hidden="true">{ICONS[k]}</svg>
      <h3>{e(t)}</h3>
      <p>{e(d)}</p>
      <a class="more" href="{link_case(s)}">{T['see']}{e(by_slug[s]['name'])}</a>
    </article>""" for k, t, d, s in T["services"])
    cards = []
    for c in CASES:
        x = CASE_ID[c["slug"]] if lang == "id" else {"industry": c["industry"], "year": c["year"], "teaser": c["teaser"]}
        cards.append(f"""      <a class="card" href="{link_case(c['slug'])}">
        {logo_thumb(c, pre)}
        <span class="body"><span class="meta">{e(x['industry'])} · {e(x['year'])}</span><span class="name">{e(c['name'])}</span><span class="teaser">{e(x['teaser'])}</span><span class="go">{T['case_go']}</span></span>
      </a>""")
    n = T["notion_card"]
    cards.append(f"""      <a class="card notion" href="{NOTION}" rel="noopener">
        <span class="body"><span class="meta">{n[0]}</span><span class="name">{n[1]}</span><span class="teaser">{n[2]}</span><span class="go">{n[3]}</span></span>
      </a>""")
    wlist = "\n".join(
        f'    <li><a href="{rel(cur, article_file(a, lang))}"><div><h3>{e(a[lang]["title"])}</h3><p>{e(a[lang]["desc"])}</p></div><span class="when">{a[lang]["minutes"]} {C["min"]}</span></a></li>'
        for a in arts(lang, tool=False))
    exp = EXPERIENCE if lang == "en" else EXPERIENCE_ID
    rows = "\n".join(f'      <li><b>{e(r)}</b><span style="color:var(--muted)">{e(w)}</span><span class="when">{e(d)}</span></li>' for r, w, d in exp)
    mc = "\n".join(f'    <div class="stat"><b>{b}</b><span>{l}</span></div>' for b, l in T["mc_stats"])
    work_note = f'\n  <p class="muted" style="margin:-12px 0 28px;color:var(--muted)">{T["work_note"]}</p>' if T["work_note"] else ""
    eng_p = "\n".join(f"      <p>{p}</p>" for p in T["eng_p"])
    eng_li = "\n".join(f"        <li>{x}</li>" for x in T["eng_list"])
    about_p = "\n".join(f"      <p>{p}</p>" for p in T["about_p"])
    hero = f"""<main id="main">
<section class="hero"><div class="wrap">
  <div>
    <p class="label">Rizky Wicaksono</p>
    <h1>{T['h1']}</h1>
    <p class="lead">{T['lead']}</p>
    <div class="actions">
      <a class="btn" href="#contact">{T['btn_cta']}</a>
      <a class="btn ghost" href="#work">{T['btn_work']}</a>
    </div>
  </div>
  <div class="hero-art"><span class="blob"><img src="{pre}assets/hero-peep.svg" alt="{T['hero_alt']}"></span></div>
</div></section>
</div>
"""
    body = f"""
<section class="block" id="about"><div class="wrap">
  <div class="about">
    <div><p class="label">{T['about_label']}</p><h2><span aria-hidden="true">👋</span> {T['about_h2']}</h2>
      <div class="stats">
          <div class="stat"><b>{T['stat_years_value']}</b><span>{T['stat_years']}</span></div>
          <div class="stat"><b>{T['stat_clients_value']}</b><span>{T['stat_clients']}</span></div>
        </div>
    </div>
    <div>
{about_p}
    </div>
  </div>
</div></section>

<section class="block dark" id="marcomm"><div class="wrap marcomm">
  <div>
    <p class="label" style="color:var(--dark-muted)">{T['mc_label']}</p>
    <h2>{T['mc_h2']}</h2>
    <p class="lead">{T['mc_lead']}</p>
    <div class="actions"><a class="btn" href="{link_case('jaff-market')}">{T['mc_btn']}</a></div>
  </div>
  <div class="mc-stats">
{mc}
  </div>
</div></section>

<section class="block" id="engineering"><div class="wrap">
  <div class="about">
    <div>
      <p class="label">{T['eng_label']}</p>
      <h2>{T['eng_h2']}</h2>
      <a class="chip" href="{rel(cur, tools_file(lang))}">{T['eng_chip']} →</a>
    </div>
    <div>
{eng_p}
      <ul class="plain">
{eng_li}
      </ul>
      <p>{T['eng_end']}</p>
    </div>
  </div>
</div></section>

<section class="block soft" id="services"><div class="wrap">
  <h2>{T['services_h2']}</h2>
  <div class="services">
{services}
  </div>
</div></section>

<section class="block" id="work"><div class="wrap">
  <h2>{T['work_h2']}</h2>{work_note}
  <div class="cards">
{chr(10).join(cards)}
  </div>
</div></section>

<section class="block soft" id="experience"><div class="wrap">
  <h2>{T['exp_h2']}</h2>
  <ul class="rows">
{rows}
  </ul>
  <p class="edu">{T['edu']}</p>
</div></section>

<section class="block" id="writing"><div class="wrap">
  <h2>{T['guides_h2']}</h2>
  <ul class="wlist">
{wlist}
  </ul>
  <p style="margin-top:24px"><a class="more" href="{rel(cur, guides_file(lang))}">{T['guides_all']}</a></p>
</div></section>

<section class="talk dark" id="contact"><div class="wrap">
  <h2>{T['talk_h2']}</h2>
  <p class="lead">{T['talk_lead']}</p>
  <div class="actions">
    <a class="btn" href="{LINKEDIN}" rel="me noopener">{T['talk_li']}</a>
    <a class="btn ghost" href="mailto:rizky.wcaksono@gmail.com">{T['talk_mail']}</a>
  </div>
</div></section>
</main>
"""
    extra = ld(PERSON) if lang == "en" else ""
    alt = {"en": home_file("en"), "id": home_file("id")}
    return head(T["title"], T["desc"], cur, extra, None, lang, alt, gsv=(lang == "en")) + hero + body + foot(cur, lang)


def case(i):
    c = CASES[i]
    prev_c = CASES[i - 1] if i > 0 else None
    next_c = CASES[i + 1] if i < len(CASES) - 1 else None
    pre = "../../"
    cover_html = logo_thumb(c, pre, "border-radius:6px;")
    stats = ""
    if c["stats"]:
        stats = '<section class="block" style="padding-block:56px 0"><div class="wrap"><div class="stats" style="margin-top:0">' + "".join(
            f'<div class="stat"><b>{e(n)}</b><span>{e(l)}</span></div>' for n, l in c["stats"]) + "</div></div></section>\n"
    bullets = "".join(f"<li>{e(b)}</li>" for b in c["bullets"])
    cov = []
    for src, hl, url in c["coverage"]:
        s = f'<span class="src">{e(src)}</span>' if src else ""
        t = thumb(img_for(url), short(src) if src else initials(c["name"]), pre=pre)
        inner = f'{t}{s}<span class="hl">{e(hl)}</span>'
        cov.append(f'<li><a class="cov" href="{e(url)}" rel="noopener">{inner}</a></li>' if url else f'<li><span class="cov">{inner}</span></li>')
    pager = '<div class="wrap pager">'
    pager += (f'<a href="../{prev_c["slug"]}/index.html"><small>Previous</small>← {e(prev_c["name"])}</a>' if prev_c else '<span></span>')
    pager += (f'<a href="../{next_c["slug"]}/index.html" style="text-align:right"><small>Next</small>{e(next_c["name"])} →</a>' if next_c else '<a href="../../index.html#work" style="text-align:right"><small>Back</small>All selected work →</a>')
    pager += "</div>"
    top = f"""<main id="main">
<section class="case-hero"><div class="wrap">
  <div>
    <a class="crumb" href="../../index.html#work">← Selected work</a>
    <h1>{e(c['name'])}</h1>
    <ul class="case-meta">
      <li><b>{e(c['industry'])}</b>Industry</li>
      <li><b>{e(c['year'])}</b>Year</li>
      <li><b>{e(c['role'])}</b>Scope</li>
    </ul>
  </div>
  {cover_html}
</div></section>
</div>
"""
    body = f"""{stats}<section class="block" style="padding-block:72px"><div class="wrap cols">
  <div><h2>Background</h2><p>{e(c['background'])}</p></div>
  <div><h2>Challenge</h2><p>{e(c['challenge'])}</p></div>
  <div><h2>Result</h2><p>{e(c['result'])}</p><ul>{bullets}</ul></div>
</div></section>

<section class="block soft" style="padding-block:72px"><div class="wrap">
  <h2>Featured coverage</h2>
  <ul class="cov-grid">
    {chr(10).join(cov)}
  </ul>
</div></section>
{pager}
</main>
"""
    nm = TITLE_NAME.get(c["slug"], c["name"])
    title = f"{nm} case study | Rizky Wicaksono"
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Rizky Wicaksono", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Selected work", "item": BASE + "/#work"},
        {"@type": "ListItem", "position": 3, "name": nm, "item": BASE + f"/work/{c['slug']}/"}]}
    path = f"/work/{c['slug']}/"
    return head(title, DESCS[c["slug"]], path, ld(crumbs), None, "en", None) + top + body + foot(path, "en")


def guides_index(lang="en"):
    C = CHROME[lang]
    cur = dir_of(guides_file(lang))
    items = "\n".join(
        f'    <li><a href="{rel(cur, article_file(a, lang))}"><div><h3>{e(a[lang]["title"])}</h3><p>{e(a[lang]["desc"])}</p></div><span class="when">{nice_date(a[lang]["date"], lang)} · {a[lang]["minutes"]} {C["min"]}</span></a></li>'
        for a in arts(lang, tool=False))
    tool_items = "\n".join(
        f'    <li><a href="{rel(cur, article_file(a, al))}"{hl(al, lang)}><div><h3>{e(a[al]["title"])}{C["en_only"] if al != lang else ""}</h3><p>{e(a[al]["desc"])}</p></div><span class="when">{nice_date(a[al]["date"], lang)} · {a[al]["minutes"]} {C["min"]}</span></a></li>'
        for a in ARTICLES if a.get("tool") for al in [lang if lang in a else "en"])
    top = f"""<main id="main">
<section class="case-hero"><div class="wrap" style="grid-template-columns:1fr">
  <div>
    <a class="crumb" href="{rel(cur, home_file(lang))}">{C['home']}</a>
    <h1>{C['bc_guides']}</h1>
    <p class="lead">{C['guides_lead']}</p>
  </div>
</div></section>
</div>
"""
    body = f"""<section class="block"><div class="wrap">
  <ul class="wlist">
{items}
  </ul>
  <h2 style="margin-top:72px">{C['tool_guides_h']}</h2>
  <p style="color:#3b3b38;max-width:720px">{C['tool_guides_lead']}</p>
  <ul class="wlist">
{tool_items}
  </ul>
</div></section>
</main>
"""
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Rizky Wicaksono", "item": public(home_file(lang))},
        {"@type": "ListItem", "position": 2, "name": C["bc_guides"], "item": public(guides_file(lang))}]}
    alt = {"en": guides_file("en"), "id": guides_file("id")}
    return head(C["guides_title"], C["guides_desc"], cur, ld(crumbs), None, lang, alt) + top + body + foot(cur, lang)


TOOL_ICONS = {  # 24px line icons, drawn in currentColor
    "pdf": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 14h6M9 17.5h4"/>',
    "video": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m10 9 5 3-5 3z"/>',
    "audio": '<path d="M6.5 9v6M10 5v14M13.5 8v8M17 10.5v3"/>',
}


def tools_index(lang="en"):
    C = CHROME[lang]
    cur = dir_of(tools_file(lang))
    cards = []
    for t in TOOLS:
        icons = "".join(f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{TOOL_ICONS[k]}</svg>' for k in t["icons"])
        tags = "".join(f"<li>{e(x)}</li>" for x in t["tags"][lang])
        glinks = ""
        if t.get("guides"):
            parts = []
            for label, slug in t["guides"]:
                ga = slug_article(slug)
                gl = lang if lang in ga else "en"
                parts.append(f'<a href="{rel(cur, article_file(ga, gl))}"{hl(gl, lang)}>{e(label)}<span class="sr"> guide{C["en_only"] if gl != lang else ""}</span></a>')
            glinks = f'<p class="guide-links">{C["tool_guides_label"]}: ' + " · ".join(parts) + "</p>"
        cards.append(f"""    <li class="card tool-card">
      <span class="tool-art" aria-hidden="true"><span class="tool-icons">{icons}</span></span>
      <span class="body">
        <span class="meta">{e(t['kinds'][lang])}</span>
        <h2 class="name">{e(t['name'])}</h2>
        <span class="teaser">{e(t['desc'][lang])}</span>
        <ul class="tags">{tags}</ul>
        {glinks}
        <a class="btn" href="{BASE}{t['url']}">{C['tool_open']}<span class="sr"> {e(t['name'])}</span></a>
      </span>
    </li>""")
    top = f"""<main id="main">
<section class="case-hero"><div class="wrap" style="grid-template-columns:1fr">
  <div>
    <a class="crumb" href="{rel(cur, home_file(lang))}">{C['home']}</a>
    <h1>{C['bc_tools']}</h1>
    <p class="lead">{C['tools_lead']}</p>
  </div>
</div></section>
</div>
"""
    body = f"""<section class="block"><div class="wrap">
  <ul class="cards tool-list">
{chr(10).join(cards)}
  </ul>
  <div class="tools-more">
    <h2>{C['tools_more_h']}</h2>
    <p>{C['tools_more_p']}</p>
    <p><a class="more" href="{rel(cur, home_file(lang) + '#engineering')}">{C['tools_why']}</a></p>
  </div>
</div></section>
</main>
"""
    ldobj = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": C["tools_title"], "url": public(tools_file(lang)), "inLanguage": lang,
         "isPartOf": {"@id": BASE + "/#website"}, "author": {"@id": BASE + "/#person"},
         "hasPart": [{"@type": "WebApplication", "name": t["name"], "url": BASE + t["url"], "description": t["desc"][lang],
                      "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any (web browser)",
                      "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                      "author": {"@id": BASE + "/#person"}} for t in TOOLS]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Rizky Wicaksono", "item": public(home_file(lang))},
            {"@type": "ListItem", "position": 2, "name": C["bc_tools"], "item": public(tools_file(lang))}]}]}
    alt = {"en": tools_file("en"), "id": tools_file("id")}
    return head(C["tools_title"], C["tools_desc"], cur, ld(ldobj), None, lang, alt) + top + body + foot(cur, lang)


def article(a, lang="en"):
    X = a[lang]
    C = CHROME[lang]
    cur = dir_of(article_file(a, lang))
    group = arts(lang, tool=bool(a.get("tool")))
    i = group.index(a)
    prev_a = group[i - 1] if i > 0 else None
    next_a = group[i + 1] if i < len(group) - 1 else None
    secs = "\n".join(f"<h2>{e(h)}</h2>\n{body_html}" for h, body_html in X["sections"])
    T = X.get("tool") if a.get("tool") else None
    howto = None
    if T:
        cta = f"""<div class="tool-cta"><div><b>{e(T['name'])}</b><p>{e(T['pitch'])}</p></div><a class="btn" href="{e(T['url'])}">{C['try_tool']}</a></div>"""
        secs = cta + "\n" + secs
    if X.get("steps"):
        sh, steps = X["steps"]
        lis = "\n".join(f"<li><b>{e(n)}</b>{t}</li>" for n, t in steps)
        secs += f'\n<h2 id="steps">{e(sh)}</h2>\n<ol class="steps">\n{lis}\n</ol>'
        howto = {"@type": "HowTo", "name": sh, "inLanguage": lang,
                 "tool": [{"@type": "HowToTool", "name": T["name"]}] if T else [],
                 "step": [{"@type": "HowToStep", "position": k + 1, "name": n, "text": re.sub(r"<[^>]+>", "", t),
                           "url": public(article_file(a, lang)) + "#steps"} for k, (n, t) in enumerate(steps)]}
    secs += "".join(f"\n<h2>{e(h)}</h2>\n{body_html}" for h, body_html in X.get("after_steps", []))
    if T:
        secs += "\n" + cta
    related = ""
    if T:
        others = [o for o in group if o is not a]
        related = f'<div class="related"><h2>{C["related"]}</h2>\n<ul>\n' + "\n".join(
            f'<li><a href="{rel(cur, article_file(o, lang))}">{e(o[lang]["title"])}</a></li>' for o in others) + "\n</ul></div>"
    faq = "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(ans)}</p>" for q, ans in X["faq"])
    src_items = []
    for title, url in X["sources"]:
        txt = e(title)
        src_items.append(f'<li><a href="{e(url)}" rel="noopener">{txt}</a></li>' if url else f"<li>{txt}</li>")
    sources = f'<div class="sources"><h2>{C["sources"]}</h2>\n<ul>\n' + "\n".join(src_items) + "\n</ul></div>"
    pager = '<div class="wrap pager">'
    pager += (f'<a href="{rel(cur, article_file(prev_a, lang))}"><small>{C["prev"]}</small>← {e(prev_a[lang]["title"])}</a>' if prev_a else "<span></span>")
    pager += (f'<a href="{rel(cur, article_file(next_a, lang))}" style="text-align:right"><small>{C["next"]}</small>{e(next_a[lang]["title"])} →</a>' if next_a else f'<a href="{rel(cur, guides_file(lang))}" style="text-align:right"><small>{C["back"]}</small>{C["all_guides"]}</a>')
    pager += "</div>"
    top = f"""<main id="main">
<section class="case-hero"><div class="wrap" style="grid-template-columns:1fr">
  <div style="max-width:860px">
    <a class="crumb" href="{rel(cur, guides_file(lang))}">{C['back_guides']}</a>
    <h1 style="font-size:clamp(32px,4.6vw,60px)">{e(X["title"])}</h1>
    <p class="meta-line"><img class="avatar" src="{rel(cur, '/assets/img/rizky-wicaksono.jpg')}" alt="Rizky Wicaksono" width="28" height="28" style="width:28px;height:28px"><span>{C['byline']} · {nice_date(X["date"], lang)} · {X["minutes"]} {C["min"]}</span></p>
  </div>
</div></section>
</div>
"""
    body = f"""<article class="block" style="padding-block:56px 40px"><div class="wrap"><div class="prose">
<div class="takeaway"><b>{C['in_short']}</b><p>{e(X["summary"])}</p></div>
{secs}
<div class="faq"><h2>{C['faq']}</h2>
{faq}
</div>
{related}
{sources}
<p style="margin-top:40px"><a class="btn" href="{rel(cur, home_file(lang) + '#contact')}" style="color:var(--btn-ink)">{C['cta']}</a></p>
</div></div></article>
{pager}
</main>
"""
    ldobj = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": X["title"], "description": X["desc"], "inLanguage": lang,
         "datePublished": X["date"], "dateModified": X["date"],
         "author": {"@id": BASE + "/#person"}, "mainEntityOfPage": public(article_file(a, lang))},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Rizky Wicaksono", "item": public(home_file(lang))},
            {"@type": "ListItem", "position": 2, "name": C["bc_guides"], "item": public(guides_file(lang))},
            {"@type": "ListItem", "position": 3, "name": X["title"], "item": public(article_file(a, lang))}]},
        {"@type": "FAQPage", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in X["faq"]]}]}
    if howto:
        ldobj["@graph"].append(howto)
    alt = {"en": article_file(a, "en"), "id": article_file(a, "id")} if all(l in a for l in LANGS) else None
    return head(f"{a['short'][lang]} | Rizky Wicaksono", X["desc"], cur, ld(ldobj), None, lang, alt) + top + body + foot(cur, lang)


def redirect_page(target_file):
    url = public(target_file)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Moved</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<meta name="robots" content="noindex">
</head><body><p>This page has moved to <a href="{url}">{url}</a>.</p></body></html>
"""


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


# ---- build everything
if ROOT != SRC_ROOT:  # a fresh output folder: start clean, then copy the static files
    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)
    os.makedirs(ROOT)
    for name in STATIC:
        src = os.path.join(SRC_ROOT, name)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, os.path.join(ROOT, name))
write("style.css", CSS)
write("index.html", home("en"))
write("id/index.html", home("id"))
for i, c in enumerate(CASES):
    write(f"work/{c['slug']}/index.html", case(i))
for lang in LANGS:
    write(guides_file(lang).lstrip("/"), guides_index(lang))
    write(tools_file(lang).lstrip("/"), tools_index(lang))
    for a in arts(lang):
        write(article_file(a, lang).lstrip("/"), article(a, lang))
# the first version of the guides lived under /writing/: keep those addresses working
write("writing/index.html", redirect_page(guides_file("en")))
for a in arts("en", tool=False):
    write(f"writing/{a['slug']['en']}/index.html", redirect_page(article_file(a, "en")))

pairs = [(home_file("en"), home_file("id")), (tools_file("en"), tools_file("id")), (guides_file("en"), guides_file("id"))] + [(article_file(a, "en"), article_file(a, "id")) for a in ARTICLES if all(l in a for l in LANGS)]
single = [f"/work/{c['slug']}/index.html" for c in CASES] + [article_file(a, l) for a in ARTICLES if not all(x in a for x in LANGS) for l in LANGS if l in a]
def url_entry(file, alt=None):
    s = f"  <url><loc>{public(file)}</loc><lastmod>2026-11-25</lastmod>"
    if alt:
        for l, f in alt.items():
            s += f'<xhtml:link rel="alternate" hreflang="{l}" href="{public(f)}"/>'
        s += f'<xhtml:link rel="alternate" hreflang="x-default" href="{public(alt["en"])}"/>'
    return s + "</url>\n"
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for en_f, id_f in pairs:
    alt = {"en": en_f, "id": id_f}
    sm += url_entry(en_f, alt) + url_entry(id_f, alt)
for f in single:
    sm += url_entry(f)
sm += "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0a0a0a"/><circle cx="32" cy="32" r="14" fill="#6cc4ff"/></svg>\n')
print("built", len(pairs) * 2 + len(single), "pages plus redirects")
