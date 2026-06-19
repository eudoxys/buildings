"""Buildings inventory
"""

import os
from time import time
from datetime import timedelta
from warnings import warn

import pandas as pd
from _find_county import find_county
import reverse_geocoder as rg

from geohash import geohash

class Buildings(pd.DataFrame):

    LIBRARY_PATH = "https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/US/{state}.csv"

    VERBOSE = False
    ANSI = True
    TARGET_PATH = "US"
    LATLON_PRECISION = 5
    GEOHASH_PRECISION = 10

    def __init__(self,
        state:str,
        refresh:bool=False,
        ):
        """Construct a state building database

        Arguments
        ---------

        - `state`: state postal code, e.g., "AK"

        - `refresh`: force refresh of local file from source data
        """
        cache = {}
        file = self.LIBRARY_PATH.format(state=state)
        if self.VERBOSE: print("Downloading",file,end="...",flush=True)
        pathname = f"{self.TARGET_PATH}/{state}.csv.gz"
        if os.path.exists(pathname) and not refresh:
            df = pd.read_csv(pathname).set_index("county")
        else:
            df = pd.read_csv(file,
                usecols=["ID","Centroid","Area","Area2D","NumFloors","CZ","BuildingType","Standard"],
                converters={
                    "Area": lambda x: int(float(x)),
                    "Area2D": lambda x: int(float(x)),
                    "NumFloors": lambda x: int(float(x)),
                }
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
                },axis=1).set_index("buildingid").sort_values(["location"])
            if self.VERBOSE: print("ok")

            counties = []
            N = len(df)
            tic = time()
            eta = None
            n = 0
            last_eta = None
            last_pcdone = None
            for buildingid,data in df.iterrows():
                n += 1
                latlon = tuple(map(lambda x:round(float(x),self.LATLON_PRECISION),data["location"].split("/")))
                county = find_county(*latlon)["county"]
                if county.split()[-1] in ["County","Municipality","Borough","Parish"]:
                    county = " ".join(county[:-1])
                county_st = f"{county} {state}"
                toc = time()
                eta = round((toc-tic)*(N-n)/n,0)
                counties.append(county_st)
                if self.VERBOSE: 
                    print(f"{'\033[0G\033[2K' if self.ANSI else ''}Processing {state} record {n} of {N} {buildingid=} {latlon=} {county_st=} ({n/N*100:.1f}% done, {n/(toc-tic):.0f}/sec, {timedelta(seconds=eta)} to go)...",flush=True)
                else:
                    pcdone = f"{n/N*100:.1f}"
                    if last_pcdone != pcdone or last_eta != eta:
                        print(f"{'\033[0G\033[2K' if self.ANSI else ''}Processing {state} ({pcdone}% done, ETA {timedelta(seconds=eta)})",flush=True,end="..." if self.ANSI else None)
                        last_pcdone = pcdone
                        last_eta = eta
            print("done")
            df["county"] = counties
            df.set_index("county",inplace=True)
            df.sort_index(inplace=True)
            os.makedirs(os.path.dirname(pathname),exist_ok=True)
            df.to_csv(pathname,index=True,header=True,compression="gzip")
        super().__init__(df)

    def to_counties(self,
        state,
        path:str|None=None,
        columns:list[str]|None=None,
        ):
        """Write county-level building inventory files

        Arguments
        ---------

        - `state`: state of which to write county files
        
        - `path`: path to read/write

        - `columns`: columns to output to CSV
        """
        if path is None:
            path = self.TARGET_PATH
        data = self.sort_index()
        
        # split location into lat/lon
        data[["latitude","longitude"]] = [[round(float(y),6) for y in x.split("/")] for x in data["location"]]

        # replace location with geohash at precision required for unique values
        ok = False
        data["location"] = [geohash(lat,lon,self.GEOHASH_PRECISION) for lat,lon in data[["latitude","longitude"]].values]
        if len(data["location"].unique()) < len(data):
            warn(f"{state=} building location index is not unique (try increasing Buildings.GEOHASH_PRECISION)")

        # save to county files
        os.makedirs(f"{path}/{state}",exist_ok=True)
        if columns is None:
            columns = [
                "location","buildingtype","buildingcode","floorarea",
                "groundarea","floors","climatezone",
                "latitude","longitude",
                ]
        files = {}
        for county in data.index.unique():
            df = data.loc[county,columns].sort_index()
            csvname = county.replace(" City and "," ")
            if self.VERBOSE: print(f"  {csvname}: {len(df)} buildings",end="...",flush=True)
            file = f"{path}/{state}/{csvname}.csv.gz"
            df.to_csv(file,index=False,compression="gzip")
            files[file] = len(df)
            if self.VERBOSE: print("ok")

        return files


# Example usage
if __name__ == "__main__":

    from time import time
    from datetime import timedelta

    pd.options.display.max_columns = None
    pd.options.display.width = None

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
        
    Buildings.LIBRARY_PATH = "/Volumes/CHASSIN_3T/AutoBEM/{state}.csv"
    Buildings.TARGET_PATH = "../US"
    try:
        for state in [x for x in STATE_CODES.values() if not os.path.exists(f"{Buildings.TARGET_PATH}/{x}")]:
            print(f"Processing {state}",end="...",flush=True)
            df = Buildings(state)
            df.to_counties(state)
    except KeyboardInterrupt as err:
        print("\nINTERRUPT: Ctrl-C received")
    # except Exception as err:
    #     print("\nEXCEPTION:",err)
