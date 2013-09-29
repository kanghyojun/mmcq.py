#! -*- coding: utf-8 -*-
from .constant import SIGBITS

__version__ = (0, 0, 1)

def get_color_index(r, g, b):
    return r << (2 * SIGBITS) + (g << SIGBITS) + b
