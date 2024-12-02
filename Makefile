ifeq (,$(wildcard .env))
    $(error No se encontró el archivo .env. Por favor, crea uno con las variables necesarias.)
endif
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: all build deploy clean start-minikube stop-minikube dashboard

# Construir Imágenes Docker
build:
	@echo "Construyendo imágenes Docker..."
	docker build -t $(DOCKER_REGISTRY)/airflow:latest $(AIRFLOW_DIR)
	docker build -t $(DOCKER_REGISTRY)/streamlit:latest $(STREAMLIT_DIR)
	@echo "Imágenes Docker construidas."

# Iniciar Minikube
start-minikube:
	@echo "Iniciando Minikube..."
	minikube start --profile=$(MINIKUBE_PROFILE)
	@echo "Minikube iniciado con el perfil $(MINIKUBE_PROFILE)."

# Desplegar Servicios en Kubernetes
deploy: build
	@echo "Creando namespace y aplicando configuraciones generales..."
	kubectl apply -f $(K8S_DIR)/namespace.yaml
	@echo "Desplegando Kafka..."
	kubectl apply -f $(KAFKA_DIR)/kafka-deployment.yaml
	kubectl apply -f $(KAFKA_DIR)/kafka-service.yaml
	@echo "Desplegando Streamlit..."
	kubectl apply -f $(STREAMLIT_DIR)/streamlit-deployment.yaml
	kubectl apply -f $(STREAMLIT_DIR)/streamlit-service.yaml
	@echo "Desplegando MongoDB..."
	kubectl apply -f $(MONGODB_DIR)/mongodb-deployment.yaml
	kubectl apply -f $(MONGODB_DIR)/mongodb-service.yaml
	@echo "Aplicando Ingress..."
	kubectl apply -f $(K8S_DIR)/ingress.yaml
	@echo "Despliegue completado."

# Detener Minikube
stop-minikube:
	@echo "Deteniendo Minikube..."
	minikube stop --profile=$(MINIKUBE_PROFILE)
	@echo "Minikube detenido."

# Limpiar Recursos
clean:
	@echo "Eliminando recursos en Kubernetes..."
	kubectl delete namespace $(NAMESPACE)
	@echo "Recursos eliminados."

# Abrir el Dashboard de Minikube
dashboard:
	@echo "Abriendo Dashboard de Minikube..."
	minikube dashboard --profile=$(MINIKUBE_PROFILE)
