"""
The file contains the strategy function that uses the efma indicator with a trailing stop loss.
It checks for a signal and executes buy and sell trades accordingly.
"""


from orders import get_position, get_all_positions, close_positions, create_market_order_with_trailing_stop_loss
from Indicators import efma_indicator
from realtime_oanda_forex_data import fetch_realtime_oanda_data
from config_oanda import api_key2, account_id2, stop_loss_pct, units, period, atr_multiplier, instrument1, time_in_force, trailing_stop_loss_distance, stop_loss

def place_orders_with_fibonacci(data, stop_loss_pct=stop_loss_pct, atr_multiplier=atr_multiplier):
    '''
    :param data: pandas dataframe object containing the forex data
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :param atr_multiplier: Generally initialized to 2 or 3
    :return: Returns the trend signal
    '''

    data = efma_indicator.enhanced_fibonacci_moving_average(data)  # Calculate Fibonacci Moving Averages


    signal = data['signal']
    print(signal)
    close = data['close']

    # Initial conditions
    in_position = False
    stop_loss_price = 0

    position = get_position(api_key2, account_id2,instrument1)

    if position is None or position['quantity'] <= 0 or position['side'] is None:
        in_position = False
    elif int(position['quantity']) > 0:
        in_position = True
    print(f"Position is {in_position}")

    for i in range(len(data) - 1, len(data)):
        print("Checking with the indicator")
        # If not in position and price is below lower band -> buy
        if not in_position and signal[i] == 1:
            print("Buy signal detected, placing buy order")
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set stop loss price
            create_market_order_with_trailing_stop_loss(api_key2, account_id2, instrument1, units,
                                                       trailing_stop_loss_distance)
            in_position = True  # Update position flag to True after buying

        # If in position and price is above upper band or hits stop loss -> sell
        elif in_position and (signal[i] == -1 or close[i] < stop_loss_price):
            print("Sell signal detected, placing sell order")
            stop_loss_price = 0  # Reset stop loss price
            close_positions(api_key2, account_id2, instrument=instrument1)
            in_position = False  # Update position flag to False after selling