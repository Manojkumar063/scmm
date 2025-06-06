from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal


class Users(BaseModel):
    """User model with validation."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)


    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Shipment(BaseModel):
    shipment_number: str = Field(..., min_length=1, max_length=50)
    container_number: str = Field(..., min_length=1, max_length=50)
    goods_number: str = Field(..., min_length=1, max_length=50)
    route: str = Field(..., min_length=1, max_length=200)
    goods_type: str = Field(..., min_length=1, max_length=100)
    device_id: str = Field(..., min_length=1, max_length=50)
    expected_delivery_date: str
    po_number: str = Field(..., min_length=1, max_length=50)
    delivery_number: str = Field(..., min_length=1, max_length=50)
    ndc_number: str = Field(..., min_length=1, max_length=50)
    batch_id: str = Field(..., min_length=1, max_length=50)
    shipment_description: Optional[str] = Field(default=None, max_length=500)
    user_id: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="pending")


    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DeviceData(BaseModel):
    """Device data model with validation."""
    device_id: int = Field(..., gt=0)
    battery_level: float = Field(..., ge=0.0, le=100.0)
    temperature: float = Field(..., ge=-50.0, le=100.0)
    route_to: str = Field(..., min_length=1, max_length=100)
    route_from: str = Field(..., min_length=1, max_length=100)
    timestamp: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Keep the old model name for backward compatibility
Devicedata = DeviceData