/* Transcript parsing and rule-based candidate extraction. Plain word rules, no AI, no network.
   Works in the browser (window.MinutesParse) and in Node (module.exports) for testing.

   parse(text)   -> { format, segments: [{ start, end, speaker, text }] }
   extract(segments, participants) -> [{ id, seg, start, speaker, text, tags, score, ranges, who, when, whoOptions }] */
(function (root) {
  "use strict";

  // ---------------------------------------------------------------- timestamps
  const T = "(\\d{1,2}:\\d{2}(?::\\d{2})?(?:[.,]\\d{1,3})?)";
  const pad = (n) => String(n).padStart(2, "0");

  function normTs(s) {
    if (!s) return "";
    const p = s.replace(/[.,]\d+$/, "").split(":").map(Number);
    let h = 0, m, sec;
    if (p.length === 3) [h, m, sec] = p; else [m, sec] = p;
    if (m >= 60) { h += Math.floor(m / 60); m %= 60; }
    return h ? `${h}:${pad(m)}:${pad(sec)}` : `${pad(m)}:${pad(sec)}`;
  }

  // ---------------------------------------------------------------- speaker names
  const NAME_WORD = "[A-Z\\u00C0-\\u00DE][\\w\\u00C0-\\u024F.'\\u2019-]*";
  const NAME = `((?:Speaker|SPEAKER|Pembicara|Peserta|Narasumber|Interviewer|Moderator)[ _]?\\d{0,2}[A-Z]?|${NAME_WORD}(?:\\s+(?:${NAME_WORD}|bin|binti|van|de|da|\\d{1,2})){0,3}(?:\\s*\\([^)]{1,30}\\))?)`;
  const NOT_SPEAKER = new Set(("note notes catatan agenda keputusan decision decisions action actions https http re subject perihal " +
    "tanggal date time waktu lokasi location tempat topik topic deadline ps nb tujuan purpose summary ringkasan hasil result " +
    "kesimpulan conclusion next pertanyaan question jawaban answer contoh example update status poin point budget anggaran " +
    "transcript transkrip peserta participants hadir attendees").split(" "));

  function speakerOk(name) {
    if (!name || name.length > 42) return false;
    const first = name.split(/\s+/)[0].toLowerCase().replace(/[^a-zÀ-ɏ]/g, "");
    return !NOT_SPEAKER.has(first);
  }

  const RE = {
    cue: new RegExp(`^${T}\\s*-->\\s*${T}`),
    range: new RegExp(`^[\\[(]?${T}\\s*(?:-->|–|—|-|to|s\\.d\\.|sd)\\s*${T}[\\])]?\\s*[:\\-–|]?\\s*(.*)$`),
    tsLead: new RegExp(`^[\\[(]${T}[\\])]\\s*[:\\-–|]?\\s*(.*)$`),
    tsBare: new RegExp(`^${T}\\s+[-–|:]?\\s*(.+)$`),
    tsAlone: new RegExp(`^[\\[(]?${T}[\\])]?$`),
    nameTs: new RegExp(`^${NAME}\\s*[\\[(]?${T}[\\])]?\\s*$`),
    nameTsColon: new RegExp(`^${NAME}\\s*[\\[(]${T}[\\])]\\s*[:\\-–]\\s*(.+)$`),
    nameColon: new RegExp(`^${NAME}\\s*:\\s*(.*)$`),
    nameAlone: new RegExp(`^((?:Speaker|SPEAKER|Pembicara)[ _]?\\d{1,2}[A-Z]?|${NAME_WORD}(?:\\s+${NAME_WORD}){0,3}:)$`),
    header: /^(transcript|transkrip|transcription|notes|catatan|webvtt.*|kind:.*|language:.*)$/i,
  };

  function splitSpeaker(text) {
    const m = text.match(RE.nameColon);
    if (m && m[2] && speakerOk(m[1])) return { speaker: m[1].trim(), text: m[2].trim() };
    return { speaker: "", text };
  }

  function clean(line) {
    return line.replace(/\*\*|__/g, "").replace(/^\s*[-•*>]\s+/, "").replace(/\s+/g, " ").trim();
  }

  // ---------------------------------------------------------------- parse
  function parseCues(lines, isVtt) {
    const segs = [];
    let cur = null;
    for (const raw of lines) {
      const line = raw.trim();
      const m = line.match(RE.cue);
      if (m) { cur = { start: normTs(m[1]), end: normTs(m[2]), speaker: "", text: "" }; segs.push(cur); continue; }
      if (!line) { cur = null; continue; }
      if (!cur) continue; // index numbers, WEBVTT header, NOTE blocks
      let t = line;
      const v = t.match(/^<v(?:\.[^ >]*)?\s+([^>]+)>/);
      if (v) cur.speaker = cur.speaker || v[1].trim();
      t = t.replace(/<[^>]+>/g, "").trim();
      if (!cur.text && !cur.speaker) {
        const s = splitSpeaker(t);
        cur.speaker = s.speaker; t = s.text;
      }
      cur.text = (cur.text ? cur.text + " " : "") + t;
    }
    return { format: isVtt ? "vtt" : "srt", segments: merge(segs.filter((s) => s.text)) };
  }

  // Subtitle cues are often half sentences: join a cue to the previous one when it is the same speaker
  // and the previous one did not end a sentence.
  function merge(segs) {
    const out = [];
    for (const s of segs) {
      const p = out[out.length - 1];
      if (p && p.speaker === s.speaker && !/[.!?…]["”’)]?$/.test(p.text) && p.text.length < 300) {
        p.text += " " + s.text; p.end = s.end || p.end;
      } else out.push({ ...s });
    }
    return out;
  }

  function parse(input) {
    const text = String(input || "").replace(/^﻿/, "").replace(/\r\n?/g, "\n");
    const lines = text.split("\n");
    const isVtt = /^\s*WEBVTT/.test(text);
    if (isVtt || lines.some((l) => RE.cue.test(l.trim()))) return parseCues(lines, isVtt);

    const segs = [];
    let curTs = "", curSpeaker = "", last = null, joinable = false;
    const kinds = new Set();
    const add = (start, end, speaker, t, canJoin) => {
      last = { start: start || "", end: end || "", speaker: speaker || "", text: t };
      segs.push(last);
      joinable = canJoin;
    };
    for (const raw of lines) {
      const line = clean(raw);
      if (!line) { joinable = false; continue; }
      if (RE.header.test(line)) continue;
      let m;
      if ((m = line.match(RE.range))) {
        kinds.add("range");
        const s = splitSpeaker(m[3]);
        if (s.speaker) curSpeaker = s.speaker;
        add(normTs(m[1]), normTs(m[2]), s.speaker || (s.text ? "" : ""), s.text, false);
        if (!s.text) joinable = true;
        continue;
      }
      if ((m = line.match(RE.nameTsColon)) && speakerOk(m[1])) {
        kinds.add("speaker-time");
        curSpeaker = m[1].trim(); curTs = normTs(m[2]);
        add(curTs, "", curSpeaker, m[3], true);
        continue;
      }
      if ((m = line.match(RE.tsAlone))) { kinds.add("time-line"); curTs = normTs(m[1]); joinable = false; continue; }
      if ((m = line.match(RE.nameTs)) && speakerOk(m[1])) {
        kinds.add("speaker-block");
        curSpeaker = m[1].trim(); curTs = normTs(m[2]); joinable = false;
        last = null;
        continue;
      }
      if ((m = line.match(RE.tsLead)) || (m = line.match(RE.tsBare))) {
        kinds.add("time");
        const s = splitSpeaker(m[2]);
        add(normTs(m[1]), "", s.speaker, s.text, false);
        continue;
      }
      if ((m = line.match(RE.nameAlone)) && speakerOk(m[1].replace(/:$/, ""))) {
        kinds.add("speaker-block");
        curSpeaker = m[1].replace(/:$/, "").trim(); joinable = false; last = null;
        continue;
      }
      const s = splitSpeaker(line);
      if (s.speaker) {
        kinds.add("speaker");
        curSpeaker = s.speaker;
        add(curTs, "", s.speaker, s.text, true);
        continue;
      }
      // a continuation line: join it to the previous segment in the same paragraph
      if (last && joinable) { last.text = (last.text ? last.text + " " : "") + line; continue; }
      if (last && !last.text) { last.text = line; joinable = true; continue; }
      add(curTs, "", curSpeaker, line, true);
    }
    let format = "plain";
    if (kinds.has("range")) format = "range";
    else if (kinds.has("speaker-time")) format = "speaker-time";
    else if (kinds.has("time-line") && kinds.has("speaker")) format = "meet";
    else if (kinds.has("speaker-block")) format = "speaker-block";
    else if (kinds.has("time")) format = "time";
    else if (kinds.has("speaker")) format = "speaker";
    return { format, segments: segs.filter((s) => s.text) };
  }

  // ---------------------------------------------------------------- extraction rules
  const L = "\\p{L}\\p{N}";
  const W = (src) => new RegExp(`(?<![${L}])(?:${src})(?![${L}])`, "giu");

  const DAYS_ID = "senin|selasa|rabu|kamis|jum'?at|sabtu";
  const DAYS_EN = "monday|tuesday|wednesday|thursday|friday|saturday|sunday";
  const MONTHS = "januari|februari|pebruari|maret|april|mei|juni|juli|agustus|september|oktober|november|nopember|desember|" +
    "january|february|march|may|june|july|august|october|december|jan|feb|mar|apr|jun|jul|agu|aug|sep|sept|okt|oct|nov|des|dec";

  const RULES = {
    action: [
      [2, W("action items?|follow[ -]?up|tindak ?lanjut(?:i|nya)?|ditindaklanjuti|deadline(?:nya)?|tenggat|paling lambat|selambat-lambatnya|next steps?|langkah (?:selanjutnya|berikutnya)|to-?do|pic(?:nya)?|tolong|mohon|harus|wajib|perlu|need(?:s)? to|have to|has to|must|please|assign(?:ed)?|due")],
      [2, W("(?:i|we)'ll|(?:i|we) will|i can (?:send|share|prepare|draft|check)|let me|saya akan|kami akan|aku akan|kita akan|nanti saya|biar saya|saya yang|aku yang|saya (?:kirim|siapkan|cek|buat|follow up|update|kabari)|akan (?:dikirim|disiapkan|dibuat|dicek|dikabari|diupdate)")],
      [1, W("akan|will|should|sebaiknya|kirim(?:kan)?|siapkan|send|share|prepare|draft|update|cek|check|review|revisi|revise|confirm|konfirmasi|kabari|by")],
    ],
    decision: [
      [2, W("disetujui|setuju|sepakat|disepakati|kesepakatan(?:nya)?|diputuskan|(?:kita|kami) putuskan|memutuskan|keputusan(?:nya)?|approved?|agreed?|decided?|decision|(?:we'?ll|let'?s|we) go with|confirmed|dikonfirmasi|settled|sudah final|udah final|sudah fix|udah fix|final ya|fix ya|deal")],
      [2, W("(?:ok(?:e|ay)?|jadi|ya) kita (?:pakai|pilih|ambil|jalan|pakai)|pakai opsi|pilih opsi|kita pilih|kita pakai")],
    ],
    agenda: [
      [2, W("agenda(?:nya)?|topik|topic|membahas|pembahasan|dibahas|(?:kita|mau|akan) bahas|discuss(?:ion)?|first item|item pertama|poin (?:pertama|kedua|ketiga|berikut(?:nya)?|selanjutnya)|next (?:topic|item|point)|moving on|lanjut ke|selanjutnya kita")],
    ],
    open: [
      [2, W("tidak setuju|belum (?:disetujui|sepakat|diputuskan|final|fix|ada keputusan)|not (?:yet )?(?:agreed|decided|approved|confirmed|final)|(?:haven'?t|hasn'?t|have not|has not)(?: yet)? (?:been )?(?:decided|agreed|approved|confirmed)|don'?t agree|disagree|masih (?:dibahas|didiskusikan|pending)|tbc|tbd|to be confirmed|pending")],
    ],
  };

  const DAY = `(?:hari )?(?:${DAYS_ID}|${DAYS_EN})`;
  const DM = `\\d{1,2} (?:${MONTHS})\\.?(?: \\d{4})?`;
  const MD = `(?:${MONTHS}) \\d{1,2}(?:st|nd|rd|th)?(?:,? \\d{4})?`;
  const DATE_RE = W([
    `${DAY},? (?:${DM}|${MD})`,
    `(?:tanggal|tgl\\.?) (?:${DM}|\\d{1,2})`,
    `${DAY}(?: (?:depan|ini|besok|next))?`,
    DM, MD,
    `\\d{1,2}[/.-]\\d{1,2}(?:[/.-]\\d{2,4})?`,
    "besok(?: pagi| siang| sore)?|lusa|minggu depan|bulan depan|pekan depan|akhir (?:minggu|pekan|bulan)(?: ini)?|hari ini|nanti sore|nanti malam",
    "tomorrow|next (?:week|month|monday|tuesday|wednesday|thursday|friday)|(?:the )?end of (?:the )?(?:day|week|month)|eod|eow|this (?:week|friday|monday)|today",
    "(?:jam|pukul) \\d{1,2}(?:[.:]\\d{2})?(?: (?:pagi|siang|sore|malam|wib))?",
    "\\d{1,2}(?:[.:]\\d{2})? ?(?:am|pm|wib)",
    "q[1-4]",
  ].join("|"));
  // "Minggu" is both Sunday and "week": only count the capitalised day, or "hari minggu".
  const SUNDAY_RE = /(?<![\p{L}])(?:hari minggu|Minggu)(?![\p{L}])/gu;

  const STOP_CAPS = new Set(("I OK Oke Ok Ya Iya Yes No Tidak Jadi Terus Lalu Nah Nanti Kalau Kita Kami Saya Aku Kamu Anda Dia Mereka Ini Itu Untuk Dan Atau Tapi Tetapi " +
    "The A An And But So We You They He She It This That Then Also Please Thanks Thank Okay Right Sure Yeah Great Good Hi Hello Halo Pak Bu Ibu Bapak Mas Mbak " +
    "Senin Selasa Rabu Kamis Jumat Sabtu Minggu Monday Tuesday Wednesday Thursday Friday Saturday Sunday Januari Februari Maret April Mei Juni Juli Agustus September Oktober November Desember " +
    "January February March May June July August October December PR AI CEO CMO KOL KPI Q1 Q2 Q3 Q4 Zoom Meet Google Teams WhatsApp WA Instagram TikTok Excel Word Deck").split(" "));

  function matchAll(re, text, cls, out) {
    re.lastIndex = 0;
    let m, found = [];
    while ((m = re.exec(text))) {
      if (!m[0]) { re.lastIndex++; continue; }
      out.push({ s: m.index, e: m.index + m[0].length, cls });
      found.push(m[0]);
    }
    return found;
  }

  function sentences(text) {
    return text.split(/(?<=[.!?…])\s+(?=["“‘'(\[]?[\p{Lu}\p{N}])/u).map((s) => s.trim()).filter(Boolean);
  }

  function nameList(participants, segments) {
    const set = new Map();
    const addName = (n) => {
      n = (n || "").replace(/\s*\([^)]*\)\s*/g, " ").trim();
      if (!n || /^(speaker|pembicara|peserta)\b/i.test(n) || n.length > 40) return;
      set.set(n.toLowerCase(), n);
    };
    (participants || []).forEach(addName);
    (segments || []).forEach((s) => addName(s.speaker));
    return [...set.values()];
  }

  const FIRST_PERSON = /(?<![\p{L}])(?:saya akan|saya yang|saya mau|saya (?:kirim|siapkan|cek|buat|update|kabari|follow)|nanti saya|biar saya|aku akan|aku yang|gue|gw|i'll|i will|i can|i need to|i have to|i'm going to|let me|on my side|dari saya)(?![\p{L}])/iu;
  const RECIPIENT = /(?:ke|kepada|untuk|dengan|to|with|for|from|dari)\s+$/i;

  function findWho(text, speaker, names) {
    const first = [], later = [];
    const has = (n) => first.concat(later).some((w) => w.toLowerCase() === n.toLowerCase());
    const push = (n, idx) => {
      n = n.trim();
      if (!n || has(n)) return;
      // a name right after "ke / to / with" is usually who receives the work, not who does it
      (idx != null && RECIPIENT.test(text.slice(Math.max(0, idx - 12), idx).replace(/\s*(?:Pak|Bu|Ibu|Bapak|Mas|Mbak|Mr\.?|Ms\.?)\s*$/, " ")) ? later : first).push(n);
    };
    const clean = (s) => (s || "").replace(/\s*\([^)]*\)/, "").trim();
    if (speaker && FIRST_PERSON.test(text)) push(clean(speaker));
    const esc = (w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    for (const n of names) {
      const fn = n.split(/\s+/)[0];
      let m = new RegExp(`(?<![\\p{L}])${esc(n)}(?![\\p{L}])`, "iu").exec(text);
      if (!m && fn.length >= 3 && !STOP_CAPS.has(fn)) m = new RegExp(`(?<![\\p{L}])${esc(fn)}(?![\\p{L}])`, "u").exec(text);
      if (m) push(n, m.index);
    }
    const hon = /(?<![\p{L}])(Pak|Bu|Ibu|Bapak|Mas|Mbak|Kak|Bang|Mr\.?|Ms\.?|Mrs\.?)\s+(\p{Lu}[\p{L}'-]+)/gu;
    let m;
    while ((m = hon.exec(text))) {
      const known = names.find((n) => n.toLowerCase().split(/\s+/).includes(m[2].toLowerCase()));
      push(known || `${m[1]} ${m[2]}`, m.index);
    }
    const team = /(?<![\p{L}])(?:[Tt]im|[Tt]eam)\s+(\p{Lu}[\p{L}&-]*|[a-z]{3,}(?= (?:akan|will|yang|harus|perlu|bisa)))/gu;
    while ((m = team.exec(text))) push(/^team/i.test(m[0]) ? `${m[1]} team` : `Tim ${m[1]}`, m.index);
    const lead = text.match(/^(\p{Lu}\p{Ll}{2,})\s+(?:akan|harus|perlu|yang|bisa|will|needs?|should|must|can|to)\b/u);
    if (lead && !STOP_CAPS.has(lead[1])) push(lead[1], 0);
    if (!first.length && !later.length) {
      const words = text.split(/\s+/);
      for (let i = 1; i < words.length; i++) {
        const w = words[i].replace(/[^\p{L}'-]/gu, "");
        if (/^\p{Lu}\p{Ll}{2,}$/u.test(w) && !STOP_CAPS.has(w) && !/[.!?:]$/.test(words[i - 1])) { push(w); break; }
      }
    }
    return first.concat(later);
  }

  function extract(segments, participants) {
    const names = nameList(participants, segments);
    const out = [];
    let n = 0;
    segments.forEach((seg, si) => {
      for (const text of sentences(seg.text)) {
        const ranges = [];
        const tags = [];
        const score = {};
        for (const [kind, rules] of Object.entries(RULES)) {
          let sc = 0;
          for (const [w, re] of rules) sc += w * Math.min(2, matchAll(re, text, kind, ranges).length);
          score[kind] = sc;
        }
        const dates = matchAll(DATE_RE, text, "date", ranges).concat(matchAll(SUNDAY_RE, text, "date", ranges));
        if (score.open) { score.decision = 0; tags.push("open"); }
        const actionNeed = score.agenda >= 2 ? 3 : 2; // "today we'll discuss" is an agenda line, not a task
        if (score.action >= actionNeed || (score.action >= 1 && dates.length && !score.agenda)) tags.push("action");
        if (score.decision >= 2) tags.push("decision");
        if (score.agenda >= 2) tags.push("agenda");
        if (dates.length) tags.push("date");
        const who = tags.includes("action") ? findWho(text, seg.speaker, names) : [];
        out.push({
          id: "c" + n++, seg: si, start: seg.start, speaker: seg.speaker, text, tags,
          strength: Math.max(score.action || 0, score.decision || 0, score.agenda || 0, score.open || 0),
          ranges: tidy(ranges.filter((r) => r.cls === "date" || tags.includes(r.cls))),
          who: who[0] || "", whoOptions: who, when: (dates[0] || "").replace(/[.,]$/, ""),
        });
      }
    });
    return out;
  }

  function tidy(ranges) {
    ranges.sort((a, b) => a.s - b.s || b.e - a.e);
    const out = [];
    for (const r of ranges) {
      const p = out[out.length - 1];
      if (p && r.s < p.e) continue;
      out.push(r);
    }
    return out;
  }

  const api = { parse, extract, normTs, sentences, nameList };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.MinutesParse = api;
})(typeof window !== "undefined" ? window : globalThis);
