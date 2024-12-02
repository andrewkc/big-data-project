# ⚽ Big Data Project 📊

## 🚀 Introducción y Justificación del Problema a Resolver
Este proyecto tiene como objetivo analizar datos de fútbol provenientes de la [repo de StatsBomb](https://github.com/statsbomb/open-data.git). La información abarca eventos, alineaciones, partidos y competiciones, permitiendo realizar análisis avanzados sobre el rendimiento de equipos y jugadores. Implementamos una arquitectura de Big Data que permite procesamiento en tiempo real y visualización de datos complejos.

---

## 📂 Descripción del Dataset, Origen y Tamaño de Data
El dataset proviene de la repo pública de [StatsBomb Open Data](https://github.com/statsbomb/open-data.git) y contiene:

- **⚽ Events**: Información detallada de eventos durante los partidos.
- **🧑‍🤝‍🧑 Lineups**: Alineaciones de equipos.
- **🏟️ Matches**: Datos generales de cada partido.
- **🔄 Three-sixty**: Datos en 360 grados.
- **📄 Competitions.json**: Información sobre competiciones.

El tamaño es considerable, abarcando múltiples competiciones y temporadas, lo que requiere procesamiento eficiente.

---

## 🛠️ Dificultad Técnica
- Procesamiento de grandes volúmenes de datos en tiempo real.
- Integración de Kafka, Dask y bases de datos NoSQL.
- Implementación en AWS utilizando buckets y microservicios.
- Generación de visualizaciones en tiempo real con Streamlit.

---

## 🧰 Herramientas y/o Tecnologías Empleadas
- **Ingesta**: Kafka 🪄
- **Procesamiento**: Dask ⚡
- **Almacenamiento**: DynamoDB 🍃
- **Orquestación**: Apache Airflow ☁️
- **Visualización**: Streamlit 📊
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
## 🗂️ Arquitectura del Proyecto

![Arquitectura del Proyecto](diagrama.jpeg)

## 🔍 Descripción de la Arquitectura
La arquitectura implementada en este proyecto sigue un flujo bien definido, donde los datos se extraen de la API de StatsBomb, se ingieren mediante Kafka, y luego se procesan en paralelo utilizando Dask. Los resultados procesados se almacenan en DynamoDB para su posterior análisis. Finalmente, la visualización de los datos se maneja a través de **Streamlit**, lo que permite construir un dashboard interactivo en tiempo real.

- **📡 Fuente de Datos**: API de StatsBomb 🌐
- **📥 Ingesta**: Kafka 📦
- **⚙️ Procesamiento**: Dask ⚡
- **💾 Almacenamiento**: DynamoDB 🍃
- **📊 Visualización**: Streamlit 📈

---

## 🔄 Descripción del Proceso ETL/ELT
- **🛠️ Extracción**: Los datos son extraídos desde la API de StatsBomb 🌐.
- **🔧 Transformación**: Mediante Dask ⚡, se aplican transformaciones como limpieza y enriquecimiento de datos.
- **💾 Carga**: Los datos transformados se almacenan en **DynamoDB** 🍃 (bases de datos NoSQL).

---

## 📈 Resultados Obtenidos y Análisis de Estos


---

## ⚠️ Dificultades Identificadas al Momento de Implementar la Solución


---

## 📝 Conclusiones y Posibles Mejoras
