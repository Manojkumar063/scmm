# Supply Chain Monitoring & Management (SCMM) System

![SCMM System Architecture](static/images/download.jpg)

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Frontend Guide](#frontend-guide)
- [Security Implementation](#security-implementation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Supply Chain Monitoring & Management (SCMM) system is a comprehensive solution for tracking shipments, monitoring IoT devices, and managing logistics operations. This web application provides real-time visibility into supply chain activities with secure user authentication and role-based access control.

## Key Features

### 🚀 Core Functionality
- **User Authentication**: Secure JWT-based login/logout with cookie management
- **Shipment Management**: Create, view, and track shipments
- **Device Monitoring**: Real-time IoT device data visualization
- **Dashboard Analytics**: Comprehensive supply chain metrics

### 🔒 Security Features
- Password hashing with bcrypt
- JWT token authentication
- CSRF protection
- Secure cookie handling
- Role-based access control

### 📊 Data Management
- MongoDB database integration
- Pydantic data validation
- Efficient CRUD operations
- Real-time data updates

## Technology Stack

### Backend
- **Python 3.9+**
- **FastAPI** - High-performance web framework
- **MongoDB** - NoSQL database
- **Pydantic** - Data validation
- **PyJWT** - JSON Web Token implementation
- **Uvicorn** - ASGI server

### Frontend
- **Bootstrap 5** - Responsive UI components
- **JavaScript** - Client-side logic
- **Chart.js** - Data visualization
- **Jinja2** - Templating engine

### DevOps
- **Poetry/Pip** - Dependency management
- **Docker** - Containerization (optional)
- **Git** - Version control

## System Architecture

```
SCMM System Architecture
┌───────────────────────────────────────────────────────────────────────┐
│                            Client Browser                            │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────────┐
│                           FastAPI Server                            │
│ ┌─────────────┐  ┌─────────────┐  ┌───────────────────────────────┐ │
│ │   Routers    │  │ Data Models │  │     Authentication Middleware │ │
│ │ - Account    │  │ - Users     │  │     - JWT Validation         │ │
│ │ - Auth       │  │ - Shipments │  │     - Role Checking          │ │
│ │ - Shipments  │  │ - Devices   │  └───────────────────────────────┘ │
│ │ - Devices    │  └─────────────┘                                   │
│ └─────────────┘                                                     │
│                           │                                         │
│                           ▼                                         │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │                         MongoDB                                │ │
│ │  - users collection                                            │ │
│ │  - shipments collection                                       │ │
│ │  - devices collection                                         │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────┘
```

## Installation Guide

### Prerequisites
- Python 3.9+
- MongoDB 4.4+
- Node.js (for frontend assets, optional)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/scmm-system.git
   cd scmm-system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv-scmm
   source venv-scmm/bin/activate  # Linux/Mac
   venv-scmm\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=scmm_db
   JWT_SECRET_KEY=your-secret-key-here
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the application**
   Open your browser to: `http://localhost:8000`

## Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `scmm_db` |
| `JWT_SECRET_KEY` | Secret for JWT token generation | - |
| `JWT_ALGORITHM` | JWT encryption algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

### Database Setup
The system will automatically create the following collections:
- `users` - User accounts and credentials
- `shipments` - Shipment tracking data
- `devices` - IoT device information and metrics

## API Documentation

The system provides comprehensive API endpoints documented with Swagger UI. After starting the server, access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key API Endpoints

#### Authentication
- `POST /login` - User authentication
- `POST /logout` - User logout
- `POST /register` - New user registration

#### Shipment Management
- `GET /shipments` - List all shipments
- `POST /shipments` - Create new shipment
- `GET /shipments/{id}` - Get shipment details

#### Device Data
- `GET /devices` - List all devices
- `GET /devices/{id}/data` - Get device metrics

#### User Management
- `GET /users` - List all users (admin only)
- `GET /users/me` - Get current user profile

## Frontend Guide

The frontend is built with Bootstrap 5 and includes the following key JavaScript modules:

### Core Modules
- **auth.js** - Handles login/logout functionality
- **register.js** - Manages user registration
- **create-shipment.js** - Shipment creation form handling
- **my_shipment.js** - Shipment listing and management
- **device-data-manager.js** - Real-time device data visualization

### Templates
The Jinja2 templates are located in the `templates/` directory and include:

- **Account Management**: `account.html`
- **Shipment Creation**: `create-shipment.html`
- **Dashboard**: `scm-dashboard.html`
- **Device Monitoring**: `device-data.html`
- **Authentication**: `login.html`, `register.html`

## Security Implementation

### Authentication Flow
1. User submits credentials via `/login` endpoint
2. Server verifies credentials and issues JWT token
3. Token is stored in secure, HttpOnly cookie
4. Subsequent requests include token in Authorization header
5. Middleware validates token for protected routes

### Security Measures
- **Password Hashing**: BCrypt algorithm
- **Token Storage**: HttpOnly, Secure cookies
- **CSRF Protection**: Implemented in sensitive forms
- **Rate Limiting**: Applied to authentication endpoints
- **CORS**: Configured for trusted origins only

## Deployment

### Production Deployment
For production deployment, consider:

1. **Using a production ASGI server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 80 --workers 4
   ```

2. **Setting up a reverse proxy** (Nginx recommended):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Implementing HTTPS** using Let's Encrypt or your SSL provider.

### Docker Deployment
A sample `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 guidelines
- Type hints for all function signatures
- Document complex functions with docstrings
- Include unit tests for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**SCMM System** © 2023 | Developed with FastAPI and MongoDB
