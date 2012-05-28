#!/usr/bin/env python
# encoding: utf-8

import code

from lib import Stock, BackTest
from strategy import Bollinger, Monkey


def help():
    print open('README.rst').read()

banner = """Back Testing Trading Strategy Console
type help() for assistance."""
bollinger = Bollinger(30, 1)
monkey = Monkey(30)
goog = Stock('GOOG')
backtest = BackTest()
backtest(goog, bollinger)
backtest.cost = lambda trade: 0.5 * trade / 100


code.interact(banner=banner, local=locals())
