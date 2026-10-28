# Inventory rebuild inputs

These files are needed only to rebuild the published inventory; they are
not checked in (see `.gitignore`).

## AutoBEM state files

Source: New, J. R., Bass, B., & Adams, M. (2023). Automatic Building Energy
Modeling (AutoBEM), Oak Ridge National Laboratory,
https://www.osti.gov/doecode/biblio/115947. One CSV per state, read from
`Buildings.LIBRARY_PATH` (set in the `__main__` block of `buildings.py`).
Retrieval date: not recorded.

Columns used: `ID`, `Centroid` (`"latitude/longitude"`), `Area` (floor area,
sq ft), `Area2D` (footprint, sq ft), `NumFloors`, `CZ`, `BuildingType`,
`Standard`.

## TIGER county boundaries

To run the `buildings.py` script you must download the
[TIGER data](https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip)
from the US Census Bureau and extract the following files into this folder:

- `tl_2023_us_county.dbf`
- `tl_2023_us_county.shp`
- `tl_2023_us_county.shx`

`_find_county.py` reads `tl_2023_us_county.shp` from the current working
directory, so run the rebuild from this folder.

## Derived files

- `../US/{ST}.csv.gz`: state inventory with a county per building, written by
  `Buildings(ST)`.
- `../US/{ST}/{County} {ST}.csv.gz`: county files, written by
  `Buildings.to_counties`.
- `../US/index.csv`: building count and URL per county, written by
  `_make_index.py`.
