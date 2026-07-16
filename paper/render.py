from datetime import date, datetime, timezone
from email.utils import format_datetime

import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape

from .config import SITE, TEMPLATES
from .issue import issue_number, long_date, short_date

_md = markdown.Markdown(extensions=["extra", "smarty", "sane_lists"])


def render_markdown(text: str) -> Markup:
    """Markdown -> HTML. Marked safe, so autoescape leaves it alone."""
    _md.reset()
    return Markup(_md.convert(text))

def dateline(html: Markup, place: str) -> Markup:
    """Slip a wire-service dateline into the first paragraph.

    Markdown gives us '<p>The first version...'. A real paper opens body copy
    with the place it was filed from, so we splice it into that first <p>
    rather than making the author type it into every file.
    """
    tag = f'<p><span class="dateline">{escape(place)} &mdash;</span> '
    # str() first: Markup.replace() would escape the tag we are trying to insert
    return Markup(str(html).replace("<p>", tag, 1))

def rfc822(d: date) -> str:
    """RSS insists on this date format and will not be reasoned with."""
    return format_datetime(datetime(d.year, d.month, d.day, tzinfo=timezone.utc))


def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["markdown"] = render_markdown
    env.filters["long_date"] = long_date
    env.filters["short_date"] = short_date
    env.filters["rfc822"] = rfc822
    env.globals["SITE"] = SITE
    env.globals["issue_number"] = issue_number
    env.globals["today"] = date.today()
    env.globals["path"] = None
    env.filters["dateline"] = dateline
    return env