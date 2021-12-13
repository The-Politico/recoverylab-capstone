import json

import pandas as pd
import us 
from scipy import stats

pd.max_rows = 60

def main():
	data_files = import_data_files('files.json')
	state_pops_df = return_state_pops_df(data_files['pops'])

	# sets what to run (1/0 == true/false)
	# ed is set not to run on public version since we are not publishing underlying data
	run_health = 	1
	run_economy = 	1
	run_social = 	1
	run_ed = 		0
	run_master = 	1

	####################################

	if run_health:

		# rank health section
		hosp_rankings = rank_hosps(data_files['hosp'], state_pops_df)
		death_rankings = rank_deaths(data_files['deaths'], state_pops_df)
		vaccine_rankings = rank_vaccines(data_files['vaccines'], state_pops_df)
		testing_rankings = rank_testing(data_files['testing'], state_pops_df, hosp_rankings)

		hosp_rankings.to_csv('data/output/scorecard/hosp_scorecard.csv', index=0)
		death_rankings.to_csv('data/output/scorecard/death_scorecard.csv', index=0)
		vaccine_rankings.to_csv('data/output/scorecard/vaccine_scorecard.csv', index=0)
		testing_rankings.to_csv('data/output/scorecard/testing_scorecard.csv', index=0)

		overall_health_rankings = rank_overall([
				(hosp_rankings, 25, 'hospitalizations'),
				(death_rankings, 25, 'deaths'),
				(vaccine_rankings, 25, 'vax'),
				(testing_rankings, 25, 'covid_testing')
		])
		overall_health_rankings.to_csv('data/output/scorecard/overall_health_scorecard.csv', index=0)




	####################################

	if run_economy:

		# rank economy section
		realgdp_rankings = rank_gdp(data_files['realgdp'])
		unemployment_rankings = rank_unemp_jobs(data_files['unemployment'], 'unemp')
		jobs_rankings = rank_unemp_jobs(data_files['jobs'], 'jobs')

		realgdp_rankings.to_csv('data/output/scorecard/realgdp_scorecard.csv', index=0)
		unemployment_rankings.to_csv('data/output/scorecard/unemployment_scorecard.csv', index=0)
		jobs_rankings.to_csv('data/output/scorecard/jobs_scorecard.csv', index=0)

		overall_economy_rankings = rank_overall([
				(realgdp_rankings, 33.3333333, 'gdp'),
				(unemployment_rankings, 33.3333333, 'unemp'),
				(jobs_rankings, 33.3333333, 'jobs'),
		])
		overall_economy_rankings.to_csv('data/output/scorecard/overall_economy_scorecard.csv', index=0)



	####################################

	if run_social:

		# rank social wellbeing section
		food_rankings = rank_hhpulse(data_files['food_insecurity'])
		usual_expenses_rankings = rank_hhpulse(data_files['usual_expenses'])
		violent_crime_rankings = rank_vcrimes(data_files['violent'], state_pops_df)

		food_rankings.to_csv('data/output/scorecard/food_scorecard.csv', index=0)
		usual_expenses_rankings.to_csv('data/output/scorecard/usual_expenses_scorecard.csv', index=0)
		violent_crime_rankings.to_csv('data/output/scorecard/violent_crime_scorecard.csv', index=0)

		overall_social_rankings = rank_overall([
				(food_rankings, 33.3333333, 'food'),
				(usual_expenses_rankings, 33.3333333, 'expenses'),
				(violent_crime_rankings, 33.3333333, 'violent_crime'),
		])
		overall_social_rankings.to_csv('data/output/scorecard/overall_social_scorecard.csv', index=0)


	####################################

	if run_ed:

		# rank education
		reading_map_rankings = rank_map(data_files['map_testing'], 		"Reading", 		"-1")
		reading_star_rankings = rank_star(data_files['star_NCEs'], 	"EL/Reading"	)
		reading_iready_rankings = rank_iready(data_files['iready_prs_combined'], 	"reading"	)

		reading_weighting_input = [{'name': "map", "test_data": reading_map_rankings, "popcol": 'stud_n_19', 'statecol': "state"},
						{'name': "star", "test_data": reading_star_rankings, "popcol": "Students", 'statecol': "State"},
						{'name': "iready", "test_data": reading_iready_rankings, "popcol": "current_n", 'statecol': "state"}
						]
		

		math_map_rankings = rank_map(data_files['map_testing'], 		"Math", 		"3rd")
		math_star_rankings = rank_star(data_files['star_NCEs'], 	"Math"	)
		math_iready_rankings = rank_iready(data_files['iready_prs_combined'], 	"math"	)

		math_weighting_input = [{'name': "map", "test_data": math_map_rankings, "popcol": 'stud_n_20', 'statecol': "state"},
						{'name': "star", "test_data": math_star_rankings, "popcol": "Students", 'statecol': "State"},
						{'name': "iready", "test_data": math_iready_rankings, "popcol": "current_n", 'statecol': "state"}
						]
		



		reading_weighted_test_rankings = weigh_testing(reading_weighting_input)
		math_weighted_test_rankings = weigh_testing(math_weighting_input)

		enrollment_rankings = rank_onecol(data_files['enrollment'], 'enrollment_change', 'state')

		reading_map_rankings.to_csv('data/output/scorecard/reading_map_scorecard.csv', index=0)
		reading_star_rankings.to_csv('data/output/scorecard/reading_star_scorecard.csv', index=0)
		reading_iready_rankings.to_csv('data/output/scorecard/reading_iready_scorecard.csv', index=0)
		math_map_rankings.to_csv('data/output/scorecard/math_map_scorecard.csv', index=0)
		math_star_rankings.to_csv('data/output/scorecard/math_star_scorecard.csv', index=0)
		math_iready_rankings.to_csv('data/output/scorecard/math_iready_scorecard.csv', index=0)



		reading_weighted_test_rankings.to_csv('data/output/scorecard/reading_weighted_test_scorecard.csv', index=0)
		math_weighted_test_rankings.to_csv('data/output/scorecard/math_weighted_test_scorecard.csv', index=0)
		enrollment_rankings.to_csv('data/output/scorecard/enrollment_scorecard.csv', index=0)


		reading_weighted_test_rankings = group_ed_scores(reading_weighted_test_rankings)
		math_weighted_test_rankings = group_ed_scores(math_weighted_test_rankings)


		overall_ed_rankings = rank_overall([
				(reading_weighted_test_rankings, 33.333333, 'reading_testing_ed'),
				(math_weighted_test_rankings, 33.333333, 'math_testing_ed'),
				(enrollment_rankings, 33.333333, 'enrollment'),
		])
		overall_ed_rankings.to_csv('data/output/scorecard/overall_ed_scorecard.csv', index=0)

		# get_us_ed(overall_ed_rankings)

	####################################

	if run_master:

		overall_dicts = {}

		for item in ['social', 'economy', 'health']: # ,'ed']:
			overall_dicts[item] = "data/output/scorecard/overall_"+ item +"_scorecard.csv"


		total_rankings_df = rank_all(overall_dicts)

		total_rankings_df.to_csv("data/output/scorecard/total_scorecard.csv", index=0)


		get_interactive_data(overall_dicts).to_csv('data/output/scorecard/interactive_data.csv', index=0)




