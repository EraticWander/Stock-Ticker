# Stock-Ticker
Stock ticker that runs across LED display modules. Stock info is grabbed from yahoo finance using yfinance librar

Need to have rpi-rgb-led-matrix installed:
https://github.com/hzeller/rpi-rgb-led-matrix

yfinance Library:
https://github.com/ranaroussi/yfinance

Used these LED modules:
https://www.aliexpress.com/item/32997717322.html?spm=a2g0o.order_list.order_list_main.76.47121802s7ga6f

Project is run from a RaspberryPI 3B

Example for running this script:
stock.py --led-rows 16 --led-cols 32 --led-chain 5 --led-slowdown-gpio 1 --led-brightness 50

--led-rows is the number of pixels a single module has from top to bottom
--led-cols is the number of pixels a single module has from left to right
--led-chain is the number of these modular that you have chainned together
--led-slowdown-gpio & --led-brightness are used to correct colour and artifacts on display. Read more from https://github.com/hzeller/rpi-rgb-led-matrix

Note, I am not a programmer by trade, this is all a hobby of mine, so the code is very rough and likely filled with bugs. I am using this all to learn more about scraping and machine learning
