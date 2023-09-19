"""
The file contains the strategy function that uses the bollingder bands indicator with a trailing stop loss.
It checks for a buy and sell signal based on the bollingder bands indicator and executes buy and sell trades accordingly.
"""

from orders import get_position, get_all_positions, close_positions,create_market_order_with_trailing_stop_loss
from Indicators import bollinger_bands
from config_oanda import api_key1, account_id1, stop_loss_pct, units, period, atr_multiplier, instrument2, time_in_force, trailing_stop_loss_distance, stop_loss, std_multiplier



def order_with_bollinger_bands(data, stop_loss_pct=stop_loss_pct, period=period, std_multiplier=std_multiplier):
    '''
    Executes buy and sell orders based on the Bollinger Bands indicator.
    :param data: pandas dataframe object containing the forex data
    :param stop_loss_pct: Percentage value to set the stop loss
    :param period: Period parameter for Bollinger Bands calculation
    :param std_multiplier: Standard deviation multiplier for Bollinger Bands calculation
    '''
    bollinger_data = bollinger_bands.bollinger_bands(data, period=period, std_multiplier=std_multiplier)
    print("Length of data:", len(data))
    print("Length of bollinger_data:", len(bollinger_data))

    data['Signals'] = bollinger_data['Signals']
    signals = data['Signals']
    close = data['close']
    print(signals)

    # Initial conditions
    in_position = False
    stop_loss_price = 0

    position = get_position(api_key1, account_id1, instrument2)

    if position is None or position['quantity'] <= 0 or position['side'] is None:
        in_position = False
    elif int(position['quantity']) > 0:
        in_position = True
    print(f"Position is {in_position}")

    for i in range(len(data) - 1, len(data)):
        print("Checking with the indicator")
        # If not in position and price is below lower band -> buy
        if not in_position and signals[i] == 1:
            print("Buy signal detected, placing buy order")
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set stop loss price
            create_market_order_with_trailing_stop_loss( api_key1, account_id1, instrument2, units,
                                                       trailing_stop_loss_distance)
            in_position = True  # Update position flag to True after buying

        # If in position and price is above upper band or hits stop loss -> sell
        elif in_position and (signals[i] == -1 or close[i] < stop_loss_price):
            print("Sell signal detected, placing sell order")
            stop_loss_price = 0  # Reset stop loss price
            close_positions(api_key1, account_id1, instrument2)
            in_position = False  # Update position flag to False after selling