########################################################################


def get_interactive_data(overall_dicts):
	master_list_dicts = []
	master_df = pd.DataFrame()

	overall_dfs = {}

	for item in overall_dicts:
		df = pd.read_csv(overall_dicts[item])
		overall_dfs[item] = df

	def get_renames(cols, topic):
		renames = {}
		for col in cols:
			if "!!" in col:
				renames[col] = col.split("!!")[1] + "_raw"
		renames['overall_score'] = 'overall_score_' + topic
		renames['state'] = "Abbr"
		return renames

	# fill in health data
	keepkeys = ['state', 'overall_score',	'hospitalizations_score',	'deaths_score',	'vax_score',	'covid_testing_score', 'per_100k_!!hospitalizations', 'per_100k_!!deaths', 'Admin_per_100k_!!vax', 'test_per_hosp_!!covid_testing']
	master_df = overall_dfs['health'][keepkeys]
	renames = get_renames(list(keepkeys), 'health')
	master_df = master_df.rename(columns=renames) 
	for col in renames:
		new_name = renames[col]
		if "raw" in new_name:
			master_df[new_name] = round(master_df[new_name],1)
	master_df['rank_health'] = master_df['overall_score_health'].rank(ascending=False, method='max')


	# fill in ed data
	try:
		keepkeys = ["state", "overall_score", "reading_testing_ed_score", "math_testing_ed_score", "enrollment_score", "enrollment_change_!!enrollment", 'group_!!math_testing_ed', 'group_!!reading_testing_ed']
		ed_df = overall_dfs['ed'][keepkeys]
		renames = get_renames(list(keepkeys), 'ed')
		ed_df = ed_df.rename(columns=renames)
		# only showing groups for this
		ed_df['rank_ed'] = ed_df['overall_score_ed'].rank(ascending=False, method='max')
		for col in renames:
			new_name = renames[col]
			if "raw" in new_name:
				try:
					ed_df[new_name] = round(ed_df[new_name] * 100,1)
				except:
					pass
		master_df = master_df.merge(ed_df, on='Abbr', how='left')
	except:
		pass


	# fill in social data
	social_df = overall_dfs['social']
	keepkeys = ['state', 'overall_score', 'food_score', 'expenses_score', 'violent_crime_score', 'percent_over_wk1_!!food', 'percent_over_wk1_!!expenses', 'change_19_20_raw_!!violent_crime']
	renames = get_renames(list(keepkeys), 'social')
	social_df = social_df[keepkeys].rename(columns=renames)
	social_df['rank_social'] = social_df['overall_score_social'].rank(ascending=False, method='max')
	social_df['food_raw'] = social_df['food_raw'] - 1
	social_df['expenses_raw'] = social_df['expenses_raw'] - 1
	social_df['violent_crime_raw'] = social_df['violent_crime_raw'] - 1
	for col in renames:
		new_name = renames[col]
		if "raw" in new_name:
			social_df[new_name] = round(social_df[new_name] * 100,1)
	master_df = master_df.merge(social_df, on='Abbr', how='left')


	# fill in economy data
	economy_df = overall_dfs['economy']
	keepkeys = ['state', 'overall_score', 'gdp_score', 'unemp_score', 'jobs_score', 'changes_mean_!!gdp', 'mean_unemp_changes_!!unemp', 'mean_jobs_changes_!!jobs']
	renames = get_renames(list(keepkeys), 'economy')
	economy_df = economy_df[keepkeys].rename(columns=renames)
	economy_df['gdp_raw'] = economy_df['gdp_raw'] - 1
	economy_df['jobs_raw'] = economy_df['jobs_raw'] - 1
	economy_df['unemp_raw'] = economy_df['unemp_raw'] - 1
	economy_df['rank_economy'] = economy_df['overall_score_economy'].rank(ascending=False, method='max')
	for col in renames:
		new_name = renames[col]
		if "raw" in new_name:
			economy_df[new_name] = round(economy_df[new_name] * 100,1)
	master_df = master_df.merge(economy_df, on='Abbr', how='left')


	# fill in total overall
	total_df = pd.read_csv("data/output/scorecard/total_scorecard.csv")
	total_df = total_df[['state', 'total_score']]
	total_df['total_rank'] = total_df['total_score'].rank(ascending=False, method='max')
	total_df = total_df.rename(columns={"state": "Abbr"})
	master_df = master_df.merge(total_df, on='Abbr', how='left')


	for col in master_df.columns:
		try:
			if 'score' in col:
				master_df[col] = round(master_df[col],0)
			else:
				master_df[col] = round(master_df[col],1)
		except:
			pass

	# add state name column
	master_df['Name'] = master_df['Abbr'].map(lambda x: us.states.lookup(x).name)



	return master_df






