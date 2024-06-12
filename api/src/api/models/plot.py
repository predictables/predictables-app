from __future__ import annotations
from pydantic import BaseModel


class PlotRequest(BaseModel):
    """Represent the data passed as part of a request to the plotting service."""

    x: list[float]
    y: list[float]
    plot_title: str | None = None


class PlotResponse(BaseModel):
    """Represent the JSON response returned from the plotting service."""

    script: str
    script_tag: str
    plot_title: str
