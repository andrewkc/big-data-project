from confluent_kafka import Consumer, KafkaException
import json

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'group.id': 'my-consumer-group',        # ID del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el inicio si no hay offset
}

# Crear una instancia del consumidor
consumer = Consumer(conf)

# Suscribirse al tópico
consumer.subscribe(['my-topic'])

# Leer mensajes del tópico
try:
    print("Esperando mensajes...")
    while True:
        msg = consumer.poll(timeout=1.0)  # Tiempo de espera para recibir mensajes
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        # Procesar mensaje recibido
        message_value = json.loads(msg.value().decode('utf-8'))
        print(f"Mensaje recibido: {message_value}")

except KeyboardInterrupt:
    print("Cerrando consumidor...")
finally:
    consumer.close()
