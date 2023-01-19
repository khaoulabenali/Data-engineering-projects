
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from twitter_etl import crawl_tweets

default_args={"owner":"airflow",
                "retries":1,
                "retry_delay": timedelta(minutes=5),
                "start_date":datetime(2022,11,3)}

dag = DAG(dag_id="twitter_dag",
    default_args=default_args,
    )

run_etl = PythonOperator(
        task_id="complete_twitter_etl",
        python_callable=crawl_tweets,
        dag=dag
        )

run_etl