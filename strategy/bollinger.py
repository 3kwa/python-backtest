class Bollinger(object):
    """ Bollinger's band trading strategy

    Bollinger's band take 2 parameters the period N of the underlying moving
    average and the widht of the band K.

    To instantiate a 20 days, 2 standard dev:

    >>> bollinger = Bollinger(20, 2)
    """

    def __init__(self, n, k):
        self.n = n
        self.k = k

    def __call__(self, tick):
        if tick.close > tick.upper_bb(self.n, self.k):
            return 'buy'
        elif tick.close < tick.lower_bb(self.n, self.k):
            return 'sell'


