from collections import namedtuple, Counter

from matplotlib.pyplot import plot, subplot, ylim, yticks, savefig, clf


Trade = namedtuple('Trade', ['order', 'tick'])

class BackTest(object):
    """ Callable object running back tests for a strategy over a stock

    >>> backtest = BackTest()

    If goog is a Stock and bollinger a strategy (cf. strategy/__init__.py)

    >>> backtest(goog, bollinger) #doctest: +SKIP
    BackTest(trades=[99], position=short, gross=1253.63, net=662.1)

    Current position is short, gross PNL is 1253.63, net PNL taking into account
    the closing of the position and the trading costs if applicable is 662.1.

    Trading costs are 0 by default. To change that set the cost attribute of
    the backtest object to a function taking a trade as an argument and returning
    the cost.

    >>> backtest.cost = lambda trade: 0.5 * trade / 100
    >>> backtest #doctest: +SKIP
    BackTest(trades=[99], position=short, gross=1253.63, net=435.78005)
    """

    sell = {'long': None, None: 'short'}
    buy = {None: 'long', 'short': None}

    def __init__(self):
        self.cost = lambda trade: 0

    def __call__(self, stock, strategy):
        self.stock = stock
        self.strategy = strategy
        self.trades = []
        for t in stock:
            if strategy(t) == 'buy' and self.position != 'long':
                self.trades.append(Trade('buy', t))
            elif strategy(t) == 'sell' and self.position != 'short':
                self.trades.append(Trade('sell', t))
        return self

    def __repr__(self):
        return 'BackTest(trades=[{1}], position={0.position}, gross={0.gross}, \
net={0.net})'.format(self, len(self.trades))

    @property
    def trade_cost(self):
        """ trade cost for the backtest period """
        return self._trade_cost(len(self.stock) - 1)

    def _trade_cost(self, tick_index):
        """ trade cost from start to tick_index """
        return sum(self.cost(abs(trade.tick.close)) for trade in self.trades
                   if trade.tick.index <= tick_index)

    @property
    def gross(self):
        """ gross pnl for the backtest period """
        return self._gross(len(self.stock) - 1)

    def _gross(self, tick_index):
        """ gross pnl from start to tick_index """
        sign = lambda trade: 1 if trade.order == 'sell' else -1
        return sum(sign(trade) * trade.tick.close for trade in self.trades
                   if trade.tick.index <= tick_index)

    @property
    def net(self):
        """ net pnl for the backtest period """
        return self._net(len(self.stock) - 1)

    def _net(self, tick_index):
        """ net pnl from start to tick_index """
        result = 0
        if self._position(tick_index) == 'long':
            result += self.stock[tick_index].close
        elif self._position(tick_index) == 'short':
            result -= self.stock[tick_index].close
        result += self._gross(tick_index)
        result -= self._trade_cost(tick_index)
        return result

    @property
    def position(self):
        """ position at the end of the backtest period """
        return self._position(len(self.stock) - 1)

    def _position(self, tick_index, numeric_flag=False):
        """ position at tick_index 1/0/-1 if numeric_flag """
        position_ = {1: 'long', 0: None, -1: 'short'}
        counter = Counter(trade.order for trade in self.trades
                          if trade.tick.index <= tick_index)
        numeric = counter['buy'] - counter['sell']
        if numeric_flag:
            return numeric
        return position_[counter['buy'] - counter['sell']]

    def plot(self):
        date = [tick.date for tick in self.stock]
        net = [self._net(tick.index) for tick in self.stock]
        position = [self._position(tick.index, True) for tick in self.stock]
        plot_net = subplot(211)
        plot(date, net)
        plot_position = subplot(212, sharex=plot_net)
        ylim(-1.5, 1.5)
        yticks((-1, 0, 1), ('short', '...', 'long'))
        plot(date, position)
        savefig('png/{0}_{1}.png'.format(self.stock.symbol,
                                     self.strategy.__class__.__name__))
        clf()
