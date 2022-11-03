from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.contrib.operators.spark_sql_operator import SparkSqlOperator
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
    dag_id="spark-analysis-queries",
    description="This DAG runs PySpark apps to analyze the data using several queries.",
    default_args=default_args,
    schedule_interval=timedelta(1),
)

start = DummyOperator(task_id="start", dag=dag)

load_csv = SparkSubmitOperator(
    task_id="load_csv",
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

count_movies_by_year = SparkSubmitOperator(
    task_id="count_movies_by_year",
    application="/usr/local/spark/app/queries/count_movies_by_year.py",
    name=spark_app_name,
    conn_id="spark_default",
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[data, postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag,
)


count_records_by_genre = SparkSubmitOperator(
    task_id="count_records_by_genre",
    application="/usr/local/spark/app/queries/count_records_by_genre.py",
    name=spark_app_name,
    conn_id="spark_default",
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[data, postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag,
)

end = DummyOperator(task_id="end", dag=dag, trigger_rule="all_done")

start >> load_csv >> [count_movies_by_year, count_records_by_genre] >> end
