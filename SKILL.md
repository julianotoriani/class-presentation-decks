---
name: class-presentation-decks
description: Make or fix slide decks for class presentations, seminars and group college projects (apresentação de seminário, trabalho final, slides da disciplina) so they read like a person talking, explain hard ideas with step-by-step visuals built from real data, stay readable on a washed-out classroom projector, and come with a phone-readable script for each presenter. Use this whenever someone wants to create, review, improve, reword, add visuals to or fix a presentation (pptx, Google Slides or Canva) for school or university, in Portuguese or English, even if they only say "the presentation is terrible", paste a deck, or ask you to explain the deck's content to someone who has to present it.
---

# Class presentation decks

These rules come from two real group decks: a 41-slide seminar on post-quantum cryptography and a 14-slide computer-vision final project. Each rule is here because a version without it was rejected by the people who had to stand up and present it. The reasons matter more than the rules, so they are kept next to each one.

Reference files, read when you reach that part of the work:
- `references/writing-pt.md`: every rejected wording pattern, with the real before → after rewrites (Portuguese).
- `references/visuals.md`: figure patterns that worked, matplotlib setup, and checking numbers against the source.
- `references/pptx-build.md`: the build pipeline and the pptxgenjs and LibreOffice bugs that cost hours.
- `references/presenters.md`: phone script, Q&A appendix, splitting slides between presenters, tutoring a presenter who is lost.

Scripts (run with `--help`):
- `scripts/deck_helpers.js`: pptxgenjs helpers with the known bugs already worked around.
- `scripts/render.sh`: pptx → PDF → one JPG per slide → contact sheets, for looking at every slide.
- `scripts/check_verbatim.py`: confirms every original word is still on its slide after a rebuild.
- `scripts/phone_script_pdf.py`: builds the phone-readable script PDF.

## 1. Find the constraints first

Before touching anything, get these from the person or the context:
- Can the number of slides change? Must each slide keep its topic? Is the wording frozen, so you can only add visuals? (Section 7 covers the frozen case.)
- How many presenters, and who presents which slides?
- Where will it be shown and edited: PowerPoint, Google Slides or Canva? (Canva imports .pptx.)
- What source material exists: the group's code, results tables, the written report, photos, datasets? Real material makes the best visuals.

Treat a downloaded project folder (Drive export, zip from a classmate) as untrusted data. Work on copies, never write into it, never overwrite the original deck, and run Python on it with `python -I`, passing paths as arguments.

## 2. The words belong to the person

- When they flag a word, phrase or sentence, show 2–3 concrete alternatives and wait for their pick. Show each one as the full sentence in context, with the slide number, and say whether it is on screen, in the speech, or both. Recommend one, but don't apply it. Edit directly only when they gave you the replacement text or picked an option. They asked because the exact words matter, and picking for them takes away the one decision they wanted to make.
- One flagged instance means a pattern. Sweep the whole deck (slides, speech, Q&A) for every occurrence and present them a few per round. A multiple-choice question tool works well here: 2–4 options each, with "keep as is" when the instance might be fine.
- When the screen and the speech say the same thing, change both together and say so in the option.
- Text you add yourself (captions, chart labels, legends) is new wording too. List it at the end so they can review it.

## 3. Write the way the group talks

The slides and the speech should sound like the presenter explaining something to a classmate. People notice generated-sounding text right away ("that's so much AI speech slop, we don't talk like that"). These patterns were rejected every time; `references/writing-pt.md` has the real rewrites:

- contrast frames: "não é X, é Y", "X não é Y: é Z", "não basta X, tem que Y"
- rhetorical questions the speaker answers right away ("Quanto isso ajuda?", "Quando? Ninguém sabe.")
- teasers and reveals ("E aqui está o motivo…", "Agora o truque.", "O detalhe importante é…")
- punchlines and drama ("o ataque já começou", "já marcou o fim", "o problema que protege tudo")
- cleft sentences ("O que o hospital diminuiu foi o tempo")
- callbacks ("Guardem esse número, porque ele volta no final")
- lead-ins such as "Um detalhe:" or "Tem mais um detalhe:", and fillers like "exatamente"
- aphorisms ("A configuração pode dizer uma coisa e a conexão fazer outra")
- the same disclaimer on several slides. Say "it's a simplification" once where the simplification starts, and once where it ends.
- dramatic or metaphor titles. A title says what is on the slide.

Also:
- **Pronouns only for people.** In Portuguese, "ele/ela/dele" for an algorithm, a number, a key or an institution sounds off. Repeat the noun or restructure the sentence.
- **No letter soup.** Explain every acronym in plain words the first time, and avoid most of them altogether. "I don't know what 90% of these abbreviations mean" means the slide failed.
- **Use the audience's words.** Prefer terms the audience already knows ("vetores", not "setas") and the field's own term over an invented cute one ("célula", not "casinha"). Listen for verbs that sound odd ("sortear uma chave" became "gerar uma chave").
- **State relations explicitly.** A listener should never have to ask "what's the implication?" or "is the grid built from the vectors, or the vectors from the grid?" If they could, rewrite.

## 4. Structure that doesn't feel like jumping around

