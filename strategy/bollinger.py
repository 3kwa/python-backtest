class Bollinger(object):
    """ Bollinger's band trading strategy """

    def __init__(self, n, k):
        self.n = n
        self.k = k

    def __call__(self, tick):
        if tick.close > tick.upper_bb(self.n, self.k):
            return 'buy'
        elif tick.close < tick.lower_bb(self.n, self.k):
            return 'sell'


