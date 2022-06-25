import math

import numpy as np
from utils import *


class DataGenerator(object):

    def __init__(self, file_name):
        assert (EXCEL in file_name) | (os.path.exists(file_name)), 'Некорректное имя файла'
        self.file_name = file_name

    # получение и запись полного списка лет и регионов
    def get_years_and_regs(self):
        xlsx_sheet = pd.read_excel(self.file_name, '11')

        xlsx_sheet.columns = xlsx_sheet.columns.str.lower()

        assert (SUBJECT in xlsx_sheet.columns) | (DISTRICT in xlsx_sheet.columns), \
            'Невозможно создать файлы с годами и районами'
        districts = xlsx_sheet[[SUBJECT, DISTRICT]].drop_duplicates()
        years = xlsx_sheet[YEAR].drop_duplicates()

        years.to_csv(YEARS_CSV, index=False)
        districts.to_csv(DISTRICT_CSV, index=False)
        assert os.path.exists(YEARS_CSV), 'Файл с годами не был создан'
        assert os.path.exists(DISTRICT_CSV), 'Файл с районами не был создан'

    # генерация csv-файлов из excel (конвертация бд)
    def generate_csv(self, sheet, value_col_name):
        years = pd.read_csv(YEARS_CSV)[YEAR].values
        districts = pd.read_csv(DISTRICT_CSV)[[SUBJECT, DISTRICT]].values

        xlsx = pd.ExcelFile(self.file_name)
        assert sheet in xlsx.sheet_names, 'Некорректнй лист'

        xlsx_sheet = pd.read_excel(xlsx, sheet)
        xlsx_sheet.columns = xlsx_sheet.columns.str.lower()
        properties = get_lower_list(xlsx_sheet, INDICATOR)

        df_list = []
        for property in properties:
            df = create_csv(xlsx_sheet, property, INDICATOR, value_col_name)
            df_list.append(df)

        columns = list(properties)
        df = combine_many_indicators(df_list, columns, years, districts)
        assert list(df.columns) == [YEAR, SUBJECT, DISTRICT] + columns, 'Файл был сформирован не правильно'

        df = add_azrf(df)
        out_file_name = DATABASE_DIR + sheet + '_' + value_col_name + CSV
        df.to_csv(out_file_name, index=False)
        assert os.path.exists(out_file_name), f'Файл {out_file_name} не был создан'

    # создание нового показателя

    def create_property(self, csv1, col1, csv2, col2, col_fin, num):
        assert (isinstance(num, int)) | (num > -3), 'Неверный параметр num'
        assert os.path.exists(csv1), f'Файла {csv1} не существует'
        df_1 = pd.read_csv(csv1)
        assert os.path.exists(csv2), f'Файла {csv2} не существует'
        df_2 = pd.read_csv(csv2)

        assert col1 in df_1.columns, f'Показателя \'{col1}\' в файле {csv1} не существует'
        assert col2 in df_2.columns, f'Показателя \'{col2}\' в файле {csv2} не существует'
        if col1 == col2:
            col2_new = f'{col2}_2'
            df_2.rename(columns={col2: col2_new}, inplace=True)
            col2 = col2_new
        df_1[col2] = df_2[col2]

        df = pd.DataFrame({YEAR: [], SUBJECT: [], DISTRICT: [], col_fin: []})
        for _, row in df_1.iterrows():
            if num == -1:
                df.loc[len(df)] = [row[YEAR], row[SUBJECT], row[DISTRICT],
                                   row[col1] - row[col2]]
            elif num == -2:
                df.loc[len(df)] = [row[YEAR], row[SUBJECT], row[DISTRICT],
                                   row[col1] + row[col2]]
            else:
                if (row[col2] != 0.0):
                    df.loc[len(df)] = [row[YEAR], row[SUBJECT], row[DISTRICT],
                               row[col1] / row[col2] * num]

        if num > 0:
            df_hampel = hampel(df[col_fin])
            df[col_fin] = df_hampel

        append_col_to_file(CSV_PROP, df, col_fin)


# фильтр Хампела для обнаружения выбросов
def hampel(values_orig):
    values = values_orig.copy()
    difference = np.abs(values.median() - values)
    median_abs_deviation = difference.median()
    threshold = 6 * median_abs_deviation
    outlier_idx = difference > threshold
    values[outlier_idx] = np.nan
    return values


# получение уникальных значений колонки для указанного листа файла
def get_lower_list(sheet, column_name):
    list_ = sheet[column_name].str.lower().unique()
    return list_


# основное преобразование показателя из excel в csv
def create_csv(xlsx_sheet, property, col_name, data_col_name):
    xlsx_with_indicator = xlsx_sheet[xlsx_sheet[col_name].str.lower() == property]
    assert data_col_name in xlsx_with_indicator.columns, 'Некорректное название столбца со значениями'
    out_file_structure = xlsx_with_indicator[[YEAR, SUBJECT, DISTRICT, data_col_name]]

    df = pd.DataFrame(out_file_structure)
    df[data_col_name].astype(float, errors='ignore')
    df.rename(columns={data_col_name: property}, inplace=True)
    return df


# объединяет датафреймы в один
def combine_many_indicators(data_list, columns, years, regs):
    df = pd.DataFrame(columns=[YEAR, SUBJECT, DISTRICT] + columns)

    for year in years:
        for reg in regs:
            subject = reg[0]
            district = reg[1]
            row_list = []
            for idx, data in enumerate(data_list):
                value = data[(data[YEAR] == year) & (data[SUBJECT] == subject) &
                                 (data[DISTRICT] == district)][columns[idx]]
                if bool(value.tolist()):
                    try:
                        row_list.append(float(value))
                    except (ValueError, TypeError):
                        row_list.append(np.nan)
                else:
                    row_list.append(np.nan)
            full_row_list = [year, subject, district] + row_list
            df.loc[len(df)] = full_row_list

    return df


def add_azrf(df):
    columns = df.columns.tolist()
    del columns[0:3]
    columns_len = len(columns)

    arzf_district = 'субъект АЗРФ'

    years = pd.read_csv(YEARS_CSV)[YEAR].values
    regs = pd.read_csv(DISTRICT_CSV)[SUBJECT].values

    for subject in regs:
        value = df[df[SUBJECT] == subject]
        for year in years:
            value_year = value[value[YEAR] == year]
            sum = [0.0] * columns_len
            index = -1
            for idx, row in value_year.iterrows():
                if row[DISTRICT] != arzf_district:
                    for idx, c in enumerate(columns):
                        if row[c] == 'X':
                            continue
                        if not math.isnan(row[c]):
                            sum[idx] = sum[idx] + row[c]
                else:
                    index = idx
            if index != -1:
                for idx, c in enumerate(columns):
                    if sum[idx] != 0.0:
                        df.at[index, c] = sum[idx]

    return df