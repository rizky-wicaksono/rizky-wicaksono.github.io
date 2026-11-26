---
key: how-to-make-an-audio-file-smaller
order: 7
title: Cara mengecilkan file audio tanpa kehilangan apa yang diucapkan
short: Cara mengecilkan ukuran file audio (M4A)
desc: Ukuran audio adalah bitrate dikali durasi. Untuk suara, M4A 64 kbps membuat wawancara 30 menit sekitar 14 MB, cukup kecil untuk email. Pengaturan dan langkahnya.
summary: 'Ukuran file audio adalah bitrate dikali durasinya. Untuk suara, audio AAC dalam file M4A pada 64 kbps sudah jernih dan kecil: satu jam sekitar 29 MB, jadi wawancara 30 menit sekitar 14 MB dan muat di email. Gunakan mono untuk satu mikrofon. Musik butuh lebih, sekitar 128 kbps.'
date: '2026-11-25'
minutes: 6
tool:
  name: M4A Compressor
  url: https://rizky-wicaksono.github.io/file-shrinker/audio.html
  kind: audio
  pitch: Atur bitrate atau target ukuran, ubah ke mono, dan simpan file .m4a sungguhan. Bisa untuk MP3, WAV, FLAC, dan file video. Gratis, dan tidak ada yang diunggah.
sources:
- title: 'Gmail Help: Send attachments with your Gmail message'
  url: https://support.google.com/mail/answer/6584?hl=en
- title: 'WhatsApp Help Center: How to send media, contacts, or location (Web)'
  url: https://faq.whatsapp.com/453914586839706/?cms_platform=web
- title: Kode sumber dan catatan teknis File Shrinker (GitHub)
  url: https://github.com/rizky-wicaksono/file-shrinker
steps_title: Cara kompres file audio, langkah demi langkah
steps:
- title: Buka M4A Compressor
  text: Buka <a href="https://rizky-wicaksono.github.io/file-shrinker/audio.html">M4A Compressor</a> di Chrome, Edge, atau Safari versi terbaru.
- title: Masukkan rekaman Anda
  text: Masukkan file M4A, MP3, WAV, FLAC, OGG, atau AAC. File video juga bisa; hanya suaranya yang diambil.
- title: Pilih kualitas atau target ukuran
  text: Pilih bitrate (64 kbps untuk suara, 128 kbps untuk musik) atau ketik target ukuran, misalnya 18 MB.
- title: Ubah ke mono untuk suara
  text: Di bagian Channels, pilih Mono untuk wawancara dengan satu mikrofon atau voice note.
- title: Kompres dan simpan
  text: Klik compress dan biarkan tab terbuka sampai selesai, lalu simpan file .m4a-nya.
faq:
- q: Berapa bitrate yang bagus untuk rekaman suara?
  a: 64 kbps mono sudah jernih untuk suara dan membuat rekaman satu jam sekitar 29 MB. Gunakan 96 kbps kalau rekaman berisi musik atau beberapa suara yang ingin tetap jernih.
- q: Apakah M4A lebih kecil dari MP3?
  a: 'Pada bitrate yang sama, ukurannya sama, karena ukuran adalah bitrate dikali durasi. Yang berbeda adalah codec-nya: M4A memakai AAC. Tentukan bitrate-nya dulu.'
- q: Bagaimana cara mengecilkan file WAV?
  a: Ubah ke M4A. WAV berkualitas CD memakai 1.411 kbps; rekaman yang sama pada 64 kbps sekitar 22 kali lebih kecil.
- q: Bisakah file M4A dikirim lewat WhatsApp?
  a: Bisa. Anda bisa mengirimnya sebagai dokumen, yang diizinkan WhatsApp hingga 2 GB, meski file yang lebih kecil lebih cepat diunduh penerima.
- q: Bisakah saya mengambil audio dari video?
  a: Bisa. Masukkan videonya ke M4A Compressor; hanya suaranya yang diambil dan disimpan sebagai file M4A.
---

<h2>Seberapa besar file audio?</h2>
<p>Ukuran adalah bitrate (kilobit per detik) dikali durasi. Audio tanpa kompresi berkualitas CD, seperti file WAV dari alat perekam, memakai 1.411 kbps: 44.100 sampel per detik, masing-masing 16 bit, dua kanal. Itu sekitar 10,6 MB per menit, atau lebih dari 600 MB untuk wawancara satu jam.</p><p>Audio terkompresi jauh lebih kecil. Berikut ruang yang dipakai audio AAC pada bitrate yang umum:</p><ul><li>48 kbps: sekitar 0,36 MB per menit, 22 MB per jam (khusus suara)</li><li>64 kbps: sekitar 0,48 MB per menit, 29 MB per jam (suara jernih, podcast)</li><li>96 kbps: sekitar 0,72 MB per menit, 43 MB per jam (suara bagus, musik cukup)</li><li>128 kbps: sekitar 0,96 MB per menit, 58 MB per jam (musik)</li></ul>

