from colorsys import hsv_to_rgb
from dataclasses import dataclass

import deprecation


@dataclass(order=True)
class Pixel:
    """Class representing a single NeoPixel."""

    index: int = 0
    x: float = 0.0  # TODO: should these be `field`s?
    y: float = 0.0
    z: float = 0.0

    # hue

    _hue: float = 0.0

    @property
    def hue(self) -> float:
        """Get `hue`."""
        return self._hue

    @hue.setter
    def hue(self, value):
        """Set `hue`."""
        self._hue = float(value)
        self.recalculate_rgb()

    # saturation

    _saturation: float = 1.0

    @property
    def saturation(self) -> float:
        """Get `saturation`."""
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        """Set `saturation`."""
        self._saturation = float(value)
        self.recalculate_rgb()

    # value

    _value: float = 1.0

    @property
    def value(self) -> float:
        """Get `saturation`."""
        return self._value

    @value.setter
    def value(self, value):
        """Set `value`."""
        self._value = float(value)
        self.recalculate_rgb()

    _rgb: tuple[int] = (0, 0, 0)

    # rgb

    @property
    def rgb(self):
        """Get `rgb`."""
        return self._rgb

    @rgb.setter
    def rgb(self, value):
        """Set `rgb`."""
        self._rgb = tuple(value)

    def recalculate_rgb(self):
        """Recalc `rgb` when `h`, `s` or `v` change."""
        self._rgb = tuple(
            int(x * 255) for x in hsv_to_rgb(self._hue, self._saturation, self._value)
        )

    angle: float = 0

    # TODO: see https://gist.github.com/robert-lucente/2179145cda7b99c278a5d0d8aacc6975#file-sorting_by_multiplefieldspythonsivji-py-L59
    @deprecation.deprecated(details="Prefer the `dataclass` interface")
    def __getitem__(self, key):
        """Implement foo['bar']."""
        return getattr(self, key)

    @deprecation.deprecated(details="Prefer the `dataclass` interface")
    def __setitem__(self, key, value):
        """Implement foo['bar'] == 'baz'."""
        setattr(self, key, value)

    @classmethod
    @deprecation.deprecated(details="Prefer the `dataclass` interface")
    def from_dict(cls, data):
        """Construct from a `dict`."""
        return cls(index=data["index"], x=data["x"], y=data["y"], z=data["z"])
