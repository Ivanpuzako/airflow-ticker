# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.incubator.apache.org/tutorial.html)
"""
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pytz
import datetime
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': 'Ivanpuzako@gmail.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

dag = DAG(
    'finance',
    default_args=default_args,
    description='btc dag',
    schedule_interval='@hourly',
)
ticker_name='BTC-USD'
output_folder = '/home/data/'

time = "{{ ts }}"
t1 = BashOperator(
    task_id="get_hour_info",
    bash_command= f'python /home/scripts/original.py {ticker_name} {output_folder} ',
    dag=dag,
    env = {'EXECUTION_TIME': time}
)

t2 = BashOperator(
    task_id="calc_hour_average",
    bash_command= f'python /home/scripts/average.py {output_folder} {ticker_name}',
    dag=dag,
    env = {'EXECUTION_TIME': time}
)

t3 = BashOperator(
    task_id="calc_5_sma",
    bash_command= f'python /home/scripts/sma.py {output_folder} {ticker_name} 5',
    dag=dag,
)
t4 = BashOperator(
    task_id="calc_20_sma",
    bash_command= f'python /home/scripts/sma.py {output_folder} {ticker_name} 20',
    dag=dag,
)

t5 = BashOperator(
    task_id="daily_plots",
    bash_command= f'python /home/scripts/plots.py {ticker_name} {output_folder}',
    dag=dag,
)

t1 >> t2 >> [t3, t4] >> t5