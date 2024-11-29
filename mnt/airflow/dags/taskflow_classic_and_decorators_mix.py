from datetime import datetime
from airflow.decorators import dag, task
from airflow.decorators.python import PythonOperator


def _task_a():
    print("Task A")
    return 42


@dag(
    dag_id="taskflow_classic_and_decorators_mix",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["taskflow_classic_and_decorators_mix"],
)
def taskflow():

    task_a = PythonOperator(task_id="task_a", python_callable=_task_a)

    @task
    def task_b(value):
        print("Task B")
        print(value)

    task_b(task_a.output) #it's equivalent of xcom_pull(task_ids="task_a")


taskflow()
