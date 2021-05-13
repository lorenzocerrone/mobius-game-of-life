from mobiusgol.utils import add_pattern_from_file, add_pattern, read_pattern_shape
import numpy as np


def make_oblique_line(height=30,
                      gospel_path="./patterns/gosperglidergun.rle",
                      eater_path="./patterns/eater1.rle"):
    offset = 14  # hard coded for this type of application
    shape = (height, height + offset)
    x = np.zeros(shape)
    gospel_shape = read_pattern_shape(gospel_path)
    x = add_pattern_from_file(x, eater_path, (0, 0), 2)
    x = add_pattern_from_file(x, gospel_path, (height - gospel_shape[0], height + offset - gospel_shape[1]), 2)
    return x


def make_horizontal_line(length=100,
                         putter_fish_path="./patterns/pufferfish.rle",
                         eater_path="./patterns/eater1.rle"):
    putter_fish_shape = read_pattern_shape(putter_fish_path)[1], read_pattern_shape(putter_fish_path)[0]

    pattern = np.zeros((putter_fish_shape[0], length))
    pattern = add_pattern_from_file(pattern, putter_fish_path, (0, length - putter_fish_shape[1]), 1)
    pattern = add_pattern_from_file(pattern, eater_path, (4, 0), 3)
    return pattern


def basic_triangle(height=30, guns_offset=6, add_lines=False):
    pattern = make_oblique_line(height)
    pattern_shape = pattern.shape
    x = np.zeros((pattern_shape[0], pattern_shape[1] * 2 + guns_offset))
    x = add_pattern(x, pattern, (0, 0))
    x = add_pattern(x, pattern, (0, pattern_shape[1] + guns_offset), flip=(1, -1))
    if add_lines:
        x = add_pattern(x, make_horizontal_line(int(1.7 * height) - 2), (12, x.shape[1] // 2), centered=True)
        x = add_pattern(x, make_horizontal_line(int(1.1 * height) - 2), (42, x.shape[1] // 2), centered=True)
        x = add_pattern(x, make_horizontal_line(int(0.5 * height) - 2), (72, x.shape[1] // 2), centered=True)

    return x


def multi_triangle(height=30, guns_offsets=(6, 50), heights_offsets=(0, 10), add_lines=(True, False)):
    patterns = []
    for offset, h_offset, lines in zip(guns_offsets, heights_offsets, add_lines):
        patterns.append(basic_triangle(height=height + 2 * h_offset, guns_offset=offset, add_lines=lines))

    largest_shape = patterns[-1].shape
    x = np.zeros((largest_shape[0] + max(heights_offsets),
                  largest_shape[1] + max(heights_offsets)))
    for pattern, offset in zip(patterns, heights_offsets):
        x = add_pattern(x, pattern, (largest_shape[0] // 2 + offset, largest_shape[1] // 2), centered=True)
    return x


def multi_triangle_row_odd(shape, num_pattern=6, layer=3):
    x = np.zeros(shape)
    triangle = multi_triangle(height=120, guns_offsets=[6, 40], heights_offsets=[0, 10])
    left_triangle = triangle[:, 0:triangle.shape[1] // 2 + 1]
    right_triangle = triangle[:, triangle.shape[1] // 2 - 2:]
    h_offset = 240
    h_offset2 = 20

    x = add_pattern(x, triangle, (triangle.shape[0] // 2 + 4 * (triangle.shape[0] + h_offset2) + h_offset,
                                           shape[1] // 2 - triangle.shape[1] // 2))
    x = add_pattern(x, triangle, (triangle.shape[0] // 2 + 4 * (triangle.shape[0] + h_offset2) + h_offset,
                                           shape[1] // 2 + triangle.shape[1] // 2))
    x = add_pattern(x, triangle, (triangle.shape[0] // 2 + 4 * (triangle.shape[0] + h_offset2) + h_offset,
                                           shape[1] // 2 - 3 * triangle.shape[1] // 2))
    x = add_pattern(x, triangle, (triangle.shape[0] // 2 + 4 * (triangle.shape[0] + h_offset2) + h_offset,
                                           shape[1] // 2 + 3 * triangle.shape[1] // 2))

    x = add_pattern(x, right_triangle, (triangle.shape[0] // 2 + 4 * (triangle.shape[0] + h_offset2) + h_offset,
                              shape[1] // 2 - 3 * triangle.shape[1] // 2 - 3 * right_triangle.shape[1] // 2))
    x = add_pattern(x, left_triangle, (triangle.shape[0] // 2 + 4 * (triangle.shape[0] + h_offset2) + h_offset,
                                                shape[1] // 2 + 3 * triangle.shape[1] // 2 + 3 * right_triangle.shape[
                                                    1] // 2))