#!/usr/bin/env bash
# Render a deck so every slide can be looked at:
#   deck.pptx -> <outdir>/<name>.pdf -> <outdir>/slide-NN.jpg -> <outdir>/contact-N.jpg (6 slides per sheet)
#
# Usage: render.sh deck.pptx [outdir]          (outdir defaults to ./render)
# Needs: LibreOffice (soffice), poppler (pdftoppm), ImageMagick (montage) for the contact sheets.
# Set SOFFICE to override the LibreOffice binary.
set -euo pipefail

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then
  sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi

DECK="$(realpath "$1")"
OUT="$(realpath -m "${2:-render}")"
NAME="$(basename "${DECK%.*}")"
SOFFICE="${SOFFICE:-soffice}"

mkdir -p "$OUT"
rm -f "$OUT"/slide-*.jpg "$OUT"/contact-*.jpg "$OUT/$NAME.pdf"

# A private profile dir lets the conversion run even if LibreOffice is already open.
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT
timeout 300 "$SOFFICE" -env:UserInstallation="file://$PROFILE" --headless \
  --convert-to pdf --outdir "$OUT" "$DECK" >/dev/null 2>&1 || true

if [[ ! -s "$OUT/$NAME.pdf" ]]; then
  echo "error: LibreOffice produced no PDF for $DECK" >&2
  exit 1
fi

pdftoppm -jpeg -r 110 "$OUT/$NAME.pdf" "$OUT/slide"
N=$(ls "$OUT"/slide-*.jpg | wc -l)

if command -v montage >/dev/null; then
  ls "$OUT"/slide-*.jpg | xargs -n 6 | nl -w1 -s' ' | while read -r k files; do
    # shellcheck disable=SC2086
    montage $files -tile 2x -geometry 900x+4+4 -background '#888888' "$OUT/contact-$k.jpg"
  done
fi

echo "ok: $N slides -> $OUT ($NAME.pdf, slide-NN.jpg$(command -v montage >/dev/null && echo ', contact-N.jpg'))"
