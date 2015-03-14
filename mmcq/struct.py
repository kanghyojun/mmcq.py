#! -*- coding: utf-8 -*-
from collections import Iterator

from .math_ import euclidean


__all__ = 'CMap', 'PQueue',


class CMap(object):

    def __init__(self):
        self.vboxes = []

    @property
    def palette(self):
        return map(lambda d: d['color'], self.vboxes)

    def append(self, item):
        self.vboxes.append({'vbox': item, 'color': item.average})

    def __len__(self):
        return len(self.vboxes)

    def nearest(self, color):
        if not self.vboxes:
            raise Exception('Empty VBoxes!')

        min_d = float('Inf')
        p_color = None
        for vbox in self.vboxes:
            vbox_color = vbox.color
            distance = euclidean(color, vbox_color)
            if min_d > distance:
                min_d = distance
                p_color = vbox.color

        return p_color

    def map(self, color):
        for vbox in self.vboxes:
            if vbox.contains(color):
                return vbox.color

        return self.nearest(color)


class PQueue(Iterator):

    def __init__(self, sorted_key):
        self.sorted_key = sorted_key
        self.items = []
        self.sorted_ = False

    def next(self):
        if not self.sorted_:
            self.items = sorted(self.items, self.sorted_key)
            self.sorted_ = True

        if not self.items:
            raise StopIteration

        return self.pop()

    def append(self, item):
        items = self.items.append(item)
        self.sorted_ = False

    def pop(self):
        if not self.sorted_:
            self.items = sorted(self.items, self.sorted_key)
            self.sorted_ = True

        r = self.items[0]
        self.items = self.items[1:]
        return r

    def __len__(self):
        return len(self.items)
