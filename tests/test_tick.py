import unittest
import datetime

import numpy

from lib.tick import Tick

class TestTick(unittest.TestCase):

    def setUp(self):
        self.stock = []
        self.stock.extend([
            Tick(self.stock, 0, datetime.date(2012, 5, 25), 1.0, 2.0, 3.0, 4.0,
                 5, 6.0),
            Tick(self.stock, 1, datetime.date(2012, 5, 26), 2.0, 4.0, 6.0, 8.0,
                 10, 12.0),
            Tick(self.stock, 2, datetime.date(2012, 5, 27), 3.0, 6.0, 9.0,
                 12.0, 15, 18.0) ])

    def test_instantiation(self):
        tick = Tick(self.stock, 3, datetime.date(2012, 5, 28), 4.0, 8.0, 12.0,
                    16.0, 20, 24.0)
        self.assertEqual(self.stock, tick.series)
        self.assertEqual(3, tick.index)
        self.assertEqual(datetime.date(2012, 5, 28), tick.date)
        self.assertEqual(4.0, tick.open)
        self.assertEqual(8.0, tick.high)
        self.assertEqual(12.0, tick.low)
        self.assertEqual(16.0, tick.close)
        self.assertEqual(20, tick.volume)
        self.assertEqual(24.0, tick.adj)

    def test_standard_dev(self):
        tick = self.stock[0]
        numpy.testing.utils.assert_almost_equal(numpy.nan, tick.std(2))
        tick = self.stock[1]
        self.assertEqual(numpy.std([4.0, 8.0]), tick.std(2))
        tick = self.stock[2]
        self.assertEqual(numpy.std([8.0, 12.0]), tick.std(2))

    def test_moving_average(self):
        tick = self.stock[0]
        numpy.testing.utils.assert_almost_equal(numpy.nan, tick.ma(2))
        tick = self.stock[1]
        self.assertEqual(numpy.mean([4.0, 8.0]), tick.ma(2))
        tick = self.stock[2]
        self.assertEqual(numpy.mean([8.0, 12.0]), tick.ma(2))

    def test_upper_bollinger_band(self):
        tick = self.stock[0]
        numpy.testing.utils.assert_almost_equal(numpy.nan, tick.upper_bb(2, 2))
        tick = self.stock[1]
        self.assertEqual(numpy.mean([4.0, 8.0]) + 2 * numpy.std([4.0, 8.0]),
                         tick.upper_bb(2, 2))
        tick = self.stock[2]
        self.assertEqual(numpy.mean([8.0, 12.0]) + 2 * numpy.std([8.0, 12.0]),
                         tick.upper_bb(2, 2))

    def test_lower_bollinger_band(self):
        tick = self.stock[0]
        numpy.testing.utils.assert_almost_equal(numpy.nan, tick.lower_bb(2, 2))
        tick = self.stock[1]
        self.assertEqual(numpy.mean([4.0, 8.0]) - 2 * numpy.std([4.0, 8.0]),
                         tick.lower_bb(2, 2))
        tick = self.stock[2]
        self.assertEqual(numpy.mean([8.0, 12.0]) - 2 * numpy.std([8.0, 12.0]),
                         tick.lower_bb(2, 2))

