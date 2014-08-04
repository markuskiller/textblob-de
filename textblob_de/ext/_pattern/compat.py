# -*- coding: utf-8 -*-

# Author: Steven Loria
# License: MIT License, see <http://opensource.org/licenses/MIT>

# Source: https://github.com/sloria/textblob-fr/textblob_fr/compat.py
# git-commit: 2013-10-28 (5c6329d209)

# Modified: 2014-08-04 Markus Killer <m.killer@langui.ch>

'''Compatibility module for shared code base on Python2 and Python3.
'''
import sys

PY2 = int(sys.version[0]) == 2
PY26 = PY2 and int(sys.version_info[1]) < 7

if PY2:
    from itertools import imap
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    imap = imap
else:
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
    imap = map
