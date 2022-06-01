import unittest

from main import *
from utils import count_arzf


class TestMethods(unittest.TestCase):

    # generate csv

    def test_generate_health_11(self):
        generate_csv('health.xlsx', ['11'], 'показатель', 'абсолютное значение')
        files = os.scandir('csv_data/11')
        for f in files:
            count_arzf(f)

    def test_generate_health_23(self):
        generate_csv('health.xlsx', ['23'], 'показатель', 'от 0-14 лет абс.&15-17 лет абс.&от 18 абс.')
        files = os.scandir('csv_data/23')
        for f in files:
            count_arzf(f)

    def test_generate_health_31(self):
        generate_csv('health.xlsx', ['31'], 'показатель', 'значение')
        files = os.scandir('csv_data/31')
        for f in files:
            count_arzf(f)

    # create indicator

    def test_doctor_100k(self):
        create_indicator('csv_data/11/количество умерших в данном ,.csv',
                         'csv_data/11/общая численность населения,о.csv',
                         'показатель',
                         'смертность на 100 тыс.csv', 100000)

    def test_death_100k(self):
        create_indicator('csv_data/31/количество врачей всех специй.csv',
                         'csv_data/11/общая численность населения,о.csv',
                         'показатель',
                         'количество врачей на 100 тыс. нас.csv', 100000)

    # descriptive statistics

    def test_ds_death_2015(self):
        describe_st('csv_data/csv_prop/смертность на 100 тыс.csv', 2015)

    # analysis time series

    def test_ts_death_2015(self):
        analysis_time_series('csv_data/11/общая численность населения,о.csv',
                             'Чукотский автономный округ', 'г. Анадырь', False)

    def test_incidence_0_14(self):
        create_indicator('csv_data/23/заболеваемость всего,,.csv',
                         'csv_data/11/численность детей (0-14 лет ).csv',
                         'от 0-14 лет абс.',
                         'заболеваемость 0-14 лет на 100 тыс.csv', 100000)

    def test_incidence_15_17(self):
        create_indicator('csv_data/23/заболеваемость всего,,.csv',
                         'csv_data/11/численность подростков (от 1).csv',
                         '15-17 лет абс.',
                         'заболеваемость 15-17 лет на 100 тыс.csv', 100000)

    # group comparison

    def test_group_incidence(self):
        group_comparison('csv_data/csv_prop/заболеваемость 0-14 лет на 100 тыс.csv',
                         'csv_data/csv_prop/заболеваемость 15-17 лет на 100 тыс.csv', False)

    # correlation regression

    def test_corr_regression(self):
        corr_regression('csv_data/csv_prop/смертность на 100 тыс.csv',
                        'csv_data/csv_prop/количество врачей на 100 тыс. нас.csv')

    # geo portal

    def test_geo_1(self):
        gen_geo_inc('csv_data/11/общая численность населения,о.csv', 'численность, ряды динамики.csv')

    def test__(self):
        df_to_geojson('численность, ряды динамики.csv')

    def test_ff(self):
        read_j()


if __name__ == '__main__':
    unittest.main()
