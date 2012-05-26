import datetime
from collections import namedtuple

import numpy
from ystockquote import get_historical_prices


class Stock(object):

    def __init__(self, symbol):
        self.data = []
        self._load(symbol)

    def _load(self, symbol):
        today = datetime.date.today().strftime('%Y%m%d')
        raw = get_historical_prices(symbol, '20010103', today)
        # Tick aware of the time series it belongs to
        self.data.extend(
            [ Tick(self.data, index, *Tick.cast(tick))
              for index, tick
              in enumerate(reversed(raw[1:])) ])

    def __iter__(self):
        for tick in self.data:
            yield tick

    def __getitem__(self, index):
        return self.data[index]

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
        return numpy.std([tick.close for tick in self.series[index-n:index]])

    def ma(self, n):
        index = self.index + 1
        return numpy.mean([tick.close for tick in self.series[index-n:index]])

    def trade(self, strategy):
        return strategy(self)

    @staticmethod
    def cast(raw_tick):
        result = [ datetime.date(*map(int, raw_tick[0].split('-'))) ]
        result.extend( map(float, raw_tick[1:]) )
        return result

class BackTest(object):

    sell = {'long': None, None: 'short'}
    buy = {None: 'long', 'short': None}

    def __call__(self, stock, strategy):
        self.position = None
        self.trades = []
        self.latest = stock[-1]
        for t in stock:
            if t.trade(strategy) == 'buy' and self.position != 'long':
                self.position = self.buy[self.position]
                self.trades.append(t.close)
            elif t.trade(strategy) == 'sell' and self.position != 'short':
                self.position = self.sell[self.position]
                self.trades.append(-t.close)
        return self.position, self.pnl, self.latest.close, len(self.trades)

    def cost(self, rate):
        return sum(abs(trade) for trade in self.trades) * rate / 100.

    @property
    def pnl(self):
        return -sum(self.trades)

    def net(self, rate):
        result = 0
        if self.position == 'long':
            result += self.latest.close
        elif self.position == 'short':
            result -= self.latest.close
        result += self.pnl
        result -= self.cost(rate)
        return result

bollinger = Bollinger(30, 1)
goog = Stock('GOOG')
backtest = BackTest()

import code; code.interact(local=locals())
