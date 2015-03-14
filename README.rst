mmcq.py -- Python implementation of Modified Median Color Quantization (MMCQ)
================================================================================

goal of this project is write `JS implemntation MMCQ`_ in python.

.. _`JS implemntation MMCQ`: https://github.com/lokesh/color-thief/

MMCQ?
------

See more at `Color quantization using modified median cut by Dan S. Bloomb`_

.. _`Color quantization using modified median cut by Dan S. Bloomb`: http://www.leptonica.com/papers/mediancut.pdf

Usage
--------

To get sample palette, you can use `mmcq.get_palette`.

.. code-block:: python

    >>> from mmcq import get_palette
    >>> with get_palette(filename='/image/something.jpg', 3) as palette:
    ...     print palette
    [(255, 234, 0), (234, 245, 22), (42, 42, 42)]
    >>> from wand import Image
    >>> with Image(filename='/image/something.jpg') as image:
    ...     print get_palette(blob=image.make_blob(), 2)
    [(255, 234, 0), (234, 245, 22)]

To get dominant color, you can use `mmcq.get_dominant_color`
which color is frist of `mmcq.get_palette`.

.. code-block:: python

   >>> from mmcq import get_dominant_color
   >>> get_dominant_color(filename='/image/something.jpg')
   (255, 234, 0)


See more at `Color thief`_.

.. _Color thief: http://lokeshdhakar.com/color-thief/
