import time
import json

import requests

key = 'YOUR_KEY_GOES_HERE'

states = ["AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
url = 'https://api.usa.gov/crime/fbi/sapi/api/estimates/states/STATENAME/2010/2020?API_KEY=' + key

all_data = []

for state in states:
	resp = requests.get(url.replace("STATENAME", state))
	json_resp = json.loads(resp.text)
	all_data += json_resp['results']
	with open('data/output/fbi-violent-crimes.json', 'w') as ofile:
		ofile.write(json.dumps(all_data))
	ofile.close()
	time.sleep(2)

