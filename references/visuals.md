# Visuals: patterns that worked, and how to draw them

## Contents
1. Ground rules
2. matplotlib setup
3. Checking numbers before drawing
4. Pattern catalogue
5. Step sequences for algorithms
6. Photos

## 1. Ground rules

- A visual earns its place by carrying information the bullets don't. Examples are a real search result with its scores, the dataset's own pictures, or the experiment's before and after. Stock icons and decorative shapes don't count.
- Draw from real data whenever it exists. Re-run the group's pipeline (their notebook, their preprocessing, their model weights) instead of inventing values. The real thing also gives the presenter something concrete to point at.
- Every mark gets a key on the slide. A bar of small rectangles with three of them crossed out in red meant nothing to the person presenting it until someone explained it. Label segments and colors directly, next to the mark rather than in a separate legend box.
- Draw each figure at the size it will have on the slide. If the picture box is 3.3 × 2.5 in, use `figsize=(3.3, 2.5)`. Font sizes in matplotlib are then real slide points: keep them at 10 pt or more, and at least 9.5 for tick labels.
- Keep a figure's numbers consistent with the slide. If a table shows 0,949 and 0,889, the chart shows −0,060, not −0,059 computed from unrounded values. Use the slide's language for decimals ("0,76" in Portuguese).
- Projector palette: dark blue `#1E40AF` for "right/same", dark red `#B91C1C` for "wrong/other", ink `#1B2430`, gray `#8A94A3`. Don't use green. Pale fills go behind dark text only.
- Label illustrations as illustrations. If an example uses a different model than the slide's numbers, say so ("Exemplo com a ResNet-50 congelada").

## 2. matplotlib setup

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, MUTED, LINE = "#1B2430", "#5B6573", "#C9D0D8"
BLUE, RED, GRAY = "#1E40AF", "#B91C1C", "#8A94A3"
plt.rcParams.update({
    # Roboto has no ✓ ✗ ⋮ glyphs: DejaVu Sans fills them in
    "font.family": ["Roboto", "DejaVu Sans"],
    "font.size": 11, "text.color": INK,
    "axes.edgecolor": LINE, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "savefig.dpi": 250,
})

def fmt(x, n=2):                     # decimal comma for pt-BR slides
    return f"{x:.{n}f}".replace(".", ",")
```

Run a script that reads downloaded data with `python -I figures.py <data_dir> <results_dir>`, passing paths as arguments. Keep the script outside the downloaded folder.

## 3. Checking numbers before drawing

Assert against the group's own reported numbers before saving anything. If an assertion fails, the reproduction differs from theirs: find out why before drawing.

```python
assert int((labels[S.argmax(1)] != labels).sum()) == 16          # "16 erros no top-1" in the report
assert abs(threshold - 0.732) < 5e-4                             # "limiar 0,732" on the slide
assert np.allclose(top3_scores, [0.664, 0.557, 0.492], atol=5e-4)
for row in csv.DictReader(open(results / "tabela_principal.csv")):
    assert abs(float(row["mAP"]) - table[(row["extrator"], row["modo"])]) < 5e-4
```

Save the example indices you chose, such as the query photo or the worked-example item, to a small `meta.json`. The deck generator can then place the same photos and quote the same numbers without hard-coding them twice.

## 4. Pattern catalogue

Each of these replaced a text-only slide.

| slide is about | visual |
|---|---|
| the problem / running example | the real query photo → a strip of the collection, with the matches outlined in blue → the results with their scores |
| "classify or search?" type comparison | a tiny diagram inside each option's card: a fixed-output classifier with a dashed "objeto novo?" box, and an index table gaining one blue row |
| "similar things end up close" | a 2D map (PCA of the real embeddings) with photo thumbnails as markers, colored borders and a group name over each cluster. Push overlapping thumbnails slightly apart and say "projeção em 2 dimensões" |
| a pipeline of N steps | N cards, each with a mini figure on the same running example: photo → vector strip; vector → unit circle; two arrows with the cosine; the top-3 with scores |
| model adaptation (a small head on a frozen network) | box diagram: photo → frozen network (gray) → vector d → head drawn as shrinking bars d → 512 → 256 (blue, "treinada") → vector 256; plus a labeled before/after scatter illustration of the loss |
| dataset split | a proportional bar, one cell per category, colored by split. **Label each segment** ("49 treino", "10 validação", "40 teste", "3 tiradas"), plus 3 sample images per split card |
| "our own photos" | an object × background grid of thumbnails (empty cell = combination not photographed), which shows the variation and the shared backgrounds at a glance |
| metric definitions (P@k, AP) | one real ranked list with ✓/✗ and scores, plus the computation written out: "P@5 = 3/5 = 0,60", "1ª: 1/1 · 4ª: 2/4 · 5ª: 3/5 · 7ª: 4/7 → AP = 0,67" |
| results over several seeds | a slope chart, frozen → head, one line per seed, with the main seed bold in blue and the others in gray |
| validation didn't predict test | signed difference bars (head − frozen), validation next to test per model, blue for a gain and red for a loss, with the value printed on each bar |
| hits and errors | two photo rows (query → top-5) with colored borders, ✓/✗ and scores, plus a bar chart of the error pattern found (for example "14 de 16 errors share the query's background, vs 26% by chance") |
| "add a new item without retraining" experiment | 4 step cards: before (query → wrong top-1 with its score), add (a stack of photos "+5"), after (query → correct results with scores), threshold (a number line with the reject zone, the threshold line and the score dot) |
| conclusion | a colored icon per column (✓ blue, ✗ red, ! ink) and a colored rule under each heading |

## 5. Step sequences for algorithms

What made a hard algorithm (lattice encryption) understandable:
- Use the same axes, scale and colors on every step, so only the new thing moves. Earlier elements stay, drawn in gray.
- Put one change per slide, and give each step a short caption that names what changed and which earlier element it uses. "From step 2 to 3 I have no idea what happened" means a step was skipped.
- Every colored element is named in the caption or with a label on the figure, so nobody has to ask "what do the red lines mean?".
- Use the audience's vocabulary in labels ("vetores", "grade", "ponto", "ruído").
- Show the difficulty as well as the mechanism. One step should show the long path an attacker must take with the public key, next to the short one with the private key.
- Put a simplification note once at the start of the drawing and once at the end, not on every slide.
- Compute every frame numerically and assert what the caption claims ("o X cai na célula do ponto (5, 3)"). A figure that contradicts its own caption destroys trust.
- If the presenter is still lost, drop a dimension: explain in 1D with small integers first (see `presenters.md`).

## 6. Photos

```python
from PIL import Image, ImageOps

def thumb(path, out, w=300):          # 3:4 portrait thumbnail, EXIF rotation applied
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    ImageOps.fit(im, (w, int(w * 4 / 3)), Image.LANCZOS).save(out, quality=90)
```

- Place photos directly in the pptx (`addImage`) where possible, since they come out sharper than inside a matplotlib figure. Draw the border as a separate unfilled rectangle 2–2.25 pt wide.
- Inside matplotlib, use `fig.add_axes([...])` with `imshow(aspect="auto")` and colored spines as borders.
- Check that photos have no faces, license plates or personal data when the assignment says so.
- Public datasets: download into their own folder, extract only the categories you show, and credit the license on the slide's source line (for example "CaltechDATA, licença CC BY 4.0").
