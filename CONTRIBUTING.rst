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

. . .should all be reported on the `Github Issue Tracker`_ . For a nicer interface, check out the `textblob-de waffle.io board`_.

.. _textblob-de waffle.io board: https://waffle.io/markuskiller/textblob-de
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
    

``make`` command
----------------

This project adopts the ``Makefile`` approach, proposed by Jeff Knupp in his 
blog post `Open Sourcing a Python Project the Right Way \
<http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/>`_. 

On Linux/OSX the ``make`` command should work out-of-the-box::

    $ make help
    
Shows all available tasks.

Using ``make`` on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^

The two ``Makefile`` s in this project should work on all three major platforms.
On Windows, ``make.exe`` included in the `MinGW/msys <http://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download>`_ 
distribution has been successfully tested. Once ``msys`` is installed 
on a Windows system, the ``path/to/msys/1.0/bin`` needs to be added to 
the ``PATH`` environment variable.

A good place to update the ``PATH`` variable are the ``Activate.ps1`` or
``activate.bat`` scripts of a virtual python build environment, created using
``virtualenv`` (``pip install virtualenv``) or ``pyvenv`` (added to Python3.3's standard
library).

``Windows PowerShell``
""""""""""""""""""""""

Add the following line at the end of ``path\to\virtual\python\env\Scripts\Activate.ps1``::

    # Add msys binaries to PATH 
    $env:PATH = "path\to\MinGW\msys\1.0\bin;$env:PATH"

Windows ``cmd.exe``
""""""""""""""""""""

Add the following line at the end of ``path\to\virtual\python\env\Scripts\activate.bat``::

    # Add msys binaries to PATH
    set "PATH=path\to\MinGW\msys\1.0\bin;%PATH%"
    
Now the ``make`` command should work as documented in ``$ make help``.