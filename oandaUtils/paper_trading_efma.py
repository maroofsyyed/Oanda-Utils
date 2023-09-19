"""
This file helps in implementing the strategy defined in this repo
Contents of config_oanda.ini will provide parameters required in this file.
"""
from oandaUtils import orders
from oandaUtils import order_with_efma
from oandaUtils.realtime_oanda_forex_data import fetch_realtime_oanda_data
import warnings
from config_oanda import api_key2, account_id2, instrument1, timeframe
warnings.filterwarnings("ignore")

orders.close_all_positions(api_key2, account_id2)


# run the strategy on realtime data from oanda api and connecting trades with oanda forex paper trading account

fetch_realtime_oanda_data(api_key2, account_id2, instrument1, timeframe, indicator = order_with_efma.place_orders_with_fibonacci)