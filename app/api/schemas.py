from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from domain.enums import RoleEnum, ChannelEnum, OrderStatusEnum

# --- Auth & Users ---
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    lgpd_consent: bool

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: RoleEnum
    class Config:
        orm_mode = True

# --- Products ---
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    class Config:
        orm_mode = True

# --- Orders & Payments ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    channel: ChannelEnum
    items: List[OrderItemCreate] = Field(..., min_items=1)

class OrderResponse(BaseModel):
    id: int
    status: OrderStatusEnum
    total: float
    class Config:
        orm_mode = True

class PaymentMockRequest(BaseModel):
    order_id: int
    amount_paid: float