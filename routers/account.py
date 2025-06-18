from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Dict
from datetime import datetime
import logging

from .jwt_handler import get_current_user
from .cookie_handler import delete_access_token_cookie
from database import users_data, shipment_data

# ────────────────────────────────────────────────────────────────────────────────
# Logger Configuration
# ────────────────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────────────────────
# Router and Templates
# ────────────────────────────────────────────────────────────────────────────────

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ────────────────────────────────────────────────────────────────────────────────
# My Account Route
# ────────────────────────────────────────────────────────────────────────────────

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

        # Format created_at
        created_at_str = "N/A"
        if "created_at" in user and user["created_at"]:
            if isinstance(user["created_at"], str):
                try:
                    user["created_at"] = datetime.fromisoformat(user["created_at"])
                except Exception:
                    user["created_at"] = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S")

            if isinstance(user["created_at"], datetime):
                created_at_str = user["created_at"].strftime("%Y-%m-%d")

        return templates.TemplateResponse(
            "account.html",
            {
                "request": request,
                "username": user.get("username"),
                "email": user.get("email", ""),
                "role": user.get("role", "user"),
                "join_date": created_at_str
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
