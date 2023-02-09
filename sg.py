import time
import random
import PySimpleGUI as sg
import pyaudio
import numpy as np

sg.theme("BluePurple")

FFT_BINS = 200

# Make a simple window to show our stuff
layout = [
    [sg.Graph(canvas_size=(500,500),
              graph_bottom_left=(0, 0),
              graph_top_right=(1,1), key="graph")],
    [sg.Graph(canvas_size=(500,500),
              graph_bottom_left=(0, 0),
              graph_top_right=(FFT_BINS,1), key="bars")],
]

window = sg.Window("visualization", layout, finalize=True)
graph = window["graph"]
bars = window["bars"]

# Setup the microphone
CHUNK = 1000  # signal is split into CHUNK number of frames
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # (sampling rate) number of frames per second
AMPLITUDE = 2 ** 16 / 2

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Run the GUI event loop
while True:
    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        break

    # Update the graph itself form the audio signal
    raw = stream.read(CHUNK, exception_on_overflow=False)

    start = time.perf_counter()
    data = np.frombuffer(raw, dtype=np.int16)
    data = data.astype(np.float32) / 65535.0
    graph.erase()

    points = []

    for x, y in enumerate(data):
        points.append((x / CHUNK,y + 0.5))

    graph.draw_lines(points, color="red", width=1)

    fft = np.fft.rfft(data, FFT_BINS)
    fft = np.abs(fft) * 0.1

    freqs = np.fft.rfftfreq(FFT_BINS, 1.0/RATE)

    bars.erase()

    peak_bin = 0
    peak_value = 0

    for i in range(1, FFT_BINS // 2):
        bars.draw_rectangle((i * 2, 0.0), ((i + 1) * 2, fft[i]), fill_color="green", line_width=0)

        if fft[i] > peak_value:
            peak_value = fft[i]
            peak_bin = i

    # Identify the peak and write it out as a label
    bars.draw_point((peak_bin * 2 + 0.5, peak_value), size=1, color="black")
    bars.draw_text(f"Peak = {freqs[peak_bin]}", location=(100, 0.7), font="Arial 50", color="black")

    print(f"Took {(time.perf_counter() - start)*1000}ms")

stream.close()
window.close()