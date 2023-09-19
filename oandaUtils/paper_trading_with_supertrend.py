"""
This file helps in implementing the strategy defined in this repo
Contents of config_oanda.ini will provide parameters required in this file.
"""
from oandaUtils import orders
from oandaUtils import order_with_supertrend
from oandaUtils.realtime_oanda_forex_data import fetch_realtime_oanda_data
import warnings
from config_oanda import api_key, account_id, instrument, timeframe
warnings.filterwarnings("ignore")

orders.close_all_positions(api_key, account_id)


# run the strategy on realtime data from oanda api and connecting trades with oanda forex paper trading account
fetch_realtime_oanda_data(api_key, account_id, instrument, timeframe,indicator = order_with_supertrend.place_orders_with_supertrend)




