from fastapi import FastAPI
from starlette.responses import JSONResponse
from joblib import load
import pandas as pd
import os

app = FastAPI()
#Loading the acb_pipeline file
model_file_path_api = '/machinelearning_as_a_service/models/predicting/gcb_pipeline.joblib'

gcb_pipe = load(model_file_path_api)

# Define a function to format features
def format_features(date: str, Day_of_sales: int,store_id: str,item_id:str, event_name: str, event_type: str, Sales_value: float, sell_price: float, revenue: float):
    return {
       'date': [date],
       'Day_of_sales': [Day_of_sales],
       'store_id':[store_id],
       'item_id':[item_id],
       'event_name': [event_name],
       'event_type': [event_type],
       'Sales_value': [Sales_value],
       'sell_price': [sell_price],
       'revenue': [revenue]
    }

# Define the root endpoint
@app.get("/")
def read_root():
    return {"Description": """A predictive model uses a machine learning algorithm to accurately predict the sales revenue for a given item in a specific store at a given date. A forecasting model using a time-series analysis algorithm that will forecast the total sales revenue across all stores and items for the next 7 days.""",
           "List of Endpoints": """prediction endpoint: https://mahjabeen-fastapi.herokuapp.com/stores/sales/prediction,Forcasting endpoint: https://mahjabeen-fastapi.herokuapp.com/forecast/, HealthCheck EndPoint:https://mahjabeen-fastapi.herokuapp.com/health/""",
           "Expected Input parameters for predictive model": """date=2011-02-06,Day_of_sales=9,store_id=TX_1,item_id=HOUSEHOLD_1_537,event_name=SuperBowl,event_type=Sporting,Sales_value=3.0,sell_price=15.98,revenue=47.94""",
           "Expected OutPut": "[47.80684273195466]",
           "GitHub Link": "https://github.com/MAHJABEENMOHIUDDIN/fastapi.git"}

# Define an endpoint to provide information about the sales model
@app.get("/health/")
async def health_check():
    welcome_message="Welcome to the FastAPI application. It's healthy!"
    return {"message": welcome_message}

# Define an endpoint for predicting sales
@app.get("/stores/sales/prediction")
def predict(
      date: str,
      Day_of_sales: int,
      store_id: str,
      item_id: str,
      event_name: str,
      event_type: str,
      Sales_value: float,
      sell_price: float,
      revenue: float,
):
    features = format_features(
        date,
        Day_of_sales,
        store_id,
        item_id,
        event_name,
        event_type,
        Sales_value, 
        sell_price,
        revenue
    )
       
    obs = pd.DataFrame(features)
    pred = gcb_pipe.predict(obs)
    return JSONResponse(pred.tolist())

# This part is used for logging, you can remove it if not needed
import logging

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)

# Log a message
logging.debug("Debug message")
#Reading the forcasting model
model_file_path_api1 = '/machinelearning_as_a_service/texas_store_sales_predictive_api/models/arima_forecasting_2.joblib'
arima_model = load(model_file_path_api1)
 
@app.get("/forecast/")
async def forecast_sales():
      forecast_data = {
            "message": "The forecast of the next 7 days sales are:",
            "forecast": arima_model.values.tolist()
        }

      return forecast_data
