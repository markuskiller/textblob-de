.PHONY: clean-pyc clean-build clean-docs docs docs-pdf

# You can set these variables from the command line.

# N: Package Name
N = textblob_de

# M: git commit message
M =

# P: Python executable
P = python

# O: Platform specific 'open' command
# Linux 'open' or 'xdg-open' / OSX: 'open' / Win: 'start'

#O = start
O = xdg-open
#O = open


help:
	@echo ""
	@echo "Please use 'make <target>' where where <target> is one of"
	@echo ""
	@echo "SETUP & CLEAN"
	@echo "-------------"
	@echo ""
	@echo "install            run 'python setup.py install'"
	@echo "uninstall          run 'pip uninstall <package>'"
	@echo "develop            install links to source files in current Python environment"
	@echo "reset-dev          uninstall all links and console scripts and make clean"
	@echo "clean              remove all artifacts"
	@echo "clean-build        remove build artifacts"
	@echo "clean-docs         remove documentation build artifacts"
	@echo "clean-pyc          remove Python file artifacts (except in 'ext')"
	@echo "clean-test         remove test artifacts (e.g. 'htmlcov')"
	@echo "clean-logs         remove log artifacts and place empty file in 'log_dir'"
	@echo ""
	@echo "TESTING"
	@echo "-------"
	@echo ""
	@echo "autopep8           automatically correct 'pep8' violations"
	@echo "lint               check style with 'flake8'"
	@echo "test               run tests quickly with the default Python"
	@echo "test-all           run tests on every Python version with tox"
	@echo "coverage           check code coverage quickly with the default Python"
	@echo ""
	@echo "PUBLISHING"
	@echo "----------"
	@echo ""
	@echo "docs               generate Sphinx HTML documentation, including API docs"
	@echo "docs-pdf           generate Sphinx HTML and PDF documentation, including API docs"
	@echo "sdist              package"
	@echo "publish            package and upload sdist and universal wheel to PyPI"
	@echo "register           update README.rst on PyPI"
	@echo "push-github        push all changes to git repository on github.com"
	@echo "push-bitbucket     push all changes to git repository on bitbucket.org"
	@echo "                   --> include commit message as M='your message'"
	@echo ""
	@echo "VARIABLES ACCESSIBLE FROM COMMAND-LINE"
	@echo "--------------------------------------"
	@echo ""
	@echo "M='your message'   mandatory git commit message"
	@echo "N='package name'   specify python package name (optional)"
	@echo "O='open|xdg-open|start'"
	@echo "                   --> specify platform specific 'open' cmd (optional)"
	@echo "P='path/to/python' specify python executable (optional)"
	@echo ""

clean: clean-build clean-pyc clean-test clean-logs clean-docs
	find . -name '.DS_Store' -exec rm -f {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-docs:
	make -C ./docs/src clean
	rm -f docs/src/apidoc/$(N).rst
	rm -f docs/src/apidoc/modules.rst

clean-pyc:
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-test:
	rm -fr htmlcov/
	rm -fr .tox/
	rm -fr *.egg
	rm -f .coverage

clean-logs:
	find . -maxdepth 4 -name '*.log' -exec rm -f {} +
	find . -maxdepth 4 -name '*.log.[1-6]' -exec rm -f {} +

install:
	pip install -r requirements.txt
	$(P) setup.py install

uninstall:
	pip uninstall $(N)

reset-dev: uninstall clean reset-env clean-logs

reset-env:
	find . -name '.python-version' -exec rm -f {} +

develop: clean prepare_dev prepare_tests
	$(P) setup.py develop

prepare_dev:
	pip install -U -r requirements-dev.txt
	pip install -r requirements.txt

prepare_tests:
	pip install -U -r requirements-tests.txt

autopep8: prepare_tests
	autopep8 -v -i -a -a *.py
	autopep8 -v -i -a -a tests/*.py
	autopep8 -v -i -a -a $(N)/*.py
	docformatter -i *.py
	docformatter -i tests/*.py
	docformatter -i $(N)/*.py

lint: prepare_tests autopep8
	flake8

test: prepare_tests develop
	$(P) run_tests.py

test-all: prepare_tests
	tox

coverage: prepare_tests
	coverage run --source $(N) run_tests.py
	coverage report -m
	coverage html
	$(O) ./htmlcov/index.html &


docs: clean clean-docs prepare_dev develop
	$(P) prepare_docs.py
	#sphinx-apidoc -P -f -o docs/src/apidoc $(N) # use api_reference.rst
	make -C ./docs/src html
	$(O) ./docs/html/index.html &
	
	
docs-pdf: docs
	make -C ./docs/src latexpdf
	#$(O) ./docs/$(subst _,-,$(N)).pdf &

publish: clean clean-logs docs-pdf
	$(P) setup.py publish
	$(O) https://pypi.python.org/pypi/$(subst _,-,$(N)) &

sdist: clean clean-logs docs-pdf
	$(P) setup.py sdist
	ls -l dist

register:
	$(P) setup.py register
	$(O) https://pypi.python.org/pypi/$(subst _,-,$(N)) &

push-bitbucket: clean clean-logs
	git add --all
	git commit -a -m "$(M)"
	git push -u origin --all
	$(O) https://bitbucket.org/mki5600/$(subst _,-,$(N)) &
	
push-github: clean clean-logs
	git add --all
	git commit -a -m "$(M)"
	git push -u origin --all
	$(O) https://github.com/markuskiller/$(subst _,-,$(N)) &

