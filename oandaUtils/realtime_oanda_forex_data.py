'''
The file is used to stream realtime forex data from oanda api data and run indicator functions over the data streamed.
'''

import time
import pandas as pd
import requests
from config_oanda import api_key, account_id, instrument, timeframe

def fetch_realtime_oanda_data(api_key, account_id, instrument, timeframe, indicator=None, *args, **kwargs):
    global df
    url = f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments/{instrument}/candles"

    # Define the headers with authorization bearer token
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept-Datetime-Format": "RFC3339"}

    # Define the query parameters
    params = {
        "granularity": timeframe,  # Specify the desired granularity (e.g., M1 for 1 minute)
        "count": 700  # Specify the number of candles to retrieve
    }

    df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

    in_position = False
    stop_loss_price = 0

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            candles_data = response.json()["candles"]
            temp_df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

            for candle in candles_data:
                timestamp = candle["time"]
                open_price = float(candle["mid"]["o"])
                high_price = float(candle["mid"]["h"])
                low_price = float(candle["mid"]["l"])
                close_price = float(candle["mid"]["c"])
                volume = float(candle["volume"])

                temp_df = temp_df.append({
                    "timestamp": timestamp,
                    "open": open_price,
                    "high": high_price,
                    "low": low_price,
                    "close": close_price,
                    "volume": volume
                }, ignore_index=True)

            params["count"] = len(candles_data)

            df = df.append(temp_df, ignore_index=True)
            df = df.drop_duplicates(subset="timestamp")
            print(df)
            # print(df.dtypes)

            # Running the specified Indicator Function
            if indicator is not None:
                indicator(df, *args, **kwargs)

        time.sleep(60)  # Delay between each request (e.g., 60 seconds)


# fetch_realtime_oanda_data(api_key, account_id, instrument, timeframe)