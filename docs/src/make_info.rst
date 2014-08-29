``make`` command
----------------

This project adopts the ``Makefile`` approach, proposed by Jeff Knupp in his 
blog post `Open Sourcing a Python Project the Right Way \
<http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/>`_. 

On Linux/OSX the ``make`` command should work out-of-the-box::

    $ make help
    
Shows all available tasks.

Using ``make`` on Windows
+++++++++++++++++++++++++

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
^^^^^^^^^^^^^^^^^^^^^^

Add the following line at the end of ``path\to\virtual\python\env\Scripts\Activate.ps1``::

    # Add msys binaries to PATH 
    $env:PATH = "path\to\MinGW\msys\1.0\bin;$env:PATH"

Windows ``cmd.exe``
^^^^^^^^^^^^^^^^^^^

Add the following line at the end of ``path\to\virtual\python\env\Scripts\activate.bat``::

    # Add msys binaries to PATH
    set "PATH=path\to\MinGW\msys\1.0\bin;%PATH%"
    
Now the ``make`` command should work as documented in ``$ make help``.