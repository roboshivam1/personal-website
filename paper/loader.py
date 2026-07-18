import sys
from pathlib import Path

import frontmatter
import yaml
from pydantic import ValidationError

from .config import CONTENT
from .models import (Car, Cartoon, Dispatch, Obituary, Photograph, Pick, Project,
                     Puzzle, Story)

DESKS: dict[str, type[Story]] = {
    "dispatches": Dispatch,
    "workshop": Project,
    "obituaries": Obituary,
}


class ContentError(Exception):
    """A file the press refuses to set."""


def load_file(path: Path, model: type[Story]) -> Story:
    post = frontmatter.load(path)
    try:
        return model(**post.metadata, slug=path.stem, body=post.content)
    except ValidationError as e:
        raise ContentError(f"{path.relative_to(CONTENT)}\n{e}") from e


def load_desk(desk: str) -> list[Story]:
    model = DESKS[desk]
    files = sorted((CONTENT / desk).glob("*.md"))
    return [load_file(p, model) for p in files]


def load_all(include_drafts: bool = False) -> list[Story]:
    """Every story from every desk, heaviest and newest first."""
    stories: list[Story] = []
    errors: list[str] = []

    for desk in DESKS:
        for path in sorted((CONTENT / desk).glob("*.md")):
            try:
                stories.append(load_file(path, DESKS[desk]))
            except ContentError as e:
                errors.append(str(e))

    if errors:
        print("\n--- the press refuses to set these ---\n", file=sys.stderr)
        for e in errors:
            print(e + "\n", file=sys.stderr)
        raise SystemExit(1)

    if not include_drafts:
        stories = [s for s in stories if not s.draft]

    seen: dict[str, Story] = {}
    for s in stories:
        if s.url in seen:
            raise SystemExit(f"Two stories claim {s.url}: {seen[s.url].slug}, {s.slug}")
        seen[s.url] = s

    stories.sort(key=lambda s: (-s.weight, -s.date.toordinal()))
    return stories


def load_cars() -> list[Car]:
    """The collection, newest arrival first."""
    path = CONTENT / "motoring.yaml"
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    try:
        cars = [Car(**c) for c in raw]
    except ValidationError as e:
        raise SystemExit(f"motoring.yaml\n{e}") from e
    return sorted(cars, key=lambda c: c.acquired, reverse=True)


def load_photographs() -> list[Photograph]:
    """The picture desk, in the order written. File order IS running order."""
    path = CONTENT / "photography.yaml"
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    try:
        return [Photograph(**p) for p in raw]
    except ValidationError as e:
        raise SystemExit(f"photography.yaml\n{e}") from e


def load_picks() -> list[Pick]:
    """The editor's picks, in the order written."""
    path = CONTENT / "culture.yaml"
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    try:
        return [Pick(**p) for p in raw]
    except ValidationError as e:
        raise SystemExit(f"culture.yaml\n{e}") from e


def load_puzzle() -> Puzzle | None:
    """This issue's crossword. Generated — see tools/crossword.py."""
    path = CONTENT / "puzzle.yaml"
    if not path.exists():
        return None
    try:
        return Puzzle(**yaml.safe_load(path.read_text(encoding="utf-8")))
    except ValidationError as e:
        raise SystemExit(f"puzzle.yaml (regenerate it: python3 tools/crossword.py)\n{e}") from e


def load_cartoons() -> list[Cartoon]:
    path = CONTENT / "cartoons.yaml"
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    try:
        return [Cartoon(**c) for c in raw]
    except ValidationError as e:
        raise SystemExit(f"cartoons.yaml\n{e}") from e