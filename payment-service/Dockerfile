FROM python:3.9-slim

WORKDIR /app
COPY app.py /app
RUN pip install Flask psycopg2-binary prometheus_flask_exporter
CMD ["python", "app.py"]
