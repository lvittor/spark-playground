import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime, col, to_timestamp
from pyspark.sql.types import DoubleType

# Create spark session
spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("WARN")


####################################
# Parameters
####################################
dataset = sys.argv[1]
postgres_db = sys.argv[2]
postgres_user = sys.argv[3]
postgres_pwd = sys.argv[4]

####################################
# Read CSV Data
####################################
print("######################################")
print("READING CSV FILES")
print("######################################")

df = spark.read.json(dataset, multiLine=True)

print("######################################")
print("LOADING POSTGRES TABLES")
print("######################################")

df.write.format("jdbc").option("url", postgres_db).option("dbtable", "public.playlist").option("user", postgres_user).option("password", postgres_pwd).mode("overwrite").save()