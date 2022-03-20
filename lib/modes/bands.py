from math import ceil
from random import random

from lib.mode import Mode
from lib.tools import hue_to_rgb


class Bands(Mode):
    """Bands of colour."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.hat.sort(key=lambda w: w[self.axis])

        if self.invert:
            self.hat.reverse()

        self.jump = self.conf["modes"]["bands"]["jump"]
        self.width = self.conf["modes"]["bands"]["width"]

    def run(self):
        """Do the stuff."""
        while True:
            colour = hue_to_rgb(random())
            for i in range(ceil(len(self.hat) / self.jump)):
                for j in range(self.jump):
                    try:
                        self.hat.light_one(
                            self.hat[i * self.jump + j]["index"],
                            colour,
                            auto_show=False,
                        )
                    except IndexError:
                        pass

                    try:
                        self.hat.light_one(
                            self.hat[i * self.jump + j - self.width]["index"],
                            [0, 0, 0],
                            auto_show=False,
                        )
                    except IndexError:
                        pass

                self.hat.show()
