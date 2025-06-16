# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

# ────────────────────────────────────────────────────────────────────────────────
# Environment Setup
# ────────────────────────────────────────────────────────────────────────────────

load_dotenv()

# ────────────────────────────────────────────────────────────────────────────────
# Logging Configuration
# ────────────────────────────────────────────────────────────────────────────────

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format=os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"),
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "logs/scmm_app.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────────────────────
# Local Imports
# ────────────────────────────────────────────────────────────────────────────────

from database import get_database_status

# Routers
from routers.login_route import router as login_router
from routers.signup_route import router as signup_router
from routers.logout_route import router as logout_router
from routers.dashboard_route import router as dashboard_router
from routers.device_data_route import router as device_data_router
from routers.my_shipment_route import router as my_shipment_router
from routers.new_shipment_route import router as new_shipment_router
from routers.user_route import router as user_router
from routers.account import router as account_router

# ────────────────────────────────────────────────────────────────────────────────
# Application Lifecycle
# ────────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔄 Starting SCMM Application...")
    yield
    logger.info("🛑 SCMM Application shutdown.")

# ────────────────────────────────────────────────────────────────────────────────
# FastAPI Application Instance
# ────────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title=os.getenv("APP_NAME", "Supply Chain Management System"),
    description="SCMM with Kafka integration",
    version=os.getenv("APP_VERSION", "1.0.0"),
    lifespan=lifespan
)

# ────────────────────────────────────────────────────────────────────────────────
# Middleware Configuration
# ────────────────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ────────────────────────────────────────────────────────────────────────────────
# Static Files & Templates
# ────────────────────────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ────────────────────────────────────────────────────────────────────────────────
# Router Registrations
# ────────────────────────────────────────────────────────────────────────────────

app.include_router(signup_router, tags=["Authentication"])
app.include_router(login_router, tags=["Authentication"])
app.include_router(logout_router, tags=["Authentication"])
app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(device_data_router, tags=["Device Management"])
app.include_router(my_shipment_router, tags=["Shipments"])
app.include_router(new_shipment_router, tags=["Shipments"])
app.include_router(user_router, tags=["User Management"])
app.include_router(account_router, tags=["Account Management"])

# ────────────────────────────────────────────────────────────────────────────────
# General Routes
# ────────────────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Redirect"])
async def root():
    return RedirectResponse("/login")


@app.get("/health", tags=["Monitoring"])
async def health():
    db_status = get_database_status()
    return {
        "status": "healthy" if db_status["status"] == "connected" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": db_status["status"]
        }
    }

# ────────────────────────────────────────────────────────────────────────────────
# Custom Error Handlers
# ────────────────────────────────────────────────────────────────────────────────

@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error-404.html", {"request": request}, status_code=404)


@app.exception_handler(500)
async def server_error(request: Request, exc: HTTPException):
    logger.error(f"500 Internal Server Error: {exc}")
    return JSONResponse({"detail": "Internal Server Error"}, status_code=500)

# ────────────────────────────────────────────────────────────────────────────────
# Application Entrypoint
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "true").lower() == "true"
    )
