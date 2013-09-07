#!/usr/bin/env python
"""
main.py : Pylint Patcher main console script
"""
import sys
import pylint.lint
from pylint_patcher import patcher

def main(args=sys.argv[1:], **kwds):
    """
    Apply the patchfile containing the pylint ignores,
    then run the linter,
    then revert the patchfile changes.
    """
    if args == []:
        # Print the Pylint usage docs
        pylint.lint.Run(args, **kwds)
        return

    # Apply the ignore patchfile before linting
    patch = patcher.Patcher(args[0])
    patch.patch()
    try:
        pylint.lint.Run(args, **kwds)
    finally:
        # Revert the ignore patchfile
        patch.unpatch()

if __name__ == "__main__": # pragma: no cover
    main()
