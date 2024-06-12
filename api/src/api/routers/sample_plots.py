from fastapi import APIRouter
from api.models.plot import PlotRequest, PlotResponse
from bokeh.plotting import figure

from plots.base.scatter import SampleScatterPlot

router = APIRouter(
    prefix="/sample-plots",
    tags=["plots"],
    responses={404: {"description": "Not found"}},
)


@router.get("/scatter", response_model=PlotResponse)
async def create_scatter_plot() -> PlotResponse:
    """Create a sample scatter plot."""
    plot = SampleScatterPlot()
    script, script_tag = plot.export_to_json()
    return PlotResponse(script=script, script_tag=script_tag, plot_title=plot.options.title)