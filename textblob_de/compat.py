# -*- coding: utf-8 -*-
# Code adapted from the main `TextBlob`_ library.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: textblob/compat.py
# :version: 2013-12-16 (e7f9cf9)
#
# :modified: 2014-09-17 <m.killer@langui.ch>
#
'''Compatibility module for shared code base on Python2 and Python3.
'''
import os
import sys


PY2 = int(sys.version[0]) == 2
PY26 = PY2 and int(sys.version_info[1]) < 7

if PY2:
    from itertools import imap, izip
    import urllib2 as request
    from urllib import quote as urlquote
    from urllib import urlencode
    _FileNotFoundError = IOError
    # ``codecs.open`` with encoding keyword on Python2
    from codecs import open as _open
    _which = "compat"
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    imap = imap
    izip = izip
    # not quite sure why this ImportError did not
    # seem to occur earlier ...
    try:
        import unicodecsv as csv
    except ImportError:
        import csv

    def implements_to_string(cls):
        '''Class decorator that renames __str__ to __unicode__ and
        modifies __str__ that returns utf-8.
        '''
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls
else:  # PY3
    from urllib import request
    from urllib.parse import quote as urlquote
    from urllib.parse import urlencode
    # ``io.open`` with encoding keyword on Python3
    from io import open as _open
    try:
        from shutil import which as _which
    except ImportError:
        _which = "compat"
    # add pypy3 compatibilty
    try:
        _FileNotFoundError = FileNotFoundError
    except NameError:
        _FileNotFoundError = IOError
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
    imap = map
    izip = zip
    import csv

    implements_to_string = lambda x: x


def with_metaclass(meta, *bases):
    """Defines a metaclass.

    Creates a dummy class with a dummy metaclass. When subclassed, the
    dummy metaclass is used, which has a constructor that instantiates a
    new class from the original parent. This ensures that the dummy
    class and dummy metaclass are not in the inheritance tree.

    Credit to Armin Ronacher.

    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})


#--- STRING FUNCTIONS --------------------------------------------------

# Source: https://github.com/clips/pattern/pattern/text/__init__.py
# git-commit: 2014-05-10 (2f944cb)

# Modified: 2014-08-04 Markus Killer <m.killer@langui.ch>

# Latin-1 (ISO-8859-1) encoding is identical to Windows-1252 except for
# the code points 128-159:
# Latin-1 assigns control codes in this range, Windows-1252 has
# characters, punctuation, symbols
# assigned to these code points.

# String functions
def decode_string(v, encoding="utf-8"):
    """Returns the given value as a Unicode string (if possible)."""
    if isinstance(encoding, basestring):
        encoding = ((encoding,),) + (("windows-1252",), ("utf-8", "ignore"))
    if isinstance(v, binary_type):
        for e in encoding:
            try:
                return v.decode(*e)
            except:
                pass
        return v
    return unicode(v)


def encode_string(v, encoding="utf-8"):
    """Returns the given value as a Python byte string (if possible)."""
    if isinstance(encoding, basestring):
        encoding = ((encoding,),) + (("windows-1252",), ("utf-8", "ignore"))
    if isinstance(v, unicode):
        for e in encoding:
            try:
                return v.encode(*e)
            except:
                pass
        return v
    return str(v)

decode_utf8 = decode_string
encode_utf8 = encode_string


def get_external_executable(_exec):
    _exec_path = _which(_exec)
    if _exec_path:
        return _exec_path
    else:
        sys.exit("Required executable '{}' not found on this system. "
                 "Please install or add to PATH".format(_exec))

# Code adapted from Python 3.4 standard library ``shutil.py`` (lines: 1067-1127)
# to work on Python2
# Source: http://stackoverflow.com/questions/9877462 [accessed: 27/08/2014]


def _shutil_which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which conforms
    to the given mode on the PATH, or None if there is no such file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode)
                and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if not os.curdir in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any([cmd.lower().endswith(ext.lower()) for ext in pathext]):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if normdir not in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None

if _which == "compat":
    _which = _shutil_which
