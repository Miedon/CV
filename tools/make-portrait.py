#!/usr/bin/env python3
"""Generate the portrait variants the pages reference.

    python tools/make-portrait.py path/to/new-photo.jpg
    python tools/make-portrait.py path/to/new-photo.jpg --box 150,148,1500,1498

Writes images/portrait-400.jpg and images/portrait-800.jpg: square, EXIF
stripped, progressive JPEG. The pages pick between them via srcset, so nothing
in the HTML needs touching when the photo is replaced.

Without --box the crop is the centre square, which is only right when the
subject sits in the middle of the frame. A full-length or portrait-orientation
shot needs an explicit box in source pixels (left,top,right,bottom) framing
head and shoulders — a centre crop would cut the head off. The box is squared
off around its own centre if it is not square already.

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


def square(im, box=None):
    """Crop to a square — the centre of the frame, or around a given box."""
    if box is None:
        side = min(im.size)
        left = (im.width - side) // 2
        top = (im.height - side) // 2
    else:
        left, top, right, bottom = box
        side = max(right - left, bottom - top)
        left += (right - left - side) // 2
        top += (bottom - top - side) // 2
        # Keep the square inside the image rather than letting PIL pad it.
        left = max(0, min(left, im.width - side))
        top = max(0, min(top, im.height - side))
        if side > min(im.size):
            sys.exit(f"--box is larger ({side}px) than the image ({im.size})")
    return im.crop((left, top, left + side, top + side))


def parse_box(arg):
    try:
        left, top, right, bottom = (int(n) for n in arg.split(","))
    except ValueError:
        sys.exit("--box wants four integers: left,top,right,bottom")
    if right <= left or bottom <= top:
        sys.exit("--box must have right > left and bottom > top")
    return left, top, right, bottom


def main():
    args = sys.argv[1:]
    box = None
    if "--box" in args:
        i = args.index("--box")
        if i + 1 >= len(args):
            sys.exit("--box needs a value")
        box = parse_box(args[i + 1])
        del args[i:i + 2]

    if len(args) != 1:
        sys.exit(__doc__)

    src = Path(args[0])
    if not src.is_file():
        sys.exit(f"not a file: {src}")

    with Image.open(src) as im:
        # Honour the EXIF orientation flag before dropping the metadata.
        im = ImageOps.exif_transpose(im)
        im = square(im, box).convert("RGB")

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
