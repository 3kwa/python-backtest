import datetime
import cPickle as pickle

from ystockquote import get_historical_prices

from tick import Tick


class Stock(object):
    """ List like stock data for a given symbol

    Loads from Yahoo when instantiated unless cache is available.

    >>> goog = Stock('GOOG')
    >>> isinstance(goog[0], Tick)
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
            with open('cache/{0}_{1}'.format(symbol, datetime.date.today())) as f:
                return pickle.load(f)
        except (IOError, EOFError):
            return None

    @staticmethod
    def save_to_cache(symbol, raw):
        """ Save the data coming from Yahoo into cache """
        with open('cache/{0}_{1}'.format(symbol, datetime.date.today()), 'w') as f:
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


