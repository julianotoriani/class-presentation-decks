# class-presentation-decks

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for making and fixing slide decks for class presentations, seminars and group college projects. It turns what we learned building two real group decks into rules Claude follows:

- **Wording**: write the way students talk. The skill lists the AI-sounding patterns we kept rejecting ("não é X, é Y", rhetorical questions, teasers, punchlines, pronouns for things, acronym soup), with real before → after rewrites in Portuguese. When you flag a sentence, Claude offers 2–3 alternatives instead of picking for you.
- **Structure**: one running example through the whole deck, heavy ideas as step-by-step visual sequences, no recap slides.
- **Visuals**: build figures from the group's real data and photos, check every number against the reported results, explain every color and mark on the slide, keep figure text at 10 pt or more.
- **Projector-safe colors**: dark blue and dark red, no green, because classroom projectors wash it out.
- **Frozen mode**: when the slide count, topics and text can't change, add visuals without rewording, and verify that every word is still on its slide.
- **Presenter material**: a phone-readable PDF script per presenter (speaker notes never get used live), a Q&A appendix, and step-by-step tutoring with quizzes for a presenter who is lost.
- **Building the file**: a pptxgenjs + matplotlib + LibreOffice pipeline, with fixes for the bugs that cost us hours.

## Install

**Claude Code**

```bash
git clone https://github.com/julianotoriani/class-presentation-decks ~/.claude/skills/class-presentation-decks
```

**Claude apps (claude.ai / desktop)**: download this repository as a zip and upload it under Settings → Capabilities → Skills.

Then ask something like "melhora essa apresentação, tá muito texto" or "make slides for our seminar on X" and the skill kicks in.

## What's inside

```
SKILL.md                      the rules, with the reasons behind them
references/writing-pt.md      rejected wording patterns with real rewrites (pt-BR)
references/visuals.md         figure patterns that worked, matplotlib setup, number checks
references/pptx-build.md      build pipeline and pptxgenjs/LibreOffice pitfalls
references/presenters.md      phone script, Q&A, splitting slides, tutoring a presenter
scripts/deck_helpers.js       pptxgenjs helpers with the pitfalls worked around
scripts/render.sh             pptx → PDF → one JPG per slide → contact sheets
scripts/check_verbatim.py     checks that a rebuilt deck kept every original word
scripts/phone_script_pdf.py   builds the phone-readable presenter script
```

The scripts need Node.js with `pptxgenjs`, Python with `matplotlib` and `reportlab`, LibreOffice, poppler (`pdftoppm`, `pdftotext`) and, for contact sheets, ImageMagick.
