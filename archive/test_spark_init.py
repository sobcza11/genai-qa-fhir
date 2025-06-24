from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.appName("TestInit").getOrCreate()

# Confirm working Spark context
print("✅ Spark session initialized:", spark.version)

# Create tiny dummy DataFrame
df = spark.createDataFrame([(1, "hello"), (2, "world")], ["id", "value"])
df.show()
