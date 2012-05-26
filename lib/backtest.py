class BackTest(object):

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
        return self.last.close - self.first.close

