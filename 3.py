import requests 
import time 
import json 
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator 
from airflow.operators.python import BranchPythonOperator 
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta 
import pandas as pd 
import numpy as np 
import os


def get_data(**kwargs): 
    ticker = kwargs['tickers']
    api_key = "1CGXHE50GPTTBW21"
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + ticker + '&apikey=' + api_key
    r = requests.get(url)

    try:
        data = r.json()
        path = "r\\C:\\Users\\Asus\\airflow-test\\data_center\\data_lake"
        with open(path + "stock_market_row_data_" + ticker + '_' + str(time.time()), "w") as outfile:
            json.dump(data, outfile)
    except:
        pass


default_dag_args = { 
    'start_date': datetime(2023,1,26), 
    'email_on_failure': False, 
    'email_on_retry': False, 
    'retries': 1, 
    'retry_delay': timedelta(minutes=5), 
    'project_id': 1 
}


with DAG("3_market_data_alphavantage_DAG", schedule_interval = '@daily', catchup=True, default_args = default_dag_args) as dag_python:
    task_0 = PythonOperator(task_id = "get_market_data", python_callable = get_data, op_kwargs = {'tickers' : ["IBM", "AAPL"]})