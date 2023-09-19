# oandaUtils

### This folder contains necessary files and to run paper trading on realtime forex data
![53E4491A-0435-4907-88F8-EAB7E304985B_1_201_a.jpeg](images%2F53E4491A-0435-4907-88F8-EAB7E304985B_1_201_a.jpeg)

#### This folder has paper trading built on 2 data providers
###  1. twelvedata:

twelvedata provide ohlc of forex data but only for these Supported intervals: "1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month"
it provides 800 api requests/day through its free version

All config parameters of twelvedata are there in config_12data.ini 

### 2.  oanda 

Oanda does not provide exact ohlc data however it converts the ask and bid price into ohlc data by taking its average called mid and then calculating the ohlc of the mid price 
however this technique is widely used 

All config parameters of twelvedata are there in config_oanda.ini 

orders.py and order_with_supertrend is common for both of them



#### Steps to Run Paper Trading

1. Clone the project somewhere.

2. You may need to install needed packages using requirements.txt inside the oandaUtils folder

3. Make sure you have Indicators and alpacaUtils packages installed in your environment.

4. Now open config.ini file in any text editor, and add the values you want to give to our
program. Restrict using special characters even for strings. Use them wherever necessary.

5. Now run either paper_trading_with_oanda_data.py or paper_trading_with_12data.py


### Comparing the OHLC data from Oanda WEB, Tradingview and the one which is fetched by realtime_oanda_forex_data.py


#### i) Onada Web

Below is the OHLC of EUR_JPY stock at 22 Jun'23 10:10 from the Oanda Web 

![Image 22-06-23 at 3.52 PM.jpg](images%2FImage%2022-06-23%20at%203.52%20PM.jpg)


#### ii) Tradingview 

Below is the OHLC of EUR_JPY stock at 22 Jun'23 10:10 from the Tradingview

![Image 22-06-23 at 3.42 PM.jpg](images%2FImage%2022-06-23%20at%203.42%20PM.jpg)


#### iii) realtime_oanda_forex_data.py

Below is the OHLC of EUR_JPY stock at 22 Jun'23 10:10 from our function realtime_oanda_forex_data.py

![Image 22-06-23 at 3.41 PM.jpg](images%2FImage%2022-06-23%20at%203.41%20PM.jpg)


We can conclude from above that the OHLC calculation that is,

    open_price = float(candle["mid"]["o"])
    high_price = float(candle["mid"]["h"])
    low_price = float(candle["mid"]["l"])
    close_price = float(candle["mid"]["c"])

where mid is the average of ask and bid seems to be correct.


### Comparing the OHLC data from twelvedata WEB, Tradingview and the one which is fetched by realtime_12data_forex_data.py


#### i) Onada Web

Below is the OHLC of EUR_JPY stock at 22 Jun'23 23:27 from the Oanda Web 
![Screenshot 2023-06-22 at 6.59.38 PM.jpg](images%2FScreenshot%202023-06-22%20at%206.59.38%20PM.jpg)




#### ii) Tradingview 

Below is the OHLC of EUR_JPY stock at 22 Jun'23 23:27 from the Tradingview

![Screenshot 2023-06-22 at 6.59.54 PM.jpg](images%2FScreenshot%202023-06-22%20at%206.59.54%20PM.jpg)




#### iii) realtime_12data_forex_data.py

Below is the OHLC of EUR_JPY stock at 22 Jun'23 23:27 from our function realtime_12data_forex_data.py

![Image 22-06-23 at 7.01 PM.jpg](images%2FImage%2022-06-23%20at%207.01%20PM.jpg)


We can conclude from above that the OHLC data that twelvedata OHLC data is not accurate it is truncated
