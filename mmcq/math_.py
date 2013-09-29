#! -*- coding: utf-8 -*-
from math import sqrt

__all__ = 'euclidean',

def euclidean(p1, p2):
    return sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(p1, p2))))
