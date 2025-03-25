from datetime import datetime, timedelta

from airflow.decorators import dag, task

from src.extract.extract import run_extraction

default_args = {
    "owner": "Abraham Ajibade",
    "depends_on_past": False,
    "start_date": datetime(2024, 8, 1),
    "email": ["abraham0ajibade@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
)
def tickit():
    @task(task_id="mongodb_to_s3")
    def mongodb_to_s3():
        """This task extracts batch data from a local mongodb location to a
        staging area in S3
        """
        run_extraction()

    # Set Task Flow
    mongodb_to_s3()


tickit()
