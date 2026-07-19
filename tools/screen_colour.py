#!/usr/bin/env python3
"""Put a photograph through a printing press.

Edit the block below, then:  python3 tools/screen.py

NOT part of the build. Screening is a taste decision, done by hand while you look
at the result. Output has the paper baked in — a finished print.

Three modes:
  mono     black ink on paper. the whole paper is this.
  duotone  black + the registration red. a second colour, still newsprint.
  cmyk     four screens at four angles, like a real comic. loud, saturated.

Colour is meant to live ONLY in Motoring and a future comic section.
"""

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageStat

# ══════════════════════════════════════════════════════════════════════
#  EDIT THIS
# ══════════════════════════════════════════════════════════════════════

INPUT = "photos_local/photography/pic15.PNG"           # the original. relative to the project root.
OUTPUT = "static/img/photos2/img15_cmyk.PNG"      # where the finished plate goes.

MODE = "cmyk"        # "mono" | "duotone" | "cmyk"
CONTACT_SHEET = False   # True -> a labelled grid of settings next to OUTPUT.

CELL = 5          # px per dot. 3 = fine, 8 = aggressively printed.
TARGET = 0.66     # average tone, 0..1. HIGHER = LIGHTER. pale subjects ~0.66.
GAIN = 1.4        # dot size multiplier. >1 lets dark dots merge.
CONTRAST = 1.1    # crushed after exposure. lower keeps midtones off black.
MAX_WIDTH = 1600

PAPER = (229, 225, 215)   # --plate-paper in paper.css. keep in step.
INK = (23, 23, 27)        # --ink, daylight edition. the black plate.
SPOT = (179, 18, 43)      # --spot, the registration red. the second plate.

# ══════════════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
OVERSAMPLE = 4
CMYK_ANGLES = {"C": 15, "M": 75, "Y": 0, "K": 45}


def expose(im, target=TARGET, contrast=CONTRAST):
    """Return an INK map: 255 = full ink, 0 = bare paper. `target` is the desired
    average PAPER lightness, so higher target -> less ink -> a lighter print."""
    lum = ImageOps.autocontrast(im.convert("L"), cutoff=1.0)
    lum = ImageEnhance.Contrast(lum).enhance(contrast)
    mean = max(0.02, min(0.98, ImageStat.Stat(lum).mean[0] / 255))
    # solve the gamma that moves this image's mean lightness to `target`.
    # done AFTER the contrast crush so the crush can't undo it.
    g = math.log(target) / math.log(mean)
    lum = lum.point([round(255 * (v / 255) ** g) for v in range(256)])
    return ImageOps.invert(lum)   # lightness -> ink coverage


def _screen(gray, cell, angle, gain):
    """One dot per cell, sized by darkness, on a rotated grid. Returns an 'L'
    coverage map: 255 = full ink, 0 = bare paper."""
    rot = gray.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=0)
    w, h = rot.size
    canvas = Image.new("L", (w * OVERSAMPLE, h * OVERSAMPLE), 0)
    draw = ImageDraw.Draw(canvas)
    half = cell * OVERSAMPLE / 2
    for x in range(0, w, cell):
        for y in range(0, h, cell):
            ink = ImageStat.Stat(rot.crop((x, y, x + cell, y + cell))).mean[0] / 255
            r = (ink ** 0.5) * half * gain
            if r < 0.35:
                continue
            cx, cy = (x + cell / 2) * OVERSAMPLE, (y + cell / 2) * OVERSAMPLE
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    back = canvas.rotate(-angle, resample=Image.BICUBIC, expand=False, fillcolor=0)
    ow, oh = gray.size
    cx, cy = back.size[0] / 2, back.size[1] / 2
    box = (int(cx - ow * OVERSAMPLE / 2), int(cy - oh * OVERSAMPLE / 2),
           int(cx + ow * OVERSAMPLE / 2), int(cy + oh * OVERSAMPLE / 2))
    return back.crop(box).resize((ow, oh), Image.LANCZOS)


