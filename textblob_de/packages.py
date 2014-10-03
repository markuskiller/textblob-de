# -*- coding: utf-8 -*-
#
# Code imported from the main `TextBlob`_ library.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: packages.py
# :version: 2013-10-21 (a88e86a76)
#
# :modified: 2014-09-17 <m.killer@langui.ch>
#
"""Module to provide import context for vendorized packages such as
``pattern``."""
from __future__ import absolute_import
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

import nltk


try:
    import pattern.de as pattern_de
    import pattern.text as pattern_text
    import pattern.tree as pattern_tree
    import pattern.search as pattern_search
except ImportError:
    sys.path.append(os.path.join(HERE, 'ext'))
    from _pattern import de as pattern_de
    from _pattern import text as pattern_text
    from _pattern import tree as pattern_tree
    from _pattern import search as pattern_search
    sys.path.pop(-1)
