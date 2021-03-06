from lib.modes.sweeper import Sweeper


class Accelerator(Sweeper):
    """Accelerator mode."""

    def run(self):
        """Do the work."""
        self.reconfigure()

        i = 0
        step = 0

        while True:
            for direction in ["faster", "slower"]:
                while self.condition(step, direction):
                    self.illuminate(self.frames[round(i) % 360], self.get_colour())

                    i = (i + step) % 360
                    step = self.incdec(step, direction)

    def condition(self, step, direction):
        """Conditional condition."""
        if direction == "faster":
            return step < self.data["limits"]["max"]

        return step > self.data["limits"]["min"]

    def incdec(self, step, direction):
        """Increment or decrement."""
        if direction == "faster":
            return step + self.jump

        return step - self.jump
