from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from statsbombpy import sb

# Configuración del consumidor Kafka
consumer = KafkaConsumer(
    "dashboard-requests",
    bootstrap_servers=["kafka:9092"],  # Dirección del clúster Kafka
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# Configuración de la base de datos MongoDB
client = MongoClient("mongodb://mongodb:27017")  # Dirección del clúster MongoDB
db = client["football"]
collection = db["search_logs"]

# Función para manejar las solicitudes
def handle_request(request):
    results = {}

    try:
        # Filtrar por ID de partido
        if request.get("match_id"):
            results["events"] = sb.events(match_id=request["match_id"], fmt="dict")

        # Filtrar por competición y temporada
        elif request.get("competition") and request.get("season"):
            results["competition_events"] = sb.competition_events(
                country="Germany",  # Modificar si la competición está en otro país
                division=request["competition"],
                season=request["season"],
                gender="male",
                fmt="dict"
            )

        # Filtrar por jugador
        if request.get("player_name"):
            # Encontrar el ID del jugador y sus estadísticas
            results["player_stats"] = sb.player_season_stats(
                competition_id=request.get("competition_id"),  # Debe calcularse si falta
                season_id=request.get("season_id"),  # Debe calcularse si falta
                fmt="dict"
            )
    except Exception as e:
        results["error"] = f"Error al procesar la solicitud: {str(e)}"

    return results

# Consumir solicitudes desde Kafka
for message in consumer:
    request = message.value
    print(f"Procesando solicitud: {request}")

    # Procesar la solicitud y obtener los resultados
    results = handle_request(request)

    # Guardar el resultado en MongoDB
    log_entry = {
        "request": request,
        "results": results,
        "status": "completed"
    }
    collection.insert_one(log_entry)
    print(f"Datos registrados en MongoDB: {log_entry}")
