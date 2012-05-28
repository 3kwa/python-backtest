from lib import Stock
from lib import BackTest
from strategy import Bollinger, Monkey


banner = """
Back Test Trading Strategy
==========================

Stock (& Tick)
--------------

Stock(SYMBOL) instantiates an object containing historical prices for a SYMBOL
since 2001. e.g. goog = Stock('GOOG'). A Stock object is akin to a list of Tick
objects.

Stock.plot is a versatile instance method allowing you to plot Tick attributes.

Tick attributes you may want to plot:
    + open
    + close
    + high
    + low
    + ma(N)
    + std(N)
    + upper_bb(N, K)
    + lower_bb(N, K)

>>> goog.plot('close', 'upper_bb(30, 1)', 'lower_bb(30, 1)')

It will save the plot in the file png/GOOG.png.

BackTest
--------

BackTest() instantiates a backtesting object. e.g. backtest = BackTest()

A strategy is a callable object accepting a Tick object as an argument and
returning buy, None or sell. e.g. bollinger = Bollinger(30, 1),
monkey = Monkey(30)

To back test the bollinger strategy against the goog stock

>>> backtest(goog, bollinger)

To plot PNL (net) and position (long/.../short) over time call BackTest.plot

>>> backtest.plot()

It will save the plot in the file png/GOOG_Bollinger.png

Trading cost
------------

Backtest.cost should be a function taking a trade amount as an argument and
returning a cost. By default there are no trading cost using yet it is very
easy to change.

>>> backtest.cost = lambda trade: 0.5 * trade / 100

Will factor in 0.5 % trading cost for the net PNL computation.

Your turn to play:
------------------"""

bollinger = Bollinger(30, 1)
monkey = Monkey(30)
goog = Stock('GOOG')
backtest = BackTest()
backtest(goog, bollinger)
backtest.cost = lambda trade: 0.5 * trade / 100

import code; code.interact(banner=banner, local=locals())
