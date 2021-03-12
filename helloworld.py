from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "start_date": days_ago(0),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "youremail@host.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG(dag_id="helloworld", schedule_interval="@daily", default_args=default_args)

# Download links
download_links = BashOperator(
    task_id='download_links',
    bash_command='rm -rf /tmp/links.rar && wget https://dorotheu-apacheairflow-objects.s3.us-east-2.amazonaws.com/links.rar -P /tmp',
    dag=dag,
)

# Unrar links
unrar_links = BashOperator(
    task_id='unrar_links',
    bash_command='unrar x -y /tmp/links.rar /tmp/.',
    dag=dag,
)

def data_transform_exec():
    # Put your code here
    pass

data_transform = PythonOperator(
    task_id="data_transform",
    python_callable=data_transform_exec,
    dag=dag
)

download_links   >> unrar_links