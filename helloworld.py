from airflow import DAG
from airflow.operators.bash_operator import BashOperator
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

# Download movies
download_movies = BashOperator(
    task_id='download_movies',
    bash_command='rm -rf /tmp/movies.rar && wget https://dorotheu-apacheairflow-objects.s3.us-east-2.amazonaws.com/movies.rar -P /tmp',
    dag=dag,
)

# Download ratings
download_ratings = BashOperator(
    task_id='download_ratings',
    bash_command='rm -rf /tmp/ratings.rar && wget https://dorotheu-apacheairflow-objects.s3.us-east-2.amazonaws.com/ratings.rar -P /tmp',
    dag=dag,
)

# Download tags
download_tags = BashOperator(
    task_id='download_tags',
    bash_command='rm -rf /tmp/tags.rar && wget https://dorotheu-apacheairflow-objects.s3.us-east-2.amazonaws.com/tags.rar -P /tmp',
    dag=dag,
)

# Unrar links
unrar_links = BashOperator(
    task_id='unrar_links',
    bash_command='unrar x -y /tmp/links.rar /tmp/.',
    dag=dag,
)

# Unrar movies
unrar_movies = BashOperator(
    task_id='unrar_movies',
    bash_command='unrar x -y /tmp/movies.rar /tmp/.',
    dag=dag,
)

# Unrar tags
unrar_ratings = BashOperator(
    task_id='unrar_ratings',
    bash_command='unrar x -y /tmp/ratings.rar /tmp/.',
    dag=dag,
)

# Unrar tags
unrar_tags = BashOperator(
    task_id='unrar_tags',
    bash_command='unrar x -y /tmp/tags.rar /tmp/.',
    dag=dag,
)

download_links   >> unrar_links
download_movies  >> unrar_movies
download_ratings >> unrar_ratings
download_tags    >> unrar_tags