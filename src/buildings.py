import os
import pandas as pd

import reverse_geocoder as rg

cache = {}

def find_county(lat: float, lon: float, precision: int=2) -> str:
    """
    Find the county/administrative region for a given latitude and longitude.
    
    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
        precision: rounding error on lat/lon (2~1/2 mile, 3~250 ft, 4~25 ft)
    
    Returns:
        A string with the county/st name

    Raises:
        RuntimeError: unable to resolve location
    """
    pos = (round(lat,precision),round(lon,precision))
    try:
        return cache[pos]
    except KeyError:
        results = rg.search((lat, lon))
        
        if results:
            result = results[0]
            admin2 = result.get("admin2", "")  # County / district
            admin1 = result.get("admin1", "")  # State / province
            country = result.get("cc", "")     # Country code
            
            if admin2:
                result = f"{admin2}, {admin1}, {country}"
            elif admin1:
                result = f"{admin1}, {admin1}, {country}"
            else:
                raise RuntimeError(f"{lat},{lon} has no known state/province in {country}")
        
        else:
            raise RuntimeError("{lat},{lon} location not found")

        cache[pos] = result
        return result


# Example usage
if __name__ == "__main__":

    pd.options.display.max_columns = None
    pd.options.display.width = None

    path = "/Volumes/CHASSIN_3T/AutoBEM"
    for file in sorted(os.listdir(path)):
        cache = {}
        df = pd.read_csv(f"{path}/{file}",
            usecols=["ID","Centroid","Area","Area2D","NumFloors","CZ","BuildingType","Standard"]
            ).rename(
            {
                "ID":"buildingid",
                "Centroid":"location",
                "Area":"floorarea",
                "Area2D":"groundarea",
                "NumFloors":"floors",
                "CZ":"climatezone",
                "BuildingType":"buildingtype",
                "Standard":"buildingcode",
            },axis=1)

        STATE_CODES = {
                "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
                "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
                "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
                "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
                "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
                "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
                "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
                "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
                "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
                "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
                "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
                "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
                "wisconsin": "WI", "wyoming": "WY",
                # Territories & DC
                "district of columbia": "DC", "washington dc": "DC", "washington d.c.": "DC",
                "puerto rico": "PR", "guam": "GU", "us virgin islands": "VI",
                "american samoa": "AS", "northern mariana islands": "MP",
            }
        counties = {}
        for n,data in df.iterrows():
            buildingid = data["buildingid"]
            latlon = tuple(map(lambda x:round(float(x),6),data["location"].split("/")))
            result = find_county(*latlon).split(",")
            county = result[0].split(" ")
            try:
                state = STATE_CODES[result[1].lower().strip()]
            except KeyError as err:
                state = result[1].upper().strip()
            assert state in STATE_CODES.values(), f"{state=} is invalid"
            if county[-1] in ["County","Municipality","Borough","Parish"]:
                county = " ".join(county[:-1])
            else:
                county = " ".join(county)
            county_st = f"{county} {state}"
            print("\033[0G\033[2K",n,buildingid,latlon,county_st,end="...",flush=True)
            if not county_st in counties:
                counties[county_st] = []
            counties[county_st].append(data.to_frame())
        for county,data in counties.items():
            pd.concat(data).to_csv(county,index=False,header=True)
