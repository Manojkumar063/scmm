# SCMM - Supply Chain Management System

A modern, containerized supply chain management platform built with FastAPI, Kafka, and MongoDB.

## 🚀 Features

- **REST API**: FastAPI backend with comprehensive endpoints
- **Real-time Messaging**: Kafka integration for event streaming
- **Database**: MongoDB for flexible data storage
- **Authentication**: JWT-based secure authentication
- **Containerized**: Docker Compose for easy deployment
- **Web Interface**: Complete frontend with dashboard and forms

## 📋 Prerequisites

- Docker & Docker Compose
- Git

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SCMM
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# Application
JWT_SECRET=your-secret-key-here
API_HOST=0.0.0.0
API_PORT=8000

# Database
MONGODB_URL=mongodb://mongo:27017
MONGODB_DB=scmm_db

# Kafka
KAFKA_BROKER=kafka:9092
KAFKA_TOPIC=scmm-events
```

## 🧪 Development

For local development without Docker:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start services individually
python backend/app/main.py
```

## 📁 Architecture

```
SCMM/
├── backend/
│   ├── app/                 # FastAPI application
│   │   ├── routers/         # API route handlers
│   │   ├── templates/       # HTML templates
│   │   └── static/          # CSS, JS, images
│   └── kafka/               # Kafka services
│       ├── consumer/        # Message consumer
│       ├── producer/        # Message producer
│       └── server/          # Kafka server setup
├── docker-compose.yml       # Multi-service orchestration
├── Dockerfile              # Application container
└── requirements.txt        # Python dependencies
```

## 🔒 Security

- JWT tokens for API authentication
- Environment-based configuration
- No hardcoded credentials
- Secure cookie handling

## 📊 Monitoring

- Application logs: `logs/scmm_app.log`
- Kafka logs: `logs/scmm.log`
- Container logs: `docker-compose logs -f`

## 🚀 Production Deployment

1. **Secure your environment**
   ```bash
   # Use strong secrets
   JWT_SECRET=$(openssl rand -hex 32)
   ```

2. **Production build**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Health checks**
   ```bash
   curl http://localhost:8000/health
   ```

## 🛠️ Common Commands

```bash
# View logs
docker-compose logs -f [service-name]

# Restart services
docker-compose restart

# Update and rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Database backup
docker exec mongo-container mongodump --out /backup

# Scale services
docker-compose up -d --scale kafka-consumer=3
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<<<<<<< HEAD
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](../../issues)
- **Documentation**: [Wiki](../../wiki)
- **Discussions**: [GitHub Discussions](../../discussions)

---

**Built with  for modern supply chain management**
=======
4. Run the application:
```powershell
uvicorn backend.app.main:app --reload --port 8001
```

## API Documentation
Once running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#Build and start all services using Docker Compose
#Open a terminal in your project root and run:
```
docker-compose down
docker-compose build
docker-compose up -d
```
>>>>>>> 0bb568122e79e3af5fb46e2605d51ad5d7b228f8
