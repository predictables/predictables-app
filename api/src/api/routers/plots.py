from fastapi import APIRouter
from api.models.plot import PlotRequest, PlotResponse
from bokeh.plotting import figure


router = APIRouter(
    prefix="/plots",
    tags=["plots"],
    responses={404: {"description": "Not found"}},
)
