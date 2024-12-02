# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime
# from kafka.src.producer import produce_competitions
# from spark.src.main import process_kafka_data

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2023, 1, 1),
#     'retries': 1
# }

# def start_producer():
#     produce_competitions()

# def start_processing():
#     process_kafka_data()

# with DAG(
#     'fetch_and_process',
#     default_args=default_args,
#     schedule_interval='@daily'
# ) as dag:
#     fetch_task = PythonOperator(
#         task_id='fetch_data',
#         python_callable=start_producer
#     )

#     process_task = PythonOperator(
#         task_id='process_data',
#         python_callable=start_processing
#     )

#     fetch_task >> process_task


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def fetch_data():
    print("Fetching data from API...")

def process_data():
    print("Processing data with Spark...")

with DAG(
    dag_id="fetch_and_process",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_data,
    )
    process_task = PythonOperator(
        task_id="process_data",
        python_callable=process_data,
    )

    fetch_task >> process_task
