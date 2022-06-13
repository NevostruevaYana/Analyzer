import unittest
from main import main
import geojson_generator
from analysis import Analysis
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
        main()

    def test_gg(self):
        geojson_generator.read_geojson_content('geojson_data/pace.geojson')


if __name__ == '__main__':
    unittest.main()
