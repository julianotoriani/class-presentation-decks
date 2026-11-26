// pptxgenjs helpers for class decks, with the known bugs worked around.
//
// Usage (in build.js, next to this file):
//   const pptxgen = require("pptxgenjs");
//   const { PALETTE, makeHelpers, dropExtraParaProps } = require("./deck_helpers");
//   const pres = new pptxgen();
//   pres.layout = "LAYOUT_16x9";                       // 10 x 5.625 in
//   const h = makeHelpers(pres, { font: "Roboto", lang: "pt-BR" });
//   const s = h.contentSlide("Título do slide", "notas do apresentador");
//   h.bullets(s, ["um item", [{ text: "item com " }, { text: "trecho vermelho", options: { color: PALETTE.RED } }]],
//             { x: 0.5, y: 1.0, w: 9, h: 2 });
//   pres.writeFile({ fileName: OUT }).then(() => dropExtraParaProps(OUT));
//
// What it fixes (see references/pptx-build.md):
//   - table cell margins are inches, not points
//   - multi-run bullet items lose their bullet in LibreOffice (dropExtraParaProps)
//   - hyphens and spaces that break inside "pré-treinada", "1 e 1", "± 0,021"
//   - lang en-US on every run (Portuguese spell-checked as English), including table cells
const fs = require("fs");

// Projector-safe palette: no green, pale tints only behind dark text.
const PALETTE = {
  INK: "1B2430", MUTED: "5B6573", LINE: "C9D0D8",
  BLUE: "1E40AF", BLUE_BG: "DBEAFE",
  RED: "B91C1C", RED_BG: "FBEAE8",
  GRAY: "8A94A3", GRAY_BG: "F1F4F6", DARK: "13202B",
};

// Non-breaking hyphen inside the listed prefixes, non-breaking spaces around ×, →, ± and in "1 e 1".
// Extend NB_PREFIXES with the hyphenated words of your deck.
const NB_PREFIXES = ["pré", "Pré", "pós", "Pós", "auto", "anti", "semi", "ViT", "ML", "ICP"];
const NB_PREFIX_RE = new RegExp(`\\b(${NB_PREFIXES.join("|")})-`, "g");
function nb(t) {
  if (typeof t !== "string") return t;
  return t
    .replace(NB_PREFIX_RE, "$1‑")
    .replace(/ ([×→±=]) (?=\S)/g, " $1 ")
    .replace(/(\d) e (?=[−-]?\d)/g, "$1 e ");
}

