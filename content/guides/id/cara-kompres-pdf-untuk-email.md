---
key: how-to-compress-a-pdf-for-email
order: 5
title: Cara kompres PDF untuk email supaya deck Anda benar-benar dibuka
short: Cara kompres PDF untuk email (di bawah 25 MB)
desc: Gmail dan Outlook.com membatasi lampiran 25 MB. Ini alasan sebaiknya menargetkan sekitar 18 MB, dan cara mengecilkan deck tanpa membuat teks buram.
summary: 'Gmail dan Outlook.com sama-sama membatasi lampiran 25 MB, dan proses encoding email membuat file sekitar sepertiga lebih besar saat dikirim, jadi targetkan sekitar 18 MB atau kurang. Untuk deck presentasi, kecilkan gambarnya saja dan biarkan teks tetap berupa teks: pada deck yang berat, bobotnya biasanya ada di foto, dan slide tetap tajam serta bisa dicari.'
date: '2026-11-25'
minutes: 7
tool:
  name: PDF Compressor
  url: https://rizky-wicaksono.github.io/file-shrinker/pdf.html
  kind: pdf
  pitch: Hanya mengecilkan gambar, teks tetap tajam dan bisa dicari, dengan target bawaan 18 MB. Gratis, dan file tidak pernah keluar dari browser Anda.
sources:
- title: 'Gmail Help: Send attachments with your Gmail message'
  url: https://support.google.com/mail/answer/6584?hl=en
- title: 'Microsoft Support: Sending limits in Outlook.com'
  url: https://support.microsoft.com/en-us/outlook/sending-limits-in-outlook-com
- title: 'Microsoft Learn: Attachment size exceeds the allowable limit (Outlook)'
  url: https://learn.microsoft.com/en-us/troubleshoot/outlook/message-body/attachment-size-exceeds-the-allowable-limit-error
- title: 'RFC 2045, MIME Part One, section 6.8: Base64 content transfer encoding'
  url: https://www.rfc-editor.org/rfc/rfc2045#section-6.8
- title: Kode sumber dan catatan teknis File Shrinker (GitHub)
  url: https://github.com/rizky-wicaksono/file-shrinker
steps_title: Cara kompres PDF untuk email, langkah demi langkah
steps:
- title: Buka PDF Compressor
  text: Buka <a href="https://rizky-wicaksono.github.io/file-shrinker/pdf.html">PDF Compressor</a> di Chrome, Edge, atau Safari. Tidak perlu memasang apa pun dan tidak perlu mendaftar.
- title: Masukkan PDF Anda
  text: Seret file ke halaman, atau klik untuk memilihnya. File dibaca di dalam tab browser dan tidak diunggah.
- title: Biarkan metode di Keep text
  text: Ini pilihan bawaan. Hanya foto dan gambar yang dikecilkan; teks, font, grafik vektor, dan tautan tetap seperti semula.
- title: Pilih tujuan Email (18 MB)
  text: Ini juga bawaan. Alat ini mencoba beberapa tingkat kualitas dan memilih yang paling tajam yang masih muat. Pilih 10 MB atau 5 MB, atau ketik angka sendiri, untuk kotak masuk yang lebih ketat.
- title: Periksa perkiraannya
  text: Alat ini menunjukkan perkiraan ukuran sebelum Anda mulai. Kalau tingkat terkecil pun tidak muat, lihat tips di bawah.
- title: Kompres dan simpan
  text: Klik compress, periksa pratinjau halaman 1, lalu simpan PDF baru dan lampirkan ke email Anda.
faq:
- q: Berapa ukuran lampiran maksimal di Gmail?
  a: 25 MB untuk akun Gmail pribadi. Lampiran yang lebih besar diubah menjadi tautan Google Drive. Administrator Workspace mengatur batas untuk akun kantor dan sekolah.
- q: Kenapa PDF 20 MB saya ditolak padahal batasnya 25 MB?
  a: Lampiran membesar sekitar sepertiga saat di-encode untuk email, dan server penerima bisa punya batas lebih rendah dari server Anda. Targetkan sekitar 18 MB atau kurang.
- q: Apakah kompres PDF membuat teks jadi buram?
  a: Tidak di mode Keep text. Hanya gambar yang disimpan ulang; teks, font, dan grafik vektor disalin tanpa perubahan. Di mode Pages as pictures, teks menjadi bagian dari gambar.
- q: Bisakah saya mengompres file PowerPoint?
  a: Ekspor dulu ke PDF, lalu kompres PDF-nya. Mengecilkan gambar langsung di file .pptx ada di daftar ide alat ini, tetapi belum dibuat.
- q: Kenapa PDF saya hampir tidak mengecil?
  a: Mungkin isinya sebagian besar sudah teks dan grafik vektor, atau gambarnya memakai CMYK atau format lain yang kurang umum, yang untuk saat ini dibiarkan apa adanya.
---

<h2>Berapa batas ukuran lampiran email?</h2>
<p>Untuk akun Gmail pribadi, batasnya 25 MB. Kalau lampiran melebihi batas itu, Gmail menghapusnya dan menggantinya dengan tautan Google Drive di dalam email. Untuk akun kantor dan sekolah di Google Workspace, batasnya diatur oleh administrator.</p><p>Outlook.com juga mencantumkan 25 MB untuk file lampiran, dan menyarankan berbagi lewat OneDrive (hingga 2 GB) untuk file yang lebih besar. Aplikasi desktop Outlook lebih ketat secara bawaan: Microsoft mendokumentasikan batas 20 MB untuk akun email internet dan 10 MB untuk akun Exchange (email kantor), yang bisa diubah administrator.</p><p>Ingat juga sisi penerima. Server email redaksi punya batasnya sendiri, dan Anda tidak bisa melihatnya. File yang berhasil keluar dari kotak keluar Anda tetap bisa ditolak saat tiba.</p>

