#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import ast


def get_version(filename):
    with open(filename) as f:
        tree = ast.parse(f.read(), filename)
        for node in tree.body:
            if (isinstance(node, ast.Assign) and
                    node.targets[0].id == '__version__'):
                version = ast.literal_eval(node.value)
        if isinstance(version, tuple):
            version = '.'.join([str(x) for x in version])
        return version
    raise Exception('__version__ not found in {}'.format(filename))


setup(name='mmcq.py',
      version=get_version('mmcq/__init__.py'),
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      packages=find_packages(),
      install_requires=[
          'Wand >= 0.3.0'
      ])
