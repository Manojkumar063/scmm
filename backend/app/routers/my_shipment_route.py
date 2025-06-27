from fastapi import Request, Depends, APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from io import StringIO
from typing import Dict, List
import csv
import logging

from backend.app.database import users_data, shipment_data
from .jwt_handler import get_current_user
from .cookie_handler import delete_access_token_cookie

# Set up router
logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="backend/app/templates")

# ─────────────────────────────────────────────────────────────
# 1. SHOW SHIPMENTS
# ─────────────────────────────────────────────────────────────
@router.get('/shipments')
def my_shipment(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """Display user shipments (admin sees all, users see their own)."""
    try:
        user_email = current_user["email"]
        user = users_data.find_one({"email": user_email})
        
        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        username = user.get("username", "Unknown User")
        role = user.get("role", "user")

        # Fetch shipments based on role
        if role == "admin":
            shipments_cursor = shipment_data.find()
        else:
            shipments_cursor = shipment_data.find({"user_id": user_email})

        shipments: List[Dict] = []
        for doc in shipments_cursor:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            shipments.append(doc)

        return templates.TemplateResponse(
            'my_shipment.html',
            {
                'request': request,
                'shipments': shipments,
                'role': role,
                'username': username
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"My shipment error for user {user_email}: {str(e)}")
        response = templates.TemplateResponse(
            'login.html',
            {
                'request': request,
                'message': "An error occurred. Please login again."
            }
        )
        delete_access_token_cookie(response)
        return response

# ─────────────────────────────────────────────────────────────
# 2. EXPORT SHIPMENTS AS CSV
# ─────────────────────────────────────────────────────────────
@router.get("/shipments/export")
def export_shipments_csv(current_user: Dict[str, str] = Depends(get_current_user)):
    """
    Export shipments that the current user is allowed to see.
    Admins get all shipments; regular users get only their own.
    Returns a streamed CSV file download.
    """
    try:
        user_email = current_user["email"]
        user = users_data.find_one({"email": user_email})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        role = user.get("role", "user")

        # Fetch shipments based on role
        if role == "admin":
            shipments_cursor = shipment_data.find()
        else:
            shipments_cursor = shipment_data.find({"user_id": user_email})

        # Prepare CSV output
        stream = StringIO()
        writer = csv.writer(stream)

        # CSV Header
        writer.writerow([
            "Shipment Number", "Route", "Device ID", "PO Number", "NDC Number",
            "Goods Number", "Container Number", "Goods Type", "Expected Delivery",
            "Delivery Number", "Batch ID", "Description", "User Email", "Created At"
        ])

        # CSV Rows
        for doc in shipments_cursor:
            writer.writerow([
                doc.get("shipment_number", ""),
                doc.get("route", ""),
                doc.get("device_id", ""),
                doc.get("po_number", ""),
                doc.get("ndc_number", ""),
                doc.get("goods_number", ""),
                doc.get("container_number", ""),
                doc.get("goods_type", ""),
                doc.get("expected_delivery_date", ""),
                doc.get("delivery_number", ""),
                doc.get("batch_id", ""),
                doc.get("shipment_description", ""),
                doc.get("user_id", ""),
                doc.get("created_at", "").strftime("%d-%m-%Y %H:%M")
                if doc.get("created_at") else ""
            ])

        stream.seek(0)
        return StreamingResponse(
            stream,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=shipments.csv"}
        )

    except Exception as e:
        logger.error(f"Export error for user {current_user['email']}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export shipments"
        )

# ─────────────────────────────────────────────────────────────
# 3. DELETE SHIPMENT
# ─────────────────────────────────────────────────────────────
@router.delete("/api/shipments/{shipment_number}")
def delete_shipment(shipment_number: str, current_user: Dict[str, str] = Depends(get_current_user)):
    """
    Delete a shipment by shipment number. Only admins can perform this action.
    """
    try:
        user_email = current_user["email"]
        user = users_data.find_one({"email": user_email})

        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        role = user.get("role", "user")
        if role != "admin":
            logger.warning(f"Unauthorized deletion attempt by {user_email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can delete shipments"
            )

        # Find and delete the shipment
        result = shipment_data.delete_one({"shipment_number": shipment_number})
        if result.deleted_count == 0:
            logger.warning(f"Shipment not found: {shipment_number}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )

        logger.info(f"Shipment {shipment_number} deleted by {user_email}")
        return {"message": "Shipment deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete shipment error for {shipment_number} by {user_email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete shipment"
        )
# ─────────────────────────────────────────────────────────────
@router.get('/dashboard')
def dashboard(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """Display the dashboard with active users and recent shipments."""
    try:
        user_email = current_user["email"]
        user = users_data.find_one({"email": user_email})
        
        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        username = user.get("username", "Unknown User")
        role = user.get("role", "user")

        # Fetch users (all for admins, own for users)
        if role == "admin":
            users_cursor = users_data.find()
        else:
            users_cursor = users_data.find({"email": user_email})

        users: List[Dict] = []
        for doc in users_cursor:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            users.append(doc)

        # Fetch recent shipments (last 5)
        if role == "admin":
            shipments_cursor = shipment_data.find().sort("created_at", -1).limit(5)
        else:
            shipments_cursor = shipment_data.find({"user_id": user_email}).sort("created_at", -1).limit(5)

        recent_shipments: List[Dict] = []
        for doc in shipments_cursor:
            doc["_id"] = str(doc["_id"])
            recent_shipments.append(doc)

        return templates.TemplateResponse(
            'dashboard.html',
            {
                'request': request,
                'users': users,
                'recent_shipments': recent_shipments,
                'role': role,
                'username': username
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dashboard error for user {user_email}: {str(e)}")
        response = templates.TemplateResponse(
            'login.html',
            {
                'request': request,
                'message': "An error occurred. Please login again."
            }
        )
        delete_access_token_cookie(response)
        return response