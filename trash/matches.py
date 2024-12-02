from confluent_kafka import Consumer, KafkaException, KafkaError
import json

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'group.id': 'my-consumer-group',  # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest',  # Comienza a leer desde el principio si no hay offset almacenado
}

# Crear una instancia del consumidor
consumer = Consumer(conf)

# Suscribirse al tópico
consumer.subscribe(['Matches'])

# Función para manejar los mensajes recibidos
def consume_message(msg):
    try:
        # Deserializar el mensaje
        result = json.loads(msg.value().decode('utf-8'))
        
        # Procesar el mensaje (en este caso, solo imprimirlo)
        print(f"\nMensaje recibido: {result}")
        
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

# Loop de consumo
try:
    while True:
        # Leer un mensaje
        msg = consumer.poll(timeout=1.5)  # timeout de 1 segundo para la poll
        
        if msg is None:
            # No hay mensajes disponibles, puedes hacer alguna acción aquí
            continue
        if msg.error():
            # Si hay algún error en el mensaje, lo manejamos
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"Fin de la partición alcanzado: {msg.partition()} @ offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Consumir el mensaje recibido
            consume_message(msg)
            consumer.commit(msg)  # Confirmar que el mensaje ha sido procesado

except KeyboardInterrupt:
    print("Consumo interrumpido por el usuario")

finally:
    # Cerrar el consumidor y liberar recursos
    consumer.close()
