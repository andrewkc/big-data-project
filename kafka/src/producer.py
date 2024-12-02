from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
from mplsoccer import VerticalPitch,Pitch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns

from confluent_kafka import Producer
import json


# Obtener los partidos de Euro 2024
matches = sb.matches(competition_id=55, season_id=282)

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

# Convertir los datos de los partidos a un formato adecuado para enviar
for match in matches.to_dict(orient='records'):
    # Enviar el mensaje al tópico 'statsbomb_topic'
    try:
        producer.produce(
            topic='statsbomb_topic', 
            value=json.dumps(match),  # Serializar cada partido a JSON
            callback=delivery_report
        )
        # Forzar el envío del mensaje
        producer.flush()
    except Exception as e:
        print(f"Error al producir mensaje: {e}")


print("Datos de los partidos enviados a Kafka")



