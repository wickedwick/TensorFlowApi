import math
from typing import List

import matplotlib.pyplot as plt

from algorithm import observe, propagate
from directions import dirs
from index import Index, Pattern
from utilities import (get_all_rotations, get_offset_tiles,
                       initialize_wave_function, is_fully_collapsed,
                       remove_duplicates)

# pixels = [[255, 255, 255, 255], [255, 0, 0, 0],
#           [255, 0, 138, 0], [255, 0, 0, 0]]

# pixels = [[0, 255, 255, 255], [138, 0, 255, 255],
#           [0, 255, 138, 255], [255, 255, 255, 255]]

# pixels = [[255, 255, 255, 255, 255, 255, 255, 255],
#           [255, 0, 0, 0, 0, 255, 255, 255],
#           [255, 0, 0, 0, 0, 255, 138, 255],
#           [255, 0, 255, 255, 255, 255, 255, 255],
#           [255, 0, 0, 0, 0, 255, 255, 255],
#           [255, 255, 255, 255, 255, 255, 138, 255],
#           [255, 255, 255, 255, 0, 0, 0, 255],
#           [255, 255, 255, 255, 255, 255, 255, 255]]

pixels = [[255, 255, 255, 255, 255, 255, 255, 255],
          [0, 0, 0, 255, 255, 255, 255, 255],
          [0, 0, 0, 46, 46, 46, 255, 255],
          [0, 0, 0, 138, 138, 46, 255, 255],
          [255, 255, 138, 92, 0, 0, 0, 255],
          [255, 255, 138, 138, 0, 46, 0, 255],
          [255, 255, 255, 255, 0, 0, 0, 255],
          [255, 255, 255, 255, 255, 255, 255, 255]]

input_size = (8, 8)
output_size = (50, 50)

# plt.imshow(pixels, cmap="gray")  # create plt
# print(pixels)
# plt.show()

N = 4  # pattern size
patterns = []
weights = {}  # dict pattern -> occurence
probability = {}  # dict pattern -> probability
for y in range(input_size[0]-(N-1)):  # row
    for x in range(input_size[1]-(N-1)):  # column
        pattern = []
        for k in pixels[y:y+N]:
            # change array to int really quick
            pattern.append([int(i) for i in k[x:x+N]])

        pattern_rotations = get_all_rotations(pattern)

        for rotation in pattern_rotations:
            if rotation not in weights:
                weights[rotation] = 1
            else:
                weights[rotation] += 1

        patterns.extend(pattern_rotations)

patterns = remove_duplicates(patterns)

sum_of_weights = 0
for weight in weights:
    sum_of_weights += weights[weight]

for pattern in patterns:
    probability[pattern] = weights[pattern] / sum_of_weights

# convert patterns from tuples into Pattern objects
patterns = [Pattern(p) for p in patterns]
weights = {pattern: weights[pattern.pixels] for pattern in patterns}
probability = {pattern: probability[pattern.pixels] for pattern in patterns}

# show
# plt.figure(figsize=(10, 10))
# for m in range(len(patterns)):
#     axs = plt.subplot(4, math.ceil(len(patterns)/4), m+1)
#     axs.imshow(patterns[m].pixels, cmap="gray", vmin=0, vmax=255)
#     axs.set_xticks([])
#     axs.set_yticks([])
#     plt.title("weight: %.0f prob: %.2f" %
#               (weights[patterns[m]], probability[patterns[m]]))
# plt.show()


index = Index(patterns)


# Generate rules for Index and save them
rules_num = 0
for pattern in patterns:
    for d in dirs:
        for pattern_next in patterns:
            # here's checking all offsets
            overlap = get_offset_tiles(pattern_next, d)
            og_dir = tuple([d[0]*-1, d[1]*-1])
            part_of_og_pattern = get_offset_tiles(pattern, og_dir)
            if (overlap) == (part_of_og_pattern):
                index.add_rule(pattern, d, pattern_next)
                rules_num += 1


# # Show data in Index
# print(f"There are {rules_num} rules")

# for d in index.data:
#     print(f'Pattern {d.pixels}')
#     for pos in index.data[d]:
#         print(f' Pos {pos}')
#         for pattern in index.data[d][pos]:
#             print(f' {pattern.pixels}')


coefficients = initialize_wave_function(output_size, patterns)

while not is_fully_collapsed(coefficients):
    min_entropy_pos = observe(coefficients, probability)
    propagate(min_entropy_pos, coefficients, index, output_size)


final_pixels = []

for i in coefficients:
    row = []
    for j in i:
        if isinstance(j, list):
            first_pixel = j[0].pixels[0][0]
        else:
            first_pixel = j.pixels[0][0]
        row.append(first_pixel)
    final_pixels.append(row)

plt.imshow(final_pixels, cmap="gray")
plt.show()
