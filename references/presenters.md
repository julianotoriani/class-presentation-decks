# Presenter material

## Contents
1. Why not speaker notes
2. The phone script (format and generator)
3. Writing the speech
4. Splitting slides between presenters
5. Q&A appendix
6. Tutoring a presenter who is lost

## 1. Why not speaker notes

In practice speaker notes never get used during a class presentation: the laptop is on the projector, and presenters can't see the notes. Presenters read from their phones instead. So keep the notes, especially if the original deck had them, but the real script is a PDF built for a phone screen.

## 2. The phone script

`scripts/phone_script_pdf.py` builds it. Its pages are 108 mm wide and as tall as needed (at least 192 mm):
- an index page: one block per presenter, with their slide range and topics; tapping it jumps to their first slide
- one page per slide: "Slide N · Name" in the presenter's color, the title, the slide image, then what to say
- an optional Q&A appendix linked from the index

Input `script.json`, one object per slide in deck order:

```json
[
  {"deckIndex": 1, "title": "Capa", "presenter": 1, "name": "Ana Souza",
   "text": "(Se apresentar e apresentar o grupo.)\n\nNosso tema é …"},
  {"deckIndex": 2, "title": "O exemplo que vamos usar", "presenter": 1, "name": "Ana Souza",
   "text": "Um hospital manda laudos …"}
]
```

- Paragraphs are separated by a blank line. A paragraph wrapped entirely in parentheses is a stage direction and is drawn in gray.
- Emit this file from the deck generator (`build.js`) at the same time as the notes, so the speech and the slides never drift apart.
- Slide images come from `render.sh` (`render/slide-01.jpg`, …). Run the renderer first.

Usage:

```bash
python3 scripts/phone_script_pdf.py --script build/script.json --slides build/render \
    --qa build/perguntas.md --title "Seminário: roteiro" --out roteiro.pdf
```

It needs `reportlab` (`pip install reportlab`). It uses Roboto if installed, otherwise DejaVu Sans, otherwise Helvetica.

## 3. Writing the speech

- Write it the way a student talks, with the same rules as the slides (`writing-pt.md`).
- The speech complements the screen instead of reading it. When the speech and the screen state the same fact, use the same words: listeners hear and read it at once.
- Aim for about 30–60 s per slide (about 130 words per minute) and give step slides about 30 s each.
- Name the running example in the speech of every section ("no caso do hospital, …").

## 4. Splitting slides between presenters

- Ask who presents which part; don't assume. People swap parts at the last minute.
- Show the word count per presenter and flag big imbalances. The group may still keep the split, because short step slides overstate the time.
- Give the group a plain list to paste into their chat, with no headings and one line per person:
  `- Ana: slides 1–5 (abertura, exemplo, RSA)`
- If the presenters aren't decided yet, keep placeholders in the notes ("vaga 3 (a definir)") instead of guessing names.

## 5. Q&A appendix

Write `perguntas.md` in this format:

```
# Perguntas prováveis

Respostas curtas para perguntas do professor.

## Por que esse número, 3329?

Resposta em 2–4 frases, no mesmo tom da fala.
```

Good sources of questions:
- comparisons with what the class already knows ("how does this compare to RSA?")
- "why this specific number / parameter?"
- "what exactly is being encrypted / recovered?"
- "why can't N qubits just break an N-bit key?"
- every myth you cut from the speech (it goes here instead)
- the limitations of your own results

## 6. Tutoring a presenter who is lost

When someone says "I'm more and more confused", stop explaining in paragraphs and switch to baby steps:
1. Drop to the smallest version: one dimension before two, numbers under 100, one secret value.
2. Teach one idea per step in 3–5 lines, then ask 2–3 short questions (a, b, c) whose answers are numbers or yes/no.
3. Wait for the answers. Correct each one, saying why in one line, then move on.
4. Define any term before a question uses it. Asking "what bits does the receiver read back?" before saying what the message is only adds confusion.
5. When an answer shows a misconception, add a step for it rather than restating the old one louder.
6. At the end, connect the toy back to the slide's drawing ("the 5 and 3 in step 7 are the same 5 and 3 here").

Example step:

```
Passo 3: ruído e arredondamento
A grade tem um ponto a cada 10 unidades. A mensagem 1 vira o ponto 70; a mensagem 0, o ponto 0.
Antes de enviar, o hospital soma um ruído pequeno, entre −4 e 4.

a) Se o hospital manda a mensagem 1 e soma o ruído 3, que número sai?
b) Qual ponto da grade está mais perto desse número?
c) Qual mensagem o laboratório lê?
```
