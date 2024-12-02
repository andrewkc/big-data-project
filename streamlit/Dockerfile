FROM python:3.9-slim
WORKDIR /app
COPY src/ /app/src/
RUN pip install --no-cache-dir streamlit pymongo kafka-python
CMD ["streamlit", "run", "/app/src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
