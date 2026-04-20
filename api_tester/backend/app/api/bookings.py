from fastapi import APIRouter, HTTPException, Depends, status
from api_tester.backend.app.models.booking import (
    BookingCreateSingle,
    BookingCreateBulk,
    BookingUpdate
)
from api_tester.backend.app.services.booking_service import BookingService
from api_tester.backend.app.core.auth_utils import get_current_user

router = APIRouter(
    tags=["Bookings"],
    dependencies=[Depends(get_current_user)]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_booking(data: BookingCreateSingle | BookingCreateBulk):
    try:
        if isinstance(data, BookingCreateSingle):
            return BookingService.create_single_booking(data)
        else:
            return BookingService.create_bulk_bookings(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{reference}")
def get_booking(reference: str):
    booking = BookingService.get_booking(reference)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.patch("/{reference}")
def update_booking(reference: str, data: BookingUpdate):
    try:
        return BookingService.update_booking(reference, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reference}")
def cancel_booking(reference: str):
    try:
        return BookingService.cancel_booking(reference)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
