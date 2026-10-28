[![Validation](https://github.com/eudoxys/buildings/actions/workflows/validate.yaml/badge.svg)](https://github.com/eudoxys/buildings/actions/workflows/validate.yaml)
[![Documentation](https://github.com/eudoxys/buildings/actions/workflows/deploy-pages.yaml/badge.svg)](https://github.com/eudoxys/buildings/actions/workflows/deploy-pages.yaml)

# US building database

`buildings` produces a county-level inventory of US buildings (location,
type, code, floor and ground area, floors, climate zone) from the AutoBEM
database produced by Joshua New at ORNL [1], for people who need
building stock data for energy modeling. The published inventory is hosted on
AWS; the package holds the code that builds it and a notebook to browse it.

Marimo notebook to preview/select/download data is available at https://molab.marimo.io/notebooks/nb_VhE7Lc7yYwafHwJxTQWyni/app.

Data archive index is located at https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/index.csv.

# Documentation

See https://www.eudoxys.com/buildings

# Installation

Install using Eudoxys Package Manager:

    pip install --upgrade eudoxys
    epm install buildings

Install using `pip`:

    pip install git+https://github.com/eudoxys/buildings

# US Building Inventory

The state-level CSV files are the original dataset from ORNL. The state folders contain the county-level datasets generated from the state-level
files.

The county-level files contain the following data

- `location`: the geohash of the building centroid is used as the unique building identifier. The length of the geohash is sufficient to guarantee the location is unique and can be used as a building identifier.

- `buildingtype`: the type of building used for energy simulation in OpenStudio (see reference [1] for details).

- `buildingcode`: the building code/standard used for energy simulation in OpenStudio (see reference [1] for details).

- `floorarea`: the building floor area in square feet.

- `groundarea`: the building footprint area in square feet.

- `floors`: the number of storeys in the building.

- `climatezone`: the climate zone used for energy simulation in OpenStudio (see reference [1] for details).

- `latitude`: the building centroid latitude in degrees north (south is negative).

- `longitude`: the building centroid longitude in degrees east (west is negative).

# Maintenance

## Update docs

    make docs

## Run tests

    pip install -e . pytest
    pytest

The tests are fast and offline; see
[`buildings/_test/README.md`](buildings/_test/README.md).

## Rebuild the inventory

Download the TIGER county shapefile as described in
[`buildings/README.md`](buildings/README.md), set `Buildings.LIBRARY_PATH` to
the AutoBEM state files in the `__main__` block of `buildings/buildings.py`,
then run from the `buildings/` folder:

    python3 buildings.py
    python3 _make_index.py

Generated files go to `US/` (gitignored) and are uploaded to the S3 bucket by
hand. A full rebuild performs a county lookup for every building and is slow.

# Examples

## Command line

    buildings

outputs

    Opening marimo notebook...ok

and opens the notebook in a browser.

## Python

Read one county using the archive index:

    import pandas as pd
    index = pd.read_csv("https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/index.csv",
        index_col=["country","state","county"])
    url = index.loc[("US","WA","King"),"url"].replace(" ","+")
    print(pd.read_csv(url).head())

# Citation

To cite this dataset use the following:

	Chassin, David P., "US Buildings Inventory" (2026). URL: https://www.eudoxys.com/buildings.

# References

[1] New, J. R., Bass, B., & Adams, M. (2023). Automatic Building Energy Modeling (AutoBEM). U.S. Department of Energy. [DOE's OSTI Database](https://www.osti.gov/doecode/biblio/115947).
