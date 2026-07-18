#!/usr/bin/env python3
"""Set this issue's crossword.

Edit WORDS below, then:  python3 tools/crossword.py

Writes content/puzzle.yaml — grid coordinates, numbering, and clues. The site
renders that as real HTML cells, so the grid scales, themes, and its numbers are
selectable text. A PNG could do none of those things.

The layout is a greedy criss-cross: place the longest word, then hang each next
word off a shared letter, refusing any placement that would run two words
alongside each other.
"""

from pathlib import Path

import yaml

# ══════════════════════════════════════════════════════════════════════
#  EDIT THIS — one entry per word. The clue is the fun part; take the time.
# ══════════════════════════════════════════════════════════════════════

NUMBER = 1          # puzzle number. bump it each issue.

WORDS = {
    "HALFTONE": "How this paper prints a photograph (8)",
    "OBITUARY": "Where dead projects are filed (8)",
    "JARVIS": "The automation desk's only correspondent (6)",
    "SOLDER": "It joins, when the iron is hot enough (6)",
    "GAZETTE": "This publication, in one word (7)",
    "REDLINE": "A Hot Wheels collector's holy grail, or an engine's limit (7)",
    "MONSOON": "It arrives late and all at once (7)",
    "DEK": "The line under the headline (3)",
    "INK": "What everything here is made of (3)",
}

OUTPUT = "content/puzzle.yaml"

# ══════════════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent


class Setter:
    def __init__(self, clues: dict[str, str]):
        self.clues = {w.upper().replace(" ", ""): c for w, c in clues.items()}
        self.words = sorted(self.clues, key=len, reverse=True)
        self.grid: dict[tuple[int, int], str] = {}
        self.placed: list[dict] = []

    def _can_place(self, word, sx, sy, horizontal) -> bool:
        for i, char in enumerate(word):
            x = sx + (i if horizontal else 0)
            y = sy + (0 if horizontal else i)

            # a different letter already sits here
            if self.grid.get((x, y), char) != char:
                return False

            # nothing may run alongside: check the two flanks of every cell,
            # unless this cell is itself a genuine crossing
            flanks = [(x, y - 1), (x, y + 1)] if horizontal else [(x - 1, y), (x + 1, y)]
            if (x, y) not in self.grid:
                if any(f in self.grid for f in flanks):
                    return False

            # and the word may not butt up against another at either end
            if i == 0:
                before = (sx - 1, sy) if horizontal else (sx, sy - 1)
                if before in self.grid:
                    return False
            if i == len(word) - 1:
                after = (x + 1, y) if horizontal else (x, y + 1)
                if after in self.grid:
                    return False
        return True

    def _write(self, word, sx, sy, horizontal):
        for i, char in enumerate(word):
            self.grid[(sx + (i if horizontal else 0), sy + (0 if horizontal else i))] = char
        self.placed.append({"word": word, "x": sx, "y": sy, "horizontal": horizontal})

    def lay_out(self) -> list[str]:
        """Returns the words it could not place. Silence would be worse."""
        if not self.words:
            return []
        self._write(self.words[0], 0, 0, True)
        unplaced = []

        for word in self.words[1:]:
            placed = False
            for (gx, gy), gchar in list(self.grid.items()):
                if placed:
                    break
                for i, char in enumerate(word):
                    if char != gchar:
                        continue
                    for horizontal in (True, False):
                        sx = gx - (i if horizontal else 0)
                        sy = gy - (0 if horizontal else i)
                        if self._can_place(word, sx, sy, horizontal):
                            self._write(word, sx, sy, horizontal)
                            placed = True
                            break
                    if placed:
                        break
            if not placed:
                unplaced.append(word)
        return unplaced

    def to_data(self) -> dict:
        min_x = min(x for x, _ in self.grid)
        min_y = min(y for _, y in self.grid)

        # standard numbering: reading order, one number per starting cell
        self.placed.sort(key=lambda w: (w["y"], w["x"]))
        numbers: dict[tuple[int, int], int] = {}
        for w in self.placed:
            coord = (w["x"], w["y"])
            if coord not in numbers:
                numbers[coord] = len(numbers) + 1
            w["number"] = numbers[coord]

        cells = [
            {"x": x - min_x, "y": y - min_y, "a": letter,
             **({"n": numbers[(x, y)]} if (x, y) in numbers else {})}
            for (x, y), letter in sorted(self.grid.items(), key=lambda kv: (kv[0][1], kv[0][0]))
        ]

        def clues(horizontal):
            return [{"n": w["number"], "clue": self.clues[w["word"]], "answer": w["word"]}
                    for w in sorted(self.placed, key=lambda w: w["number"])
                    if w["horizontal"] is horizontal]

        return {
            "number": NUMBER,
            "cols": max(x for x, _ in self.grid) - min_x + 1,
            "rows": max(y for _, y in self.grid) - min_y + 1,
            "cells": cells,
            "across": clues(True),
            "down": clues(False),
        }


def main():
    setter = Setter(WORDS)
    unplaced = setter.lay_out()
    data = setter.to_data()

    out = ROOT / OUTPUT
    out.write_text(
        "# GENERATED by tools/crossword.py — edit WORDS in that file, not this one.\n"
        + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    print(f"puzzle no. {data['number']} -> {OUTPUT}")
    print(f"  {data['cols']}x{data['rows']}, {len(data['across'])} across, {len(data['down'])} down")
    if unplaced:
        print(f"  COULD NOT PLACE: {', '.join(unplaced)}")
        print("  (no shared letter, or every crossing would touch another word)")


if __name__ == "__main__":
    main()