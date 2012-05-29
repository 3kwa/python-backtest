"""
Use this folder to define your trading strategies.

A strategy is a callable object taking a Tick (cf. lib/tick.py) as an
argument and returns 'buy', 'sell' or None.

Use __init__(self, ...) to define the strategy parameters at instantiation e.g.
the Bollinger band strategy takes 2 parameters the period N and the width of
the band K : Bollinger(N, K)

>>> bollinger = Bollinger(30, 1)

Define your strategy in the magic method __call__(self, tick) in order to be
able to call the strategy with a Tick.

>>> bollinger(tick) #doctest: +SKIP
'sell'
"""

from bollinger import Bollinger
from monkey import Monkey
