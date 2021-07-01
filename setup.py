# -*- coding: utf-8 -*-
'''Code imported from ``textblob-fr`` sample extension.

:repo: `https://github.com/sloria/textblob-fr`_
:source: run_tests.py
:version: 2013-10-28 (5c6329d209)

:modified: July 2014 <m.killer@langui.ch>

'''
import sys
import subprocess
import re
from setuptools import setup

packages = ['textblob_de']
requires = ["textblob>=0.9.0"]


BUILD_CMD = "python setup.py sdist bdist_wheel"
CHECK_DIST_CMD = "twine check dist/*"
PUBLISH_CMD = "twine upload dist/*"
REGISTER_CMD = "twine register textblob-de"
TEST_PUBLISH_CMD = 'twine upload --repository-url https://test.pypi.org/legacy/ dist/*'
TEST_CMD = 'python run_tests.py'


def find_version(fname):
    """Attempts to find the version number in the file names fname.

    Raises RuntimeError if not found.

    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("textblob_de/__init__.py")

if 'publish' in sys.argv:
    try:
        __import__('wheel')
    except ImportError:
        print("wheel required. Run `pip install wheel`.")
        sys.exit(1)
    try:
        __import__('twine')
    except ImportError:
        print("twine required. Run `pip install twine`.")
        sys.exit(1)
    build = subprocess.call(BUILD_CMD, shell=True)
    check_dist = subprocess.call(CHECK_DIST_CMD, shell=True)
    status = subprocess.call(PUBLISH_CMD, shell=True)
    sys.exit(status)

if 'publish_test' in sys.argv:
    try:
        __import__('wheel')
    except ImportError:
        print("wheel required. Run `pip install wheel`.")
        sys.exit(1)
    try:
        __import__('twine')
    except ImportError:
        print("twine required. Run `pip install twine`.")
        sys.exit(1)
    build = subprocess.call(BUILD_CMD, shell=True)
    check_dist = subprocess.call(CHECK_DIST_CMD, shell=True)
    status = subprocess.call(TEST_PUBLISH_CMD, shell=True)
    sys.exit(status)
    
if 'register' in sys.argv:
    try:
        __import__('twine')
    except ImportError:
        print("twine required. Run `pip install twine`.")
        sys.exit(1)
    status = subprocess.call(REGISTER_CMD, shell=True)
    sys.exit(status)

if 'run_tests' in sys.argv:
    try:
        __import__('nose')
    except ImportError:
        print('nose required. Run `pip install nose`.')
        sys.exit(1)

    status = subprocess.call(TEST_CMD, shell=True)
    sys.exit(status)


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='textblob-de',
    version=__version__,
    description='German language support for TextBlob.',
    long_description=('\n' +
        read("README.rst") + '\n\n' + read("HISTORY.rst")),
    author='Markus Killer',
    author_email='m.killer@langui.ch',
    url='https://github.com/markuskiller/textblob-de',
    packages=packages,
    package_dir={
        'textblob_de': 'textblob_de'},
    include_package_data=True,
    package_data={
        "textblob_de": [
            "data/*.*",
            "ext/*.*",
            "ext/_pattern/*.*",
            "ext/_pattern/text/*.*",
            "ext/_pattern/text/de/*.*",
        ]},
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    keywords=[
        'textblob',
        'textblob_de',
        'nlp',
        'linguistics',
        'nltk',
        'pattern'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: German',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    test_suite='tests',
    tests_require=['nose'],
)
