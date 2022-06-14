import unittest
from analysis import Analysis
import geojson_generator
from main import main
from graphics import Graphics
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
        d = DataGenerator('health.xlsx')
        a = Analysis()
        gg = Graphics()
        # group_comparison_list = [[CSV_PROP, 'заболеваемость 0-14 лет на 100 тыс. нас.', CSV_PROP,
        #                           'заболеваемость 15-17 лет на 100 тыс. нас.', False]]
        # for g in group_comparison_list:
        #     a.group_comparison(g[0], g[1], g[2], g[3], g[4])
        #
        # property_list = [[CSV_23_18_, CSV_23_IND[0], CSV_11, CSV_11_IND[5], 'заболеваемость от 18 лет на 100 тыс. нас.',
        #                   100000]]
        # for p in property_list:
        #     d.create_property(p[0], p[1], p[2], p[3], p[4], p[5])
        # gg.plot_multi_box(['заболеваемость 0-14 лет на 100 тыс. нас.', 'заболеваемость 15-17 лет на 100 тыс. нас.',
        #                    'заболеваемость от 18 лет на 100 тыс. нас.'], 'сравнение заболеваемости')

        corr_regr_list = [[[CSV_27_18_60, CSV_28_B], ['число случаев временной нетрудоспособности'], [
            'психические расстройства, всего',
            'невротические, связанные со стрессом и соматоформные расстройства',
            'синдром зависимости от алкоголя (алкоголизм)',
            'синдром зависимости от наркотических веществ (наркомания)']]]
        for c in corr_regr_list:
            a.multiple_corr_regr(c[0], c[1], c[2])


    def test_gg(self):
        geojson_generator.read_geojson_content('geojson_data/pace.geojson')


if __name__ == '__main__':
    unittest.main()
