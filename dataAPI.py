import yfinance as yf

# Figures out % change from closing price of previous day and current stock price
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

# takes in a list of ticker symbols, gets the current price and previous day closing price, outputs dictionary
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

