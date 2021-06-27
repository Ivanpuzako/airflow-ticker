import pandas as pd
import os
from dateutil import tz
import datetime
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

def save_average(path, save_to):
    df = pd.read_csv(path)
    low_mean = df['Low'].mean()
    high_mean = df['High'].mean()
    ret = pd.DataFrame({
        "Low_mean": low_mean,
        "High_mean": high_mean}, index=[0]
        )
    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    ret.to_csv(save_to)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='arguments')
    parser.add_argument('data_folder', type=str, help='folder to save data')
    parser.add_argument('ticker_name', type=str)
    args = parser.parse_args()
    data_folder = args.data_folder
    ticker = args.ticker_name
    
    time = os.environ.get("EXECUTION_TIME")
    time = dateutil.parser.parse(time)
    time = to_local_timezone(time)
    
    date = str(time.date())
    hour = str(time.hour)
    original_hour_file = os.path.join(data_folder, ticker, 'original', date, hour + '.csv')
    average_hour_file = original_hour_file.replace('/original/', '/average/')
    save_average(original_hour_file, average_hour_file)       
            