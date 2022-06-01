import pandas as pd
import os
from utils import YEAR, INDICATOR, CSV, \
    SUBJECT, DISTRICT, CSV_DATA, CSV_PROPERTY, YEARS_CSV, DISTRICT_CSV


class Data:

    @staticmethod
    def get_list(env, column_name):
        list_ = env[column_name].unique()
        return list_

    @staticmethod
    def get_lower_list(env, column_name):
        list_ = env[column_name].str.lower().unique()
        return list_

    @staticmethod
    def create_sheet(sheet_name, xlsx_sheet, property, col_name, data_col_name):
        file_name = str(property).replace(':', ',')
        xlsx_with_indicator = xlsx_sheet[xlsx_sheet[col_name].str.lower() == property]
        indicators = data_col_name.split('&')
        out_file_structure = xlsx_with_indicator[[YEAR, SUBJECT, DISTRICT] + indicators]

        df = pd.DataFrame(out_file_structure)
        for i in indicators:
            # ignore non float values
            df[i].astype(float, errors='ignore')

        dir = CSV_DATA + sheet_name + '/'
        if not os.path.exists(dir):
            os.mkdir(dir)

        df.rename(columns={data_col_name: INDICATOR}, inplace=True)
        df.to_csv(dir + file_name[:28] +
                  file_name[len(file_name) - 1] + CSV, index=False)

    @staticmethod
    def create_mark(csv_1, csv_2, col_name, out_csv, num):
        csv1 = pd.read_csv(csv_1)
        csv2 = pd.read_csv(csv_2)

        years = pd.read_csv(YEARS_CSV)[YEAR].values
        regs = pd.read_csv(DISTRICT_CSV)[[SUBJECT, DISTRICT]].values

        df = pd.DataFrame({YEAR: [], SUBJECT: [], DISTRICT: [], INDICATOR: []})
        for year in years:
            for reg in regs:
                subject = reg[0]
                district = reg[1]
                # get row with identity year, subject and district
                value1 = csv1[(csv1[YEAR] == year) & (csv1[SUBJECT] == subject)
                              & (csv1[DISTRICT] == district)][col_name].tolist()
                value2 = csv2[(csv2[YEAR] == year) & (csv2[SUBJECT] == subject)
                              & (csv2[DISTRICT] == district)][INDICATOR].tolist()
                if (bool(value1) & bool(value2)):
                    df.loc[len(df)] = [year, subject, district,
                                        value1[0] / value2[0] * num]

        dir = CSV_DATA + CSV_PROPERTY
        if not os.path.exists(dir):
            os.mkdir(dir)

        df.to_csv(dir + out_csv, index=False)
        return df


    @staticmethod
    def combine_indicators(data_x, data_y, name_x, name_y):
        years = pd.read_csv(YEARS_CSV)[YEAR].values
        regs = pd.read_csv(DISTRICT_CSV)[[SUBJECT, DISTRICT]].values

        data = pd.DataFrame({YEAR: [], SUBJECT: [], DISTRICT: [], name_x: [], name_y: []})

        for year in years:
            for reg in regs:
                subject = reg[0]
                district = reg[1]
                value1 = data_x[(data_x[YEAR] == year) & (data_x[SUBJECT] == subject)
                              & (data_x[DISTRICT] == district)][INDICATOR].tolist()
                value2 = data_y[(data_y[YEAR] == year) & (data_y[SUBJECT] == subject)
                               & (data_y[DISTRICT] == district)][INDICATOR].tolist()
                if (bool(value1) & bool(value2)):
                    data.loc[len(data)] = [year, subject, district,
                        float(data_x[(data_x[YEAR] == year) & (data_x[SUBJECT] == subject)
                              & (data_x[DISTRICT] == district)][INDICATOR]),
                        float(data_y[(data_y[YEAR] == year) & (data_y[SUBJECT] == subject)
                              & (data_y[DISTRICT] == district)][INDICATOR])]
        return data