from confluent_kafka import Producer
from statsbombpy import sb
import time
import json

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

# Obtener el DataFrame de competiciones
competitions = sb.competitions()

# Crear la lista de tuplas (competition_id, season_id)
competition_season_tuples = list(competitions[['competition_id', 'season_id']].itertuples(index=False, name=None))

# Iterar sobre las tuplas y llamar a la función matches, publicando en Kafka
for competition_id, season_id in competition_season_tuples:
    try:
        result = sb.matches(competition_id, season_id)  # Llama a la función con la tupla
        
        # Convertir el DataFrame a un diccionario o lista antes de serializarlo
        # Por ejemplo, si el resultado es un DataFrame, puedes convertirlo a una lista de diccionarios:
        result_dict = result.to_dict(orient='records')  # Convierte el DataFrame a una lista de diccionarios
        
        # Convertir el resultado a JSON
        message = json.dumps(result_dict)
        
        # Enviar el mensaje a Kafka
        producer.produce('Matches', key=f'{competition_id}-{season_id}', value=message, callback=delivery_report)
        producer.flush()  # Asegurar que el mensaje se envíe antes de continuar
        print(f"\nMensaje enviado para competition_id={competition_id}, season_id={season_id}")
        print(result)
    except Exception as e:
        print(f"Error procesando competition_id={competition_id}, season_id={season_id}: {e}")
    finally:
        # Agregar un retraso de 1 segundo entre las llamadas
        time.sleep(1)
