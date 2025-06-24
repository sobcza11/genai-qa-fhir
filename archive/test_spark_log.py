from pyspark.sql import SparkSession

print("🚀 Launching Spark...")
spark = SparkSession.builder.appName("TestSpark").getOrCreate()
print("✅ Spark initialized")

df = spark.createDataFrame([(1, "hello"), (2, "world")], ["id", "value"])
df.show()
