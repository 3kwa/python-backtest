import datetime
from collections import namedtuple
import cPickle as pickle

import numpy
from ystockquote import get_historical_prices


class Stock(object):
    """ List like stock data for a given symbol

    Loads from Yahoo when instantiated unless cache is available.

    >>> goog = Stock('GOOG')
    >>> isinstance(goog[-1], Tick)
    True
    """

    def __init__(self, symbol=None):
        self.data = []
        if symbol is not None:
            self.load(symbol)

    def load(self, symbol):
        """ Loads the stock quote for symbol from Yahoo or cache """
        raw = Stock.get_from_cache(symbol)
        if raw is None:
            today = datetime.date.today().strftime('%Y%m%d')
            raw = get_historical_prices(symbol, '20010103', today)
            Stock.save_to_cache(symbol, raw)
        # Tick aware of the time series it belongs to
        self.data.extend(
            [ Tick(self.data, index, *Stock.cast(tick))
              for index, tick
              in enumerate(reversed(raw[1:])) ])

    @staticmethod
    def get_from_cache(symbol):
        """ Get the date for symbol from cache return list or none """
        try:
            with open('{0}_{1}'.format(symbol, datetime.date.today())) as f:
                return pickle.load(f)
        except (IOError, EOFError):
            return None

    @staticmethod
    def save_to_cache(symbol, raw):
        """ Save the data coming from Yahoo into cache """
        with open('{0}_{1}'.format(symbol, datetime.date.today()), 'w') as f:
            pickle.dump(raw, f)

    @staticmethod
    def cast(raw_tick):
        """ Cast the data from a Yahoo raw tick into relevant types

        >>> Stock.cast(('2012-05-25', '1.0'))
        [datetime.date(2012, 5, 25), 1.0]
        """
        result = [ datetime.date(*map(int, raw_tick[0].split('-'))) ]
        result.extend( map(float, raw_tick[1:]) )
        return result

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
    """ Tick i.e. stock price etc. on a given day

    Contains a reference to the time series it belongs to (Stock.data) and its
    index in the list for metric computation.

    >>> Tick([], 0, datetime.date(2012, 5, 25), 1.0, 1.0, 1.0,
    ...              1.0, 1, 1.0)
    Tick(series=[...], index=0, date=2012-05-25 open=1.0, high=1.0, low=1.0, close=1.0, volume=1, adj=1.0)
    """

    __slots__ = ()

    def std(self, n):
        index = self.index + 1
        return numpy.std([tick.close for tick in self.series[index-n:index]])

    def ma(self, n):
        index = self.index + 1
        return numpy.mean([tick.close for tick in self.series[index-n:index]])

    def __repr__(self):
        return 'Tick(series=[...], index={0.index}, date={0.date} \
open={0.open}, high={0.high}, low={0.low}, close={0.close}, \
volume={0.volume}, adj={0.adj})'.format(self)


class BackTest(object):

    sell = {'long': None, None: 'short'}
    buy = {None: 'long', 'short': None}

    def __call__(self, stock, strategy):
        self.position = None
        self.trades = []
        self.latest = stock[-1]
        for t in stock:
            if strategy(t) == 'buy' and self.position != 'long':
                self.position = self.buy[self.position]
                self.trades.append(t.close)
            elif strategy(t) == 'sell' and self.position != 'short':
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
backtest = BackTest()

#import code; code.interact(local=locals())
