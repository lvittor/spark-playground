# Spark Playgorund
A very simple demonstration of how to use SparkSQL to transform data from a CSV to a PostgreSQL table.

## Build the image

```shell
docker build --rm --force-rm -t docker-airflow-spark:latest .
```

## Start containers

```shell
docker-compose up
```

### Go to the services web UI

#### Airflow

http://localhost:8282

Go to Connections > spark_default > Host (spark://spark), Port (7077)

#### Spark

http://localhost:8181

#### Postgres 

Testing database: test

Airflow database: airflow
