# Supply Chain Management Module (SCMM)

A FastAPI-based supply chain management application with real-time IoT data streaming and Kafka integration.

## Current Project Structure
```
SCMM/
├── main.py                 # FastAPI application entry point
├── database.py            # MongoDB database configuration
├── models.py              # Pydantic data models
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
│
├── kafka_module/                # Kafka Integration
│   ├── consumer.py       # Kafka consumer implementation
│   ├── server.py         # server
│   ├── docker-compose.yml  #docker yml file
│   └── producer.py       # Kafka producer implementation
│
├── routers/              # API Routes
│   ├── __init__.py
│   ├── account.py        # Account management routes
│   ├── cookie_handler.py # Cookie management utilities
│   ├── dashboard_route.py # Dashboard data routes
│   ├── device_data_route.py # Device management routes
│   ├── jwt_handler.py    # JWT authentication handler
│   ├── login_route.py    # Login endpoints
│   ├── logout_route.py   # Logout endpoints
│   ├── my_shipment_route.py # User shipment routes
│   ├── new_shipment_route.py # Create shipment routes
│   ├── signup_route.py   # Registration routes
│   └── user_route.py     # User management routes
│
├── static/              # Static Assets
│   ├── css/
│   │   └── styles.css   # Global CSS styles
│   ├── images/
│   │   └── download.jpg # Application images
│   └── js/
│       ├── auth.js      # Authentication JavaScript
│       ├── create-shipment.js # Shipment creation logic
│       ├── device-data-manager.js # Device data handling
│       ├── login.js     # Login form handling
│       ├── my_shipment.js # Shipment management
│       ├── register.js  # Registration form handling
│       └── security.js  # Security utilities
│
├── templates/           # HTML Templates
│   ├── account.html    # Account profile page
│   ├── create-shipment.html # New shipment form
│   ├── device-data.html # Device monitoring dashboard
│   ├── error-404.html  # Error page
│   ├── landingpage.html # Landing page
│   ├── login.html      # Login page
│   ├── my_shipment.html # User shipments view
│   ├── register.html   # Registration page
│   ├── scm-dashboard.html # Main dashboard
│   └── users.html      # User management interface
│
└── venv-scmm/          # Virtual Environment
    ├── Include/
    ├── Lib/
    │   └── site-packages/ # Python dependencies
    └── Scripts/          # Virtual environment executables
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
