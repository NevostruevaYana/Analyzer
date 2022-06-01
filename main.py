import os
import pandas as pd
from data import Data
import numpy as np
from scipy import stats
import argparse
from geoportal import gen_geo_inc, df_to_geojson, read_j
from plot import Plot
from utils import YEAR, SPACE, SUBJECT, DISTRICT, \
    YEARS_CSV, DISTRICT_CSV, INDICATOR, CSV, CSV_DATA, CSV_PROPERTY, gen_label


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

        properties = Data.get_lower_list(xlsx_sheet, prop_col_name)

        for property in properties:
            Data.create_sheet(sheet, xlsx_sheet, property, prop_col_name, value_col_name)


def hampel(values_orig):
    values = values_orig.copy()
    difference = np.abs(values.median() - values)
    median_abs_deviation = difference.median()
    threshold = 6 * median_abs_deviation
    outlier_idx = difference > threshold
    values[outlier_idx] = np.nan
    return values


def create_indicator(file1, file2, col_name, out_file, num):
    df = Data.create_mark(file1, file2, col_name, out_file, num)
    Plot.paintPointDiagram(df, INDICATOR, out_file)

    df_hampel = hampel(df[INDICATOR])
    df[INDICATOR] = df_hampel
    df = df.drop(df[df.isna().T.any()].index)

    file_name = CSV_DATA + CSV_PROPERTY + out_file
    df.to_csv(file_name, index=False)
    Plot.paintPointDiagram(df, INDICATOR, out_file)


def describe_st(file_name, year):
    df = pd.read_csv(file_name)
    if (year != None):
        year = int(year)
        df = df[df[YEAR] == year]
    indicator = df[INDICATOR]

    ds = indicator.describe()
    print(ds)

    # Shapiro-Wilk normal test
    stat, p = stats.shapiro(indicator)
    print('Shapiro-Wilk')
    print('Statistics=%.3f, p-value=%.3f' % (stat, p))
    shapiro_wilk = False
    alpha = 0.05
    if p > alpha:
        shapiro_wilk = True
    if (shapiro_wilk):
        print('Распределение по Шапиро-Уилку нормальное')
    else:
        print('Распределение по Шапиро-Уилку не поддается закону нормального распределения')
    print()

    # Pirson criteria normal test
    stat, p = stats.normaltest(indicator)
    print('Pirson')
    print('Statistics=%.3f, p-value=%.3f' % (stat, p))
    pirson = False
    if p > alpha:
        pirson = True
    if (pirson):
        print('Распределение по критерию Пирсона нормальное')
    else:
        print('Распределение по критерию Пирсона не поддается закону нормального распределения')

    Plot.paintHist(file_name, indicator, year)


def analysis_time_series(file_name, subject, district, geo):
    df = pd.read_csv(file_name)

    data = df[(df[SUBJECT] == subject) & (df[DISTRICT] == district)]

    years_list = data[YEAR].tolist()
    int_y = [int(x) for x in years_list]
    indicators = data[INDICATOR].tolist()
    f_ind = [float(x) for x in indicators]

    abs_inc_basic = list()
    abs_inc_chain = list()
    growth_rate_of_basic = list()
    growth_rate_of_chain = list()
    growth_inc_of_basic = list()
    growth_inc_of_chain = list()
    first_ind = f_ind[0]

    for i in f_ind:
        abs_inc_basic.append(i - f_ind[0])
        abs_inc_chain.append(i - first_ind)
        gg = i / f_ind[0] * 100
        growth_rate_of_basic.append(gg)
        jj = i / first_ind * 100
        growth_rate_of_chain.append(jj)
        growth_inc_of_basic.append(gg - 100)
        growth_inc_of_chain.append(jj - 100)
        first_ind = i

    data.insert(data.shape[1], 'абсолют. прирост базисных', abs_inc_basic)
    data.insert(data.shape[1], 'абсолют. прирост цепных', abs_inc_chain)
    data.insert(data.shape[1], 'темп роста базисных, %', growth_rate_of_basic)
    data.insert(data.shape[1], 'темп роста цепных, %', growth_rate_of_chain)
    data.insert(data.shape[1], 'темп прироста базисных, %', growth_inc_of_basic)
    data.insert(data.shape[1], 'темп прироста цепных, %', growth_inc_of_chain)

    print(subject + district)
    print(data)

    if data.shape[0] != 1:
        av_row = (0.5 * (f_ind[0] + f_ind[len(f_ind) - 1]) + sum(f_ind[1:len(f_ind) - 1])) / (data.shape[0] - 1)
        av_abs_inc = (f_ind[len(f_ind) - 1] - f_ind[0]) / (data.shape[0] - 1)
        av_growth_rate = pow(f_ind[len(f_ind) - 1] / f_ind[0], 1 / (data.shape[0] - 1)) * 100
        av_inc_rate = av_growth_rate - 100

    if not geo:
        print(subject + SPACE + district)
        print('Тенденция роста населения с ' + str(years_list[0]) + ' по ' + str(years_list[len(years_list) - 1]) + ' гг.')
        print()
        print("Средний уровень ряда: " + str(round(av_row, 2)) + " чел.")
        print("Средний абсолютный прирост: " + str(round(av_abs_inc, 2)) + " чел.")
        print("Средний темп роста: " + str(round(av_growth_rate, 2)) + " %")
        print("Средний темп прироста: " + str(round(av_inc_rate, 2)) + " %")

        Plot.paintDynamicDiagram(int_y, f_ind, district, years_list)

    return data


