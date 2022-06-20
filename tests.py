import unittest
from analysis import Analysis
import geojson_generator
from graphics import Graphics
from geojson_generator import *
from data_generator import *
from csv_table_to_doxc import create_docx_table
import timeit


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

    # generate csv
    # def test_ty(self):
    #     with self.assertRaises(AssertionError) as ctx:
    #         DataGenerator('file.csv')
    #     self.assertEqual(ctx.exception.args[0], 'Некорректное имя файла')
    #
    # def test_generate_csv(self):
    #     add_all_dir()
    #     data = DataGenerator('health.xlsx')
    #
    #     data.get_years_and_regs()
    #     data_list = [('11', 'абсолютное значение'), ('23', 'от 0-14 лет абс.'), ('23', '15-17 лет абс.'),
    #                  ('23', 'от 18 абс.'), ('27', '0-14 лет абс.'), ('27', '15-17 лет абс.'), ('27', '18-60 абс.'),
    #                  ('28', 'мужчины знач'), ('28', 'женщины знач.'), ('31', 'значение')]
    #     for d in data_list:
    #         data.generate_csv(d[0], d[1])
    #
    # def test_create_property(self):
    #     data = DataGenerator('health.xlsx')
    #     property_list = [[CSV_11, CSV_11_IND[10], CSV_11, CSV_11_IND[0], 'смертность на 100 тыс. нас.', 100000],
    #                      [CSV_11, CSV_11_IND[8], CSV_11, CSV_11_IND[0], 'рождаемость на 100 тыс. нас.', 100000],
    #                      [CSV_PROP, CSV_PROP_IND[1], CSV_PROP, CSV_PROP_IND[0], 'естеств. прирост на 100 тыс. нас.',
    #                       -1],
    #                      [CSV_31, CSV_31_IND[16], CSV_11, CSV_11_IND[0], 'количество врачей на 100 тыс. нас.', 100000],
    #                      [CSV_23_0_14, CSV_23_IND[0], CSV_11, CSV_11_IND[2], 'заболеваемость 0-14 лет на 100 тыс. нас.',
    #                       100000],
    #                      [CSV_23_15_17, CSV_23_IND[0], CSV_11, CSV_11_IND[4],
    #                       'заболеваемость 15-17 лет на 100 тыс. нас.', 100000],
    #                      [CSV_23_18_, CSV_23_IND[0], CSV_11, CSV_11_IND[5], 'заболеваемость от 18 лет на 100 тыс. нас.',
    #                       100000],
    #                      [CSV_11, CSV_11_IND[11], CSV_11, CSV_11_IND[3], 'младенческая смертность на 1000 нас.', 1000],
    #                      [CSV_11, CSV_11_IND[1], CSV_11, CSV_11_IND[0], 'удельный вес сельского нас., %', 100],
    #                      [CSV_11, CSV_11_IND[6], CSV_11, CSV_11_IND[0], 'работающее население, %', 100],
    #                      [CSV_28_G, CSV_28_IND[1], CSV_28_B, CSV_28_IND[1],
    #                       'число случаев временной нетрудоспособности',
    #                       -2],
    #                      [CSV_11, CSV_11_IND[6], CSV_11, CSV_11_IND[0], 'работающее население, %', 100],
    #                      [CSV_PROP, 'число случаев временной нетрудоспособности', CSV_11, CSV_11_IND[0],
    #                       'безработица, %', 100],
    #                      [CSV_27_18_60, CSV_27_IND[0], CSV_11, CSV_11_IND[5],
    #                       'психические расстройства в возр. от 18 лет, %', 100],
    #                      [CSV_27_18_60, CSV_27_IND[1], CSV_11, CSV_11_IND[5],
    #                       'невротические и соматоформные расстройства в возр. от 18 лет, %', 100],
    #                      [CSV_27_18_60, CSV_27_IND[2], CSV_11, CSV_11_IND[5],
    #                       'другие непсихотические расстройства в возр. от 18 лет, %', 100],
    #                      [CSV_27_18_60, CSV_27_IND[3], CSV_11, CSV_11_IND[5], 'алкоголизм в возр. от 18 лет, %', 100],
    #                      [CSV_27_18_60, CSV_27_IND[4], CSV_11, CSV_11_IND[5], 'наркомания от 18 лет, %', 100],
    #                      [CSV_31, CSV_31_IND[21], CSV_11, CSV_11_IND[0],
    #                       'число лиц, которым оказана медицинская помощь при выездах на 100 тыс. нас.', 100000],
    #                      [CSV_11, CSV_11_IND[6], CSV_11, CSV_11_IND[7], 'численность работающих мужчин', -1],
    #                      [CSV_PROP, CSV_PROP_IND[17], CSV_11, CSV_11_IND[6], 'работающих мужчин, %', 100],
    #                      [CSV_11, CSV_11_IND[7], CSV_11, CSV_11_IND[6], 'работающих женщин, %', 100],
    #                      ]
    #
    #     for p in property_list:
    #         data.create_property(p[0], p[1], p[2], p[3], p[4], p[5])
    #
    # def test_descriptive_stats(self):
    #     analysis = Analysis()
    #     graphics = Graphics()
    #
    #     descriptive_stat_list = [[CSV_PROP, CSV_PROP_IND[0:3]]]
    #     for d in descriptive_stat_list:
    #         for factor in [YEAR, SUBJECT]:
    #             analysis.descriptive_stat(d[0], d[1], factor)
    #
    #     graphics.plot_multi_descr_stat(CSV_PROP_IND[0:3], 'медико-демогр. показатели')
    #
    # def test_time_series(self):
    #     analysis = Analysis()
    #
    #     time_series_list = [(CSV_11, CSV_11_IND[0]), (CSV_PROP, 'смертность на 100 тыс. нас.'),
    #                         (CSV_PROP, 'рождаемость на 100 тыс. нас.')]
    #     for t in time_series_list:
    #         analysis.time_series(t[0], t[1])
    #
    # def test_group_comparison(self):
    #     analysis = Analysis()
    #
    #     group_comparison_list = [[CSV_PROP, 'работающих мужчин, %', CSV_PROP,
    #                               'работающих женщин, %']
    #                              ]
    #     for g in group_comparison_list:
    #         for factor in [YEAR, SUBJECT]:
    #             analysis.group_comparison(factor, g[0], g[1], g[2], g[3])
    #
    #     multi_group_comparison_list = [[[CSV_PROP], ['заболеваемость 0-14 лет на 100 тыс. нас.',
    #                                                  'заболеваемость 15-17 лет на 100 тыс. нас.',
    #                                                  'заболеваемость от 18 лет на 100 тыс. нас.'],
    #                                     'заболеваемость']]
    #     for m in multi_group_comparison_list:
    #         for factor in [YEAR, SUBJECT]:
    #             analysis.multi_group_comparison(factor, m[0], m[1], m[2])
    #
    # def test_correlation_regression(self):
    #     analysis = Analysis()
    #
    #     corr_regr_list = [[[CSV_27_18_60, CSV_28_B, CSV_PROP], ['безработица, %'], [
    #         'психические расстройства в возр. от 18 лет, %',
    #         'невротические и соматоформные расстройства в возр. от 18 лет, %',
    #         'алкоголизм в возр. от 18 лет, %', 'наркомания от 18 лет, %']],
    #                       [[CSV_27_18_60, CSV_28_B, CSV_PROP, CSV_31], ['смертность на 100 тыс. нас.'], [
    #                           'психические расстройства в возр. от 18 лет, %',
    #                           'безработица, %',
    #                           'наркомания от 18 лет, %',
    #                           'число лиц, которым оказана медицинская помощь при выездах на 100 тыс. нас.',
    #                           'количество врачей на 100 тыс. нас.'
    #                       ]],
    #                       [[CSV_PROP, CSV_31], ['рождаемость на 100 тыс. нас.'], [
    #                           'удельный вес сельского нас., %',
    #                           'среднедушевой доход населения',
    #                           'работающее население, %'
    #                       ]],
    #                       [[CSV_PROP, CSV_31], ['заболеваемость от 18 лет на 100 тыс. нас.'], [
    #                           'прожиточный минимум',
    #                           'безработица, %',
    #                           'процент лиц с доходами ниже прожиточного минимума',
    #                           'среднедушевой доход населения',
    #                           'число лиц, которым оказана медицинская помощь при выездах на 100 тыс. нас.',
    #                           'количество врачей на 100 тыс. нас.'
    #                       ]]
    #                       ]
    #     for c in corr_regr_list:
    #         analysis.correlation_regression(c[0], c[1], c[2])
    #
    #     generate_geojson_from_df_time_series([DISTRICT_POLYGON + 'здоровьеАрхангельска.geojson',
    #                                           DISTRICT_POLYGON + 'здоровьеКрасноярск.geojson',
    #                                           DISTRICT_POLYGON + 'здоровьеРеспублика К.geojson',
    #                                           DISTRICT_POLYGON + 'здоровьеЯмало-Ненецк.geojson'],
    #                                          TIME_SERIES_DIR + RES, 'общая численность населения: всего',
    #                                          'прирост', 'abs inc chain&growth inc of chain, %',
    #                                          'geojson_data/прирост')
    #
    # def test_gg(self):
    #     geojson_generator.read_geojson_content('geojson_data/приростКрасноярск.geojson')


    def test_timeit_csv_generator(self):
        loops = 10
        t = timeit.timeit(setup="from data_generator import DataGenerator;"
                           "data = DataGenerator('health.xlsx')",
                           stmt="data.generate_csv('28', 'мужчины знач')", number=loops)
        timeit_to_file('data_generator', 'generate_csv', loops, t/loops, '~1500 строк excel -> csv')

    def test_timeit_property_creator(self):
        loops = 10
        t = timeit.timeit(setup="from data_generator import DataGenerator;"
                           "data = DataGenerator('health.xlsx');from utils import CSV_11, CSV_11_IND",
                           stmt="data.create_property(CSV_11, CSV_11_IND[10], CSV_11, CSV_11_IND[0], "
                                "'смертность на 100 тыс. нас.', 100000)",
                          number=loops)
        timeit_to_file('data_generator', 'create_property', loops, t/loops, '~2000 csv -> csv')

    def test_timeit_descriptive_stat_y(self):
        loops = 10
        t = timeit.timeit(setup="from analysis import Analysis;"
                           "from utils import CSV_PROP, CSV_PROP_IND, YEAR; analysis = Analysis()",
                           stmt="analysis.descriptive_stat(CSV_PROP, CSV_PROP_IND[0:3], YEAR)",
                          number=loops)
        timeit_to_file('analyzer', 'descriptive_stat (YEARS)', loops, t/loops,
                       '~1000 csv + create graphics for YEARS')

    def test_timeit_descriptive_stats_s(self):
        loops = 10
        t = timeit.timeit(setup="from analysis import Analysis;"
                           "from utils import CSV_PROP, CSV_PROP_IND, SUBJECT; analysis = Analysis()",
                           stmt="analysis.descriptive_stat(CSV_PROP, CSV_PROP_IND[0:3], SUBJECT)",
                          number=loops)
        timeit_to_file('analyzer', 'descriptive_stat (DISTRICTS)', loops, t/loops,
                       '~1000 csv + create graphics for SUBJECTS')

    def test_timeit_time_series(self):
        loops = 10
        t = timeit.timeit(setup="from analysis import Analysis;"
                           "from utils import CSV_P11, CSV_11_IND; analysis = Analysis()",
                           stmt="analysis.time_series(CSV_11, CSV_11_IND[0])",
                          number=loops)
        timeit_to_file('analyzer', 'time_series', loops, t/loops, '~1000 csv + create graphics')

    def test_timeit_group_comparison_y(self):
        loops = 10
        t = timeit.timeit(setup="from analysis import Analysis;"
                           "from utils import CSV_PROP,  YEAR; analysis = Analysis()",
                           stmt="analysis.group_comparison(YEAR, CSV_PROP, 'работающих мужчин, %', "
                                "CSV_PROP, 'работающих женщин, %')",
                          number=loops)
        timeit_to_file('analyzer', 'group_comparison (YEARS)', loops, t/loops,
                       '~1000 csv + create graphics for YEARS')

    def test_timeit_group_comparison_s(self):
        loops = 10
        t = timeit.timeit(setup="from analysis import Analysis;"
                           "from utils import CSV_PROP, SUBJECT; analysis = Analysis()",
                           stmt="analysis.group_comparison(SUBJECT, CSV_PROP, 'работающих мужчин, %', "
                                "CSV_PROP, 'работающих женщин, %')",
                          number=loops)
        timeit_to_file('analyzer', 'group_comparison (DISTRICTS)', loops, t/loops,
                       '~1000 csv + create graphics for SUBJECTS')

    def test_timeit_multi_group_comparison_y(self):
        loops = 10
        t = timeit.timeit(setup="from analysis import Analysis;"
                           "from utils import CSV_PROP,  YEAR; analysis = Analysis()",
                           stmt="analysis.multi_group_comparison(YEAR, [CSV_PROP], "
                                "['заболеваемость 0-14 лет на 100 тыс. нас.', 'заболеваемость 15-17 лет на 100 тыс. нас.', "
                                "'заболеваемость от 18 лет на 100 тыс. нас.'],'заболеваемость')",
                          number=loops)
        timeit_to_file('analyzer', 'multi_group_comparison (YEARS)', loops, t/loops,
                       '~1000 csv + create graphics for YEARS')

    def test_timeit_multi_group_comparison_s(self):
        loops = 10
        t = timeit.timeit(setup="from analysis import Analysis;"
                           "from utils import CSV_PROP, SUBJECT; analysis = Analysis()",
                           stmt="analysis.multi_group_comparison(SUBJECT, [CSV_PROP], "
                                "['заболеваемость 0-14 лет на 100 тыс. нас.', 'заболеваемость 15-17 лет на 100 тыс. нас.', "
                                "'заболеваемость от 18 лет на 100 тыс. нас.'],'заболеваемость')",
                          number=loops)
        timeit_to_file('analyzer', 'multi_group_comparison (DISTRICTS)', loops, t/loops,
                       '~1000 csv + create graphics for SUBJECTS')


def timeit_to_file(module, function, loops, t, ch):
    df = pd.DataFrame({'module': [module], 'function': [function], 'loops': [loops],
                           '~time': [t], 'ch': [ch]})
    if os.path.exists('performance_report.csv'):
        read_df = pd.read_csv('performance_report.csv')
        read_df = read_df.append(df, ignore_index=True)
        read_df.to_csv('performance_report.csv', index=False)
    else:
        df.to_csv('performance_report.csv', index=False)
        assert os.path.exists('performance_report.csv'), f'Файл performance_report.csv не был создан'


if __name__ == '__main__':
    unittest.main()