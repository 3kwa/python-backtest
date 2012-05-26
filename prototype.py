from lib import Stock
from lib import BackTest
from strategy import Bollinger, Monkey


bollinger = Bollinger(30, 1)
monkey = Monkey(30)
goog = Stock('GOOG')
backtest = BackTest()


import code; code.interact(local=locals())