def rank_all(overall_dicts):
	overall_dfs = []

	for item in overall_dicts:
		df = pd.read_csv(overall_dicts[item])
		df = df[['state', 'overall_score']]
		overall_dfs.append(df)

	master_df = overall_dfs[0]

	master_df = master_df.add_suffix("_" + list(overall_dicts.keys())[0])
	master_df['state'] = master_df["state_" + list(overall_dicts.keys())[0]]
	master_df.drop("state_" + list(overall_dicts.keys())[0], axis=1, inplace=True)



	for ind, df in enumerate(overall_dfs):
		df["overall_score_"+ list(overall_dicts.keys())[ind]] = df['overall_score']
		df.drop("overall_score", axis=1, inplace=True)
		if ind == 0:
			continue
		master_df = master_df.merge(df, on='state')			

	point_cols = [x for x in list(master_df.columns) if "overall_score" in x]

	master_df['total_score'] = master_df[point_cols].sum(axis=1) / len(overall_dfs)


	# adjust for ED == -1
	# master_df.iloc[master_df['overall_score_ed'] == -1, master_df.columns.get_loc('total_score')] = master_df[master_df['overall_score_ed'] == -1][["overall_score_economy", "overall_score_health", "overall_score_social"]].sum(axis=1) / (len(overall_dfs) -1)

	return master_df.sort_values("total_score")



