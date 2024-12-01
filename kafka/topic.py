from confluent_kafka.admin import AdminClient, NewTopic

def run():
    try:
        kafka_config = {
            'bootstrap.servers': 'localhost:9092',
            'client.id': 'myapp'
        }

        admin = AdminClient(kafka_config)
        print("Connecting...")

        # Create the topic
        topic_list = [NewTopic(topic="Competitions", num_partitions=2, replication_factor=1),
                      NewTopic(topic="Matches", num_partitions=2, replication_factor=1),
                      NewTopic(topic="Lineups", num_partitions=2, replication_factor=1),
                      NewTopic(topic="Events", num_partitions=2, replication_factor=1)]
        result = admin.create_topics(topic_list)

        for topic, future in result.items():
            try:
                future.result()
                print(f"Topic {topic} created successfully!")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")

    except Exception as ex:
        print(f"Something bad happened: {ex}")
    finally:
        print("Done")

if __name__ == "__main__":
    run()
