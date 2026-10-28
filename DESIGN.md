# eudoxys/buildings — package design (draft 1)

Status: draft reconstructed from the implementation at commit `15a1da4`,
2026-10-28; not yet agreed. Each decision below records what the code does
now. Review it, and confirm or reverse each decision.

## Purpose

`buildings` provides a building-by-building inventory of the US building
stock, split into one file per county, for use as input to building energy
and load modeling. It is derived entirely from the ORNL AutoBEM state
datasets [1]; the county of each building is assigned from US Census TIGER
2023 county boundaries.

The package has two audiences:

- **Data users** read the published files from the `buildings.eudoxys.com`
  S3 bucket, directly or through the marimo notebook (`notebook.py`, opened
  by the `buildings` command). They don't need to run the build.
- **Maintainers** run the build (`Buildings`, `to_counties`, `_make_index.py`)
  to regenerate the published files and upload them by hand.

Excluded: energy simulation, load shapes, and building attributes not in
AutoBEM. These belong in downstream packages that read this inventory.

Coverage: the states present in the AutoBEM release used [1]; country code
`US` only. The AutoBEM vintage and retrieval date are not recorded (see Open
questions).

## Decisions settled

Numbers are permanent: add `Nb` rows for related later decisions; edit a
reversed decision in place and note the date.

| # | Decision |
|---|---|
| 1 | AutoBEM [1] is the only source of building attributes; values are passed through unchanged except for renaming and integer conversion. |
| 2 | Processing unit is the state: `Buildings(state)` builds one state at a time from one AutoBEM CSV per state. |
| 3 | Published unit is the county: one gzipped CSV per county, so users download only the area they need. |
| 4 | County is assigned by point-in-polygon of the building centroid in TIGER 2023 county polygons, offline (no geocoding API). |
| 5 | Buildings whose centroid falls in no county (after a small nudge, see Method step 3) are dropped and logged, not kept with an empty county. |
| 6 | The building identifier is the geohash of its centroid at `GEOHASH_PRECISION = 10`; AutoBEM's `ID` is not published. Uniqueness is checked and a warning issued, not enforced. |
| 7 | Centroid coordinates are published separately as `latitude`/`longitude` in degrees, rounded to 6 decimals. |
| 8 | Published column names are AutoBEM fields renamed to lowercase single words (`floorarea`, `climatezone`); units (sq ft, degrees) are documented, not encoded in names. These names are now part of the published data. |
| 9 | Intermediate state files `{TARGET_PATH}/{ST}.csv.gz` are kept and reused unless `refresh=True`, because the county lookup is slow. |
| 10 | Files are hosted on S3 at `https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/` and uploaded by hand; the repository holds code only, never data. |
| 11 | `US/index.csv` lists every county file with its building count and URL, and is the entry point for users and the notebook. |
| 12 | The `buildings` command opens the hosted notebook; data access in Python is through pandas on the published URLs, not through package functions. |
| 13 | Failure to read or build a state logs an error and returns an empty frame, so a multi-state rebuild continues past a bad state. |

## Conventions inherited from `eudoxys/geohash`

- `geohash(lat,lon,precision)` encodes building locations; precision 10
  gives cells of roughly 1.2 m × 0.6 m.

Other Eudoxys conventions (packaging, CLI, docs, tests) follow the
`eudoxys-package` skill. The `cache` package is not used (see Open questions).

## Module layout

```
buildings/
  __init__.py       package docs; re-exports Buildings, main
  buildings.py      Buildings(state, refresh=False): state inventory frame;
                    Buildings.to_counties(state, path, columns): county files;
                    __main__: rebuild all states
  cli.py            main(): `buildings [open]` opens the notebook
  _find_county.py   find_county(lat, lon): TIGER point-in-polygon lookup
  _make_index.py    _make_index(): writes US/index.csv
notebook.py         marimo notebook: browse the published inventory
```

### Constructor and columns

```python
Buildings(state:str, refresh:bool=False)
```

returns a `pandas.DataFrame` subclass indexed by `county`.

| object | index | columns |
|---|---|---|
| `Buildings(state)` | `county` (`"<county> <ST>"`) | `location` (`"lat/lon"`), `floorarea`, `groundarea`, `floors`, `climatezone`, `buildingtype`, `buildingcode` |
| county file (`to_counties`) | none | `location` (geohash), `buildingtype`, `buildingcode`, `floorarea`, `groundarea`, `floors`, `climatezone`, `latitude`, `longitude` |
| `index.csv` | `country`, `state`, `county` | `buildings`, `url` |

## Sources

| output | primary source | fallback | anchor/reconciliation |
|---|---|---|---|
| building attributes | AutoBEM state CSV [1] (`LIBRARY_PATH`) | none | none |
| county | TIGER 2023 county shapefile (`tl_2023_us_county`) | nudged centroid (Method step 3) | none |
| identifier | geohash of AutoBEM centroid | none | uniqueness warning |

## Method

1. **Read state.** If `{TARGET_PATH}/{ST}.csv.gz` exists and `refresh` is
   false, read it and stop. Otherwise read the AutoBEM CSV at
   `LIBRARY_PATH`, keeping `ID`, `Centroid`, `Area`, `Area2D`, `NumFloors`,
   `CZ`, `BuildingType`, `Standard`; convert areas and floors to integers;
   rename to the published names; sort by centroid.