def rank_overall(overall_data):

	all_states = ['MS', 'OK', 'SD', 'GA', 'WA', 'AL', 'NE', 'AR', 'OR', 'VA', 'ID', 'TX', 'TN', 'MO', 'KS', 'IA', 'OH', 'NV', 'KY', 'MT', 'PA', 'AZ', 'NC', 'IN', 'UT', 'HI', 'MI', 'NM', 'SC', 'LA', 'WY', 'CO', 'NH', 'FL', 'NJ', 'WI', 'ME', 'WV', 'CA', 'IL', 'MD', 'ND', 'DE', 'MN', 'NY', 'CT', 'VT', 'AK', 'MA', 'RI']


	for dataset in overall_data:
		df = dataset[0]
		df['score'] = df['percentile'] * dataset[1]


	missing_state_data = {key: 0 for key in all_states}
	missing_state_scores = {key: 0 for key in all_states}
	state_overall_scores = [{'state': x, 'overall_score': 0} for x in all_states]

	for state in all_states:
		for dataset in overall_data:
			if state not in list(dataset[0]['state']):
				missing_state_data[state] += 1
				missing_state_scores[state] += dataset[1]
			else:
				state_dict = [x for x in state_overall_scores if x['state'] == state][0]
				this_score = dataset[0][dataset[0]['state'] == state].score.sum()
				state_dict['overall_score'] += this_score
				state_dict[dataset[2] + "_score"] = this_score

	for missing_state in missing_state_data:
		state_miss_ct = missing_state_data[missing_state]
		if state_miss_ct > 0:
			state_dict = [x for x in state_overall_scores if x['state'] == missing_state][0]
			score_so_far = state_dict['overall_score']
			max_obs_score_so_far = 100 - missing_state_scores[missing_state]
			missing_score = missing_state_scores[missing_state]
			extrapolated_score = (max_obs_score_so_far + missing_score) * score_so_far / max_obs_score_so_far
			state_dict['overall_score'] = extrapolated_score
			state_dict['missing_categories'] = state_miss_ct

	state_overall_scores_df = pd.DataFrame(state_overall_scores)

	for dataset in overall_data:
		dataset_df = dataset[0].add_suffix("_!!"+dataset[2])
		state_overall_scores_df = state_overall_scores_df.merge(dataset_df, left_on='state', right_on="state_!!" + dataset[2], how='left' )


	# if education doesnt have testing scores, give it a -1 
	if "reading_testing_ed_score" in state_overall_scores_df.columns:
		no_reading = state_overall_scores_df['reading_testing_ed_score'].isna()
		no_math = state_overall_scores_df['math_testing_ed_score'].isna()
		state_overall_scores_df.iloc[(list(no_reading)) and (list(no_math)), state_overall_scores_df.columns.get_loc('overall_score')] = -1


	return state_overall_scores_df.sort_values("overall_score", ascending=0)

def get_us_ed(df):
	df['weight_reading_col'] = df['change_avgd_!!reading_testing_ed']*(df['student_n_!!reading_testing_ed']/df['student_n_!!reading_testing_ed'].sum())
	df['weight_math_col'] = df['change_avgd_!!math_testing_ed']*(df['student_n_!!math_testing_ed']/df['student_n_!!math_testing_ed'].sum())

	print("** us reading overall change ", df['weight_reading_col'].sum())
	print("** us math overall change ",df['weight_math_col'].sum())


