import unittest

import analysis
from analysis import Analysis
import geojson_generator
from data import *


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)
        self.years = pd.read_csv(YEARS_CSV)[YEAR].values
        self.regs = pd.read_csv(DISTRICT_CSV)[[SUBJECT, DISTRICT]].values
        self.analysis = Analysis()
        self.data = Data()

    def test_t(self):
        analysis.t(CSV_DATA + '31/' + 'gen.csv', CSV_DATA + 'csv_prop/' + 'gen.csv')

    # generate csv

    def test_years_regs(self):
        self.data.get_years_and_regs('health.xlsx', '11')

    def test_generate_health_11(self):
        self.data.generate_csv('health.xlsx', ['11'], 'показатель', 'абсолютное значение')

    def test_generate_health_23(self):
        self.data.generate_csv('health.xlsx', ['23'], 'показатель', 'от 0-14 лет абс.')
        self.data.generate_csv('health.xlsx', ['23'], 'показатель', '15-17 лет абс.')
        self.data.generate_csv('health.xlsx', ['23'], 'показатель', 'от 18 абс.')

    def test_generate_health_27(self):
        self.data.generate_csv('health.xlsx', ['27'], 'показатель', '0-14 лет абс.')
        self.data.generate_csv('health.xlsx', ['27'], 'показатель', '15-17 лет абс.')
        self.data.generate_csv('health.xlsx', ['27'], 'показатель', '18-60 абс.')

    def test_generate_health_28(self):
        self.data.generate_csv('health.xlsx', ['28'], 'показатель', 'мужчины знач')
        self.data.generate_csv('health.xlsx', ['28'], 'показатель', 'женщины знач.')

    def test_generate_health_31(self):
        self.data.generate_csv('health.xlsx', ['31'], 'показатель', 'значение')

    # create indicator

    def test_create_prop(self):
        self.data.create_indicator(CSV_11, CSV_11_IND[10], CSV_11, CSV_11_IND[0],
                         'смертность на 100 тыс. нас.', 100000)

        self.data.create_indicator(CSV_31, CSV_31_IND[16], CSV_11, CSV_11_IND[0],
                         'количество врачей на 100 тыс. нас.', 100000)

        self.data.create_indicator(CSV_23_0_14, CSV_23_IND[0], CSV_11, CSV_11_IND[2],
                         'заболеваемость 0-14 лет на 100 тыс. нас.csv', 100000)

        self.data.create_indicator(CSV_23_0_14, CSV_23_IND[0], CSV_11, CSV_11_IND[4],
                         'заболеваемость 15-17 лет на 100 тыс. нас.csv', 100000)

        self.data.create_indicator(CSV_11, CSV_11_IND[11], CSV_11, CSV_11_IND[3],
                                   'младенческая смертность на 1 тыс. нас.csv', 1000)

    # descriptive statistics

    def test_ds_death_Y(self):
        self.analysis.descriptive_st(CSV_PROP, 'смертность на 100 тыс. нас.', YEAR)

    def test_ds_death_S(self):
        self.analysis.descriptive_st(CSV_PROP, 'смертность на 100 тыс. нас.', SUBJECT)

    # analysis time series

    def test_ts_death(self):
        self.analysis.analysis_time_series(CSV_11, CSV_11_IND[0])

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