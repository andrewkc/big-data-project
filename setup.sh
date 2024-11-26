#!/bin/bash

ENV_NAME="venv"

echo "Creando entorno virtual..."
python3 -m venv $ENV_NAME

echo "Activando el entorno virtual..."
source $ENV_NAME/bin/activate

if [ -f "requirements.txt" ]; then
  echo "Instalando dependencias desde requirements.txt..."
  pip install -r requirements.txt
else
  echo "No se encontró el archivo requirements.txt. Saltando instalación de dependencias."
fi

