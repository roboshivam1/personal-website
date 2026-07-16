"""Print an issue: content/ + templates/ -> dist/"""

import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

from .images import process_all as screen_images
from .config import DIST, SECTION_BLURB, STATIC
from .issue import issue_number
from .loader import load_all
from .models import Dispatch, Obituary, Project
from .render import make_env

env = make_env()


def write(url_path: str, html: str) -> None:
    """/lab-notes/foo/ -> dist/lab-notes/foo/index.html"""
    out = DIST / url_path.strip("/") / "index.html" if url_path != "/" else DIST / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def build(include_drafts: bool = False) -> int:
    stories = load_all(include_drafts)
    if not stories:
        sys.exit("Nothing to print. Write something in content/.")

    dispatches = [s for s in stories if isinstance(s, Dispatch)]
    projects = [s for s in stories if isinstance(s, Project)]
    obituaries = [s for s in stories if isinstance(s, Obituary)]

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    pages = 0

    # --- front page: a function of weight, not a hand-maintained file ---
    lead, *rest = stories

    # "INSIDE TODAY" — one line per desk, with how much is in it.
    index = Counter(s.section for s in stories)

    write("/", env.get_template("index.html").render(
        path="/", lead=lead, seconds=rest[:4], briefs=rest[4:9],
        bench=sorted(projects, key=lambda p: -p.date.toordinal())[:4],
        index=sorted(index.items()),
        corrections=[s for s in stories if s.correction][:2],
    ))

    # --- one page per story ---
    for s in stories:
        template = {
            Dispatch: "article.html",
            Project: "project.html",
            Obituary: "obituary.html",
        }[type(s)]
        write(s.url, env.get_template(template).render(path=s.url, story=s,
                                                       description=s.dek))
        pages += 1

    # --- section indexes ---
    by_section: dict[str, list] = defaultdict(list)
    for d in dispatches:
        by_section[d.section].append(d)

    for section, items in by_section.items():
        items.sort(key=lambda s: -s.date.toordinal())
        write(f"/{section}/", env.get_template("section.html").render(
            path=f"/{section}/", section=section,
            blurb=SECTION_BLURB.get(section, ""), stories=items,
        ))
        pages += 1

    write("/workshop/", env.get_template("workshop.html").render(
        path="/workshop/",
        stories=sorted(projects, key=lambda p: -p.date.toordinal()),
    ))
    write("/obituaries/", env.get_template("obituaries.html").render(
        path="/obituaries/",
        stories=sorted(obituaries, key=lambda o: -o.died.toordinal()),
    ))
    write("/about/", env.get_template("about.html").render(path="/about/"))
    pages += 3

    # --- archive, grouped into issues ---
    issues: dict[int, list] = defaultdict(list)
    for s in sorted(stories, key=lambda s: -s.date.toordinal()):
        issues[issue_number(s.date)].append(s)
    write("/archive/", env.get_template("archive.html").render(
        path="/archive/", issues=sorted(issues.items(), reverse=True),
    ))
    pages += 1

    # --- feed ---
    feed = env.get_template("rss.xml").render(
        stories=sorted(stories, key=lambda s: -s.date.toordinal())[:20]
    )
    (DIST / "rss.xml").write_text(feed, encoding="utf-8")

    # --- static assets, copied verbatim (img/ is handled separately) ---
    for asset in STATIC.iterdir():
        if asset.name == "img":
            continue
        dest = DIST / asset.name
        shutil.copytree(asset, dest) if asset.is_dir() else shutil.copy2(asset, dest)

    # --- photographs, through the press ---
    screened = screen_images()
    if screened:
        print(f"Screened {screened} photographs")

    return pages

def main() -> None:
    drafts = "--drafts" in sys.argv
    pages = build(include_drafts=drafts)
    print(f"Printed {pages} pages to {DIST.relative_to(Path.cwd())}/"
          + (" (including drafts)" if drafts else ""))


if __name__ == "__main__":
    main()