"""Generate US county index"""

import os
import stat

PATH = "../US"
with open(f"{PATH}/index.csv","w") as fh:
	for state in sorted([x for x in os.listdir(PATH) if os.path.isdir(f"{PATH}/{x}")]):
		for file in sorted([x for x in os.listdir(f"{PATH}/{state}") if x.endswith(".csv.gz")]):
			print(f"US/{state}/{file}",file=fh)
