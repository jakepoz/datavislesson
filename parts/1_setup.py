# Learning to visualize audio
# Mr. Poznanski == Poz - nan - ski == Pause - NaN - Ski

# We are going to use PySimpleGUI to draw some graphs
# (I tried matplotlib but it was too slow)

import numpy as np
import PySimpleGUI as sg
import pyaudio

sg.theme("BluePurple")

layout = [
    [sg.Graph(canvas_size=(500,300),
              graph_bottom_left=(0, 0),
              graph_top_right=(1,1), key="graph")],
]

window = sg.Window("Visualization", layout, finalize=True)
graph = window["graph"]

while True:
    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        break

window.close()

