# CLAUDE.md

Guidance for Claude when working in the `eudoxys/buildings` repository.
General Eudoxys package conventions are in the `eudoxys-package` skill
(`eudoxys/claude`); this file records only what is specific to this package.

## What this is

`buildings` builds a county-level inventory of US buildings from the ORNL
AutoBEM state files, publishes it to the `buildings.eudoxys.com` S3 bucket
(uploaded by hand), and provides a marimo notebook to browse it. Python 3.12,
alpha. The main input is one AutoBEM CSV per state plus the TIGER 2023 county
shapefile; the outputs are `US/{ST}.csv.gz`, `US/{ST}/{County} {ST}.csv.gz`,
and `US/index.csv`.

- Docs site: https://www.eudoxys.com/buildings (pdoc from docstrings)
- Maintainer: David P. Chassin
- CLI entry point: `buildings` -> `buildings.cli:main` (opens the notebook)

## Where things are

- `MANIFEST.md`: map of every file, a task index, and what not to read.
  Read it first instead of listing folders.
- `DESIGN.md`: design reconstructed from the implementation (draft, not
  yet agreed), numbered decisions, and open questions. Follow its
  decisions; ask before departing from one.

Sibling Eudoxys dependencies: `geohash` (`geohash(lat,lon,precision)` for the
building identifier).

## Core conventions

- `Buildings` subclasses `pandas.DataFrame`; construct with a state postal
  code. It reads its local copy `{TARGET_PATH}/{ST}.csv.gz` unless
  `refresh=True`; otherwise it rebuilds from `LIBRARY_PATH`.
- Class attributes (`LIBRARY_PATH`, `TARGET_PATH`, `GEOHASH_PRECISION`, ...)
  are the configuration; the `__main__` block overrides them for a rebuild.
- Column names are lowercase with no separators (`floorarea`, `climatezone`);
  areas are in square feet, coordinates in degrees. These names are part of
  the published data, so don't rename them.
- County keys are `"<county> <ST>"`; county file URLs replace spaces with `+`.
- Failures to read or build a state are logged and give an empty frame.

## Style

Existing modules mix 4-space indentation (`buildings.py`, `cli.py`) and tabs
(`_make_index.py`); match the file you are editing.

## Build, test, docs

```bash
python3.12 -m venv .venv && . .venv/bin/activate
pip install --upgrade pip && pip install -e . pytest
pytest
python .github/check_manifest.py
make docs
```

Tests are fast and offline (synthetic state `XX`). CI (`validate.yaml`)
runs the manifest check, pylint (informational), and pytest on Python 3.12.
Rebuilding the inventory is slow and needs the AutoBEM files and the TIGER
shapefile; don't run it unprompted.

## Known rough edges (don't "fix" silently; mention or ask)

- `Buildings.__init__` and the maintenance scripts print progress to stdout
  (with ANSI codes) rather than logging; errors now go through `logging`.
- In `Buildings.__init__`, the suffix-stripping line
  `" ".join(county[:-1])` joins characters, not words; it only runs when a
  TIGER `NAME` ends in "County", "Municipality", "Borough" or "Parish".
- The retry loop in `Buildings.__init__` shifts both latitude and longitude
  by the same growing offset to find a county for points on a border.
- `_find_county.py` reads `tl_2023_us_county.shp` from the current working
  directory, so the rebuild must be run from `buildings/`.
- `_make_index.py` computes a per-state summary for an index HTML page but
  doesn't write it.
- `notebook.py` (repo root) is the published molab notebook; keep its
  location unless the molab link is updated too.
- Column names don't encode units (`floorarea` is in sq ft); changing them
  would break published data and its users.

## Working rules

- Never commit `US/` (generated inventory) or the TIGER `tl_*` files; both
  are gitignored.
- When a public signature, column, or output changes, update the docstrings,
  the package docstring, and `README.md` in the same PR.
- Update `MANIFEST.md` when adding, moving, or deleting files, and run
  `python .github/check_manifest.py`.
- The conventional small test case is the synthetic state in
  `buildings/_test/conftest.py`; for a real check use a small state
  (e.g. `DE`), not a full rebuild.
