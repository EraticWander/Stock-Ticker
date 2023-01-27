from samplebase import SampleBase
from rgbmatrix import graphics
import logging
import time
import dataAPI
import datetime
import threading
from multiprocessing import Process
#importing the module 
import logging 
#now we will Create and configure logger 
logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
#Let us Create an object 
logger=logging.getLogger() 
#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        #--led-rows 16 --led-cols 32 --led-chain 5 --led-slowdown-gpio 1 --led-brightness 50
        
        #get config file that has the stocks we want to see
        path = "/home/pi/ftp/files/stock/config.txt"
        with open(path, 'r') as f:
            self.stocks = f.read()
        self.stocks = self.stocks.strip()
        self.stocks = self.stocks.split(",")
        #call our function which builds out stock list
        self.stockData = dataAPI.getTickerData(self.stocks)

    #function that update the stock list every 10 seconds
    def updatestockData():
        path = "/home/pi/ftp/files/stock/config.txt"
        with open(path, 'r') as f:
            stocks = f.read()
        stocks =stocks.strip()
        stocks = stocks.split(",")
        stockUpdate = dataAPI.getTickerData(stocks)
        logger.info ("Stock Data Updated")
        logger.info (stockUpdate)
        return stockUpdate

    #function that draws the canvas
    def drawTicker(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        #load fonts
        font = graphics.Font()
        font.LoadFont("/home/pi/ftp/files/stock/fonts/clR6x12.bdf")
        fontSub = graphics.Font()
        fontSub.LoadFont("/home/pi/ftp/files/stock/fonts/5x7.bdf")
        #set position to be the size of the canvas
        pos = offscreen_canvas.width
        #set colours
        textColor = graphics.Color(255, 255, 0)
        blueColor = graphics.Color(4, 66, 165)
        greenColor = graphics.Color(0, 168, 36)
        redColor = graphics.Color(153, 6, 1)
        #as long as we are in trading hours the list will update
        stock_data = RunText.updatestockData()
        while self.start_time < self.now < self.end_time:
            offscreen_canvas.Clear()
            # Draw ticker (on what, font, where, size, color, say what)
            # Draw ticker, price, pct_ch placing each after the last position. ex. pos + ticker + 5 + price + 5
            #length is how we space things so its not all right up against eachother
            length = 0
            for c in stock_data: 
                pct_ch = stock_data[c]['pct_ch']
                # makes pct_ch green if positive return
                if float(pct_ch[:-1]) > 0:
                    color = greenColor
                else:
                    color = redColor

                ticker = graphics.DrawText(offscreen_canvas, font, pos + length, 8, textColor, c)
                price = graphics.DrawText(offscreen_canvas, fontSub, pos + length, 15, blueColor, str(stock_data[c]['price']))
                pct_ch_len = graphics.DrawText(offscreen_canvas, fontSub, pos + price + 5 + length, 15, color, str(pct_ch))
                length += price + 5 + 5 + pct_ch_len

            #counts down the position, once zero it breaks the function
            pos -= 1
            if (pos + length  < 0):
                pos = offscreen_canvas.width
                stock_data = RunText.updatestockData()
                self.now = (datetime.datetime.now() - datetime.timedelta(hours=0)).time()

            #sets the speed for how fast the words go across the canvas    
            time.sleep(0.03)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        return

    def run(self):
        logger.info ("Run")
        # To turn off when sleeping
        #define the start and end times and reports what time it is currently
        self.start_time = datetime.time(hour=6, minute=25)
        self.end_time = datetime.time(hour=13, minute=5)
        self.now = (datetime.datetime.now() - datetime.timedelta(hours=0)).time()
        logger.info  (self.now)
        #start updating stock fucntion in thread
        #threading.Thread(target=RunText.updatestockData, args=(self, )).start()
        #start drawing canvas function in thread
        threading.Thread(target=RunText.drawTicker, args=(self, )).start()


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
