#!/usr/bin/env python3
"""Site-wide data: links, case studies and experience. Used by build.py."""
import html, json, os, sys, textwrap

SRC_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # the repo root
# Output folder: first command-line argument, else _site/ in the repo root.
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(SRC_ROOT, "_site")
STATIC = ["assets", "share-v2.png"]  # copied as-is from the repo root into the output folder
BASE = "https://rizky-wicaksono.github.io"
LINKEDIN = "https://www.linkedin.com/in/rizky-wicaksono"
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

CASES = [
    dict(
        slug="jaff-market", name="JAFF Market", year="2025", industry="Film",
        role="Marketing Communications Assistant Manager",
        teaser="Led marketing communications for a film industry market",
        desc="Case study: 663 media coverages, 8.5M social media views and 1,120 approved business meetings for JAFF Market, the business platform of the Jogja-NETPAC Asian Film Festival.",
        stats=[("663", "Media coverages"), ("8.5M", "Social media views"), ("1,120", "Approved business meetings")],
        background="In 2025, concurrent with my role at Dialogue Communications, I was also appointed as Marketing Communications Assistant Manager for JAFF Market, the business and networking platform of the Jogja-NETPAC Asian Film Festival (JAFF). I led the integrated marketing communications strategy across public relations, social media, branding, website, and documentation, coordinating a team of 36 core members and 26 volunteers.",
        challenge="The main challenge was to strengthen JAFF Market’s visibility and establish it as a credible film industry marketplace, distinct from the festival itself. This required an integrated communication approach that could build industry credibility, expand audience reach, and create a consistent brand experience across digital, media, and on-site touchpoints.",
        result="Through the integrated marketing communications strategy, I helped strengthen JAFF Market’s visibility among industry professionals while expanding its reach to broader audiences. The communication ecosystem also supported the market’s digital participation and business networking objectives.",
        bullets=[
            "Generated 663 media coverages through 9 press releases, 8 thought leadership articles, 13 media interviews/visits, and partnerships with 49 media outlets.",
            "Generated 8.5M social media views, 1.2M reach, and 69.1K interactions, while growing Instagram by 8.8K followers.",
            "Reached 200K+ audiences through 14 KOL collaborations, generating 15K+ engagements.",
            "Reached 68K+ unique website visitors and supported 6,806 platform users, including 1,120 approved business meetings.",
        ],
        coverage=[
            ("Variety", "JAFF Market Partners with Cinepoint to Track Indonesia’s Box Office Surge as Local Films Outpace Hollywood", "https://variety.com/2025/film/news/jaff-market-cinepoint-indonesias-film-boom-1236525440/"),
            ("Screen Daily", "“It is time”: how the fast-growing Indonesian film industry inspired the inaugural JAFF Market", "https://www.screendaily.com/features/it-is-time-how-the-fast-growing-indonesian-film-industry-inspired-the-inaugural-jaff-market/5199619.article"),
            ("Asian Movie Pulse", "JAFF Market Opens Submissions for Filmmakers and Creators Across Asia", "https://asianmoviepulse.com/2025/08/jaff-market-opens-submissions-for-filmmakers-and-creators-across-asia/"),
            ("Antara", "JAFF dorong sineas daftar program JAFF Market untuk jaring koneksi", "https://www.antaranews.com/berita/5065397/jaff-dorong-sineas-daftar-program-jaff-market-untuk-jaring-koneksi"),
        ],
    ),
    dict(
        slug="daikin-indonesia", name="DAIKIN Indonesia", year="2024 to 2025", industry="Consumer and manufacturing",
        role="Communication strategy",
        teaser="Launch campaign for a new factory and its first locally made products",
        desc="Case study: 334+ media coverages, 3 press conferences and 11M+ views for the DAIKIN Indonesia factory launch and the #KeputusanYangTepat campaign.",
        stats=[("334+", "Media coverages"), ("11M+", "Views through KOL collaborations"), ("3", "Press conferences")],
        background="In 2024, I worked on a campaign for DAIKIN Indonesia, supporting the launch of its new factory and first line of locally produced products. The initiative was part of DAIKIN’s broader mission toward carbon neutrality and sustainability. To bring this vision to life, I developed the strategic communication direction for the #KeputusanYangTepat campaign.",
        challenge="The main challenge was to craft a strong narrative that positioned DAIKIN as a leader in sustainable innovation, not just in product quality but also in long-term environmental commitment. This required a 360-degree communication approach, combining branding, influencer engagement, and media relations to deliver consistent messaging across all touchpoints.",
        result="Through this campaign, I helped reinforce DAIKIN’s brand positioning as a trusted, sustainable air solution provider. The initiative successfully built positive media traction, strengthened consumer awareness, and aligned with DAIKIN’s FY24 product strategy, with the campaign continuing through 2025 to support long-term brand growth and innovation.",
        bullets=[
            "Secured 334+ media coverages, including multiple tier-1 outlets.",
            "Organized 3 press conferences and 1 exclusive media interview to amplify key messages.",
            "Reached over 11M+ total views across online platforms through KOL collaborations.",
        ],
        coverage=[
            ("NNA ASIA", "ダイキン、現地生産の家庭用エアコンを発売", "https://www.nna.jp/news/2810704"),
            ("CNBC Indonesia", "100% Diproduksi di RI, AC Nusantara Prestige Resmi Diluncurkan", "https://www.cnbcindonesia.com/tech/20250630134002-37-644922/100-diproduksi-di-ri-ac-nusantara-prestige-resmi-diluncurkan"),
            ("Jakarta Globe", "Daikin Opens $206 Million AC Factory in West Java, Targets Exports by 2027", "https://jakartaglobe.id/business/daikin-opens-206-million-ac-factory-in-west-java-targets-exports-by-2027"),
            ("Cooling Post", "Daikin opens residential AC factory in Indonesia", "https://www.coolingpost.com/world-news/daikin-opens-residential-ac-factory-in-indonesia/"),
        ],
    ),
    dict(
        slug="dfi-retail-nusantara", name="PT DFI Retail Nusantara Tbk", year="2025", industry="Retail",
        role="PR and communication strategy",
        teaser="Corporate rebrand told through Guardian and IKEA",
        desc="Case study: public relations for PT DFI Retail Nusantara Tbk, the company behind Guardian Indonesia and IKEA Indonesia, during its rebrand from Hero Supermarket.",
        stats=[],
        background="Since 2025, I have been responsible for managing public relations and communication strategies for PT DFI Retail Nusantara Tbk, overseeing its two flagship retail brands, Guardian Indonesia and IKEA Indonesia. My focus has been on strengthening brand reputation, amplifying visibility, and maintaining consistent communication across both brands.",
        challenge="When I joined, PT DFI Retail Nusantara Tbk had just transitioned from its previous identity as PT Hero Supermarket Tbk, while still retaining the stock code HERO. The key challenge was to build public and media awareness of the new corporate identity, not by telling the story directly, but by doing so through its consumer-facing brands, Guardian and IKEA. This required a strategic balance: reinforcing the brands’ own narratives while subtly communicating the parent company’s transformation and long-term vision.",
        result="Through integrated communication planning and consistent brand storytelling, I helped strengthen DFI’s visibility and credibility during its transition period.",
        bullets=[
            "Strengthened media relations and press outreach, resulting in continuous tier-1 coverage for DFI, Guardian and IKEA’s initiatives.",
            "Supported DFI’s corporate rebranding efforts by ensuring all communication materials, releases, and campaign narratives aligned with the company’s refreshed positioning.",
        ],
        coverage=[
            ("Kontan", "DFI Retail Dorong Transformasi, Guardian Buka Gerai Berkonsep Inovatif", "https://industri.kontan.co.id/news/dfi-retail-dorong-transformasi-guardian-buka-gerai-berkonsep-inovatif"),
            ("Investor.id", "DFI Retail Nusantara (HERO) Andalkan Guardian Perkuat Pasar Ritel Kesehatan", "https://investor.id/business/410523/dfi-retail-nusantara-hero-andalkan-guardian-perkuat-pasar-ritel-kesehatan"),
            ("SWA", "Guardian dan IKEA Dorong Pendapatan DFI Retail Nusantara (HERO) Tembus Rp2,35 Triliun di Semester I/2025", "https://swa.co.id/read/462228/guardian-dan-ikea-dorong-pendapatan-dfi-retail-nusantara-hero-tembus-rp235-triliun-di-semester-i2025"),
            ("Kontan", "Pola Berubah, Ini Strategi DFI Retail Nusantara (HERO) Hadapi Pelemahan Industri", "https://industri.kontan.co.id/news/pola-berubah-ini-strategi-dfi-retail-nusantara-hero-hadapi-pelemahan-industri"),
        ],
    ),
    dict(
        slug="guardian-indonesia", name="Guardian Indonesia", year="2025", industry="Health and beauty retail",
        role="PR strategy",
        teaser="Brand refresh from health store to lifestyle brand",
        desc="Case study: public relations for Guardian Indonesia as it refreshed its identity from a traditional health store to an interactive lifestyle brand.",
        stats=[],
        background="As part of my role managing PT DFI Retail Nusantara Tbk’s communications portfolio, I also manage the Public Relations strategy for Guardian Indonesia, one of Indonesia’s leading health and beauty retailers. The main objective was to strengthen Guardian’s brand positioning as an accessible yet trusted wellness destination, while keeping the brand relevant and engaging to both loyal and new consumers.",
        challenge="Guardian was transforming to refresh its brand identity, shifting from being perceived as a traditional health store to becoming a vibrant, interactive lifestyle brand. The challenge was to communicate this evolution across multiple channels, ensuring consistency between in-store experiences, media exposure, and digital engagement, while maintaining the brand’s trust and credibility in the wellness category.",
        result="Through strategic storytelling and consistent brand communication, I helped redefine Guardian’s public image and increase its media visibility across health, lifestyle, and business publications.",
        bullets=[
            "Developed and executed press release and media engagement plans highlighting new store concepts, product innovation, and consumer experiences.",
            "Strengthened media relations, ensuring continuous exposure aligned with the brand’s direction.",
        ],
        coverage=[
            ("Tempo", "Dukung Gaya Hidup Sehat, 8.500 Pelari Ramaikan Guardian Run 2025", "https://www.tempo.co/gaya-hidup/dukung-gaya-hidup-sehat-8-500-pelari-ramaikan-guardian-run-2025-2071982"),
            ("Antara", "Guardian Indonesia perluas akses sanitasi sekolah untuk kesehatan anak", "https://www.antaranews.com/berita/4968881/guardian-indonesia-perluas-akses-sanitasi-sekolah-untuk-kesehatan-anak"),
            ("IDN Times", "Wajah Baru Guardian Plaza Indonesia, Fresh dan Lebih Luas!", "https://www.idntimes.com/life/women/wajah-baru-guardian-plaza-indonesia-00-rqp85-vsxhs2"),
            ("Marketeers", "Guardian Buka Kembali Gerai di Plaza Indonesia Jadi Makin Imersif", "https://www.marketeers.com/guardian-buka-kembali-gerai-di-plaza-indonesia-jadi-makin-imersif/"),
        ],
    ),
    dict(
        slug="crif-clik", name="PT CRIF Lembaga Informasi Keuangan (CLIK)", year="2024", industry="Financial services",
        role="PR and communication strategy",
        teaser="Explained a B2B credit brand to the media",
        desc="Case study: public relations and thought leadership for CRIF Lembaga Informasi Keuangan (CLIK), a credit information and business analytics company in Indonesia.",
        stats=[],
        background="In 2024, I managed the public relations and communication strategy for PT CRIF Lembaga Informasi Keuangan (CLIK), a leader in credit information and business analytics. CLIK plays a vital role in Indonesia’s financial ecosystem by providing data-driven credit information services that empower financial institutions to make smarter, more responsible lending decisions.",
        challenge="The main challenge was to build public trust and awareness for a B2B brand operating in a highly regulated and technical industry. Many stakeholders, from financial institutions to the media, had limited understanding of CLIK’s function and impact. The communication strategy therefore needed to simplify complex topics around credit information, data analytics, and financial inclusion, while positioning CLIK as a reliable, compliant, and forward-thinking industry leader.",
        result="Through a focused mix of media relations, thought leadership, and strategic storytelling, I successfully elevated CLIK’s visibility and credibility within the financial services sector.",
        bullets=[
            "Crafted and executed press release and media outreach plans to communicate CLIK’s milestones and key partnerships.",
            "Positioned company executives as industry thought leaders, through interviews, op-eds, and expert commentary in top-tier financial media.",
            "Developed content strategies that translated complex financial concepts into accessible narratives for broader audiences.",
        ],
        coverage=[
            ("The Jakarta Post", "OJK to legitimize firms that credit-score the unbanked", None),
            ("", "Menilik Peran Biro Kredit Swasta Memperkuat Akses dan Infrastruktur Kredit", None),
            ("", "Lembaga Keuangan Didorong Perbesar Akses Masyarakat Memperoleh Kredit", None),
            ("", "CLIK Dukung Pemerintah Wujudkan Pemerataan Akses Keuangan untuk UMKM", None),
        ],
    ),
    dict(
        slug="trinity-entertainment-group", name="Trinity Entertainment Group", year="2023", industry="Music and entertainment",
        role="PR and communication",
        teaser="Artist visibility and a youth orchestra’s debut concert",
        desc="Case study: public relations for Trinity Entertainment Group (Trinity Optima Production) and the first public concert of Trinity Youth Symphony Orchestra, The Legends 8.",
        stats=[],
        background="In 2023, I managed public relations and communication initiatives for Trinity Entertainment Group (Trinity Optima Production), one of Indonesia’s leading music and entertainment companies. My key focus was on artist visibility, media engagement, and brand storytelling, while also supporting Trinity Youth Symphony Orchestra (TRUST) in launching their first public concert, The Legends 8.",
        challenge="The challenge was to maintain consistent media presence for a diverse entertainment portfolio from mainstream music artists to a classical youth orchestra, each requiring unique communication strategies. For TRUST, the task was to introduce the orchestra to a wider audience, position it as a credible youth-driven musical ensemble, and drive excitement for their debut concert.",
        result="By combining strong media outreach, creative storytelling, and targeted positioning, I helped amplify both Trinity’s brand voice and TRUST’s concert presence in the public eye.",
        bullets=[
            "Planned and executed the PR strategy for TRUST’s “The Legends 8” concert, including press materials, media relations, and interview coordination.",
            "Secured national media coverage across entertainment and lifestyle platforms.",
            "Strengthened Trinity’s media relationships.",
            "Collaborated closely with internal teams to align messaging between Trinity’s commercial artists and TRUST’s orchestral initiatives.",
        ],
        coverage=[
            ("", "Antusiasme Tinggi Terhadap Orkestra yang Tak Disangka oleh Trinity Youth Symphony Orchestra", None),
            ("", "Cara Trinity Inkubasi Siapkan Figur Baru seperti Afgan dan Maudy Ayunda untuk Gen Z", None),
            ("", "Trinity Optima Production Jadi Perusahaan Label Rekaman Lokal Terbesar di Indonesia", None),
            ("", "Yonathan Nugroho, CEO Trinity Optima: Kiat Trinity Optima Bangkit dari Tekanan Perubahan", None),
        ],
    ),
    dict(
        slug="croplife-indonesia", name="CropLife Indonesia", year="2023", industry="Agriculture and biotechnology",
        role="Communication strategy",
        teaser="Annual content plan on agricultural biotechnology",
        desc="Case study: annual social media and content strategy for CropLife Indonesia, making agricultural biotechnology understandable to the public.",
        stats=[],
        background="In 2023, I had the opportunity to strategize a communication plan for CropLife Indonesia (CLID) under Dialogue Communications, focusing on strengthening public understanding of biotechnology in agriculture. My main objective was to make this complex and often technical topic more accessible to the general public while ensuring alignment with the interests of key stakeholders, from policymakers to farmers.",
        challenge="The main challenge was transforming scientific narratives into engaging, easy-to-digest messages that could resonate with both industry professionals and everyday audiences. Beyond that, I needed to identify credible public figures who could authentically advocate for biotechnology, bridging the gap between awareness and acceptance.",
        result="By combining storytelling with strategic content planning, I helped increase CLID’s social media visibility and audience engagement, ensuring each communication piece served both educational and advocacy purposes. The campaign also successfully positioned CLID as a trusted voice in Indonesia’s agricultural innovation space.",
        bullets=[
            "Developed and executed the annual social media and content strategy, aligning with advocacy goals.",
            "Produced educational digital content that simplified complex biotech narratives for a wider audience.",
            "Secured collaborations with public figures and influencers, amplifying the campaign’s reach and impact.",
        ],
        coverage=[
            ("", "CropLife: Benih bioteknologi diperlukan guna perkuat ketahanan pangan", None),
            ("", "Kerap Gagal Panen, Petani Harus Adopsi Konsep Lebih Modern", None),
            ("", "Pertanian Modern Upaya Menggenjot Produksi Panen", None),
            ("", "Ketahanan Pangan Kian Rapuh, Indonesia Berpotensi Menjadi Importir Beras Terbesar di Dunia", None),
        ],
    ),
]

EXPERIENCE = [
    ("Communications Consultant", "Image Dynamics PR · Netflix Indonesia", "Mar 2026 to now"),
    ("Public Relations Consultant", "Image Dynamics PR · Suzuki Indonesia", "Jan 2026 to now"),
    ("Public Relations Consultant", "Image Dynamics PR · Shell Indonesia", "Now"),
    ("Marketing Communications Assistant Manager", "JAFF Market", "Jun 2025 to Jan 2026"),
    ("Senior Public Relations Consultant", "Dialogue Communications", "Jul 2024 to Jan 2026"),
    ("Junior Public Relations Consultant", "Dialogue Communications", "Jan 2023 to Jun 2024"),
    ("Corporate Communications Intern", "PT Moda Integrasi Transportasi Jabodetabek", "Nov 2022 to Jan 2023"),
    ("Public Relations Intern", "Lifepal", "Jun to Oct 2022"),
    ("Public Relations Intern", "Thamrin Group", "Jun to Jul 2021"),
]

