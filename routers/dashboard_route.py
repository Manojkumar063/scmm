from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import logging
from typing import Dict

from .jwt_handler import get_current_user
from .cookie_handler import delete_access_token_cookie
from database import users_data,shipment_data

# Set up logger
logger = logging.getLogger(__name__)

# Create router and templates object
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
def dashboard(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """
    Display the user dashboard based on role.
    """
    try:
        user_email = current_user.get("email")
        logger.info(f"Dashboard accessed by user: {user_email}")        # Get total count of shipments
        count = shipment_data.count_documents({})
        logger.info(f"Total shipments count: {count}")
        
        # Check if database connection exists
        if users_data is None:
            logger.error("Database connection not available")
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "message": "Database connection error. Please try again later."}
            )
        
        user = users_data.find_one({"email": user_email})

        if not user:
            logger.warning(f"User not found in database: {user_email}")
            response = templates.TemplateResponse(
                "login.html",
                {"request": request, "message": "User account not found. Please login again."}
            )
            delete_access_token_cookie(response)
            return response

        username = user.get("username", "Unknown User")
        role = user.get("role", "user")
        
        logger.info(f"Rendering dashboard for user: {username}, role: {role}")

        return templates.TemplateResponse(
            "scm-dashboard.html",
            {
                "request": request,
                "current_user": current_user,
                "role": role,
                "username": username,
                'count': count
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
