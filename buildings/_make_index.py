"""Generate inventory index"""

import os
import stat

import pandas as pd

PATH = "../US"
URL = "https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/US"
REFRESH = False

def _make_index():
	"""Make index files"""
	csvpath = f"{PATH}/index.csv"
	data = None
	if os.path.exists(csvpath) and not REFRESH:
		try:
			data = pd.read_csv(csvpath,index_col=["country","state","county"])
		except Exception as err:
			print(f"ERROR [_make_index.py]: {csvpath=} {err=}")
	if data is None:
		data = []
		for state in sorted([x for x in os.listdir(PATH) if os.path.isdir(f"{PATH}/{x}")]):
			for file in sorted([x for x in os.listdir(f"{PATH}/{state}") if x.endswith(".csv.gz")]):
				county = " ".join(file.split()[:-1])
				print(file,end="... ",flush=True)
				n = len(pd.read_csv(f"{PATH}/{state}/{file}"))
				data.append(pd.DataFrame(
					data={
						"country": ["US"],
						"state": [state],
						"county": [county],
						"buildings": [n],
						"url": [f"{URL}/{state}/{file}"],
					}))
				print(n,"buildings")
		data = pd.concat(data).set_index(["country","state","county"])
		data.to_csv(csvpath,index=True)

	# write index HTML
	state = data.groupby(["country","state"])["buildings"].sum().to_frame("buildings[k]").round(-2)/1e3

if __name__ == '__main__':
	_make_index()