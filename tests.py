import unittest
from analysis import Analysis
import geojson_generator
from main import main
from graphics import Graphics
from geojson_generator import *
from data_generator import *


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

    # generate csv
    def test_ty(self):
        with self.assertRaises(AssertionError) as ctx:
            DataGenerator('file.csv')
        self.assertEqual(ctx.exception.args[0], 'Некорректное имя файла')

    def test_ggg(self):
        add_all_dir()
        data = DataGenerator('health.xlsx')
        analysis = Analysis()
        property_list = [
                         [CSV_28_G, CSV_28_IND[1], CSV_11, CSV_11_IND[0], 'число случаев временной нетрудоспособности на 100 тыс.нас.', 100000]]

        for p in property_list:
            data.create_property(p[0], p[1], p[2], p[3], p[4], p[5])

        corr_regr_list = [
                          [[CSV_PROP, CSV_31], ['рождаемость на 100 тыс. нас.'], [
                              'удельный вес сельского нас., %',
                              'среднедушевой доход населения',
                              'число случаев временной нетрудоспособности на 100 тыс.нас.'
                          ]],
            [[CSV_PROP, CSV_31], ['заболеваемость от 18 лет на 100 тыс. нас.'], [
                'прожиточный минимум',
                'среднедушевой доход населения',
                'число посещений поликлинических медицинских учреждений',
                'количество врачей на 100 тыс. нас.'
            ]]
                          ]
        for c in corr_regr_list:
            analysis.multiple_corr_regr(c[0], c[1], c[2])

    def test_gg(self):
        geojson_generator.read_geojson_content('geojson_data/приростКрасноярск.geojson')


if __name__ == '__main__':
    unittest.main()
