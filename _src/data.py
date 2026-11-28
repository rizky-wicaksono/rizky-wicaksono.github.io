#!/usr/bin/env python3
"""Site-wide data: links, case studies and experience. Used by build.py."""
import html, json, os, sys, textwrap

from content import load_cases, load_home

SRC_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # the repo root
# Output folder: first command-line argument, else _site/ in the repo root.
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(SRC_ROOT, "_site")
STATIC = ["assets", "share-v2.png", "meeting-minutes"]  # meeting-minutes/ is the Meeting Minutes Maker tool, served at /meeting-minutes/  # copied as-is from the repo root into the output folder
BASE = "https://rizky-wicaksono.github.io"
LINKEDIN = "https://www.linkedin.com/in/rizky-wicaksono"
EMAIL = "rizky.wcaksono@gmail.com"
NOTION = "https://rizkywcaksono.notion.site/Rizky-Wicaksono-Selected-Works-in-Communications-289a1011ab8a80149838f9cf12a1e07d"
e = html.escape


def logo_path(slug):
    """A client logo dropped in assets/logos/<slug>.(svg|png|webp|jpg) is shown on a light tile."""
    for ext in ("svg", "png", "webp", "jpg"):
        if os.path.exists(os.path.join(SRC_ROOT, "assets", "logos", f"{slug}.{ext}")):
            return f"assets/logos/{slug}.{ext}"
    return None


def logo_tile(c, pre=""):
    p = logo_path(c["slug"])
    return f'<span class="logo-tile"><img src="{pre}{p}" alt="{e(c["name"])} logo"></span>' if p else ""

# Case studies: content/cases/<slug>.yml (edited with Pages CMS)
CASES, CASE_ID, DESCS, TITLE_NAME, IMAGES = load_cases()

# Experience rows: the `experience` list in content/home/en.yml
EXPERIENCE = load_home("en")[1]

