from random import randrange
from typing import Tuple, Callable


class RandomColor:
    def __init__(self):
        self.max_value = 256
        self.r, self.g, self.b = self._get_random_rgb_color()

        self.r_shift_func = self._get_minus_or_plus(self.r)
        self.g_shift_func = self._get_minus_or_plus(self.g)
        self.b_shift_func = self._get_minus_or_plus(self.b)

    def _get_random_rgb_color(self) -> Tuple[int, int, int]:
        return randrange(30, 256), randrange(30, 256), randrange(30, 256)

    def _get_minus_or_plus(self, value: int) -> Callable[[int, int], int]:
        if value > self.max_value // 2:
            return lambda x, y: x - y
        else:
            return lambda x, y: x + y