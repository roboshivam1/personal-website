"""Put photographs through a printing press.

A real halftone screen: the image is divided into cells, and each cell gets one
dot whose SIZE is proportional to how dark that cell is. Dark areas grow fat
dots that touch and merge; light areas shrink to specks. That variable dot size
is the thing CSS cannot do — a CSS overlay is a fixed grid multiplied over the
image, which reads as texture, not as print.

The screen is rotated (real presses use 45 degrees for single-colour work) so
the dot grid does not moire against the pixel grid.
"""

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageStat

from .config import DIST, STATIC

SOURCE = STATIC / "img"
OUT = DIST / "img"

SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}

# Tuning. CELL is the big one: bigger = coarser, more obviously printed.
CELL = 5          # px per dot cell, measured on the source image
OVERSAMPLE = 4    # dots are drawn at this scale, then shrunk. gives smooth edges.
ANGLE = 45        # screen angle, degrees
CONTRAST = 1.25   # crushed before screening, or midtones turn to mush (1.6 blows out highlights)
GAIN = 1.4        # dot size multiplier. >1 lets dark dots merge, like wet ink.
MAX_WIDTH = 1600  # source photos get resized to this first


def halftone(im: Image.Image) -> Image.Image:
    im = im.convert("L")
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)

    # Rotate into screen space. White fill so the corners we add are paper.
    rot = im.rotate(ANGLE, resample=Image.BICUBIC, expand=True, fillcolor=255)
    w, h = rot.size

    canvas = Image.new("L", (w * OVERSAMPLE, h * OVERSAMPLE), 255)
    draw = ImageDraw.Draw(canvas)

    half = CELL * OVERSAMPLE / 2
    for x in range(0, w, CELL):
        for y in range(0, h, CELL):
            cell = rot.crop((x, y, x + CELL, y + CELL))
            darkness = (255 - ImageStat.Stat(cell).mean[0]) / 255
            # sqrt because a dot's AREA should track darkness, not its radius
            r = (darkness ** 0.5) * half * GAIN
            if r < 0.35:
                continue
            cx = (x + CELL / 2) * OVERSAMPLE
            cy = (y + CELL / 2) * OVERSAMPLE
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=0)

    # Rotate back and cut the original frame out of the middle.
    back = canvas.rotate(-ANGLE, resample=Image.BICUBIC, expand=False, fillcolor=255)
    ow, oh = im.size
    cx, cy = back.size[0] / 2, back.size[1] / 2
    box = (
        int(cx - ow * OVERSAMPLE / 2), int(cy - oh * OVERSAMPLE / 2),
        int(cx + ow * OVERSAMPLE / 2), int(cy + oh * OVERSAMPLE / 2),
    )
    return back.crop(box).resize((ow, oh), Image.LANCZOS)


def process_all() -> int:
    """Screen every photo in static/img/ into dist/img/. Skips work already done."""
    if not SOURCE.exists():
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    done = 0

    for src in sorted(SOURCE.iterdir()):
        if src.suffix.lower() not in SUFFIXES:
            continue

        # A leading underscore means "leave this one alone" — logos, diagrams,
        # anything that a halftone would destroy rather than flatter.
        if src.stem.startswith("_"):
            shutil.copy2(src, OUT / src.name)
            done += 1
            continue

        dest = OUT / (src.stem + ".png")
        if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
            continue

        im = Image.open(src)
        if im.width > MAX_WIDTH:
            im = im.resize(
                (MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS
            )
        halftone(im).save(dest, optimize=True)
        print(f"  screened {src.name} -> img/{dest.name}")
        done += 1

    return done