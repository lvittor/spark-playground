# Spark Playgorund


## Build the image

```shell
make build AIRFLOW_VERSION=1.10.14 SPARK_VERSION= HADDOP_VERSION=
```

## Start containers

```shell
make up
```

### Go to the services web UI

#### Airflow

http://localhost:8282

Go to Connections > spark_default > Host (spark://spark), Port (7077)

#### Spark

http://localhost:8181

#### Postgres 

Testing database:

Airflow database: 
