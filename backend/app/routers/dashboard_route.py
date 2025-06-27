from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
from typing import Dict
from datetime import datetime, timedelta

from .jwt_handler import get_current_user
from .cookie_handler import delete_access_token_cookie
from backend.app.database import users_data, shipment_data, device_data

# ────────────────────────────────────────────────────────────────────────────────
# Logger Setup
# ────────────────────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────────────────────
# Router & Templates Configuration
# ────────────────────────────────────────────────────────────────────────────────
router = APIRouter()
templates = Jinja2Templates(directory="backend/app/templates")

# ────────────────────────────────────────────────────────────────────────────────
# Dashboard Route
# ────────────────────────────────────────────────────────────────────────────────
@router.get("/dashboard")
def dashboard(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """
    Display the user dashboard based on role.
    """
    try:
        user_email = current_user.get("email")
        logger.info(f"Dashboard accessed by user: {user_email}")

        # Stats from collections
        active_shipments = shipment_data.count_documents({})
        online_devices = device_data.count_documents({})
        active_users = users_data.count_documents({})

        # Get user data
        user = users_data.find_one({"email": user_email})
        username = user.get("username", "Unknown User")
        role = user.get("role", "user")

        logger.info(f"Rendering dashboard for user: {username}, role: {role}")
        logger.info(f"Stats - Shipments: {active_shipments}, Devices: {online_devices}, Users: {active_users}")

        return templates.TemplateResponse(
            "scm-dashboard.html",
            {
                "request": request,
                "username": username,
                "role": role,
                "active_shipments": active_shipments,
                "devices_online": online_devices,
                "active_users": active_users
            }
        )

    except HTTPException:
        logger.error(f"HTTP Exception in dashboard for user: {current_user.get('email', 'unknown')}")
        raise

    except Exception as e:
        logger.error(f"Dashboard error for {current_user.get('email', 'unknown')}: {str(e)}")
        response = templates.TemplateResponse(
            "login.html",
            {"request": request, "message": "An error occurred. Please login again."}
        )
        delete_access_token_cookie(response)
        return response
