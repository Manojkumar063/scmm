from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import logging

# Import routers
from routers.login_route import router as login_router
from routers.signup_route import router as signup_router
from routers.dashboard_route import router as dashboard_router
from routers.device_data_route import router as device_data_router
from routers.my_shipment_route import router as my_shipment_router
from routers.new_shipment_route import router as new_shipment_router
from routers.logout_route import router as logout_router
from routers.user_route import router as user_router
from routers.account import router as my_account
from routers.my_shipment_route import router as shipment_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Supply Chain Management System",
    description="A FastAPI-based supply chain management application",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register all routers
app.include_router(signup_router, tags=["Authentication"])
app.include_router(login_router, tags=["Authentication"])
app.include_router(logout_router, tags=["Authentication"])
app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(device_data_router, tags=["Device Management"])
app.include_router(my_shipment_router, tags=["Shipments"])
app.include_router(new_shipment_router, tags=["Shipments"])
app.include_router(user_router, tags=["User Management"])
app.include_router(my_account, tags=["Account Management"])
app.include_router(shipment_router, tags=["Shipment Management"])

@app.get("/")
async def root():
    """Redirect root to registration page."""
    return RedirectResponse(url="/register")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "SCMM API is running"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse("error-404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {exc}")
    return templates.TemplateResponse("error-404.html", {"request": request}, status_code=500)

if __name__ == '__main__':
    logger.info("Starting SCMM application...")
    uvicorn.run(
        'main:app', 
        host='127.0.0.1', 
        port=8000, 
        reload=True,
        log_level="info"
    )