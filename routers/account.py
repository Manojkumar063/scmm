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

@router.get("/my_account")
def account(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """
    Display the user's account information.
    """
    try:
        user_email = current_user["email"]
        user = users_data.find_one({"email": user_email})
        
        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(status_code=401, detail="User not found")

        return templates.TemplateResponse(
            "account.html",
            {
                "request": request,
                "username": user.get("username", "Unknown User"),
                "email": user.get("email", ""),
                "role": user.get("role", "user"),
                "join_date": user.get("join_date", "N/A")
            }
        )
    except Exception as e:
        logger.error(f"Account page error: {str(e)}")
        response = templates.TemplateResponse(
            "login.html",
            {"request": request, "message": "Please login again"}
        )
        delete_access_token_cookie(response)
        return response