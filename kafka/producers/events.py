import time
import json
from confluent_kafka import Producer
from statsbombpy import sb
import pandas as pd

# Configuración del productor de Kafka
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

# Leer los match_ids desde el archivo CSV
df_matches_id = pd.read_csv('matches_ids.csv')

# Convertir la columna 'match_id' a una lista de Python
matches_id = df_matches_id['match_id'].tolist()

# Iterar sobre los match_id y obtener los lineups
for match_id in matches_id:
    try:
        # Obtener el lineup para el match_id
        result = sb.events(match_id=match_id, split=True, flatten_attrs=False)["dribbles"]
        
        # Verificar si el resultado es un DataFrame
        if isinstance(result, pd.DataFrame):
            # Convertir el DataFrame en una lista de diccionarios
            result_dict = result.to_dict(orient='records')
        else:
            result_dict = result  # Si no es un DataFrame, se usa directamente el resultado

        # Convertir el resultado a JSON
        message = json.dumps(result_dict, default=str)  # Usar default=str para manejar tipos no serializables
        
        # Enviar el mensaje a Kafka
        producer.produce('Events', key=f'{match_id}', value=message, callback=delivery_report)
        producer.flush()  # Asegurar que el mensaje se envíe antes de continuar
        print(f"\nMensaje enviado para match_id={match_id}")
        print(result)
        
    except Exception as e:
        print(f"Error procesando match_id={match_id}: {e}")
    finally:
        # Agregar un retraso de 1 segundo entre las llamadas
        time.sleep(1)