function makeHelpers(pres, { font = "Roboto", lang = "pt-BR", titleSize = 24, masterName = "CONTEUDO" } = {}) {
  const P = PALETTE;

  pres.theme = { headFontFace: font, bodyFontFace: font };
  pres.defineSlideMaster({
    title: masterName,
    background: { color: "FFFFFF" },
    objects: [{
      placeholder: {
        options: {
          name: "title", type: "title", x: 0.5, y: 0.28, w: 9.0, h: 0.6,
          fontFace: font, fontSize: titleSize, bold: true, color: P.INK, align: "left", valign: "middle", margin: 0,
        },
        text: "",
      },
    }],
    slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.25, fontFace: font, fontSize: 10, color: P.MUTED, align: "right" },
  });

  function contentSlide(title, notes) {
    const s = pres.addSlide({ masterName });
    s.addText(title, { placeholder: "title", lang });
    if (notes) s.addNotes(notes);
    return s;
  }

  // t: string, or [{text, options}] runs (each run gets nb()).
  function text(slide, t, o = {}) {
    const body = Array.isArray(t) ? t.map((r) => ({ ...r, text: nb(r.text) })) : nb(t);
    slide.addText(body, { fontFace: font, lang, color: P.INK, margin: 0, valign: "top", isTextBox: true, ...o });
  }

  // items: strings, or arrays of runs for an item with colored parts. The bullet goes on the first run only;
  // call dropExtraParaProps() on the saved file so LibreOffice keeps it.
  function bullets(slide, items, o = {}) {
    const runs = [];
    items.forEach((item, i) => {
      const parts = Array.isArray(item) ? item : [{ text: item }];
      parts.forEach((p, k) => {
        const opt = { ...(p.options || {}) };
        if (k === 0) opt.bullet = { indent: 14 };
        if (k === parts.length - 1 && i < items.length - 1) opt.breakLine = true;
        runs.push({ text: nb(p.text), options: opt });
      });
    });
    slide.addText(runs, {
      fontFace: font, lang, fontSize: 16, color: P.INK, valign: "top", margin: 0,
      paraSpaceAfter: 8, isTextBox: true, ...o,
    });
  }

  function source(slide, t) {
    text(slide, t, { x: 0.5, y: 5.2, w: 8.4, h: 0.25, fontSize: 9, color: P.MUTED, valign: "middle" });
  }

  function rect(slide, o) {
    const fill = o.fill || P.GRAY_BG;
    slide.addShape(pres.shapes.RECTANGLE, { line: { color: fill, width: 0 }, ...o, fill: { color: fill } });
  }

  function arrow(slide, x1, y1, x2, y2, color = P.MUTED, width = 1.5) {
    slide.addShape(pres.shapes.LINE, {
      x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
      flipH: x2 < x1, flipV: y2 < y1, line: { color, width, endArrowType: "triangle" },
    });
  }

  // Image with explicit size (compute h from the figure's figsize so nothing stretches).
  function img(slide, file, x, y, w, h) {
    slide.addImage({ path: file, x, y, w, h });
  }

  // Photo thumbnail with an optional colored border drawn as a separate unfilled rectangle.
  function photo(slide, file, x, y, w, { border = null, borderWidth = 2, ratio = 4 / 3 } = {}) {
    const h = w * ratio;
    slide.addImage({ path: file, x, y, w, h });
    if (border) {
      slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { type: "none" }, line: { color: border, width: borderWidth } });
    }
    return h;
  }

  // Numbered step card with a figure: used for pipelines and experiments (4 cards of w=2.1 fit 10" with 0.2 gaps).
  function stepCard(slide, { x, y = 1.0, w = 2.1, h = 3.45, n, title, body, foot, color = P.BLUE, fig, arrowAfter = true }) {
    rect(slide, { x, y, w, h, fill: P.GRAY_BG });
    text(slide, String(n), { x: x + 0.14, y: y + 0.1, w: 0.35, h: 0.42, fontSize: 22, bold: true, color, valign: "middle" });
    text(slide, title, { x: x + 0.48, y: y + 0.1, w: w - 0.6, h: 0.42, fontSize: 16, bold: true, valign: "middle" });
    if (fig) img(slide, fig, x + 0.12, y + 0.6, w - 0.24, (w - 0.24) * 1.0 / 1.86);
    text(slide, body, { x: x + 0.14, y: y + 1.72, w: w - 0.28, h: 1.15, fontSize: 13 });
    if (foot) text(slide, foot, { x: x + 0.14, y: y + 2.88, w: w - 0.28, h: 0.5, fontSize: 12.5, bold: true, color });
    if (arrowAfter) arrow(slide, x + w + 0.02, y + 1.1, x + w + 0.18, y + 1.1, P.INK, 1.75);
  }

  // rows[0] is the header. o: {x, y, w, colW, left (number of left-aligned columns), highlight (body row indexes), rowH, fontSize}
  function table(slide, rows, o) {
    const left = o.left ?? 1;
    const hl = o.highlight || [];
    const head = rows[0].map((t, k) => ({
      text: t, options: { lang, bold: true, color: "FFFFFF", fill: { color: P.INK }, align: k < left ? "left" : "right" },
    }));
    const body = rows.slice(1).map((r, ri) => r.map((t, k) => ({
      text: t,
      options: {
        lang, align: k < left ? "left" : "right",
        fill: { color: hl.includes(ri) ? P.BLUE_BG : "FFFFFF" }, bold: hl.includes(ri) && k >= left,
      },
    })));
    slide.addTable([head, ...body], {
      x: o.x, y: o.y, w: o.w, colW: o.colW, rowH: o.rowH || 0.3,
      fontFace: font, lang, fontSize: o.fontSize || 11, color: P.INK, valign: "middle",
      margin: [0, 0.08, 0, 0.08],                       // INCHES since pptxgenjs 3.8, not points
      border: { type: "solid", pt: 0.75, color: P.LINE },
    });
  }

  return { contentSlide, text, bullets, source, rect, arrow, img, photo, stepCard, table, nb };
}

// pptxgenjs writes one <a:pPr> per run; LibreOffice applies the last one, so a bullet item with a colored
// second run loses its bullet. Keep only the first <a:pPr> of each paragraph. Call after writeFile().
async function dropExtraParaProps(file) {
  const JSZip = require("jszip");                     // installed with pptxgenjs
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    const xml = await zip.file(name).async("string");
    zip.file(name, xml.replace(/(<\/a:r>)<a:pPr\b[^>]*?(?:\/>|>.*?<\/a:pPr>)/g, "$1"));
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

module.exports = { PALETTE, nb, makeHelpers, dropExtraParaProps };
