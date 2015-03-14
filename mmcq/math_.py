#! -*- coding: utf-8 -*-
from math import sqrt


__all__ = 'euclidean',


def euclidean(p1, p2):
    return sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2) + pow(p2[2] - p1[2], 2) )
