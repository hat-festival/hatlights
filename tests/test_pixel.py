from unittest import TestCase

from lib.pixel import Pixel


class TestPixel(TestCase):
    """Test the Pixel."""

    def test_constructor(self):
        """Test it gets the right data."""
        pix = Pixel(index=0, x=0.5, y=0.5, z=0.5)
        assert pix.index == 0
        assert pix.x == 0.5  # noqa: PLR2004

    def test_setting_rgb(self):
        """Test we can set the Pixel's `rgb`."""
        pix = Pixel(index=0, x=0.5, y=0.5, z=0.5)
        pix.rgb = [4, 5, 6]
        assert pix.rgb == (4, 5, 6)

    def test_setting_hue(self):
        """Test that setting the `hue` also changes the `rgb`."""
        pix = Pixel(index=0, x=0.5, y=0.5, z=0.5)
        pix.rgb = [6, 7, 8]
        assert pix.rgb == (6, 7, 8)

        pix.hue = 0.5
        assert pix.hue == 0.5  # noqa: PLR2004
        assert pix.rgb == (0, 255, 255)

    def test_setting_hsv(self):
        """Test that futzing with `h`, `s` and `v` changes the `rgb."""
        pix = Pixel(index=0, x=0.5, y=0.5, z=0.5)
        pix.hue = 1 / 3
        pix.value = 0.5

        assert pix.rgb == (0, 127, 0)

    def test_dict_getters(self):
        """Test we can do `foo['bar']`."""
        pix = Pixel(index=0, x=0.5, y=0.5, z=0.5)
        assert pix["x"] == 0.5  # noqa: PLR2004
        assert pix["hue"] == 0.0

    def test_dist_setters(self):
        """Test we can do `foo['bar']` = 'baz'."""
        pix = Pixel(index=0, x=0.5, y=0.5, z=0.5)
        pix["x"] = 1.0
        assert pix.x == 1.0
