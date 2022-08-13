from typing import List

from directions import dirs


class Pattern:
    def __init__(self, pixels):
        self.pixels = pixels

    def __len__(self):
        return 1


class Index:
    """
    Tells which combinations of patterns are allowed for all patterns

    data (dict):
        pattern -> posible_connections (dict):
                    relative_position -> patterns (list)
    """

    def __init__(self, patterns: List[Pattern]):
        self.data = {}
        for pattern in patterns:
            self.data[pattern] = {}
            for d in dirs:
                self.data[pattern][d] = []

    def add_rule(self, pattern: Pattern, relative_position: tuple, next_pattern: Pattern):
        self.data[pattern][relative_position].append(next_pattern)

    def check_possibility(self, pattern: Pattern, check_pattern: Pattern, relative_pos: tuple):
        if isinstance(pattern, list):
            pattern = pattern[0]

        return check_pattern in self.data[pattern][relative_pos]
