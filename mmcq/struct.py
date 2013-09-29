#! -*- coding: utf-8 -*-
from .math_ import euclidean

__all__ = 'CMap',

class CMap(object):

    def __init__(self):
        self.vboxes = []


    @property
    def palette(self):
        return map(lambda vbox: vbox.color, self.vboxes)


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

   
   def forcebw(self):
       pass
