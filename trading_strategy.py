from __future__ import print_function

from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma
import random
import matplotlib.pyplot as plt 
import datetime
import numpy as np
import os


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, model_predictor, date_to_portfolio, start_date, date_to_tweets):
        super(MyStrategy, self).__init__(feed, 30000)
        self.__position = None
        self.__instrument = instrument
        self.predictor = model_predictor
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        #self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.results = date_to_portfolio
        self.start = start_date
        self.date_to_tweets = date_to_tweets

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        #if self.__sma[-1] is None:
            #return

        bar = bars[self.__instrument]
        if bar.getDateTime() < self.start:
            return
        if bar.getDateTime() not in self.date_to_tweets:
            return 

        self.results[bar.getDateTime()] = self.getBroker().getEquity()
        percent_change = (self.predictor.predict(np.array([self.date_to_tweets[bar.getDateTime()]])))[0][0]
        

        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            #if bar.getPrice() > self.__sma[-1]:
            if percent_change > 0:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        #elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
        elif percent_change < 0 and not self.__position.exitActive():
            self.__position.exitMarket()

class RandomPredictor(object):
    def __init__(self):
        self.me = None

    def predict(self, x):
        return x + random.uniform(-1, 1)


def run_strategy(rp, ticker, results_dict, start_date, date_to_tweets):
    # Load the bar feed from the CSV file
    file_name = os.path.join('financial_data', 'EOD-' + ticker + '.csv')
    feed = quandlfeed.Feed()
    feed.addBarsFromCSV(ticker, file_name)

    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, ticker, rp, results_dict, start_date, date_to_tweets)
    myStrategy.run()
    print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())


#date_to_portfolio = {}
#rp = RandomPredictor()
#start_date = datetime.datetime(2016, 1, 1)
#run_strategy(rp, date_to_portfolio, start_date)

'''
date_to_portfolio = {}
rp = RandomPredictor()
run_strategy(1, rp, date_to_portfolio)
#print(date_to_portfolio)
X = []
Y = []
for k, v in date_to_portfolio.items():
    X.append(k)
    Y.append(v)

plt.plot(X, Y)
plt.show()
'''


