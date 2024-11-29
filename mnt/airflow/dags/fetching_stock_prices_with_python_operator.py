import requests

from datetime import datetime

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
from airflow.operators.python import PythonOperator

from include.stock_market.tasks import _get_stock_prices

SYMBOL = 'AAPL'

@dag(
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['fetching_stock_prices_with_python_operator'],
)
def fetching_stock_prices_with_python_operator():
    
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
      
    # tylko dekoratory musza byc wywlowane w DAGU. dlatego nie ma wywolania get_stock_prices a jest is_api_available
    is_api_available() >> get_stock_prices
    

fetching_stock_prices_with_python_operator()


# tests --> airflow tasks test fetching_stock_prices_with_python_operator is_api_available 2023-01-01
