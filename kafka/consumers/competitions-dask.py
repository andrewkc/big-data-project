from confluent_kafka import Consumer, KafkaException
import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client
import json
import boto3
from botocore.exceptions import ClientError

def process_data(df):
    """
    Data processing function. You can add more transformations as needed.
    This example counts the competitions by season and filters the international competitions.
    """
    # Dask aggregation example
    competition_count = df.groupby('season_name').size().compute()  # Count competitions by season

    # Filter international competitions
    international_competitions = df[df['competition_international'] == True].compute()

    return competition_count, international_competitions

def consume_messages():
    # Consumer configuration
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    # Create Dask client
    client = Client()  # Start a Dask client

    # Create a consumer instance
    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe(['Competitions'])

    # Create DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
    table = dynamodb.Table('competitions') 

    print("Waiting for messages on the 'Competitions' topic...")
    try:
        while True:
            msg = consumer.poll(timeout=1.5)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            # Process message
            key = msg.key().decode('utf-8') if msg.key() else None
            value = msg.value().decode('utf-8')
            print(f"\nReceived message with key: {key}")

            # Convert the 'value' message (JSON) into a dictionary
            try:
                data_dict = json.loads(value)  # Convert JSON message to a dictionary
                print(data_dict)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {value}")
                continue

            # Create a Pandas DataFrame and convert it to a Dask DataFrame (if needed)
            data = pd.DataFrame([data_dict])  # Convert dictionary to a DataFrame
            df = dd.from_pandas(data, npartitions=1)  # Load as a Dask DataFrame

            # Process the data
            competition_count, international_competitions = process_data(df)

            # Add processed results to the dictionary
            data_dict['competition_count_by_season'] = competition_count.to_dict()  # Aggregation result
            data_dict['international_competitions'] = international_competitions.to_dict(orient='records')  # Filtered international competitions

            # Save the dictionary with processed data to DynamoDB
            try:
                response = table.put_item(
                    Item={
                        'competition_id': data_dict.get('competition_id'), 
                        'season_id': data_dict.get('season_id'), 
                        'data': data_dict,
                        'competition_count_by_season': data_dict.get('competition_count_by_season'),  # Aggregation result
                        'international_competitions': data_dict.get('international_competitions')  # Filtered data
                    }
                )
                print(f"Data saved to DynamoDB: {response}")
            except ClientError as e:
                print(f"Error saving to DynamoDB: {e.response['Error']['Message']}")

    except KeyboardInterrupt:
        print("\nClosing consumer...")
    finally:
        consumer.close()
        client.close()  # Close the Dask client

# Call the function to start the consumer
if __name__ == '__main__':
    consume_messages()
