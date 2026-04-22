from pydantic import BaseModel, Field
from datetime import datetime


class PaymentCreate(BaseModel):
    booking_ref: str
    amount: float
    method: str = Field(..., description="Payment method: card, apple_pay, google_pay")


class Payment(BaseModel):
    payment_id: str
    booking_ref: str
    amount: float
    method: str
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
