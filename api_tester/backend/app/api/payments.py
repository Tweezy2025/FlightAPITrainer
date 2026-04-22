from fastapi import APIRouter, HTTPException

from ..models.payment import PaymentCreate, Payment
from ..services.payment_service import PaymentService

router = APIRouter(tags=["Payments"])



@router.post("/", response_model=Payment)
def create_payment(payload: PaymentCreate):
    return PaymentService.create_payment(payload)


@router.get("/{payment_id}", response_model=Payment)
def get_payment(payment_id: str):
    payment = PaymentService.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.delete("/{payment_id}", response_model=Payment)
def cancel_payment(payment_id: str):
    payment = PaymentService.cancel_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
