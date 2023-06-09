"""
The `model` module provides a function to train a recurrent neural network model on
historical stock prices and make predictions for future prices.

The module requires `tensorflow` and `pandas` packages to be installed.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import finnhub
"""
The `train_model` function takes the following parameters:
- `Symbol`: a string representing the stock symbol to train the model on
- `Interval`: a string representing the Interval of the historical stock prices, 
              e.g. "1d" for daily or "1h" for hourly
- `seq_length`: an integer representing the length of the input sequence for the RNN model
- `epochs`: an integer representing the number of epochs to train the model for
- `batch_size`: an integer representing the batch size to use during training

The function returns the trained Keras model.

Example usage:
"""
# connect to FinnHub API
finnhub_client = finnhub.Client(api_key="cgcvrtpr01qum7u5pd7gcgcvrtpr01qum7u5pd80")

# define the stock symbol and time Interval
SYMBOL = 'AAPL'
INTERVAL = 'D'

# retrieve historical stock data from FinnHub API
res = finnhub_client.stock_candles(SYMBOL, INTERVAL, 1590988249, 1622524249)

# convert the response to a pandas dataframe
df = pd.DataFrame(res)

# drop columns except for date and close
df.drop(['o', 'h', 'l', 'v', 's'], axis=1, inplace=True)

print(df.columns)

# rename the columns
df.columns = ['ds', 'y']

# convert the date column to datetime format
df['ds'] = pd.to_datetime(df['ds'], unit='s')

# sort the dataframe by date
df.sort_values('ds', inplace=True)

# set the date column as the index
df.set_index('ds', inplace=True)

# save the dataframe as a CSV file
df.to_csv('AAPL_daily_candles.csv')

# split the dataset into train and test sets
train_size = int(len(df) * 0.8)
train_df, test_df = df.iloc[:train_size], df.iloc[train_size:]

# scale the data to range of 0 to 1
scaler = MinMaxScaler()
train_scaled = scaler.fit_transform(train_df)
test_scaled = scaler.transform(test_df)

# function to create input/output sequences
def create_sequences(data, seq_len):
    """ The create_sequences function creates sequences for training
    the model by taking the input data and sequence length as arguments.
    It returns the input sequence X_ and the corresponding output sequence y_.
    The X_ and y_ arrays are created by looping over the data array and
    appending the values to the arrays.
    """
    eks = []
    wei = []
    for i in range(seq_len, len(data)):
        eks.append(data[i-seq_len:i, 0])
        wei.append(data[i, 0])
    return np.array(eks), np.array(wei)

# create input/output sequences for train and test sets
seq_length = 30
X_train, y_train = create_sequences(train_scaled, seq_length)
X_test, y_test = create_sequences(test_scaled, seq_length)

# reshape the input data for LSTM
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# build the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(seq_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=2)

# evaluate the model on the test set
score = model.evaluate(X_test, y_test, verbose=0)
print(f'Test loss: {score}')

# make predictions on the test set
y_pred = model.predict(X_test)

# create a dataframe to store the predictions and actual values
pred_df = pd.DataFrame({'ds': test_df.index[seq_length:],
                        'y_true': test_df['y'].values[seq_length:],
                        'y_pred': y_pred.reshape(-1)})

# convert the date column back to datetime format
pred_df['ds'] = pd.to_datetime(pred_df['ds'])

# set the date column as the index
pred_df.set_index('ds', inplace=True)

# calculate the mean absolute error (MAE)
mae = np.mean(np.abs(pred_df['y_true'] - pred_df['y_pred']))
print(f'MAE: {mae:.2f}')

# save the model
model.save('model.h5')
