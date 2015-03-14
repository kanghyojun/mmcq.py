#! -*- coding: utf-8 -*-
from .constant import SIGBITS, RSHIFT, MAX_ITERATION, FRACT_BY_POPULATIONS
from .region import Vbox
from .struct import CMap, PQueue


__all__ = 'mmcq', 'get_histo', 'get_color_index',


def get_color_index(r, g, b):
    return (r << (2 * SIGBITS)) + (g << SIGBITS) + b


def get_histo(colors):
    histo_size = 1 << (3 * SIGBITS)
    histo = list([0 for x in range(int(histo_size))])
    for color in colors:
        r = color[0] >> RSHIFT
        g = color[1] >> RSHIFT
        b = color[2] >> RSHIFT
        i = get_color_index(r, g, b)
        histo[i] = histo[i] + 1

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

    return Vbox(min(r_colors),
                max(r_colors),
                min(g_colors),
                max(g_colors),
                min(b_colors),
                max(b_colors),
                histo)


def median_cut(histo, vbox):
    if not vbox.count:
        return None

    rw = vbox.r2 - vbox.r1 +1
    gw = vbox.g2 - vbox.g1 +1
    bw = vbox.b2 - vbox.b1 +1
    maxw = max([rw, gw, bw])
    if vbox.count == 1:
        return (vbox.copy, )

    tot = 0
    sum_ = 0
    partialsum = {}
    lookaheadsum = {}
    do_cut_color = None
    if maxw == rw:
        do_cut_color = 'r'
        for i in range(vbox.r1, vbox.r2+1):
            for j in range(vbox.g1, vbox.g2+1):
                for k in range(vbox.b1, vbox.b2+1):
                    index = get_color_index(i, j, k)
                    sum_ += histo[index]

            tot += sum_
            partialsum[i] = tot
    elif maxw == gw:
        do_cut_color = 'g'
        for i in range(vbox.g1, vbox.g2+1):
            for j in range(vbox.r1, vbox.r2+1):
                for k in range(vbox.b1, vbox.b2+1):
                    index = get_color_index(j, i, k)
                    sum_ += histo[index]

            tot += sum_
            partialsum[i] = tot
    elif maxw == bw:
        do_cut_color = 'b'
        for i in range(vbox.b1, vbox.b2+1):
            for j in range(vbox.r1, vbox.r2+1):
                for k in range(vbox.g1, vbox.g2+1):
                    index = get_color_index(j, k, i)
                    sum_ += histo[index]

            tot += sum_
            partialsum[i] = tot

    for k, v in partialsum.iteritems():
        lookaheadsum[k] = tot - v

    dim1 = do_cut_color + '1'
    dim2 = do_cut_color + '2'
    dim1_val = getattr(vbox, dim1)
    dim2_val = getattr(vbox, dim2)
    for i in range(dim1_val, dim2_val+1):
        if partialsum[i] > (tot / 2):
            vbox1 = vbox.copy
            vbox2 = vbox.copy
            left = i - dim1_val
            right = dim2_val - i
            if left <= right:
                d2 = min([dim2_val - 1, ~~(i + right / 2)])
            else:
                d2 = max([dim1_val, ~~(i - 1 - left / 2)])

            while not partialsum[d2]:
                d2 += 1

            count2 = lookaheadsum[d2]
            while not count2 and (d2 - 1) in partialsum:
                d2 -= 1
                count2 = lookaheadsum[d2]

            setattr(vbox1, dim2, d2)
            setattr(vbox2, dim1, getattr(vbox1, dim2) + 1)
            return (vbox1, vbox2)


def mmcq(colors, max_color):
    if not isinstance(colors, list) or not colors:
        raise Exception('`colors` MUST be list '
                        'that contains items not %s'.format(colors))

    if max_color < 2 or max_color > 256:
        raise Exception('`max_color` MUST be a integer value between '
                        '2 and 256. not %s'.format(max_color))

    def iter(lh, target):
        n_colors = 1
        n_iters = 0

    pq = PQueue(lambda x, y: x.count >= y.count)
    histo = get_histo(colors)
    histo_size = 1 << (3 * SIGBITS)
    vbox = vbox_from_colors(colors, histo)
    pq.append(vbox)
    def iter_(lh, target):
        n_color = 1
        n_iter = 0
        while n_iter < MAX_ITERATION:
            vbox = lh.pop()
            if not vbox.count:
                lh.append(vbox)
                n_iter += 1
                continue
            vboxes = median_cut(histo, vbox)
            if not vboxes:
                return None
            lh.append(vboxes[0])
            if len(vboxes) == 2:
                lh.append(vboxes[1])
                n_color += 1
            if n_color >= target:
                return None
            if n_iter > MAX_ITERATION:
                return None
            n_iter += 1

    iter_(pq, FRACT_BY_POPULATIONS * max_color)
    pq2 = PQueue(lambda x, y: (y.volume * y.count) - (x.volume * x.count))
    for vbox in pq:
        pq2.append(vbox)

    iter_(pq2, max_color - len(pq2))
    cmap = CMap()
    for vbox in pq2:
        cmap.append(vbox)

    return cmap
