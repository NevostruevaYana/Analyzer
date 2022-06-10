import unittest
from analysis import Analysis
import geojson_generator
from data import *


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)
        self.analysis = Analysis()
        self.data = Data()

    # generate csv

    def test_generate_health_11(self):
        self.data.generate_csv('health.xlsx', ['11'], 'показатель', 'абсолютное значение')

    def test_generate_health_23(self):
        self.data.generate_csv('health.xlsx', ['23'], 'показатель', 'от 0-14 лет абс.&15-17 лет абс.&от 18 абс.')

    def test_generate_health_31(self):
        self.data.generate_csv('health.xlsx', ['31'], 'показатель', 'значение')

    # create indicator

    def test_death_100k(self):
        self.data.create_indicator('csv_data/11/количество умерших в данном ,.csv',
                         'csv_data/11/общая численность населения,о.csv',
                         'показатель',
                         'смертность на 100 тыс. нас.csv', 100000)

    def test_doctor_100k(self):
        self.data.create_indicator('csv_data/31/количество врачей всех специй.csv',
                         'csv_data/11/общая численность населения,о.csv',
                         'показатель',
                         'количество врачей на 100 тыс. нас.csv', 100000)

    def test_incidence_0_14(self):
        self.data.create_indicator('csv_data/23/заболеваемость всего,,.csv',
                         'csv_data/11/численность детей (0-14 лет ).csv',
                         'от 0-14 лет абс.',
                         'заболеваемость 0-14 лет на 100 тыс. нас.csv', 100000)

    def test_incidence_15_17(self):
        self.data.create_indicator('csv_data/23/заболеваемость всего,,.csv',
                         'csv_data/11/численность подростков (от 1).csv',
                         '15-17 лет абс.',
                         'заболеваемость 15-17 лет на 100 тыс. нас.csv', 100000)

    # descriptive statistics

    def test_ds_death_Y(self):
        self.analysis.descriptive_st('csv_data/csv_prop/смертность на 100 тыс. нас.csv', YEAR)

    def test_ds_death_S(self):
        self.analysis.descriptive_st('csv_data/csv_prop/смертность на 100 тыс. нас.csv', SUBJECT)

    # analysis time series

    def test_ts_death(self):
        self.analysis.analysis_time_series('csv_data/11/общая численность населения,о.csv')

    # group comparison

    def test_group_incidence(self):
        self.analysis.group_comparison('csv_data/csv_prop/заболеваемость 0-14 лет на 100 тыс. нас.csv',
                         'csv_data/csv_prop/заболеваемость 15-17 лет на 100 тыс. нас.csv', False)

    # correlation regression

    def test_corr_regression(self):
        self.analysis.corr_regression('csv_data/csv_prop/смертность на 100 тыс. нас.csv',
                        'csv_data/csv_prop/количество врачей на 100 тыс. нас.csv')

    # geo portal

    def test_add_geo(self):
        geojson_generator.generate_geojson_from_df('geojson_data/здоровьеАрхангельска.geojson',
                 'csv_data/analysis/time_series/общая численность населения,о.csv',
                 'прирост','абсолют. прирост цепных&темп прироста цепных, %',
                 'abs&pace in percent','geojson_data/prii.geojson')

    def test_read_j(self):
        geojson_generator.read_geojson_content('geojson_data/prii.geojson')


if __name__ == '__main__':
    unittest.main()