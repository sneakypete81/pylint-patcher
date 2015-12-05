#!/usr/bin/env python
import sys
import setuptools

requires = ["pylint", "logilab-common"]

console_script = """
[console_scripts]
pylint-patcher = pylint_patcher.main:main
pylint-patcher-gui = pylint_patcher.main_gui:main
"""

# from pylint_patcher._version import __version__
exec(open("pylint_patcher/_version.py").read())

kw = {'entry_points': console_script,
      'zip_safe': True,
      'install_requires': requires
      }

setuptools.setup(name='pylint-patcher',
      version=__version__,
      description="Pylint addon to store lint exceptions in a patchfile.",
      long_description=open("README.rst").read(),
      author="Pete Burgers",
      url="https://github.com/sneakypete81/pylint-patcher",
      packages=["pylint_patcher",
                "pylint_patcher.external",
                "pylint_patcher.external.pylint"],
      keywords=["pylint-patcher", "pylint_patcher", "pylint",
                "pylint-patcher-gui", "pylint_patcher_gui",
                "patch", "patchfile"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Quality Assurance",
                   "Topic :: Utilities",
                   ],
      license="GPL 2.0",
      test_suite="tests",
      **kw
      )
