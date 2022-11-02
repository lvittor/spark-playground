from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

spark_master = "spark://spark:7077"
spark_app_name = "Spark Test"
postgres_driver_jar = "/usr/local/spark/resources/jars/postgresql-42.4.0.jar"

data = "/usr/local/spark/resources/data/netflix.csv"
postgres_db = "jdbc:postgresql://postgres/test"
postgres_user = "test"
postgres_pwd = "postgres"

now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="spark-test",
    description="This DAG runs a simple Pyspark app.",
    default_args=default_args,
    schedule_interval=timedelta(1),
)

start = DummyOperator(task_id="start", dag=dag)

spark_job = SparkSubmitOperator(
    task_id="spark_job",
    application="/usr/local/spark/app/netflix.py",
    name=spark_app_name,
    conn_id="spark_default",
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[data, postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag,
)

spark_read = SparkSubmitOperator(
    task_id="spark_read",
    application="/usr/local/spark/app/read_postgres.py",
    name=spark_app_name,
    conn_id="spark_default",
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag,
)

end = DummyOperator(task_id="end", dag=dag)

start >> spark_job >> spark_read >> end
