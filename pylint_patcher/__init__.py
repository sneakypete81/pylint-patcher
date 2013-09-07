"""
__init__.py : pylint_patcher top level
"""
from ._version import __version__
import patcher
import differ
import main

PATCHFILENAME = ".pylint-ignores.patch"


