import random

class Monkey(object):
    """ Silly monkey strategy every freq tick roll the dice

    To instantiate a 30 tick monkey:

    >>> monkey = Monkey(30)
    """

    def __init__(self, freq):
        self.freq = freq

    def __call__(self, tick):
        if tick.index % self.freq:
            return None
        return random.choice(('buy', 'sell', None))
