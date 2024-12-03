from confluent_kafka import Producer
from statsbombpy import sb
import time

# Configuración del productor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'client.id': 'my-producer'
}

# Crear una instancia del productor
producer = Producer(conf)

# Función de callback para manejar eventos de envío
def delivery_report(err, msg):
    if err is not None:
        print(f"Error en el envío del mensaje: {err}")
    else:
        print(f"\nMensaje enviado a {msg.topic()} [{msg.partition()}] @ {msg.offset()}")

# Obtener el dataframe de competencias
competitions = sb.competitions()

# Barajar las filas del dataframe
shuffled_competitions = competitions.sample(frac=1, random_state=42).reset_index(drop=True)

# Iterar sobre cada fila y enviarla como mensaje
for idx, row in shuffled_competitions.iterrows():
    # Convertir la fila a un string para enviarla como mensaje
    message = row.to_json()
    
    # Producir el mensaje a Kafka
    producer.produce('Competitions', key=f'key-{idx}', value=message, callback=delivery_report)
    producer.flush()  # Asegurar que el mensaje se envíe antes de continuar
    print(f"Mensaje enviado: {message}")
    time.sleep(1)  # Pausa opcional entre envíos
