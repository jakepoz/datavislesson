import numpy as np
import pyaudio
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], '-r')


CHUNK = 1024  # signal is split into CHUNK number of frames
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # (sampling rate) number of frames per second
AMPLITUDE = 2 ** 16 / 2

DISPLAY_TIME = 1.0

xdata = np.arange(0.0, 1.0, 1.0 / (RATE * DISPLAY_TIME))
ydata = np.repeat(0.0, len(xdata))
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def init():
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    start = time.perf_counter()

    global ydata
    data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
    ydata = np.roll(ydata, -CHUNK)
    ydata[-CHUNK:] = (data.astype(np.float32) / 65535.0)

    ln.set_data(xdata, ydata)

    print(time.perf_counter() - start)

    return ln,

ani = FuncAnimation(fig, update, interval=33,
                    init_func=init, blit=True)
plt.show()