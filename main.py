import os
import pandas as pd
import scipy.stats as sts
from data import Data
import numpy as np
import matplotlib.pyplot as boxplot
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import math
import scipy
from sklearn.feature_selection import f_regression
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import argparse
from plot import Plot
from utils import YEAR, SUBJECT_WITH_DISTRICT, SUBJECT, DISTRICT, SPACE, \
    YEARS_CSV, DISTRICT_CSV, INDICATOR, CSV


def generate_csv(args):
    file = args.file
    values = args.values.lower()
    indicator_names = args.names.lower()
    sheets = args.sheets.split("&")

    xlsx = pd.ExcelFile(file)
    if sheets is None:
        sheets = xlsx.sheet_names

    for sheet in sheets:
        xlsx_sheet = pd.read_excel(xlsx, sheet)

        # some columns are different case
        xlsx_sheet.columns = xlsx_sheet.columns.str.lower()

        xlsx_sheet[SUBJECT_WITH_DISTRICT] = xlsx_sheet[SUBJECT] + SPACE + xlsx_sheet[DISTRICT]

        districts = Data.get_list(xlsx_sheet, SUBJECT_WITH_DISTRICT)
        years = Data.get_list(xlsx_sheet, YEAR)

        if not os.path.exists(YEARS_CSV) and not os.path.exists(DISTRICT_CSV):
            pd.DataFrame(years).to_csv(YEARS_CSV, index=False)
            pd.DataFrame(districts).to_csv(DISTRICT_CSV, index=False)

        indicators = Data.get_lower_list(xlsx_sheet, indicator_names)

        for indicator in indicators:
            Data.create_sheet(xlsx_sheet, indicator_names, indicator, values, years, districts)


def create_indicator(args):
    file1 = args.file
    file2 = args.file2
    col = args.column
    out_file = args.outfile
    num = float(args.count)

    years = pd.read_csv(YEARS_CSV)['0'].values
    regs = pd.read_csv(DISTRICT_CSV)['0'].values

    Data.create_mark(file1, file2, col, years, regs, out_file, num)
    Plot.checkBD(out_file, INDICATOR)
    file = pd.read_csv(out_file)

    std = file[INDICATOR].std()
    mean = file[INDICATOR].std()
    file_without_std = file[file[INDICATOR] < std + mean]

    file_without_std.to_csv(out_file, index=False)
    Plot.checkBD(out_file, INDICATOR)


def describe_st(args):
    file_name = args.file
    year = args.year

    df = pd.read_csv(file_name)
    data = df
    if (year != None):
        year = int(year)
        data = df[df[YEAR] == year]
    indicator = data[INDICATOR]

    ds = indicator.describe()
    print(ds)

    stat, p = stats.shapiro(indicator)  # тест Шапиро-Уилк
    print('Shapiro-Wilk')
    print('Statistics=%.3f, p-value=%.3f' % (stat, p))
    shapiro_wilk = False
    alpha = 0.05
    if p > alpha:
        shapiro_wilk = True

    print("Shapiro-Wilk: " + str(shapiro_wilk))

    stat, p = stats.normaltest(indicator)  # Критерий согласия Пирсона
    print('Pirson')
    print('Statistics=%.3f, p-value=%.3f' % (stat, p))
    pirson = False
    if p > alpha:
        pirson = True

    print("Pirson: " + str(pirson))

    fig, ax = plt.subplots()
    ax.set_title(file_name.replace('.csv', ''))
    ax.hist(indicator)
    ax.set_xlabel('Показатель в ' + str(year) + ' году')
    ax.set_ylabel('Количество регионов, входящих в интервал')
    plt.show()


