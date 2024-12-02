import streamlit as st
from kafka import KafkaProducer
import json
from statsbombpy import sb

# Kafka Producer Configuración
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Dashboard Interactivo
st.title("Football Analytics Dashboard")

# Filtros disponibles
competition = st.selectbox("Seleccione una Competición:", ["1. Bundesliga", "Premier League", "Champions League"])
season = st.selectbox("Seleccione una Temporada:", ["2019/2020", "2020/2021"])
match_id = st.text_input("ID del Partido (opcional):", "")
player_name = st.text_input("Nombre del Jugador (opcional):", "")

# Obtener los IDs dinámicos de StatsBomb
competitions = sb.competitions(fmt="dict")
selected_competition = next((c for c in competitions if c["competition_name"] == competition), None)

# Botón para buscar datos
if st.button("Buscar"):
    if not selected_competition:
        st.error("Competición no encontrada.")
    else:
        # Construir solicitud
        request = {
            "competition": competition,
            "season": season,
            "match_id": int(match_id) if match_id else None,
            "player_name": player_name,
            "competition_id": selected_competition["competition_id"],
            "season_id": next((s["season_id"] for s in competitions if s["season_name"] == season), None)
        }
        # Enviar solicitud a Kafka
        producer.send("dashboard-requests", value=request)
        st.success(f"Solicitud enviada: {request}")
        st.write("Esperando resultados...")
