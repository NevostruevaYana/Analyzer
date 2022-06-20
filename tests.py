import unittest
from analysis import Analysis
import geojson_generator
from main import main
from graphics import Graphics
from geojson_generator import *
from data_generator import *
from csv_table_to_doxc import create_docx_table


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

    # generate csv
    def test_ty(self):
        with self.assertRaises(AssertionError) as ctx:
            DataGenerator('file.csv')
        self.assertEqual(ctx.exception.args[0], 'Некорректное имя файла')

    def test_generate_csv(self):
        add_all_dir()
        data = DataGenerator('health.xlsx')

        data.get_years_and_regs()
        data_list = [('11', 'абсолютное значение'), ('23', 'от 0-14 лет абс.'), ('23', '15-17 лет абс.'),
                     ('23', 'от 18 абс.'), ('27', '0-14 лет абс.'), ('27', '15-17 лет абс.'), ('27', '18-60 абс.'),
                     ('28', 'мужчины знач'), ('28', 'женщины знач.'), ('31', 'значение')]
        for d in data_list:
            data.generate_csv(d[0], d[1])

    def test_create_property(self):
        data = DataGenerator('health.xlsx')
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
                         [CSV_28_G, CSV_28_IND[1], CSV_28_B, CSV_28_IND[1],
                          'число случаев временной нетрудоспособности',
                          -2],
                         [CSV_11, CSV_11_IND[6], CSV_11, CSV_11_IND[0], 'работающее население, %', 100],
                         [CSV_PROP, 'число случаев временной нетрудоспособности', CSV_11, CSV_11_IND[0],
                          'безработица, %', 100],
                         [CSV_27_18_60, CSV_27_IND[0], CSV_11, CSV_11_IND[5],
                          'психические расстройства в возр. от 18 лет, %', 100],
                         [CSV_27_18_60, CSV_27_IND[1], CSV_11, CSV_11_IND[5],
                          'невротические и соматоформные расстройства в возр. от 18 лет, %', 100],
                         [CSV_27_18_60, CSV_27_IND[2], CSV_11, CSV_11_IND[5],
                          'другие непсихотические расстройства в возр. от 18 лет, %', 100],
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

    def test_gg(self):
        geojson_generator.read_geojson_content('geojson_data/приростКрасноярск.geojson')

    def test_r(self):
        create_docx_table(CORR_REGR_DIR + RES)


if __name__ == '__main__':
    unittest.main()