<h2>Kenapa targetnya 18 MB, bukan 25 MB?</h2>
<p>Email dirancang untuk teks, jadi lampiran diubah menjadi teks sebelum dikirim. Metode standarnya, Base64, mengubah setiap 3 byte menjadi 4 karakter (RFC 2045), sehingga file membesar sekitar 33%, ditambah sedikit lagi untuk jeda baris. PDF 18 MB berjalan sebagai kira-kira 24 MB.</p><p>Gmail dan Microsoft tidak menyatakan dengan jelas apakah batas 25 MB menghitung file Anda atau pesan yang sudah di-encode, jadi sisakan ruang. Sekitar 18 MB muat di bawah 25 MB setelah encoding dan juga di bawah batas bawaan 20 MB aplikasi desktop Outlook. Kalau Anda tahu penerima memakai server kantor yang ketat, turunkan lagi: 5 sampai 7 MB aman untuk batas 10 MB.</p>

<h2>Kenapa PDF saya besar sekali?</h2>
<p>Pada kebanyakan deck yang berat, ukurannya berasal dari foto. Aplikasi presentasi sering menyimpan setiap gambar dalam resolusi saat ditempel, sehingga satu foto dari ponsel bisa berisi jauh lebih banyak piksel daripada yang bisa ditampilkan slide. Teks, grafik, dan bentuk yang dibuat di aplikasi hanya memakan sedikit ruang.</p><p>Karena itu, cara terbaik mengecilkan deck adalah mengubah ukuran gambar sesuai kebutuhan halaman, dan membiarkan bagian lain apa adanya.</p>

<p>[[steps]]</p>

<h2>Ukuran file adalah bagian dari pitch Anda</h2>
<p>Ukuran file mudah dianggap urusan teknis. Dalam media relations, ia bagian dari pesan. Wartawan sering membaca pitch sekilas di ponsel, di sela tenggat. Lampiran 24 MB yang lambat dibuka, atau email yang ditolak server redaksi, tidak akan pernah dibaca, sebagus apa pun cerita di dalamnya.</p><p>Pertanyaan yang berguna sebelum menekan kirim: <em>apa yang dibutuhkan wartawan ini untuk memutuskan apakah ada beritanya?</em> Biasanya itu siaran pers di badan email, deck atau lembar fakta yang ringan, dan tautan ke sisanya. Selebihnya untuk nanti, setelah mereka tertarik. Sebagian besar media relations adalah memudahkan kerja wartawan; file yang terbuka dalam dua detik adalah cara kecil dan nyata untuk melakukannya.</p><p>Pemikiran yang sama berlaku di dalam organisasi Anda. Deck untuk direksi yang bisa dibuka di perjalanan menuju rapat akan dibaca; yang harus menunggu Wi-Fi kantor sering tidak. (Ini pandangan saya sebagai praktisi, bukan aturan dari studi mana pun.)</p>

<h2>Keep text atau Pages as pictures: pilih yang mana?</h2>
<ul><li><strong>Keep text</strong> (paling cocok untuk deck, press kit, dan laporan). Setiap gambar diperkecil sesuai ukurannya di halaman lalu disimpan sebagai JPEG. Pada tingkat Balanced, artinya hingga 150 dpi, yang terlihat bersih di laptop atau proyektor. Gambar hanya diganti kalau versi barunya jelas lebih kecil. Teks tetap bisa dipilih dan dicari, dan tautan tetap berfungsi.</li><li><strong>Pages as pictures</strong> (paling cocok untuk hasil pindaian). Setiap halaman menjadi satu gambar. Dokumen hasil pindaian jadi jauh lebih kecil, tetapi teksnya tidak bisa lagi dipilih atau dicari. Anda juga bisa beralih ke hitam putih, yang cocok untuk teks hasil pindaian.</li></ul>

<h2>Kalau masih belum muat</h2>
<ul><li>Pilih tingkat yang lebih kecil (Small atau Smallest). Foto menjadi lebih lembut, tetapi teks dan grafik tetap tajam di mode Keep text.</li><li>Pecah deck menjadi dua file, misalnya cerita utama dan lampiran.</li><li>Kirim tautan saja. Untuk press kit lengkap, lampirkan PDF yang ringan dan tautkan ke folder bersama berisi file ukuran penuh.</li></ul><p>Untuk press kit, jangan kecilkan foto yang ingin Anda muat di media. Wartawan butuh gambar beresolusi tinggi lengkap dengan keterangan dan kredit. Kompres deck yang dikirim untuk dibaca, dan simpan file asli di folder. <a href="../cara-menulis-siaran-pers/index.html">Panduan menulis siaran pers</a> membahas apa saja yang perlu disertakan.</p>

<h2>Amankah mengompres deck rahasia secara online?</h2>
<p>Banyak kompresor online mengunggah file Anda ke server mereka untuk diproses. Untuk deck yang masih embargo atau dokumen klien, itu risiko nyata. File Shrinker bekerja di dalam tab browser Anda: file tidak dikirim ke mana pun, tidak ada akun dan tidak ada pelacakan, dan menutup tab akan menghapusnya.</p><p>Perlu mengirim video atau audio juga? Lihat <a href="../cara-kompres-video-untuk-email-dan-whatsapp/index.html">cara kompres video untuk email dan WhatsApp</a> dan <a href="../cara-mengecilkan-ukuran-file-audio/index.html">cara mengecilkan ukuran file audio</a>.</p>
