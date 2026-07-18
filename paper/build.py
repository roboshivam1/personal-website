"""Print an issue: content/ + templates/ -> dist/"""

import shutil
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from .config import DIST, PICK_DESKS, SECTION_BLURB, STATIC
from .issue import issue_number
from .loader import (load_all, load_cars, load_cartoons, load_photographs,
                     load_picks, load_puzzle)
from .models import Dispatch, Obituary, Project
from .render import make_env
from .ticker import load_ticker

env = make_env()


def write(url_path: str, html: str) -> None:
    """/lab-notes/foo/ -> dist/lab-notes/foo/index.html"""
    out = DIST / url_path.strip("/") / "index.html" if url_path != "/" else DIST / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def build(include_drafts: bool = False) -> int:
    stories = load_all(include_drafts)
    cars = load_cars()
    ticker = load_ticker()
    photographs = load_photographs()
    picks = load_picks()
    puzzle = load_puzzle()
    cartoons = load_cartoons()
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
    # --- the front page is a series of slots, each taking from what is left ---
    lead, *rest = stories

    # Column One: the left-hand feature. Marked by hand, or failing that the
    # heaviest opinion/notes piece — it is deliberately not the news.
    one = next((s for s in rest if s.column_one), None)
    if one is None:
        one = next((s for s in rest if s.section in ("op-ed", "lab-notes")), None)

    bench = sorted(projects, key=lambda p: -p.date.toordinal())[:4]

    # Car of the issue: rotates on its own with the issue number, so it is never
    # stale and never needs remembering. Oldest-first so a new car goes to the
    # back of the queue rather than jumping it.
    car = None
    if cars:
        queue = sorted(cars, key=lambda c: c.acquired)
        car = queue[issue_number(date.today()) % len(queue)]

    # Photograph of the issue. Offset by a third of the run so it does not
    # advance in lockstep with the car — two dials turning together read as one.
    photo = None
    if photographs:
        n = issue_number(date.today()) + len(photographs) // 3
        photo = photographs[n % len(photographs)]

    # The standing recommendation. Only starred picks are eligible, so the rail
    # never leads with something the editor merely tolerates.
    pick = None
    starred = [p for p in picks if p.star] or picks
    if starred:
        pick = starred[(issue_number(date.today()) * 2) % len(starred)]

    cartoon = cartoons[issue_number(date.today()) % len(cartoons)] if cartoons else None

    # Every slot claims its stories, and later slots cannot re-use them. A page
    # that prints the same item in two places has an editor who is not reading it.
    taken = {lead.url} | {b.url for b in bench} | ({one.url} if one else set())
    seconds = [s for s in rest if s.url not in taken][:3]
    taken |= {s.url for s in seconds}
    briefs = [s for s in rest if s.url not in taken][:5]

    # "INSIDE TODAY" — one line per desk, with how much is in it.
    index = Counter(s.section for s in stories)

    write("/", env.get_template("index.html").render(
        path="/", lead=lead, one=one, seconds=seconds, briefs=briefs,
        bench=bench, car=car, ticker=ticker, photo=photo,
        pick=pick, pick_desks=PICK_DESKS, puzzle=puzzle, cartoon=cartoon,
        index=sorted(index.items()),
        corrections=[s for s in stories if s.correction][:2],
    ))
    pages += 1

    # Reverse index: for each project slug, the dispatches that declared
    # `about: <slug>`. The connection is authored once on the dispatch; the
    # project page reads it back here, so the two sides can never disagree.
    related: dict[str, list] = defaultdict(list)
    for d in dispatches:
        if d.about:
            related[d.about].append(d)
    for slug in related:
        related[slug].sort(key=lambda d: -d.date.toordinal())

    # A dispatch that names a project it doesn't point at is almost always a
    # typo in `about:` — surface it rather than silently linking nothing.
    project_slugs = {p.slug for p in projects}
    for d in dispatches:
        if d.about and d.about not in project_slugs:
            print(f"  note: {d.slug} is 'about' {d.about!r}, which is not a workshop project")

    # --- one page per story ---
    for s in stories:
        template = {
            Dispatch: "article.html",
            Project: "project.html",
            Obituary: "obituary.html",
        }[type(s)]
        extra = {"related": related.get(s.slug, [])} if isinstance(s, Project) else {}
        write(s.url, env.get_template(template).render(path=s.url, story=s,
                                                       description=s.dek, **extra))
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

    if cars:
        # ARRIVALS: how many cars came in, by year. Real papers printed shipping
        # arrivals as a table exactly like this. Counts, not names — with 70 cars
        # a list of names in a rail is a wall; a bar chart is a glance.
        by_year = Counter(c.acquired.year for c in cars)
        peak = max(by_year.values())
        arrivals = [(y, n, round(100 * n / peak)) for y, n in sorted(by_year.items(), reverse=True)]
        write("/motoring/", env.get_template("motoring.html").render(
            path="/motoring/", cars=cars, arrivals=arrivals,
        ))
        pages += 1

    if photographs:
        write("/photography/", env.get_template("photography.html").render(
            path="/photography/", photographs=photographs,
        ))
        pages += 1

    if picks:
        # An arts page leads with one review and lists the rest. Without a lead
        # everything is the same size and nothing is a page.
        review = next((p for p in picks if p.star), picks[0])
        rest_picks = [p for p in picks if p is not review]
        desks = [(kind, label, [p for p in rest_picks if p.kind == kind])
                 for kind, label in PICK_DESKS.items()]
        write("/culture/", env.get_template("culture.html").render(
            path="/culture/", review=review, desks=[d for d in desks if d[2]],
            picks=picks, pick_desks=PICK_DESKS,
        ))
        pages += 1

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

    # --- static assets, copied verbatim. photographs included: they arrive
    #     already screened by tools/screen.py, so the build never touches them.
    for asset in STATIC.iterdir():
        dest = DIST / asset.name
        shutil.copytree(asset, dest) if asset.is_dir() else shutil.copy2(asset, dest)

    return pages


def main() -> None:
    drafts = "--drafts" in sys.argv
    pages = build(include_drafts=drafts)
    print(f"Printed {pages} pages to {DIST.relative_to(Path.cwd())}/"
          + (" (including drafts)" if drafts else ""))


if __name__ == "__main__":
    main()