# -*- coding: utf-8 -*-
#
# Code imported from ``textblob-fr`` sample extension.
#
# :repo: `https://github.com/sloria/textblob-fr`_
# :source: textblob_fr/compat.py
# :version: 2013-10-28 (5c6329d209)
#
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
