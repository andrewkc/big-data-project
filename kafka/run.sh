pip install -r requirements.txt
docker network create kafka-net
docker run --name zookeeper --network kafka-net -p 2181:2181 -d zookeeper
docker run -p 9092:9092 \
  --name kafka \
  --network kafka-net \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -d confluentinc/cp-kafka

python topic.py