"""Loads the site content from content/: home page text, case studies, tools and the guides.

Guides: loaded from content/guides/<lang>/<slug>.md (YAML frontmatter + HTML body).

These files are what Pages CMS edits. Each file is one article in one language; the English and
Indonesian versions of the same article share the same `key` (the English slug). The file name is the slug.

Body format: each section starts with an <h2> heading (a "## Heading" line also works). A paragraph that
contains only [[steps]] marks where the numbered steps from the frontmatter go; sections after it come
after the steps. Everything else in the body is kept as written (HTML).
"""
import glob, html, os, re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "..", "content", "guides")
LANGS = ("en", "id")

_FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.S)
_H2 = re.compile(r"^(?:<h2[^>]*>(.*?)</h2>|##[ \t]+(.+?))[ \t]*$", re.M)
_STEPS = re.compile(r"^[ \t]*(?:<p>)?\s*\[\[steps\]\]\s*(?:</p>)?[ \t]*$", re.M)


def _sections(text):
    """Split HTML into [(heading, body_html)] at each <h2> or ## line."""
    out = []
    marks = list(_H2.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        heading = m.group(1) if m.group(1) is not None else m.group(2)
        heading = html.unescape(re.sub(r"<[^>]+>", "", heading)).strip()
        out.append((heading, text[m.end():end].strip()))
    return out


def _parse(path):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    m = _FM.match(raw)
    if not m:
        raise ValueError(f"{path}: missing --- frontmatter ---")
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    parts = _STEPS.split(body, maxsplit=1)
    X = {
        "title": fm["title"], "desc": fm["desc"], "summary": fm["summary"],
        "date": str(fm["date"]), "minutes": fm["minutes"],
        "sources": [(s["title"], s.get("url") or "") for s in fm.get("sources") or []],
        "sections": _sections(parts[0]),
        "faq": [(f["q"], f["a"]) for f in fm.get("faq") or []],
    }
    if fm.get("steps"):  # numbered steps; they go where [[steps]] is in the body (or at the end)
        X["steps"] = (fm.get("steps_title") or "", [(s["title"], s["text"]) for s in fm["steps"]])
    if len(parts) > 1:
        X["after_steps"] = _sections(parts[1])
    tool = fm.get("tool") or {}
    if tool.get("name"):  # the CMS may save an empty tool box on PR guides; only a named tool counts
        X["tool"] = {k: tool.get(k) or "" for k in ("name", "url", "kind", "pitch")}
    return fm, X


def load_articles():
    """Returns articles in the shape build.py expects:
    {"slug": {lang: slug}, "short": {lang: short}, "tool": bool, "order": int, "en": {...}, "id": {...}}"""
    by_key = {}
    for lang in LANGS:
        for path in sorted(glob.glob(os.path.join(CONTENT, lang, "*.md"))):
            fm, X = _parse(path)
            slug = os.path.splitext(os.path.basename(path))[0]
            a = by_key.setdefault(fm.get("key") or slug, {"slug": {}, "short": {}})
            a["slug"][lang] = slug
            a["short"][lang] = fm.get("short") or fm["title"]
            a[lang] = X
            if lang == "en" or "order" not in a:
                a["order"] = fm.get("order", 999)
            a["tool"] = a.get("tool") or bool(X.get("tool"))
    return sorted(by_key.values(), key=lambda a: (a["order"], a["slug"].get("en") or next(iter(a["slug"].values()))))


# ---------------------------------------------------------------- home page, case studies, tools

ROOT_CONTENT = os.path.join(HERE, "..", "content")


def _s(v):
    """Text value from YAML: None becomes "", numbers the CMS may save unquoted become strings."""
    return "" if v is None else str(v)


def _yaml(*parts):
    with open(os.path.join(ROOT_CONTENT, *parts), encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_home(lang):
    """content/home/<lang>.yml -> (HOME[lang] dict as build.py expects, experience rows)."""
    d = _yaml("home", f"{lang}.yml")
    T = {}
    for k, v in d.items():
        if k == "experience":
            continue
        if k == "mc_stats":
            v = [(_s(x["number"]), _s(x["label"])) for x in v or []]
        elif k == "services":
            v = [(_s(x["icon"]), _s(x["title"]), _s(x["text"]), _s(x["case"])) for x in v or []]
        elif k == "notion_card":
            v = tuple(_s((v or {}).get(f)) for f in ("meta", "name", "teaser", "go"))
        elif isinstance(v, list):
            v = [_s(x) for x in v]
        else:
            v = _s(v)
        T[k] = v
    exp = [(_s(x["role"]), _s(x["where"]), _s(x["when"])) for x in d.get("experience") or []]
    return T, exp


def load_cases():
    """content/cases/<slug>.yml -> (CASES list, Indonesian card text by slug, case page descriptions,
    short names for page titles, coverage preview images by article URL)."""
    cases, case_id, descs, title_name, images = [], {}, {}, {}, {}
    for path in glob.glob(os.path.join(ROOT_CONTENT, "cases", "*.yml")):
        slug = os.path.splitext(os.path.basename(path))[0]
        d = _yaml("cases", os.path.basename(path))
        cov = []
        for x in d.get("coverage") or []:
            url = _s(x.get("url")) or None
            cov.append((_s(x.get("outlet")), _s(x.get("headline")), url))
            if url and x.get("image"):
                images[url] = {"image": _s(x["image"])}
        cases.append(dict(
            order=d.get("order", 999), slug=slug, name=_s(d["name"]), year=_s(d.get("year")), industry=_s(d.get("industry")),
            role=_s(d.get("role")), teaser=_s(d.get("teaser")),
            stats=[(_s(x["number"]), _s(x["label"])) for x in d.get("stats") or []],
            background=_s(d.get("background")), challenge=_s(d.get("challenge")), result=_s(d.get("result")),
            bullets=[_s(x) for x in d.get("bullets") or []], coverage=cov))
        x = d.get("card_id") or {}
        case_id[slug] = {k: _s(x.get(k)) for k in ("industry", "year", "teaser")}
        descs[slug] = _s(d.get("desc"))
        if d.get("title_name"):
            title_name[slug] = _s(d["title_name"])
    cases.sort(key=lambda c: (c["order"], c["slug"]))
    return cases, case_id, descs, title_name, images


def load_tools():
    """content/tools.yml -> TOOLS list as build.py expects."""
    out = []
    for t in _yaml("tools.yml").get("tools") or []:
        x = {"slug": _s(t.get("slug")), "url": _s(t["url"]), "name": _s(t["name"]),
             "kinds": {}, "desc": {}, "tags": {}, "icons": [_s(i) for i in t.get("icons") or []]}
        for lang, key in (("en", "english"), ("id", "indonesian")):
            L = t.get(key) or {}
            x["kinds"][lang] = _s(L.get("kinds"))
            x["desc"][lang] = _s(L.get("desc"))
            x["tags"][lang] = [_s(g) for g in L.get("tags") or []]
        if t.get("guides"):
            x["guides"] = [(_s(g["label"]), _s(g["guide"])) for g in t["guides"]]
        out.append(x)
    return out
