import pandas as pd
import numpy as np
import os
import datetime
import argparse


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='arguments')
    parser.add_argument('data_folder', type=str, help='folder to save data')
    parser.add_argument('ticker_name', type=str, default='BTC-USD',
                        help='ticker name to collect data')
    parser.add_argument('window_size', type=int, help='folder to save data')
    args = parser.parse_args()

    ticker_name = args.ticker_name
    data_path = args.data_folder
    window_size = args.window_size
    averages_dir = os.path.join(data_path, ticker_name, "average")
    print(averages_dir)
    all_df = pd.DataFrame()
    
    for date in os.listdir(averages_dir):
        date_avg_dir = os.path.join(averages_dir, date)
        for h in os.listdir(date_avg_dir):
            hour_avg = pd.read_csv(os.path.join(date_avg_dir, h))
            hour_avg['time'] = [datetime.datetime.strptime(f"{str(date)} {h.split('.')[0]}", '%Y-%m-%d %H')]
            hour_avg.set_index('time', inplace=True, drop=True)
            all_df = all_df.append(hour_avg)
    all_df = all_df.drop("Unnamed: 0", axis=1)
    all_df = all_df.sort_index().reset_index()
    sma = all_df.iloc[:, 1:].rolling(window=window_size).mean()
    sma['time'] = all_df['time']
    
    moving_averages_dir  = averages_dir.replace('average', 'moving_averages')
    os.makedirs(moving_averages_dir, exist_ok=True)
    for i, row in sma.iterrows():
        if not pd.isna(row['Low_mean']):
            sma_date_dir = os.path.join(moving_averages_dir,str(row['time'].date()))
            os.makedirs(sma_date_dir, exist_ok=True)
            out_csv = os.path.join(moving_averages_dir, 
                                   str(row['time'].date()),
                                   f'{window_size}SMA_'+str(row['time'].hour) + '.csv')
            print(out_csv)
            pd.DataFrame({f'Low_mean_{window_size}_sma': [row['Low_mean']],
                            f'High_mean_{window_size}_sma': [row['High_mean']],
                            'time': [row['time']]}).to_csv(out_csv, index=False)
