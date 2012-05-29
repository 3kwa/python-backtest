import unittest
import os
import datetime

from numpy.testing.utils import assert_almost_equal

from lib.stock import Stock
from lib.tick import Tick
from lib.backtest import Trade, BackTest
from test_helpers import get_historical_prices, raise_if_called, NewDate

class TestBackTest(unittest.TestCase):

    def setUp(self):
        self.built_in_date = datetime.date
        datetime.date = NewDate
        self.goog = Stock('GOOG', get_historical_prices)
        self.backtest = BackTest()
        self.backtest.stock = self.goog

    def tearDown(self):
        datetime.date = self.built_in_date
        os.remove('cache/GOOG_2012-05-25')
        self.backtest.stock = None
        self.backtest.trades = []
        self.backtest.cost = lambda trade: 0

    def test_initial_cost_zero(self):
        self.assertEqual(0, self.backtest.cost(100))

    def test_setting_cost_to_lambda(self):
        self.backtest.cost = lambda trade: 10 + 5 * trade / 100
        self.assertEqual(15, self.backtest.cost(100))

    def test_trade_cost_calculation(self):
        tick = Tick(self.goog, 0, datetime.date(2012, 5, 25), 1.0, 2.0, 3.0,
                    4.0, 5, 6.0)
        self.backtest.trades.append(Trade('buy', tick))
        self.assertEqual(0, self.backtest.trade_cost)
        self.backtest.cost = lambda trade: 0.5 * trade / 100
        self.assertEqual(0.02, self.backtest.trade_cost)
        tick = Tick(self.goog, 1, datetime.date(2012, 5, 25), 1.0, 2.0, 3.0,
                    4.0, 5, 6.0)
        self.backtest.trades.append(Trade('sell', tick))
        self.assertEqual(0.04, self.backtest.trade_cost)
        self.assertEqual(0.02, self.backtest._trade_cost(0))
        self.assertEqual(0.04, self.backtest._trade_cost(1))

    def test_position_calculation(self):
        tick = Tick(self.goog, 0, datetime.date(2012, 5, 25), 1.0, 2.0, 3.0,
                    4.0, 5, 6.0)
        self.backtest.trades.append(Trade('buy', tick))
        self.assertEqual('long', self.backtest.position)
        tick = Tick(self.goog, 1, datetime.date(2012, 5, 25), 1.0, 2.0, 3.0,
                    4.0, 5, 6.0)
        self.backtest.trades.append(Trade('sell', tick))
        self.assertIsNone(self.backtest.position)
        tick = Tick(self.goog, 2, datetime.date(2012, 5, 25), 1.0, 2.0, 3.0,
                    4.0, 5, 6.0)
        self.backtest.trades.append(Trade('sell', tick))
        self.assertEqual('short', self.backtest.position)

    def test_gross_pnl_calculation(self):
        tick = self.goog[0]
        self.backtest.trades.append(Trade('buy', tick))
        self.assertEqual(-100.34, self.backtest.gross)
        tick = self.goog[10]
        self.backtest.trades.append(Trade('sell', tick))
        assert_almost_equal(1.17, self.backtest.gross)

    def test_net_pnl_zero_calculation(self):
        tick = self.goog[0]
        self.backtest.trades.append(Trade('buy', tick))
        assert_almost_equal(491.19, self.backtest.net, 2)
        self.assertEqual(0, self.backtest._net(0))
        assert_almost_equal(1.17, self.backtest._net(10))
        tick = self.goog[10]
        self.backtest.trades.append(Trade('sell', tick))
        assert_almost_equal(1.17, self.backtest.net)
        self.backtest.cost = lambda trade: 0.5 * trade / 100
        assert_almost_equal(0.16, self.backtest.net, 2)
