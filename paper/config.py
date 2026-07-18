from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
DIST = ROOT / "dist"

SITE = {
    "name": "The Basement Gazette",
    "motto": "software · hardware · things half-built",
    "city": "Jaipur",
    "established": 2026,
    "url": "https://shvmkpr.in",
    "author": "Shivam",
    "description": (
        "The personal paper of Shivam — developer, maker, and tech consultant in "
        "Jaipur. Projects, essays, lab notes, and the occasional obituary."
    ),
    "first_issue": date(2026, 7, 1),
    # --- front page furniture. placeholders: replace with real values. ---
    "price": "Free",
    "edition": "★★★ Late Edition",
    "circulation": 11,          # be honest. it is funnier honest.
    # The markets desk. symbol is a 4-letter ticker; repo is owner/name.
    # Placeholder repos — swap in your own.
    "repos": [
        {"symbol": "JRVS", "repo": "pallets/jinja"},
        {"symbol": "EBIK", "repo": "python-pillow/Pillow"},
        {"symbol": "VDYT", "repo": "pydantic/pydantic"},
        {"symbol": "SQON", "repo": "python-markdown/markdown"},
    ],
    "weather": {                # placeholder — a build-time fetch can fill this later
        "summary": "Hazy, hot",
        "high": 39,
        "low": 28,
    },
    "nav": [
        ("Front page", "/"),
        ("Workshop", "/workshop/"),
        ("Motoring", "/motoring/"),
        ("Pictures", "/photography/"),
        ("Lab notes", "/lab-notes/"),
        ("Op-ed", "/op-ed/"),
        ("Obituaries", "/obituaries/"),
        ("Archive", "/archive/"),
        ("About", "/about/"),
    ],
}

# The culture desks. Deliberately absent from SITE["nav"] — this is a colophon,
# not a desk that files weekly. It is reached from About, and from the standing
# recommendation in the front-page rail.
PICK_DESKS = {
    "film": "At the pictures",
    "book": "On the shelf",
    "record": "The workshop playlist",
}

SECTION_BLURB = {
    "lab-notes": "Short. Unfinished. Written the same day the thing happened.",
    "op-ed": "Opinions, held loosely, argued firmly. The section where being wrong in public is the point.",
    "software": "Longer pieces on systems I have built and the parts that fought back.",
}