import json
from confluent_kafka import Consumer, KafkaException, KafkaError

# Configuración del consumidor de Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'group.id': 'my-consumer-group',        # ID del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Empezar desde el primer mensaje si no hay offset almacenado
}

# Crear una instancia del consumidor
consumer = Consumer(conf)

# Función para manejar los mensajes consumidos
def handle_message(msg):
    try:
        # Decodificar el mensaje en formato JSON
        message_value = msg.value().decode('utf-8')  # Los mensajes se envían como bytes
        message_json = json.loads(message_value)  # Convertirlo en un objeto JSON

        # Aquí puedes procesar el mensaje como quieras. Ejemplo:
        print(f"Mensaje recibido para match_id={msg.key().decode('utf-8')}:")
        print(message_json)
        
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")

# Suscribirse al tema 'Lineups'
consumer.subscribe(['Lineups'])

# Loop principal para consumir los mensajes
try:
    while True:
        # Leer un mensaje desde Kafka
        msg = consumer.poll(timeout=1.0)  # Timeout en segundos, ajusta según tu necesidad

        # Si se obtiene un mensaje
        if msg is None:
            continue  # No hay mensaje disponible, continuar esperando
        elif msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Esto significa que hemos llegado al final de la partición
                print(f"Final de partición {msg.partition} alcanzado")
            else:
                raise KafkaException(msg.error())
        else:
            # Procesar el mensaje
            handle_message(msg)

except KeyboardInterrupt:
    print("Consumo interrumpido por el usuario")

finally:
    # Cerrar el consumidor
    consumer.close()
