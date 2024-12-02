FROM apache/airflow:2.6.0
WORKDIR /opt/airflow
COPY dags/ /opt/airflow/dags/
RUN pip install --no-cache-dir apache-airflow-providers-amazon
CMD ["airflow", "standalone"]