def group_ed_scores(df):

	group_names  = ['Little or no learning loss', "Some learning loss", "Most learning loss"]

	df['group'] = ''

	df.iloc[df['change_avgd'] > .99, df.columns.get_loc('group')] = group_names[0]

	remaining_len = len(df[df['group'] != group_names[0]])
	remaining_len_half = round(remaining_len/2,0)

	df = df.reset_index()

	print(df.loc[remaining_len_half]['change_avgd'])


	df.iloc[df['change_avgd'] < df.loc[remaining_len_half]['change_avgd'], df.columns.get_loc('group')] = group_names[2]
	df.iloc[df['group'] == "", df.columns.get_loc('group')] = group_names[1]

	points = {group_names[0]: 1, group_names[1]: 2/3, group_names[2]: 1/3}

	df['percentile'] = df['group'].map(lambda x: points[x])

	hide_cols = [x for x in list(df.columns) if 'change_avg' in x or "zscore" in x]
	df = df.drop(columns=hide_cols)
	
	return df

def rank_iready(filename, subj):
	df = pd.read_csv(filename)

	df['NCE_spring19_' + subj] = df['median_percentile_rank_spr19-' + subj].apply(lambda x: pr_to_NCE(x))
	df['NCE_spring21_' + subj] = df['median_percentile_rank_spr21-' + subj].apply(lambda x: pr_to_NCE(x))


	df[subj + '_change'] = df['NCE_spring21_' + subj] / df['NCE_spring19_' + subj]


	df['current_n'] = df[subj + "_current_n"]

	df['change_data'] = df[subj + "_change"]

	df = df[df['state'] != 'All States']

	return zscore_to_percentile(df, subj + "_change", statecol='state')



def rank_onecol(filename, colname,statecolname):
	df = pd.read_csv(filename)
	if colname == 'enrollment_change':
		df = df[df[colname] != -1]
	return zscore_to_percentile(df,colname, statecol=statecolname)


def weigh_testing(weighting_input):

	data_to_weight = {}

	for test in weighting_input:
		for state in test['test_data']['state']:
			if state not in data_to_weight:
				data_to_weight[state] = get_state_weighing_data(state, weighting_input)



	weighted_data = []


	for state in data_to_weight:
		d = {}
		d['state'] = state
		# if theres just one test for this state
		if len(data_to_weight[state]) == 1:
			d['student_n'] = data_to_weight[state][0]['student_n']
			d['change_avgd'] = data_to_weight[state][0]['change_data']
		# if there are mult tests for this state
		else:
			total_n = sum([int(x['student_n']) for x in data_to_weight[state]])
			change_avg = 0
			for test in data_to_weight[state]:
				change_avg += test['change_data'] * test['student_n'] / total_n
			d['student_n'] = total_n
			d['change_avgd'] = change_avg
		weighted_data.append(d)



	weighted_df = pd.DataFrame(weighted_data)

	return zscore_to_percentile(weighted_df, 'change_avgd', statecol="state")



def get_state_weighing_data(stateabbrv, weighting_input):
	state_data = []
	for test in weighting_input:
		test_df = test['test_data']
		states_in_test = list(test_df['state'])
		if stateabbrv in states_in_test:
			d = {}
			state_row = test_df[test_df['state'] == stateabbrv]
			if len(state_row) > 1:
				# this should not happen!
				print('more than one row for state in here')
				return
			d['zscore'] = state_row['zscore'].sum()
			d['student_n'] = state_row[test['popcol']].sum()
			d['change_data'] = state_row['change_data'].sum()
			state_data.append(d)
	return state_data


def pr_to_NCE(pr):
	return (21.06*stats.norm.ppf(pr/100)) + 50


def rank_star(filepath, subj):
	# this is students grade 2-8
	df = pd.read_csv(filepath)
	df['NCE_change'] = df['NCE_Spring2021_observed_mean'] / df['NCE_Fall2019_observed_mean']
	df = df[df['Subject'] == subj]

	df = df[df['State'].str.contains("AllStates") == False]
	df['change_data'] = df['NCE_change']
	df = zscore_to_percentile(df, 'NCE_change', statecol="State")
	keep_cols = ['state', 'Subject', "Students", 'NCE_change', 'zscore', 'change_data', 'NCE_Spring2021_observed_mean', 'NCE_Fall2019_observed_mean']
	df = df[keep_cols]
	return df

