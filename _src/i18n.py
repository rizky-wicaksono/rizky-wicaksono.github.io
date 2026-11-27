"""Interface text, English and Bahasa Indonesia. Home page copy, cases and tools are loaded from content/."""

from content import load_home, load_tools

NAV = {
    "en": {"about": "About", "work": "Work", "tools": "Tools", "guides": "PR Guides", "contact": "Contact"},
    "id": {"about": "Tentang", "work": "Karya", "tools": "Tools", "guides": "Panduan PR", "contact": "Kontak"},
}

CHROME = {
    "en": {
        "skip": "Skip to content", "tag": "Public relations consultant in Jakarta.",
        "note": "Article images belong to their publishers and link to the original articles. Client names and logos belong to their owners.",
        "site": "Site", "about": "About", "work": "Selected work", "guides": "PR Guides", "contact": "Contact",
        "elsewhere": "Elsewhere", "email": "Email", "notion": "Notion portfolio",
        "in_short": "In short", "faq": "Frequently asked questions", "sources": "Sources and further reading",
        "back_guides": "← PR Guides", "home": "← Home", "prev": "Previous", "next": "Next", "back": "Back", "all_guides": "All guides →",
        "cta": "Plan your next campaign", "min": "min read",
        "byline": "Draft by AI · Reviewed by Rizky Wicaksono", "locale": "en_US",
        "guides_title": "PR Guides | Rizky Wicaksono",
        "guides_desc": "Practical PR guides on press releases, pitching journalists, measuring results and PR for AI search, adjusted for Indonesia.",
        "guides_lead": "Practical guides on public relations, media relations, measurement and PR for AI search, adjusted for Indonesia.",
        "bc_guides": "PR Guides",
        "tools": "Tools", "bc_tools": "Tools", "tool_open": "Open tool",
        "tools_title": "Tools for PR work | Rizky Wicaksono",
        "tools_desc": "Free tools for everyday PR work, built by Rizky Wicaksono with AI. File Shrinker makes PDFs, videos and audio small enough to email; Meeting Minutes Maker turns transcripts into minutes.",
        "tools_lead": "Small, free tools that take the repetitive parts out of PR work. Built with AI as part of my public relations engineering work.",
        "tools_more_h": "More tools are on the way",
        "tools_more_p": "Next on the list are tools for media lists and pitching. They will appear here as each one is ready.",
        "tools_why": "Why I build these",
        "tool_guides_h": "Tool how-tos", "tool_guides_lead": "Step-by-step guides for the tools on the Tools page: what size to aim for, which settings to pick, and why.",
        "tool_guides_label": "Guides", "en_only": "", "related": "Related guides", "try_tool": "Try it free",
    },
    "id": {
        "skip": "Lompat ke konten", "tag": "Konsultan public relations di Jakarta.",
        "note": "Gambar artikel adalah milik penerbitnya dan terhubung ke artikel aslinya. Nama klien dan logo adalah milik pemiliknya.",
        "site": "Situs", "about": "Tentang", "work": "Karya pilihan", "guides": "Panduan PR", "contact": "Kontak",
        "elsewhere": "Di tempat lain", "email": "Email", "notion": "Portofolio Notion",
        "in_short": "Ringkasnya", "faq": "Pertanyaan yang sering diajukan", "sources": "Sumber dan bacaan lanjutan",
        "back_guides": "← Panduan PR", "home": "← Beranda", "prev": "Sebelumnya", "next": "Berikutnya", "back": "Kembali", "all_guides": "Semua panduan →",
        "cta": "Rencanakan kampanye berikutnya", "min": "menit baca",
        "byline": "Draf oleh AI · Ditinjau oleh Rizky Wicaksono", "locale": "id_ID",
        "guides_title": "Panduan PR | Rizky Wicaksono",
        "guides_desc": "Panduan PR praktis tentang siaran pers, pitching ke wartawan, pengukuran hasil, dan PR untuk pencarian AI, disesuaikan untuk Indonesia.",
        "guides_lead": "Panduan praktis tentang public relations, media relations, pengukuran, dan PR untuk pencarian AI, disesuaikan untuk Indonesia.",
        "bc_guides": "Panduan PR",
        "tools": "Tools", "bc_tools": "Tools", "tool_open": "Buka alat",
        "tools_title": "Tools untuk kerja PR | Rizky Wicaksono",
        "tools_desc": "Alat gratis untuk kerja PR sehari-hari, dibuat Rizky Wicaksono dengan AI. File Shrinker mengecilkan PDF, video, dan audio supaya muat dikirim lewat email; Pembuat Notulen Rapat mengubah transkrip jadi notulen.",
        "tools_lead": "Alat kecil dan gratis yang memangkas bagian repetitif dari kerja PR. Dibuat dengan AI sebagai bagian dari kerja public relations engineering saya.",
        "tools_more_h": "Alat lain menyusul",
        "tools_more_p": "Berikutnya adalah alat untuk daftar media dan pitching. Semuanya akan muncul di sini begitu siap.",
        "tools_why": "Kenapa saya membuat ini",
        "tool_guides_h": "Panduan alat", "tool_guides_lead": "Panduan langkah demi langkah untuk alat di halaman Tools: ukuran yang perlu dikejar, pengaturan yang dipilih, dan alasannya.",
        "tool_guides_label": "Panduan", "en_only": " (English)", "related": "Panduan terkait", "try_tool": "Coba gratis",
    },
}

MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "id": ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
}

# Home page copy: content/home/en.yml and content/home/id.yml (edited with Pages CMS)
HOME = {lang: load_home(lang)[0] for lang in ("en", "id")}

# Card text on the Indonesian home page: the `id` block in each content/cases/<slug>.yml (CASE_ID, from data.py)
from data import CASE_ID  # noqa: E402

EXPERIENCE_ID = load_home("id")[1]

# Tools page: one card per tool, from content/tools.yml (edited with Pages CMS). url is the tool's address on this domain.
TOOLS = load_tools()
