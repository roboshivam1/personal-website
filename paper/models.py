from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Story(BaseModel):
    """Fields every desk shares. Never instantiated directly."""

    model_config = ConfigDict(extra="forbid")

    title: str
    dek: str | None = None
    date: date
    weight: int = 10
    hero: str | None = None
    tags: list[str] = Field(default_factory=list)
    draft: bool = False

    # Filled in by the loader, not by frontmatter.
    slug: str = ""
    body: str = ""

    @property
    def url(self) -> str:
        return f"/{self.section}/{self.slug}/"


class Dispatch(Story):
    """Writing. The section becomes the URL prefix."""

    section: Literal["software", "op-ed", "lab-notes"] = "lab-notes"


class Project(Story):
    """Things on the bench."""

    section: Literal["workshop"] = "workshop"
    status: Literal["live", "in progress", "shelved", "shipped"] = "in progress"
    stack: list[str] = Field(default_factory=list)
    link: str | None = None


class Obituary(Story):
    """Things that died. The schema will not let you be vague about why."""

    section: Literal["obituaries"] = "obituaries"
    born: date
    died: date
    cause_of_death: str
    