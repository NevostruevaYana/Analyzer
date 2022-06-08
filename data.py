import pandas as pd
import os
import numpy as np
from plot import *
from utils import *


# генерация csv-файлов из excel
def generate_csv(file, sheets, prop_col_name, value_col_name):
    xlsx = pd.ExcelFile(file)
    if sheets is None:
        sheets = xlsx.sheet_names

    # read all sheets
    for sheet in sheets:
        xlsx_sheet = pd.read_excel(xlsx, sheet)

        # some columns are different case
        xlsx_sheet.columns = xlsx_sheet.columns.str.lower()

        districts = xlsx_sheet[[SUBJECT, DISTRICT]].drop_duplicates()
        years = xlsx_sheet[YEAR].drop_duplicates()

        # create CSV-files years and districts
        if not os.path.exists(YEARS_CSV) and not os.path.exists(DISTRICT_CSV):
            years.to_csv(YEARS_CSV, index=False)
            districts.to_csv(DISTRICT_CSV, index=False)

        properties = get_lower_list(xlsx_sheet, prop_col_name)

        for property in properties:
            create_csv(sheet, xlsx_sheet, property, prop_col_name, value_col_name)

        files = os.scandir('csv_data/' + sheet)
        for f in files:
            count_arzf(f)


# создание нового показателя
def create_indicator(file1, file2, col_name, out_file, num):
    df = create_new_csv_indicator(file1, file2, col_name, out_file, num)
    paintPointDiagram(df, INDICATOR, out_file)

    df_hampel = hampel(df[INDICATOR])
    df[INDICATOR] = df_hampel

    file_name = CSV_DATA + CSV_PROPERTY + out_file
    df.to_csv(file_name, index=False)
    paintPointDiagram(df, INDICATOR, out_file)


# получение уникальных значений колонки для указанного листа файла
def get_lower_list(sheet, column_name):
    list_ = sheet[column_name].str.lower().unique()
    return list_


# фильтр Хампела для обнаружения выбросов
def hampel(values_orig):
    values = values_orig.copy()
    difference = np.abs(values.median() - values)
    median_abs_deviation = difference.median()
    threshold = 6 * median_abs_deviation
    outlier_idx = difference > threshold
    values[outlier_idx] = np.nan
    return values


# основное преобразование показателя из excel в csv
def create_csv(sheet_name, xlsx_sheet, property, col_name, data_col_name):
    file_name = str(property).replace(':', ',')
    xlsx_with_indicator = xlsx_sheet[xlsx_sheet[col_name].str.lower() == property]
    indicators = data_col_name.split('&')
    out_file_structure = xlsx_with_indicator[[YEAR, SUBJECT, DISTRICT] + indicators]

    df = pd.DataFrame(out_file_structure)
    for i in indicators:
        # ignore non float values
        df[i].astype(float, errors='ignore')

    dir_ = CSV_DATA + sheet_name + '/'
    if not os.path.exists(dir_):
        os.mkdir(dir_)

    df.rename(columns={data_col_name: INDICATOR}, inplace=True)
    df.to_csv(dir_ + file_name[:28] +
              file_name[len(file_name) - 1] + CSV, index=False)


# создание нового показателя
def create_new_csv_indicator(csv_1, csv_2, col_name, out_csv, num):
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
            if bool(value1) & bool(value2):
                df.loc[len(df)] = [year, subject, district,
                                   value1[0] / value2[0] * num]

    dir = CSV_DATA + CSV_PROPERTY
    if not os.path.exists(dir):
        os.mkdir(dir)

    df.to_csv(dir + out_csv, index=False)
    return df


# объединение 2 показателей в один csv
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
