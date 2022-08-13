
UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)
UP_LEFT = (-1, -1)
UP_RIGHT = (1, -1)
DOWN_LEFT = (-1, 1)
DOWN_RIGHT = (1, 1)
dirs = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


def valid_dirs(pos, output_size):
    x, y = pos

    valid_directions = []

    if x == 0:
        valid_directions.extend([RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_RIGHT])
        elif y == output_size[1]-1:
            valid_directions.extend([UP, UP_RIGHT])
        else:
            valid_directions.extend([DOWN, DOWN_RIGHT, UP, UP_RIGHT])
    elif x == output_size[0]-1:
        valid_directions.extend([LEFT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT])
        elif y == output_size[1]-1:
            valid_directions.extend([UP, UP_LEFT])
        else:
            valid_directions.extend([DOWN, DOWN_LEFT, UP, UP_LEFT])
    else:
        valid_directions.extend([LEFT, RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT, DOWN_RIGHT])
        elif y == output_size[1]-1:
            valid_directions.extend([UP, UP_LEFT, UP_RIGHT])
        else:
            valid_directions.extend(
                [UP, UP_LEFT, UP_RIGHT, DOWN, DOWN_LEFT, DOWN_RIGHT])

    return valid_directions
