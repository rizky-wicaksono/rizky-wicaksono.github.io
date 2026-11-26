# rizky-wicaksono.github.io

Personal site of Rizky Wicaksono, built from `_src/` (Python) and `content/` (the guides, in Markdown).

## Mengedit panduan lewat Pages CMS (Bahasa Indonesia)

1. Buka [app.pagescms.org](https://app.pagescms.org), masuk dengan akun GitHub, lalu pilih repo `rizky-wicaksono.github.io`.
2. Di menu kiri pilih **Guides (English)** atau **Panduan (Bahasa Indonesia)**, lalu klik artikel yang ingin diubah.
3. Ubah judul, ringkasan, isi artikel, langkah-langkah, FAQ, atau sumber. Di isi artikel, setiap bagian diawali **Heading 2**. Paragraf yang hanya berisi `[[steps]]` menandai tempat langkah-langkah bernomor muncul; jangan dihapus.
4. Klik **Save**. Pages CMS menyimpan perubahan sebagai commit ke GitHub. GitHub Actions ("Build and deploy site") lalu membangun ulang situs dan menerbitkannya, biasanya dalam 1–2 menit. Progresnya terlihat di tab **Actions** di GitHub.

Artikel baru: buat di kedua koleksi, isi **Translation key** dengan nama file versi Inggris (tanpa `.md`) dan **Order** dengan angka yang sama di kedua bahasa. Nama file menjadi alamat halaman, jadi pakai huruf kecil dan tanda hubung.

## Editing the guides with Pages CMS (English)

1. Go to [app.pagescms.org](https://app.pagescms.org), sign in with GitHub and pick the `rizky-wicaksono.github.io` repo.
2. Choose **Guides (English)** or **Panduan (Bahasa Indonesia)** on the left, then open an article.
3. Edit the title, summary, article body, steps, FAQ or sources. In the body, each section starts with a **Heading 2**. A paragraph containing only `[[steps]]` marks where the numbered steps appear; keep it.
4. Click **Save**. Pages CMS commits the change to GitHub, and the "Build and deploy site" GitHub Action rebuilds and publishes the site, usually within a minute or two. You can follow it in the **Actions** tab.

New article: create it in both collections, set **Translation key** to the English file name (without `.md`) and use the same **Order** number in both languages. The file name becomes the page address, so use lowercase words joined by hyphens.

## Building locally

```bash
pip install -r _src/requirements.txt
python _src/build.py
```

The site is written to `_site/`. Case studies, the home page and page chrome are in `_src/data.py` and `_src/i18n.py`; images are in `assets/`.
