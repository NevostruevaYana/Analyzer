import unittest
from main import main
import timeit
from geojson_generator import *
from analysis import Analysis
from data_generator import *


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

    def test_main(self):
        main()

    def test_timeit_csv_generator(self):
        loops = 100
        t = timeit.timeit(setup="from data_generator import DataGenerator;"
                                "data = DataGenerator('health.xlsx')",
                          stmt="data.generate_csv('28', 'мужчины знач')", number=loops)
        timeit_to_file('data_generator', 'generate_csv', loops, t / loops, '~1500 строк excel -> csv')

    def test_timeit_property_creator(self):
        loops = 500
        t = timeit.timeit(setup="from data_generator import DataGenerator;"
                                "data = DataGenerator('health.xlsx');from utils import CSV_11, CSV_11_IND",
                          stmt="data.create_property(CSV_11, CSV_11_IND[10], CSV_11, CSV_11_IND[0], "
                               "'смертность на 100 тыс. нас.', 100000)",
                          number=loops)
        timeit_to_file('data_generator', 'create_property', loops, t / loops, '~2000 csv -> csv')

    def test_timeit_descriptive_stat_y(self):
        loops = 1000
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_PROP, CSV_PROP_IND, YEAR; analysis = Analysis()",
                          stmt="analysis.descriptive_stat(CSV_PROP, CSV_PROP_IND[0:3], YEAR)",
                          number=loops)
        timeit_to_file('analyzer', 'descriptive_stat (YEARS)', loops, t / loops,
                       '~1000 csv + create graphics for YEARS')

    def test_timeit_descriptive_stat_s(self):
        loops = 1000
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_PROP, CSV_PROP_IND, SUBJECT; analysis = Analysis()",
                          stmt="analysis.descriptive_stat(CSV_PROP, CSV_PROP_IND[0:3], SUBJECT)",
                          number=loops)
        timeit_to_file('analyzer', 'descriptive_stat (SUBJECTS)', loops, t / loops,
                       '~1000 csv + create graphics for SUBJECTS')

    def test_timeit_time_series(self):
        loops = 100
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_11, CSV_11_IND; analysis = Analysis()",
                          stmt="analysis.time_series(CSV_11, CSV_11_IND[0])",
                          number=loops)
        timeit_to_file('analyzer', 'time_series', loops, t / loops, '~1000 csv + create graphics')

    def test_timeit_group_comparison_y(self):
        loops = 100
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_PROP, YEAR; analysis = Analysis()",
                          stmt="analysis.group_comparison(YEAR, CSV_PROP, 'работающих мужчин, %', "
                               "CSV_PROP, 'работающих женщин, %')",
                          number=loops)
        timeit_to_file('analyzer', 'group_comparison (YEARS)', loops, t / loops,
                       '~1000 csv + create graphics for YEARS')

    def test_timeit_group_comparison_s(self):
        loops = 1000
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_PROP, SUBJECT; analysis = Analysis()",
                          stmt="analysis.group_comparison(SUBJECT, CSV_PROP, 'работающих мужчин, %', "
                               "CSV_PROP, 'работающих женщин, %')",
                          number=loops)
        timeit_to_file('analyzer', 'group_comparison (SUBJECTS)', loops, t / loops,
                       '~1000 csv + create graphics for SUBJECTS')

    def test_timeit_multi_group_comparison_y(self):
        loops = 100
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_PROP, YEAR; analysis = Analysis()",
                          stmt="analysis.multi_group_comparison(YEAR, [CSV_PROP], "
                               "['заболеваемость 0-14 лет на 100 тыс. нас.', 'заболеваемость 15-17 лет на 100 тыс. нас.', "
                               "'заболеваемость от 18 лет на 100 тыс. нас.'],'заболеваемость')",
                          number=loops)
        timeit_to_file('analyzer', 'multi_group_comparison (YEARS)', loops, t / loops,
                       '~1000 csv + create graphics for YEARS')

    def test_timeit_multi_group_comparison_s(self):
        loops = 1000
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_PROP, SUBJECT; analysis = Analysis()",
                          stmt="analysis.multi_group_comparison(SUBJECT, [CSV_PROP], "
                               "['заболеваемость 0-14 лет на 100 тыс. нас.', 'заболеваемость 15-17 лет на 100 тыс. нас.', "
                               "'заболеваемость от 18 лет на 100 тыс. нас.'],'заболеваемость')",
                          number=loops)
        timeit_to_file('analyzer', 'multi_group_comparison (SUBJECTS)', loops, t / loops,
                       '~1000 csv + create graphics for SUBJECTS')

    def test_timeit_correlation_regression(self):
        loops = 1000
        t = timeit.timeit(setup="from analysis import Analysis;"
                                "from utils import CSV_PROP, CSV_31; analysis = Analysis()",
                          stmt="analysis.correlation_regression([CSV_PROP, CSV_31], ['рождаемость на 100 тыс. нас.'], "
                               "[ 'удельный вес сельского нас., %', 'среднедушевой доход населения', "
                               "'работающее население, %'])",
                          number=loops)
        timeit_to_file('analyzer', 'correlation_regression', loops, t / loops,
                       '~1000 csv + create graphics')

    def test_timeit_geo_time_series(self):
        loops = 1000
        t = timeit.timeit(setup="from geojson_generator import generate_geojson_from_df_time_series;"
                                "from utils import DISTRICT_POLYGON, TIME_SERIES_DIR, RES",
                          stmt="generate_geojson_from_df_time_series([DISTRICT_POLYGON + "
                               "'здоровьеАрхангельска.geojson'],TIME_SERIES_DIR + RES, "
                               "'общая численность населения: всего', 'прирост', "
                               "'abs inc chain&growth inc of chain, %', 'geojson_data/прирост')",
                          number=loops)
        timeit_to_file('geojson_generator', 'generate_geojson_from_df_time_series', loops, t / loops,
                       '~1000 csv')

    def test_timeit_geo_prop(self):
        loops = 100
        t = timeit.timeit(setup="from geojson_generator import generate_geojson_from_df_prop;"
                                "from utils import DISTRICT_POLYGON",
                          stmt="generate_geojson_from_df_prop([DISTRICT_POLYGON + "
                               "'здоровьеАрхангельска.geojson'], 'geojson_data/показатели')",
                          number=loops)
        timeit_to_file('geojson_generator', 'generate_geojson_from_df_prop', loops, t / loops,
                       '~1000 csv, ~20 properties')

def timeit_to_file(module, function, loops, t, ch):
    df = pd.DataFrame({'module': [module], 'function': [function], 'loops': [round(loops, 2)],
                       '~time, sec': [t], 'characteristic': [ch]})
    if os.path.exists('performance_report.csv'):
        read_df = pd.read_csv('performance_report.csv')
        read_df = read_df.append(df, ignore_index=True)
        read_df.to_csv('performance_report.csv', index=False)
    else:
        df.to_csv('performance_report.csv', index=False)
        assert os.path.exists('performance_report.csv'), f'Файл performance_report.csv не был создан'


if __name__ == '__main__':
    unittest.main()
