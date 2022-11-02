import sys
import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Get the second argument passed to spark-submit (the first is the python app)
data = sys.argv[1]
postgres_db = sys.argv[2]
postgres_user = sys.argv[3]
postgres_pwd = sys.argv[4]

# Read file
df = spark.read.format("csv").option("header", True).load(data)
df.show(truncate=False)

(
    df.write
    .format("jdbc")
    .option("url", postgres_db")
    .option("dbtable", "public.netflix")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)