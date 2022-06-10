import pandas as pd
import os
import numpy as np

YEAR = 'год'
YEAR_GEO = 'year'
SUBJECT_WITH_DISTRICT = 'субъект,район'
SUBJECT = 'субъект'
SUBJECT_GEO = 'subject'
DISTRICT = 'район'
DISTRICT_GEO = 'district'
INDICATOR = 'показатель'
INDICATOR_GEO = 'indicator'
SPACE = ' '
YEARS_CSV = 'годы.csv'
DISTRICT_CSV = 'районы.csv'
CSV = '.csv'
NONE_STR = 'None'
CSV_DATA = 'csv_data/'
CSV_PROPERTY = 'csv_prop/'
DESCRIPTIVE_NAME = 'csv_data/analysis/descriptive_st/descriptive.csv'
TIME_SERIES_NAME = 'csv_data/analysis/time_series/'
GROUP_COMPARISON_NAME = 'csv_data/analysis/group_comparison/results.csv'
CORRELATION = ['слабая', 'сильная', 'умеренная']


# remove dir and extension
def gen_label(name):
    return name.split('/').pop().removesuffix(CSV)


# add value for ARZF districts
def count_arzf(file_name):
    df = pd.read_csv(file_name)

    # get columns with indicator
    cols = df.columns.tolist()
    del cols[0:3]
    cols_len = len(cols)

    arzf_district = 'субъект АЗРФ'

    years = pd.read_csv(YEARS_CSV)[YEAR].values
    regs = pd.read_csv(DISTRICT_CSV)[SUBJECT].values

    for subject in regs:
        value = df[df[SUBJECT] == subject]
        for year in years:
            value_year = value[value[YEAR] == year]
            sum = [0.0] * cols_len
            index = -1
            for idx, row in value_year.iterrows():
                if row[DISTRICT] != arzf_district:
                    for idx, c in enumerate(cols):
                        if row[c] == 'X':
                            continue
                        sum[idx] = sum[idx] + row[c]
                else:
                    index = idx
            if index != -1:
                for idx, c in enumerate(cols):
                    if sum[idx] != 0.0:
                        df.at[index, c] = sum[idx]

    df.to_csv(file_name, index=False)