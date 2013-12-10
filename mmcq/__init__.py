#! -*- coding: utf-8 -*-
from contextlib import contextmanager

from .constant import SIGBITS
from .quantize import mmcq

@contextmanager
def get_palette(color_count=10, quality=10, **kwards):
    from wand.image import Image, Color
    if not any(['filename' in kwards, 'blob' in kwards, 'file' in kwards]):
        raise Exception('One of `filename`, `blob`, `file` MUST required.')

    with Image(**kwards) as image:
        colors = []
        image.resize(200, 200)
        for x in xrange(0, image.height):
            for y in xrange(0, image.width, quality):
                color = image[x][y]
                r = color.red_int8
                g = color.green_int8
                b = color.blue_int8
                a = color.alpha_int8
                if r < 250 and g < 250 and b < 250:
                    colors.append((r, g, b))

        c_map = mmcq(colors, color_count)
        yield c_map.palette


def get_dominant_color(color_count=5, quality=10, **kwards):
    with get_palette(color_count, quality, **kwards) as palette:
        return palette[0]
