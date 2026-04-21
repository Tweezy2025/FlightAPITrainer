from api_tester.backend.app.db.mongo import db
from api_tester.backend.app.models.booking import (
    BookingCreateSingle,
    BookingCreateBulk,
    BookingUpdate
)
from bson import ObjectId
import uuid


class BookingService:

    @staticmethod
    def create_single_booking(data: BookingCreateSingle):
        # 1. Находим рейс
        flight = db.flights.find_one({"flight_number": data.flight_number})
        if not flight:
            raise ValueError("Flight not found")

        # 2. Проверяем наличие мест
        if flight["seats_available"] <= 0:
            raise ValueError("Недостаточно мест")


        # 3. Считаем цену
        base_price = flight["price"]
        luggage_fee = 500 if data.has_luggage else 0
        total_price = base_price + luggage_fee

        # 4. Уменьшаем количество мест
        db.flights.update_one(
            {"flight_number": data.flight_number},
            {"$inc": {"seats_available": -1}}
        )

        # 5. Формируем документ
        booking = {
            "booking_ref": str(uuid.uuid4())[:8].upper(),
            "flight_number": data.flight_number,
            "status": "confirmed",
            "total_price": total_price,
            "passengers": [
                {
                    "name": data.passenger,
                    "email": data.email,
                    "phone": data.phone,
                    "has_luggage": data.has_luggage,
                    "seat_preference": None
                }
            ],
        }

        # 6. Сохраняем
        result = db.bookings.insert_one(booking)
        booking["_id"] = str(result.inserted_id)

        return booking

    @staticmethod
    def create_bulk_bookings(data: BookingCreateBulk):
        # 1. Находим рейс
        flight = db.flights.find_one({"flight_number": data.flight_number})
        if not flight:
            raise ValueError("Flight not found")

        passenger_count = len(data.passengers)

        # 2. Проверяем наличие мест
        if flight["seats_available"] < passenger_count:
            raise ValueError("Недостаточно мест")

        base_price = flight["price"]

        bookings_created = []
        total_amount = 0

        # 3. Создаём отдельное бронирование для каждого пассажира
        for p in data.passengers:
            luggage_fee = 500 if p.has_luggage else 0
            price = base_price + luggage_fee
            total_amount += price

            booking = {
                "booking_ref": str(uuid.uuid4())[:8].upper(),
                "flight_number": data.flight_number,
                "status": "confirmed",
                "price": price,
                "passenger": p.name,
                "email": p.email,
                "phone": p.phone,
                "has_luggage": p.has_luggage,
                "seat_preference": p.seat_preference,
                "seat_assigned": p.seat_preference or "auto"
            }

            result = db.bookings.insert_one(booking)
            booking["_id"] = str(result.inserted_id)

            bookings_created.append(booking)

        # 4. Применяем промокод
        discount = 0
        if data.promo_code == "SUMMER2024":
            discount = min(500, total_amount * 0.1)

        total_amount_after = total_amount - discount

        # 5. Уменьшаем количество мест
        db.flights.update_one(
            {"flight_number": data.flight_number},
            {"$inc": {"seats_available": -passenger_count}}
        )

        # 6. Возвращаем агрегированный ответ
        return {
            "success": True,
            "total_bookings_created": passenger_count,
            "total_amount": total_amount_after,
            "discount_applied": discount,
            "bookings": bookings_created
        }

    @staticmethod
    def get_booking(reference: str):
        return db.bookings.find_one({"booking_ref": reference}, {"_id": 0})

    @staticmethod
    def update_booking(reference: str, data: BookingUpdate):
        # 1. Находим бронирование
        booking = db.bookings.find_one({"booking_ref": reference})
        if not booking:
            raise ValueError("Booking not found")

        # 2. Готовим обновляемые поля
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            raise ValueError("No fields to update")

        updated_fields = update_data.copy()

        # 3. Если изменился багаж — пересчитываем total_price
        if "has_luggage" in update_data:
            flight = db.flights.find_one({"flight_number": booking["flight_number"]})
            base_price = flight["price"]
            luggage_fee = 500 if update_data["has_luggage"] else 0
            new_total = base_price + luggage_fee

            update_data["total_price"] = new_total
            updated_fields["total_price"] = new_total

            # обновляем багаж внутри passengers[0]
            booking["passengers"][0]["has_luggage"] = update_data["has_luggage"]

        # 4. Добавляем updated_at
        from datetime import datetime
        update_data["updated_at"] = datetime.utcnow().isoformat()
        updated_fields["updated_at"] = update_data["updated_at"]

        # 5. Обновляем запись
        db.bookings.update_one(
            {"booking_ref": reference},
            {"$set": update_data}
        )

        # 6. Получаем обновлённые данные
        current = db.bookings.find_one({"booking_ref": reference}, {"_id": 0})

        # 7. Возвращаем структуру, которую ожидает тест
        return {
            "success": True,
            "booking_ref": reference,
            "updated_fields": updated_fields,
            "current_data": current
        }

    @staticmethod
    def cancel_booking(reference: str):
        # 1. Находим бронирование
        booking = db.bookings.find_one({"booking_ref": reference})
        if not booking:
            raise ValueError("Booking not found")

        flight_number = booking["flight_number"]

        # 2. Увеличиваем количество мест обратно
        db.flights.update_one(
            {"flight_number": flight_number},
            {"$inc": {"seats_available": 1}}
        )

        # 3. Удаляем бронирование
        db.bookings.delete_one({"booking_ref": reference})

        # 4. Формируем ответ, который ожидает тест
        return {
            "success": True,
            "booking_ref": reference,
            "refund_info": {
                "amount": booking.get("total_price", 0),
                "status": "pending"
            }
        }

