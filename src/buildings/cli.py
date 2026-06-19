"""US building inventory command line interface

Syntax
------

    buildings STATE ...

Description
-----------

Processes the building inventory for the specifies state(s). States are
specified using the states' postal abbrevations, e.g., AK for Alaska, etc.
"""

import os
import sys

from buildings import Buildings

E_OK = 0

def main(argv:list[str]|None=None):
    """Main function

    Arguments
    ---------

    - `argv`: main command arguments

    Returns
    -------

    - `int`: exit code
    """
    if argv is None:
        argv = sys.argv[1:] if len(sys.argv) > 1 else []
    assert isinstance(argv,list), f"{argv=} must be a list"

    for arg in argv:
        if arg.startswith("-p=") or arg.startswith("--precision="):
            Buildings.PRECISION = int(arg.split("=")[1])
        elif not arg.startswith("-"):
            print("Processing",arg,flush=True,end="...")
            if os.path.exists(f"../US/{arg}.csv"):
                Buildings.LIBRARY_PATH = "../US/{state}"
            Buildings(arg).to_counties(path="../US")
            print("ok")
        else:
            raise ValueError(f"{arg=} is invalid")

    return E_OK

if __name__ == '__main__':
    main(["-p=1","DC"])
