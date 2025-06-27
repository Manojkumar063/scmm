from fastapi import Request, Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import logging
from typing import Dict, List
from datetime import datetime, timedelta

# # Import custom handlers and database collections
from .jwt_handler import get_current_user  # Auth middleware to extract current user from JWT
from backend.app.database import device_data, users_data  # MongoDB collections
from .cookie_handler import delete_access_token_cookie  # Clears access token cookies

# # ────────────────────────────────────────────────────────────────────────────────
# # Logger, Router, Templates
# # ────────────────────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)  # Set up logger for debugging and monitoring
router = APIRouter()  # Initialize API router for grouping endpoints
templates = Jinja2Templates(directory="backend/app/templates")  # Setup Jinja2 template directory

# ────────────────────────────────────────────────────────────────────────────────
# Device Data Page (Web)
# ────────────────────────────────────────────────────────────────────────────────
@router.get('/device-data')
def devicedata(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """Display device data page (admin only)."""
    try:
        user_email = current_user["email"]
        user = users_data.find_one({'email': user_email})

        logger.info(f"Device data page accessed by user: {user_email}")

        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        username = user.get("username", "Unknown User")
        role = user.get("role", "user")

        if role != "admin":
            return templates.TemplateResponse('error-404.html', {'request': request})

        devices = list(device_data.find())
        # logger.info(f"Fetched devices: {devices}")

        logger.info(f"Rendering device data page for user: {username}, role: {role}")

        return templates.TemplateResponse(
            'device-data.html',
            {
                'request': request,
                "role": role,
                'username': username,
                'devices': devices
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rendering device data page: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error"}
        )

# # ────────────────────────────────────────────────────────────────────────────────
# # API: Device Data
# # ────────────────────────────────────────────────────────────────────────────────
# @router.get('/api/device-data')
# async def get_device_data_api(current_user: Dict[str, str] = Depends(get_current_user)):
#     """API endpoint to fetch device data (admin only)."""
#     try:
#         user_email = current_user["email"]
#         user = users_data.find_one({'email': user_email})

#         if not user:
#             logger.warning(f"User not found: {user_email}")
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

#         if user.get("role", "user") != "admin":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Access denied. Admin privileges required."
#             )

#         devices_cursor = device_data.find().sort("timestamp", -1).limit(100)
#         devices: List[Dict] = []

#         for device in devices_cursor:
#             device_dict = {
#                 "id": str(device.get("_id", "")),
#                 "device_id": device.get("device_id", "N/A"),
#                 "battery_level": device.get("battery_level", 0),
#                 "temperature": device.get("temperature", 0),
#                 "humidity": device.get("humidity", 0),
#                 "route_to": device.get("route_to", "N/A"),
#                 "route_from": device.get("route_from", "N/A"),
#                 "timestamp": device.get("timestamp").isoformat() if device.get("timestamp") else datetime.utcnow().isoformat(),
#                 "is_active": device.get("is_active", True),
#                 "status": "Active" if device.get("is_active", True) else "Inactive"
#             }
#             devices.append(device_dict)

#         logger.info(f"Returning {len(devices)} device records for user: {user_email}")

#         return JSONResponse(content={
#             "success": True,
#             "data": devices,
#             "count": len(devices)
#         })

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"API device data error for user {current_user.get('email', 'unknown')}: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to fetch device data"
#         )


# # ────────────────────────────────────────────────────────────────────────────────
# # API: Device Stats
# # ────────────────────────────────────────────────────────────────────────────────
# @router.get('/api/device-data/stats')
# async def get_device_stats(current_user: Dict[str, str] = Depends(get_current_user)):
#     """API endpoint to fetch device statistics (admin only)."""
#     try:
#         user_email = current_user["email"]
#         user = users_data.find_one({'email': user_email})

#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

#         if user.get("role", "user") != "admin":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Access denied. Admin privileges required."
#             )

#         total_devices = device_data.count_documents({})
#         active_devices = device_data.count_documents({"is_active": True})
#         low_battery_devices = device_data.count_documents({"battery_level": {"$lt": 20}})
#         high_temp_devices = device_data.count_documents({"temperature": {"$gt": 30}})

#         twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
#         recent_devices = device_data.count_documents({"timestamp": {"$gte": twenty_four_hours_ago}})

#         stats = {
#             "total_devices": total_devices,
#             "active_devices": active_devices,
#             "low_battery_warnings": low_battery_devices,
#             "high_temp_alerts": high_temp_devices,
#             "recent_updates": recent_devices
#         }

#         logger.info(f"Device stats calculated for user: {user_email} - Stats: {stats}")

#         return JSONResponse(content={
#             "success": True,
#             "stats": stats
#         })

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Device stats error for user {current_user.get('email', 'unknown')}: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to fetch device statistics"
#         )


# # ────────────────────────────────────────────────────────────────────────────────
# # API: Chart Data
# # ────────────────────────────────────────────────────────────────────────────────
# @router.get('/api/device-data/chart')
# async def get_device_chart_data(current_user: Dict[str, str] = Depends(get_current_user)):
#     """API endpoint to fetch device data for charts (admin only)."""
#     try:
#         user_email = current_user["email"]
#         user = users_data.find_one({'email': user_email})

#         if not user or user.get("role") != "admin":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Access denied. Admin privileges required."
#             )

#         devices_cursor = device_data.find().sort("timestamp", -1).limit(20)

#         temperature_data = []
#         humidity_data = []
#         labels = []

#         for device in reversed(list(devices_cursor)):
#             timestamp = device.get("timestamp", datetime.utcnow())
#             labels.append(timestamp.strftime("%H:%M:%S") if isinstance(timestamp, datetime) else str(timestamp)[-8:])
#             temperature_data.append(device.get("temperature", 0))
#             humidity_data.append(device.get("humidity", 0))

#         chart_data = {
#             "labels": labels,
#             "temperature": temperature_data,
#             "humidity": humidity_data
#         }

#         return JSONResponse(content={
#             "success": True,
#             "chart_data": chart_data
#         })

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Chart data error for user {current_user.get('email', 'unknown')}: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to fetch chart data"
#         )


# #────────────────────────────────────────────────────────────────────────────────
# #API: Simulate Device Data
# #────────────────────────────────────────────────────────────────────────────────
# @router.post('/api/device-data/simulate')
# async def simulate_device_data(current_user: Dict[str, str] = Depends(get_current_user)):
#     """API endpoint to simulate device data for testing (admin only)."""
#     try:
#         user_email = current_user["email"]
#         user = users_data.find_one({'email': user_email})

#         if not user or user.get("role") != "admin":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Access denied. Admin privileges required."
#             )

#         import random

#         sample_devices = [
#             {"device_id": "DEV001", "route_from": "Mumbai", "route_to": "Delhi"},
#             {"device_id": "DEV002", "route_from": "Chennai", "route_to": "Bangalore"},
#             {"device_id": "DEV003", "route_from": "Kolkata", "route_to": "Hyderabad"},
#         ]

#         inserted_count = 0
#         for device_info in sample_devices:
#             sample_data = {
#                 "device_id": device_info["device_id"],
#                 "battery_level": random.randint(10, 100),
#                 "temperature": round(random.uniform(15, 40), 2),
#                 "humidity": round(random.uniform(30, 80), 2),
#                 "route_to": device_info["route_to"],
#                 "route_from": device_info["route_from"],
#                 "timestamp": datetime.utcnow(),
#                 "is_active": random.choice([True, True, True, False])  # 75% active
#             }

#             result = device_data.insert_one(sample_data)
#             if result.inserted_id:
#                 inserted_count += 1

#         logger.info(f"Simulated {inserted_count} device data records")

#         return JSONResponse(content={
#             "success": True,
#             "message": f"Successfully simulated {inserted_count} device data records",
#             "inserted_count": inserted_count
#         })

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Simulate data error: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to simulate device data"
#         )
