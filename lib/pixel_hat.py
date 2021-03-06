import platform

from lib.pixel import Pixel
from lib.scaler import Scaler
from lib.tools import gamma_correct

if "arm" in platform.platform():  # nocov
    import board
    from neopixel import NeoPixel


class PixelHat(list):
    """Hat with pixels."""

    def __init__(
        self, locations="conf/locations.yaml", auto_centre=False
    ):  # pylint: disable=W0231
        self.locations = locations
        self.scaler = Scaler(locations, auto_centre=auto_centre)

        for location in self.scaler:
            self.append(Pixel(location))

        if "arm" in platform.platform():
            self.pixels = NeoPixel(board.D21, len(self), auto_write=False)  # nocov
        else:
            self.pixels = FakePixel(4)

    def light_one(self, index, colour, auto_show=True):
        """Light up a single pixel."""
        self.pixels[index] = gamma_correct(colour)
        if auto_show:
            self.pixels.show()

    def colour_indeces(self, indeces, colour, auto_show=True):
        """Apply a colour to a list of lights."""
        for index in indeces:
            self.pixels[index] = gamma_correct(colour)
        if auto_show:
            self.pixels.show()

    def illuminate(self, colours):
        """Apply a whole list of colours to ourself."""
        for index, colour in enumerate(colours):
            self.light_one(index, colour, auto_show=False)
        self.show()

    def off(self):
        """Turn all the lights off."""
        self.pixels.fill([0, 0, 0])
        self.pixels.show()

    def show(self):
        """Show our lights."""
        self.pixels.show()


class FakePixel(list):
    """Fake NeoPixels for testing."""

    def __init__(self, length):  # pylint: disable=W0231
        """Construct."""
        self.length = length
        for _ in range(self.length):
            self.append((0, 0, 0))

    def fill(self, colour):
        """Pretend to fill the pixels."""
        for index, _ in enumerate(self):
            self[index] = colour

    def show(self):
        """Pretend to show the lights."""
        print(f"Showing lights: {str(self)}")
