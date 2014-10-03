Contributing guidelines
=======================

In General
----------

- `PEP 8`_, when sensible.
- Test ruthlessly. Write docs for new features.
- Even more important than Test-Driven Development--*Human-Driven Development*.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/


In Particular
-------------

Questions, Feature Requests, Bug Reports, and Feedback. . .
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

. . .should all be reported on the `Github Issue Tracker`_.

.. _`Github Issue Tracker`: https://github.com/markuskiller/textblob-de/issues?state=open


Setting Up for Local Development
++++++++++++++++++++++++++++++++

1. Fork textblob-de on Github. ::

    $ git clone https://github.com/markuskiller/textblob-de.git
    $ cd textblob-de
    
2. (recommended) Create and activate virtual python environment. ::

    $ pip install -U virtualenv
    $ virtualenv tb-de
    $ <activate virtual environment>

3. Install development requirements and run ``setupy.py develop``.
   (see `Makefile help <project_makefile.html>`_ for overview of available 
   ``make`` targets)::

    $ make develop

