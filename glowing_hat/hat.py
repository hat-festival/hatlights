import platform

from glowing_hat.brightness_controllers.brightness_control import BrightnessControl
from glowing_hat.conf import conf
from glowing_hat.pixel import Pixel
from glowing_hat.tools.scaler import Scaler
from glowing_hat.tools.utils import is_pi, rgb_from_hsv

if is_pi():  # nocov
    import board
    from neopixel import NeoPixel


# TODO: sort_by sets the default axis, which then sets the current "angle" on the pixels
# TODO: `apply_thing_to_one_pixel()`?


class Hat:
    """A list of Pixels."""

    def __init__(self, locations=None):
        """Construct."""
        if not locations:
            locations = f"conf/{platform.node()}/locations.yaml"

        self.pixels = list(map(Pixel, Scaler(locations)))

        if is_pi():
            self.lights = NeoPixel(
                getattr(board, f"D{conf['data-pin']}"),
                len(self.pixels),
                auto_write=False,
            )  # nocov
            self.brightness_control = BrightnessControl()

        else:
            self.lights = FakeLights(len(self.pixels))
            self.brightness_control = FakeBrightnessControl()

    def light_up(self):
        """Light up our lights."""
        for pixel in self.pixels:
            self.lights[pixel["index"]] = rgb_for(
                pixel, self.brightness_control.factor.value
            )
        self.show()

    def light_one(self, pixel):
        """Light up one pixel."""
        self.lights[pixel["index"]] = rgb_for(
            pixel, self.brightness_control.factor.value
        )

    def show(self):
        """Light all our lights."""
        self.lights.show()

    def sort(self, axis):
        """Sort our pixels along an axis."""
        self.pixels.sort(key=lambda w: w[axis])

    # TODO: needs a proper name
    def sort_plain(self):
        """Sort by our indeces."""
        self.pixels.sort(key=lambda x: x["index"])

    def sort_by_indeces(self, indeces):
        """Sort by some arbitrary indeces."""
        self.pixels = [
            next(filter(lambda x: x["index"] == index, self.pixels))
            for index in indeces
        ]

    # TODO: naming might get a bit unwieldy here
    def apply_list(self, data, key):
        """Apply a list of `key` to our pixels."""
        for index, pixel in enumerate(self.pixels):
            pixel[key] = data[index]

    def apply_hues(self, hues):
        """Apply a list of hues to our pixels."""
        self.apply_list(hues, "hue")

    def apply_values(self, values):
        """Apply a list of values to our pixels."""
        self.apply_list(values, "value")

    def update_hues_from_angles(self, offset=0):
        """Update hues given an offset."""
        for pixel in self.pixels:
            pixel.hue_from_angle(offset=offset)

    ###

    def apply_singular_thing(self, singular, key):
        """Apply one `whatever` to all pixels."""
        for pixel in self.pixels:
            pixel[key] = singular

    def apply_hue(self, hue):
        """Apply one `hue` to all pixels."""
        self.apply_singular_thing(hue, "hue")

    def apply_value(self, value):
        """Apply one `value` to all pixels."""
        self.apply_singular_thing(value, "value")

    def apply_saturation(self, saturation):
        """Apply one `saturation` to all pixels."""
        self.apply_singular_thing(saturation, "saturation")

    def off(self):
        """Make it dark."""
        self.apply_value(0)
        self.light_up()

    ###

    def apply_thing_to_one_pixel(self, index, singular, key):
        """Apply one `whatever` to one pixel."""
        self.pixels[index][key] = singular

    def apply_hue_to_one_pixel(self, index, hue):
        """Apply `hue` to one pixel."""
        self.apply_thing_to_one_pixel(index, hue, "hue")

    def apply_value_to_one_pixel(self, index, value):
        """Apply `value` to one pixel."""
        self.apply_thing_to_one_pixel(index, value, "value")

    def apply_saturation_to_one_pixel(self, index, saturation):
        """Apply `saturation` to one pixel."""
        self.apply_thing_to_one_pixel(index, saturation, "saturation")

    ###

    def __getitem__(self, index):
        """Implement `foo[bar]`."""
        return self.pixels[index]

    def __len__(self):
        """Implement `len()`."""
        return len(self.pixels)


def rgb_for(pixel, brightness_factor):
    """Make the RGB value from a pixel's state."""
    return rgb_from_hsv(
        pixel["hue"], pixel["saturation"], pixel["value"] * brightness_factor
    )


class FakeLights(list):
    """Fake NeoPixels for testing."""

    def __init__(self, length):  # pylint: disable=W0231
        """Construct."""
        self.length = length
        for _ in range(self.length):
            self.append((0, 0, 0))

        self.record = []

    def show(self):
        """Pretend to show the lights."""
        self.record.append(self[:])


class FakeBrightnessControl:
    """Fake brightness control for testing."""

    def __init__(self):
        """Construct."""
        self.factor = FakeFactor(1.0)


class FakeFactor:
    """Fake value thing."""

    def __init__(self, value):
        """Construct."""
        self.value = value
