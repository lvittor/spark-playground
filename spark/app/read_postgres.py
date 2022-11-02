import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Create spark session
spark = SparkSession.builder.getOrCreate()

postgres_db = sys.argv[1]
postgres_user = sys.argv[2]
postgres_pwd = sys.argv[3]

df = ( 
    spark.read
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.netflix")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .load()
)

df.printSchema()
