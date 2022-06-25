from data_generator import DataGenerator
from analysis import Analysis
from geojson_generator import *
from utils import *
from graphics import Graphics


def main():
    add_all_dir()
    data = DataGenerator('health.xlsx')

    data.get_years_and_regs()
    data_list = [('11', 'абсолютное значение'), ('23', 'от 0-14 лет абс.'), ('23', '15-17 лет абс.'),
                 ('23', 'от 18 абс.'), ('27', '0-14 лет абс.'), ('27', '15-17 лет абс.'), ('27', '18-60 абс.'),
                 ('28', 'мужчины знач'), ('28', 'женщины знач.'), ('31', 'значение')]
    for d in data_list:
        data.generate_csv(d[0], d[1])

    property_list = [[CSV_11, CSV_11_IND[10], CSV_11, CSV_11_IND[0], 'смертность на 100 тыс. нас.', 100000],
                     [CSV_11, CSV_11_IND[8], CSV_11, CSV_11_IND[0], 'рождаемость на 100 тыс. нас.', 100000],
                     [CSV_PROP, CSV_PROP_IND[1], CSV_PROP, CSV_PROP_IND[0], 'естеств. прирост на 100 тыс. нас.',
                      -1],
                     [CSV_31, CSV_31_IND[16], CSV_11, CSV_11_IND[0], 'количество врачей на 100 тыс. нас.', 100000],
                     [CSV_23_0_14, CSV_23_IND[0], CSV_11, CSV_11_IND[2], 'заболеваемость 0-14 лет на 100 тыс. нас.',
                      100000],
                     [CSV_23_15_17, CSV_23_IND[0], CSV_11, CSV_11_IND[4],
                      'заболеваемость 15-17 лет на 100 тыс. нас.', 100000],
                     [CSV_23_18_, CSV_23_IND[0], CSV_11, CSV_11_IND[5], 'заболеваемость от 18 лет на 100 тыс. нас.',
                      100000],
                     [CSV_11, CSV_11_IND[11], CSV_11, CSV_11_IND[3], 'младенческая смертность на 1000 нас.', 1000],
                     [CSV_11, CSV_11_IND[1], CSV_11, CSV_11_IND[0], 'удельный вес сельского нас., %', 100],
                     [CSV_11, CSV_11_IND[6], CSV_11, CSV_11_IND[0], 'работающее население, %', 100],
                     [CSV_28_G, CSV_28_IND[1], CSV_28_B, CSV_28_IND[1], 'число случаев временной нетрудоспособности',
                      -2],
                     [CSV_11, CSV_11_IND[6], CSV_11, CSV_11_IND[0], 'работающее население, %', 100],
                     [CSV_PROP, 'число случаев временной нетрудоспособности', CSV_11, CSV_11_IND[0],
                      'безработица, %', 100],
                     [CSV_27_18_60, CSV_27_IND[0], CSV_11, CSV_11_IND[5], 'психические расстройства в возр. от 18 лет, %', 100],
                     [CSV_27_18_60, CSV_27_IND[1], CSV_11, CSV_11_IND[5],
                      'невротические и соматоформные расстройства в возр. от 18 лет, %', 100],
                     [CSV_27_18_60, CSV_27_IND[2], CSV_11, CSV_11_IND[5], 'другие непсихотические расстройства в возр. от 18 лет, %', 100],
                     [CSV_27_18_60, CSV_27_IND[3], CSV_11, CSV_11_IND[5], 'алкоголизм в возр. от 18 лет, %', 100],
                     [CSV_27_18_60, CSV_27_IND[4], CSV_11, CSV_11_IND[5], 'наркомания от 18 лет, %', 100],
                     [CSV_31, CSV_31_IND[21], CSV_11, CSV_11_IND[0],
                      'число лиц, которым оказана медицинская помощь при выездах на 100 тыс. нас.', 100000],
                     [CSV_11, CSV_11_IND[6], CSV_11, CSV_11_IND[7], 'численность работающих мужчин', -1],
                     [CSV_PROP, CSV_PROP_IND[17], CSV_11, CSV_11_IND[6], 'работающих мужчин, %', 100],
                     [CSV_11, CSV_11_IND[7], CSV_11, CSV_11_IND[6], 'работающих женщин, %', 100],
                     ]

    for p in property_list:
        data.create_property(p[0], p[1], p[2], p[3], p[4], p[5])

    analysis = Analysis()
    graphics = Graphics()

    descriptive_stat_list = [[CSV_PROP, CSV_PROP_IND[0:3], YEAR],
                             [CSV_PROP, CSV_PROP_IND[0:3], SUBJECT]]
    for d in descriptive_stat_list:
        analysis.descriptive_stat(d[0], d[1], d[2])

    graphics.plot_multi_descr_stat(CSV_PROP_IND[0:3], 'медико-демогр. показатели')

    time_series_list = [(CSV_11, CSV_11_IND[0]), (CSV_PROP, 'смертность на 100 тыс. нас.'),
                        (CSV_PROP, 'рождаемость на 100 тыс. нас.')]
    for t in time_series_list:
        analysis.time_series(t[0], t[1])

    group_comparison_list = [[CSV_PROP, 'работающих мужчин, %', CSV_PROP,
                                'работающих женщин, %']
                            ]
    for g in group_comparison_list:
        for factor in [YEAR, SUBJECT]:
            analysis.group_comparison(factor, g[0], g[1], g[2], g[3])

    multi_group_comparison_list = [[[CSV_PROP], ['заболеваемость 0-14 лет на 100 тыс. нас.',
                                                'заболеваемость 15-17 лет на 100 тыс. нас.',
                                                'заболеваемость от 18 лет на 100 тыс. нас.'],
                                                'заболеваемость']]
    for m in multi_group_comparison_list:
        for factor in [YEAR, SUBJECT]:
            analysis.multi_group_comparison(factor, m[0], m[1], m[2])

    corr_regr_list = [[[CSV_27_18_60, CSV_28_B, CSV_PROP], ['безработица, %'], [
        'психические расстройства в возр. от 18 лет, %',
        'невротические и соматоформные расстройства в возр. от 18 лет, %',
        'алкоголизм в возр. от 18 лет, %', 'наркомания от 18 лет, %']],
                      [[CSV_27_18_60, CSV_28_B, CSV_PROP, CSV_31], ['смертность на 100 тыс. нас.'], [
                          'психические расстройства в возр. от 18 лет, %',
                          'безработица, %',
                          'наркомания от 18 лет, %',
                          'число лиц, которым оказана медицинская помощь при выездах на 100 тыс. нас.',
                          'количество врачей на 100 тыс. нас.'
                      ]],
                      [[CSV_PROP, CSV_31], ['рождаемость на 100 тыс. нас.'], [
                          'удельный вес сельского нас., %',
                          'среднедушевой доход населения',
                          'работающее население, %'
                      ]],
                      [[CSV_PROP, CSV_31], ['заболеваемость от 18 лет на 100 тыс. нас.'], [
                          'прожиточный минимум',
                          'безработица, %',
                          'процент лиц с доходами ниже прожиточного минимума',
                          'среднедушевой доход населения',
                          'число лиц, которым оказана медицинская помощь при выездах на 100 тыс. нас.',
                          'количество врачей на 100 тыс. нас.'
                      ]]
                      ]
    for c in corr_regr_list:
        analysis.correlation_regression(c[0], c[1], c[2])

    generate_geojson_from_df_time_series([DISTRICT_POLYGON + 'здоровьеАрхангельска.geojson',
                                          DISTRICT_POLYGON + 'здоровьеКрасноярск.geojson',
                                          DISTRICT_POLYGON + 'здоровьеРеспублика К.geojson',
                                          DISTRICT_POLYGON + 'здоровьеЯмало-Ненецк.geojson'],
                                         TIME_SERIES_DIR + RES, 'общая численность населения: всего',
                                         'прирост', 'abs inc chain&growth inc of chain, %',
                                         'geojson_data/прирост')
    generate_geojson_from_df_prop([DISTRICT_POLYGON + 'здоровьеАрхангельска.geojson',
                                   DISTRICT_POLYGON + 'здоровьеКрасноярск.geojson',
                                   DISTRICT_POLYGON + 'здоровьеРеспублика К.geojson',
                                   DISTRICT_POLYGON + 'здоровьеЯмало-Ненецк.geojson'],
                                  'geojson_data/показатели')

# Предполагается обязательное наличие колонок год, район, субъект
if __name__ == '__main__':
    main()