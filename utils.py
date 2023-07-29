import math
import random
from typing import Tuple


class RandColorIterator:
    def __init__(self) -> None:
        self.golden_ratio_conjugate = 0.618033988749895
        self.hue = random.random()
        self.saturation = 0.7
        self.value = 0.95

    def __next__(self) -> Tuple[int, int, int, int]:
        self.hue = math.fmod(self.hue + 0.618033988749895, 1)
        return hsv_to_rgb(self.hue, self.saturation, self.value) + (255,)


def hsv_to_rgb(h, s, v) -> Tuple[int, int, int]:
    """HSV values in [0..1]
    returns [r, g, b] values in [0..1]
    """
    h_i = int(h * 6)
    f = h * 6 - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    if h_i == 0:
        r, g, b = v, t, p
    elif h_i == 1:
        r, g, b = q, v, p
    elif h_i == 2:
        r, g, b = p, v, t
    elif h_i == 3:
        r, g, b = p, q, v
    elif h_i == 4:
        r, g, b = t, p, v
    elif h_i == 5:
        r, g, b = v, p, q
    return int(255 * r), int(255 * g), int(255 * b)