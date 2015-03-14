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
        self._count = None

    @property
    def volume(self):
        if self._volumn is None:
            sub_r = self.r2 - self.r1
            sub_g = self.g2 - self.g1
            sub_b = self.b2 - self.b1
            self._volumn = (sub_r + 1) * (sub_g + 1) + (sub_b + 1)

        return self._volumn

    @property
    def copy(self):
        copied = deepcopy(self)
        copied._avg = None
        copied._volumn = None
        copied._count = None
        return copied

    @property
    def average(self):
        from .quantize import get_color_index
        if self._avg is None:
            total = 0
            mult = 1 << (8 - SIGBITS)
            r_sum = 0
            g_sum = 0
            b_sum = 0
            for i in range(self.r1, self.r2 + 1):
                for j in range(self.g1, self.g2 + 1):
                    for k in range(self.b1, self.b2 + 1):
                        index = get_color_index(i, j, k)
                        hval = self.histo[index]
                        total += hval
                        r_sum += hval * (i + 0.5) * mult
                        g_sum += hval * (j + 0.5) * mult
                        b_sum += hval * (k + 0.5) * mult

            if total:
                r_avg = ~~int(r_sum / total)
                g_avg = ~~int(g_sum / total)
                b_avg = ~~int(b_sum / total)
            else:
                r_avg = ~~int(mult * (self.r1 + self.r2 + 1) / 2)
                g_avg = ~~int(mult * (self.g1 + self.g2 + 1) / 2)
                b_avg = ~~int(mult * (self.b1 + self.b2 + 1) / 2)

            self._avg = r_avg, g_avg, b_avg

        return self._avg

    def contains(self, pixel):
        r_v = pixel[0] >> RSHIFT
        g_v = pixel[1] >> RSHIFT
        b_v = pixel[2] >> RSHIFT

        return all([
            r_v >= self.r1,
            r_v <= self.r2,
            g_v >= self.g1,
            g_v <= self.g2,
            b_v >= self.b1,
            b_v <= self.b2,
        ])

    @property
    def count(self):
        from .quantize import get_color_index
        if not self._count:
            n_pix = 0
            his_len = len(self.histo)
            for i in range(self.r1, self.r2):
                for j in range(self.g1, self.g2):
                    for k in range(self.b1, self.b2):
                        index_ = get_color_index(i, j, k)
                        try:
                            n_pix += self.histo[index_]
                        except IndexError:
                            pass

            self._count = n_pix

        return self._count
