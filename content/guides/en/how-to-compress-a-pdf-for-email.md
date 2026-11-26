---
key: how-to-compress-a-pdf-for-email
order: 5
title: How to compress a PDF for email so your deck actually gets opened
short: How to compress a PDF for email (under 25 MB)
desc: Gmail and Outlook.com cap attachments at 25 MB. Here is why you should aim for about 18 MB, and how to shrink a heavy deck without blurring the text.
summary: 'Gmail and Outlook.com both limit attachments to 25 MB, and email encoding makes a file about a third bigger on its way out, so aim for about 18 MB or less. For a slide deck, shrink only the pictures and leave the text as text: in a heavy deck the weight is usually in the photos, and the slides stay sharp and searchable.'
date: '2026-11-25'
minutes: 7
tool:
  name: PDF Compressor
  url: https://rizky-wicaksono.github.io/file-shrinker/pdf.html
  kind: pdf
  pitch: Shrinks only the pictures, keeps text sharp and searchable, and aims for 18 MB by default. Free, and the file never leaves your browser.
sources:
- title: 'Gmail Help: Send attachments with your Gmail message'
  url: https://support.google.com/mail/answer/6584?hl=en
- title: 'Microsoft Support: Sending limits in Outlook.com'
  url: https://support.microsoft.com/en-us/outlook/sending-limits-in-outlook-com
- title: 'Microsoft Learn: Attachment size exceeds the allowable limit (Outlook)'
  url: https://learn.microsoft.com/en-us/troubleshoot/outlook/message-body/attachment-size-exceeds-the-allowable-limit-error
- title: 'RFC 2045, MIME Part One, section 6.8: Base64 content transfer encoding'
  url: https://www.rfc-editor.org/rfc/rfc2045#section-6.8
- title: File Shrinker source code and technical notes (GitHub)
  url: https://github.com/rizky-wicaksono/file-shrinker
steps_title: How to compress a PDF for email, step by step
steps:
- title: Open the PDF Compressor
  text: Go to the <a href="https://rizky-wicaksono.github.io/file-shrinker/pdf.html">PDF Compressor</a> in Chrome, Edge or Safari. There is nothing to install and no sign-up.
- title: Add your PDF
  text: Drag the file onto the page, or click to choose it. It is read inside your browser tab and is not uploaded.
- title: Keep the method on Keep text
  text: This is the default. It shrinks only the photos and pictures; text, fonts, vector charts and links stay as they are.
- title: Set the goal to Email (18 MB)
  text: Also the default. The tool tries its quality levels and picks the sharpest one that fits. Choose 10 MB or 5 MB, or type your own number, for stricter inboxes.
- title: Check the estimate
  text: The tool shows the expected size before you start. If even the smallest level will not fit, see the tips below.
- title: Compress and save
  text: Click compress, check the preview of page 1, then save the new PDF and attach it to your email.
faq:
- q: What is the maximum attachment size in Gmail?
  a: 25 MB for personal Gmail accounts. Bigger attachments are turned into a Google Drive link. Workspace administrators set the limit for work and school accounts.
- q: Why does my 20 MB PDF bounce when the limit is 25 MB?
  a: Attachments grow by about a third when they are encoded for email, and the receiving server may have a lower limit than yours. Aim for about 18 MB or less.
- q: Will compressing a PDF make the text blurry?
  a: Not in Keep text mode. Only the pictures are re-saved; text, fonts and vector graphics are copied unchanged. In Pages as pictures mode, text becomes part of an image.
- q: Can I compress a PowerPoint file?
  a: Export it to PDF first, then compress the PDF. Shrinking pictures inside .pptx files directly is on the tool’s list of ideas but not built yet.
- q: Why did my PDF barely get smaller?
  a: It may be mostly text and vector graphics already, or its pictures may use CMYK or other less common formats, which the tool leaves as they are for now.
---

