from colorsys import hsv_to_rgb
from datetime import datetime
from math import atan2, degrees
from pathlib import Path

from lib.gamma import gamma


def hue_to_rgb(hue):
    """Generate a GRB triple from a hue."""
    return list(map(lambda x: int(x * 255), hsv_to_rgb(hue, 1, 1)))  # noqa: C417


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return tuple(map(lambda n: gamma[int(n)], triple))  # noqa: C417


def normalise(triple, factor=1):
    """Adjust colours."""
    return tuple(map(lambda x: int(x * factor), gamma_correct(triple)))  # noqa: C417


def make_key(key, namespace):
    """Make compound key."""
    return f"{namespace}:{key}"


def close_enough(actual, target, tolerance=0.1):
    """Is a value close enough."""
    if abs(target - actual) <= tolerance:
        return True

    return False


def scale_colour(triple, factor):
    """Dim a colour."""
    return list(map(lambda x: int(x * factor), triple))  # noqa: C417


def remove_axis(axis):
    """Remove an axis from x, y, z."""
    return list(filter(lambda x: x != axis, ["x", "y", "z"]))


def colour_set_to_colour_list(colour_set, width):
    """Turn a colour-set definition into a list of RGB triples."""
    result = []
    for triple in list(colour_set.values()):
        for _ in range(width):
            result.append(triple)  # noqa: PERF401

    return result


def colour_from_time():
    """Generate an RGB triple from a hue from sub-seconds."""
    return hue_to_rgb(datetime.now().microsecond / 10**6)  # noqa: DTZ005


def is_pi():
    """Detect if we're on a Pi."""
    model_file = "/sys/firmware/devicetree/base/model"
    return Path(model_file).exists() and "Raspberry Pi" in Path(model_file).read_text()


# https://stackoverflow.com/a/62482938
def angle_to_point(axis_0, axis_1):
    """Get the angle of this line with the horizontal axis."""
    theta = atan2(axis_1, axis_0)
    ang = degrees(theta)
    if ang < 0:
        ang = 360 + ang

    if ang == 0:
        ang = 360

    return ang


# TODO this shouldn't have `hue_to_rgb` stuck in the middle of it
def brighten_pixels_less_than_y(pixels, y_value, scale_factor):
    """Colour-scale some pixels."""
    lights = []
    for pixel in pixels:
        colour = hue_to_rgb(pixel["hue"])
        if pixel["y"] < y_value:
            lights.append(colour)
        else:
            lights.append(scale_colour(colour, scale_factor))

    return lights
