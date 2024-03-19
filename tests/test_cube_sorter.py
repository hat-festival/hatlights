from unittest import TestCase

from lib.sorters.cube_sorter import CubeSorter


class TestCubeSorter(TestCase):
    """Test the CubeSorter."""

    def setUp(self):
        """Set things up."""
        self.sorter = CubeSorter(locations="tests/fixtures/hat/locations/simple.yaml")

    def test_sorting(self):
        """Try the sorter."""
        assert just_the_indeces(self.sorter.sort_from(-1, 0, 0)) == [2, 1, 0, 3, 4]
        assert just_the_indeces(self.sorter.sort_from(0, -1, 0)) == [4, 3, 2, 1, 0]
        assert just_the_indeces(self.sorter.sort_from(-1, -1, -1)) == [2, 3, 0, 4, 1]
        assert just_the_indeces(self.sorter.sort_from(1, 1, 1)) == [1, 4, 0, 3, 2]

    def test_sorting_a_bigger_cube(self):
        """Test we can sort for a bigger cube."""
        # we can go arbitrarily large but it breaks these orderings
        assert just_the_indeces(self.sorter.sort_from(0, -2, 0)) == [4, 3, 2, 1, 0]


def just_the_indeces(pixel_list):
    """Get just the indeces of the pixels."""
    return [x.index for x in pixel_list]
