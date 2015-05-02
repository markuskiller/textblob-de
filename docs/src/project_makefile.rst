--------------------
Project ``Makefile``
--------------------

    ::

     generated: 02 May 2015 - 16:47

	
	Please use 'make <target>' where where <target> is one of
	
	SETUP & CLEAN
	-------------
	
	install            run 'python setup.py install'
	uninstall          run 'pip uninstall <package>'
	develop            install links to source files in current Python environment
	reset-dev          uninstall all links and console scripts and make clean
	clean              remove all artifacts
	clean-build        remove build artifacts
	clean-docs         remove documentation build artifacts
	clean-pyc          remove Python file artifacts (except in 'ext')
	clean-test         remove test artifacts (e.g. 'htmlcov')
	clean-logs         remove log artifacts and place empty file in 'log_dir'
	
	TESTING
	-------
	
	autopep8           automatically correct 'pep8' violations
	lint               check style with 'flake8'
	test               run tests quickly with the default Python
	test-all           run tests on every Python version with tox
	coverage           check code coverage quickly with the default Python
	
	PUBLISHING
	----------
	
	docs               generate Sphinx HTML documentation, including API docs
	docs-pdf           generate Sphinx HTML and PDF documentation, including API docs
	sdist              package
	publish            package and upload sdist and universal wheel to PyPI
	register           update README.rst on PyPI
	push-github        push all changes to git repository on github.com
	push-bitbucket     push all changes to git repository on bitbucket.org
				--> include commit message as M='your message'
	
	VARIABLES ACCESSIBLE FROM COMMAND-LINE
	--------------------------------------
	
	M='your message'   mandatory git commit message
	N='package name'   specify python package name (optional)
	O='open|xdg-open|start'
				--> specify platform specific 'open' cmd (optional)
	P='path/to/python' specify python executable (optional)
	

