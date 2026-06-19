"""Generate US county index"""

import os
import stat

PATH = "../US"
with open(f"{PATH}/index.csv","w") as fh:
	print("country,state,county,url",file=fh)
	for state in sorted([x for x in os.listdir(PATH) if os.path.isdir(f"{PATH}/{x}")]):
		for file in sorted([x for x in os.listdir(f"{PATH}/{state}") if x.endswith(".csv.gz")]):
			county = " ".join(file.split()[:-1])
			print(f"US,{state},{county},https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/US/{state}/{file}",file=fh)
