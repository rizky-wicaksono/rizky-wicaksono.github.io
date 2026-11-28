/* Minimal .docx writer, made for this page. No library and no network.
   A .docx file is a ZIP archive of a few XML files. This file builds those XML files from a simple model
   and packs them with a tiny ZIP writer (STORE method, no compression), so everything happens in the browser.

   MinutesDocx.build(model) -> Uint8Array
   model = { kicker, title, meta: [[label, value]], sections: [{ title, kind: "list" | "olist" | "actions",
             items: [{ text, note }] or [{ who, what, when, note }], head: [no, what, who, when] }], closing } */
(function () {
  "use strict";

  // ---------- ZIP (store only) ----------
  const CRC_TABLE = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(bytes) {
    let c = 0xffffffff;
    for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  }

  function dosTime(d) {
    const time = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
    const date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    return { time, date };
  }

  function zip(files) {
    const enc = new TextEncoder();
    const now = dosTime(new Date());
    const chunks = [];
    const central = [];
    let offset = 0;
    for (const f of files) {
      const name = enc.encode(f.name);
      const data = typeof f.data === "string" ? enc.encode(f.data) : f.data;
      const crc = crc32(data);
      const local = new DataView(new ArrayBuffer(30));
      local.setUint32(0, 0x04034b50, true);
      local.setUint16(4, 20, true);         // version needed
      local.setUint16(6, 0x0800, true);     // flags: UTF-8 names
      local.setUint16(8, 0, true);          // method: store
      local.setUint16(10, now.time, true);
      local.setUint16(12, now.date, true);
      local.setUint32(14, crc, true);
      local.setUint32(18, data.length, true);
      local.setUint32(22, data.length, true);
      local.setUint16(26, name.length, true);
      local.setUint16(28, 0, true);
      chunks.push(new Uint8Array(local.buffer), name, data);

      const cen = new DataView(new ArrayBuffer(46));
      cen.setUint32(0, 0x02014b50, true);
      cen.setUint16(4, 20, true);           // version made by
      cen.setUint16(6, 20, true);
      cen.setUint16(8, 0x0800, true);
      cen.setUint16(10, 0, true);
      cen.setUint16(12, now.time, true);
      cen.setUint16(14, now.date, true);
      cen.setUint32(16, crc, true);
      cen.setUint32(20, data.length, true);
      cen.setUint32(24, data.length, true);
      cen.setUint16(28, name.length, true);
      cen.setUint16(30, 0, true);
      cen.setUint16(32, 0, true);
      cen.setUint16(34, 0, true);
      cen.setUint16(36, 0, true);
      cen.setUint32(38, 0, true);
      cen.setUint32(42, offset, true);
      central.push(new Uint8Array(cen.buffer), name);
      offset += 30 + name.length + data.length;
    }
    const cenSize = central.reduce((n, c) => n + c.length, 0);
    const end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true);
    end.setUint16(8, files.length, true);
    end.setUint16(10, files.length, true);
    end.setUint32(12, cenSize, true);
    end.setUint32(16, offset, true);
    const all = chunks.concat(central, [new Uint8Array(end.buffer)]);
    const out = new Uint8Array(all.reduce((n, c) => n + c.length, 0));
    let p = 0;
    for (const c of all) { out.set(c, p); p += c.length; }
    return out;
  }

  // ---------- WordprocessingML ----------
  function x(s) {
    return String(s == null ? "" : s)
      .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F￾￿]/g, "")
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function run(text, o = {}) {
    const rp = [];
    if (o.bold) rp.push("<w:b/>");
    if (o.italic) rp.push("<w:i/>");
    if (o.color) rp.push(`<w:color w:val="${o.color}"/>`);
    if (o.size) rp.push(`<w:sz w:val="${o.size}"/><w:szCs w:val="${o.size}"/>`);
    const parts = String(text == null ? "" : text).split("\n");
    const body = parts.map((t, i) => (i ? "<w:br/>" : "") + `<w:t xml:space="preserve">${x(t)}</w:t>`).join("");
    return `<w:r>${rp.length ? `<w:rPr>${rp.join("")}</w:rPr>` : ""}${body}</w:r>`;
  }

  function para(runs, o = {}) {
    const pp = [];
    if (o.style) pp.push(`<w:pStyle w:val="${o.style}"/>`);
    if (o.keepNext) pp.push("<w:keepNext/>");
    if (o.after != null) pp.push(`<w:spacing w:after="${o.after}"/>`);
    if (o.indent) pp.push(`<w:ind w:left="${o.indent}" w:hanging="${o.hanging || 0}"/>`);
    return `<w:p>${pp.length ? `<w:pPr>${pp.join("")}</w:pPr>` : ""}${runs}</w:p>`;
  }

  const NOTE = { italic: true, color: "6B6B6B", size: 18 };

  function cell(content, width, o = {}) {
    const tc = [`<w:tcW w:w="${width}" w:type="dxa"/>`];
    if (o.shade) tc.push(`<w:shd w:val="clear" w:color="auto" w:fill="${o.shade}"/>`);
    return `<w:tc><w:tcPr>${tc.join("")}</w:tcPr>${content}</w:tc>`;
  }

  function actionsTable(sec) {
    const W = [700, 4626, 1900, 1800];
    const border = '<w:top w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/>';
    let t = `<w:tbl><w:tblPr><w:tblW w:w="${W.reduce((a, b) => a + b, 0)}" w:type="dxa"/><w:tblBorders>${border}</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>`;
    t += `<w:tblGrid>${W.map((w) => `<w:gridCol w:w="${w}"/>`).join("")}</w:tblGrid>`;
    t += '<w:tr><w:trPr><w:tblHeader/></w:trPr>' + sec.head.map((h, i) => cell(para(run(h, { bold: true }), { after: 0 }), W[i], { shade: "E7E6E2" })).join("") + "</w:tr>";
    sec.items.forEach((it, i) => {
      const what = para(run(it.what || "")  + (it.note ? run(" " + it.note, NOTE) : ""), { after: 0 });
      t += "<w:tr>" + [
        cell(para(run(String(i + 1)), { after: 0 }), W[0]),
        cell(what, W[1]),
        cell(para(run(it.who || ""), { after: 0 }), W[2]),
        cell(para(run(it.when || ""), { after: 0 }), W[3]),
      ].join("") + "</w:tr>";
    });
    return t + "</w:tbl>" + para("", { after: 0 });
  }

  function documentXml(m) {
    const b = [];
    if (m.kicker) b.push(para(run(m.kicker, { bold: true, color: "14307A", size: 20 }), { style: "Kicker" }));
    b.push(para(run(m.title), { style: "Title" }));
    for (const [label, value] of m.meta) {
      if (value) b.push(para(run(label + ": ", { bold: true }) + run(value), { after: 40 }));
    }
    for (const sec of m.sections) {
      b.push(para(run(sec.title), { style: "Heading1", keepNext: true }));
      if (sec.kind === "actions") { b.push(actionsTable(sec)); continue; }
      sec.items.forEach((it, i) => {
        const mark = sec.kind === "olist" ? `${i + 1}.` : "•";
        b.push(para(run(mark + "\t") + run(it.text) + (it.note ? run(" " + it.note, NOTE) : ""), { style: "ListPara", indent: 360, hanging: 360 }));
      });
    }
    if (m.closing) b.push(para(run(m.closing, { italic: true }), { style: "Closing" }));
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
      '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">' +
      "<w:body>" + b.join("") +
      '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1300" w:right="1300" w:bottom="1300" w:left="1300" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>' +
      "</w:body></w:document>";
  }

  const STYLES = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial" w:cs="Arial"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault>' +
    '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>' +
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>' +
    '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr></w:style>' +
    '<w:style w:type="paragraph" w:styleId="Kicker"><w:name w:val="Kicker"/><w:basedOn w:val="Normal"/><w:next w:val="Title"/><w:pPr><w:spacing w:after="40"/></w:pPr><w:rPr><w:caps/></w:rPr></w:style>' +
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="320" w:after="120"/><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="0A0A0A"/></w:pBdr><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>' +
    '<w:style w:type="paragraph" w:styleId="ListPara"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="80"/><w:tabs><w:tab w:val="left" w:pos="360"/></w:tabs></w:pPr></w:style>' +
    '<w:style w:type="paragraph" w:styleId="Closing"><w:name w:val="Closing"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="360"/></w:pPr><w:rPr><w:color w:val="404040"/></w:rPr></w:style>' +
    "</w:styles>";

  function build(m) {
    const now = new Date().toISOString().replace(/\.\d+Z$/, "Z");
    const files = [
      { name: "[Content_Types].xml", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>' },
      { name: "_rels/.rels", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>' },
      { name: "docProps/core.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${x(m.title)}</dc:title><dc:creator>${x(m.author || "")}</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">${now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">${now}</dcterms:modified></cp:coreProperties>` },
      { name: "word/_rels/document.xml.rels", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>' },
      { name: "word/styles.xml", data: STYLES },
      { name: "word/document.xml", data: documentXml(m) },
    ];
    return zip(files);
  }

  window.MinutesDocx = { build, zip, crc32 };
})();
