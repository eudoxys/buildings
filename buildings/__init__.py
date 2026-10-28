"""US Building Inventory

Syntax
------

    buildings [open] [-h] [-d] [-w] [--version]

Positional arguments
--------------------

  - `open`: open the building inventory marimo notebook in a browser window
    (default)

Optional arguments
------------------

  - `-d|--debug`: enable debug logging and traceback on exceptions

  - `-h|--help`: show this help message and exit

  - `-w|--warning`: enable warning messages from python

  - `--version`: show the package version and exit

Description
-----------

This package generates an inventory of US buildings based on the AutoBEM
database produced by Joshua New at ORNL [1]. The state-level CSV files are
the original dataset from ORNL. The state folders contain the county-level
datasets generated from the state-level files.

The state-level building inventory is located on AWS using the following URL
template:

	https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/US/{state}.csv

The county-level building inventory is located on AWS using the following URL
template:

	https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/US/{state}/{county}+{state}.csv.gz

A comprehensive list of counties is available at

  https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/index.csv

Given a state postal code (e.g., `"AK"`), `buildings.Buildings` returns a
data frame that is expected to satisfy:

  1. **Index.** The index is named `county` and holds `"<county> <state>"`,
     e.g., `"King WA"`. Buildings for which no county is found are dropped.

  2. **Columns.** `location` (centroid as `"latitude/longitude"`),
     `floorarea`, `groundarea`, `floors`, `climatezone`, `buildingtype`, and
     `buildingcode`, as defined below.

  3. **Repeatability.** The result is read from
     `{TARGET_PATH}/{state}.csv.gz` when that file exists, so repeated calls
     return the same frame unless `refresh=True`.

`buildings.Buildings.to_counties` then writes one gzipped CSV per county with
the columns listed below, in which `location` is replaced by a geohash of
precision `buildings.Buildings.GEOHASH_PRECISION` and the centroid is split
into `latitude` and `longitude`.

What is not promised
--------------------

  - Building attributes are those of the AutoBEM source [1]; they are not
    checked against any other inventory.

  - Geohash uniqueness is checked but not enforced; a warning is issued when
    two buildings share a geohash at the configured precision.

  - Building a state inventory from source data requires the TIGER county
    shapefile (see `buildings/README.md` in the repository) and a county
    lookup for every building, which is slow for large states. Users of the
    published inventory only need the URLs above.

```mermaid
flowchart LR
    autobem[(AutoBEM state CSV)] --> Buildings
    tiger[(TIGER county shapes)] --> Buildings
    Buildings --> state[US/ST.csv.gz]
    Buildings -- to_counties --> county[US/ST/County ST.csv.gz]
    county --> index[index.csv]
```

Data
----

The county-level files contain the following data

- `location`: the geohash of the building centroid is used as the unique
  building identifier. The length of the geohash is sufficient to guarantee
  the location is unique and can be used as a building identifier.

- `buildingtype`: the type of building used for energy simulation in
  OpenStudio (see reference [1] for details).

- `buildingcode`: the building code/standard used for energy simulation in
  OpenStudio (see reference [1] for details).

- `floorarea`: the building floor area in square feet.

- `groundarea`: the building footprint area in square feet.

- `floors`: the number of storeys in the building.

- `climatezone`: the climate zone used for energy simulation in OpenStudio
  (see reference [1] for details).

- `latitude`: the building centroid latitude in degrees north (south is
  negative).

- `longitude`: the building centroid longitude in degrees east (west is
  negative).

Citation
--------

To cite this dataset or package use the following:

- Chassin, David P., "US Buildings Inventory" (2026). URL:
  https://www.eudoxys.com/buildings.

Package Information
-------------------

- Documentation: https://www.eudoxys.com/buildings

- Notebook: https://molab.marimo.io/notebooks/nb_VhE7Lc7yYwafHwJxTQWyni/app

- Source code: https://github.com/eudoxys/buildings

- Issues: https://github.com/eudoxys/buildings/issues

- License: https://github.com/eudoxys/buildings/blob/main/LICENSE

- Dependencies:

  - [pandas](https://pypi.org/project/pandas)
  - [geopandas](https://pypi.org/project/geopandas)
  - [shapely](https://pypi.org/project/shapely)
  - [geohash](https://github.com/eudoxys/geohash)


References
----------

1. New, J. R., Bass, B., & Adams, M. (2023). Automatic Building Energy Modeling (AutoBEM). U.S. Department of Energy. [DOE's OSTI Database](https://www.osti.gov/doecode/biblio/115947).
"""

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("buildings")
except Exception: # pylint: disable=broad-exception-caught
    __version__ = "dev"

# re-export the public API
from buildings.buildings import Buildings
from buildings.cli import main
