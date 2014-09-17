# -*- coding: utf-8 -*-
"""Prepare docs (usually called by Makefile)."""
from __future__ import unicode_literals, print_function

import os
import re
import subprocess
import time

from textblob_de.compat import _open, get_external_executable

_HERE = os.path.dirname(__file__)


def read(fname):
    with _open(fname, encoding='utf-8') as fp:
        content = fp.read()
    return content


def get_rst_title(string, symbol, overline=False):
    n = len(string)
    if overline:
        string = n * symbol + "\n" + string + "\n" + n * symbol
    else:
        string = string + "\n" + n * symbol
    return string


def get_credits():
    """Extract credits from `AUTHORS.rst`"""
    credits = read(os.path.join(_HERE, "AUTHORS.rst")).split("\n")
    from_index = credits.index("Active Contributors")
    credits = "\n".join(credits[from_index + 2:])
    return credits


def rst2markdown_github(path_to_rst, path_to_md, pandoc="pandoc"):
    """
    Converts ``rst`` to **markdown_github**, using :program:`pandoc`

    **Input**

        * ``FILE.rst``

    **Output**

        * ``FILE.md``

    """
    _proc = subprocess.Popen([pandoc, "-f", "rst",
                              "-t", "markdown_github",
                              #"-o", path_to_md,
                              path_to_rst],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    print("Converting README.rst to markdown_github, "
          "using 'pandoc' ...")
    _stdout, _stderr = _proc.communicate()
    with _open(path_to_md, "w", encoding="utf-8") as _md:
        _skip_newline = False
        for line in _stdout.decode('utf-8').split(os.linesep):
            line = re.sub("``` sourceCode", "``` python", line)
            if line.startswith("[!["):
                _md.write(line)
                _md.write("\n")
                if not line.startswith(("[![LICENSE")):
                    _skip_newline = True
            elif _skip_newline and line == "":
                _skip_newline = False
                continue
            else:
                _md.write(line)
                _md.write("\n")

    if _stderr:
        print("pandoc.exe STDERR: ", _stderr)
    if os.path.isfile(path_to_md) and os.stat(path_to_md).st_size > 0:
        print("README.rst converted and saved as: {}".format(path_to_md))


def console_help2rst(cwd, help_cmd, path_to_rst, rst_title,
                     format_as_code=False):
    """
    Extract HELP information from ``<program> -h | --help`` message

    **Input**

        * ``$ <program> -h | --help``
        * ``$ cd <cwd> && make help``

    **Output**

        * ``docs/src/console_help_xy.rst``

    """
    generated_time_str = """

    ::

     generated: {0}

""".format(time.strftime("%d %B %Y - %H:%M"))

    with _open(path_to_rst, "w", encoding='utf-8') as f:
        print("File", f)
        print("cwd", cwd)
        print("help_cmd", help_cmd)
        os.chdir(cwd)
        _proc = subprocess.Popen(
            help_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,)
        help_msg = _proc.stdout.readlines()
        f.write(get_rst_title(
                rst_title,
                "-",
                overline=True))
        f.write(generated_time_str)
        if "README" in path_to_rst:
            help_msg = "".join(help_msg[10:])
            #help_msg = PACKAGE_DOCSTRING + help_msg
        for line in help_msg:
            # exclude directory walk messages of 'make'
            if line.strip().startswith("make[1]:"):
                print("skipped line: {}".format(line))
            # exclude warning messages
            elif line.strip().startswith("\x1b[1m"):
                print("skipped line: {}".format(line))
            # exclude warning messages on Windows (without ``colorama``)
            elif line.strip().startswith("Using fallback version of '"):
                print("skipped line: {}".format(line))
            else:
                # correctly indent tips in 'make help'
                if line.strip().startswith("-->"):
                    f.write(3 * "\t")
                if format_as_code:
                    f.write("\t" + line.strip())
                    f.write("\n")
                else:
                    f.write(line)

        f.write("\n")
        if "README" in path_to_rst:
            f.write(get_rst_title("Credits", "^"))
            f.write(get_credits())

    print("\ncmd:{} in dir:{} --> RST generated:\n\t{}\n\n".format(
        help_cmd, cwd, path_to_rst))


def update_docs(readme=True, makefiles=True):
    """Update documentation (ready for publishing new release)

    Usually called by ``make docs``

    :param bool make_doc: generate DOC page from Makefile help messages

    """
    if readme:
        _pandoc = get_external_executable("pandoc")
        rst2markdown_github(os.path.join(_HERE, "README.rst"),
                            os.path.join(_HERE, "README.md"),
                            pandoc=_pandoc)

    if makefiles:
        _make = get_external_executable("make")
        project_makefile_dir = os.path.abspath(_HERE)
        project_makefile_rst = os.path.join(
            _HERE,
            'docs',
            'src',
            'project_makefile.rst')
        docs_makefile_dir = os.path.join(_HERE, 'docs', 'src')
        docs_makefile_rst = os.path.join(
            _HERE,
            'docs',
            'src',
            'docs_makefile.rst')

        #: ``help2rst_queue`` stores tuples of
        #: ``(cwd, help_cmd, path_to_rst_file, rst_title_of_new_file)``
        help2rst_queue = [
            (project_makefile_dir, [_make, "help"], project_makefile_rst,
             "Project ``Makefile``"),

            (docs_makefile_dir, [_make, "help"], docs_makefile_rst,
             "Documentation ``Makefile``")]

        for cwd, help_cmd, outfile, title in help2rst_queue:
            console_help2rst(
                cwd,
                help_cmd,
                outfile,
                title,
                format_as_code=True)

if __name__ == '__main__':
    """Usually called by Makefile."""

    update_docs(readme=True,
                makefiles=True,
                )
