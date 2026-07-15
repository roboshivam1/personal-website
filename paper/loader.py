import sys
from pathlib import Path

import frontmatter
from pydantic import ValidationError

from .config import CONTENT
from .models import Dispatch, Obituary, Project, Story

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