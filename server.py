import mesa

from agents import *
from model import StreetView


def street_portrayal(agent):
    if agent is None:
        return

    portrayal = {}


    if type(agent) is Buildings:
        portrayal["Color"] = ["#0390fc", "#0390fc", "#0390fc"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is ParkingSpots:
        portrayal["Color"] = ["#fcf803", "#fcf803", "#fcf803"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is RoundAbout:
        portrayal["Color"] = ["#5e2a03", "#5e2a03", "#5e2a03"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is Stop:
        portrayal["Color"] = ["#ff0000", "#ff0000", "#ff0000"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is Go:
        portrayal["Color"] = ["#0ecf15", "#0ecf15", "#0ecf15"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is Car:
        portrayal["Color"] = ["#000", "#000", "#000"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(street_portrayal, 25, 25, 600, 600)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Buildings", "Color": "#0390fc"},
        {"Label": "ParkingSpots", "Color": "#fcf803"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("- Parameters -"),
    "buildings": mesa.visualization.StaticText("Buildings (Blue)"),
    "parkingSpots": mesa.visualization.StaticText("Parking Spots (Yellow)"),
}

server = mesa.visualization.ModularServer(
    StreetView, [canvas_element, chart_element], "Street Mesa Simulation", model_params
)
server.port = 8521