def _lay_ink(base, coverage, ink):
    """Paint `ink` onto `base` where `coverage` says so. Multiplicative, so inks
    stack the way overlapping plates do."""
    layer = Image.new("RGB", base.size, ink)
    return Image.composite(ImageChops.multiply(base, layer), base, coverage)


def screen_mono(im, cell=CELL, target=TARGET, gain=GAIN, contrast=CONTRAST):
    cov = _screen(expose(im, target, contrast), cell, 45, gain)
    return _lay_ink(Image.new("RGB", cov.size, PAPER), cov, INK)


def screen_duotone(im, cell=CELL, target=TARGET, gain=GAIN, contrast=CONTRAST):
    """Black plate carries tone; red plate carries only the reddest parts."""
    out = Image.new("RGB", im.size, PAPER)
    black_cov = _screen(expose(im, target, contrast), cell, 45, gain)
    r, g, b = im.convert("RGB").split()
    redness = ImageChops.subtract(r, ImageChops.lighter(g, b))
    red_cov = _screen(ImageOps.autocontrast(redness, cutoff=2), cell, 15, gain)
    out = _lay_ink(out, red_cov, SPOT)
    out = _lay_ink(out, black_cov, INK)
    return out


def screen_cmyk(im, cell=CELL, gain=GAIN):
    """Four plates, four angles. Real comic-book printing."""
    out = Image.new("RGB", im.size, PAPER)
    inks = {"C": (0, 160, 220), "M": (210, 20, 120), "Y": (250, 210, 0), "K": INK}
    for ch, chan in zip("CMYK", im.convert("CMYK").split()):
        cov = _screen(chan, cell, CMYK_ANGLES[ch], gain)
        out = _lay_ink(out, cov, inks[ch])
    return out


def screen(im, mode=None, **kw):
    mode = mode or MODE
    if mode == "mono":
        return screen_mono(im, **kw)
    if mode == "duotone":
        return screen_duotone(im, **kw)
    if mode == "cmyk":
        return screen_cmyk(im, cell=kw.get("cell", CELL), gain=kw.get("gain", GAIN))
    raise SystemExit(f"unknown MODE {mode!r} — use mono, duotone, or cmyk")


def load(path, max_width=MAX_WIDTH):
    im = Image.open(path).convert("RGB")
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    return im


def contact_sheet(src):
    thumb = load(src, 420)
    tiles = []
    for cell in (3, 5, 8):
        for target in (0.52, 0.62, 0.72):
            tile = screen(thumb, cell=cell, target=target)
            label = f"CELL {cell}  TARGET {target}"
            d = ImageDraw.Draw(tile)
            d.rectangle((0, 0, 10 + 6 * len(label), 18), fill=INK)
            d.text((4, 4), label, fill=PAPER, font=ImageFont.load_default())
            tiles.append(tile)
    tw, th = tiles[0].size
    sheet = Image.new("RGB", (tw * 3 + 40, th * 3 + 40), PAPER)
    for i, t in enumerate(tiles):
        sheet.paste(t, (10 + (i % 3) * (tw + 10), 10 + (i // 3) * (th + 10)))
    return sheet


def main():
    src = ROOT / INPUT
    if not src.exists():
        raise SystemExit(f"No such photo: {src}\nEdit INPUT at the top of this file.")
    if CONTACT_SHEET:
        out = (ROOT / OUTPUT).with_name(Path(OUTPUT).stem + "-contact.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        contact_sheet(src).save(out)
        print(f"contact sheet ({MODE}) -> {out.relative_to(ROOT)}")
        print("open it, pick a tile, copy CELL/TARGET, set CONTACT_SHEET = False, run again")
        return
    out = ROOT / OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    screen(load(src)).save(out, optimize=True)
    print(f"screened {INPUT} ({MODE}) -> {OUTPUT}   (CELL {CELL}, TARGET {TARGET})")


if __name__ == "__main__":
    main()