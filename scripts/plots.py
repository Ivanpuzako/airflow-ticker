import pandas as pd
import os
import datetime
import dateutil
from datetime import timedelta
import pytz
import argparse
import matplotlib.pyplot as plt

def get_sma_df(moving_averages_dir, sma_number):
    
    smas_df = pd.DataFrame()
    for date in os.listdir(moving_averages_dir):
        date_moving_avg_dir = os.path.join(moving_averages_dir, date)
        for sma in os.listdir(date_moving_avg_dir):
            if sma.startswith(f'{int(sma_number)}SMA'):
                hour_avg = pd.read_csv(os.path.join(date_moving_avg_dir, sma))
                hour_avg.set_index('time', inplace=True, drop=True)
                smas_df = smas_df.append(hour_avg)
    str_to_time = lambda x: dateutil.parser.parse(x)
    smas_df.index = smas_df.index.map(str_to_time)
    smas_df = smas_df.sort_index().reset_index()
    return smas_df

def create_date_plot(sma_5, sma_20, save_dir):
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sma_5['time'], sma_5['Low_mean_5_sma'], color='tab:orange', label='SMA_5 Low')
    ax.plot(sma_5['time'], sma_5['High_mean_5_sma'], color='tab:red', label='SMA_5 High')
    
    if sma_20 is not None:
        ax.plot(sma_20['time'], sma_20['Low_mean_20_sma'], color='tab:gray', label='SMA_20 Low')
        ax.plot(sma_20['time'], sma_20['High_mean_20_sma'], color='tab:blue', label='SMA_20 High')

    plt.xticks(rotation=90)
    ax.set_xlabel('Time')
    ax.set_ylabel('USD cost')
    ax.set_title('TS Plot')
    ax.grid(True)
    ax.legend(loc='upper left')
    ax.figure.savefig(os.path.join(save_dir, 'ts_plot.png'))
    return ax.figure

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='arguments')
    parser.add_argument('ticker_name', type=str, default='BTC-USD',
                        help='ticker name to collect data')
    parser.add_argument('data_folder', type=str, help='folder to save data')
    args = parser.parse_args()
    data_path = args.data_folder
    ticker_name = args.ticker_name
    moving_averages_dir = os.path.join(data_path, ticker_name, "moving_averages")
    smas_5 = get_sma_df(moving_averages_dir, 5)
    smas_20 = get_sma_df(moving_averages_dir, 20)

    plots_dir = os.path.join(data_path, ticker_name, 'plots')
    if len(smas_5):
        unique_dates = smas_5['time'].map(lambda x: x.date()).unique()
        for date in unique_dates:
            date_dir = os.path.join(plots_dir, str(date))
            os.makedirs(date_dir, exist_ok=True)
            smas_5_date = smas_5[smas_5['time'].map(lambda x: x.date() <= date)]
            smas_20_date = smas_20[smas_20['time'].map(lambda x: x.date() <= date)] if len(smas_20) else None
            figure = create_date_plot(smas_5_date, smas_20_date, date_dir)        