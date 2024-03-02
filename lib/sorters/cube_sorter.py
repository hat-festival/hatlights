from lib.pixel import Pixel
from lib.scaler import Scaler


class CubeSorter:
    """Pre-calculate orderings along many axes."""

    def __init__(self, locations="conf/locations.yaml"):
        """Construct."""
        self.locations = locations
        self.scaler = Scaler(locations, auto_centre=False)
        self.pixels = list(map(Pixel, self.scaler))

    def sort_from(self, *point):
        """Sort from a point."""
        arranged = []
        # body diagonal of a 2x2x2 cube is 2*sqrt(3)
        for r in range(0, 7000, 1):
            radius = r / 1000
            arranged += list(
                filter(
                    lambda pixel: is_inside_sphere(pixel, point, radius)
                    and pixel not in arranged,
                    self.pixels,
                )
            )

        return arranged


def is_inside_sphere(pixel, centre, radius):
    """Is this pixel inside this sphere."""
    # https://math.stackexchange.com/a/3118250
    return (
        (pixel["x"] - centre[0]) ** 2
        + (pixel["y"] - centre[1]) ** 2
        + (pixel["z"] - centre[2]) ** 2
    ) < radius**2
