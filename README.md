# POLITICO Recovery Lab - Capstone data

This repository contains the code and underlying data for [POLITICO's pandemic response scorecard](www.politico.com/interactives/2021/recovery-lab-states-pandemic-covid-ranking/).

[Read the full methodology here](https://www.politico.com/news/2021/12/15/main-recoverylab-capstone-data-methodology-524101). 

To run the analysis script:

1. Clone this repository
1. (optional) Convert to a Python virtual environment (using Python 3.x) and install the depdencies in requirements.txt using `pip install -r requirements.txt`
1. Run `process_data.py`

Below are the details for what is contained in this repository:

### Scripting files

* [process_data.py](process_data.py): Script to clean, analyze and export majority of files contained in this repository. Runs a `main()` function that runs through each of the four data categories used in this analysis: health, economy, social well-being and education. Individual categories can be run or excluded by changing the following variables. `run_master` indicates whether the script should create an averaged score across all categories.
```python
run_health = 	1
run_economy = 	1
run_social = 	1
run_ed = 	0
run_master = 	1

```
NOTE: Education testing data is intentionally not contained in this repository because of limitations discussed [in the methodology](https://www.politico.com/news/2021/12/15/main-recoverylab-capstone-data-methodology-524101).
* [files.json](files.json): Locations for each of the data input files
* [scrape_fbi.py](scrape_fbi.py): Scrapes the FBI's violent crime data pages for each state, with a pause between each state
* [fbi-to-csv.py](fbi-to-csv.py): Converts the raw FBI data to a CSV file
* [parse_bls_states.py](parse_bls_states.py): Convert to convert raw unemployment and jobs HTML files downloaded from BLS's multi-screen search tool. NOTE: This step could be avoided by directly downloading the CSV files from the [BLS website](https://www.bls.gov/). 

### Directories

* [/data/](/data/): Where all data is contained
* [/data/input](/data/input): Raw data files to be used in the analysis. NOTE this does not include education testing files.
* [/data/output](/data/output): All code–generated data files
* [/data/output/scorecard](/data/output/scorecard): All code–generated data files that are used in scorecard

### Data files to note

* [/data/output/scorecard/interactive_data.csv](/data/output/scorecard/interactive_data.csv): Data used to power the POLITICO interactive. 
* [/data/output/scorecard/total_scorecard.csv](/data/output/scorecard/total_scorecard.csv): Summary topline scorecard data
* [/data/input/state-pops.csv](/data/input/state-pops.csv): State populations and age breakdowns from the U.S. Census Bureau.

