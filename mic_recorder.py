import pyaudio
import threading
import numpy as np
import atexit

class Recorder(object):
    def __init__(self, rate=4000, chunksize=1024):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    @property
    def stream(self):
        self._stream = self.p.open(format=pyaudio.paInt16,
                                   channels=1,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.chunksize,
                                   stream_callback=self.new_frame)
        return self._stream

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames

    def start(self):
        self.stream.start_stream()

    def pause(self):
        with self.lock:
            self.stop = True
        self.stream.close()

    def unpause(self):
        with self.lock:
            self.stop = False
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()

# Attribution: https://flothesof.github.io/pyqt-microphone-fft-application.html