<h2>What is the attachment limit for email?</h2>
<p>For personal Gmail accounts the limit is 25 MB. If your attachments go over it, Gmail removes them and puts a Google Drive link in the email instead. For work and school accounts on Google Workspace, the administrator sets the limit.</p><p>Outlook.com also lists 25 MB for attached files, and suggests sharing from OneDrive (up to 2 GB) for anything bigger. The Outlook desktop app is stricter by default: Microsoft documents a 20 MB limit for internet email accounts and 10 MB for Exchange (business) accounts, where the administrator can change it.</p><p>Remember the other side, too. The journalist’s newsroom mail server has its own limit, and you cannot see it. A file that leaves your outbox can still bounce on arrival.</p>

<h2>Why aim for 18 MB, not 25 MB?</h2>
<p>Email was built for text, so attachments are converted to text before they are sent. The standard method, Base64, turns every 3 bytes into 4 characters (RFC 2045), which makes the file about 33% bigger, plus a little more for line breaks. An 18 MB PDF travels as roughly 24 MB.</p><p>Gmail and Microsoft do not say clearly whether their 25 MB counts your file or the encoded message, so leave room. About 18 MB fits under 25 MB after encoding and also under the 20 MB default of the Outlook desktop app. If you know the recipient is on a strict company server, go lower: 5 to 7 MB is a safe size for a 10 MB limit.</p>

<h2>Why is my PDF so big?</h2>
<p>In most heavy decks, the size comes from photos. A presentation app often keeps every picture at the resolution it was pasted in, so one phone photo can hold far more pixels than the slide can show. Text, charts and shapes drawn in the app take very little space.</p><p>That is why the best way to shrink a deck is to resize the pictures to what the page actually needs, and leave everything else alone.</p>

<p>[[steps]]</p>

<h2>File size is part of your pitch</h2>
<p>It is easy to treat file size as a technical detail. In media relations it is part of the message. A journalist often skims pitches on a phone, between deadlines. A 24 MB attachment that is slow to open, or an email that bounces off the newsroom server, never gets read, however good the story inside is.</p><p>A useful question before you hit send: <em>what does this journalist need to decide whether there is a story?</em> Usually that is the release in the email body, a light deck or fact sheet, and a link to the rest. Everything else is for later, once they say yes. Making a journalist’s job easier is most of media relations; a file that opens in two seconds is a small, concrete way to do it.</p><p>The same thinking applies inside your own organisation. The board deck that a director can open on the way to a meeting gets read; the one that waits for office Wi-Fi often does not. (This is my practitioner view, not a rule from any study.)</p>

<h2>Keep text or Pages as pictures: which one?</h2>
<ul><li><strong>Keep text</strong> (best for decks, press kits and reports). Each picture is scaled down to what its size on the page needs and saved as a JPEG. On the Balanced level that means up to 150 dpi, which looks clean on a laptop or projector. A picture is replaced only when the new version is clearly smaller. Text stays selectable and searchable, and links keep working.</li><li><strong>Pages as pictures</strong> (best for scans). Every page becomes one image. It shrinks scanned documents more, but the text can no longer be selected or searched. You can also switch to black and white, which suits scanned text.</li></ul>

<h2>What to do when it still won’t fit</h2>
<ul><li>Pick a smaller level (Small or Smallest). Photos get softer, but text and charts stay sharp in Keep text mode.</li><li>Split the deck into two files, for example the story and the appendix.</li><li>Send a link instead. For a full press kit, attach a light PDF and link to a shared folder with the full-size files.</li></ul><p>For press kits, do not shrink the photos you want media to publish. Journalists need high-resolution images with captions and credits. Compress the deck you send for reading, and keep originals in the folder. The <a href="../how-to-write-a-press-release/index.html">press release guide</a> covers what else to include.</p>

<h2>Is it safe to compress a confidential deck online?</h2>
<p>Many online compressors upload your file to their server to process it. For a deck under embargo or a client document, that is a real risk. File Shrinker does the work inside your browser tab: the file is not sent anywhere, there is no account and no tracking, and closing the tab clears it.</p><p>Sending video or audio too? See <a href="../how-to-compress-a-video-for-email-and-whatsapp/index.html">how to compress a video for email or WhatsApp</a> and <a href="../how-to-make-an-audio-file-smaller/index.html">how to make an audio file smaller</a>.</p>
