import requests
import pandas as pd
import time

def get_stock_data(api_key, symbol):
    # Define the API endpoint and parameters
    endpoint = 'https://finnhub.io/api/v1/stock/candle'
    resolution = 'D'

    # Define the features used for prediction
    features = ['o', 'h', 'l', 'c', 't', 'v']

    # Get the data from the past year
    now = int(pd.Timestamp.now().timestamp())
    from_time = now - (86400 * 365)
    params = {
    'symbol': 'AAPL',
    'resolution': 'D',
    'from': int(time.time()) - 86400*30, # 86400 seconds in a day
    'to': int(time.time()),
    'token': 'cgcvrtpr01qum7u5pd7gcgcvrtpr01qum7u5pd80'
    }

    response = requests.get(endpoint, params=params)

    # Check if API request was successful
    if response.status_code != 200:
        print(f"Error {response.status_code} - API request unsuccessful")
        return None

    # Load the API response data into a Pandas DataFrame
    data = response.json()
    df = pd.DataFrame({features[i]: data[i] for i in range(len(features))})

    # Rename the timestamp column and set it as the DataFrame index
    df = df.rename(columns={'t': 'Timestamp'}).set_index('Timestamp')

    # Convert the timestamp from Unix time to a Pandas DateTime object
    df.index = pd.to_datetime(df.index, unit='s')

    # Sort the DataFrame by timestamp in ascending order
    df = df.sort_index()

    return df
