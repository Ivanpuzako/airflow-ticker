Airflow for stock tracking
---

This repo uses [airflow tutorial](https://github.com/tuanavu/airflow-tutorial) for running airflow and contains a DAG for tracking some ticker

## Description

The DAG will hourly:

1) Get data for a ticker (ticker is a company name at stock market) using yfinance library and save df locally at: 
   `data/{TICKER_NAME}/original/{DATE}/{HOUR}.csv`

 
2) Calculate the mean price value (mean of the 'High' and 'Low' columns from the output of the previous step) and save locally at: 
   `data/{TICKER_NAME}/average/{DATE}/{HOUR}.csv`

 
3) Calculate 5 SMA and 20 SMA of the mean price (SMA-simple moving average). 5MA - is just the mean of the previous 5 values. Save the dataframe at: 
`data/{TICKER_NAME}/moving_averages/{DATE}/5SMA_{HOUR}.csv`

 
4) Calculate 20 SMA of the mean price. 20MA - is just the mean of the previous 20 values. Save the dataframe at: 
   `data/{TICKER_NAME}/moving_averages/{DATE}/20SMA_{HOUR}.csv`

 

5) Create a daily TS plot with the mean, 5SMA and 20SMA lines and save it at: 
   `data/{TICKER_NAME}/plots/{DATE}/ts_plot.png`

 

Thus, steps of DAG|Pipeline should be executed in given order: step1 > step2 > [step_3, step_4] > step_5

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

- Clone this repo
- Install the prerequisites
- Run the service
- Check http://localhost:8080
- Done! :tada:

### Prerequisites

- Install [Docker](https://www.docker.com/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)
- Following the Airflow release from [Python Package Index](https://pypi.python.org/pypi/apache-airflow)

### Usage

Select the ticker name for running pipeline in file
`examples/intro-example/dags/finance.py` field `ticker_name`

Run the web service with docker

```
docker-compose up

# Build the image
# docker-compose up -d --build
```

To stop srvice run

`docker-compose down`

Check http://localhost:8080/