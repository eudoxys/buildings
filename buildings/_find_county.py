import geopandas as gpd
from shapely.geometry import Point
from functools import lru_cache

# Download once from: https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip
# Unzip and point to the .shp file
COUNTY_SHAPEFILE_PATH = "tl_2023_us_county.shp"

@lru_cache(maxsize=1)
def _load_counties():
    """
    Load and cache the county boundary shapefile.
    Cached so the (slow) file read only happens once per process.
    """
    gdf = gpd.read_file(COUNTY_SHAPEFILE_PATH)
    # Build a spatial index for fast point-in-polygon lookups
    gdf.sindex
    return gdf


def find_county(lat: float, lon: float) -> dict | None:
    """
    Find the US county containing a given lat/lon using actual
    county border polygons (offline, no API calls).

    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees

    Returns:
        dict with county name, state FIPS, county FIPS, and full GEOID,
        or None if the point doesn't fall inside any county polygon
        (e.g. it's in the ocean or outside the US).
    """
    counties = _load_counties()
    point = Point(lon, lat)  # shapely Point is (x=lon, y=lat)

    # Fast bounding-box pre-filter via spatial index, then exact polygon test
    possible_idx = list(counties.sindex.intersection(point.bounds))
    candidates = counties.iloc[possible_idx]

    match = candidates[candidates.contains(point)]

    if match.empty:
        return None

    row = match.iloc[0]
    return {
        "county": row["NAME"],
        "state_fips": row["STATEFP"],
        "county_fips": row["COUNTYFP"],
        "geoid": row["GEOID"],
    }


# Example usage
if __name__ == "__main__":
    test_coords = [
        (47.6062, -122.3321),  # Seattle, WA -> King County
        (40.7128, -74.0060),   # New York, NY -> New York County
        (34.0522, -118.2437),  # Los Angeles, CA -> Los Angeles County
        (25.0, -80.0),         # Atlantic Ocean -> None
    ]

    for lat, lon in test_coords:
        result = find_county(lat, lon)
        print(f"({lat}, {lon}) -> {result}")
