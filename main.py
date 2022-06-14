from data_generator import DataGenerator
from analysis import Analysis
from geojson_generator import generate_geojson_from_df
from utils import *


def main():
    add_all_dir()
    data = DataGenerator('health.xlsx')

    data.get_years_and_regs()
    data_list = [(['11'], 'абсолютное значение'), (['23'], 'от 0-14 лет абс.'), (['23'], '15-17 лет абс.'),
                 (['23'], 'от 18 абс.'), (['27'], '0-14 лет абс.'), (['27'], '15-17 лет абс.'), (['27'], '18-60 абс.'),
                 (['28'], 'мужчины знач'), (['28'], 'женщины знач.'), (['31'], 'значение')]
    for d in data_list:
        data.generate_csv(d[0], d[1])

    property_list = [[CSV_11, CSV_11_IND[10], CSV_11, CSV_11_IND[0], 'смертность на 100 тыс. нас.', 100000],
                     [CSV_11, CSV_11_IND[8], CSV_11, CSV_11_IND[0], 'рождаемость на 100 тыс. нас.', 100000],
                     [CSV_PROP, CSV_PROP_IND[1], CSV_PROP, CSV_PROP_IND[0], 'естеств. прирост на 100 тыс. нас.', -1],
                     [CSV_31, CSV_31_IND[16], CSV_11, CSV_11_IND[0], 'количество врачей на 100 тыс. нас.', 100000],
                     [CSV_23_0_14, CSV_23_IND[0], CSV_11, CSV_11_IND[2], 'заболеваемость 0-14 лет на 100 тыс. нас.', 100000],
                     [CSV_23_15_17, CSV_23_IND[0], CSV_11, CSV_11_IND[4], 'заболеваемость 15-17 лет на 100 тыс. нас.', 100000],
                     [CSV_23_18_, CSV_23_IND[0], CSV_11, CSV_11_IND[5], 'заболеваемость от 18 лет на 100 тыс. нас.',100000],
                     [CSV_11, CSV_11_IND[11], CSV_11, CSV_11_IND[3], 'младенческая смертность на 1000 нас.', 1000]]
    for p in property_list:
        data.create_property(p[0], p[1], p[2], p[3], p[4], p[5])

    analysis = Analysis()

    descriptive_stat_list = [[CSV_PROP, CSV_PROP_IND[0:3], YEAR],
                             [CSV_PROP, CSV_PROP_IND[0:3], SUBJECT]]
    for d in descriptive_stat_list:
        analysis.descriptive_stat(d[0], d[1], d[2])

    time_series_list = [(CSV_11, CSV_11_IND[0])]
    for t in time_series_list:
        analysis.time_series(t[0], t[1])

    group_comparison_list = [[CSV_PROP, 'заболеваемость 0-14 лет на 100 тыс. нас.', CSV_PROP,
                                    'заболеваемость 15-17 лет на 100 тыс. нас.', False]]
    for g in group_comparison_list:
        analysis.group_comparison(g[0], g[1], g[2], g[3], g[4])

    corr_regr_list = [[[CSV_27_18_60, CSV_28_B], ['число случаев временной нетрудоспособности'], [
                            'психические расстройства, всего',
                            'невротические, связанные со стрессом и соматоформные расстройства',
                            'синдром зависимости от алкоголя (алкоголизм)',
                            'синдром зависимости от наркотических веществ (наркомания)']]]
    for c in corr_regr_list:
        analysis.multiple_corr_regr(c[0], c[1], c[2])

    generate_geojson_from_df('geojson_data/districts/здоровьеАрхангельска.geojson',
                             TIME_SERIES_DIR + '/общая численность населения, всего.csv',
                                               'прирост', 'abs inc chain&growth inc of chain, %',
                                               'abs&pace in percent', 'geojson_data/pace.geojson')


# Предполагается обязательное наличие колонок Год, Район, Субъект
if __name__ == '__main__':
    main()