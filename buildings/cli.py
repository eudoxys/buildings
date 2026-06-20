"""US building inventory command line interface

Syntax
------

    buildings

Description
-----------

Opens the buildings inventory Marimo notebook in a browser window.
"""

import os
import sys
import webbrowser as web

from buildings import Buildings

E_OK = 0
E_FAILED = 1

def main(argv:list[str]|None=None):
    """Main function

    Arguments
    ---------

    - `argv`: main command arguments

    Returns
    -------

    - `int`: exit code
    """
    print("Opening marimo notebook",end="...",flush=True)
    try:
        web.open("https://molab.marimo.io/notebooks/nb_VhE7Lc7yYwafHwJxTQWyni/app")
        print("ok")
        return E_OK
    except Exception as err:
        print("ERROR [buildings]:",err)
        return E_FAILED

if __name__ == '__main__':
    main()
