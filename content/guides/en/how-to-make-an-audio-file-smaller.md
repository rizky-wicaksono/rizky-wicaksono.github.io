---
key: how-to-make-an-audio-file-smaller
order: 7
title: How to make an audio file smaller without losing what was said
short: How to make an audio file smaller (M4A)
desc: Audio size is bitrate times length. For speech, 64 kbps M4A keeps a 30-minute interview near 14 MB, small enough to email. Settings and steps.
summary: 'An audio file’s size is its bitrate multiplied by its length. For speech, AAC audio in an M4A file at 64 kbps is clear and small: one hour is about 29 MB, so a 30-minute interview is about 14 MB and fits in an email. Use mono for a single microphone. Music needs more, around 128 kbps.'
date: '2026-11-25'
minutes: 6
tool:
  name: M4A Compressor
  url: https://rizky-wicaksono.github.io/file-shrinker/audio.html
  kind: audio
  pitch: Set a bitrate or a target size, switch to mono, and save a real .m4a file. Works with MP3, WAV, FLAC and video files. Free, and nothing is uploaded.
sources:
- title: 'Gmail Help: Send attachments with your Gmail message'
  url: https://support.google.com/mail/answer/6584?hl=en
- title: 'WhatsApp Help Center: How to send media, contacts, or location (Web)'
  url: https://faq.whatsapp.com/453914586839706/?cms_platform=web
- title: File Shrinker source code and technical notes (GitHub)
  url: https://github.com/rizky-wicaksono/file-shrinker
steps_title: How to compress an audio file, step by step
steps:
- title: Open the M4A Compressor
  text: Go to the <a href="https://rizky-wicaksono.github.io/file-shrinker/audio.html">M4A Compressor</a> in a current version of Chrome, Edge or Safari.
- title: Add your recording
  text: Drop in an M4A, MP3, WAV, FLAC, OGG or AAC file. A video file works too; only its sound is kept.
- title: Choose quality or a target size
  text: Pick a bitrate (64 kbps for speech, 128 kbps for music) or type a target size such as 18 MB.
- title: Switch to mono for speech
  text: Under Channels, choose Mono for a single-microphone interview or voice note.
- title: Compress and save
  text: Click compress and keep the tab open until it finishes, then save the .m4a file.
faq:
- q: What bitrate is good for a voice recording?
  a: 64 kbps mono is clear for speech and keeps an hour to about 29 MB. Use 96 kbps if the recording has music or several voices you want to keep crisp.
- q: Is M4A smaller than MP3?
  a: 'At the same bitrate, the file size is the same, because size is bitrate times length. What differs is the codec: M4A uses AAC. Choose the bitrate first.'
- q: How do I make a WAV file smaller?
  a: Convert it to M4A. A WAV at CD quality uses 1,411 kbps; the same recording at 64 kbps is about 22 times smaller.
- q: Can I send an M4A file on WhatsApp?
  a: Yes. You can send it as a document, which WhatsApp allows up to 2 GB, though a smaller file is quicker for the recipient to download.
- q: Can I get the audio out of a video?
  a: Yes. Drop the video into the M4A Compressor; only the sound is kept and saved as an M4A file.
---

<h2>How big is an audio file?</h2>
<p>Size is bitrate (kilobits per second) times length. Uncompressed CD-quality audio, such as a WAV file from a recorder, uses 1,411 kbps: 44,100 samples a second, 16 bits each, two channels. That is about 10.6 MB per minute, or more than 600 MB for an hour-long interview.</p><p>Compressed audio is far smaller. Here is how much space AAC audio takes at common bitrates:</p><ul><li>48 kbps: about 0.36 MB a minute, 22 MB an hour (speech only)</li><li>64 kbps: about 0.48 MB a minute, 29 MB an hour (clear speech, podcasts)</li><li>96 kbps: about 0.72 MB a minute, 43 MB an hour (good speech, fair music)</li><li>128 kbps: about 0.96 MB a minute, 58 MB an hour (music)</li></ul>

<h2>Which settings should I use for speech?</h2>
<ul><li><strong>Bitrate:</strong> 64 kbps for interviews, podcasts and voice memos. Go down to 48 kbps only if size matters more than sound.</li><li><strong>Channels:</strong> mono. One voice on one microphone does not need two channels, and mono gives the bitrate to a single channel.</li><li><strong>Sample rate:</strong> keep it as is, or choose 22 kHz for speech. Lower rates cut high frequencies, which voices barely use.</li></ul><p>To hit an exact size, choose Target file size instead and type a number, such as 18 MB for email. The tool picks the bitrate that lands close to it.</p>

<p>[[steps]]</p>

<h2>A recording is a record</h2>
<p>An interview recording is not just a file. It is the most accurate record of what your spokesperson said, and in a dispute about a quote it is often the only one. That makes a few PR questions worth asking before you compress and send anything:</p><ul><li><strong>Did everyone know they were being recorded?</strong> Say so at the start, on tape. It protects the journalist and your spokesperson alike.</li><li><strong>Who keeps the original, and for how long?</strong> Agree on it with the client. If a quote is challenged months later, you will want the full recording, not a compressed excerpt.</li><li><strong>What was off the record?</strong> A shared recording travels. If part of the conversation was off the record, do not send that part on.</li></ul><p>Sharing your own recording with the reporter after an interview can also build trust: it shows you are confident in what was said and helps them quote accurately. (Practitioner advice; check your client’s policy first.)</p>

<h2>How PR teams use this</h2>
<ul><li><strong>Interview recordings for journalists.</strong> After a media interview, send the reporter a compressed copy so they can check quotes. A 30-minute talk at 64 kbps mono is about 14 MB.</li><li><strong>Spokesperson voice notes and radio grabs.</strong> Short clips at 64 to 96 kbps send fast on WhatsApp and email.</li><li><strong>Podcast guest files.</strong> Share a light listening copy for review, and keep the original for the edit.</li><li><strong>Audio from a video.</strong> Drop in the event video to get just the speech as a small M4A, useful for transcription.</li></ul><p>Always keep the original recording. Compression removes detail that cannot be brought back, so edit from the original and send the small copy.</p>

<h2>Why M4A, and is my recording uploaded?</h2>
<p>M4A is AAC audio in an MP4 file. It plays on iPhone, Android, Windows and Mac without extra apps. The tool encodes with the AAC encoder built into your browser, so the recording is never uploaded, which matters for off-the-record or embargoed interviews.</p><p>Sending a deck or a video as well? See <a href="../how-to-compress-a-pdf-for-email/index.html">how to compress a PDF for email</a> and <a href="../how-to-compress-a-video-for-email-and-whatsapp/index.html">how to compress a video for email or WhatsApp</a>.</p>
