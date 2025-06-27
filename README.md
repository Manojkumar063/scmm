# Supply Chain Management Module (SCMM)

A FastAPI-based supply chain management application with real-time IoT data streaming and Kafka integration.

## Current Project Structure
```
SCMM/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── backend/
│   ├── __init__
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── account.py
│   │   │   ├── cookie_handler.py
│   │   │   ├── dashboard_route.py
│   │   │   ├── device_data_route.py
│   │   │   ├── jwt_handler.py
│   │   │   ├── login_route.py
│   │   │   ├── logout_route.py
│   │   │   ├── my_shipment_route.py
│   │   │   ├── new_shipment_route.py
│   │   │   ├── signup_route.py
│   │   │   ├── user_route.py
│   │   │   └── __pycache__/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── styles.css
│   │   │   ├── images/
│   │   │   ├── js/
│   │   │   └── uploads/
│   │   └── templates/
│   │       ├── account.html
│   │       ├── create-shipment.html
│   │       ├── device-data.html
│   │       ├── error-404.html
│   │       ├── landingpage.html
│   │       ├── login.html
│   │       ├── my_shipment.html
│   │       ├── register.html
│   │       ├── scm-dashboard.html
│   │       └── users.html
│   ├── kafka/
│   │   ├── __init__.py
│   │   ├── consumer/
│   │   │   ├── __init__.py
│   │   │   ├── consumer.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   ├── producer/
│   │   │   ├── __init__.py
│   │   │   ├── Dockerfile
│   │   │   ├── producer.py
│   │   │   └── requirements.txt
│   │   └── server/
│   │       ├── __init__.py
│   │       ├── Dockerfile
│   │       └── server.py
│   └── venv-scmm/
│       ├── LICENSE.txt
│       ├── pyvenv.cfg
│       ├── Include/
│       ├── Lib/
│       │   └── site-packages/
│       └── Scripts/
│           ├── activate
│           ├── activate.bat
│           ├── Activate.ps1
│           ├── ...
```

## Key Features
- User Authentication & Authorization
- Real-time IoT Device Data Streaming via Kafka
- Shipment Management & Tracking
- User Management System
- Dashboard Analytics
- MongoDB Database Integration
- Responsive Web Interface

## Tech Stack
- Backend: FastAPI (Python)
- Database: MongoDB
- Message Broker: Apache Kafka
- Frontend: Bootstrap 5, JavaScript
- Authentication: JWT
- Template Engine: Jinja2

## Setup Instructions

1. Create and activate virtual environment:
```powershell
python -m venv venv-scmm
.\venv-scmm\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
MONGODB_URL=your_mongodb_url
DATABASE_NAME=your_database_name
KAFKA_BOOTSTRAP_SERVERS=your_kafka_servers
JWT_SECRET=your_jwt_secret
```

4. Run the application:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation
Once running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
