# Building the .pptx: pipeline and the bugs that cost hours

## Contents
1. Layout of a deck project
2. Pitfalls (symptom → fix)
3. Rendering and looking at every slide
4. Rebuilding an exported deck in frozen mode
5. Delivering

## 1. Layout of a deck project

```
deck/
├── build.sh            # one command: figures → pptx → validate → render
├── build/
│   ├── figures.py      # matplotlib; reads data, asserts numbers, writes fig/*.png + fig/meta.json
│   ├── build.js        # pptxgenjs; requires deck_helpers.js; writes ../deck.pptx
│   ├── fig/            # generated
│   └── render/         # generated: deck.pdf, slide-NN.jpg, contact-N.jpg
└── deck.pptx, deck.pdf
```

`build.sh` sketch:

```bash
set -euo pipefail
cd "$(dirname "$0")/build"
python -I figures.py "$DATA_DIR" "$RESULTS_DIR"
node build.js
zip -dq ../deck.pptx "*/" || true          # drop ZIP folder entries (see pitfall 8)
bash "$SKILL/scripts/render.sh" ../deck.pptx render
```

Install pptxgenjs locally with `npm install pptxgenjs`. Copy `scripts/deck_helpers.js` next to `build.js` and require it.

## 2. Pitfalls (symptom → fix)

1. **Tables with giant cells, or the table pushed off the slide.** Since pptxgenjs v3.8, table cell `margin` is in **inches**: `margin: [0, 6, 0, 6]` gives 6-inch margins. Use `[0, 0.08, 0, 0.08]`.

2. **A bullet made of several colored runs loses its bullet.** pptxgenjs writes an `<a:pPr>` for every run of a paragraph, and LibreOffice applies the last one, which has no bullet. Putting `bullet` on every run doesn't help: each run then becomes its own bullet. Fix: put `bullet` on the first run only, then post-process the saved file so each paragraph keeps only its first `<a:pPr>` (`dropExtraParaProps()` in `deck_helpers.js`).

3. **Lines that break inside "pré-treinada", "1 e 1", "± 0,021" or "16 × 4".** Replace the hyphen with U+2011 (non-breaking hyphen) and the spaces around ×, →, ± with U+00A0. `nb()` in `deck_helpers.js` does it; add the words your deck needs.

4. **PowerPoint underlines all the Portuguese as misspelled.** pptxgenjs writes `lang="en-US"` on every run. Pass `lang: "pt-BR"` on text boxes, bullets, the title placeholder and **every table cell's options**, because table cells don't inherit it.

5. **✓ ✗ ⋮ show as empty boxes.** Roboto has no such glyphs. In matplotlib use `font.family: ["Roboto", "DejaVu Sans"]`. In pptx shapes that only hold a symbol, set `fontFace: "DejaVu Sans"` or "Segoe UI Symbol".

6. **The bold text in your render doesn't match PowerPoint.** Without `Roboto-Bold.ttf` installed (for example in `~/.fonts`), LibreOffice draws all bold Roboto as DejaVu Sans Bold, which is wider. Your previews then show overflow that won't exist, or hide overflow that will. Install the real font files before trusting a render.

7. **Bullets show as boxes in the original deck's render.** Google Slides exports use a private-use bullet glyph. That's one reason to rebuild an exported deck instead of patching it.

8. **The validator warns about "folder entries in the ZIP".** Some cloud services fail to open those files. Run `zip -dq deck.pptx "*/"` after writing.

9. **A corrupt file after small changes.** Common causes: hex colors with `#` or 8 digits, a negative shadow offset, or one options object reused for two shapes (pptxgenjs mutates option objects; build a fresh object each time).

10. **Stretched images.** Pass both `w` and `h`, computed from the figure's `figsize` or the photo's aspect ratio.

11. **Text overflowing a card in PowerPoint but not in the preview.** Use the same fonts in both. Leave about 10% slack in text boxes, and prefer shortening the layout over shrinking fonts below 12 pt for body text and 9 pt for source lines.

12. **LibreOffice conversion silently produces nothing.** Check that the PDF exists after converting. A Python wrapper run with an interpreter that lacks its dependencies can fail without an error. With plain `soffice`, pass `--outdir` and a fresh profile dir if another instance is open (`render.sh` does this).

## 3. Rendering and looking at every slide

```bash
bash scripts/render.sh deck.pptx render     # render/deck.pdf, render/slide-01.jpg…, render/contact-1.jpg…
```

Look at the contact sheets after every build, and open slides with small text at full size. What to check:
- clipped labels in figures; text touching or overflowing card edges
- a bullet that lost its marker, or one item split into two bullets
- tables: column widths, wrapped cells ("cabeça (melhor\npasso)" means the column is too narrow)
- arrows that point at nothing; overlapping thumbnails
- every color, mark and symbol explained on the slide itself

## 4. Rebuilding an exported deck in frozen mode

1. Unpack the pptx (`python -I -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" deck.pptx unz`) and dump each slide's shapes: position, size, font size, color and text. Also dump `ppt/notesSlides/*` and map them through `ppt/slides/_rels/slideN.xml.rels`, because notes files are not numbered like the slides.
2. Render the original to PDF and images for side-by-side comparison.
3. Write `build.js` reproducing every slide's text **verbatim**, including line-level emphasis (red run, bold line) and the notes, then add the visuals.
4. Run `python3 scripts/check_verbatim.py original.pdf new.pdf`. It lists, per slide, original words missing from the new version. The only acceptable misses are hyphenation artifacts and approved wording changes.

## 5. Delivering

- Deliver the .pptx plus a PDF render. Google Slides opens the pptx. Canva imports it (re-import after every change; don't count on editing an existing Canva design through tools).
- Never overwrite the group's original file. Use a new name or a new folder.
- In the final message, tell the person: what each slide gained, the open wording proposals with 2–3 options each, every new label or caption you wrote (it's new wording they haven't approved), and any approximation (nudged map positions, illustrative sketches).