def rank_map(filepath, subj, grade):
	df = pd.read_csv(filepath)


	df = df[df['measurement_scale'] == subj]
	df = df[df['grade'] == grade]
	df = df[df['cohort'] == "cohorts_d"]

	sp_21_df = df[df['term_string'] == "SP '21"]
	fl_19_df = df[df['term_string'] == "FL '19"]


	merged_df = sp_21_df.merge(fl_19_df, on='state', suffixes=('_20', "_19"))

	merged_df['percentile_20_NCE'] = merged_df['percentile_20'].map(lambda x:pr_to_NCE(x))
	merged_df['percentile_19_NCE'] = merged_df['percentile_19'].map(lambda x:pr_to_NCE(x))


	merged_df['NCE_drop'] = merged_df['percentile_20_NCE'] - merged_df['percentile_19_NCE']
	merged_df['NCE_drop_change'] = merged_df['percentile_20_NCE'] / merged_df['percentile_19_NCE']

	keep_cols = ['state', 'NCE_drop', 'stud_n_20', 'stud_n_19', 'NCE_drop_change', 'percentile_20_NCE', 'percentile_19_NCE']


	merged_df = merged_df[keep_cols]
	merged_df['change_data'] = merged_df['NCE_drop_change']


	return zscore_to_percentile(merged_df, 'change_data', statecol="state")






def rank_vcrimes(filepath, state_pops_df):
	df = pd.read_csv(filepath)
	df = df.merge(state_pops_df, left_on='state_abbr', right_on='state_abbrv', how='right', suffixes=("","_y"))


	df['crimes_per_100k'] = df['violent_crime'] *100*1000 / df['population']

	df_2019 = df[df['year'] == 2019]
	df_2020 = df[df['year'] == 2020]

	df_19_20 = df_2019.merge(df_2020, on='state_abbr', suffixes=("_19", "_20"))

	df_19_20['change_19_20_raw'] = df_19_20['violent_crime_20'] / df_19_20['violent_crime_19']

	keep_cols = ['state_abbr', 'population_19', 'year_19', 'violent_crime_19', 'violent_crime_20', 'crimes_per_100k_19', 'crimes_per_100k_20', 'change_19_20_raw']

	return zscore_to_percentile(df_19_20[keep_cols], 'change_19_20_raw', reverse=True, statecol="state_abbr")

def rank_hhpulse(filepath):
	df = pd.read_csv(filepath, skiprows=3)


	states = list(df.Area)[1:52]

	df = df[df.Area.isin(states)]

	min_wk = str(df.Week.min())

	# note for usual expenses this is not week 1 but is week 13 - first wk asked that Q?
	non_week_1_df = df[df.Week!=min_wk]
	week_1_df = df[df.Week==min_wk]

	avg_df = non_week_1_df.groupby("Area").mean().reset_index()

	avg_df = avg_df.merge(week_1_df[['Area', "Percent"]], on='Area', how='left', suffixes=("_avg", "_wk1"))

	
	avg_df['percent_over_wk1'] = avg_df['Percent_avg'] / avg_df['Percent_wk1']


	return zscore_to_percentile(avg_df, 'percent_over_wk1', reverse=True, statecol="Area") 



def rank_unemp_jobs(filepath, desc):
	df = pd.read_csv(filepath)

	states = list(set(list(df.state)))

	list_dicts = df.to_dict('records')

	months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

	new_data = []
	for state in states:
		if state == "Puerto Rico" or state=="Virgin Islands" or state=="VI":
			continue
		d = {}
		d['state'] = state
		state_rows = [x for x in list_dicts if x['state'] == state]
		state_2019_row = [x for x in state_rows if x['Year'] == "2019" or x['Year'] == 2019][0]
		state_2020_row = [x for x in state_rows if x['Year'] == "2020" or x['Year'] == 2020][0]
		state_2021_row = [x for x in state_rows if x['Year'] == "2021" or x['Year'] == 2021][0]


		sum_changes = 0

		for month in months:
			if month in ['Jan', 'Feb']:
				if str(state_2021_row[month]) != "nan":
					d[month + '_change_2021_19'] = float(state_2021_row[month]) / float(state_2019_row[month])
					sum_changes += d[month + '_change_2021_19']
			else:
				if str(state_2021_row[month]) != "nan":
					d[month + '_change_2021_19'] = float(state_2021_row[month]) / float(state_2019_row[month])
					sum_changes += d[month + '_change_2021_19']
				d[month + '_change_2020_19'] = float(state_2020_row[month]) / float(state_2019_row[month])
				sum_changes += d[month + '_change_2020_19']

		# denominator is the number of items in row minus 1 bc we have state name
		d['mean_'+ desc +'_changes'] = sum_changes / (len(d) - 1)

		new_data.append(d)

	df = pd.DataFrame(new_data)
	df = zscore_to_percentile(df, 'mean_'+ desc +'_changes', reverse = desc=="unemp", statecol="state")

	return df





