# MANIFEST

Map of the `eudoxys/buildings` repository. Every tracked file is covered by
one row or glob below; check with `python .github/check_manifest.py`.
Update this file in the same PR that adds, moves, or deletes a file.

## Start here

1. `CLAUDE.md` — conventions and working rules
2. `DESIGN.md` — design, decisions, open questions
3. `buildings/__init__.py` — package docs and public API
4. `buildings/buildings.py` — the `Buildings` inventory class

## Task index

- Change an output column: `buildings/buildings.py` (`to_counties` defaults and class docstring), `buildings/__init__.py` Data section, `README.md`, `notebook.py` table columns, `DESIGN.md` Outputs
- Add a CLI option: `buildings/cli.py`, `buildings/__init__.py` Syntax section
- Fix a test: `buildings/_test/`; fixture data in `buildings/_test/conftest.py`
- Rebuild the published inventory: `__main__` block of `buildings/buildings.py`, then `buildings/_make_index.py`; see `buildings/README.md` and the README Maintenance section
- Update docs: docstrings, then `make docs`
- Release: `pyproject.toml` version; see the eudoxys-package skill checklist

## Package

| Path | Purpose | Notes |
|---|---|---|
| `buildings/__init__.py` | package docs, re-exports | pdoc landing page |
| `buildings/cli.py` | CLI `main()` | entry point `buildings`; tested by `_test/test_cli.py` |
| `buildings/buildings.py` | `Buildings` state inventory, `to_counties` | `__main__` rebuilds all states (slow); tested by `_test/test_buildings.py` |
| `buildings/_find_county.py` | county lookup from TIGER shapes | needs `tl_2023_us_county.shp` in the working directory; not tested |
| `buildings/_make_index.py` | writes `US/index.csv` | maintenance script; run from `buildings/` |
| `buildings/README.md` | how to get the TIGER county data | provenance of rebuild inputs |
| `buildings/.gitignore` | generated-output ignores | |

## Tests

| Path | Purpose | Notes |
|---|---|---|
| `buildings/_test/README.md` | how to run tests | |
| `buildings/_test/conftest.py` | synthetic state fixture | |
| `buildings/_test/test_*.py` | tests | all fast and offline |

## Notebook

| Path | Purpose | Notes |
|---|---|---|
| `notebook.py` | marimo notebook to browse the published inventory | published on molab; reads the S3 index |

## Repository

| Path | Purpose | Notes |
|---|---|---|
| `README.md` | user overview | |
| `CLAUDE.md` | assistant guidance | |
| `DESIGN.md` | package design | draft reconstructed from code |
| `MANIFEST.md` | this file | |
| `CONTRIBUTING.md` | contributor guide | approved-issue rule |
| `TODO.md` | roadmap | |
| `pyproject.toml` | packaging | version here |
| `requirements.txt` | dependencies | |
| `Makefile` | `make docs`, `make test` | |
| `LICENSE` | MIT | |
| `.gitignore` | | GitHub Python template plus `/US/` |
| `.gitattributes` | | |
| `.github/workflows/*.yaml` | CI: tests, docs, approved-issue check, issue assignment | |
| `.github/check_manifest.py` | checks this file | |

## Don't read

`docs/` (generated), `.venv/`, `US/` (generated inventory, large), TIGER `tl_*` files, `**/__marimo__/` session files.
