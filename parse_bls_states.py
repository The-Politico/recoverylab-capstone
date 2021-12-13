import pandas as pd


def merge_tables(input_file):

	html_text = ""

	with open(input_file, 'r') as ofile:
		html_text = ofile.read()
	ofile.close()

	dfs = pd.read_html(html_text)

	all_data_dfs = []
	active_state = ""

	for i in range(0,len(dfs)):
		# there are 2 tables for each state - one with metadata about the state and one with the actual data we care about 
		if i % 2==0:
			# this is getting the state name from the first table
			active_state = dfs[i].iloc[2,1]
		else: 
			# this is getting the unemployment data, and adding a column called "state"
			dfs[i]['state'] = active_state
			# if active_state == "Arkansas":
			# 	print(dfs[i])
			dfs[i] = dfs[i][dfs[i]['Year'].str.contains("P") == False]
			for colname in dfs[i].columns:
				dfs[i][colname] = dfs[i][colname].str.replace("\(P\)", "") 
			all_data_dfs.append(dfs[i])


	# combines all of our dataframes into one csv
	if "unemp" in input_file:
		pd.concat(all_data_dfs).to_csv('data/output/unemployment-state-out.csv', index=0)
	if "jobs" in input_file:
		final_df = pd.concat(all_data_dfs)

		print(final_df[final_df['state'] == "Arkansas"])
		pd.concat(all_data_dfs).to_csv('data/output/jobs-state-out.csv', index=0)


merge_tables("data/input/unemployment-state-html.html")
merge_tables("data/input/jobs-state-html.html")

