# File: kafka/producer/Dockerfile
FROM python:3.11-slim
RUN pip install kafka-python
WORKDIR /producer
COPY . .
CMD ["python", "producer.py"]