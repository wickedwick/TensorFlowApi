import math
import random

from index import Pattern


def get_all_rotations(pixelMatrix):
    """
    Return original array as well as rotated by 90, 180 and 270 degrees in the form of tuples
    """
    pixelMatrix_rotated_1 = [[pixelMatrix[j][i] for j in range(
        len(pixelMatrix))] for i in range(len(pixelMatrix[0])-1, -1, -1)]
    pixelMatrix_rotated_2 = [[pixelMatrix_rotated_1[j][i] for j in range(len(
        pixelMatrix_rotated_1))] for i in range(len(pixelMatrix_rotated_1[0])-1, -1, -1)]
    pixelMatrix_rotated_3 = [[pixelMatrix_rotated_2[j][i] for j in range(len(
        pixelMatrix_rotated_2))] for i in range(len(pixelMatrix_rotated_2[0])-1, -1, -1)]
    return tuple(tuple(row) for row in pixelMatrix), \
        tuple(tuple(row) for row in pixelMatrix_rotated_1), \
        tuple(tuple(row) for row in pixelMatrix_rotated_2), \
        tuple(tuple(row) for row in pixelMatrix_rotated_3)


def get_first_pixels(coefficients):
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

    return final_pixels


def get_min_entropy_pos(coefficients, probability):
    """
    Return position of tile with the lowest entropy
    """
    minEntropy = None
    minEntropyPos = None

    for x, col in enumerate(coefficients):
        for y, row in enumerate(col):
            entropy = get_shannon_entropy((x, y), coefficients, probability)

            if entropy == 0:
                continue

            if minEntropy is None or entropy < minEntropy:
                minEntropy = entropy
                minEntropyPos = (x, y)
    return minEntropyPos


def get_offset_tiles(pattern: Pattern, offset: tuple):
    if offset == (0, 0):
        return pattern.pixels
    if offset == (-1, -1):
        return tuple([pattern.pixels[1][1]])
    if offset == (0, -1):
        return tuple(pattern.pixels[1][:])
    if offset == (1, -1):
        return tuple([pattern.pixels[1][0]])
    if offset == (-1, 0):
        return tuple([pattern.pixels[0][1], pattern.pixels[1][1]])
    if offset == (1, 0):
        return tuple([pattern.pixels[0][0], pattern.pixels[1][0]])
    if offset == (-1, 1):
        return tuple([pattern.pixels[0][1]])
    if offset == (0, 1):
        return tuple(pattern.pixels[0][:])
    if offset == (1, 1):
        return tuple([pattern.pixels[0][0]])


def get_possible_patterns_at_position(position, coefficients):
    """
    Return possible patterns at position (x, y)
    """
    x, y = position
    possible_patterns = coefficients[x][y]
    return possible_patterns


def get_shannon_entropy(position, coefficients, probability):
    """
    Calcualte the Shannon Entropy of the wavefunction at position (x, y)
    """
    x, y = position
    entropy = 0

    # A cell with one valid pattern has 0 entropy
    if len(coefficients[x][y]) == 1:
        return 0

    for pattern in coefficients[x][y]:
        entropy += probability[pattern] * math.log(probability[pattern], 2)
    entropy *= -1

    # Add noise to break ties and near-ties
    entropy -= random.uniform(0, 0.1)
    return entropy


def initialize_wave_function(size, patterns):
    """
    Initialize wave function of the size 'size' where in each tile no patterns are foridden yet.
    Coefficients describe what patterns can occur in each tile. At the beggining, at every possition there is full set
    of patterns available
    """

    coefficients = []

    for col in range(size[0]):
        row = []
        for r in range(size[1]):
            row.append(patterns)
        coefficients.append(row)
    return coefficients


def is_fully_collapsed(coefficients):
    """
    Check if wave function is fully collapsed meaning that for each tile available is only one pattern
    """
    for col in coefficients:
        for entry in col:
            if(len(entry) > 1):
                return False
    return True


def remove_duplicates(patterns):
    """
    Remove duplicates from list of patterns
    """
    patterns_without_duplicates = []
    for pattern in patterns:
        if pattern not in patterns_without_duplicates:
            patterns_without_duplicates.append(pattern)

    patterns = patterns_without_duplicates

    return patterns
