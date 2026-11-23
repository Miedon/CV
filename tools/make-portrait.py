#!/usr/bin/env python3
"""Generate the portrait variants the pages reference.

    python tools/make-portrait.py path/to/new-photo.jpg

Writes images/portrait-400.jpg and images/portrait-800.jpg: square, centre
cropped, EXIF stripped, progressive JPEG. The pages pick between them via
srcset, so nothing in the HTML needs touching when the photo is replaced.

Keep the original alongside as images/portrait-source.jpg so the variants can
be regenerated later.
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is missing: python -m pip install Pillow")

SIZES = (400, 800)
QUALITY = 82
OUT_DIR = Path(__file__).resolve().parent.parent / "images"


def square(im):
    """Centre crop to a square, keeping as much of the frame as possible."""
    side = min(im.size)
    left = (im.width - side) // 2
    top = (im.height - side) // 2
    return im.crop((left, top, left + side, top + side))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    src = Path(sys.argv[1])
    if not src.is_file():
        sys.exit(f"not a file: {src}")

    with Image.open(src) as im:
        # Honour the EXIF orientation flag before dropping the metadata.
        im = ImageOps.exif_transpose(im)
        im = square(im).convert("RGB")

        if min(im.size) < max(SIZES):
            print(f"note: source is only {im.width}px wide; "
                  f"{max(SIZES)}px variant will be upscaled")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for size in SIZES:
            out = OUT_DIR / f"portrait-{size}.jpg"
            im.resize((size, size), Image.LANCZOS).save(
                out, "JPEG", quality=QUALITY, optimize=True, progressive=True
            )
            print(f"{out.relative_to(OUT_DIR.parent)}  {out.stat().st_size // 1024} KB")

    keep = OUT_DIR / "portrait-source.jpg"
    if src.resolve() != keep.resolve():
        print(f"\nremember to keep the original as {keep.relative_to(OUT_DIR.parent)}")


if __name__ == "__main__":
    main()