<h2>Pengaturan apa yang cocok untuk rekaman suara?</h2>
<ul><li><strong>Bitrate:</strong> 64 kbps untuk wawancara, podcast, dan memo suara. Turunkan ke 48 kbps hanya kalau ukuran lebih penting daripada kualitas suara.</li><li><strong>Kanal:</strong> mono. Satu suara di satu mikrofon tidak butuh dua kanal, dan mono memberikan seluruh bitrate ke satu kanal.</li><li><strong>Sample rate:</strong> biarkan apa adanya, atau pilih 22 kHz untuk suara. Sample rate yang lebih rendah memotong frekuensi tinggi, yang jarang dipakai suara manusia.</li></ul><p>Untuk mencapai ukuran tertentu, pilih Target file size lalu ketik angkanya, misalnya 18 MB untuk email. Alat ini memilih bitrate yang hasilnya mendekati angka itu.</p>

<p>[[steps]]</p>

<h2>Rekaman adalah catatan</h2>
<p>Rekaman wawancara bukan sekadar file. Ia catatan paling akurat tentang apa yang diucapkan juru bicara Anda, dan saat ada sengketa kutipan, sering kali hanya itu yang Anda punya. Karena itu, ada beberapa pertanyaan PR yang layak diajukan sebelum mengompres dan mengirim apa pun:</p><ul><li><strong>Apakah semua orang tahu sedang direkam?</strong> Sampaikan di awal, terekam. Ini melindungi wartawan dan juru bicara Anda sekaligus.</li><li><strong>Siapa yang menyimpan rekaman asli, dan berapa lama?</strong> Sepakati dengan klien. Kalau sebuah kutipan dipersoalkan berbulan-bulan kemudian, Anda butuh rekaman utuh, bukan potongan yang sudah dikompres.</li><li><strong>Bagian mana yang off the record?</strong> Rekaman yang dibagikan bisa menyebar. Kalau sebagian percakapan off the record, jangan teruskan bagian itu.</li></ul><p>Membagikan rekaman Anda sendiri kepada wartawan setelah wawancara juga bisa membangun kepercayaan: itu menunjukkan Anda yakin dengan apa yang diucapkan dan membantu mereka mengutip dengan akurat. (Saran praktisi; cek dulu kebijakan klien Anda.)</p>

<h2>Bagaimana tim PR memakainya</h2>
<ul><li><strong>Rekaman wawancara untuk wartawan.</strong> Setelah wawancara media, kirim salinan yang sudah dikompres supaya wartawan bisa mengecek kutipan. Obrolan 30 menit pada 64 kbps mono sekitar 14 MB.</li><li><strong>Voice note juru bicara dan potongan untuk radio.</strong> Klip pendek pada 64 sampai 96 kbps terkirim cepat lewat WhatsApp dan email.</li><li><strong>File tamu podcast.</strong> Bagikan salinan ringan untuk ditinjau, dan simpan yang asli untuk proses edit.</li><li><strong>Audio dari video.</strong> Masukkan video acara untuk mendapatkan suaranya saja sebagai M4A kecil, berguna untuk transkripsi.</li></ul><p>Selalu simpan rekaman aslinya. Kompresi membuang detail yang tidak bisa dikembalikan, jadi edit dari yang asli dan kirim salinan yang kecil.</p>

<h2>Kenapa M4A, dan apakah rekaman saya diunggah?</h2>
<p>M4A adalah audio AAC di dalam file MP4. File ini bisa diputar di iPhone, Android, Windows, dan Mac tanpa aplikasi tambahan. Alat ini memakai encoder AAC bawaan browser, jadi rekaman tidak pernah diunggah, yang penting untuk wawancara off the record atau yang masih embargo.</p><p>Perlu mengirim deck atau video juga? Lihat <a href="../cara-kompres-pdf-untuk-email/index.html">cara kompres PDF untuk email</a> dan <a href="../cara-kompres-video-untuk-email-dan-whatsapp/index.html">cara kompres video untuk email dan WhatsApp</a>.</p>
