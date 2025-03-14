import requests

from datetime import datetime

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
from airflow.operators.python import PythonOperator

from include.stock_market.tasks import (
    _get_stock_prices, _store_prices
)


SYMBOL = 'AAPL'

@dag(
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['storing_stock_prices_in_minio'],
)
def storing_stock_prices_in_minio():
    
    @task.sensor(poke_interval=30, timeout=300, mode='poke')
    def is_api_available() -> PokeReturnValue:
        api = BaseHook.get_connection('stock_api')
        url = f"{api.host}{api.extra_dejson['endpoint']}"
        response = requests.get(url, headers=api.extra_dejson['headers'])
        condition = response.json()['finance']['result'] is None
        return PokeReturnValue(is_done=condition, xcom_value=url)


    get_stock_prices = PythonOperator(
        task_id='get_stock_prices',
        python_callable=_get_stock_prices,
        op_kwargs={'url': '{{ task_instance.xcom_pull(task_ids="is_api_available") }}', 'symbol': SYMBOL}
        
    )
    
    store_prices = PythonOperator(
        task_id='store_prices',
        python_callable=_store_prices,
        op_kwargs={'stock': '{{ task_instance.xcom_pull(task_ids="get_stock_prices") }}'}
    )
      
    # tylko dekoratory musza byc wywlowane w DAGU. dlatego nie ma wywolania get_stock_prices a jest is_api_available
    is_api_available() >> get_stock_prices >> store_prices
    

storing_stock_prices_in_minio()


# tests --> airflow tasks test storing_stock_prices_in_minio is_api_available 2023-01-01
