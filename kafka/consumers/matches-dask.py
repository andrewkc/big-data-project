from confluent_kafka import Consumer, KafkaException
import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client
import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

from decimal import Decimal, InvalidOperation
import math

def convert_to_decimal(obj):
    """Convierte todos los floats a Decimal en un diccionario o lista, y maneja NaN o Infinity."""
    if isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    elif isinstance(obj, float):
        # Verificar si el valor es NaN o Infinity
        if math.isinf(obj) or math.isnan(obj):
            return None  # O puedes elegir otro valor, como '0' o 'NaN'
        try:
            return Decimal(str(obj))  # Convertir a Decimal
        except InvalidOperation:
            return None  # En caso de error al convertir
    return obj

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
    consumer.subscribe(['Matches'])
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
    table = dynamodb.Table('matches') 

    print("Esperando mensajes en el topic 'Matches'...")
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

            # Convertir los valores flotantes a Decimal
            data_dict = convert_to_decimal(data_dict)

            # Crear un DataFrame de Pandas y convertirlo en Dask DataFrame
            data = pd.DataFrame([data_dict])  # Convierte el diccionario a un DataFrame
            df = dd.from_pandas(data, npartitions=1)  # Cargar como Dask DataFrame
            #print(df.compute())  # Procesar en memoria (ajusta según el flujo)

            try:
                response = table.put_item(
                    Item={
                        'match_id': key,
                        'data': data_dict
                    }
                )
                print(f"Data saved to DynamoDB: {response}")
            except ClientError as e:
                print(f"Error saving to DynamoDB: {e.response['Error']['Message']}")
            
    except KeyboardInterrupt:
        print("\nCerrando consumidor...")
    finally:
        consumer.close()
        client.close()  # Cerrar el cliente Dask

# Llamar a la función para iniciar el consumidor
if __name__ == '__main__':
    consume_messages()
