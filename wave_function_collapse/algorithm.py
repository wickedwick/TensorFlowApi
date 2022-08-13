import random
from directions import valid_dirs
from utilities import get_min_entropy_pos, get_possible_patterns_at_position


def observe(coefficients, probability):
    # Find the lowest entropy
    min_entropy_pos = get_min_entropy_pos(coefficients, probability)

    if min_entropy_pos == None:
        print("All tiles have 0 entropy")
        return

    # Choose a pattern at lowest entropy position which is most frequent in the sample
    possible_patterns = get_possible_patterns_at_position(
        min_entropy_pos, coefficients)

    # calculate max probability for patterns that are left
    max_p = 0
    for pattern in possible_patterns:
        if max_p < probability[pattern]:
            max_p == probability[pattern]

    semi_random_pattern = random.choice(
        [pat for pat in possible_patterns if probability[pat] >= max_p])

    # Set this pattern to be the only available at this position
    coefficients[min_entropy_pos[0]][min_entropy_pos[1]] = semi_random_pattern

    return min_entropy_pos


def propagate(min_entropy_pos, coefficients, index, output_size):
    stack = [min_entropy_pos]

    while len(stack) > 0:
        pos = stack.pop()

        possible_patterns = get_possible_patterns_at_position(
            pos, coefficients)

        # Iterate through each location immediately adjacent to the current location
        for d in valid_dirs(pos, output_size):
            adjacent_pos = (pos[0] + d[0], pos[1] + d[1])
            possible_patterns_at_adjacent = get_possible_patterns_at_position(
                adjacent_pos, coefficients)

            # Iterate over all still available patterns in adjacent tile
            # and check if pattern is still possible in this location
            if not isinstance(possible_patterns_at_adjacent, list):
                possible_patterns_at_adjacent = [possible_patterns_at_adjacent]
            for possible_pattern_at_adjacent in possible_patterns_at_adjacent:
                if len(possible_patterns) > 1:
                    is_possible = any([index.check_possibility(
                        pattern, possible_pattern_at_adjacent, d) for pattern in possible_patterns])
                else:
                    is_possible = index.check_possibility(
                        possible_patterns, possible_pattern_at_adjacent, d)

                """
                If the tile is not compatible with any of the tiles in the current location's wavefunction
                then it's impossible for it to ever get choosen so it needs to be removed from the other
                location's wavefunction
                """
                if not is_possible:
                    x, y = adjacent_pos
                    coefficients[x][y] = [patt for patt in coefficients[x][y]
                                          if patt.pixels != possible_pattern_at_adjacent.pixels]

                    if adjacent_pos not in stack:
                        stack.append(adjacent_pos)
