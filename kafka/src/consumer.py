from confluent_kafka import Consumer, KafkaException
import json

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'group.id': 'my-consumer-group',        # ID del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el inicio si no hay offset
}

consumer = Consumer(conf)

consumer.subscribe(['statsbomb_topic'])

# Leer mensajes del tópico
try:
    print("Esperando mensajes...")
    while True:
        msg = consumer.poll(timeout=1.0)  # Tiempo de espera para recibir mensajes
        if msg is None:
            continue  # No se recibió mensaje
        if msg.error():
            raise KafkaException(msg.error())
        
        # Si el mensaje está disponible, procesarlo
        try:
            # Deserializar el mensaje JSON recibido
            event_data = json.loads(msg.value().decode('utf-8'))
            print("Evento recibido:", event_data)  # Imprimir el evento

        except Exception as e:
            print(f"Error al procesar el mensaje: {e}")
    
except KeyboardInterrupt:
    print("Proceso interrumpido por el usuario")
finally:
    # Cerrar el consumidor cuando termine
    consumer.close()
