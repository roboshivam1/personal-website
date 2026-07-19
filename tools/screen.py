#!/usr/bin/env python3
"""Put a photograph through a printing press.

Edit the block below, then:  python3 tools/screen.py

This is NOT part of the build. Screening a photo is a taste decision, so it
happens by hand, while you look at the result. The output has the paper colour
baked into the pixels — a finished print. Drop it in static/img/ and the site
shows it as-is, identically in every edition, forever.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageStat

# ══════════════════════════════════════════════════════════════════════
#  EDIT THIS
# ══════════════════════════════════════════════════════════════════════

INPUT = "photos/HW/acura90nsx.jpg"           # the original. relative to the project root.
OUTPUT = "static/img/motoring/acura90nsx_dotted.jpg"      # where the finished plate goes.

CONTACT_SHEET = False   # True -> ignore OUTPUT, write a labelled grid of nine
                        # settings next to it. Open it, pick a tile, copy its
                        # numbers down here, set this back to False, run again.

CELL = 5          # px per dot. 3 = fine, 8 = aggressively printed. THE look knob.
TARGET = 0.52     # average tone of the plate, 0..1. THE exposure knob.
GAIN = 1.4        # dot size multiplier. >1 lets dark dots merge, like wet ink.
ANGLE = 45        # screen angle. 45 is what a real press uses for one colour.
CONTRAST = 1.15   # crushed a little after exposure. 1.6 blows out highlights.
MAX_WIDTH = 1600  # the original gets resized to this first.

PAPER = (229, 225, 215)   # --plate-paper in paper.css. keep these two in step.
INK = (23, 23, 27)        # --ink, daylight edition.

# ══════════════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent   # paths above are relative to here,
OVERSAMPLE = 4                                  # not to wherever you ran python from


def expose(im, target=TARGET, contrast=CONTRAST):
    """Pull this plate's average tone to `target`, whatever it started at.

    A photo of a white wall lives at the top of the range. autocontrast alone is
    a LINEAR stretch and leaves it there — or worse, lifts it. So solve a curve
    instead: find the gamma where mean**g == target. Bright photos get a steep
    curve, normal ones pass through untouched.
    """
    im = ImageOps.autocontrast(im.convert("L"), cutoff=1.0)
    mean = ImageStat.Stat(im).mean[0] / 255
    if 0.02 < mean < 0.98:
        g = math.log(target) / math.log(mean)
        im = im.point([round(255 * (v / 255) ** g) for v in range(256)])
    return ImageEnhance.Contrast(im).enhance(contrast)


def screen(im, cell=CELL, target=TARGET, gain=GAIN, angle=ANGLE, contrast=CONTRAST):
    """One dot per cell, sized by that cell's darkness, on a rotated grid."""
    gray = expose(im, target, contrast)
    rot = gray.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=255)
    w, h = rot.size

    canvas = Image.new("L", (w * OVERSAMPLE, h * OVERSAMPLE), 255)
    draw = ImageDraw.Draw(canvas)
    half = cell * OVERSAMPLE / 2

    for x in range(0, w, cell):
        for y in range(0, h, cell):
            cellbox = rot.crop((x, y, x + cell, y + cell))
            darkness = (255 - ImageStat.Stat(cellbox).mean[0]) / 255
            r = (darkness ** 0.5) * half * gain      # sqrt: dot AREA tracks darkness
            if r < 0.35:
                continue
            cx, cy = (x + cell / 2) * OVERSAMPLE, (y + cell / 2) * OVERSAMPLE
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=0)

    back = canvas.rotate(-angle, resample=Image.BICUBIC, expand=False, fillcolor=255)
    ow, oh = gray.size
    cx, cy = back.size[0] / 2, back.size[1] / 2
    plate = back.crop((
        int(cx - ow * OVERSAMPLE / 2), int(cy - oh * OVERSAMPLE / 2),
        int(cx + ow * OVERSAMPLE / 2), int(cy + oh * OVERSAMPLE / 2),
    )).resize((ow, oh), Image.LANCZOS)

    # Paint it: ink where the dots are, paper everywhere else.
    out = Image.new("RGB", plate.size, PAPER)
    out.paste(Image.new("RGB", plate.size, INK), mask=ImageOps.invert(plate))
    return out


def load(path, max_width=MAX_WIDTH):
    im = Image.open(path)
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    return im


def contact_sheet(src):
    """Same photo, nine settings, each tile labelled with its own numbers."""
    thumb = load(src, 420)
    tiles = []
    for cell in (3, 5, 8):
        for target in (0.42, 0.52, 0.62):
            tile = screen(thumb, cell=cell, target=target)
            label = f"CELL {cell}  TARGET {target}"
            d = ImageDraw.Draw(tile)
            d.rectangle((0, 0, 10 + 6 * len(label), 18), fill=INK)
            d.text((4, 4), label, fill=PAPER, font=ImageFont.load_default())
            tiles.append(tile)

    tw, th = tiles[0].size
    sheet = Image.new("RGB", (tw * 3 + 40, th * 3 + 40), PAPER)
    for i, tile in enumerate(tiles):
        sheet.paste(tile, (10 + (i % 3) * (tw + 10), 10 + (i // 3) * (th + 10)))
    return sheet


def main():
    src = ROOT / INPUT
    if not src.exists():
        raise SystemExit(f"No such photo: {src}\nEdit INPUT at the top of this file.")

    if CONTACT_SHEET:
        out = (ROOT / OUTPUT).with_name(Path(OUTPUT).stem + "-contact.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        contact_sheet(src).save(out)
        print(f"contact sheet -> {out.relative_to(ROOT)}")
        print("open it, pick a tile, copy its numbers into CELL/TARGET, "
              "set CONTACT_SHEET = False, run again")
        return

    out = ROOT / OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    screen(load(src)).save(out, optimize=True)
    print(f"screened {INPUT} -> {OUTPUT}   (CELL {CELL}, TARGET {TARGET})")


if __name__ == "__main__":
    main()