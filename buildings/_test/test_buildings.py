"""Fast, offline tests of `buildings.Buildings` on synthetic data"""

import os

import pandas as pd

from buildings import Buildings

COLUMNS = ["location","buildingtype","buildingcode","floorarea",
    "groundarea","floors","climatezone","latitude","longitude"]

def test_state_from_local_file(state_cache): # pylint: disable=unused-argument
    """A state frame is read from TARGET_PATH and indexed by county"""
    data = Buildings("XX")
    assert data.index.name == "county"
    assert len(data) == 3
    assert sorted(data.index.unique()) == ["Alpha XX","Beta XX"]
    for column in ["location","floorarea","groundarea","floors",
            "climatezone","buildingtype","buildingcode"]:
        assert column in data.columns

def test_to_counties(state_cache):
    """One file per county, with the documented columns and row counts

    `Beta XX` has a single building, which must still be written as one row.
    """
    files = Buildings("XX").to_counties("XX",path=str(state_cache))
    assert files == {
        f"{state_cache}/XX/Alpha XX.csv.gz": 2,
        f"{state_cache}/XX/Beta XX.csv.gz": 1,
        }
    for file,count in files.items():
        assert os.path.exists(file)
        county = pd.read_csv(file)
        assert list(county.columns) == COLUMNS
        assert len(county) == count
        assert county["location"].str.len().eq(Buildings.GEOHASH_PRECISION).all()
        assert county["location"].is_unique
        assert county["latitude"].between(-90,90).all()
        assert county["longitude"].between(-180,180).all()

def test_to_counties_columns(state_cache):
    """The `columns` argument selects the output columns"""
    files = Buildings("XX").to_counties("XX",path=str(state_cache),
        columns=["location","floorarea"])
    for file in files:
        assert list(pd.read_csv(file).columns) == ["location","floorarea"]

def test_unreadable_state_is_empty(tmp_path,monkeypatch):
    """A state that cannot be read or built gives an empty frame, not an exception"""
    monkeypatch.setattr(Buildings,"TARGET_PATH",str(tmp_path))
    monkeypatch.setattr(Buildings,"LIBRARY_PATH",str(tmp_path / "missing-{state}.csv"))
    assert len(Buildings("XX")) == 0
