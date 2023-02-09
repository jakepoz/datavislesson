# Learning to visualize audio
# Mr. Poznanski == Poz - nan - ski == Pause - NaN - Ski

# Now, we are going to draw the waveform as a graph

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

# Setup the microphone
RATE = 44100  # (sampling rate) number of frames per second
CHANNELS = 1
CHUNK = 1000  # signal is split into CHUNK number of frames
FORMAT = pyaudio.paInt16

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while True:
    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        break

    raw = stream.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(raw, dtype=np.int16)
    data = data.astype(np.float32) / 65535.0

    graph.erase()
    points = []

    for x, y in enumerate(data):
        points.append((x / CHUNK, y * 2 + 0.5))

    graph.draw_lines(points, color="red", width=1)


stream.close()
window.close()

