from datetime import date, timedelta

from .config import SITE

FORTNIGHT = timedelta(days=14)


def issue_number(d: date) -> int:
    """Issues advance one per fortnight since the first issue."""
    return max(1, (d - SITE["first_issue"]) // FORTNIGHT + 1)


_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]
_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def long_date(d: date) -> str:
    return f"{_DAYS[d.weekday()]}, {d.day} {_MONTHS[d.month - 1]} {d.year}"


def short_date(d: date) -> str:
    return f"{d.day} {_MONTHS[d.month - 1][:3]} {d.year}"


def month_year(d: date) -> str:
    return f"{_MONTHS[d.month - 1]} {d.year}"