def analysis_time_series(args):
    file = args.file
    district = args.names

    df = pd.read_csv(file)
    data = df[df[SUBJECT_WITH_DISTRICT] == district]
    data.drop(columns=[SUBJECT_WITH_DISTRICT], axis=1, inplace=True)

    years_list = data[YEAR].tolist()
    int_y = [int(x) for x in years_list]
    indicators = data[INDICATOR].tolist()
    f_ind = [float(x) for x in indicators]

    fig, ax = plt.subplots()
    ax.plot(int_y, f_ind, 'o-')
    ax.grid(True)
    ax.set_title('Ряд динамики\n' + district + ' с ' + str(years_list[0]) + ' по ' + str(years_list[len(years_list) - 1]) + ' гг.')
    ax.set_xlabel('Год')
    ax.set_ylabel('Показатель')
    plt.show()

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

    data.insert(data.shape[1], 'Абсолют. прирост базисных', abs_inc_basic)
    data.insert(data.shape[1], 'Абсолют. прирост цепных', abs_inc_chain)
    data.insert(data.shape[1], 'Темп роста базисных, %', growth_rate_of_basic)
    data.insert(data.shape[1], 'Темп роста цепных, %', growth_rate_of_chain)
    data.insert(data.shape[1], 'Темп прироста базисных, %', growth_inc_of_basic)
    data.insert(data.shape[1], 'Темп прироста цепных, %', growth_inc_of_chain)

    print(data)

    av_row = (0.5 * (f_ind[0] + f_ind[len(f_ind) - 1]) + sum(f_ind[1:len(f_ind) - 1])) / (data.shape[0] - 1)
    av_abs_inc = (f_ind[len(f_ind) - 1] - f_ind[0]) / (data.shape[0] - 1)
    av_growth_rate = pow(f_ind[len(f_ind) - 1] / f_ind[0], 1 / (data.shape[0] - 1)) * 100
    av_inc_rate = av_growth_rate - 100

    print(district + ' с ' + str(years_list[0]) + ' по ' + str(years_list[len(years_list) - 1]) + ' гг.')
    print()
    print("Средний уровень ряда: " + str(av_row) + " чел.")
    print("Средний абсолютный прирост: " + str(av_abs_inc) + " чел.")
    print("Средний темп роста: " + str(av_growth_rate) + " %")
    print("Средний темп прироста: " + str(av_inc_rate) + " %")


def group_comparison(args):
    file = args.file
    file2 = args.file2
    # names = args.names.split('&')
    dependency = args.dependency

    data = pd.read_csv(file)
    data2 = pd.read_csv(file2)
    name = file.removesuffix(CSV)
    name2 = file2.removesuffix(CSV)

    x = data[INDICATOR]
    y = data2[INDICATOR]

    statx, px = stats.normaltest(x)  # Критерий согласия Пирсона
    staty, py = stats.normaltest(y)
    pirsonx = False
    pirsony = False
    alpha = 0.05
    if px > alpha:
        pirsonx = True
    if py > alpha:
        pirsony = True

    print(name + ': ' + str(round(x.mean(), 1)) + '+-' + str(round(x.std(), 1)))
    print(name2 + ': ' + str(round(y.mean(), 1)) + '+-' + str(round(y.std(), 1)))

    if (pirsonx & pirsony):
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

    # sns.boxplot(df, x='показатель', y='значение')
    plt.boxplot([data['показатель'], data2['показатель']], labels=[name, name2])
    plt.show()


def fisher_criterion(v1, v2):
    return abs(np.mean(v1) - np.mean(v2)) / (np.var(v1) + np.var(v2))


def criterion(r, n):
    return r*np.sqrt((n-2)/(1-r*r))


def corr_regr(args):
    years = pd.read_csv(YEARS_CSV)['0'].values
    regs = pd.read_csv(DISTRICT_CSV)['0'].values

    file1 = args.file
    file2 = args.file2

    data_x = pd.read_csv(file1)
    data_y = pd.read_csv(file2)

    name_x = file1.removesuffix(CSV)
    name_y = file2.removesuffix(CSV)

    data = Data.combine_indicators(data_x, data_y, name_x, name_y, years, regs)

    x = data[name_x].values
    y = data[name_y].values

    fx = [float(n) for n in x]
    fy = [float(n) for n in y]

    slope, intercept, r, p, stderr = stats.linregress(fx, fy)
    print(fisher_criterion(fx, fy))
    print(slope)
    print(intercept)
    print(r)
    print(p)
    print(stderr)

    print()
    t = criterion(r, len(fx))
    t_alpha = sts.t.ppf(0.975, len(fx)-2)
    print(t)
    print(t_alpha)
    print(abs(t)>t_alpha)

    if abs(r) < 0.3:
        print('Связь слабая')
    elif abs(r) > 0.6:
        print('Связь тесная')
    else:
        print('Связь умеренная')

    line = f'Regression line: y={intercept:.2f}+{slope:.2f}x\nr={r:.2f}'
    print(line)
    fig, ax = plt.subplots()

    ax.scatter(fx, fy, c = 'k', s = 2, label='Data points')
    ffy = [x * slope + intercept for x in fx]
    ax.plot(fx, ffy, label=line)

    ax.set_xlabel(name_x)
    ax.set_ylabel(name_y)
    ax.legend(facecolor='white')
    plt.show()


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
    parser.add_argument('-cr', '--correlation_regression', action='store_true', help='Running correlation regression analysis')
    parser.add_argument('-gr', '--group', action='store_true', help='Get csv')

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

    if generate:
        generate_csv(args)

    if indicator:
        create_indicator(args)

    if time_series:
        analysis_time_series(args)

    if descriptive_statistics:
        describe_st(args)

    if group:
        group_comparison(args)

    if correlation_regression:
        corr_regr(args)

# Предполагается обязательное наличие колонок Год, Район, Субъект
if __name__ == "__main__":
    main()
