'''
# This file helps in getting market orders and using them with stop loss and updates about the positions of
different instruments
'''

import oandapyV20
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.accounts import AccountDetails
from oandapyV20.endpoints.orders import OrderCreate
from oandapyV20.endpoints.positions import PositionClose
import oandapyV20.endpoints.trades as trades
import time
import json
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest, TrailingStopLossDetails
#
# from config_oanda import api_key, account_id, stop_loss_pct, units, period, atr_multiplier, instrument, time_in_force, trailing_stop_loss_distance, stop_loss
#

def create_market_order_with_trailing_stop_loss(api_key, account_id, instrument, units, trailing_stop_loss_distance):
    # Create an instance of the API
    client = API(access_token=api_key)

    # Calculate the trailing stop loss distance
    trailing_stop_loss_distance = trailing_stop_loss_distance

    # Create the TrailingStopLossDetails object
    trailing_stop_loss_on_fill = TrailingStopLossDetails(distance=trailing_stop_loss_distance)

    # Create the MarketOrderRequest object
    order_request = MarketOrderRequest(
        instrument=instrument,
        units=units,
        trailingStopLossOnFill=trailing_stop_loss_on_fill.data
    )

    # Print the order details
    print(json.dumps(order_request.data, indent=4))

    # Create the order
    order_create = orders.OrderCreate(account_id, data=order_request.data)

    try:
        # Send the order request
        response = client.request(order_create)

        # Process the response
        if response.get("orderCreateTransaction") is not None:
            print("Order created successfully.")
            print("Order ID:", response.get("orderCreateTransaction").get("id"))
        elif response.get("orderRejectTransaction") is not None:
            print("Order creation failed.")
            print("Error:", response.get("orderRejectTransaction").get("rejectReason"))
        else:
            print("Unknown response format:", response)

    except oandapyV20.exceptions.V20Error as e:
        print("Error occurred during order creation:", str(e))

# create_market_order_with_trailing_stop_loss()




def get_all_positions(api_key, account_id):
    '''
    :return: Returns a list of all open positions of instrument along with their order details
    '''
    # config = get_config()
    api = API(access_token= api_key, environment="practice")

    r = trades.OpenTrades(accountID=account_id)
    rv = api.request(r)

    positions = rv['trades']
    return list(positions)

# print(get_all_positions())


def get_position(api_key, account_id, instrument):
    '''

    :param instrument: Instrument for which you want to stream the data
    :return: Returns the quatity, side and instrument imn position in same order
    '''
    all_positions = get_all_positions(api_key, account_id)

    for position in all_positions:
        if position['instrument'] == instrument:
            quantity = int(position['currentUnits'])
            side = "Long" if quantity > 0 else "Short"
            instrument = position['instrument']
            return {'quantity': quantity, 'side': side, 'instrument': instrument}

    return None

# print(get_position('EUR_USD'))


def close_positions(api_key, account_id, instrument):
    '''
    :param instrument: Instrument for which you want to stream the data
    :return: Closes specific trade with the instrument
    '''

    api = API(access_token=api_key, environment="practice")
    r = trades.OpenTrades(accountID=account_id)
    rv = api.request(r)

    open_trades = rv["trades"]

    for trade in open_trades:
        if trade["instrument"] == instrument:
            trade_id = trade["id"]
            break
    else:
        print("No open trade found for the specified symbol.")
        return

    r = trades.TradeClose(accountID=account_id, tradeID=trade_id)
    api.request(r)

    print(f"Closing specific trade with symbol: {instrument}")

# close_positions('USD_CHF')


def close_all_positions(api_key, account_id):
    '''
    :return: Closes all the open trades.
    '''
    api = API(access_token=api_key, environment="practice")

    # Get all open positions
    r = trades.OpenTrades(accountID=account_id)
    response = api.request(r)
    open_trades = response['trades']

    if not open_trades:
        print("No open trades to close.")
        return

    # Close each trade
    for trade in open_trades:
        trade_id = trade['id']
        instrument = trade['instrument']
        data = {
            "units": "ALL"
        }
        r = trades.TradeClose(accountID=account_id, tradeID=trade_id, data=data)
        api.request(r)
        print(f"Trade with ID {trade_id} for instrument {instrument} has been closed.")
        time.sleep(0.5)  # Add a delay to avoid rate limit issues


