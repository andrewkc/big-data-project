# big-data-project

### Entorno virtual

#### Windows

```bash
.\venv\Scripts\activate
python -m venv venv
```
#### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Instalar dependencias

```bash
pip install -r requirements.txt
```



### Docker para Kafka

```bash
docker network create kafka-net
```

```bash
docker run --name zookeeper --network kafka-net -p 2181:2181 -d zookeeper
```

```bash
docker run -p 9092:9092 --name kafka --network kafka-net -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -d confluentinc/cp-kafka 
```