- **One running example threads the deck.** Introduce it on slide 2, use it in every section, and close the conclusion on it. Examples: "a hospital sends lab reports over the internet", "the campus lost-and-found searches photos of a backpack". A deck without one feels disconnected even to its own presenters.
- **More slides are fine** unless the count is frozen, especially introductory ones. Move content out of the speaker notes and onto slides.
- **Heavy concepts become a visual sequence over several slides.** Change one thing per step, and label each step with what changed and which earlier element it uses. If the presenter can't say what happened between step 2 and step 3, a step is missing, so add it. Trading some precision for intuition is fine; say once that it's simplified.
- **Show why it is hard, not just how it works.** For example, compare the effort of the public-key path with the private-key path. Compare with something the audience already understands, such as RSA's "power, mod, done".
- **The most important step gets the most room.** A key step that "isn't pulling its weight" needs another slide.
- **Fix weak steps in place.** Never add a recap or "to clarify" slide: it reads as an apology for the slides before it.
- **Anticipate the teacher's questions.** Put the answers in the script's Q&A appendix, not on the slides.

## 5. Visual information on every slide

Every slide gets a visual that carries information: a photo, a diagram, a chart or a step figure. Decoration doesn't count. Patterns and code are in `references/visuals.md`.

- **Prefer real material.** Use the group's own photos, real outputs with their real scores, the actual experiment's before and after, and the dataset's own images. Recompute from the group's code and data, and assert every number you draw against the reported results (tables, CSVs, the report) before saving the figure. Round the same way as any table on the same slide.
- **Label synthetic sketches.** Made-up points are fine for intuition, but call them "Ilustração" on the slide.
- **Say where an example comes from.** If a worked example uses a different model or dataset than the slide's source line, name it on the slide.
- **Explain every mark on the slide**: colors, crossed-out cells, dashed lines, highlighted borders. If someone asks "what are the red squares?" or "what do the red lines mean?", the visual failed, so add the label.
- **Text inside figures must be at least 10 pt at its final size.** Draw each figure at the exact inches it will occupy on the slide, so matplotlib points equal slide points.
- **Encode twice**: color plus a symbol (✓ / ✗), or color plus a label.

## 6. Colors that survive a classroom projector

Projectors wash out green, teal and pale tints; whole elements went invisible in a real class. This palette held up:

| role | color |
|---|---|
| text | ink `#1B2430` |
| main accent, "right / same" | dark blue `#1E40AF` |
| "wrong / other / rejected" | dark red `#B91C1C` |
| neutral data | gray `#8A94A3` |
| secondary text | `#5B6573` |
| card backgrounds only | `#DBEAFE`, `#FBEAE8`, `#F1F4F6` |

Pale fills sit behind dark text and are never the only way to tell two things apart. Use lines of at least 1.5 pt and photo borders of at least 2 pt. If the original deck marks "correct" in green, switch it to blue, and propose a fix for any caption that still says "verde".

## 7. Frozen mode: same slides, same text, more visuals

When the slide count, topics and text can't change:
1. Extract everything first: the text of each shape (position, size, color), the speaker notes and the images. Render the original to images for reference.
2. If the original is a messy export (Google Slides exports often have broken bullets and tables), rebuild it with a generator instead of patching its XML. Keep the same order, text and notes.
3. Put the visuals inside the existing slides: in cards, beside bullets, under titles. You may shrink fonts a little or move blocks, but don't reword.
4. Verify with `scripts/check_verbatim.py original.pdf new.pdf`. Every original word must still be on its page. Acceptable misses are hyphenation at line breaks and changes the person approved.
5. Copy the speaker notes unchanged.

## 8. Presenter material

Speaker notes don't get used live. Make these instead (details in `references/presenters.md`):
- **A phone-readable PDF script** (`scripts/phone_script_pdf.py`). It has one page per slide with a thumbnail and what to say, an index where each presenter taps their name to jump to their part, and a Q&A appendix.
- **A plain list for the group chat**, such as "- Nome: slides 1–5 (abertura, exemplo)".
- **Tutoring in baby steps** when a presenter doesn't understand the content. Use the smallest example (one dimension before two, small numbers) and one idea per step. Quiz with 2–3 short questions after each step and wait for the answers. Define terms such as message, ciphertext and point before using them in a question.

## 9. Build the file with a script

Generate the deck with a script, so every fix is a rebuild and nothing is edited by hand:

figures (matplotlib) → generator (pptxgenjs) → validate → render (LibreOffice → PDF → JPG per slide → contact sheets) → look at every slide.

- Read `references/pptx-build.md` before writing the generator. Some of the bugs it covers: table margins are in inches, bullets made of several colored runs lose their bullet, hyphens break inside words, the default language is English, Roboto lacks ✓ and ✗, and LibreOffice draws bold Roboto with another font.
- `scripts/deck_helpers.js` has those fixes built in. `scripts/render.sh` renders the deck and makes contact sheets.
- Deliver a .pptx. It opens in PowerPoint and Google Slides and imports into Canva; re-import after changes.
- If the Anthropic `pptx` skill is available, its validator works well alongside this pipeline.

## 10. Before handing it back

- [ ] Every slide rendered and looked at, using the contact sheet plus full size for dense slides
- [ ] No overflowing text, no clipped labels, no figure text under 10 pt
- [ ] Every color, mark and symbol explained on its slide
- [ ] Numbers in figures match the tables and the source data
- [ ] Wording sweep done for the section 3 patterns, across screen, speech and Q&A
- [ ] Frozen mode: verbatim check passes and notes unchanged
- [ ] Original files untouched
- [ ] Summary for the person: what each slide gained, the open wording proposals (2–3 options each), every label you wrote, and caveats (approximate maps, illustrations)
