from unittest import TestCase

import redis

from lib.colour_wheel import ColourWheel


class TestColourWheel(TestCase):
    """Test the hue-spinner."""

    def setUp(self):
        """Setup."""
        self.redis = redis.Redis()

    def test_finding_start_hue(self):
        """Test it finds the existing hue."""
        self.redis.set("test:hue", 0.777)
        wheel = ColourWheel(namespace="test")
        self.assertEqual(wheel.start_hue, 0.777)

    def test_with_no_start_hue(self):
        """Test it handles no start hue."""
        self.redis.delete("test:hue")
        wheel = ColourWheel(namespace="test")
        self.assertEqual(wheel.start_hue, 0)
