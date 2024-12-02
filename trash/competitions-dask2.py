from confluent_kafka import Consumer, KafkaException
import dask.dataframe as dd
import pandas as pd  # Importa pandas
from dask.distributed import Client
import json
import boto3
from botocore.exceptions import ClientError

def consume_messages():
    # Configuración del consumidor
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    # Crear cliente Dask
    client = Client()  # Inicia un cliente Dask

    # Crear una instancia del consumidor
    consumer = Consumer(conf)

    # Suscribirse al topic
    consumer.subscribe(['Competitions'])

    # Crear cliente DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Cambia la región según sea necesario
    table = dynamodb.Table('competitions')  # Nombre de tu tabla en DynamoDB

    print("Esperando mensajes en el topic 'Competitions'...")
    try:
        while True:
            msg = consumer.poll(timeout=1.5)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            # Procesar mensaje
            key = msg.key().decode('utf-8') if msg.key() else None
            value = msg.value().decode('utf-8')
            print(f"\nRecibido mensaje con key: {key}")

            # Convertir el mensaje 'value' (JSON) en un diccionario
            try:
                data_dict = json.loads(value)  # Convierte el mensaje JSON a un diccionario
                print(data_dict)
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON: {value}")
                continue

            # Guardar el diccionario en DynamoDB
            try:
                # Suponiendo que 'id' es una clave única en DynamoDB. Modifica según tu modelo de datos.
                response = table.put_item(
                    Item={
                        'competition_id': data_dict.get('competition_id'),  # Asegúrate de que el campo 'id' exista en tu JSON
                        'season_id': data_dict.get('season_id'),  # Asegúrate de que el campo 'id' exista en tu JSON
                        'data': data_dict           # Almacena todo el diccionario en el campo 'data'
                    }
                )
                print(f"Datos guardados en DynamoDB: {response}")
            except ClientError as e:
                print(f"Error al guardar en DynamoDB: {e.response['Error']['Message']}")

            # Crear un DataFrame de Pandas y convertirlo en Dask DataFrame (si es necesario)
            data = pd.DataFrame([data_dict])  # Convierte el diccionario a un DataFrame
            df = dd.from_pandas(data, npartitions=1)  # Cargar como Dask DataFrame
            #print(df.compute())  # Procesar en memoria (ajusta según el flujo)
            

    except KeyboardInterrupt:
        print("\nCerrando consumidor...")
    finally:
        consumer.close()
        client.close()  # Cerrar el cliente Dask

# Llamar a la función para iniciar el consumidor
if __name__ == '__main__':
    consume_messages()
