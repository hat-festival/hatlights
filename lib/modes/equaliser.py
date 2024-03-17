from lib.mode import Mode
from lib.renderers.sweeper import angle  # TODO rehome this to tools?
from lib.tools import hue_to_rgb, scale_colour
from multiprocessing import Process, Value
from lib.fourier import Fourier
from time import sleep

class Equaliser(Mode):
    """Equalise."""

    def configure(self):
        """Configure ourself."""
        self.decay_amount = 0.05
        self.decay_interval = 0.05

        self.max_y = 1.0
        self.default_y = Value("f", 0.3)
        self.active_y = Value("f", self.default_y.value)

        self.fft = Fourier(self)
        self.fft_proc = Process(target=self.fft.transform)
        self.reducer_proc = Process(target=self.reduce)

        self.hues = []
        for pix in self.hat.pixels:
            pix["angle"] = (angle(pix["x"], pix["z"]) - 90) % 360
            pix["hue"] = pix["angle"] / 360

        self.reducer_proc.start()
        self.fft_proc.start()

    def run(self):
        """Do the sork."""
        self.configure()

        lights = []
        for pixel in self.hat.pixels:
            colour = hue_to_rgb(pixel["hue"])
            if 0.5 < pixel["y"] < 0.6:
                lights.append(colour)
            else:
                lights.append(scale_colour(colour, 0.3))

        while True:
            self.from_list(lights)

    def trigger(self):
        """Spike our `y`. Called by our FFT."""
        self.active_y.value = self.max_y

    def reduce(self):
        """Constantly reducing the `y`."""
        while True:
            if self.active_y.value > self.default_y.value:
                self.active_y -= self.decay_amount
                sleep(self.decay_interval)
            else:
                sleep(1)