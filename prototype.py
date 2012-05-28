import code

from lib import Stock, BackTest
from strategy import Bollinger, Monkey


banner = open('README.rst').read()
bollinger = Bollinger(30, 1)
monkey = Monkey(30)
goog = Stock('GOOG')
backtest = BackTest()
backtest(goog, bollinger)
backtest.cost = lambda trade: 0.5 * trade / 100


code.interact(banner=banner, local=locals())
