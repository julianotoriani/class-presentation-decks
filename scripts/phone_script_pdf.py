#!/usr/bin/env python3
"""Build a phone-readable presenter script: one page per slide (slide image + what to say),
an index where each presenter taps their name to jump to their part, and an optional Q&A appendix.

Usage:
  phone_script_pdf.py --script script.json --slides render/ --out roteiro.pdf
                      [--qa perguntas.md] [--title "Seminário: roteiro"]

script.json: a list in deck order, one object per slide:
  {"deckIndex": 3, "title": "Classificar ou buscar?", "presenter": 1, "name": "Ana Souza",
   "text": "Paragraphs separated by a blank line.\\n\\n(Stage directions in parentheses are drawn in gray.)"}
--slides: folder with slide-01.jpg, slide-02.jpg, … (from render.sh or pdftoppm -jpeg).
perguntas.md: "# Title", an intro paragraph, then "## Question" followed by answer paragraphs.

Needs reportlab (pip install reportlab). Uses Roboto if installed, else DejaVu Sans, else Helvetica.
"""
import argparse
import glob
import json
import os
import re
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

W = 108 * mm          # phone-width page; height grows with the text
MIN_H = 192 * mm
M = 7 * mm
CW = W - 2 * M
PARA_GAP = 3.2 * mm

INK = HexColor("#1B2430")
MUTED = HexColor("#5B6573")
LINE = HexColor("#C9D0D8")
QA_COLOR = INK
# one color per presenter, dark enough for a phone in sunlight; cycles after 6
PRESENTER_COLORS = ["#1E40AF", "#7C3AED", "#C2410C", "#BE185D", "#0F766E", "#B91C1C"]


def find_font(names):
    roots = [os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts"),
             "/usr/share/fonts", "/usr/local/share/fonts", "/Library/Fonts", "C:/Windows/Fonts"]
    for root in roots:
        for name in names:
            hits = glob.glob(os.path.join(root, "**", name), recursive=True)
            if hits:
                return hits[0]
    return None


