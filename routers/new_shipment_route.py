from fastapi import Request, Form, Depends, APIRouter, HTTPException, status
from fastapi.templating import Jinja2Templates
from database import users_data, shipment_data
from datetime import datetime
import logging
from typing import Dict

from .jwt_handler import get_current_user
from .cookie_handler import delete_access_token_cookie
from models import Shipment

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/new_shipment')
def create_shipment_get(request: Request, current_user: Dict[str, str] = Depends(get_current_user)):
    """Display new shipment creation form."""
    try:
        user_email = current_user['email']
        user = users_data.find_one({'email': user_email})
        
        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        role = user.get("role", "user")
        username = user.get("username", "Unknown User")
        today_date = datetime.now().strftime('%Y-%m-%d')

        return templates.TemplateResponse(
            'create-shipment.html',
            {
                'request': request,
                'role': role,
                'today_date': today_date,
                'username': username
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"New shipment GET error for user {current_user.get('email', 'unknown')}: {str(e)}")
        response = templates.TemplateResponse(
            'login.html',
            {'request': request, 'message': "An error occurred. Please login again."}
        )
        delete_access_token_cookie(response)
        return response


# Modify the create_shipment_post function to return JSON:
@router.post('/new_shipment')
async def create_shipment_post(
    request: Request,
    current_user: Dict[str, str] = Depends(get_current_user),
    shipmentNumber: str = Form(..., description="Unique shipment number"),
    routeDetails: str = Form(..., min_length=1, description="Shipment route"),
    deviceId: str = Form(..., description="Device ID"),
    poNumber: str = Form(..., description="Purchase order number"),
    ndcNumber: str = Form(..., description="NDC number"),
    serialNumberOfGoods: str = Form(..., description="Goods serial number"),
    containerNumber: str = Form(..., description="Container number"),
    goodsType: str = Form(..., min_length=1, description="Type of goods"),
    expectedDeliveryDate: str = Form(..., description="Expected delivery date"),
    deliveryNumber: str = Form(..., description="Unique delivery number"),
    batchId: str = Form(..., description="Batch ID"),
    shipmentDescription: str = Form(..., description="Shipment description")
):
    """Create new shipment with validation."""
    try:
        # print(f"Creating shipment with data: {shipmentNumber}, {routeDetails}, {deviceId}, {poNumber}, {ndcNumber}, {serialNumberOfGoods}, {containerNumber}, {goodsType}, {expectedDeliveryDate}, {deliveryNumber}, {batchId}, {shipmentDescription}")
        user_email = current_user['email']
        user = users_data.find_one({'email': user_email})
        # print(f"Current user: {user_email}")
        if not user:
            logger.warning(f"User not found: {user_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        # print(f"User found: {user}")
        role = user.get("role", "user")
        username = user.get("username", "Unknown User")
        # print(f"User role: {role}, username: {username}")
        # Check for duplicate shipment number
        if shipment_data.find_one({"shipment_number": shipmentNumber}):
            return templates.TemplateResponse(
                'create-shipment.html',
                {
                    'request': request,
                    'message': f"The shipment number '{shipmentNumber}' already exists.",
                    'role': role,
                    'username': username
                }
            )
        # print(f"Shipment number '{shipmentNumber}' is unique.")
        # Check for duplicate delivery number
        if shipment_data.find_one({"delivery_number": deliveryNumber}):
            return templates.TemplateResponse(
                'create-shipment.html',
                {
                    'request': request,
                    'message': f"The delivery number '{deliveryNumber}' already exists.",
                    'role': role,
                    'username': username
                }
            )
        # print(f"Delivery number '{deliveryNumber}' is unique.")
        # Create shipment document
        shipment_doc = Shipment(
            shipment_number=shipmentNumber,
            route=routeDetails.strip(),
            device_id=deviceId,
            po_number=poNumber,
            ndc_number=ndcNumber,
            goods_number=serialNumberOfGoods,
            container_number=containerNumber,
            goods_type=goodsType.strip(),
            expected_delivery_date=expectedDeliveryDate,
            delivery_number=deliveryNumber,
            batch_id=batchId,
            shipment_description=shipmentDescription.strip(),
            user_id=user_email,
            created_at=datetime.now()
        )
        # print(f"Shipment document created: {shipment_doc}")
        # Insert shipment
        result = shipment_data.insert_one(shipment_doc.dict())

        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create shipment"
            )

        logger.info(f"Shipment created successfully by {user_email}: {shipmentNumber}")
        return {"message": "Shipment created successfully", "shipment_id": str(result.inserted_id)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"New shipment POST error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )