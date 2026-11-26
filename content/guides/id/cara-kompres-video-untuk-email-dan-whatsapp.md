---
key: how-to-compress-a-video-for-email-and-whatsapp
order: 6
title: Cara kompres video untuk email dan WhatsApp supaya sampai tepat waktu
short: Cara kompres video untuk email dan WhatsApp
desc: Lampiran email dibatasi 25 MB; WhatsApp Web mencantumkan 100 MB pada 720p untuk video. Cara menentukan ukuran yang pas dan mengecilkan MP4 di browser.
summary: 'Untuk email, video harus muat dalam batas lampiran 25 MB seperti file lain, jadi targetkan sekitar 18 MB. Untuk WhatsApp, pusat bantuannya mencantumkan batas video bawaan 100 MB pada 720p di WhatsApp Web (64 MB pada 480p untuk koneksi lebih lambat). Ukuran video kira-kira sama dengan bitrate dikali durasi, jadi dua hal yang paling menentukan adalah resolusi dan durasi: 720p sudah cukup untuk layar ponsel, dan klip satu menit muat dalam 18 MB pada sekitar 2,4 Mbps.'
date: '2026-11-25'
minutes: 7
tool:
  name: MP4 Compressor
  url: https://rizky-wicaksono.github.io/file-shrinker/video.html
  kind: video
  pitch: Pilih resolusi, atau ketik target ukuran seperti 18 MB, dan dapatkan MP4 yang bisa diputar hampir di mana saja. Gratis, dan video tidak pernah keluar dari browser Anda.
sources:
- title: 'WhatsApp Help Center: How to send media, contacts, or location (Web)'
  url: https://faq.whatsapp.com/453914586839706/?cms_platform=web
- title: 'Gmail Help: Send attachments with your Gmail message'
  url: https://support.google.com/mail/answer/6584?hl=en
- title: 'Microsoft Support: Sending limits in Outlook.com'
  url: https://support.microsoft.com/en-us/outlook/sending-limits-in-outlook-com
- title: Kode sumber dan catatan teknis File Shrinker (GitHub)
  url: https://github.com/rizky-wicaksono/file-shrinker
steps_title: Cara kompres video, langkah demi langkah
steps:
- title: Buka MP4 Compressor
  text: Buka <a href="https://rizky-wicaksono.github.io/file-shrinker/video.html">MP4 Compressor</a> di Chrome, Edge, atau Safari versi terbaru.
- title: Masukkan video Anda
  text: Seret file MP4, MOV, WebM, atau MKV, atau klik untuk memilihnya. File tetap di perangkat Anda.
- title: Pilih resolusi
  text: 720p pilihan yang baik untuk email dan WhatsApp. Pilih 480p atau 360p untuk klip panjang atau target yang sangat kecil.
- title: Atur ukurannya
  text: Pilih Target file size lalu ketik 18 untuk email, atau pakai pilihan cepat (10, 25, 50, atau 100 MB). Atau pilih Quality (High, Balanced, atau Smallest) kalau tidak butuh ukuran yang pasti.
- title: Tentukan frame rate dan suara
  text: Pertahankan frame rate asli kecuali perlu lebih hemat; 30 atau 24 fps menghemat sedikit. Untuk percakapan, suara Smaller (sekitar 96 kbps) sudah cukup. Untuk b-roll tanpa suara, hapus suaranya.
- title: Kompres dan simpan
  text: Biarkan tab tetap terbuka dan terlihat selama proses, karena komputer Anda sendiri yang melakukan encoding. Lalu simpan MP4-nya.
faq:
- q: Berapa ukuran terbaik untuk mengirim video lewat email?
  a: Sekitar 18 MB atau kurang. Gmail dan Outlook.com mengizinkan 25 MB, tetapi encoding menambah sekitar sepertiga, dan sebagian server email kantor mengizinkan lebih sedikit.
- q: Bagaimana mengirim video yang melebihi batas WhatsApp?
  a: Turunkan resolusi atau potong videonya, atau kirim lewat opsi Dokumen, yang diizinkan WhatsApp hingga 2 GB. Untuk file yang sangat besar, tautan cloud lebih mudah bagi penerima.
- q: Resolusi mana yang sebaiknya saya pilih?
  a: 720p untuk sebagian besar kebutuhan email dan WhatsApp. 1080p hanya kalau klipnya pendek atau targetnya besar; 480p untuk klip panjang.
- q: Bisakah saya mengubah MOV dari iPhone menjadi MP4?
  a: Bisa. Alat ini membaca file MOV, WebM, dan MKV dan selalu menyimpan hasilnya sebagai MP4.
- q: Kenapa prosesnya lambat?
  a: Komputer Anda sendiri yang melakukan encoding, bukan server. Video yang lebih panjang dan beresolusi lebih tinggi butuh waktu lebih lama, dan tab harus tetap terbuka dan terlihat.
---

