## Predicting Stock Prices with LSTM and Flask
This is a project that aims to predict stock prices using Long Short-Term Memory (LSTM) models and Flask framework.

# Requirements
To run this project, you need to have the following requirements installed:

Python 3
Docker
To install Python 3, you can follow the instructions provided on the official website. To install Docker, you can follow the instructions provided on the official website.

# Installation
To install this project, you can follow these steps:

- Clone this repository to your local machine using the following command:
git clone https://github.com/your-username/predicting-stock-prices-with-lstm-and-flask.git
Replace your-username with your actual username on GitHub.

- Navigate to the project directory:
cd predicting-stock-prices-with-lstm-and-flask

- Create a virtual environment for the project:
python -m venv venv

- Activate the virtual environment:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/Linux

Install the required packages:
pip install -r requirements.txt

# Usage
To use this project, you can follow these steps:

Start the Flask app:
flask run

1) Open your web browser and go to http://localhost:5000/ to access the index page.
2) Enter the stock symbol (e.g., AAPL for Apple Inc.) and the number of days to predict, then click the "Predict" button.
3) Wait for the prediction to be displayed on the web page.
4) To view the dashboard, go to http://localhost:5000/dashboard on your web browser.

The dashboard will display a line chart that shows the actual and predicted stock prices over time, as well as the accuracy of the model.

# Docker
This project also includes a Dockerfile that you can use to build a Docker image for the project. To do so, you can follow these steps:

Build the Docker image:
docker build -t predicting-stock-prices .

Run the Docker container:
docker run -p 5000:5000 predicting-stock-prices

Access the Flask app in your web browser at http://localhost:5000/ as usual.

# Credits
This project was inspired by the following resources:

Predicting Stock Prices with LSTM by Pablo Castilla
How to Build a Python Flask Web App Serverless with AWS Lambda, API Gateway, & DynamoDB by Tech with Tim
