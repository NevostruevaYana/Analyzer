from data import *
from analysis import *
import argparse
from geoportal import *
from utils import YEAR, SPACE, SUBJECT, DISTRICT, \
    YEARS_CSV, DISTRICT_CSV, INDICATOR, CSV, CSV_DATA, CSV_PROPERTY, gen_label


def main():
    # Сброс ограничений на число столбцов
    pd.set_option('display.max_columns', None)

    # Сброс ограничений на количество символов в записи
    pd.set_option('display.max_colwidth', None)

    parser = argparse.ArgumentParser('python main.py')

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
        sheets = args.sheets.split('&')
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
if __name__ == '__main__':
    main()