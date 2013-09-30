#! -*- coding: utf-8 -*-
from contextlib import contextmanager

from wand.image import Image, Color

from .constant import SIGBITS
from .quantize import mmcq

__version__ = (0, 0, 1)

class Timer(object):

    def __init__(self):
        self.start = None
        self.l = []

    def mark(self, name=''):
        from time import time
        if not self.start:
            self.start = time()
        else:
            t = time() - self.start
            self.l.append((name , t))

    def clear(self):
        self.l = []

    def __repr__(self):
        r = ""
        for i, x in enumerate(self.l):
            if x[0]:
                r += "%d mark `%s`, %.2f seconds\n" % (i, x[0], x[1])
            else:
                r += "%d mark, %.2f seconds\n" % (i, x[1])

        return r


@contextmanager
def get_palette(color_count=10, quality=10, **kwards):
    t = Timer()
    if not any(['filename' in kwards, 'blob' in kwards, 'file' in kwards]):
        raise Exception('One of `filename`, `blob`, `file` MUST required.')

    with Image(**kwards) as image:
        t.mark()
        colors = []
        image.resize(200, 200)
        for x in xrange(0, image.height):
            print x
            for y in xrange(0, image.width, quality):
                color = image[x][y]
                r = color.red_int8
                g = color.green_int8
                b = color.blue_int8
                a = color.alpha_int8
                if r < 250 and g < 250 and b < 250:
                    colors.append((r, g, b))

        t.mark('scanning ended')
        print t
        c_map = mmcq(colors, color_count)
        yield c_map.palette


def get_dominant_color(color_count=5, quality=10, **kwards):
    with get_palette(color_count, quality, **kwards) as palette:
        return palette[0]
