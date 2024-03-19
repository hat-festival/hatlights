from unittest import TestCase

from lib.pixel import Pixel
from lib.scaler import Scaler, deconstruct, find_largest_span, normalise_list


class TestScaler(TestCase):
    """Test the Scaler."""

    def test_constructor(self):
        """Test it gets the right data."""
        scaler = Scaler("tests/fixtures/scaler/simple-locations.yaml")
        self.assertEqual(  # noqa: PT009
            scaler.absolutes,
            {
                "lights": [
                    {"index": 0, "x": 0, "y": 0, "z": 0},
                    {"index": 1, "x": 1, "y": 1, "z": 1},
                    {"index": 2, "x": 2, "y": 2, "z": 2},
                    {"index": 3, "x": 3, "y": 3, "z": 3},
                    {"index": 4, "x": 4, "y": 4, "z": 4},
                ],
                "centres": {"x": 2, "y": 2, "z": 2},
            },
        )

    def test_simple_scaling(self):
        """Test it scales the simple data."""
        scaler = Scaler("tests/fixtures/scaler/simple-locations.yaml")
        self.assertEqual(find_extreme(scaler), 1.0)  # noqa: PT009
        self.assertEqual(  # noqa: PT009
            scaler,
            [
                {"index": 0, "x": -1, "y": 1, "z": -1},
                {"index": 1, "x": -0.5, "y": 0.5, "z": -0.5},
                {"index": 2, "x": 0, "y": 0, "z": 0},
                {"index": 3, "x": 0.5, "y": -0.5, "z": 0.5},
                {"index": 4, "x": 1, "y": -1, "z": 1},
            ],
        )

    def test_offset_scaling(self):
        """Test it scales the offset data."""
        scaler = Scaler("tests/fixtures/scaler/offset-locations.yaml")
        self.assertEqual(find_largest_span(scaler.absolutes), 1.5)  # noqa: PT009
        self.assertEqual(find_extreme(scaler), 1.0)  # noqa: PT009
        self.assertEqual(  # noqa: PT009
            scaler,
            [
                {
                    "index": 0,
                    "x": -0.3333333333333333,
                    "y": 0.6666666666666666,
                    "z": -0.6666666666666666,
                },
                {"index": 1, "x": 0.3333333333333333, "y": 0.0, "z": 0.0},
                {
                    "index": 2,
                    "x": 1.0,
                    "y": -0.6666666666666666,
                    "z": 0.6666666666666666,
                },
            ],
        )

    def test_messy_scaling(self):
        """Test it scales the messy data."""
        scaler = Scaler("tests/fixtures/scaler/messy-locations.yaml")
        self.assertEqual(find_largest_span(scaler.absolutes), 200)  # noqa: PT009
        self.assertEqual(find_extreme(scaler), 1.0)  # noqa: PT009
        self.assertEqual(  # noqa: PT009
            scaler,
            [
                {"index": 0, "x": -0.38, "y": 0.945, "z": -0.57},
                {"index": 1, "x": 0.55, "y": -1.0, "z": -0.79},
                {"index": 2, "x": 0.045, "y": 0.91, "z": 0.65},
            ],
        )

    def test_backloaded_scaling(self):
        """Test it scales the back-loaded data (where the extreme is -1.0)."""
        scaler = Scaler("tests/fixtures/scaler/back-loaded-locations.yaml")
        self.assertEqual(find_largest_span(scaler.absolutes), 45)  # noqa: PT009
        self.assertEqual(find_extreme(scaler), 1.0)  # noqa: PT009
        self.assertEqual(  # noqa: PT009
            scaler,
            [
                {
                    "index": 0,
                    "x": -0.3333333333333333,
                    "y": 0.6666666666666666,
                    "z": -1.0,
                },
                {
                    "index": 1,
                    "x": -0.1111111111111111,
                    "y": 0.2222222222222222,
                    "z": -0.3333333333333333,
                },
                {
                    "index": 2,
                    "x": 0.1111111111111111,
                    "y": -0.2222222222222222,
                    "z": 0.3333333333333333,
                },
            ],
        )

    def test_inverted_scaling(self):
        """Test it correctly inverts the y-axis."""
        scaler = Scaler("tests/fixtures/scaler/invertable-locations.yaml")
        self.assertEqual(find_largest_span(scaler.absolutes), 30)  # noqa: PT009
        self.assertEqual(find_extreme(scaler), 1.0)  # noqa: PT009
        self.assertEqual(  # noqa: PT009
            scaler,
            [
                {
                    "index": 0,
                    "x": -0.3333333333333333,
                    "y": 0.3333333333333333,
                    "z": -0.3333333333333333,
                },
                {"index": 1, "x": 0.0, "y": 0.0, "z": 0.0},
                {
                    "index": 2,
                    "x": 0.3333333333333333,
                    "y": -1.0,
                    "z": 0.3333333333333333,
                },
            ],
        )

    def test_realistic_scaling(self):
        """Test it scales the actual data."""
        scaler = Scaler("tests/fixtures/scaler/actual-locations.yaml")
        self.assertEqual(find_extreme(scaler), 1.0)  # noqa: PT009

    def test_non_autocentering(self):
        """Test it does independent centering."""
        scaler = Scaler(
            "tests/fixtures/scaler/non-centered-locations.yaml",
            auto_centre=True,
        )
        self.assertEqual(  # noqa: PT009
            scaler,
            [
                {
                    "index": 0,
                    "x": -1,
                    "y": -1,
                    "z": -1,
                },
                {
                    "index": 1,
                    "x": 0,
                    "y": 0,
                    "z": -0.5,
                },
                {
                    "index": 2,
                    "x": 1,
                    "y": 1,
                    "z": 1,
                },
            ],
        )

    def test_as_pixels(self):
        """Test it yields a list of `Pixels`."""
        scaler = Scaler("tests/fixtures/scaler/messy-locations.yaml")
        pixels = scaler.as_pixels()
        assert pixels[0] == Pixel(
            index=0,
            x=-0.38,
            y=0.945,
            z=-0.57,
            _hue=0.0,
            _saturation=1.0,
            _value=1.0,
            _rgb=(0, 0, 0),
            angle=0,
        )


