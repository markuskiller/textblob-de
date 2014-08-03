# -*- coding: utf-8 -*-
#
# Code imported from ``textblob`` main package.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: packages.py
# :version: 2014-10-21 (a88e86a76)
#
# :modified: 2014-08-03 <m.killer@langui.ch>
#
'''
Module to provide import context for vendorized packages such as nltk or pattern.
'''
from __future__ import absolute_import
import sys
import os

try:
    import nltk
except ImportError:
    from textblob.packages import nltk

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, 'ext'))

import _pattern as pattern

sys.path.pop(-1)