def rank_gdp(filepath):
	df = pd.read_csv(filepath, skiprows=4)
	df = df[df['2021:Q2'].isna()==False]

	pandemic_qs = ["2020:Q2", "2020:Q3", "2020:Q4", "2021:Q1", "2021:Q2"]

	for quarter in pandemic_qs:
		df[quarter + "_over19"] = df[quarter] /  df["2019:" + quarter[-2:]]

	list_dicts = df.to_dict('records')

	for row in list_dicts:
		changes_sum = 0
		for quarter in pandemic_qs:
			changes_sum += row[quarter + "_over19"]
		row['changes_mean'] = changes_sum / len(pandemic_qs)

	df = pd.DataFrame(list_dicts)


	keep_cols = ['GeoName', 'changes_mean']
	keep_cols += [x for x in list(df.columns) if "over" in x]
	df = df[keep_cols]

	remove_states = ["Far West", "Rocky Mountain", "Plains", "Southwest", "Southeast", "United States", "Great Lakes", "New England", "Mideast",]
	df = df[df['GeoName'].isin(remove_states)==False]
	df = zscore_to_percentile(df, "changes_mean", statecol="GeoName")
	return df





def rank_testing(filepath, state_pops_df, hosp_rankings):

	df = pd.read_csv(filepath)
	max_dates = df.groupby('state').max().date


	list_dicts = df.to_dict('records')

	new_data = []

	for item in list_dicts:
		if item['date'] == max_dates[item['state']]:
			new_data.append(item)

	df = pd.DataFrame(new_data)

	df = df.groupby(['state']).sum().reset_index()
	df = df.merge(state_pops_df, left_on='state', right_on='state_abbrv', how='right', suffixes=("","_y"))
	df = df[df['state'].isin(["PR"]) == False]

	df['testing_per_100k'] = 100 * 1000 * df.total_results_reported/df['population']



	# adjust based on hospitalizations
	merged_df = df.merge(hosp_rankings[['state', 'per_100k']], on='state')

	merged_df['test_per_hosp'] = merged_df['testing_per_100k'] / merged_df['per_100k']

	merged_df = zscore_to_percentile(merged_df, "test_per_hosp", statecol="state")

	merged_df = merged_df[['testing_per_100k', 'test_per_hosp', 'state', 'zscore', 'percentile']]

	return merged_df





def rank_vaccines(filepath, state_pops_df):
	df = pd.read_csv(filepath)
	df = df.merge(state_pops_df, left_on='Location', right_on='state_abbrv', how='right', suffixes=("","_y"))
	df = df[df['state_abbrv'].isin([ "PR"]) == False]

	df['Date']= pd.to_datetime(df['Date'])


	max_date = df.Date.max()
	df = df[df['Date'] == max_date][['Location','Date', "Administered", 'population']]
	df['Admin_per_100k'] = df['Administered'] * 100 * 1000 / df['population']


	df = zscore_to_percentile(df, "Admin_per_100k", statecol="Location")
	return df



def zscore_to_percentile(df, zscore_col, reverse=False, statecol='state'):

	reverse_mult = 1
	if reverse == True:
		reverse_mult = -1

	# standardize state naming

	# (this is just because enrollment data)
	df = df[df[statecol].isin(['BUREAU OF INDIAN EDUCATION', 'U.S. VIRGIN ISLANDS']) == False]
	df['state'] = df[statecol].map(lambda x:us.states.lookup(x).abbr)

	# fliter out dc and territories 
	df = df[df['state'].isin(["DC", "GU", "PR", "AS"]) == False]
	df['std_dev'] = df[zscore_col].std(ddof=1)


	df['zscore'] = (df[zscore_col] - df[zscore_col].mean())/df['std_dev']

	
	df['percentile'] = stats.norm.cdf(df['zscore'] * reverse_mult)

	# drop old state column if not `state`
	if statecol != 'state':
		df.drop(columns=[statecol], inplace=True)

	return df.sort_values("zscore")



