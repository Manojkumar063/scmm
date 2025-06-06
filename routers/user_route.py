# user_route.py
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import logging
from typing import Dict, List
from pydantic import BaseModel

from .jwt_handler import get_current_user
from .cookie_handler import delete_access_token_cookie
from database import users_data

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory='templates')

# Pydantic models for request validation
class UserUpdateRequest(BaseModel):
    username: str = None
    email: str = None
    role: str = None
    status: str = None

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
            # Set default status if not present
            if "status" not in usr:
                usr["status"] = "active"
            users_list.append(usr)

        return templates.TemplateResponse("users.html", {
            "request": request,
            "users": users_list,
            "role": role,
            "username": username,
            "current_user_email": current_user.get("email")
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

@router.get('/api/users/{user_email}')
def get_user_details(
    user_email: str,
    current_user: Dict[str, str] = Depends(get_current_user)
):
    """Get user details for editing (admin only)."""
    try:
        check_admin_access(current_user)

        user = users_data.find_one({"email": user_email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Remove sensitive data
        user.pop("password", None)
        user["_id"] = str(user.get("_id", ""))
        
        # Set default status if not present
        if "status" not in user:
            user["status"] = "active"

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user details error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put('/api/users/{user_email}')
def edit_user(
    user_email: str,
    user_data: UserUpdateRequest,
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

        # Check if user exists
        existing_user = users_data.find_one({"email": user_email})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Build update data
        update_data = {}
        if user_data.username:
            update_data["username"] = user_data.username
        if user_data.role and user_data.role in ["user", "admin"]:
            update_data["role"] = user_data.role
        if user_data.status and user_data.status in ["active", "inactive", "locked"]:
            update_data["status"] = user_data.status

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )

        result = users_data.update_one(
            {"email": user_email},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info(f"User {user_email} updated by admin {current_user['email']}")
        return {"message": "User updated successfully", "updated_fields": update_data}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User edit error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete('/api/users/{user_email}')
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

@router.post('/api/users/{user_email}/reset-password')
def reset_user_password(
    user_email: str,
    current_user: Dict[str, str] = Depends(get_current_user)
):
    """Reset user password (admin only)."""
    try:
        check_admin_access(current_user)

        # Check if user exists
        user = users_data.find_one({"email": user_email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Generate a temporary password (you should implement proper password generation)
        import secrets
        import string
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        # Hash the password (implement your password hashing logic here)
        # For example, if you're using bcrypt:
        # from passlib.context import CryptContext
        # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # hashed_password = pwd_context.hash(temp_password)
        
        # For now, just using plain text (NOT RECOMMENDED FOR PRODUCTION)
        hashed_password = temp_password  # Replace with proper hashing
        
        result = users_data.update_one(
            {"email": user_email},
            {"$set": {"password": hashed_password, "password_reset_required": True}}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info(f"Password reset for user {user_email} by admin {current_user['email']}")
        
        # In production, you should send this password via email instead of returning it
        return {
            "message": "Password reset successfully",
            "temporary_password": temp_password,
            "note": "User must change password on next login"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )   