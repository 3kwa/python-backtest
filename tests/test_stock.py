import unittest
import datetime
import cPickle as pickle
import shutil
import os

from lib.stock import Stock


def get_historical_prices(*args):
    """ injectable get_historical_prices """
    with open('tests/fixtures/GOOG_2012-05-25') as f:
        return pickle.load(f)

def raise_if_called(*args):
    raise Exception

class NewDate(datetime.date):
    """ class to mock datetime.date.today """
    @classmethod
    def today(cls):
        return cls(2012, 5, 25)

class TestHelpers(unittest.TestCase):

    def setUp(self):
        self.built_in_date = datetime.date
        datetime.date = NewDate

    def tearDown(self):
        datetime.date = self.built_in_date

    def test_datetime_mock(self):
        self.assertEqual(self.built_in_date(2012, 5, 25), datetime.date.today())

    def test_get_historical_prices_patch(self):
        self.assertEqual('2012-05-25',
                         max(raw_tick[0] for raw_tick
                             in get_historical_prices()[1:]))

    def test_raise_if_called(self):
        self.assertRaises(Exception, raise_if_called, None)

class TestStock(unittest.TestCase):

    def setUp(self):
        self.built_in_date = datetime.date
        datetime.date = NewDate
        Stock.get_historical_prices = get_historical_prices

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
