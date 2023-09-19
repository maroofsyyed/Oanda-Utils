"""
The file contains the strategy function that uses the Supertrend indicator with a trailing stop loss.
It checks for an uptrends and downtrends based on the Supertrend indicator and executes buy and sell trades accordingly.
"""

from orders import get_position, get_all_positions, close_positions,create_market_order_with_trailing_stop_loss
from Indicators import supertrend
from config_oanda import api_key, account_id, stop_loss_pct, units, period, atr_multiplier, instrument, time_in_force, trailing_stop_loss_distance, stop_loss


def place_orders_with_supertrend(data, stop_loss_pct = stop_loss_pct, period= period, atr_multiplier=atr_multiplier ):
    '''

    :param data:pandas dataframe object containing the forex data
    :param stop_loss_pct:Percentage value to set the trailing stop loss
    :param period:period parameter for supertrend calculation
    :param atr_multiplier: generally initialised to 2 OR 3
    :return: returns the trend signal
    '''
    # global stop_loss_price, in_position


    data['Supertrend'] = supertrend.supertrend(data, period=period, atr_multiplier=atr_multiplier)['Supertrend']
    is_uptrend = data['Supertrend']
    close = data['close']

    # Initial conditions
    in_position = False
    stop_loss_price = 0

    position = get_position(api_key, account_id, instrument)

    if position is None or position['quantity'] <= 0 or position['side'] is None:
        in_position = False
    elif int(position['quantity']) > 0:
        in_position = True
    print(f"Position is {in_position}")

    for i in range(len(data)-1, len(data)):
        print("Checking with the indicator")
        # If not in position and price is on uptrend -> buy
        if not in_position and is_uptrend[i]:      # is_uptrend[i] should be changed too
            print("Uptrend Spotted, Buying")
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price
            # create_market_order_with_trailing_stop_loss(instrument=instrument, units=units, time_in_force=time_in_force,
            #                                     position_fill='DEFAULT', take_profit=None, stop_loss=stop_loss,
            #                                     trailing_stop_loss_distance=trailing_stop_loss_distance)
            create_market_order_with_trailing_stop_loss(api_key, account_id, instrument, units,
                                                          trailing_stop_loss_distance)


        # If in position and price is on downtrend or hits stop loss -> sell
        elif in_position and (not is_uptrend[i] or close[i] < stop_loss_price):
            print("Downtrend Spotted, closing the bought asset")
            stop_loss_price = 0  # Reset stop loss price
            close_positions(instrument=instrument)
            in_position = False




