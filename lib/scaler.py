from pathlib import Path

import yaml

from lib.pixel import Pixel


class Scaler(list):
    """Pixel scaler thing."""

    def __init__(self, locations="conf/locations.yaml", auto_centre=False):  # pylint: disable=W0231  # noqa: FBT002
        """Construct."""
        self.locations = locations
        self.absolutes = yaml.safe_load(Path(locations).read_text(encoding="UTF-8"))

        self.auto_centre = auto_centre

        if self.auto_centre:
            deconstructed = deconstruct(self.absolutes["lights"])
            for axis in ["x", "y", "z"]:
                deconstructed[axis] = normalise_list(deconstructed[axis])

            for i in range(len(deconstructed["x"])):
                scaled_light = {"index": i}
                scaled_light = {}
                for axis in ["index", "x", "y", "z"]:
                    scaled_light[axis] = deconstructed[axis][i]

                self.append(scaled_light)

        else:
            largest_span = find_largest_span(self.absolutes)
            for light in self.absolutes["lights"]:
                scaled_light = {"index": light["index"]}
                for axis in ["x", "y", "z"]:
                    centre = self.absolutes["centres"][axis]
                    scaled_light[axis] = (light[axis] - centre) / largest_span
                    if axis == "y":
                        scaled_light[axis] = 0 - scaled_light[axis]
                self.append(scaled_light)

    # TODO make this the default
    def as_pixels(self):
        """Return as a list of `Pixels`."""
        return [
            Pixel(
                index=item["index"],
                x=item["x"],
                y=item["y"],
                z=item["z"],
            )
            for item in self
        ]


def find_largest_span(absolutes):
    """Find the largest step from the centre, given some lists."""
    largest = 0
    centres = absolutes["centres"]
    deconstructed = deconstruct(absolutes["lights"])

    for axis in ["x", "y", "z"]:
        centre = centres[axis]
        for value in deconstructed[axis]:
            if value >= centre:
                if value - centre > largest:
                    largest = value - centre

            elif centre - value > largest:
                largest = centre - value

    return largest


def normalise_list(items):
    """Scale a list from -1 to 1."""
    reset = list(map(lambda x: x - min(items), items))  # noqa: C417
    factor = max(reset) / 2
    scaled = list(map(lambda x: x / factor, reset))  # noqa: C417
    normalised = list(map(lambda x: x - 1, scaled))  # noqa: C417

    return normalised  # noqa: RET504


def deconstruct(absolutes):
    """Pull the data to pieces."""
    deconstructed = {}

    for axis in ["index", "x", "y", "z"]:
        deconstructed[axis] = list(map(lambda w: w[axis], absolutes))  # noqa: C417

    return deconstructed
