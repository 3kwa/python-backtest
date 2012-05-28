import random

class Monkey(object):
    """ Silly monkey strategy every freq days roll the dice """

    def __init__(self, freq):
        self.freq = freq

    def __call__(self, tick):
        if tick.index % self.freq:
            return None
        return random.choice(('buy', 'sell', None))
