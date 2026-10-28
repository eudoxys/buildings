"""Shared test setup

The package has no download cache, so there is no `BUILDINGS_CACHEDIR`.
The `state_cache` fixture writes a small synthetic state file where
`buildings.Buildings` looks for its local copy, so tests never download the
AutoBEM source or need the TIGER county shapefile.
"""

import pandas as pd
import pytest

from buildings import Buildings

@pytest.fixture
def state_cache(tmp_path,monkeypatch):
    """Point `Buildings.TARGET_PATH` at a temporary folder holding `XX.csv.gz`

    Returns the temporary folder.
    """
    data = pd.DataFrame({
        "county": ["Alpha XX","Alpha XX","Beta XX"],
        "location": ["47.60620/-122.33210","47.61000/-122.34000","46.00000/-120.00000"],
        "floorarea": [1000,25000,1800],
        "groundarea": [1000,5000,900],
        "floors": [1,5,2],
        "climatezone": ["4C","4C","5B"],
        "buildingtype": ["SingleFamily","MediumOffice","SingleFamily"],
        "buildingcode": ["90.1-2004","90.1-2013","90.1-2004"],
        })
    data.to_csv(tmp_path / "XX.csv.gz",index=False,compression="gzip")
    monkeypatch.setattr(Buildings,"TARGET_PATH",str(tmp_path))
    return tmp_path