def group_comparison(file, file2, dependency):
    data = pd.read_csv(file)
    data2 = pd.read_csv(file2)

    name = file.removesuffix(CSV)
    name2 = file2.removesuffix(CSV)

    x = data[INDICATOR]
    y = data2[INDICATOR]

    stat_x, px = stats.normaltest(x)  # Критерий согласия Пирсона
    stat_y, py = stats.normaltest(y)
    pirson_x = False
    pirson_y = False
    alpha = 0.05
    if px > alpha:
        pirson_x = True
    if py > alpha:
        pirson_y = True

    print(name + ': ' + str(round(x.mean(), 2)) + '+-' + str(round(x.std(), 2)))
    print(name2 + ': ' + str(round(y.mean(), 2)) + '+-' + str(round(y.std(), 2)))

    if (pirson_x & pirson_y):
        if (dependency):
            # 2 зависимые выборки (normal)
            t = stats.ttest_rel(x, y)
            print(t)
        else:
            # 2 независимые выборки (normal)
            t = stats.ttest_ind(x, y)
            print(t)
    else:
        if (dependency):
            # 2 зависимые группы
            t = stats.wilcoxon(x, y)
            print(t)
        else:
            # 2 независимые группы
            t = stats.mannwhitneyu(x, y)
            print(t)

    if t[1] > 0.05:
        print('Различия выборок не существенны')
    else:
        print('Различия выборок существенны')

    Plot.paintBox(data, data2, name, name2)


def corr_regression(file1, file2):
    data_x = pd.read_csv(file1)
    data_y = pd.read_csv(file2)

    name_x = gen_label(file1)
    name_y = gen_label(file2)

    data = Data.combine_indicators(data_x, data_y, name_x, name_y)
    data = data.drop(data[data.isnull().T.any()].index)

    x = data[name_x].values
    y = data[name_y].values

    fx = [float(n) for n in x]
    fy = [float(n) for n in y]

    slope, intercept, r, p, stderr = stats.linregress(fx, fy)
    print(slope)
    print(intercept)
    print(r)
    print(p)
    print(stderr)

    if abs(r) < 0.3:
        print('Связь слабая')
    elif abs(r) > 0.6:
        print('Связь тесная')
    else:
        print('Связь умеренная')

    print(f'Regression line: y={intercept:.2f}+{slope:.2f}x\n'
          f'Regression coefficient: r={r:.2f}')

    Plot.paintCorrelation(fx, fy, slope, intercept, r, name_x, name_y)


def main():
    # Сброс ограничений на число столбцов
    pd.set_option('display.max_columns', None)

    # Сброс ограничений на количество символов в записи
    pd.set_option('display.max_colwidth', None)

    parser = argparse.ArgumentParser("python main.py")

    parser.add_argument('-g', '--generate', action='store_true', help='Get csv')
    parser.add_argument('-i', '--create_indicator', action='store_true', help='Get csv with new indicator')
    parser.add_argument('-ds', '--descriptive_statistics', action='store_true', help='Running descriptive statistics')
    parser.add_argument('-ts', '--time_series', action='store_true', help='Running time series analysis')
    parser.add_argument('-cr', '--correlation_regression', action='store_true',
                        help='Running correlation regression analysis')
    parser.add_argument('-gr', '--group', action='store_true', help='Get csv')
    parser.add_argument('-geo', '--geo', action='store_true', help='Get csv')

    parser.add_argument('-f', '--file', type=str, help='Input xlsx (csv) file')
    parser.add_argument('-f2', '--file2', type=str, help='Input csv file2')
    parser.add_argument('-fout', '--outfile', type=str, help='Output csv file')

    parser.add_argument('-s', '--sheets', type=str, help='Only some sheets')
    parser.add_argument('-n', '--names', type=str, help='Name')
    parser.add_argument('-y', '--year', type=str, help='Year')
    parser.add_argument('-v', '--values', type=str, help='Column name with values')
    parser.add_argument('-c', '--count', type=str, help='Some number')
    parser.add_argument('-d', '--dependency', action='store_true', help='Dependent sample or not')
    parser.add_argument('-col', '--column', default=INDICATOR, help='Dependent sample or not')

    args = parser.parse_args()

    generate = args.generate
    descriptive_statistics = args.descriptive_statistics
    indicator = args.create_indicator
    time_series = args.time_series
    correlation_regression = args.correlation_regression
    group = args.group
    geo = args.geo
    print()

    if geo:
        file = args.file
        out_file = args.outfile
        gen_geo_inc(file, out_file)

    if generate:
        file = args.file
        sheets = args.sheets.split("&")
        prop_col_name = args.names.lower()
        value_col_name = args.values.lower()
        generate_csv(file, sheets, prop_col_name, value_col_name)

    if indicator:
        file1 = args.file
        file2 = args.file2
        col_name = args.column
        out_file = args.outfile
        num = float(args.count)
        create_indicator(file1, file2, col_name, out_file, num)

    if descriptive_statistics:
        file_name = args.file
        year = args.year
        describe_st(file_name, year)

    if time_series:
        file_name = args.file
        district = args.names

        district = district.split(',')
        subject = district[0]
        district = district[1]

        analysis_time_series(file_name, subject, district, False)

    if group:
        file = args.file
        file2 = args.file2
        dependency = args.dependency
        group_comparison(file, file2, dependency)

    if correlation_regression:
        file1 = args.file
        file2 = args.file2
        corr_regression(file1, file2)


# Предполагается обязательное наличие колонок Год, Район, Субъект
if __name__ == "__main__":
    main()
