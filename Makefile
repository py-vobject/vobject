# -*- coding: utf-8; mode: makefile-gmake -*-

test:
	.venv/bin/python tests.py

clean:
	rm -rf .venv

# HINT:
# - black is not supported in py2 and py3.7 support stopped in black v23.7.0
#   https://github.com/psf/black/blob/main/CHANGES.md#2370
# - option --skip-string-normalization protects (among other things),
#   against deleting the unicode prefix in Python 2

format: venv
	- .venv/bin/python -m black --skip-string-normalization .
	@echo "\n"
	@echo "WARNING:"
	@echo "  Not all modifications from black are compatible to Python v2.x !!!"
	@echo "  E.g. don't merge patches of Python-2 unicode like: u'lorem ..' --> 'lorem ..'"
	@echo "\n"

black: venv
	.venv/bin/python -m black --skip-string-normalization --check --diff .

# HINT: pylint uses the AST (https://docs.python.org/3/library/ast.html) from
# the python interpreter.  To lint a py2 code base a Python 2 interpreter is
# needed.

# pylint in py3.x: all rules are taken from .pylintrc, additional some options
# disable to be py2 compatible
pylint: venv
	.venv/bin/python -m pylint --output-format=parseable \
		--disable=useless-option-value,redundant-u-string-prefix,unnecessary-pass,super-with-arguments \
		./vobject/ setup.py tests.py

# pylint in py2.7: addtional to the rules from .pylintrc disable messages which
# are only relevant in python 3
# Latest pylint version for py2 is pylint v1.9.5
pylint2.7: venv2.7
	.venv/bin/python -m pylint --output-format=parseable \
		--disable=bad-option-value,bad-continuation,superfluous-parens,old-style-class \
		./vobject/ setup.py tests.py

venv: clean
	- asdf local python system
	@python --version
	@python -c "import sys; sys.version_info[0] == 3 or (sys.stderr.write('ERROR: python 3 is required!\n'), sys.exit(42))"
	python -m venv .venv
	.venv/bin/python -m pip install --upgrade pip setuptools wheel
	.venv/bin/pip install -r requirements-dev.txt

venv2.7: clean
	- asdf local python 2.7.18
	@python --version
	@python -c "import sys; sys.version_info[0] == 2 or (sys.stderr.write('ERROR: python 2 is required!\n'), sys.exit(42))"
	python -m pip install virtualenv
	python -m virtualenv .venv
	.venv/bin/python -m pip install --upgrade pip setuptools wheel
	.venv/bin/pip install -r requirements-dev.txt


.PHONY: test clean venv venv2.7 black pylint pylint2.7
