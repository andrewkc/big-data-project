import boto3
from botocore.exceptions import ClientError
import pandas as pd
import dask.dataframe as dd
import json
from confluent_kafka import Consumer, KafkaException
from dask.distributed import Client

def process_data(df):
    """
    Agregar las métricas de los eventos. Esto puede incluir métricas por hora, por usuario, entre otras.
    """
    # Verificar si la columna 'timestamp' existe
    #if 'timestamp' in df.columns:
    #    # Convertir la columna 'timestamp' a tipo datetime, si aún no lo está
    #    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    #
    #else:
    #    print("Error: la columna 'timestamp' no existe en los datos.")
    #    return None, None, None

    # Número total de eventos
    #total_events = df.shape[0].compute()

    # Frecuencia de eventos por hora
    #events_by_hour = df.groupby(df['timestamp'].dt.hour).size().compute()

    # Promedio de eventos por usuario
    #events_per_user = df.groupby('user_id').size().mean().compute()

    # Porcentaje de eventos fallidos
    #failed_events_percentage = df[df['status'] == 'failed'].shape[0].compute() / df.shape[0].compute() * 100

    #return total_events, events_by_hour, events_per_user, failed_events_percentage
    #return total_events #failed_events_percentage


def save_to_dynamodb(table_name, item):
    """
    Guarda los datos procesados en DynamoDB.
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)
    
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

            # Calcular las métricas adicionales
            #total_events = process_data(df)

            #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            #if total_events is None:
            #    continue
            #print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

            # Agregar las métricas al diccionario original
            #data_dict['total_events'] = total_events
            #data_dict['events_by_hour'] = events_by_hour.to_dict()
            #data_dict['events_per_user'] = events_per_user
            #data_dict['failed_events_percentage'] = failed_events_percentage
            
            data_dict = data_dict[0]
            # Guardar los datos originales con las métricas calculadas en DynamoDB
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
