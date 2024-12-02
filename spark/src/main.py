from data_loader import load_data_from_kafka
from data_processor import process_data
from db_writer import write_to_mongodb
from pyspark.sql import SparkSession

def main():
    # Crear sesión de Spark
    spark = SparkSession.builder \
        .appName("StatsBombKafkaStream") \
        .getOrCreate()

    # Cargar datos desde Kafka
    raw_stream = load_data_from_kafka(spark)

    # Procesar los datos
    processed_data = process_data(raw_stream)

    # Escribir los resultados en MongoDB o Neo4j
    write_to_mongodb(processed_data)

    # Iniciar el streaming (si es streaming en tiempo real)
    processed_data.writeStream \
        .format("console") \
        .outputMode("append") \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    main()
