# US building database

Documentation is located at https://www.eudoxys.com/buildings.

Marimo notebook to preview/select/download data is available at https://molab.marimo.io/notebooks/nb_VhE7Lc7yYwafHwJxTQWyni/app.

Data archive index is located at https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/index.csv.

US Building Inventory
---------------------

This package generates an inventory of US buildings based on the AutoBEM database produced by Joshua New at ORNL [1]

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

Citation
--------

To cite this dataset use the following:

	Chassin, David P., "US Buildings Inventory" (2026). URL: https://www.eudoxys.com/buildings.

References
----------

[1] New, J. R., Bass, B., & Adams, M. (2023). Automatic Building Energy Modeling (AutoBEM). U.S. Department of Energy. [DOE's OSTI Database](https://www.osti.gov/doecode/biblio/115947).

