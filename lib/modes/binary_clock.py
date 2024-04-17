from datetime import datetime
from time import sleep

from lib.mode import Mode


class Clock(Mode):
    """A binary clock."""

    def run(self):
        """Do the stuff."""
        self.hat.off()

        while True:
            binaries = binary_hms(datetime.now())  # noqa: DTZ005
            self.accumulator = 0

            self.draw_divider()

            seconds = list(reversed(bin_string_to_values(binaries["seconds"])))
            for index in range(len(seconds)):
                self.hat.apply_hue_to_one_pixel(self.accumulator, self.conf["hues"]["seconds"])
                self.hat.apply_value_to_one_pixel(self.accumulator, seconds[index])
                self.accumulator += 1

            self.draw_divider()

            minutes = list(reversed(bin_string_to_values(binaries["minutes"])))
            for index in range(len(minutes)):
                self.hat.apply_hue_to_one_pixel(
                    self.accumulator, self.conf["hues"]["minutes"]
                )
                self.hat.apply_value_to_one_pixel(self.accumulator, minutes[index])
                self.accumulator += 1

            self.draw_divider()

            hours = list(reversed(bin_string_to_values(binaries["hours"])))
            for index in range(len(hours)):
                self.hat.apply_hue_to_one_pixel(
                    self.accumulator, self.conf["hues"]["hours"]
                )
                self.hat.apply_value_to_one_pixel(self.accumulator, hours[index])
                self.accumulator += 1

            self.draw_divider()

            self.hat.light_up()

            sleep(0.1)

    def draw_divider(self, width=1):
        """Draw a divider."""
        for _ in range(width):
            self.hat.apply_value_to_one_pixel(self.accumulator, 1.0)
            self.hat.apply_saturation_to_one_pixel(self.accumulator, 0.0)
            self.accumulator += 1


def bin_string_to_values(string):
    """Convert a binary-string to some values."""
    return list(map(float, string))


def binary_hms(timestamp):
    """Get the binary pieces of a timestamp."""
    return {
        "hours": f"{timestamp.hour:>05b}",
        "minutes": f"{timestamp.minute:>06b}",
        "seconds": f"{timestamp.second:>06b}",
    }
