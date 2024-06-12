from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import numpy as np
import pandas as pd
import polars as pl
from enum import Enum, auto

from bokeh.plotting import figure
from bokeh.embed import json_item
import json


@dataclass
class BaseAxis(ABC):
    """Represents a minimal interface for an axis object."""

    label: str | None = None
    range: tuple[float, float] | None = None


@dataclass
class XAxis(BaseAxis):
    """Represents a minimal interface for an x-axis object."""

    label: str | None = None
    range: tuple[float, float] | None = None

    @classmethod
    def from_data(cls, data: list[float], label: str | None = None):
        return (
            cls(range=(min(data), max(data)))
            if label is None
            else cls(range=(min(data), max(data)), label=label)
        )


@dataclass
class YAxis(BaseAxis):
    """Represents a minimal interface for a y-axis object."""

    label: str | None = None
    range: tuple[float, float] | None = None

    @classmethod
    def from_data(cls, data: list[float], label: str | None = None):
        return (
            cls(range=(min(data), max(data)))
            if label is None
            else cls(range=(min(data), max(data)), label=label)
        )


@dataclass
class BasePlotSeries(ABC):
    """Represents a minimal interface for a plot series object."""

    x: list[float]
    y: list[float]


@dataclass
class ListSeries(BasePlotSeries):
    """Represents a plot series object that can be created from two lists."""

    x: list[float]
    y: list[float]


@dataclass
class DictPlotSeries(BasePlotSeries):
    """Represents a plot series object that can be created from a dictionary."""

    d: dict[str, list[float]]
    x_label: str = "x"
    y_label: str = "y"

    def __post_init__(self):
        self.x = self.d[x_label]
        self.y = self.d[y_label]


@dataclass
class JSONPlotSeries(BasePlotSeries):
    """Represents a plot series object that can be created from a JSON string."""

    json_str: str
    x_label: str = "x"
    y_label: str = "y"

    def __post_init__(self):
        d = json.loads(self.json_str)
        self.x = d[x_label]
        self.y = d[y_label]


@dataclass
class NumpyPlotSeries(BasePlotSeries):
    """Represents a plot series object that can be created from a NumPy array."""

    x: np.ndarray
    y: np.ndarray

    def __post_init__(self):
        self.x = self.x.tolist()
        self.y = self.y.tolist()


@dataclass
class PandasPlotSeries(BasePlotSeries):
    """Represents a plot series object that can be created from a Pandas DataFrame."""

    df: pd.DataFrame
    x_label: str = "x"
    y_label: str = "y"

    def __post_init__(self):
        self.x = self.df[x_label].tolist()
        self.y = self.df[y_label].tolist()


@dataclass
class PolarsPlotSeries(BasePlotSeries):
    """Represents a plot series object that can be created from a Polars DataFrame."""

    df: pl.DataFrame | pl.LazyFrame
    x_label: str = "x"
    y_label: str = "y"

    def __post_init__(self):
        self.x = (
            self.df[x_label].to_numpy().tolist()
            if not isinstance(self.df, pl.LazyFrame)
            else self.df[x_label].collect().to_numpy().tolist()
        )
        self.y = (
            self.df[y_label].to_numpy().tolist()
            if not isinstance(self.df, pl.LazyFrame)
            else self.df[y_label].collect().to_numpy().tolist()
        )


@dataclass
class PlotData:
    """Represents a minimal interface for a plot data object."""

    data: list[BasePlotSeries] | None = None

    def __post_init__(self):
        self.data = []

    def add_series(self, series: BasePlotSeries):
        self.data.append(series)


class MarkerStyle(Enum):
    """Represents the style of marker to use in a plot."""

    CIRCLE = auto()
    SQUARE = auto()
    TRIANGLE = auto()
    NONE = auto()  # for no marker


class LineStyle(Enum):
    """Represents the style of line to use in a plot."""

    SOLID = auto()
    DASHED = auto()
    DOTTED = auto()
    NONE = auto()  # for no line


class Colors(Enum):
    """Represents the style of line to use in a plot."""

    PRIMARY = "black"
    SECONDARY = "red"
    TERTIARY = "blue"
    NONE = "none"


COLOR_MAP = [Colors.PRIMARY.value, Colors.SECONDARY.value, Colors.TERTIARY.value]


@dataclass
class Line:
    """Represents a minimal interface for a line object."""

    line_style: LineStyle = LineStyle.SOLID
    line_color: str = Colors.PRIMARY.value
    line_width: int = 1


@dataclass
class BlankLine(Line):
    """Represents a blank line object."""

    line_style: LineStyle = LineStyle.NONE
    line_color: str = Colors.NONE.value
    line_width: int = 0


@dataclass
class Marker:
    """Represents a minimal interface for a marker object."""

    marker_style: MarkerStyle = MarkerStyle.CIRCLE
    marker_fill_color: str = Colors.PRIMARY.value
    marker_fill_alpha: float = 0.5
    marker_size: int = 10

    marker_outline: Line | None = None

    def __post_init__(self):
        self.marker_outline = BlankLine()

    def outline(
        self,
        outline_style: LineStyle | None = None,
        outline_color: str | None = None,
        outline_width: int | None = None,
    ):
        current = self.marker_outline

        line_style, line_color, line_width = (
            line_style or current.line_style,
            line_color or current.line_color,
            line_width or current.line_width,
        )

        return Line(line_style=line_style, line_color=line_color, line_width=line_width)


@dataclass
class BasePlotOptions(ABC):
    """Represents a minimal interface for a plot options object."""

    title: str | None
    marker: Marker | None
    line: Line | None


@dataclass
class BasePlot(ABC):
    """Represents a minimal interface for a plot object."""

    data: PlotData
    options: BasePlotOptions
    x_axis: XAxis
    y_axis: YAxis

    def __post_init__(self):
        self.data = PlotData()
        self.options = BasePlotOptions(
            title="",
            marker=Marker(),
            line=Line(),
        )


    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def export_to_json(self) -> str:
        pass
