"""US building inventory command line interface

See `buildings` for the command syntax.

Examples
--------

    buildings

outputs

    Opening marimo notebook...ok

and opens the building inventory notebook in a browser window.
"""

import sys
import argparse
import logging
import warnings
import webbrowser as web

_logger = logging.getLogger(__file__)

NOTEBOOK_URL = "https://molab.marimo.io/notebooks/nb_VhE7Lc7yYwafHwJxTQWyni/app"
"""URL of the building inventory marimo notebook"""

E_OK = 0
"""Exit code for success"""

E_FAILED = 1
"""Exit code for failure"""

def main(argv:list[str]|None=None) -> int:
    """Command line entry point

    Arguments
    ---------

      - `argv`: command line arguments (default `sys.argv[1:]`)

    Returns
    -------

      - `int`: exit code (0 on success)
    """
    # pylint: disable=import-outside-toplevel
    from buildings import __version__
    parser = argparse.ArgumentParser(prog="buildings",
        description="US building inventory",
        epilog="See https://www.eudoxys.com/buildings for full documentation.")
    parser.add_argument("command",nargs="?",choices=["open"],default="open",
        help="open the building inventory notebook in a browser (default)")
    parser.add_argument("-d","--debug",action="store_true",help="enable debug logging and traceback on exceptions")
    parser.add_argument("-w","--warning",action="store_true",help="enable warning messages from python")
    parser.add_argument("--version",action="version",version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    if not args.warning:
        warnings.simplefilter("ignore")

    try:
        if args.command == "open":
            print("Opening marimo notebook",end="...",flush=True)
            _logger.debug("opening %s",NOTEBOOK_URL)
            if not web.open(NOTEBOOK_URL):
                print("failed")
                raise RuntimeError(f"no browser available; open {NOTEBOOK_URL} by hand")
            print("ok")
        return E_OK
    except Exception as err: # pylint: disable=broad-exception-caught
        if args.debug:
            raise
        print(f"ERROR [buildings]: {err}",file=sys.stderr)
        return E_FAILED

if __name__ == "__main__":
    sys.exit(main())
