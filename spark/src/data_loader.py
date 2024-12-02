from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql import functions as F
from importlib import import_module


def create_spark_session():
    return SparkSession.builder \
        .appName("StatsBombKafkaStream") \
        .getOrCreate()

def load_data_from_kafka(spark):
    try:
        raw_stream = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "statsbomb_topic") \
            .load()

        # Verifica el esquema de los datos
        raw_stream.printSchema()

        # Convierte el valor de Kafka de byte a string
        processed_stream = raw_stream.selectExpr("CAST(value AS STRING)")
        return processed_stream
    except Exception as e:
        print(f"Error en la carga de datos desde Kafka: {e}")
        raise


if __name__ == "__main__":
    spark = create_spark_session()
    df = load_data_from_kafka(spark)
    
    # Mostrar los datos en consola para verificar
    query = df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
    
    query.awaitTermination()