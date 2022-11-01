import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Create spark session
spark = (SparkSession
    .builder
    .getOrCreate()
)

####################################
# Parameters
####################################
postgres_db = sys.argv[1]
postgres_user = sys.argv[2]
postgres_pwd = sys.argv[3]

####################################
# Read Postgres
####################################
print("######################################")
print("READING POSTGRES TABLES")
print("######################################")

df = spark.read.format("jdbc").option("url", postgres_db).option("dbtable", "public.playlist").option("user", postgres_user).option("password", postgres_pwd).load()

df.printSchema()
df.select("name").show(20)

# print("######################################")
# print("EXECUTING QUERY AND SAVING RESULTS")
# print("######################################")
# # Save result to a CSV file
# df_result.coalesce(1).write.format("csv").mode("overwrite").save("/usr/local/spark/resources/data/output_postgres", header=True)