def rank_deaths(filepath, state_pops_df):
	deaths_df = pd.read_csv(filepath)
	total_deaths_df = deaths_df[['tot_death', 'state']].groupby("state").max().reset_index()
	
	# fold NYC into NY deaths
	total_deaths_df['state'] = total_deaths_df['state'].str.replace("NYC", "NY")
	total_deaths_df = total_deaths_df[['tot_death', 'state']].groupby("state").sum().reset_index()

	# confirmed max total deaths is also the most recent daily data for tot_death
	total_deaths_df_merged = total_deaths_df.merge(state_pops_df, left_on='state', right_on='state_abbrv', how='right', suffixes=("","_y"))
	total_deaths_df_merged = total_deaths_df_merged[total_deaths_df_merged['state_abbrv'].isin([ "PR"]) == False]

	total_deaths_df_merged['deaths_per_capita'] = total_deaths_df_merged['tot_death'] / total_deaths_df_merged['population']
	total_deaths_df_merged['per_100k'] = total_deaths_df_merged['deaths_per_capita'] * 100 * 1000
	# show total number of deaths per 100k, then footnote the score 
	return zscore_to_percentile(total_deaths_df_merged, 'per_100k', True, statecol="state")




def rank_hosps(filepath, state_pops_df):
	hosp_df = pd.read_csv(filepath)
	hosp_df_merged = hosp_df.merge(state_pops_df, left_on='state', right_on='state_abbrv', how='right', suffixes=("","_y"))
	hosp_df_merged = hosp_df_merged[hosp_df_merged['state_abbrv'].isin(["PR"]) == False]
	# when all startes started repoting
	df_filtered_dates = hosp_df_merged[hosp_df_merged['date'] > "2020/03/26"]


	df_filtered_dates['covid_hosp_admissions_per_capita'] = (df_filtered_dates['previous_day_admission_adult_covid_confirmed'] + df_filtered_dates['previous_day_admission_pediatric_covid_confirmed'] )/ df_filtered_dates['population']
	df_filtered_dates['per_100k'] = df_filtered_dates['covid_hosp_admissions_per_capita'] * 100 * 1000

	just_admissions_df = df_filtered_dates[['state', 'per_100k']].groupby("state").sum().reset_index()


	# show average daily hosps per 100k, then footnote the score 
	return zscore_to_percentile(just_admissions_df, 'per_100k', reverse=True, statecol="state")

def adjust_age(df, cat):
	# from here https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html#footnote04
	# updated nov 29
	adjust_factors = {
	"hosp":
		{
		"pop_over_85_pct": 10,
		"pop_75_84_pct": 8,
		"pop_65_74_pct": 5,
		"pop_50_64_pct": 4,
		"pop_40_49_pct": 2,
		"pop_30_39pct": 2,
		"pop_under_30_pct": 1
		},

	"death":
		{
		"pop_over_85_pct": 370,
		"pop_75_84_pct": 150,
		"pop_65_74_pct": 65,
		"pop_50_64_pct": 25,
		"pop_40_49_pct": 10,
		"pop_30_39pct": 4,
		"pop_under_30_pct": 1
		}
	}

	list_dicts = df.to_dict('records')

	for state in list_dicts:
		adjusted_total = 0
		for col in adjust_factors[cat]:
			adjusted_total += state['per_100k'] / (state[col] * adjust_factors[cat][col])
		state['adjusted'] = adjusted_total
	df = pd.DataFrame(list_dicts)

	df[cat + "-per_100k"] = df['per_100k']
	df = df[['state', 'adjusted', 'pop_over_85_pct', cat + "-per_100k"]].sort_values('adjusted').reset_index()

	return df

def import_data_files(filepath):
	with open(filepath, 'r') as ofile:
		contents = ofile.read()
		contents = contents.replace("\n","").replace("\t","")
		return json.loads(contents) 
	ofile.close()

def return_state_pops_df(filepath):
	df = pd.read_csv(filepath)
	list_dicts = df.to_dict('records')
	for item in list_dicts:
		item['state_abbrv'] = us.states.lookup(item['state']).abbr
	return pd.DataFrame(list_dicts)

if __name__ == "__main__":
	main()