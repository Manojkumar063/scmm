# File: Dockerfile
FROM python:3.9-slim

WORKDIR /scmm

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]
