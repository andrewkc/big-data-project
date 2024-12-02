from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Inicializar la sesión de Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

# Configurar el consumidor de Kafka
kafka_bootstrap_servers = "localhost:9092"
topic_name = "Competitions"

# Leer desde Kafka usando Spark Structured Streaming
kafka_stream_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", topic_name) \
    .load()

# Convertir los valores de Kafka a cadenas de texto
kafka_stream_df = kafka_stream_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Realizar alguna operación con los datos (aquí solo estamos imprimiendo el contenido)
query = kafka_stream_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Esperar que la consulta termine
query.awaitTermination()
