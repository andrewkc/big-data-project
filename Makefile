# carpetas principales
KAFKA_DIR=kafka
SPARK_DIR=spark

# correr make <comando>
up:
	@echo "Levantando servicios de Kafka y Spark..."
	docker-compose -f $(KAFKA_DIR)/docker-compose.yml up -d
	docker-compose -f $(SPARK_DIR)/docker-compose.yml up -d

down:
	@echo "Deteniendo servicios de Kafka y Spark..."
	docker-compose -f $(KAFKA_DIR)/docker-compose.yml down
	docker-compose -f $(SPARK_DIR)/docker-compose.yml down

logs:
	@echo "Mostrando logs de Kafka y Spark..."
	docker-compose -f $(KAFKA_DIR)/docker-compose.yml logs
	docker-compose -f $(SPARK_DIR)/docker-compose.yml logs

kafka-up:
	@echo "Levantando servicios de Kafka..."
	docker-compose -f $(KAFKA_DIR)/docker-compose.yml up -d

spark-up:
	@echo "Levantando servicios de Spark..."
	docker-compose -f $(SPARK_DIR)/docker-compose.yml up -d

kafka-down:
	@echo "Deteniendo servicios de Kafka..."
	docker-compose -f $(KAFKA_DIR)/docker-compose.yml down

spark-down:
	@echo "Deteniendo servicios de Spark..."
	docker-compose -f $(SPARK_DIR)/docker-compose.yml down

kafka-logs:
	@echo "Mostrando logs de Kafka..."
	docker-compose -f $(KAFKA_DIR)/docker-compose.yml logs

spark-logs:
	@echo "Mostrando logs de Spark..."
	docker-compose -f $(SPARK_DIR)/docker-compose.yml logs

clean:
	@echo "Eliminando contenedores, volúmenes y redes..."
	docker-compose -f $(KAFKA_DIR)/docker-compose.yml down --volumes --remove-orphans
	docker-compose -f $(SPARK_DIR)/docker-compose.yml down --volumes --remove-orphans
