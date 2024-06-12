from dataclasses import dataclass

from .base_plot import (
    BasePlot,
    XAxis,
    YAxis,
    PlotData,
    BasePlotOptions,
    Marker,
    Line,
    MarkerStyle,
    LineStyle,
    Colors,
    BlankLine,
)

from .base_plot import ListSeries

from bokeh.plotting import figure
from bokeh.resources import INLINE, Resources
from bokeh.embed import json_item, autoload_static
import json


@dataclass
class ScatterPlotOptions(BasePlotOptions):
    """Represents the options for a scatter plot."""

    marker: Marker | None = None
    line: Line | None = None

    def __post_init__(self):
        self.marker = Marker(
            marker_style=MarkerStyle.CIRCLE,
            marker_fill_color=Colors.PRIMARY.value,
            marker_fill_alpha=0.5,
            marker_size=6,
            marker_outline=BlankLine(),
        )
        self.line = BlankLine()

    def marker_style(self, marker_style: MarkerStyle):
        self.marker.marker_style = marker_style
        return self



@dataclass
class ScatterPlot(BasePlot):
    """Represents a scatter plot."""

    data: PlotData
    options: ScatterPlotOptions
    x_axis: XAxis
    y_axis: YAxis

    def __post_init__(self):
        super().__post_init__()
        self.x_axis = XAxis('x')
        self.y_axis = YAxis('y')

    def plot(self) -> figure:
        p = figure(
            title=self.options.title if self.options.title is not None else None,
            x_axis_label=self.x_axis.label if self.x_axis.label is not None else "x",
            y_axis_label=self.y_axis.label if self.y_axis.label is not None else "y",
        )

        for i, series in enumerate(self.data.data):
            p.circle(
                series.x,
                series.y,
                fill_color=self.options.marker.marker_fill_color,
                fill_alpha=self.options.marker.marker_fill_alpha,
                size=self.options.marker.marker_size,
                line_color=self.options.marker.marker_outline.line_color,
                line_width=self.options.marker.marker_outline.line_width,
            )

        return p

    def export_to_json(self) -> (str, str):
        # return json.dumps(json_item(self.plot()))

        return autoload_static(self.plot(), Resources(mode="inline"), ".")


class SampleScatterPlot(ScatterPlot):
    """Represents a sample scatter plot for testing purposes."""

    def __init__(self):
        x = [1, 2, 3, 4, 5]
        y = [5, 4, 3, 2, 1]
        data = PlotData()
        data.add_series(ListSeries(x, y))

        x_axis = XAxis("Sample x-axis")
        y_axis = YAxis("Sample y-axis")
        options = ScatterPlotOptions(title="Sample Scatter Plot (for Testing)")

        super().__init__(data, x_axis, y_axis, options)