def register_fonts():
    for regular, medium in (("Roboto-Regular.ttf", "Roboto-Medium.ttf"), ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")):
        r, b = find_font([regular]), find_font([medium])
        if r and b:
            pdfmetrics.registerFont(TTFont("Body", r))
            pdfmetrics.registerFont(TTFont("Body-Medium", b))
            return "Body", "Body-Medium"
    return "Helvetica", "Helvetica-Bold"


BODY_FONT, MEDIUM_FONT = register_fonts()
TAG = ParagraphStyle("tag", fontName=MEDIUM_FONT, fontSize=10, leading=13)
TITLE = ParagraphStyle("title", fontName=MEDIUM_FONT, fontSize=16, leading=20, textColor=INK)
BODY = ParagraphStyle("body", fontName=BODY_FONT, fontSize=13, leading=18.5, textColor=INK)
STAGE = ParagraphStyle("stage", parent=BODY, textColor=MUTED)
SMALL = ParagraphStyle("small", fontName=BODY_FONT, fontSize=11, leading=15, textColor=MUTED)
QUESTION = ParagraphStyle("question", fontName=MEDIUM_FONT, fontSize=14, leading=18.5, textColor=INK)


def color_of(k, order):
    return HexColor(PRESENTER_COLORS[order.index(k) % len(PRESENTER_COLORS)])


def slide_images(folder):
    images = {}
    for f in glob.glob(os.path.join(folder, "slide-*.jpg")) + glob.glob(os.path.join(folder, "slide-*.png")):
        images[int(re.search(r"slide-(\d+)\.(jpg|png)$", f).group(1))] = f
    return images


def speech_paragraphs(text):
    paras = []
    for block in text.strip().split("\n\n"):
        block = " ".join(block.split())
        if block:
            style = STAGE if block.startswith("(") and block.endswith(")") else BODY
            paras.append(Paragraph(escape(block), style))
    return paras


def height_of(flowables, gap):
    return sum(f.wrap(CW, 10_000)[1] for f in flowables) + gap * max(0, len(flowables) - 1)


def draw_stack(c, flowables, y, gap):
    for f in flowables:
        _, h = f.wrap(CW, 10_000)
        f.drawOn(c, M, y - h)
        y -= h + gap
    return y


def read_questions(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        blocks = [b.strip() for b in f.read().split("\n\n") if b.strip()]
    title, intro, qas = "Perguntas", [], []
    for b in blocks:
        if b.startswith("## "):
            qas.append((b[3:].strip(), []))
        elif b.startswith("# "):
            title = b[2:].strip()
        elif qas:
            qas[-1][1].append(" ".join(b.split()))
        else:
            intro.append(" ".join(b.split()))
    return title, intro, qas


def draw_index(c, items, order, title, qa_title):
    blocks = []
    for k in order:
        mine = [it for it in items if it["presenter"] == k]
        lo, hi = min(it["deckIndex"] for it in mine), max(it["deckIndex"] for it in mine)
        topics = []
        for it in mine:
            if it["title"] not in topics:
                topics.append(it["title"])
        head = Paragraph(escape(f"{mine[0]['name']}"), ParagraphStyle(
            "h", parent=TAG, fontSize=13, leading=17, textColor=color_of(k, order)))
        rng = f"Slide {lo}" if lo == hi else f"Slides {lo} a {hi}"
        blocks.append((k, head, Paragraph(escape(f"{rng}: " + " · ".join(topics)), SMALL)))
    if qa_title:
        blocks.append(("qa", Paragraph(escape(qa_title), ParagraphStyle(
            "h", parent=TAG, fontSize=13, leading=17, textColor=QA_COLOR)),
            Paragraph("Respostas curtas, no fim deste PDF.", SMALL)))

    intro = [Paragraph(escape(title), TITLE),
             Paragraph("Uma página por slide, com a imagem do slide e o que falar. "
                       "Toque no nome para ir direto para a sua parte.", SMALL)]
    h = M + height_of(intro, 2 * mm) + 6 * mm
    h += sum(height_of([hd, tp], 1.2 * mm) + 5 * mm for _, hd, tp in blocks)
    c.setPageSize((W, max(MIN_H, h + M)))
    y = draw_stack(c, intro, c._pagesize[1] - M, 2 * mm) - 4 * mm
    for k, head, topics in blocks:
        top = y
        y = draw_stack(c, [head, topics], y, 1.2 * mm)
        c.setFillColor(QA_COLOR if k == "qa" else color_of(k, order))
        c.rect(M - 3 * mm, y + 1.2 * mm, 1 * mm, top - y - 1.2 * mm, stroke=0, fill=1)
        c.linkRect("", "qa" if k == "qa" else f"p{k}", (M - 3 * mm, y + 1.2 * mm, W - M, top), relative=0, thickness=0)
        y -= 5 * mm
    c.showPage()


def draw_slide(c, it, image, order, first_of_presenter):
    k = it["presenter"]
    color = color_of(k, order)
    first_name = it["name"].split()[0]
    tag = Paragraph(escape(f"Slide {it['deckIndex']} · {first_name}"), ParagraphStyle("t", parent=TAG, textColor=color))
    title = Paragraph(escape(it["title"]), TITLE)
    body = speech_paragraphs(it.get("text", ""))
    img_h = CW * 9 / 16
    h = M + height_of([tag, title], 1.5 * mm) + 4 * mm + img_h + 5 * mm + height_of(body, PARA_GAP) + M
    c.setPageSize((W, max(MIN_H, h)))
    page_h = c._pagesize[1]

    key = f"s{it['deckIndex']}"
    c.bookmarkPage(key)
    if first_of_presenter:
        c.bookmarkPage(f"p{k}")
        c.addOutlineEntry(it["name"], f"p{k}", level=0)
    c.addOutlineEntry(f"{it['deckIndex']}. {it['title']}", key, level=1)

    c.setFillColor(color)
    c.rect(0, page_h - 2 * mm, W, 2 * mm, stroke=0, fill=1)
    y = draw_stack(c, [tag, title], page_h - M, 1.5 * mm) - 2.5 * mm
    if image:
        c.drawImage(image, M, y - img_h, CW, img_h)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.rect(M, y - img_h, CW, img_h, stroke=1, fill=0)
    y -= img_h + 5 * mm
    draw_stack(c, body, y, PARA_GAP)
    c.showPage()


def draw_questions(c, title, intro, qas):
    def qa_flowables(q, answer):
        return [Paragraph(escape(q), QUESTION)] + [Paragraph(escape(a), BODY) for a in answer]

    head = [Paragraph(escape(title), TITLE)] + [Paragraph(escape(t), SMALL) for t in intro]
    groups, current, used = [], [], M + height_of(head, 2 * mm) + 6 * mm
    for q, answer in qas:
        h = height_of(qa_flowables(q, answer), 2 * mm) + 7 * mm
        if current and used + h + M > MIN_H:
            groups.append(current)
            current, used = [], M
        current.append((q, answer))
        used += h
    groups.append(current)

    for gi, group in enumerate(groups):
        blocks = [qa_flowables(q, a) for q, a in group]
        h = M + (height_of(head, 2 * mm) + 6 * mm if gi == 0 else 0)
        h += sum(height_of(b, 2 * mm) + 7 * mm for b in blocks) + M
        c.setPageSize((W, max(MIN_H, h)))
        page_h = c._pagesize[1]
        if gi == 0:
            c.bookmarkPage("qa")
            c.addOutlineEntry(title, "qa", level=0)
        c.setFillColor(QA_COLOR)
        c.rect(0, page_h - 2 * mm, W, 2 * mm, stroke=0, fill=1)
        y = page_h - M
        if gi == 0:
            y = draw_stack(c, head, y, 2 * mm) - 6 * mm
        for b in blocks:
            y = draw_stack(c, b, y, 2 * mm) - 5 * mm
            c.setStrokeColor(LINE)
            c.setLineWidth(0.5)
            c.line(M, y + 2.5 * mm, W - M, y + 2.5 * mm)
        c.showPage()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True)
    ap.add_argument("--slides", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--qa")
    ap.add_argument("--title", default="Roteiro da apresentação")
    a = ap.parse_args()

    with open(a.script, encoding="utf-8") as f:
        items = json.load(f)
    images = slide_images(a.slides)
    missing = [it["deckIndex"] for it in items if it["deckIndex"] not in images]
    if missing:
        raise SystemExit(f"missing slide images for slides {missing}: render the deck first")
    order = []
    for it in items:
        if it["presenter"] not in order:
            order.append(it["presenter"])

    c = canvas.Canvas(a.out, pagesize=(W, MIN_H))
    c.setTitle(a.title)
    c.showOutline()
    questions = read_questions(a.qa)
    draw_index(c, items, order, a.title, questions[0] if questions else None)
    seen = set()
    for it in items:
        draw_slide(c, it, images[it["deckIndex"]], order, it["presenter"] not in seen)
        seen.add(it["presenter"])
    if questions:
        draw_questions(c, *questions)
    c.save()
    print(f"ok: {a.out} ({c.getPageNumber() - 1} pages)")


if __name__ == "__main__":
    main()
