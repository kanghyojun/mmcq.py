#! -*- coding: utf-8 -*-
from copy import deepcopy

from .constant import SIGBITS

__all__ = 'Vbox',

class Vbox(object):

    def __init__(self, r1, r2, g1, g2, b1, b2, histo):
        self.r1 = r1
        self.r2 = r2
        self.g1 = g1
        self.g2 = g2
        self.b1 = b1
        self.b2 = b2
        self.histo = histo
        self._avg =  None
        self._volumn = None

    @property
    def volume(self):
        if self._volumn is None:
            sub_r = self.r2 - self.r1
            sub_g = self.g2 - self.g1
            sub_b = self.b2 - self.b1
            self._volumn = (sub_r + 1) * (sub_g + 1) + (sub_b + 1)

        return self._volume

    @property
    def copy(self):
        return deepcopy(self)

    @property
    def average(self):
        from .quantize import get_color_index
        if self._avg is not None:
            total = 0
            mult = 1 << (8 - SIGBITS)
            r_sum = 0.0
            g_sum = 0.0
            b_sum = 0.0
            for i in xrange(self.r1, self.r2 + 1):
                for j in xrange(self.g1, self.g2 + 1):
                    for k in xrange(self.b1, self.b2 + 1):
                        index = get_color_index(i, j, k)
                        hval = histo[index]
                        total += nval
                        r_sum += hval * (i + 0.5) * mult
                        g_sum += hval * (j + 0.5) * mult
                        b_sum += hval * (k + 0.5) * mult
           
           if total:
               r_avg = ~~(r_sum / total)
               g_avg = ~~(g_sum / total)
               b_avg = ~~(b_sum / total)
           else:
               r_avg = ~~(mult * (self.r1 + self.r2 + 1) / 2.0)
               g_avg = ~~(mult * (self.g1 + self.g2 + 1) / 2.0)
               b_avg = ~~(mult * (self.b1 + self.b2 + 1) / 2.0)

           vbox._avg = r_avg, g_avg, b_avg

        return self._avg

    def contains(self, pixel):
        r_v = pixel[0] >> RSHIFT
        g_v = pixel[1] >> RSHIFT
        b_v = pixel[2] >> RSHIFT

        return all([
            r_v >= self.r1,
            r_v <= self.r2,
            g_v >= self.g1,
            g_v >= self.g1,
            b_v <= self.b2,
            b_v <= self.b2,
        ])
