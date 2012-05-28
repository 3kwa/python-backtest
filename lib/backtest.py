class BackTest(object):
    """ Callable object running back tests for a strategy over a stock

    >>> backtest = BackTest()

    If goog is a Stock and bollinger a strategy (cf. strategy/__init__.py)

    >>> backtest(goog, bollinger)
    BackTest(trades=[99], position=short, gross=1253.63, net=662.1, passive=491.19)

    Current position is short, gross PNL is 1253.63, net PNL taking into account
    the closing of the position and the trading costs if applicable is 662.1.

    A passive strategy (buy on day 1 sell on last day) would have returned 491.19

    Trading costs are 0 by default. To change that set the cost attribute of
    the backtest object to a function taking a trade as an argument and returning
    the cost.

    >>> backtest.cost = lambda trade: 0.5 * trade / 100
    >>> backtest
    BackTest(trades=[99], position=short, gross=1253.63, net=435.78005, passive=491.19)
    """

    sell = {'long': None, None: 'short'}
    buy = {None: 'long', 'short': None}

    def __init__(self):
        self.cost = lambda trade: 0

    def __call__(self, stock, strategy):
        self.position = None
        self.trades = []
        self.first = stock[0]
        self.last = stock[-1]
        for t in stock:
            if strategy(t) == 'buy' and self.position != 'long':
                self.position = self.buy[self.position]
                self.trades.append(t.close)
            elif strategy(t) == 'sell' and self.position != 'short':
                self.position = self.sell[self.position]
                self.trades.append(-t.close)
        return self

    def __repr__(self):
        return 'BackTest(trades=[{1}], position={0.position}, gross={0.pnl}, \
net={0.net}, passive={0.passive})'.format(self, len(self.trades))

    @property
    def trade_cost(self):
        """ return the cost trading cost over the backtesting period """
        return sum(self.cost(abs(trade)) for trade in self.trades)

    @property
    def pnl(self):
        return -sum(self.trades)

    @property
    def net(self):
        result = 0
        if self.position == 'long':
            result += self.last.close
        elif self.position == 'short':
            result -= self.last.close
        result += self.pnl
        result -= self.trade_cost
        return result

    @property
    def passive(self):
        """ buy on day 1 sell on last day """
        return self.last.close - self.first.close
