from collections import namedtuple
import datetime

import numpy


numpy.seterr(invalid='ignore')

class Tick(namedtuple('Tick',
                      ['series', 'index', 'date', 'open', 'high', 'low',
                       'close', 'volume', 'adj'])):
    """ Tick i.e. stock price etc. on a given day

    Contains a reference to the time series it belongs to (Stock.data) and its
    index in the list in order to compute metrics.

    >>> Tick([], 0, datetime.date(2012, 5, 25), 1.0, 1.0, 1.0,
    ...              1.0, 1, 1.0)
    Tick(series=[...], index=0, date=2012-05-25 open=1.0, high=1.0, low=1.0, close=1.0, volume=1, adj=1.0)
    """

    __slots__ = ()

    def __repr__(self):
        return 'Tick(series=[...], index={0.index}, date={0.date} \
open={0.open}, high={0.high}, low={0.low}, close={0.close}, \
volume={0.volume}, adj={0.adj})'.format(self)

    def std(self, n):
        index = self.index + 1
        return numpy.std([tick.close for tick in self.series[index-n:index]])

    def ma(self, n):
        index = self.index + 1
        return numpy.mean([tick.close for tick in self.series[index-n:index]])

    def upper_bb(self, n, k):
        return self.ma(n) + k * self.std(n)

    def lower_bb(self, n, k):
        return self.ma(n) - k * self.std(n)


