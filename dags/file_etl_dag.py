from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Add scripts to path
sys.path.insert(0, '/opt/airflow/scripts')

from extract import extract_data
from transform import transform_data
from load import load_data

default_args = {
    'owner': 'team_project',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'file_etl_pipeline',
    default_args=default_args,
    description='Simple ETL: Read CSV -> Transform -> Write CSV',
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'project'],
)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

extract_task >> transform_task >> load_task