# from math import sqrt

# from glowing_hat.renderers.rotator import line, point_on_line


# def test_flat_line():
#     """Test a flat line."""
#     assert close_enough(line(0), [(0.0, 0.0), (1.0, 0.0)])


# def test_45_degree_line():
#     """Test a 45-degree line."""
#     assert close_enough(line(45), [(0, 0), ((sqrt(2) / 2), sqrt(2) / 2)])


# def test_vertical_line():
#     """Test a vertical line."""
#     assert close_enough(line(90), [(0.0, 0.0), (0.0, 1.0)])


# def test_point_on_line():
#     """Test if a point is on a line."""
#     assert point_on_line((0, 0), ((0, 0), (1, 0)))
#     assert point_on_line((0.1, 0.1), ((0, 0), (1, 1)))


# def test_point_near_line():
#     """Test if a point is *near* a line."""
#     assert point_on_line((0, 0.01), ((0, 0), (1, 0)))


# ###


# def close_enough(actual, expected):
#     """These numbers are fucking fiddly."""
#     for i in range(len(expected)):  # pylint:disable=C0200
#         for j in range(len(expected[i])):
#             if abs(expected[i][j] - actual[i][j]) > 0.0000001:
#                 return False

#     return True
