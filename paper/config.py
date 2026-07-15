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
    "nav": [
        ("Front page", "/"),
        ("Workshop", "/workshop/"),
        ("Lab notes", "/lab-notes/"),
        ("Op-ed", "/op-ed/"),
        ("Obituaries", "/obituaries/"),
        ("Archive", "/archive/"),
        ("About", "/about/"),
    ],
}

SECTION_BLURB = {
    "lab-notes": "Short. Unfinished. Written the same day the thing happened.",
    "op-ed": "Opinions, held loosely, argued firmly. The section where being wrong in public is the point.",
    "software": "Longer pieces on systems I have built and the parts that fought back.",
}