#! -*- coding: utf-8 -*-
from .constant import SIGBITS, RSHIFT, MAX_ITERATION
from .region import Vbox

__all__ = 'get_histo', 'get_color_index',


def get_color_index(r, g, b):
    return r << (2 * SIGBITS) + (g << SIGBITS) + b


def get_histo(colors):
    histo_size = 1 << (3 * SIGBITS)
    histo = [0 for x in xrange(histo_size)]
    for color in colors:
        r = color[0] >> RSHIFT
        g = color[1] >> RSHIFT
        b = color[2] >> RSHIFT
        i = get_color_index(r, g, b)
        histo[i] += 1

    return histo


def vbox_from_colors(colors, histo):
    r_colors = []
    g_colors = []
    b_colors = []
    for color in colors:
        r = color[0] >> RSHIFT
        g = color[1] >> RSHIFT
        b = color[2] >> RSHIFT
        r_colors.append(r)
        g_colors.append(r)
        b_colors.append(r)

    return Vbox(min(r), max(r), min(g), max(g), min(b), max(b), histo)
