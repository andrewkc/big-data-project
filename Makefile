ifeq (,$(wildcard .env))
    $(error No se encontró el archivo .env. Por favor, crea uno con las variables necesarias.)
endif
include .env
export $(shell sed 's/=.*//' .env)

# correr make <comando>
.PHONY: up down logs clean setup-venv install-requirements run-spark run-kafka create-network start-zookeeper start-kafka stop-zookeeper stop-kafka

up:
	@echo "Levantando servicios de Kafka y Spark..."
	docker-compose -f kafka/docker-compose.yml up -d
	docker-compose -f spark/docker-compose.yml up -d

down:
	@echo "Deteniendo servicios de Kafka y Spark..."
	docker-compose -f kafka/docker-compose.yml down
	docker-compose -f spark/docker-compose.yml down

logs:
	@echo "Mostrando logs de Kafka y Spark..."
	docker-compose -f kafka/docker-compose.yml logs
	docker-compose -f spark/docker-compose.yml logs

setup-venv:
	@echo "Configurando entorno virtual en $(VENV_DIR)..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Instalando dependencias..."
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS_FILE)

install-requirements: setup-venv
	@echo "Dependencias instaladas en el entorno virtual."

run-spark:
	@echo "Ejecutando Spark..."
	$(VENV_DIR)/bin/python spark/src/main.py

run-kafka:
	@echo "Ejecutando Kafka..."
	$(VENV_DIR)/bin/python kafka/src/main.py

clean:
	@echo "Limpiando servicios y entorno..."
	docker-compose -f kafka/docker-compose.yml down --volumes --remove-orphans
	docker-compose -f spark/docker-compose.yml down --volumes --remove-orphans
	rm -rf $(VENV_DIR)

create-network:
	@echo "Creando red Docker para Kafka..."
	docker network create $(NETWORK_NAME) || echo "La red $(NETWORK_NAME) ya existe."

start-zookeeper:
	@echo "Iniciando contenedor Zookeeper..."
	docker run --name $(ZOOKEEPER_CONTAINER) --network $(NETWORK_NAME) -p 2181:2181 -d zookeeper || echo "Zookeeper ya está corriendo."

start-kafka:
	@echo "Iniciando contenedor Kafka..."
	docker run -p 9092:9092 --name $(KAFKA_CONTAINER) --network $(NETWORK_NAME) \
		-e KAFKA_ZOOKEEPER_CONNECT=$(ZOOKEEPER_CONTAINER):2181 \
		-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
		-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
		-d $(KAFKA_IMAGE) || echo "Kafka ya está corriendo."

stop-zookeeper:
	@echo "Deteniendo contenedor Zookeeper..."
	docker stop $(ZOOKEEPER_CONTAINER) || echo "Zookeeper no está corriendo."
	docker rm $(ZOOKEEPER_CONTAINER) || echo "Zookeeper no existe."

stop-kafka:
	@echo "Deteniendo contenedor Kafka..."
	docker stop $(KAFKA_CONTAINER) || echo "Kafka no está corriendo."
	docker rm $(KAFKA_CONTAINER) || echo "Kafka no existe."
