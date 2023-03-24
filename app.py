"""
This module contains the Flask app for stock prediction.
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from tensorflow import keras
from finnubapi import get_stock_data

app = Flask(__name__)
CORS(app)

model = keras.models.load_model('model.h5')

# load the latest data from the CSV file
df_ = pd.read_csv('AAPL_daily_candles.csv')

@app.route('/')
def home():
    
    """
    Renders the 'index.html' template, which serves as the homepage for the application.

    Returns:
    --------
    str:
        The rendered HTML content of the 'index.html' template.
    """
    return render_template('index.html')

@app.route('/predict')
def predict():
    
    """
    Load the latest data from a CSV file, prepare the data for training and testing the machine learning model,
    train the model, make predictions on the test data, calculate the mean squared error (MSE) and mean absolute error (MAE),
    calculate the accuracy, and return a JSON response containing the accuracy, MSE, and a prediction for the next day.

    Returns:
    JSON: A JSON response containing the accuracy, MSE, and a prediction for the next day.
    """

    # use the last 30 rows for testing and the rest for training
    x_train = df_.iloc[:-30, 0].values.reshape(-1, df_.iloc[:-30, 0].shape[0], 1)
    y_train = df_.iloc[:-30, 1].values
    x_test = df_.iloc[-30:, 0].values.reshape(-1, df_.iloc[-30:, 0].shape[0], 1)
    y_test = df_.iloc[-30:, 1].values

    # train the model on the training data
    model.fit(x_train, y_train, epochs=10)

    # make predictions on the test data
    y_pred = model.predict(x_test)

    # calculate accuracy and MSE
    mse = np.mean(np.square(y_pred - y_test))
    mae = np.mean(np.abs(y_pred - y_test))
    accuracy = (1 - mae) * 100

    # get the prediction for the next day
    next_day_prediction = model.predict(x_test[-1].reshape(1, 30, 1))[0][0]

    return jsonify({'accuracy': accuracy, 'mse': mse, 'prediction': next_day_prediction})


if __name__ == '__main__':
    app.run(debug=True)
