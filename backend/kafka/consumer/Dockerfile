FROM python:3.11-slim
ENV PYTHONPATH="/scmm"
WORKDIR /consumer
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/kafka/consumer/ ./
COPY backend/app /scmm/app
CMD ["python", "consumer.py"]