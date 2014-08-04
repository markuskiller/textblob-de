#### PATTERN | DE | RULE-BASED SHALLOW PARSER ######################################################
# Copyright (c) 2012 University of Antwerp, Belgium
# Author: Tom De Smedt <tom@organisms.be>
# License: BSD (see LICENSE.txt for details).
# http://www.clips.ua.ac.be/pages/pattern

# Source: https://github.com/clips/pattern/pattern/text/de/__main__.py
# git-commit: 2013-05-29 (68fd41e)

# Modified: 2014-08-04 Markus Killer <m.killer@langui.ch>

####################################################################################################
# In Python 2.7+ modules invoked from the command line  will look for a __main__.py.

from __init__ import parse, commandline
commandline(parse)