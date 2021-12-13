import json

import pandas as pd

fbi_data = []

with open('data/output/fbi-violent-crimes.json', 'r') as ofile:
	pd.DataFrame(json.loads(ofile.read())).to_csv('data/output/fbi-violent-crimes.csv', index=0)