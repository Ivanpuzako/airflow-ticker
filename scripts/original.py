import pandas as pd
import os
import numpy as np
import yfinance as yf
import datetime
import pytz
from dateutil import tz
import dateutil
import argparse
#1) Get data for a ticker (ticker is a company name at stock market) using yfinance library 
# and save df locally at: {HW_PATH}/data/{TICKER_NAME}/original/{DATE}/{HOUR}.csv

def to_local_timezone(t):
    from_zone = tz.tzutc()
    to_zone = tz.gettz('Europe/Moscow')
    utc = t.replace(tzinfo=from_zone)
    result = utc.astimezone(to_zone)
    return result

def ticker_info_last_hour(ticker_name, end_time):
    #end_time = datetime.datetime.strptime(f"{date} {hour}", '%Y-%m-%d %H')
    start_time = end_time - datetime.timedelta(hours=1)
    
    ticker = yf.Ticker(ticker_name)
    hour_history = ticker.history(start=start_time, end=end_time, interval='5m')
    hour_history.index = hour_history.index.tz_convert('Europe/Moscow')
    return hour_history, end_time

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='arguments')
    parser.add_argument('ticker_name', type=str, default='BTC-USD',
                        help='ticker name to collect data')
    parser.add_argument('data_folder', type=str, help='folder to save data')
    args = parser.parse_args()

    ticker_name = args.ticker_name
    data_path = args.data_folder

    end_time = os.environ.get("EXECUTION_TIME")
    end_time = dateutil.parser.parse(end_time)
    history, end_time= ticker_info_last_hour(ticker_name, end_time)
    end_time = to_local_timezone(end_time)
    local_date, local_hour = str(end_time.date()), str(end_time.hour)

    result_path = os.path.join(data_path, ticker_name, 'original', local_date)
    os.makedirs(result_path, exist_ok=True)
    history.to_csv(os.path.join(result_path, local_hour+'.csv'))