2. **Locate.** Round each centroid to `LATLON_PRECISION = 5` decimals and
   find the containing TIGER county polygon.
3. **Nudge.** If no county contains the point, add an offset to both
   latitude and longitude, starting at 1e-7° and doubling while below 1e-4°,
   and retry.
4. **Drop.** Buildings still without a county are logged and dropped.
5. **Key.** County key is the TIGER `NAME` plus the state code, e.g.
   `"King WA"`.
6. **Save state.** Index by county, sort, and write `{TARGET_PATH}/{ST}.csv.gz`.
7. **Split.** `to_counties` splits the centroid into `latitude`/`longitude`
   (6 decimals), replaces `location` with the geohash, warns if geohashes
   are not unique, and writes one file per county.
8. **Index.** `_make_index.py` counts the rows of every county file and
   writes `index.csv` with the S3 URL of each.

Building counts are not reconciled against AutoBEM totals; dropped
buildings are only reported in the log.

## Outputs

### County file `US/{ST}/{County} {ST}.csv.gz`

Key: `location` (geohash; unique within the file by intent, see decision 6).

| column | dtype | notes |
|---|---|---|
| `location` | str | geohash, 10 characters |
| `buildingtype` | str | AutoBEM/OpenStudio building type |
| `buildingcode` | str | AutoBEM/OpenStudio code or standard |
| `floorarea` | int | sq ft |
| `groundarea` | int | footprint, sq ft |
| `floors` | int | storeys |
| `climatezone` | str | AutoBEM climate zone |
| `latitude` | float | degrees north, 6 decimals |
| `longitude` | float | degrees east, 6 decimals |

Example rows (values are illustrative only):

```
location,buildingtype,buildingcode,floorarea,groundarea,floors,climatezone,latitude,longitude
c23nb62w20,SingleFamily,90.1-2004,1800,900,2,4C,47.606200,-122.332100
c23nb6x1kq,MediumOffice,90.1-2013,25000,5000,5,4C,47.610000,-122.340000
```

### `US/index.csv`

Key: `(country, state, county)`.

| column | dtype | notes |
|---|---|---|
| `country` | str | `US` |
| `state` | str | postal code |
| `county` | str | county name without the state code |
| `buildings` | int | rows in the county file |
| `url` | str | S3 URL of the county file (spaces must be replaced by `+` to fetch) |

## Files and formats

- State intermediate: `US/{ST}.csv.gz`, gzipped CSV, indexed by `county`.
- County files: `US/{ST}/{County} {ST}.csv.gz`, gzipped CSV, no index;
  `" City and "` in a county name is replaced by `" "` in the file name.
- Index: `US/index.csv`, plain CSV.
- `US/` is written beside the repository by the maintenance scripts and is
  gitignored. Sizes and building counts per state: not recorded (to
  confirm on real data).

## Dependencies and gaps in sibling packages

| need | status |
|---|---|
| geohash encoding | `geohash.geohash` ✔ |
| county lookup | none; private `_find_county.py` |
| cached downloads | not used; local state files instead (decision 9) |

## Known issues to handle

- A county with a single building must still be written as one row (fixed
  in eudoxys/buildings#3; files published before that fix may be wrong).
- TIGER `NAME` normally excludes the "County" suffix; the code that strips
  "County", "Municipality", "Borough" or "Parish" joins characters rather
  than words if it ever runs.
- Centroids on coastlines or borders may fall outside every polygon; the
  nudge in Method step 3 moves diagonally only (assumption: a shift of up
  to about 1e-4° is enough; adjust the loop bounds to change it).
- County names with spaces need `+` in URLs.
- `_find_county.py` reads the shapefile from the working directory, so the
  build runs from `buildings/`.

## Open questions

1. **AutoBEM provenance.** Which AutoBEM release and retrieval date were
   used? Options: record them in `buildings/README.md`, or add a version
   column to `index.csv`.
2. **AutoBEM `ID`.** Should the source building ID be published alongside
   the geohash for traceability? Options: add a column (changes published
   files), or keep geohash only.
3. **County identifier.** Should county files carry the county FIPS
   (`GEOID`, which `find_county` already returns) to avoid name ambiguity?
   Options: add to `index.csv` only, or to file names as well.
4. **Dropped buildings.** Should dropped counts per state be written to the
   index or a log file rather than only logged?
5. **Territories and DC.** The rebuild loop lists territories and DC; are
   they in scope if AutoBEM covers them?
6. **Python data access.** Should the package offer a function that loads a
   county from S3 (e.g. `Buildings.county(state, county)`), instead of
   users building URLs themselves?
7. **Caching.** Should state intermediates move to the Eudoxys `cache`
   package, per the package guidelines, instead of `TARGET_PATH`?

## References

1. New, J. R., Bass, B., & Adams, M. (2023). Automatic Building Energy
   Modeling (AutoBEM). U.S. Department of Energy.
   https://www.osti.gov/doecode/biblio/115947