<h2>Seberapa besar video yang bisa dikirim lewat email dan WhatsApp?</h2>
<ul><li><strong>Email:</strong> 25 MB untuk lampiran Gmail dan Outlook.com. Gmail mengubah file yang lebih besar menjadi tautan Google Drive. Karena lampiran membesar sekitar sepertiga saat di-encode, targetkan sekitar 18 MB (<a href="../cara-kompres-pdf-untuk-email/index.html">panduan PDF</a> menjelaskan alasannya).</li><li><strong>WhatsApp (sebagai video):</strong> di WhatsApp Web, pusat bantuannya mencantumkan batas video bawaan 100 MB dan 720p untuk koneksi lebih cepat, serta 64 MB dan 480p untuk koneksi lebih lambat. Format yang didukung antara lain MP4, MOV, MKV, AVI, FLV, dan 3GP.</li><li><strong>WhatsApp (sebagai dokumen):</strong> file yang dikirim lewat opsi Dokumen bisa sampai 2 GB. Berguna untuk file besar, tetapi lambat diunduh dengan data seluler.</li></ul>

<h2>Berapa ukuran video saya nanti?</h2>
<p>Ukuran video adalah bitrate-nya (berapa banyak data yang dipakai setiap detik) dikali durasinya. Jadi untuk target ukuran yang sama, klip yang lebih panjang mendapat lebih sedikit data per detik. Berikut total bitrate, gambar ditambah suara, yang muat dalam 18 MB:</p><ul><li>30 detik: sekitar 4,8 Mbps</li><li>1 menit: sekitar 2,4 Mbps</li><li>2 menit: sekitar 1,2 Mbps</li><li>3 menit: sekitar 0,8 Mbps</li></ul><p>Makin sedikit data per detik, makin kotak-kotak gambarnya, terutama pada resolusi tinggi. Untuk klip panjang, turunkan resolusi ke 720p atau 480p, atau potong dulu videonya. MP4 Compressor akan memperingatkan Anda kalau pengaturannya bakal terlihat kotak-kotak.</p>

<p>[[steps]]</p>

<h2>Setiap potongan adalah keputusan redaksional</h2>
<p>Saat Anda memotong pernyataan juru bicara menjadi klip 40 detik untuk WhatsApp, Anda melakukan pekerjaan editor: memutuskan apa yang didengar audiens. Itu pekerjaan PR yang wajar, tetapi membawa tanggung jawab. Klip yang mengubah makna ucapan, atau membuang bagian yang pasti ditanyakan wartawan, bisa membuat Anda kehilangan kepercayaan yang nilainya lebih besar dari pemberitaannya.</p><p>Kebiasaan sederhana ini membantu: kirim klip pendek supaya cepat, dan tawarkan rekaman utuh tanpa potongan di sampingnya. Itu menunjukkan kepada redaksi bahwa Anda tidak menyembunyikan apa pun, dan memberi mereka kesempatan memeriksa konteksnya sendiri. Beri nama file dengan jelas juga, berisi nama pembicara, acara, dan tanggal, supaya produser yang menemukan file itu seminggu kemudian masih tahu isinya.</p><p>Kecepatan sama pentingnya dengan kerapian. Pratinjau 720p yang tiba saat editor masih menyusun rencana hari itu sering lebih berharga daripada file 4K sempurna yang datang setelah susunan acara dikunci. (Saran praktisi, bukan aturan redaksi.)</p>

<h2>Bagaimana tim PR memakainya</h2>
<ul><li><strong>Klip juru bicara untuk media online.</strong> Kirim pratinjau 720p lewat WhatsApp atau email supaya editor bisa memutuskan dengan cepat.</li><li><strong>Cuplikan acara untuk media dan mitra.</strong> Potongan pendek 720p di bawah 18 MB muat dalam email yang sama dengan siaran pers.</li><li><strong>B-roll untuk televisi.</strong> Stasiun TV biasanya menginginkan kualitas terbaik yang Anda punya, jadi kirim pratinjau kecil dan tautan ke file berkualitas penuh, bukan hanya salinan yang sudah dikompres.</li></ul>

<h2>Kenapa MP4, dan apakah video saya diunggah?</h2>
<p>Alat ini menyimpan MP4 dengan video H.264, kombinasi yang bisa diputar di hampir semua ponsel, laptop, dan aplikasi edit. Kompresinya memakai encoder video bawaan browser, jadi tidak ada yang diunggah: klip tidak pernah keluar dari perangkat Anda, yang penting untuk rekaman yang belum dirilis. Konsekuensinya soal kecepatan. Video panjang atau beresolusi tinggi bisa butuh waktu di laptop yang lebih lama.</p><p>Perlu mengecilkan deck atau rekaman juga? Lihat <a href="../cara-kompres-pdf-untuk-email/index.html">cara kompres PDF untuk email</a> dan <a href="../cara-mengecilkan-ukuran-file-audio/index.html">cara mengecilkan ukuran file audio</a>.</p>
