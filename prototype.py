import datetime
from collections import namedtuple

import numpy
from ystockquote import get_historical_prices


today = datetime.date.today().strftime('%Y%m%d')
goog = get_historical_prices('GOOG', '20010103', today)

class Tick(namedtuple('Tick',
                      ['series', 'index', 'date', 'open', 'high', 'low',
                       'close', 'volume', 'adj'])):
    def std(self, n):
        index = self.index + 1
        return numpy.std([float(tick.close) for tick in self.series[index-n:index]])
    def ma(self, n):
        index = self.index + 1
        return numpy.mean([float(tick.close) for tick in self.series[index-n:index]])

# instantiating ticks
ticks = []
# extending ticks with Tick object pointing to ticks
ticks.extend([Tick(ticks, index, *tick) for index, tick in enumerate(reversed(goog[1:]))])

import code; code.interact(local=locals())
