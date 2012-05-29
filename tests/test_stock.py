import unittest
import datetime
import cPickle as pickle
import shutil
import os

from lib.stock import Stock
from test_helpers import get_historical_prices, raise_if_called, NewDate

class TestStock(unittest.TestCase):

    def setUp(self):
        self.built_in_date = datetime.date
        datetime.date = NewDate

    def tearDown(self):
        datetime.date = self.built_in_date

    def test_get_from_cache_not_available(self):
        self.assertIsNone(Stock.get_from_cache('GOOG'))

    def test_get_from_cache_available(self):
        shutil.copy('tests/fixtures/GOOG_2012-05-25', 'cache/GOOG_2012-05-25')
        self.assertIsNotNone(Stock.get_from_cache('GOOG'))
        os.remove('cache/GOOG_2012-05-25')

    def test_save_to_cache(self):
        self.assertFalse(os.path.exists('cache/GOOG_2012-05-25'))
        Stock.save_to_cache('GOOG', None)
        self.assertTrue(os.path.exists('cache/GOOG_2012-05-25'))
        os.remove('cache/GOOG_2012-05-25')

    def test_instantiation_no_cache(self):
        self.assertFalse(os.path.exists('cache/GOOG_2012-05-25'))
        self.assertIsNotNone(Stock('GOOG', get_historical_prices))
        self.assertTrue(os.path.exists('cache/GOOG_2012-05-25'))
        os.remove('cache/GOOG_2012-05-25')

    def test_instantiation_with_cache(self):
        shutil.copy('tests/fixtures/GOOG_2012-05-25', 'cache/GOOG_2012-05-25')
        self.assertIsNotNone(Stock('GOOG', raise_if_called))
        os.remove('cache/GOOG_2012-05-25')
