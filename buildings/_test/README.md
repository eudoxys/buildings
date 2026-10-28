Testing
-------

From the repository root:

	python3.12 -m venv .venv
	. .venv/bin/activate
	python3 -m pip install --upgrade pip
	pip install -e . pytest
	pytest

All tests are fast (seconds) and offline. They use a small synthetic state
(`XX`) written to a temporary folder by the `state_cache` fixture in
`conftest.py`, so they do not download the AutoBEM source data or need the
TIGER county shapefile. No credentials or environment variables are needed.

test_buildings.py
-----------------

Checks `buildings.Buildings` on the synthetic state: the frame is indexed by
`county` with the documented columns; `to_counties` writes one file per
county with the documented columns, row counts, geohash length and
uniqueness, and valid latitude/longitude; the `columns` argument selects
output columns; and an unreadable state gives an empty frame.

	pytest buildings/_test/test_buildings.py

test_cli.py
-----------

Checks the `buildings` command without opening a browser: the default
command opens the notebook URL, a failure prints a one-line error and
returns nonzero, `--version` works, and unknown commands are rejected.

	pytest buildings/_test/test_cli.py
