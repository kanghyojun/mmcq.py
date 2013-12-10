#! -*- coding: utf-8 -*-
from setuptools import setup

from mmcq.version import VERSION

setup(name='mmcq.py',
      version=VERSION,
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'Wand >= 0.3.0'
      ])
