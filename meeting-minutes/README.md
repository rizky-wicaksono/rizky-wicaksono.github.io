# Meeting Minutes Maker

**Turn a meeting transcript into minutes of meeting or a client contact report, right in your browser. Free, no sign-up, no AI, and your transcript never leaves your computer.**

Live at **[rizky-wicaksono.github.io/meeting-minutes](https://rizky-wicaksono.github.io/meeting-minutes/)** · Indonesian interface: [`?lang=id`](https://rizky-wicaksono.github.io/meeting-minutes/?lang=id)

Built by [Rizky Wicaksono](https://rizky-wicaksono.github.io) as part of a public experiment in *public relations engineering* (more on that [below](#why-this-exists-public-relations-engineering)).

---

## What it does

1. **Reads a transcript.** Paste it, or open a `.txt`, `.srt` or `.vtt` file. It understands:
   - `[00:00 - 00:13] text` and `[00:00:00.000 --> 00:00:05.000] text` (MacWhisper, whisper.cpp)
   - `[00:13] text`, `00:13 text`
   - SRT and WebVTT subtitles, including `<v Name>` speaker tags
   - Google Meet and Gemini transcripts (a timestamp on its own line, then `Name: text`), and `**Speaker 1 (00:12):** text`
   - Otter and MacWhisper speaker blocks (`Name  0:03` on one line, the text below)
   - `Name: text` lines, and plain notes with no timestamps at all
2. **Suggests lines** for Agenda, Decisions, Action items and open points, using Indonesian and English word rules: *action item, follow up, tindak lanjut, deadline, harus, perlu, paling lambat, akan, tolong, disetujui, sepakat, diputuskan, kita putuskan, agreed, decided, next steps, by Friday*, days and dates (*Senin, besok, minggu depan, 12 Desember, 12/12*), and *belum sepakat / not decided yet* for open points. For action items it suggests **who** (a participant or speaker named in the line, or the speaker when they say “saya akan” / “I’ll”) and **when**. Matches are highlighted so you can see why a line was picked.
3. **You decide.** Add suggestions to a section with a button or by dragging, edit every line, reorder or remove items, and add your own. Each item keeps its source timestamp and speaker as a small note; tick a box to include those notes in the output.
4. **Exports** a live preview, **Copy text** (pastes with formatting into Google Docs, Word or email), **Download .md** and **Download .docx**.

Section titles can be renamed to match a house template, the output can be Indonesian or English (independently of the interface language), and there is a *Contact report* mode with an optional closing line asking the client to flag anything that differs.

**It is semi-automatic on purpose.** The rules are simple and will miss things and flag things that are not tasks. Check every decision, number and deadline against the recording before sending.

## Privacy

- Everything runs in the browser tab. The page's Content Security Policy sets `connect-src 'none'`, so it cannot send the transcript anywhere even by mistake.
- Nothing is stored unless you click **Save draft in this browser**, which keeps one draft in `localStorage` on that device. **Clear everything** removes it.
- No accounts, analytics, cookies or third-party code. Fonts are self-hosted.

## Files

```
index.html   the page and its layout CSS
app.js       interface, sections, drag and drop, preview, export, draft
parse.js     transcript parser and the word rules (also runs in Node for testing)
docx.js      a small hand-written .docx writer: WordprocessingML + a ZIP writer (store method), no library
samples.js   made-up sample transcripts (Indonesian, English, mixed)
theme.css    shared look with rizky-wicaksono.github.io and File Shrinker
fonts/       Manrope, self-hosted
licenses/    font license
```

The folder is copied as-is into the site by `_src/build.py` (see `STATIC` in `_src/data.py`), so it is served at `/meeting-minutes/`. To try it locally, run a web server from the repository root, for example `python3 -m http.server`, and open `http://localhost:8000/meeting-minutes/`.

## Why this exists: public relations engineering

Marketing has had "marketing engineers" and growth engineers for years: people who know the craft *and* can build the tools that make it faster. Public relations mostly doesn't have that role yet. I'm trying to build it.

I'm Rizky Wicaksono, a PR consultant based in Jakarta. As a **public relations engineer**, my aim is to:

- **Use AI and just enough code to cut repetitive PR work** such as media monitoring, first drafts, media lists and reporting, so more time goes to strategy and relationships.
- **Turn PR playbooks into small tools that can be reused** by me, my team, and anyone else who finds them useful.
- **Write openly about what works and what doesn't**, including the failures.

Minutes and contact reports are a good example. Every client meeting ends with one, it is the record everyone goes back to when a deadline or an approval is disputed, and it usually gets written late at night from memory. A transcript helps, but pasting a confidential client meeting into an online AI summariser is a risk many clients would not accept. So this tool does the boring part (finding the lines that look like decisions and tasks) on your own device, and leaves the judgement to you.

Guide: [How to write meeting minutes from a transcript](https://rizky-wicaksono.github.io/guides/how-to-write-meeting-minutes-from-a-transcript/) · [Cara membuat notulen rapat dari transkrip](https://rizky-wicaksono.github.io/id/guides/cara-membuat-notulen-rapat-dari-transkrip/)

More tools: **[rizky-wicaksono.github.io/tools](https://rizky-wicaksono.github.io/tools/)**

---

Made by [Rizky Wicaksono](https://rizky-wicaksono.github.io), public relations engineer in the making.
