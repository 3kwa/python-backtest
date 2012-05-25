import datetime
from collections import namedtuple

import numpy
from ystockquote import get_historical_prices


today = datetime.date.today().strftime('%Y%m%d')
goog = get_historical_prices('GOOG', '20010103', today)

class Strategy(object):

    def __call__(self, tick):
       return self.signal(tick)

class Bollinger(Strategy):

    def __init__(self, n, k):
        self.n = n
        self.k = k

    def upper(self, tick):
        return tick.ma(self.n) + self.k * tick.std(self.n)

    def lower(self, tick):
        return tick.ma(self.n) - self.k * tick.std(self.n)

    def signal(self, tick):
        if tick.close > self.upper(tick):
            return 'buy'
        elif tick.close < self.lower(tick):
            return 'sell'

class Tick(namedtuple('Tick',
                      ['series', 'index', 'date', 'open', 'high', 'low',
                       'close', 'volume', 'adj'])):
    def std(self, n):
        index = self.index + 1
        return numpy.std([float(tick.close) for tick in self.series[index-n:index]])
    def ma(self, n):
        index = self.index + 1
        return numpy.mean([float(tick.close) for tick in self.series[index-n:index]])
    def trade(self, strategy):
        return strategy(self)

# instantiating ticks
ticks = []
# extending ticks with Tick object pointing to ticks
ticks.extend([Tick(ticks, index, *tick) for index, tick in enumerate(reversed(goog[1:]))])

bol = Bollinger(20, 2)

import code; code.interact(local=locals())
