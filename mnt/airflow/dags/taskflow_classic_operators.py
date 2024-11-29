from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def _task_a():
    print("Task A")
    return 42


def _task_b(ti=None):
    print("Task B")
    print(ti.xcom_pull(task_ids="task_a"))


with DAG(
    dag_id="taskflow_classic_operators",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["taskflow_classic_operators"],
):
    task_a = PythonOperator(task_id="task_a", python_callable=_task_a)

    task_b = PythonOperator(task_id="task_b", python_callable=_task_b)
