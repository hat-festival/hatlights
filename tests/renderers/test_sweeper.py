from lib.hat import Hat
from lib.renderers.sweeper import Sweeper
from lib.tools import angle_to_point


def test_construct():
    """Test it gets the right data."""
    hat = Hat(locations="tests/fixtures/conf/circles/1-location.yaml")
    swpr = Sweeper(hat=hat)

    assert swpr.hat.pixels[0].x == 0


def test_two_location_data():
    """Test it generates the simplest frame-set for 2 locations."""
    hat = Hat(locations="tests/fixtures/conf/circles/2-locations.yaml")
    swpr = Sweeper(hat=hat)

    assert swpr.populate("x", "z", 180) == [
        [(0, 0.5), (1, 1.0)],
        [(0, 1.0), (1, 0.5)],
    ]


def test_eight_location_data():
    """Test it generates a frame-set for 8 locations."""
    hat = Hat(locations="tests/fixtures/conf/circles/8-locations.yaml")
    swpr = Sweeper(hat=hat)

    assert swpr.populate("x", "z", 90) == [
        [
            (0, 0.75),
            (1, 0.625),
            (2, 0.5),
            (3, 0.375),
            (4, 0.25),
            (5, 0.125),
            (6, 1.0),
            (7, 0.875),
        ],
        [
            (0, 0.5),
            (1, 0.375),
            (2, 0.25),
            (3, 0.125),
            (4, 1.0),
            (5, 0.875),
            (6, 0.75),
            (7, 0.625),
        ],
        [
            (0, 0.25),
            (1, 0.125),
            (2, 1.0),
            (3, 0.875),
            (4, 0.75),
            (5, 0.625),
            (6, 0.5),
            (7, 0.375),
        ],
        [
            (0, 1.0),
            (1, 0.875),
            (2, 0.75),
            (3, 0.625),
            (4, 0.5),
            (5, 0.375),
            (6, 0.25),
            (7, 0.125),
        ],
    ]


def test_make_frame():
    """Test it makes a simple frame."""
    hat = Hat(locations="tests/fixtures/conf/circles/2-locations.yaml")
    swpr = Sweeper(hat=hat)

    assert swpr.make_frame("x", "z", 0) == [(0, 1.0), (1, 0.5)]
    assert swpr.make_frame("x", "z", 180) == [(0, 0.5), (1, 1.0)]


def test_make_bigger_frame():
    """Test it makes a frame."""
    hat = Hat(locations="tests/fixtures/conf/circles/8-locations.yaml")
    swpr = Sweeper(hat=hat)

    assert swpr.make_frame("x", "z", 0) == [
        (0, 1.0),
        (1, 0.875),
        (2, 0.75),
        (3, 0.625),
        (4, 0.5),
        (5, 0.375),
        (6, 0.25),
        (7, 0.125),
    ]
    assert swpr.make_frame("x", "z", 180) == [
        (0, 0.5),
        (1, 0.375),
        (2, 0.25),
        (3, 0.125),
        (4, 1.0),
        (5, 0.875),
        (6, 0.75),
        (7, 0.625),
    ]


def test_make_reversed_frame():
    """Test it makes an inverted frame."""
    hat = Hat(locations="tests/fixtures/conf/circles/8-locations.yaml")
    swpr = Sweeper(hat=hat)

    assert swpr.make_frame("x", "z", 0, rev=True) == [
        (0, 1.0),
        (1, 0.125),
        (2, 0.25),
        (3, 0.375),
        (4, 0.5),
        (5, 0.625),
        (6, 0.75),
        (7, 0.875),
    ]


def test_angle():
    """Test it gets the angle from an (x, y) pair."""
    assert angle_to_point(1, 0) == 360  # noqa: PLR2004
    assert angle_to_point(0, 1) == 90  # noqa: PLR2004
    assert angle_to_point(-1, 0) == 180  # noqa: PLR2004
    assert angle_to_point(0, -1) == 270  # noqa: PLR2004

    assert angle_to_point(1, 1) == 45  # noqa: PLR2004
    assert angle_to_point(-1, 1) == 135  # noqa: PLR2004
