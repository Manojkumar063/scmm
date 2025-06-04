from fastapi import Request, Depends, APIRouter, HTTPException, status
from fastapi.templating import Jinja2Templates
import logging
from typing import Dict, List

from .jwt_handler import get_current_user
from database import device_data, users_data
from .cookie_handler import delete_access_token_cookie

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/device-data')
def devicedata(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """Display device data (admin only)."""
    try:
        user_email = current_user["email"]
        user = users_data.find_one({'email': user_email})
        print(f"User email: {user_email}")
        logger.info(f"Device data accessed by user: {user_email}")
        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        print(f"User found: {user}")
        username = user.get("username", "Unknown User")
        role = user.get("role", "user")
        print(f"User role: {role}")
        # Check admin access
        if role != "admin":
            return templates.TemplateResponse('404.html', {'request': request})
        logger.info(f"Rendering device data for user: {username}, role: {role}")
        # Fetch device data
        devices_cursor = device_data.find()
        devices: List[Dict] = []
        print(f"Devices cursor: {devices_cursor}")
        for device in devices_cursor:
            device["_id"] = str(device.get("_id", ""))
            devices.append(device)
        logger.info(f"Total devices found: {len(devices)}")
        print(f"Devices: {devices}")
        return templates.TemplateResponse(
            'device-data.html',
            {
                'request': request,
                "role": role,
                'devices': devices,
                'username': username
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Device data error for user {current_user.get('email', 'unknown')}: {str(e)}")
        response = templates.TemplateResponse(
            'login.html',
            {'request': request, 'message': "An error occurred. Please login again."}
        )
        delete_access_token_cookie(response)
        return response