# ⚽ Big Data Project 📊

## 🚀 Introducción y justificación del problema a resolver
El proyecto tiene como objetivo analizar datos de fútbol provenientes de la [repo de StatsBomb](https://github.com/statsbomb/open-data.git). La información incluye eventos, alineaciones, partidos y competiciones, lo que permite realizar análisis avanzados sobre el rendimiento de equipos y jugadores. La implementación sigue una arquitectura de Big Data, permitiendo el procesamiento en tiempo real y la visualización de datos complejos.

---

## 📂 Descripción del dataset, origen y tamaño de data
El dataset proviene de la repo pública de [StatsBomb Open Data](https://github.com/statsbomb/open-data.git) y contiene:

- **⚽ Events**: Información detallada de los eventos durante los partidos.
- **🧑‍🤝‍🧑 Lineups**: Alineaciones de los equipos.
- **🏟️ Matches**: Datos generales de cada partido.
- **🔄 Three-sixty**: Datos en 360 grados.
- **📄 Competitions.json**: Información sobre competiciones.

El tamaño del dataset es considerable, abarcando múltiples competiciones y temporadas, lo que requiere procesamiento eficiente.

---

## 🛠️ Dificultad técnica
- Procesamiento de grandes volúmenes de datos en tiempo real.
- Integración de múltiples tecnologías como Kafka, Spark Streaming y bases de datos NoSQL.
- Implementación en AWS utilizando buckets y microservicios.

---

## 🧰 Herramientas y/o tecnologías empleadas
- **Ingesta**: Kafka 🪄
- **Procesamiento**: Spark Streaming ⚡
- **Almacenamiento**: MongoDB 🍃 y Neo4j 🌐
- **Orquestación**: Apache Airflow ☁️
- **Visualización**: Node.js 📊
- **Infraestructura**: AWS ☁️

---

## ▶️ Indicaciones de cómo ejecutar el proyecto

### 🖥️ Entorno virtual

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

#### Instalar dependencias 📦
```bash
pip install -r requirements.txt
```

---

## 🐳 Docker para Kafka
```bash
docker network create kafka-net
docker run --name zookeeper --network kafka-net -p 2181:2181 -d zookeeper
docker run -p 9092:9092 --name kafka --network kafka-net -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -d confluentinc/cp-kafka 
```

--- 

## 🗂️ Arquitectura del proyecto

![Arquitectura del Proyecto](diagrama.jpeg)

## 🔍 Descripción de la arquitectura
- **📡 Fuente de datos**: API de StatsBomb 🌐
- **📥 Ingesta**: Kafka 📦
- **⚙️ Procesamiento**: Spark Streaming ⚡
- **💾 Almacenamiento**: MongoDB 🍃 y Neo4j 🌐
- **📋 Orquestación**: Apache Airflow ☁️
- **📊 Visualización**: Node.js 📈

## 🔄 Descripción del proceso ETL/ELT
- **🛠️ Extracción**: Los datos son extraídos desde la API de StatsBomb 🌐.
- **🔧 Transformación**: Mediante Spark Streaming ⚡, se aplican transformaciones como limpieza y enriquecimiento de datos.
- **💾 Carga**: Los datos transformados se almacenan en **MongoDB** 🍃 (documentos) y **Neo4j** 🌐 (relaciones).

---

## 📈 Resultados obtenidos y análisis de estos
*(faltaaa.)*

---

## ⚠️ Dificultades identificadas al momento de implementar la solución
*(faltaaaaa.)*

---

## 📝 Conclusiones y posibles mejoras
*(faltaaa.)*


