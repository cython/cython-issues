#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

setup(
  name = 'Test',
  ext_modules = [Extension("mylib", ["mylib.c"])]
)
