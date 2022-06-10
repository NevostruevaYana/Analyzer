from utils import *


class Data(object):

    def __init__(self):
        self.years = pd.read_csv(YEARS_CSV)[YEAR].values
        self.regs = pd.read_csv(DISTRICT_CSV)[[SUBJECT, DISTRICT]].values

    # получение и запись полного списка лет и регионов
    def get_years_and_regs(self, file, sheet):
        xlsx_sheet = pd.read_excel(file, sheet)

        xlsx_sheet.columns = xlsx_sheet.columns.str.lower()

        districts = xlsx_sheet[[SUBJECT, DISTRICT]].drop_duplicates()
        years = xlsx_sheet[YEAR].drop_duplicates()

        years.to_csv(YEARS_CSV, index=False)
        districts.to_csv(DISTRICT_CSV, index=False)

    # генерация csv-файлов из excel (конвертация бд)
    def generate_csv(self, file_name, sheets, prop_col_name, value_col_name):
        xlsx = pd.ExcelFile(file_name)
        if sheets is None:
            sheets = xlsx.sheet_names

        # read all sheets
        for sheet_name in sheets:
            xlsx_sheet = pd.read_excel(xlsx, sheet_name)

            xlsx_sheet.columns = xlsx_sheet.columns.str.lower()

            properties = get_lower_list(xlsx_sheet, prop_col_name)
            print(properties)

            df_list = []
            for property in properties:
                df = create_csv(xlsx_sheet, property, prop_col_name, value_col_name)
                df_list.append(df)

            df = combine_many_indicators(df_list, properties, self.years, self.regs)

            df = count_arzf(df)
            df.to_csv(CSV_DATA + sheet_name + '_' + value_col_name + CSV, index=False)

    # создание нового показателя

    def create_indicator(self, csv1, col1, csv2, col2, col_fin, num):
        csv = pd.read_csv(csv1)
        csv2 = pd.read_csv(csv2)

        csv[col2] = csv2[col2]

        df = pd.DataFrame({YEAR: [], SUBJECT: [], DISTRICT: [], col_fin: []})
        for _, row in csv.iterrows():
            df.loc[len(df)] = [row[YEAR], row[SUBJECT], row[DISTRICT],
                               row[col1] / row[col2] * num]

        df_hampel = hampel(df[col_fin])
        df[col_fin] = df_hampel
        # df = df.dropna()

        append_col_to_file(CSV_PROP, df, col_fin)

        # paintPointDiagram(df, INDICATOR, out_file)


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
    indicators = data_col_name.split('&')
    out_file_structure = xlsx_with_indicator[[YEAR, SUBJECT, DISTRICT] + indicators]

    df = pd.DataFrame(out_file_structure)
    for i in indicators:
        # ignore non float values
        df[i].astype(float, errors='ignore')

    df.rename(columns={data_col_name: property}, inplace=True)
    return df


def combine_many_indicators(data_list, properties, years, regs):
    columns = list(properties)

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


def count_arzf(df):
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
                        sum[idx] = sum[idx] + row[c]
                else:
                    index = idx
            if index != -1:
                for idx, c in enumerate(columns):
                    if sum[idx] != 0.0:
                        df.at[index, c] = sum[idx]

    return df