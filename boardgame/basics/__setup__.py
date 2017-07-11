#!/usr/bin/env python

from distutils.core import setup

setup(name='basics',
      version='1.0',
      description='Basic toolset',
      author='Connor Ullmann',
      author_email='cogrul@umich.edu',
      packages=['basics'],
      requires=['random', 'json', 'numpy', 'datetime', 'sys', 'pygame', 'time', 'os', 'platform', 'threading', 'math'])
