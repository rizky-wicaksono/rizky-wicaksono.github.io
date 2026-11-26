---
key: how-to-compress-a-video-for-email-and-whatsapp
order: 6
title: How to compress a video for email and WhatsApp so it arrives in time
short: How to compress a video for email or WhatsApp
desc: Email caps attachments at 25 MB; WhatsApp Web lists 100 MB at 720p for videos. How to work out the right size and shrink an MP4 in your browser.
summary: 'For email, a video has to fit the same 25 MB attachment limit as any file, so aim for about 18 MB. For WhatsApp, the help center lists a default video limit of 100 MB at 720p on WhatsApp Web (64 MB at 480p on slower connections). Video size is roughly bitrate times length, so the two levers that matter are resolution and length: 720p is plenty for a phone screen, and a one-minute clip fits in 18 MB at about 2.4 Mbps.'
date: '2026-11-25'
minutes: 7
tool:
  name: MP4 Compressor
  url: https://rizky-wicaksono.github.io/file-shrinker/video.html
  kind: video
  pitch: Pick a resolution, or type a target size such as 18 MB, and get an MP4 that plays almost anywhere. Free, and the video never leaves your browser.
sources:
- title: 'WhatsApp Help Center: How to send media, contacts, or location (Web)'
  url: https://faq.whatsapp.com/453914586839706/?cms_platform=web
- title: 'Gmail Help: Send attachments with your Gmail message'
  url: https://support.google.com/mail/answer/6584?hl=en
- title: 'Microsoft Support: Sending limits in Outlook.com'
  url: https://support.microsoft.com/en-us/outlook/sending-limits-in-outlook-com
- title: File Shrinker source code and technical notes (GitHub)
  url: https://github.com/rizky-wicaksono/file-shrinker
steps_title: How to compress a video, step by step
steps:
- title: Open the MP4 Compressor
  text: Go to the <a href="https://rizky-wicaksono.github.io/file-shrinker/video.html">MP4 Compressor</a> in a current version of Chrome, Edge or Safari.
- title: Add your video
  text: Drag in an MP4, MOV, WebM or MKV file, or click to choose one. It stays on your device.
- title: Choose a resolution
  text: 720p is a good choice for email and WhatsApp. Pick 480p or 360p for long clips or very small targets.
- title: Set the size
  text: Choose Target file size and type 18 for email, or use a preset (10, 25, 50 or 100 MB). Or choose Quality (High, Balanced or Smallest) if you do not need an exact size.
- title: Decide on frame rate and sound
  text: Keep the original frame rate unless you need to save more; 30 or 24 fps saves a little. For speech, Smaller sound (about 96 kbps) is fine. For silent b-roll, remove the sound.
- title: Compress and save
  text: Keep the tab open and visible while it works, since your own computer does the encoding. Then save the MP4.
faq:
- q: What is the best size to email a video?
  a: About 18 MB or less. Gmail and Outlook.com allow 25 MB, but encoding adds about a third, and some company mail servers allow less.
- q: How do I send a video longer than WhatsApp allows?
  a: Lower the resolution or trim it, or send it with the Document option, which WhatsApp allows up to 2 GB. For very large files, a cloud link is easier for the recipient.
- q: Which resolution should I choose?
  a: 720p for most email and WhatsApp use. 1080p only if the clip is short or the target is large; 480p for long clips.
- q: Can I turn a MOV from an iPhone into an MP4?
  a: Yes. The tool reads MOV, WebM and MKV files and always saves the result as MP4.
- q: Why is it slow?
  a: Your own computer does the encoding, not a server. Longer and higher-resolution videos take more time, and the tab must stay open and visible.
---

<h2>How big can a video be on email and WhatsApp?</h2>
<ul><li><strong>Email:</strong> 25 MB for Gmail and Outlook.com attachments. Gmail turns anything bigger into a Google Drive link. Because attachments grow by about a third when they are encoded, aim for about 18 MB (the <a href="../how-to-compress-a-pdf-for-email/index.html">PDF guide</a> explains why).</li><li><strong>WhatsApp (as a video):</strong> on WhatsApp Web, the help center lists a default video limit of 100 MB and 720p for faster connections, and 64 MB and 480p for slower ones. Supported formats include MP4, MOV, MKV, AVI, FLV and 3GP.</li><li><strong>WhatsApp (as a document):</strong> files sent with the Document option can be up to 2 GB. That is useful for a large file, but it is slow to download on mobile data.</li></ul>

<h2>How big will my video be?</h2>
<p>A video’s size is its bitrate (how much data it uses each second) multiplied by its length. So for a fixed target size, a longer clip gets less data per second. Here is the total bitrate, picture plus sound, that fits in 18 MB:</p><ul><li>30 seconds: about 4.8 Mbps</li><li>1 minute: about 2.4 Mbps</li><li>2 minutes: about 1.2 Mbps</li><li>3 minutes: about 0.8 Mbps</li></ul><p>The less data per second, the blockier the picture gets, especially at high resolutions. For long clips, lower the resolution to 720p or 480p, or trim the video first. The MP4 Compressor warns you when your settings will look blocky.</p>

<p>[[steps]]</p>

<h2>Every cut is an editorial choice</h2>
<p>When you trim a spokesperson’s statement into a 40-second clip for WhatsApp, you are doing what an editor does: deciding what the audience hears. That is normal PR work, but it carries a responsibility. A clip that changes the meaning of what was said, or leaves out the part a journalist would ask about, can cost you more trust than the coverage is worth.</p><p>A simple habit helps: send the short clip for speed, and offer the full, uncut recording alongside it. It tells the newsroom you have nothing to hide, and it lets them check context themselves. Name files clearly too, with the speaker, the event and the date, so a producer who finds the file a week later still knows what it is.</p><p>Speed matters as much as polish. A 720p preview that lands while the editor is still planning the day is often worth more than a perfect 4K file that arrives after the rundown is set. (Practitioner advice, not a newsroom rule.)</p>

<h2>How PR teams use this</h2>
<ul><li><strong>A spokesperson clip for an online newsroom.</strong> Send a 720p preview by WhatsApp or email so the editor can decide quickly.</li><li><strong>Event highlights for media and partners.</strong> A short 720p cut under 18 MB fits in the same email as the press release.</li><li><strong>B-roll for TV.</strong> Broadcasters usually want the best quality you have, so send a small preview and a link to the full-quality file, not a compressed copy only.</li></ul>

<h2>Why MP4, and is my video uploaded?</h2>
<p>The tool saves an MP4 with H.264 video, a combination that plays on almost every phone, laptop and editing app. The compression uses the video encoder built into your browser, so nothing is uploaded: the clip never leaves your device, which matters for unreleased footage. The trade-off is speed. A long or high-resolution video can take a while on an older laptop.</p><p>Need to shrink a deck or a recording too? See <a href="../how-to-compress-a-pdf-for-email/index.html">how to compress a PDF for email</a> and <a href="../how-to-make-an-audio-file-smaller/index.html">how to make an audio file smaller</a>.</p>
