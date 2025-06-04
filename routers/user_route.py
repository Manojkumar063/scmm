
# user_route.py
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
import logging
from typing import Dict, List

from .jwt_handler import get_current_user
from .cookie_handler import delete_access_token_cookie
from database import users_data

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory='templates')

def check_admin_access(current_user: Dict[str, str]) -> Dict:
    """Check if current user has admin access and return user data."""
    user_email = current_user.get("email")
    user = users_data.find_one({"email": user_email})

    if not user:
        logger.warning(f"User not found: {user_email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user

@router.get('/users')
def users(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """Display all users (admin only)."""
    try:
        user = check_admin_access(current_user)
        username = user.get("username", "Admin")
        role = user.get("role")

        # Fetch all users
        users_cursor = users_data.find()
        users_list: List[Dict] = []

        for usr in users_cursor:
            usr["_id"] = str(usr.get("_id", ""))
            # Remove password from response for security
            if "password" in usr:
                del usr["password"]
            users_list.append(usr)

        return templates.TemplateResponse("users.html", {
            "request": request,
            "users": users_list,
            "role": role,
            "username": username
        })

    except HTTPException as e:
        if e.status_code == status.HTTP_403_FORBIDDEN:
            return templates.TemplateResponse('404.html', {'request': request})
        raise
    except Exception as e:
        logger.error(f"Users GET error for {current_user.get('email', 'unknown')}: {str(e)}")
        response = templates.TemplateResponse('login.html', {
            'request': request,
            'message': "An error occurred. Please login again."
        })
        delete_access_token_cookie(response)
        return response

@router.put('/users/{user_email}')
def edit_user(
    user_email: str,
    user_data: Dict,
    current_user: Dict[str, str] = Depends(get_current_user)
):
    """Update user data (admin only)."""
    try:
        check_admin_access(current_user)

        # Validate user_email
        if not user_email or "@" not in user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Remove sensitive fields that shouldn't be updated this way
        sensitive_fields = ["password", "_id"]
        for field in sensitive_fields:
            user_data.pop(field, None)

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )

        result = users_data.update_one(
            {"email": user_email},
            {"$set": user_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info(f"User {user_email} updated by admin {current_user['email']}")
        return {"message": "User updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User edit error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete('/users/{user_email}')
def delete_user(
    user_email: str,
    current_user: Dict[str, str] = Depends(get_current_user)
):
    """Delete user (admin only)."""
    try:
        admin_user = check_admin_access(current_user)

        # Prevent admin from deleting themselves
        if user_email == current_user["email"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )

        # Validate user_email
        if not user_email or "@" not in user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        result = users_data.delete_one({"email": user_email})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info(f"User {user_email} deleted by admin {current_user['email']}")
        return {"message": "User deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User deletion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )