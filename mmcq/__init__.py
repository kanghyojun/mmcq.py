#! -*- coding: utf-8 -*-
from contextlib import contextmanager

from wand.image import Image

from .constant import SIGBITS

__version__ = (0, 0, 1)


@contextmanager
def get_palette(color_count=10, quality=10, **kwards):
    if not any(['filename' in kwards, 'blob' in kwards, 'file' in kwards]):
        raise Exception('One of `filename`, `blob`, `file` MUST required.')

    with Image(**kwards) as image:
        colors = []
        for x in xrange(0, image.height, quality):
            for y in xrange(0, image.width, quality):
                color = image[x][y]
                r = color.red_int8
                g = color.green_int8
                b = color.blue_int8
                a = color.alpha_int8
                if a >= 125 and r < 250 and g < 250 and b < 250:
                    colors.append((r, g, b))

        c_map = mmcq(colors, color_count)
        return c_map.palette()
