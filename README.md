# rizky-wicaksono.github.io

Personal site of Rizky Wicaksono, built from `_src/` (Python) and `content/` (all editable text: home page, case studies, tools and guides).

## Apa saja yang bisa diedit / What you can edit

| Di Pages CMS / In Pages CMS | File | Isi / Contents |
| --- | --- | --- |
| Beranda (Bahasa Indonesia), Home page (English) | `content/home/id.yml`, `content/home/en.yml` | Semua teks beranda, termasuk angka, layanan, dan pengalaman / All home page text, incl. stats, services, experience |
| Studi kasus / Case studies | `content/cases/<slug>.yml` | Satu file per klien, termasuk liputan dan teks kartu Indonesia / One file per client, incl. coverage and the Indonesian card text |
| Tools | `content/tools.yml` | Kartu di halaman Tools / Cards on the Tools page |
| Guides (English), Panduan (Bahasa Indonesia) | `content/guides/<lang>/<slug>.md` | Panduan PR dan panduan alat / PR guides and tool how-tos |
| (kode / code) | `meeting-minutes/` | Alat Pembuat Notulen Rapat, disalin apa adanya ke `/meeting-minutes/` / The Meeting Minutes Maker tool, copied as-is to `/meeting-minutes/`. See its README. |

Teks tombol navigasi, footer, dan label kecil lainnya masih ada di `_src/i18n.py`. / Navigation, footer and other small interface labels are still in `_src/i18n.py`.

## Mengedit lewat Pages CMS (Bahasa Indonesia)

1. Buka [app.pagescms.org](https://app.pagescms.org), masuk dengan akun GitHub, lalu pilih repo `rizky-wicaksono.github.io`.
2. Di menu kiri pilih bagian yang ingin diubah, misalnya **Beranda (Bahasa Indonesia)**, **Studi kasus**, atau **Panduan (Bahasa Indonesia)**.
3. Untuk panduan: ubah judul, ringkasan, isi artikel, langkah-langkah, FAQ, atau sumber. Di isi artikel, setiap bagian diawali **Heading 2**. Paragraf yang hanya berisi `[[steps]]` menandai tempat langkah-langkah bernomor muncul; jangan dihapus.
4. Klik **Save**. Pages CMS menyimpan perubahan sebagai commit ke GitHub. GitHub Actions ("Build and deploy site") lalu membangun ulang situs dan menerbitkannya, biasanya dalam 1–2 menit. Progresnya terlihat di tab **Actions** di GitHub.

Artikel baru: buat di kedua koleksi, isi **Translation key** dengan nama file versi Inggris (tanpa `.md`) dan **Order** dengan angka yang sama di kedua bahasa. Nama file menjadi alamat halaman, jadi pakai huruf kecil dan tanda hubung.

## Editing with Pages CMS (English)

1. Go to [app.pagescms.org](https://app.pagescms.org), sign in with GitHub and pick the `rizky-wicaksono.github.io` repo.
2. Pick what to edit on the left, for example **Home page (English)**, **Case studies** or **Guides (English)**.
3. For guides: edit the title, summary, article body, steps, FAQ or sources. In the body, each section starts with a **Heading 2**. A paragraph containing only `[[steps]]` marks where the numbered steps appear; keep it.
4. Click **Save**. Pages CMS commits the change to GitHub, and the "Build and deploy site" GitHub Action rebuilds and publishes the site, usually within a minute or two. You can follow it in the **Actions** tab.

New article: create it in both collections, set **Translation key** to the English file name (without `.md`) and use the same **Order** number in both languages. The file name becomes the page address, so use lowercase words joined by hyphens.

## Building locally

```bash
pip install -r _src/requirements.txt
python _src/build.py
```

The site is written to `_site/`. Interface labels are in `_src/i18n.py`, layout and CSS in `_src/build.py`; images are in `assets/`.
