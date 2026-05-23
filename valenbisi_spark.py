from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc
from pyspark.sql.types import *
import json

spark = SparkSession.builder \
    .appName("Valenbisi") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.24.0.8:29092") \
    .option("subscribe", "valenbisi") \
    .option("startingOffsets", """{"valenbisi":{"0":1}}""") \
    .load()

json_str = df.selectExpr("CAST(value AS STRING) as json").first()["json"]
data = json.loads(json_str)
stations = data["network"]["stations"]

schema = StructType([
    StructField("id", StringType()),
    StructField("name", StringType()),
    StructField("free_bikes", IntegerType()),
    StructField("empty_slots", IntegerType()),
    StructField("timestamp", StringType()),
])

stations_df = spark.createDataFrame(stations, schema=schema)

stations_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres_container:5432/postgres") \
    .option("dbtable", "valenbisi_stations") \
    .option("user", "postgres") \
    .option("password", "Welcome01") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

print("Datos guardados en PostgreSQL correctamente")