def test_find_largest_span():
    """Test it finds the largest span."""
    assert (
        find_largest_span(
            {
                "lights": [
                    {"index": 0, "x": 1, "y": 2, "z": 3},
                    {"index": 1, "x": 10, "y": 11, "z": 12},
                    {"index": 2, "x": 4, "y": 5, "z": 6},
                    {"index": 3, "x": 7, "y": 8, "z": 9},
                    {"index": 4, "x": 25, "y": 14, "z": 15},
                ],
                "centres": {"x": 7, "y": 8, "z": 9},
            }
        )
        == 18  # noqa: PLR2004
    )


def test_deconstruct():
    """Test it breaks-up the data."""
    assert deconstruct(
        [
            {"index": 0, "x": 1, "y": 2, "z": 3},
            {"index": 1, "x": 10, "y": 11, "z": 12},
            {"index": 2, "x": 4, "y": 5, "z": 6},
            {"index": 3, "x": 7, "y": 8, "z": 9},
            {"index": 4, "x": 13, "y": 14, "z": 15},
        ]
    ) == {
        "index": [0, 1, 2, 3, 4],
        "x": [1, 10, 4, 7, 13],
        "y": [2, 11, 5, 8, 14],
        "z": [3, 12, 6, 9, 15],
    }


def test_normalise_list():
    """Test it normalises a list."""
    assert normalise_list([-1, 0, 1]) == [-1, 0, 1]
    assert normalise_list([1, 2, 3]) == [-1, 0, 1]
    assert normalise_list([19, 25, 31]) == [-1, 0, 1]
    assert normalise_list([19, 22, 25, 31]) == [-1, -0.5, 0, 1]
    assert normalise_list([19, 31, 25, 22]) == [-1.0, 1.0, 0.0, -0.5]


###


def find_extreme(data):
    """Find the largest absolute value in some data."""
    largest = 0

    for item in data:
        for axis in ["x", "y", "z"]:
            if abs(item[axis]) > largest:
                largest = abs(item[axis])

    return largest
