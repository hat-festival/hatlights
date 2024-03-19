from lib.colour_normaliser import ColourNormaliser
from lib.conf import conf
from lib.scaler import Scaler
from lib.tools import angle_to_point, hue_to_rgb, is_pi

if is_pi():  # nocov
    import board
    from neopixel import NeoPixel


class Hat:
    """Hat with pixels."""

    def __init__(self, locations="conf/locations.yaml", auto_centre=False):  # noqa: FBT002
        """Construct."""
        self.conf = conf
        self.locations = locations
        self.scaler = Scaler(locations, auto_centre=auto_centre)
        self.pixels = self.scaler.as_pixels()
        self.normaliser = ColourNormaliser()

        if is_pi():
            self.lights = NeoPixel(
                board.D21, len(self.pixels), auto_write=False
            )  # nocov
        else:
            self.lights = FakeLights(len(self.pixels))

        self.restart_normaliser()

    def restart_normaliser(self):
        """Restart the normaliser."""
        if is_pi():
            self.normaliser.run()

    def light_one(self, index, colour, auto_show=True):  # noqa: FBT002
        """Light up a single pixel."""
        self.lights[index] = self.normaliser.normalise(colour)

        if auto_show:
            self.show()

    def colour_indeces(self, indeces, colour, auto_show=True):  # noqa: FBT002
        """Apply a colour to a list of lights."""
        for index in indeces:
            self.lights[index] = self.normaliser.normalise(colour)

        if auto_show:
            self.show()

    def sort(self, axis):
        """Sort our pixels along an axis."""
        self.pixels.sort(key=lambda w: w[axis])

    def fill(self, colour):
        """Fill every light with a colour."""
        for index in range(len(self.lights)):
            self.light_one(index, colour, auto_show=False)
        self.show()

    def illuminate(self, colours):
        """Apply a whole list of colours to ourself."""
        for index, colour in enumerate(colours):
            self.light_one(self.pixels[index]["index"], colour, auto_show=False)
        self.show()

    def off(self):
        """Turn all the lights off."""
        self.lights.fill((0, 0, 0))
        self.lights.show()

    def show(self):
        """Show our lights."""
        self.lights.show()

    @property
    def length(self):
        """How long are we."""
        return len(self.pixels)

    def __len__(self):
        """Support `len()`."""
        return self.length

    def reverse(self):
        """Turn ourself around."""
        self.pixels.reverse()

    # TODO: break these up so we can selectively apply, but have
    # "hues from angles" check for angles first etc
    def apply_angles(self, axis_0, axis_1, rotation=0):
        """Apply angles to pixels."""
        for pixel in self.pixels:
            pixel["angle"] = (
                angle_to_point(pixel[axis_0], pixel[axis_1]) - rotation
            ) % 360

    def hues_from_angles(self, axis_0, axis_1, rotation=0):
        """Assign hues from pixel angles."""
        self.apply_angles(axis_0, axis_1, rotation=rotation)
        for pixel in self.pixels:
            pixel["hue"] = pixel["angle"] / 360

    def rgbs_from_angles(self, axis_0, axis_1, rotation=0):
        """Assign rgbs from pixel angles."""
        self.hues_from_angles(axis_0, axis_1, rotation=rotation)
        for pixel in self.pixels:
            pixel["rgb"] = hue_to_rgb(pixel["hue"])

    def light_up(self):
        """Light ourselves up based on our RGBs."""
        for index, pixel in enumerate(self.pixels):
            self.lights[index] = pixel["rgb"]
        self.lights.show()


class FakeLights(list):
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
        # print(f"Showing lights: {str(self)}")
