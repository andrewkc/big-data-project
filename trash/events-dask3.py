import boto3
from botocore.exceptions import ClientError
import pandas as pd
import dask.dataframe as dd
import json
from confluent_kafka import Consumer, KafkaException
from dask.distributed import Client
from decimal import Decimal

def process_data(df):
    """
    Agregar las métricas de los eventos. Esto puede incluir métricas por hora, por usuario, entre otras.
    """
    # Aquí iría la lógica para calcular las métricas, si fuera necesario
    pass

def convert_to_decimal(item):
    """
    Convierte los valores de tipo float en el diccionario a Decimal para ser compatibles con DynamoDB.
    """
    if isinstance(item, dict):
        for key, value in item.items():
            item[key] = convert_to_decimal(value)  # Recursión para valores anidados
    elif isinstance(item, list):
        return [convert_to_decimal(i) for i in item]
    elif isinstance(item, float):
        return Decimal(str(item))  # Convertir float a Decimal
    return item

def save_to_dynamodb(table_name, item):
    """
    Guarda los datos procesados en DynamoDB.
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)

    # Convertir los floats a Decimal
    item = convert_to_decimal(item)
    
    try:
        response = table.put_item(Item=item)
        print(f"Data saved to DynamoDB: {response}")
    except ClientError as e:
        print(f"Error saving to DynamoDB: {e.response['Error']['Message']}")

def consume_messages():
    # Configuración del consumidor Kafka
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    # Crear cliente de Dask
    client = Client()

    # Crear una instancia del consumidor
    consumer = Consumer(conf)

    # Suscribirse al topic de Kafka
    consumer.subscribe(['Events'])

    print("Waiting for messages on the 'Events' topic...")
    try:
        while True:
            msg = consumer.poll(timeout=1.5)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            # Procesar mensaje
            value = msg.value().decode('utf-8')
            print(f"\nReceived message: {value}")

            # Convertir el mensaje JSON a un diccionario
            try:
                data_dict = json.loads(value)
                print(data_dict)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {value}")
                continue

            # Crear un DataFrame de Pandas y convertirlo a DataFrame de Dask
            data = pd.DataFrame([data_dict])
            df = dd.from_pandas(data, npartitions=1)

            # Calcular las métricas adicionales (si se desea implementar)
            # total_events = process_data(df)

            # Agregar las métricas al diccionario original (si las hay)
            # data_dict['total_events'] = total_events

            # Guardar los datos originales con las métricas calculadas en DynamoDB
            data_dict = data_dict[0]
            save_to_dynamodb('events', {
                'id': data_dict.get('id'),  # Usamos el ID del evento como clave primaria
                **data_dict,  # Desempaquetamos los datos originales y los agregamos a la tabla
            })

    except KeyboardInterrupt:
        print("\nClosing consumer...")
    finally:
        consumer.close()
        client.close()  # Cerrar el cliente de Dask

# Llamar a la función para iniciar el consumidor
if __name__ == '__main__':
    consume_messages()
