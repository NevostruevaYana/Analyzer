import math

import numpy as np
import pandas as pd
from utils import YEAR, SUBJECT_WITH_DISTRICT, INDICATOR, CSV, NONE_STR

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
    def create_sheet(xlsx, col_name, indicator, data_col_name, years, regs):
        file_name = str(indicator).replace(':', ',')
        xlsx_with_indicator = xlsx[xlsx[col_name].str.lower() == indicator]
        indicators = data_col_name.split('&')
        out_file_structure = xlsx_with_indicator[[YEAR, SUBJECT_WITH_DISTRICT] + indicators]
        df = pd.DataFrame(out_file_structure)

        df = df.drop(df[df.isnull().T.any()].index)
        # for year in years:
        #     for reg in regs:
        #         if len(df[(df[YEAR] == year) & (df[SUBJECT_WITH_DISTRICT] == reg)]) == 0:
        #             df.loc[len(df)] = [f"{year}", f"{reg}"] + list(np.repeat([f"{None}"], len(df.columns) - 2))

        df.rename(columns={data_col_name: INDICATOR}, inplace=True)
        df.to_csv(file_name[:28] + file_name[len(file_name) - 1] + CSV, index=False)

    @staticmethod
    def create_mark(csv_1, csv_2, col_name, years, regs, out_csv, num):
        csv1 = pd.read_csv(csv_1)
        csv2 = pd.read_csv(csv_2)

        df = pd.DataFrame({YEAR: [], SUBJECT_WITH_DISTRICT: [], INDICATOR: []})
        for reg in regs:
            for year in years:
                a = csv1[(csv1[YEAR] == year) & (csv1[SUBJECT_WITH_DISTRICT] == reg)][col_name].tolist()
                aa = csv2[(csv2[YEAR] == year) & (csv2[SUBJECT_WITH_DISTRICT] == reg)][INDICATOR].tolist()
                if (bool(a)) & (bool(aa)):
                    if (a[0] != NONE_STR) & (aa[0] != NONE_STR) & (aa[0] != '0.0'): #& (a[0] != '0.0') & (aa[0] != '0.0'):
                        if (not math.isnan(float(a[0]))) & (not math.isnan(float(aa[0]))):
                            df.loc[len(df)] = [f"{year}", f"{reg}",
                                               f"{float(a[0]) / float(aa[0]) * num}"]

        df.to_csv(out_csv, index=False)

    @staticmethod
    def combine_indicators(data_x, data_y, name_x, name_y, years, regs):
        data = pd.DataFrame({YEAR: [], SUBJECT_WITH_DISTRICT: [], name_x: [], name_y: []})

        for year in years:
            for reg in regs:
                if len(data_x[(data_x[YEAR] == year) & (data_x[SUBJECT_WITH_DISTRICT] == reg)]) == 1 & \
                        len(data_y[(data_y[YEAR] == year) & (data_y[SUBJECT_WITH_DISTRICT] == reg)]) == 1:
                    if not ((data_x[(data_x[YEAR] == year) & (data_x[SUBJECT_WITH_DISTRICT] == reg)][
                                 INDICATOR].tolist()[
                                 0] == NONE_STR) | (
                                    data_y[(data_y[YEAR] == year) & (data_y[SUBJECT_WITH_DISTRICT] == reg)][
                                        INDICATOR].tolist()[
                                        0] == NONE_STR) |
                            (
                                    data_y[(data_y[YEAR] == year) & (data_y[SUBJECT_WITH_DISTRICT] == reg)][
                                        INDICATOR].tolist()[
                                        0] is None) |
                            (data_x[(data_x[YEAR] == year) & (data_x[SUBJECT_WITH_DISTRICT] == reg)][
                                 INDICATOR].tolist()[
                                 0] is None)
                    ):
                        data.loc[len(data)] = [f"{year}", f"{reg}",
                                               float(data_x[(data_x[YEAR] == year) & (
                                                           data_x[SUBJECT_WITH_DISTRICT] == reg)][INDICATOR]),
                                               float(data_y[(data_y[YEAR] == year) & (
                                                           data_y[SUBJECT_WITH_DISTRICT] == reg)][INDICATOR])]
        return data