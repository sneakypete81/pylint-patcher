#!/usr/bin/env python
"""
main-gui.py : Pylint Patcher GUI
"""
import sys
from external.pylint import gui

def main(args=sys.argv[1:]):
    gui.Run(args)

if __name__ == "__main__": # pragma: no cover
    main()