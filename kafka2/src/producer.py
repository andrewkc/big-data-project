from confluent_kafka import Producer
import json

# Configuración del productor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
}

# Crear una instancia del productor
producer = Producer(conf)

# Función de callback para manejar la confirmación de entrega
def delivery_report(err, msg):
    if err is not None:
        print(f"Error al enviar mensaje: {err}")
    else:
        print(f"Mensaje enviado a {msg.topic()} [{msg.partition()}]")

# Datos para enviar
data = {
    'event_id': 1,
    'event_type': 'Pass',
    'player': 'Lionel Messi',
    'location': [50, 30],
    'pass_end_location': [70, 40]
}

# Enviar mensaje al tópico
try:
    producer.produce(
        topic='my-topic',
        value=json.dumps(data),
        callback=delivery_report
    )
    # Forzar envío del mensaje
    producer.flush()
except Exception as e:
    print(f"Error al producir mensajes: {e}")
