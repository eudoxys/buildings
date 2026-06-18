
import os
from warnings import warn

import pandas as pd

from geohash import geohash

pd.options.display.width = None
pd.options.display.max_columns = None

for file in [x for x in os.listdir("US") if x.endswith(".csv") or x.endswith(".csv.gz")]:

    print("Reading",file,flush=True)
    
    data = pd.read_csv(f"US/{file}",
        index_col=[0],
        converters={
            "floorarea": lambda x:round(float(x),1),
            "groundarea": lambda x:round(float(x),1),
            "floors": lambda x:int(float(x)),
        }
        ).sort_index()
    
    # split location into lat/lon
    data[["latitude","longitude"]] = [[round(float(y),6) for y in x.split("/")] for x in data["location"]]

    # replace location with geohash at precision required for unique values
    ok = False
    prec = 8
    while not ok and prec <= 12:
        data["location"] = [geohash(lat,lon,prec) for lat,lon in data[["latitude","longitude"]].values]
        ok = len(data["location"].unique()) == len(data)
        prec += 1
    if not ok:
        warn("building location index is not unique")

    # save to county files
    state = file.replace(".csv","")
    os.makedirs(f"US/{state}",exist_ok=True)
    columns = [
        "location","buildingtype","buildingcode","floorarea",
        "groundarea","floors","climatezone",
        "latitude","longitude",
        ]
    for county in data.index.unique():
        df = data.loc[county,columns].sort_index()
        csvname = county.replace(" City and "," ")
        print(f"  {csvname}: {len(df)} buildings",end="...",flush=True)
        df.to_csv(f"US/{state}/{csvname}.csv.gz",
                index=False,
                compression="gzip",
                )
        print("ok")
