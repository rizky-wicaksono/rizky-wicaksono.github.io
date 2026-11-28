/* Meeting Minutes Maker: page logic. Everything stays in this tab; nothing is sent anywhere.
   Uses MinutesParse (parse.js), MinutesSamples (samples.js) and MinutesDocx (docx.js). */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const DRAFT_KEY = "meeting-minutes:draft";
  const SITE = "https://rizky-wicaksono.github.io";
  const SECS = ["participants", "agenda", "discussion", "decisions", "actions"];

  // ------------------------------------------------------------------ interface text
  const U = {
    en: {
      skip: "Skip to the tool", navTools: "Tools", navWork: "Work", navGuides: "PR Guides", navContact: "Contact", crumb: "← All tools",
      h1: "Meeting Minutes Maker",
      lead: "Turn a meeting transcript into minutes or a client contact report: agenda, discussion, decisions and action items. You pick what goes in; the tool only suggests.",
      trust1: "Free, no sign-up", trust2: "Nothing is uploaded", trust3: "No AI: simple word rules you can check",
      sTranscript: "Transcript", loadFile: "Open .txt / .srt / .vtt file", sampleLabel: "Load a sample transcript",
      sampleNone: "Try a sample transcript…", sampleId: "Sample: Indonesian, [00:00 - 00:13] style", sampleEn: "Sample: English, SRT subtitles", sampleMixed: "Sample: mixed, Google Meet style",
      transcriptLabel: "Transcript text", transcriptPh: "Paste the transcript here, or drop a .txt, .srt or .vtt file on this box.\n\nWorks with [00:00 - 00:13] text, [00:13] text, SRT/VTT subtitles, Google Meet and Gemini transcripts, MacWhisper and Otter exports, “Name: text” lines and plain text.",
      sDetails: "Meeting details", fTitle: "Meeting title", fTitlePh: "e.g. Media briefing preparation", fDate: "Date", fType: "Document type",
      typeMom: "Minutes of meeting", typeContact: "Contact report", fClient: "Client / organisation", fLocation: "Location / platform", fLocationPh: "e.g. Zoom, client office",
      fParticipants: "Participants", fParticipantsHint: "One per line, or separated by commas.", fPrepared: "Prepared by",
      fClosing: "Closing note (optional)", fClosingHint: "Common in contact reports: ask the other side to flag anything that differs from their notes.", closingBtn: "Use the standard line",
      sCands: "Suggestions from the transcript",
      semiAuto: "Semi-automatic. These lines were picked by simple word rules (like “deadline”, “agreed”, “please”, a day or a date), not by AI. They will miss things and flag things that are not tasks. Check every line against the recording before you send the minutes.",
      showAll: "Show every line (to add discussion points)", sSections: "Minutes",
      secHint: "Drag suggestions here, or use the Add buttons. Edit any text. Section titles can be renamed to match your template.",
      sOutput: "Preview and export", outLang: "Output language", incSrc: "Include source time and speaker", resetTitles: "Reset section titles",
      copy: "Copy text", dlMd: "Download .md", dlDocx: "Download .docx (Word)",
      sPrivacy: "Privacy",
      priv1: "Everything happens in this browser tab. The transcript is not uploaded, and this page makes no network requests while you work. Close the tab and it is gone.",
      priv2: "Nothing is saved unless you click “Save draft in this browser”. That keeps one draft in this browser’s local storage on this device only, until you clear it. Do not use it on a shared computer.",
      saveDraft: "Save draft in this browser", loadDraft: "Restore saved draft", clearAll: "Clear everything",
      guideLead: "How to write minutes people can trust, and why the recording still matters:", guideLink: "read the guide",
      foot: "Meeting Minutes Maker is made by Rizky Wicaksono, public relations engineer. Free to use. Your transcript never leaves this browser.",
      footTools: "All tools", footHome: "Portfolio", footSrc: "Source on GitHub",
      // dynamic
      fmt: { srt: "SRT subtitles", vtt: "WebVTT subtitles", range: "[start - end] timestamps", "speaker-time": "speaker with timestamp", meet: "Google Meet / Gemini style", "speaker-block": "speaker blocks (Otter / MacWhisper style)", time: "[time] timestamps", speaker: "“Name: text” lines", plain: "plain text, no timestamps" },
      parsed: (f, n, s, k) => `Read as <b>${f}</b>: ${n} ${n === 1 ? "passage" : "passages"}${s ? `, ${s} ${s === 1 ? "speaker" : "speakers"}` : ""}. <b>${k}</b> ${k === 1 ? "suggestion" : "suggestions"} below.`,
      noText: "Paste a transcript or try a sample to see suggestions.",
      fAll: "Suggested", fAction: "Action items", fDecision: "Decisions", fAgenda: "Agenda", fOpen: "Open points", fDate: "Dates",
      tag: { action: "Possible action", decision: "Possible decision", agenda: "Agenda?", open: "Not decided?", date: "Date" },
      addTo: "Add to:", added: (s) => `✓ Added to ${s}`, sugg: "Suggested", who: "Who", what: "What", when: "When",
      noCands: "No lines matched the rules. Turn on “Show every line” to pick discussion points yourself.",
      dragHere: "Drop suggestions here or add an item.", addItem: "+ Add item", addAction: "+ Add action item",
      partFromForm: "From the Participants field in step 2.", partSpeakers: "Speakers in the transcript, not in the list yet:", partNone: "No participants yet. Fill in step 2 or add speakers below.",
      up: "Move up", down: "Move down", remove: "Remove", secTitle: "Section title", itemText: "Item text",
      copied: "Copied. Paste it into an email, Google Docs or Word.", copyFail: "Could not copy automatically. Select the preview and copy it.",
      saved: (t) => `Draft saved in this browser at ${t}. It stays until you click “Clear everything”.`, restored: "Draft restored.", noStorage: "This browser blocked local storage, so the draft could not be saved.",
      cleared: "Everything cleared, including any saved draft.", confirmClear: "Clear the transcript, details, minutes and any saved draft in this browser? This cannot be undone.",
      confirmSample: "Replace the current transcript, meeting details and minutes with the sample?", draftExists: (t) => `A draft saved in this browser on ${t} is available.`,
      emptyDoc: "The preview appears here as you add items.", leave: "Your minutes are not saved. Leave anyway?",
      downloaded: (f) => `Saved ${f}.`, fileRead: (f) => `Opened ${f}.`, fileErr: "Could not read that file. Use a plain text, .srt or .vtt file.",
    },
    id: {
      skip: "Lompat ke alat", navTools: "Tools", navWork: "Karya", navGuides: "Panduan PR", navContact: "Kontak", crumb: "← Semua alat",
      h1: "Pembuat Notulen Rapat",
      lead: "Ubah transkrip rapat menjadi notulen atau contact report untuk klien: agenda, pembahasan, keputusan, dan tindak lanjut. Anda yang memilih isinya; alat ini hanya memberi saran.",
      trust1: "Gratis, tanpa daftar", trust2: "Tidak ada yang diunggah", trust3: "Tanpa AI: aturan kata sederhana yang bisa dicek",
      sTranscript: "Transkrip", loadFile: "Buka file .txt / .srt / .vtt", sampleLabel: "Muat contoh transkrip",
      sampleNone: "Coba contoh transkrip…", sampleId: "Contoh: bahasa Indonesia, format [00:00 - 00:13]", sampleEn: "Contoh: bahasa Inggris, subtitle SRT", sampleMixed: "Contoh: campuran, gaya Google Meet",
      transcriptLabel: "Teks transkrip", transcriptPh: "Tempel transkrip di sini, atau jatuhkan file .txt, .srt, atau .vtt ke kotak ini.\n\nBisa membaca [00:00 - 00:13] teks, [00:13] teks, subtitle SRT/VTT, transkrip Google Meet dan Gemini, ekspor MacWhisper dan Otter, baris “Nama: teks”, dan teks biasa.",
      sDetails: "Detail rapat", fTitle: "Judul rapat", fTitlePh: "mis. Persiapan media briefing", fDate: "Tanggal", fType: "Jenis dokumen",
      typeMom: "Notulen rapat (MoM)", typeContact: "Contact report", fClient: "Klien / organisasi", fLocation: "Tempat / platform", fLocationPh: "mis. Zoom, kantor klien",
      fParticipants: "Peserta", fParticipantsHint: "Satu per baris, atau dipisah koma.", fPrepared: "Disusun oleh",
      fClosing: "Catatan penutup (opsional)", fClosingHint: "Lazim di contact report: minta pihak lain memberi tahu jika ada yang berbeda dari catatan mereka.", closingBtn: "Pakai kalimat standar",
      sCands: "Saran dari transkrip",
      semiAuto: "Semi-otomatis. Baris ini dipilih dengan aturan kata sederhana (seperti “deadline”, “disepakati”, “tolong”, nama hari, atau tanggal), bukan AI. Pasti ada yang terlewat dan ada yang salah tandai. Cek setiap baris dengan rekamannya sebelum notulen dikirim.",
      showAll: "Tampilkan semua baris (untuk menambah poin pembahasan)", sSections: "Notulen",
      secHint: "Seret saran ke sini, atau pakai tombol Tambah. Semua teks bisa diedit. Judul bagian bisa diganti agar sesuai template Anda.",
      sOutput: "Pratinjau dan ekspor", outLang: "Bahasa dokumen", incSrc: "Sertakan waktu dan pembicara sumber", resetTitles: "Kembalikan judul bagian",
      copy: "Salin teks", dlMd: "Unduh .md", dlDocx: "Unduh .docx (Word)",
      sPrivacy: "Privasi",
      priv1: "Semua proses terjadi di tab browser ini. Transkrip tidak diunggah, dan halaman ini tidak membuat permintaan jaringan selama Anda bekerja. Tutup tab, semuanya hilang.",
      priv2: "Tidak ada yang disimpan kecuali Anda mengklik “Simpan draf di browser ini”. Itu menyimpan satu draf di penyimpanan lokal browser ini, hanya di perangkat ini, sampai Anda menghapusnya. Jangan dipakai di komputer bersama.",
      saveDraft: "Simpan draf di browser ini", loadDraft: "Pulihkan draf tersimpan", clearAll: "Hapus semuanya",
      guideLead: "Cara menulis notulen yang bisa dipercaya, dan kenapa rekaman tetap penting:", guideLink: "baca panduannya",
      foot: "Pembuat Notulen Rapat dibuat oleh Rizky Wicaksono, public relations engineer. Gratis. Transkrip Anda tidak pernah keluar dari browser ini.",
      footTools: "Semua alat", footHome: "Portofolio", footSrc: "Kode sumber di GitHub",
      fmt: { srt: "subtitle SRT", vtt: "subtitle WebVTT", range: "timestamp [mulai - selesai]", "speaker-time": "pembicara dengan timestamp", meet: "gaya Google Meet / Gemini", "speaker-block": "blok per pembicara (gaya Otter / MacWhisper)", time: "timestamp [waktu]", speaker: "baris “Nama: teks”", plain: "teks biasa, tanpa timestamp" },
      parsed: (f, n, s, k) => `Terbaca sebagai <b>${f}</b>: ${n} bagian${s ? `, ${s} pembicara` : ""}. <b>${k}</b> saran di bawah.`,
      noText: "Tempel transkrip atau coba contoh untuk melihat saran.",
      fAll: "Disarankan", fAction: "Tindak lanjut", fDecision: "Keputusan", fAgenda: "Agenda", fOpen: "Belum diputuskan", fDate: "Tanggal",
      tag: { action: "Mungkin tindak lanjut", decision: "Mungkin keputusan", agenda: "Agenda?", open: "Belum diputuskan?", date: "Tanggal" },
      addTo: "Tambah ke:", added: (s) => `✓ Masuk ke ${s}`, sugg: "Saran", who: "Siapa", what: "Apa", when: "Kapan",
      noCands: "Tidak ada baris yang cocok dengan aturan. Nyalakan “Tampilkan semua baris” untuk memilih poin pembahasan sendiri.",
      dragHere: "Jatuhkan saran di sini atau tambah item.", addItem: "+ Tambah item", addAction: "+ Tambah tindak lanjut",
      partFromForm: "Dari kolom Peserta di langkah 2.", partSpeakers: "Pembicara di transkrip yang belum ada di daftar:", partNone: "Belum ada peserta. Isi di langkah 2 atau tambahkan pembicara di bawah.",
      up: "Naikkan", down: "Turunkan", remove: "Hapus", secTitle: "Judul bagian", itemText: "Teks item",
      copied: "Tersalin. Tempel ke email, Google Docs, atau Word.", copyFail: "Tidak bisa menyalin otomatis. Blok pratinjau lalu salin.",
      saved: (t) => `Draf tersimpan di browser ini pukul ${t}. Draf tetap ada sampai Anda klik “Hapus semuanya”.`, restored: "Draf dipulihkan.", noStorage: "Browser ini memblokir penyimpanan lokal, jadi draf tidak bisa disimpan.",
      cleared: "Semua sudah dihapus, termasuk draf tersimpan.", confirmClear: "Hapus transkrip, detail, notulen, dan draf yang tersimpan di browser ini? Tidak bisa dibatalkan.",
      confirmSample: "Ganti transkrip, detail rapat, dan notulen saat ini dengan contoh?", draftExists: (t) => `Ada draf yang tersimpan di browser ini pada ${t}.`,
      emptyDoc: "Pratinjau muncul di sini saat Anda menambah item.", leave: "Notulen belum disimpan. Tetap keluar?",
      downloaded: (f) => `Tersimpan: ${f}.`, fileRead: (f) => `Membuka ${f}.`, fileErr: "File tidak bisa dibaca. Gunakan file teks biasa, .srt, atau .vtt.",
    },
  };

  // ------------------------------------------------------------------ document text (output language)
  const O = {
    en: {
      mom: "Minutes of Meeting", contact: "Contact Report", date: "Date", client: "Client / organisation", location: "Location / platform", prepared: "Prepared by",
      sections: { participants: "Participants", agenda: "Agenda", discussion: "Discussion", decisions: "Decisions", actions: "Action items" },
      no: "No.", what: "Action", who: "Who", when: "When", locale: "en-GB",
      closing: "If any of the above differs from your understanding, please let us know within two working days. Otherwise we will take these notes as agreed.",
    },
    id: {
      mom: "Notulen Rapat", contact: "Contact Report", date: "Tanggal", client: "Klien / organisasi", location: "Tempat / platform", prepared: "Disusun oleh",
      sections: { participants: "Peserta", agenda: "Agenda", discussion: "Pembahasan", decisions: "Keputusan", actions: "Tindak lanjut (action items)" },
      no: "No.", what: "Tindakan", who: "Siapa", when: "Kapan", locale: "id-ID",
      closing: "Jika ada bagian yang berbeda dari pemahaman Anda, mohon kabari kami dalam dua hari kerja. Jika tidak ada tanggapan, catatan ini kami anggap telah disepakati.",
    },
  };

  // ------------------------------------------------------------------ state
  const blank = () => ({
    transcript: "",
    meta: { title: "", date: new Date().toISOString().slice(0, 10), type: "mom", client: "", location: "", participants: "", prepared: "", closing: "" },
    sections: { participants: [], agenda: [], discussion: [], decisions: [], actions: [] },
    titles: {}, outLang: null, incSrc: false,
  });
  let S = blank();
  let ui = new URLSearchParams(location.search).get("lang") || ((navigator.language || "").toLowerCase().startsWith("id") ? "id" : "en");
  if (!U[ui]) ui = "en";
  let parsed = { format: "plain", segments: [] }, cands = [], filter = "all", showAll = false, dirty = false, seq = 1;
  const nid = () => "i" + Date.now().toString(36) + (seq++);
  const t = (k) => U[ui][k];
  const outL = () => S.outLang || ui;
  const secTitle = (k) => (S.titles[k] != null && S.titles[k] !== "" ? S.titles[k] : O[outL()].sections[k]);

  // ------------------------------------------------------------------ language
  function applyUi() {
    document.documentElement.lang = ui;
    $$("[data-i]").forEach((el) => { const v = U[ui][el.dataset.i]; if (typeof v === "string") el.textContent = v; });
    $$("[data-i-ph]").forEach((el) => { el.placeholder = U[ui][el.dataset.iPh]; });
    $$("[data-ui-lang]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.uiLang === ui)));
    const pre = ui === "id" ? "/id" : "";
    const hrefs = { home: `${SITE}${pre}/`, tools: `${SITE}${pre}/tools/`, work: `${SITE}${pre}/#work`, guides: `${SITE}${pre}/guides/`, contact: `${SITE}${pre}/#contact` };
    $$("[data-href]").forEach((a) => { a.href = hrefs[a.dataset.href]; });
    $("#guideLink").href = ui === "id" ? `${SITE}/id/guides/cara-membuat-notulen-rapat-dari-transkrip/` : `${SITE}/guides/how-to-write-meeting-minutes-from-a-transcript/`;
    document.title = ui === "id" ? "Pembuat Notulen Rapat: ubah transkrip jadi notulen atau contact report" : "Meeting Minutes Maker: turn a transcript into minutes or a contact report";
    $("#outLang").value = outL();
    renderFilters(); renderCands(); renderSections(); renderPreview(); parseInfo(); draftInfo();
  }

  // ------------------------------------------------------------------ parsing
  function participants() {
    return S.meta.participants.split(/\n|,(?![^(]*\))/).map((s) => s.trim()).filter(Boolean);
  }
  function stripRole(n) { return n.replace(/\s*\([^)]*\)\s*/g, " ").trim(); }
  const candKey = (c) => (c.start || "") + "|" + c.text;

  function reparse() {
    parsed = MinutesParse.parse(S.transcript);
    cands = MinutesParse.extract(parsed.segments, participants().map(stripRole));
    renderFilters(); renderCands(); renderNames(); parseInfo(); renderSections();
  }
  function parseInfo() {
    const el = $("#parseInfo");
    if (!S.transcript.trim()) { el.textContent = t("noText"); return; }
    const speakers = new Set(parsed.segments.map((s) => s.speaker).filter(Boolean)).size;
    const k = cands.filter((c) => c.tags.length).length;
    el.innerHTML = t("parsed")(esc(t("fmt")[parsed.format] || parsed.format), parsed.segments.length, speakers, k);
  }
  function renderNames() {
    const names = MinutesParse.nameList(participants().map(stripRole), parsed.segments);
    $("#names").innerHTML = names.map((n) => `<option value="${esc(n)}">`).join("");
  }

  // ------------------------------------------------------------------ suggestions list
  const FILTERS = [["all", "fAll"], ["action", "fAction"], ["decision", "fDecision"], ["agenda", "fAgenda"], ["open", "fOpen"], ["date", "fDate"]];
  function renderFilters() {
    const n = (k) => (k === "all" ? cands.filter((c) => c.tags.length).length : cands.filter((c) => c.tags.includes(k)).length);
    $("#filters").innerHTML = FILTERS.map(([k, label]) =>
      `<button type="button" class="chip" data-filter="${k}" aria-pressed="${filter === k}">${esc(t(label))}<span class="c">${n(k)}</span></button>`).join("");
  }
  function highlight(text, ranges) {
    let out = "", p = 0;
    for (const r of ranges) { out += esc(text.slice(p, r.s)) + `<mark class="${r.cls}">${esc(text.slice(r.s, r.e))}</mark>`; p = r.e; }
    return out + esc(text.slice(p));
  }
  function primaryTarget(c) {
    if (c.tags.includes("open")) return "discussion";
    if (c.tags.includes("action")) return "actions";
    if (c.tags.includes("decision")) return "decisions";
    if (c.tags.includes("agenda")) return "agenda";
    return "discussion";
  }
  function addedTo(c) {
    const key = candKey(c);
    for (const k of SECS) if (S.sections[k].some((it) => it.from === key)) return k;
    return null;
  }
  function renderCands() {
    const list = cands.filter((c) => (showAll && filter === "all") || (filter === "all" ? c.tags.length : c.tags.includes(filter)));
    const el = $("#cands");
    if (!S.transcript.trim()) { el.innerHTML = `<li class="empty">${esc(t("noText"))}</li>`; return; }
    if (!list.length) { el.innerHTML = `<li class="empty">${esc(t("noCands"))}</li>`; return; }
    el.innerHTML = list.map((c) => {
      const prim = primaryTarget(c);
      const done = addedTo(c);
      const tags = c.tags.map((g) => `<span class="tag t-${g}">${esc(t("tag")[g])}</span>`).join("");
      const sugg = c.tags.includes("action") && (c.who || c.when)
        ? `<p class="sugg">${esc(t("sugg"))}: ${c.who ? `${esc(t("who"))} <b>${esc(c.who)}</b>` : ""}${c.who && c.when ? " · " : ""}${c.when ? `${esc(t("when"))} <b>${esc(c.when)}</b>` : ""}</p>` : "";
      const btns = ["agenda", "discussion", "decisions", "actions"].map((k) =>
        `<button type="button" data-add="${k}" class="${k === prim && c.tags.length ? "primary" : ""}">${esc(secTitle(k))}</button>`).join("");
      const pbtn = c.speaker ? `<button type="button" data-add="participants">${esc(secTitle("participants"))}</button>` : "";
      return `<li class="cand${done ? " added" : ""}" draggable="true" data-id="${c.id}">
        <div class="meta">${c.start ? `<span class="ts">${esc(c.start)}</span>` : ""}${c.speaker ? `<b>${esc(c.speaker)}</b>` : ""}${tags}</div>
        <p>${highlight(c.text, c.ranges)}</p>${sugg}
        <div class="adds">${done ? `<span>${esc(t("added")(secTitle(done)))}</span>` : `<span>${esc(t("addTo"))}</span>`}${btns}${pbtn}</div>
      </li>`;
    }).join("");
  }

  function addFromCand(c, sec, before) {
    if (sec === "participants") {
      const name = c.speaker;
      if (name && !participants().some((p) => stripRole(p).toLowerCase() === stripRole(name).toLowerCase())) {
        S.meta.participants = (S.meta.participants.trim() ? S.meta.participants.trim() + "\n" : "") + name;
        $("#m-participants").value = S.meta.participants;
        renderNames();
      }
      changed(); renderSections(); renderCands(); return;
    }
    const base = { id: nid(), from: candKey(c), ts: c.start || "", speaker: c.speaker || "" };
    const item = sec === "actions" ? { ...base, what: c.text, who: c.who || "", when: c.when || "" } : { ...base, text: c.text };
    const arr = S.sections[sec];
    const i = before ? arr.findIndex((x) => x.id === before) : -1;
    i >= 0 ? arr.splice(i, 0, item) : arr.push(item);
    changed(); renderSections(); renderCands();
  }

  // ------------------------------------------------------------------ sections editor
  function renderSections() {
    const box = $("#sections");
    const focused = document.activeElement && box.contains(document.activeElement) ? document.activeElement.dataset.focus : null;
    box.innerHTML = SECS.map((k) => {
      const items = S.sections[k];
      let body;
      if (k === "participants") {
        const ps = participants();
        const known = new Set(ps.map((p) => stripRole(p).toLowerCase()));
        const extra = [...new Set(parsed.segments.map((s) => s.speaker).filter(Boolean))].filter((n) => !known.has(stripRole(n).toLowerCase()));
        body = (ps.length ? `<ul class="pchips">${ps.map((p) => `<li>${esc(p)}</li>`).join("")}</ul><p class="hint-small">${esc(t("partFromForm"))}</p>` : `<p class="empty">${esc(t("partNone"))}</p>`) +
          (extra.length ? `<p class="hint-small">${esc(t("partSpeakers"))}</p><ul class="pchips">${extra.map((n) => `<li style="background:none;padding:0"><button type="button" data-speaker="${esc(n)}">+ ${esc(n)}</button></li>`).join("")}</ul>` : "");
      } else {
        body = `<ol class="items">${items.map((it, i) => itemHtml(k, it, i, items.length)).join("")}</ol>` +
          (items.length ? "" : `<p class="empty">${esc(t("dragHere"))}</p>`) +
          `<button type="button" class="btn small ghost" data-new="${k}">${esc(k === "actions" ? t("addAction") : t("addItem"))}</button>`;
      }
      const count = k === "participants" ? participants().length : items.length;
      return `<div class="sec" data-sec="${k}">
        <div class="sec-head"><input type="text" class="sec-title" data-title="${k}" data-focus="title-${k}" value="${esc(secTitle(k))}" aria-label="${esc(t("secTitle"))}"><span class="count">${count}</span></div>
        ${body}</div>`;
    }).join("");
    if (focused) { const el = box.querySelector(`[data-focus="${focused}"]`); if (el) { el.focus(); if (el.setSelectionRange && el.value) el.setSelectionRange(el.value.length, el.value.length); } }
  }
  const rows = (v) => Math.min(6, Math.max(2, Math.ceil(String(v || "").length / 38)));
  function itemHtml(k, it, i, n) {
    const src = it.ts || it.speaker ? `<span class="src">${esc([it.ts, it.speaker].filter(Boolean).join(" · "))}</span>` : "";
    const main = k === "actions"
      ? `<div class="act">
          <textarea rows="${rows(it.what)}" data-field="what" data-focus="${it.id}-what" aria-label="${esc(t("what"))}">${esc(it.what)}</textarea>
          <label>${esc(t("who"))}<input type="text" list="names" data-field="who" data-focus="${it.id}-who" value="${esc(it.who)}"></label>
          <label>${esc(t("when"))}<input type="text" data-field="when" data-focus="${it.id}-when" value="${esc(it.when)}"></label>
        </div>${src}`
      : `<textarea rows="${rows(it.text)}" data-field="text" data-focus="${it.id}-text" aria-label="${esc(t("itemText"))}">${esc(it.text)}</textarea>${src}`;
    return `<li class="item" draggable="true" data-item="${it.id}" data-sec="${k}">
      <span class="grip" aria-hidden="true">⋮⋮</span>
      <div>${main}</div>
      <div class="ibtns">
        <button type="button" data-move="-1" aria-label="${esc(t("up"))}" title="${esc(t("up"))}" ${i === 0 ? "disabled" : ""}>↑</button>
        <button type="button" data-move="1" aria-label="${esc(t("down"))}" title="${esc(t("down"))}" ${i === n - 1 ? "disabled" : ""}>↓</button>
        <button type="button" data-remove aria-label="${esc(t("remove"))}" title="${esc(t("remove"))}">✕</button>
      </div></li>`;
  }
  function findItem(id) {
    for (const k of SECS) { const i = S.sections[k].findIndex((x) => x.id === id); if (i >= 0) return { k, i }; }
    return null;
  }

  // ------------------------------------------------------------------ output model
  function fmtDate(iso) {
    if (!iso) return "";
    const d = new Date(iso + "T12:00:00");
    if (isNaN(d)) return iso;
    return d.toLocaleDateString(O[outL()].locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  }
  function model() {
    const L = O[outL()], m = S.meta;
    const note = (it) => (S.incSrc && (it.ts || it.speaker) ? `(${[it.ts, it.speaker].filter(Boolean).join(", ")})` : "");
    const sections = [];
    const ps = participants();
    if (ps.length) sections.push({ key: "participants", title: secTitle("participants"), kind: "list", items: ps.map((p) => ({ text: p, note: "" })) });
    for (const k of ["agenda", "discussion", "decisions"]) {
      const items = S.sections[k].filter((it) => it.text.trim()).map((it) => ({ text: it.text.trim(), note: note(it) }));
      if (items.length) sections.push({ key: k, title: secTitle(k), kind: k === "agenda" ? "olist" : "list", items });
    }
    const acts = S.sections.actions.filter((it) => (it.what + it.who + it.when).trim()).map((it) => ({ what: it.what.trim(), who: it.who.trim(), when: it.when.trim(), note: note(it) }));
    if (acts.length) sections.push({ key: "actions", title: secTitle("actions"), kind: "actions", items: acts, head: [L.no, L.what, L.who, L.when] });
    const docType = L[m.type] || L.mom;
    return {
      kicker: m.title.trim() ? docType : "", title: m.title.trim() || docType, author: m.prepared.trim(),
      meta: [[L.date, fmtDate(m.date)], [L.client, m.client.trim()], [L.location, m.location.trim()], [L.prepared, m.prepared.trim()]],
      sections, closing: m.closing.trim(),
    };
  }
  const hasContent = () => S.transcript.trim() || SECS.some((k) => S.sections[k].length) || S.meta.title.trim();

  function toHtml(M, forClipboard) {
    const cs = forClipboard ? { th: ' style="border:1px solid #a6a6a6;padding:4px 8px;background:#e7e6e2;text-align:left"', td: ' style="border:1px solid #a6a6a6;padding:4px 8px;vertical-align:top"', tb: ' style="border-collapse:collapse"', note: ' style="color:#6b6b6b;font-style:italic"' } : { th: "", td: "", tb: "", note: ' class="note"' };
    const nt = (n) => (n ? ` <span${cs.note}>${esc(n)}</span>` : "");
    let h = (M.kicker ? `<p class="kicker">${esc(M.kicker)}</p>` : "") + `<h1>${esc(M.title)}</h1>`;
    h += M.meta.filter(([, v]) => v).map(([l, v]) => `<p class="m"><b>${esc(l)}:</b> ${esc(v)}</p>`).join("");
    for (const s of M.sections) {
      h += `<h2>${esc(s.title)}</h2>`;
      if (s.kind === "actions") {
        h += `<table${cs.tb}><thead><tr>${s.head.map((x) => `<th${cs.th}>${esc(x)}</th>`).join("")}</tr></thead><tbody>` +
          s.items.map((it, i) => `<tr><td${cs.td}>${i + 1}</td><td${cs.td}>${esc(it.what)}${nt(it.note)}</td><td${cs.td}>${esc(it.who)}</td><td${cs.td}>${esc(it.when)}</td></tr>`).join("") + "</tbody></table>";
      } else {
        const tag = s.kind === "olist" ? "ol" : "ul";
        h += `<${tag}>` + s.items.map((it) => `<li>${esc(it.text)}${nt(it.note)}</li>`).join("") + `</${tag}>`;
      }
    }
    if (M.closing) h += `<p class="closing"><i>${esc(M.closing)}</i></p>`;
    return h;
  }
  function toMarkdown(M) {
    const mdEsc = (s) => String(s).replace(/([\\`*_[\]#|<>])/g, "\\$1");
    const cell = (s) => String(s).replace(/\|/g, "\\|").replace(/\n+/g, " ");
    const nt = (n) => (n ? ` _${mdEsc(n)}_` : "");
    let md = (M.kicker ? `_${mdEsc(M.kicker)}_\n\n` : "") + `# ${mdEsc(M.title)}\n\n`;
    md += M.meta.filter(([, v]) => v).map(([l, v]) => `**${mdEsc(l)}:** ${mdEsc(v)}  `).join("\n") + "\n";
    for (const s of M.sections) {
      md += `\n## ${mdEsc(s.title)}\n\n`;
      if (s.kind === "actions") {
        md += `| ${s.head.map(cell).join(" | ")} |\n| --- | --- | --- | --- |\n`;
        md += s.items.map((it, i) => `| ${i + 1} | ${cell(it.what)}${it.note ? " _" + cell(it.note) + "_" : ""} | ${cell(it.who)} | ${cell(it.when)} |`).join("\n") + "\n";
      } else {
        md += s.items.map((it, i) => `${s.kind === "olist" ? i + 1 + "." : "-"} ${mdEsc(it.text).replace(/\n/g, "\n   ")}${nt(it.note)}`).join("\n") + "\n";
      }
    }
    if (M.closing) md += `\n_${mdEsc(M.closing)}_\n`;
    return md;
  }
  function toPlain(M) {
    let s = (M.kicker ? M.kicker.toUpperCase() + "\n" : "") + M.title + "\n\n";
    s += M.meta.filter(([, v]) => v).map(([l, v]) => `${l}: ${v}`).join("\n") + "\n";
    for (const sec of M.sections) {
      s += `\n${sec.title.toUpperCase()}\n`;
      if (sec.kind === "actions") {
        s += sec.items.map((it, i) => `${i + 1}. ${it.what}${it.note ? " " + it.note : ""}\n   ${sec.head[2]}: ${it.who || "-"} | ${sec.head[3]}: ${it.when || "-"}`).join("\n") + "\n";
      } else {
        s += sec.items.map((it, i) => `${sec.kind === "olist" ? i + 1 + "." : "-"} ${it.text}${it.note ? " " + it.note : ""}`).join("\n") + "\n";
      }
    }
    if (M.closing) s += `\n${M.closing}\n`;
    return s;
  }
  function renderPreview() {
    const M = model();
    const empty = !M.sections.length && !S.meta.title.trim();
    $("#preview").innerHTML = toHtml(M, false) + (empty ? `<p class="placeholder">${esc(t("emptyDoc"))}</p>` : "");
  }
  let pvTimer;
  function changed() {
    dirty = true;
    clearTimeout(pvTimer);
    pvTimer = setTimeout(renderPreview, 120);
  }

  // ------------------------------------------------------------------ export
  function fileBase() {
    const slug = (S.meta.title || O[outL()][S.meta.type]).toLowerCase().normalize("NFKD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60);
    return [S.meta.date, slug || "minutes"].filter(Boolean).join("-");
  }
  function download(name, blob) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
    status("#outStatus", t("downloaded")(name));
  }
  function status(sel, msg) {
    const el = $(sel);
    el.textContent = msg;
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.textContent = ""; }, 6000);
  }
  async function copy() {
    const M = model();
    const plain = toPlain(M), html = toHtml(M, true);
    try {
      if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {
        await navigator.clipboard.write([new ClipboardItem({ "text/plain": new Blob([plain], { type: "text/plain" }), "text/html": new Blob([html], { type: "text/html" }) })]);
      } else await navigator.clipboard.writeText(plain);
      status("#outStatus", t("copied"));
    } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = plain; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      let ok = false;
      try { ok = document.execCommand("copy"); } catch (_) { ok = false; }
      ta.remove();
      status("#outStatus", ok ? t("copied") : t("copyFail"));
    }
  }

  // ------------------------------------------------------------------ draft (only on request)
  function storage() { try { return window.localStorage; } catch (e) { return null; } }
  function readDraft() { try { const s = storage(); return s ? JSON.parse(s.getItem(DRAFT_KEY) || "null") : null; } catch (e) { return null; } }
  function draftInfo() {
    const d = readDraft();
    $("#loadDraft").hidden = !d;
    if (d && !$("#draftStatus").textContent) $("#draftStatus").textContent = t("draftExists")(new Date(d.savedAt).toLocaleString(ui === "id" ? "id-ID" : "en-GB"));
  }
  function saveDraft() {
    const s = storage();
    try {
      if (!s) throw new Error("no storage");
      const savedAt = new Date().toISOString();
      s.setItem(DRAFT_KEY, JSON.stringify({ v: 1, savedAt, state: S }));
      dirty = false;
      $("#loadDraft").hidden = false;
      status("#draftStatus", t("saved")(new Date(savedAt).toLocaleTimeString(ui === "id" ? "id-ID" : "en-GB", { hour: "2-digit", minute: "2-digit" })));
    } catch (e) { status("#draftStatus", t("noStorage")); }
  }
  function loadState(st) {
    S = Object.assign(blank(), st);
    S.meta = Object.assign(blank().meta, st.meta || {});
    S.sections = Object.assign(blank().sections, st.sections || {});
    fillForm(); reparse(); renderPreview();
  }
  function fillForm() {
    $("#transcript").value = S.transcript;
    for (const [k, id] of Object.entries(FIELDS)) $(id).value = S.meta[k] || "";
    $("#incSrc").checked = !!S.incSrc;
    $("#outLang").value = outL();
  }

  // ------------------------------------------------------------------ events
  const FIELDS = { title: "#m-title", date: "#m-date", type: "#m-type", client: "#m-client", location: "#m-location", participants: "#m-participants", prepared: "#m-prepared", closing: "#m-closing" };
  for (const [k, id] of Object.entries(FIELDS)) {
    $(id).addEventListener("input", (e) => {
      S.meta[k] = e.target.value;
      changed();
      if (k === "participants") partTimer();
    });
  }
  let pTimer;
  function partTimer() { clearTimeout(pTimer); pTimer = setTimeout(() => { cands = MinutesParse.extract(parsed.segments, participants().map(stripRole)); renderCands(); renderNames(); renderSections(); }, 400); }
  $("#m-type").addEventListener("change", (e) => { S.meta.type = e.target.value; changed(); });

  let tTimer;
  $("#transcript").addEventListener("input", (e) => { S.transcript = e.target.value; changed(); clearTimeout(tTimer); tTimer = setTimeout(reparse, 350); });

  function readFile(f) {
    if (!f) return;
    const r = new FileReader();
    r.onload = () => { S.transcript = String(r.result || ""); $("#transcript").value = S.transcript; changed(); reparse(); status("#outStatus", t("fileRead")(f.name)); };
    r.onerror = () => status("#outStatus", t("fileErr"));
    r.readAsText(f);
  }
  $("#file").addEventListener("change", (e) => { readFile(e.target.files[0]); e.target.value = ""; });
  const ta = $("#transcript");
  ta.addEventListener("dragover", (e) => { if (e.dataTransfer && [...e.dataTransfer.types].includes("Files")) { e.preventDefault(); ta.classList.add("dropping"); } });
  ta.addEventListener("dragleave", () => ta.classList.remove("dropping"));
  ta.addEventListener("drop", (e) => { if (e.dataTransfer.files.length) { e.preventDefault(); ta.classList.remove("dropping"); readFile(e.dataTransfer.files[0]); } });

  $("#sample").addEventListener("change", (e) => {
    const smp = MinutesSamples[e.target.value];
    e.target.value = "";
    if (!smp) return;
    if (hasContent() && !confirm(t("confirmSample"))) return;
    const keep = { outLang: S.outLang, incSrc: S.incSrc };
    S = Object.assign(blank(), keep);
    S.transcript = smp.text;
    Object.assign(S.meta, smp.meta);
    fillForm(); changed(); reparse();
  });

  $$("[data-ui-lang]").forEach((b) => b.addEventListener("click", () => {
    ui = b.dataset.uiLang;
    const u = new URL(location.href); u.searchParams.set("lang", ui); history.replaceState(null, "", u);
    applyUi();
  }));
  $("#outLang").addEventListener("change", (e) => { S.outLang = e.target.value; changed(); renderSections(); renderCands(); renderPreview(); });
  $("#incSrc").addEventListener("change", (e) => { S.incSrc = e.target.checked; changed(); });
  $("#resetTitles").addEventListener("click", () => { S.titles = {}; changed(); renderSections(); renderCands(); });
  $("#closingDefault").addEventListener("click", () => { S.meta.closing = O[outL()].closing; $("#m-closing").value = S.meta.closing; changed(); });
  $("#showAll").addEventListener("change", (e) => { showAll = e.target.checked; if (showAll) filter = "all"; renderFilters(); renderCands(); });
  $("#filters").addEventListener("click", (e) => { const b = e.target.closest("[data-filter]"); if (!b) return; filter = b.dataset.filter; renderFilters(); renderCands(); });

  $("#cands").addEventListener("click", (e) => {
    const b = e.target.closest("[data-add]"); if (!b) return;
    const c = cands.find((x) => x.id === b.closest(".cand").dataset.id);
    if (c) addFromCand(c, b.dataset.add);
  });

  const secs = $("#sections");
  secs.addEventListener("input", (e) => {
    const el = e.target;
    if (el.dataset.title) { S.titles[el.dataset.title] = el.value; changed(); return; }
    const li = el.closest("[data-item]"); if (!li || !el.dataset.field) return;
    const f = findItem(li.dataset.item); if (!f) return;
    S.sections[f.k][f.i][el.dataset.field] = el.value;
    changed();
  });
  secs.addEventListener("change", (e) => { if (e.target.dataset.title) renderCands(); });
  secs.addEventListener("click", (e) => {
    const sp = e.target.closest("[data-speaker]");
    if (sp) { addFromCand({ speaker: sp.dataset.speaker }, "participants"); return; }
    const nw = e.target.closest("[data-new]");
    if (nw) {
      const k = nw.dataset.new, id = nid();
      S.sections[k].push(k === "actions" ? { id, what: "", who: "", when: "", ts: "", speaker: "" } : { id, text: "", ts: "", speaker: "" });
      changed(); renderSections();
      const f = secs.querySelector(`[data-item="${id}"] textarea`); if (f) f.focus();
      return;
    }
    const li = e.target.closest("[data-item]"); if (!li) return;
    const f = findItem(li.dataset.item); if (!f) return;
    const arr = S.sections[f.k];
    const mv = e.target.closest("[data-move]");
    if (mv) {
      const j = f.i + Number(mv.dataset.move);
      if (j < 0 || j >= arr.length) return;
      [arr[f.i], arr[j]] = [arr[j], arr[f.i]];
      changed(); renderSections();
      const btn = secs.querySelector(`[data-item="${li.dataset.item}"] [data-move="${mv.dataset.move}"]`);
      (btn && !btn.disabled ? btn : secs.querySelector(`[data-item="${li.dataset.item}"] textarea`)).focus();
    } else if (e.target.closest("[data-remove]")) {
      arr.splice(f.i, 1);
      changed(); renderSections(); renderCands();
    }
  });

  // drag and drop: suggestions into sections, and items between and within sections
  let drag = null;
  document.addEventListener("dragstart", (e) => {
    const c = e.target.closest && e.target.closest(".cand");
    const it = e.target.closest && e.target.closest(".item");
    if (it && /TEXTAREA|INPUT/.test(document.activeElement && document.activeElement.tagName) && it.contains(document.activeElement)) { e.preventDefault(); return; }
    if (c) drag = { type: "cand", id: c.dataset.id };
    else if (it) { drag = { type: "item", id: it.dataset.item }; it.classList.add("dragging"); }
    else return;
    e.dataTransfer.effectAllowed = "copyMove";
    e.dataTransfer.setData("text/plain", drag.id);
  });
  document.addEventListener("dragend", () => { drag = null; $$(".dragging,.over").forEach((x) => x.classList.remove("dragging", "over")); });
  secs.addEventListener("dragover", (e) => {
    if (!drag) return;
    const sec = e.target.closest(".sec"); if (!sec || sec.dataset.sec === "participants" && drag.type === "item") return;
    e.preventDefault();
    $$(".sec.over").forEach((x) => x !== sec && x.classList.remove("over"));
    sec.classList.add("over");
  });
  secs.addEventListener("dragleave", (e) => { const sec = e.target.closest(".sec"); if (sec && !sec.contains(e.relatedTarget)) sec.classList.remove("over"); });
  secs.addEventListener("drop", (e) => {
    if (!drag) return;
    const sec = e.target.closest(".sec"); if (!sec) return;
    e.preventDefault();
    const k = sec.dataset.sec;
    const before = e.target.closest("[data-item]");
    if (drag.type === "cand") {
      const c = cands.find((x) => x.id === drag.id);
      if (c) addFromCand(c, k, before && before.dataset.item);
    } else {
      const f = findItem(drag.id); if (!f || k === "participants") return;
      const [it] = S.sections[f.k].splice(f.i, 1);
      let moved = it;
      if (f.k !== k) { // convert between plain items and action rows
        moved = k === "actions" ? { id: it.id, from: it.from, ts: it.ts, speaker: it.speaker, what: it.text || "", who: "", when: "" }
          : { id: it.id, from: it.from, ts: it.ts, speaker: it.speaker, text: f.k === "actions" ? [it.what, it.who, it.when].filter(Boolean).join(" — ") : it.text };
      }
      const arr = S.sections[k];
      const j = before ? arr.findIndex((x) => x.id === before.dataset.item) : -1;
      j >= 0 ? arr.splice(j, 0, moved) : arr.push(moved);
      changed(); renderSections(); renderCands();
    }
    drag = null;
  });

  $("#copy").addEventListener("click", copy);
  $("#dlMd").addEventListener("click", () => download(fileBase() + ".md", new Blob([toMarkdown(model())], { type: "text/markdown;charset=utf-8" })));
  $("#dlDocx").addEventListener("click", () => download(fileBase() + ".docx", new Blob([MinutesDocx.build(model())], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" })));
  $("#saveDraft").addEventListener("click", saveDraft);
  $("#loadDraft").addEventListener("click", () => { const d = readDraft(); if (d && d.state) { loadState(d.state); dirty = false; status("#draftStatus", t("restored")); } });
  $("#clearAll").addEventListener("click", () => {
    if (!confirm(t("confirmClear"))) return;
    const s = storage(); try { s && s.removeItem(DRAFT_KEY); } catch (e) { /* ignore */ }
    S = blank(); filter = "all"; showAll = false; $("#showAll").checked = false;
    fillForm(); reparse(); renderPreview(); draftInfo();
    dirty = false;
    status("#draftStatus", t("cleared"));
  });
  window.addEventListener("beforeunload", (e) => { if (dirty && hasContent()) { e.preventDefault(); e.returnValue = t("leave"); } });

  // for automated tests only: read the current output without touching the clipboard or downloads
  window.__minutes = { model, toMarkdown, toPlain, toHtml, state: () => S };

  fillForm();
  reparse();
  applyUi();
})();
