import yfinance as yf
import time
import datetime
import numpy

#get stock price from Yahoo

def price_diff(preClose, lastPrice):
    p1 = float(lastPrice)
    p2 = float(preClose)
    if p2 > p1:
        pctDiff = 100*(p2-p1)/p1
        return ("%.2f" %pctDiff) + "%"
    elif p2 < p1:
        pctDiff = 100*(p2-p1)/p1
        return ("%.2f" %pctDiff) + "%"
    elif p2 == p1:
        pctDiff = 0
        return ("%.2f" %pctDiff) + "%"

def getTickerData(stocks):
    tickerData = {}
    for x in stocks:
        ticker = yf.Ticker(x)
        #current price
        history = ticker.history()
        lastPrice = history['Close'][-1]

        #previous day close
        preClose = history['Close'][-2]
        pctChange = price_diff(lastPrice, preClose)
        tickerData[x] = {'price':lastPrice, 'pct_ch':pctChange}
    return tickerData

