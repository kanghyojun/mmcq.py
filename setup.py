#! -*- coding: utf-8 -*-
from setuptools import setup
from mmcq import __version__

setup(name='mmcq.py',
      version='%d.%d.%d' % __version__,
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'Wand == 0.3.5'
      ])
