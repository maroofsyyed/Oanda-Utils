"""
This file helps in implementing the strategy defined in this repo
Contents of config_oanda.ini will provide parameters required in this file.
"""
from config_oanda import api_key1 , account_id1, instrument2, timeframe
from oandaUtils import orders
from oandaUtils import order_with_bollinger_bands
from oandaUtils.realtime_oanda_forex_data import fetch_realtime_oanda_data
import warnings
warnings.filterwarnings("ignore")


#close all the open positions
orders.close_all_positions(api_key1, account_id1)


# run the strategy on realtime data from oanda api and connecting trades with oanda forex paper trading account
fetch_realtime_oanda_data(api_key1, account_id1, instrument2, timeframe, indicator = order_with_bollinger_bands.order_with_bollinger_bands)