from confluent_kafka import Consumer, KafkaException

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'group.id': 'my-consumer-group',        # ID del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Comenzar desde el inicio de los mensajes
}

# Crear una instancia del consumidor
consumer = Consumer(conf)

# Suscribirse al topic
consumer.subscribe(['Competitions'])

# Leer mensajes del topic
try:
    print("Esperando mensajes en el topic 'Competitions'...")
    while True:
        # Intentar obtener un mensaje
        msg = consumer.poll(timeout=1.5)  # Tiempo de espera para recibir mensajes
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        # Procesar el mensaje
        key = msg.key().decode('utf-8') if msg.key() else None
        value = msg.value().decode('utf-8')
        print(f"\nRecibido mensaje con key: {key}, value: {value}")

except KeyboardInterrupt:
    print("\nCerrando consumidor...")
finally:
    # Cerrar el consumidor
    consumer.close()
