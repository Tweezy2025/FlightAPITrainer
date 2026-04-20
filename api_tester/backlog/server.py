# server.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import random
import string
import logging
from datetime import datetime
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Отключает экранирование Unicode
CORS(app)

# Настройка логирования — ДО всех маршрутов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['FlightBookDB']

@app.route('/')
def home():
    return jsonify({
        "status": "OK",
        "message": "Сервер бронирования работает",
        "version": "1.0.0",
        "endpoints": {
            "flights": "/api/flights",
            "bookings": "/api/bookings",
            "airlines": "/api/airlines"
        }
    })

def generate_ref():
    """Генерация уникального кода бронирования"""
    chars = string.ascii_uppercase + string.digits
    return "FBT-" + ''.join(random.choice(chars) for _ in range(6))

# --- КОЛЛЕКЦИЯ FLIGHTS (РЕЙСЫ) ---

@app.route('/api/flights', methods=['GET'])
def search_flights():
    departure = request.args.get('departure')
    arrival = request.args.get('arrival')
    date = request.args.get('date')  # Формат YYYY-MM-DD

    query = {}
    if departure:
        query['departure'] = departure
    if arrival:
        query['arrival'] = arrival
    if date:
        # Фильтрация по дате вылета (упрощённо)
        query['departure_time'] = {'$gte': f"{date}T00:00:00Z", '$lt': f"{date}T23:59:59Z"}

    flights = list(db.flights.find(query, {'_id': 0}))
    return jsonify(flights), 200

@app.route('/api/flights', methods=['POST'])
def add_flight():
    data = request.get_json()

    # Базовая валидация
    required_fields = ['flight_number', 'airline', 'departure', 'arrival',
                     'departure_time', 'arrival_time', 'price', 'seats_available']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Отсутствует поле: {field}"}), 400

    flight = {
        "flight_number": data['flight_number'],
        "airline": data['airline'],
        "departure": data['departure'],
        "arrival": data['arrival'],
        "departure_time": data['departure_time'],
        "arrival_time": data['arrival_time'],
        "price": float(data['price']),
        "seats_available": int(data['seats_available']),
        "status": "scheduled"
    }

    result = db.flights.insert_one(flight)
    return jsonify({
        "message": "Рейс добавлен успешно",
        "flight_number": flight['flight_number']
    }), 201

# --- КОЛЛЕКЦИЯ BOOKINGS (БРОНИРОВАНИЯ) ---

@app.route('/api/bookings', methods=['GET'])
def get_all_bookings():
    bookings = list(db.bookings.find({}, {'_id': 0}))
    return jsonify(bookings), 200

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    logger.info("Создание нового бронирования")

    # Определяем, массовый ли это запрос
    is_bulk = 'passengers' in data and isinstance(data['passengers'], list)

    if is_bulk:
        return _create_bulk_bookings(data)
    else:
        return _create_single_booking(data)


def _create_single_booking(data):
    """Логика создания одиночного бронирования"""
    required_fields = ['flight_number', 'passenger', 'email', 'phone']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        logger.warning(f"Отсутствуют обязательные поля: {missing_fields}")
        return jsonify({
            "error": "Отсутствуют обязательные поля",
            "missing_fields": missing_fields
        }), 400

    flight = db.flights.find_one({'flight_number': data['flight_number']})
    if not flight:
        logger.warning(f"Рейс {data['flight_number']} не найден")
        return jsonify({"error": "Рейс не найден"}), 404

    base_price = flight['price']
    luggage_fee = 500 if data.get('has_luggage') else 0
    total_price = base_price + luggage_fee

    booking = {
        "booking_ref": generate_ref(),
        "flight_id": str(flight['_id']),
        "passenger": data['passenger'],
        "email": data['email'],
        "phone": data['phone'],
        "booking_time": datetime.utcnow().isoformat(),
        "total_price": total_price,
        "has_luggage": data.get('has_luggage', False),
        "status": "confirmed"
    }

    db.bookings.insert_one(booking)
    db.flights.update_one(
        {'_id': flight['_id']},
        {'$inc': {'seats_available': -1}}
    )

    return jsonify({
        "booking_ref": booking['booking_ref'],
        "total_price": booking['total_price'],
        "status": booking['status']
    }), 201

def _create_bulk_bookings(data):
    """Логика массового бронирования нескольких пассажиров на один рейс"""
    # Проверка обязательных полей для массового бронирования
    required_fields = ['flight_number', 'passengers']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({
            "error": "Отсутствуют обязательные поля для массового бронирования",
            "missing_fields": missing_fields
        }), 400

    flight_number = data['flight_number']
    passengers = data['passengers']

    # Проверка наличия рейса
    flight = db.flights.find_one({'flight_number': flight_number})
    if not flight:
        return jsonify({"error": "Рейс не найден"}), 404

    available_seats = flight['seats_available']
    requested_seats = len(passengers)

    if requested_seats > available_seats:
        return jsonify({
            "error": "Недостаточно мест на рейсе",
            "available_seats": available_seats,
            "requested_seats": requested_seats
        }), 400

    # Валидация данных каждого пассажира
    validation_errors = []
    for i, passenger in enumerate(passengers):
        passenger_errors = _validate_passenger_data(passenger, i)
        if passenger_errors:
            validation_errors.extend(passenger_errors)

    if validation_errors:
        return jsonify({
            "error": "Ошибки валидации данных пассажиров",
            "details": validation_errors
        }), 400

    # Создание бронирований
    created_bookings = []
    total_amount = 0

    for passenger in passengers:
        base_price = flight['price']
        luggage_fee = 500 if passenger.get('has_luggage') else 0
        total_price = base_price + luggage_fee
        total_amount += total_price

        booking = {
            "booking_ref": generate_ref(),
            "flight_id": str(flight['_id']),
            "passenger": passenger['name'],
            "email": passenger['email'],
            "phone": passenger['phone'],
            "booking_time": datetime.utcnow().isoformat(),
            "total_price": total_price,
            "has_luggage": passenger.get('has_luggage', False),
            "seat_preference": passenger.get('seat_preference'),
            "status": "confirmed"
        }

        db.bookings.insert_one(booking)
        created_bookings.append({
            "booking_ref": booking['booking_ref'],
            "passenger_name": passenger['name'],
            "total_price": total_price,
            "status": "confirmed",
            "seat_assigned": _assign_seat(flight, passenger.get('seat_preference'))
        })

    # Обновление количества мест
    db.flights.update_one(
        {'_id': flight['_id']},
        {'$inc': {'seats_available': -requested_seats}}
    )

    # Применение промокода, если есть
    discount_applied = 0
    if 'promo_code' in data:
        discount = _calculate_discount(data['promo_code'], total_amount)
        total_amount -= discount
        discount_applied = discount

    response_data = {
        "success": True,
        "message": "Массовое бронирование выполнено успешно",
        "flight_number": flight_number,
        "total_bookings_created": len(created_bookings),
        "total_amount": total_amount,
        "discount_applied": discount_applied,
        "bookings": created_bookings,
        "seats_remaining": available_seats - requested_seats,
        "timestamp": datetime.utcnow().isoformat()
    }

    return jsonify(response_data), 200

def _validate_passenger_data(passenger, index):
    errors = []
    required = {
        'name': 'Имя пассажира обязательно',
        'email': 'Email обязателен',
        'phone': 'Телефон обязателен'
    }
    for field, message in required.items():
        if field not in passenger or not passenger[field]:
            errors.append(f"Пассажир {index + 1}: {message}")
    # Дополнительная проверка email
    if 'email' in passenger and passenger['email']:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, passenger['email']):
            errors.append(f"Пассажир {index + 1}: Некорректный формат email")
    return errors


def _assign_seat(flight, preference=None):
    """Назначение места с учётом предпочтений"""
    # Здесь должна быть логика назначения мест
    # Для примера возвращаем случайное место
    import random
    rows = range(1, 20)
    seats = ['A', 'B', 'C', 'D', 'E', 'F']
    if preference == 'window':
        seats = ['A', 'F']
    elif preference == 'aisle':
        seats = ['B', 'E']
    return f"{random.choice(rows)}{random.choice(seats)}"

def _calculate_discount(promo_code, total_amount):
    """Расчёт скидки по промокоду"""
    # Пример простой логики расчёта скидки
    if promo_code == "SUMMER2024":
        return min(500, total_amount * 0.1)  # 10 %, но не более 500 руб.
    return 0

@app.route('/api/bookings/<ref>', methods=['GET'])
def get_booking(ref):
    booking = db.bookings.find_one({'booking_ref': ref}, {'_id': 0})
    if not booking:
        return jsonify({"error": "Бронирование не найдено"}), 404
    return jsonify(booking), 200

@app.route('/api/bookings/<ref>', methods=['PUT'])
def update_booking_put(ref):
    data = request.get_json()
    update_fields = {}

    if 'passenger' in data:
        update_fields['passenger'] = data['passenger']
    if 'phone' in data:
        update_fields['phone'] = data['phone']
    if 'has_luggage' in data:
        # Пересчитываем цену при изменении багажа
        flight = db.flights.find_one({'flight_id': data.get('flight_id')})
        base_price = flight['price'] if flight else 0
        luggage_fee = 500 if data['has_luggage'] else 0
        update_fields['total_price'] = base_price + luggage_fee
        update_fields['has_luggage'] = data['has_luggage']

    result = db.bookings.update_one(
        {'booking_ref': ref},
        {'$set': update_fields}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Бронирование не обновлено"}), 400

    updated_booking = db.bookings.find_one({'booking_ref': ref}, {'_id': 0})
    return jsonify(updated_booking), 200

@app.route('/api/bookings/<ref>', methods=['PATCH'])
def update_booking_patch(ref):
    logger.info(f"=== Начало обработки обновления бронирования: {ref} ===")

    # Поиск бронирования
    booking = db.bookings.find_one({'booking_ref': ref})
    if not booking:
        logger.warning(f"Бронирование {ref} не найдено в базе данных")
        return jsonify({"error": "Бронирование не найдено"}), 404

    logger.info(f"Найдено бронирование: пассажир {booking['passenger']}")

    # Получаем данные из запроса
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "Нет данных для обновления"}), 400

    # Формируем поля для обновления
    update_fields = {}

    if 'passenger' in update_data:
        update_fields['passenger'] = update_data['passenger']

    if 'email' in update_data:
        update_fields['email'] = update_data['email']

    if 'phone' in update_data:
        update_fields['phone'] = update_data['phone']

    if 'has_luggage' in update_data:
        # Пересчитываем стоимость, если изменился багаж
        base_price = 5000
        luggage_fee = 1000 if update_data['has_luggage'] else 0
        update_fields['total_price'] = base_price + luggage_fee
        update_fields['has_luggage'] = update_data['has_luggage']

    if 'status' in update_data:
        update_fields['status'] = update_data['status']

    # Добавляем время обновления
    update_fields['updated_at'] = datetime.utcnow().isoformat()

    if not update_fields:
        return jsonify({"error": "Нет полей для обновления"}), 400

    # Обновляем бронирование
    result = db.bookings.update_one(
        {'booking_ref': ref},
        {'$set': update_fields}
    )

    if result.modified_count == 0:
        logger.warning(f"Бронирование {ref} не было обновлено (возможно, данные не изменились)")
        return jsonify({
            "message": "Данные не были изменены или бронирование не найдено"
        }), 200

    # Получаем обновлённое бронирование
    updated_booking = db.bookings.find_one({'booking_ref': ref})

    response_data = {
        "success": True,
        "message": "Бронирование успешно обновлено",
        "booking_ref": ref,
        "updated_fields": list(update_fields.keys()),
        "current_data": {
            "passenger": updated_booking['passenger'],
            "email": updated_booking.get('email', ''),
            "phone": updated_booking.get('phone', ''),
            "has_luggage": updated_booking['has_luggage'],
            "total_price": updated_booking['total_price'],
            "status": updated_booking['status'],
            "updated_at": updated_booking['updated_at']
        },
        "timestamp": datetime.utcnow().isoformat()
    }

    logger.info(f"Бронирование {ref} успешно обновлено: {update_fields}")
    return jsonify(response_data), 200


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/api/bookings/<ref>', methods=['DELETE'])
def cancel_booking(ref):
    logger.info(f"Начало обработки отмены бронирования: {ref}")

    # Поиск бронирования
    booking = db.bookings.find_one({'booking_ref': ref})
    if not booking:
        logger.warning(f"Бронирование не найдено: {ref}")
        return jsonify({"error": "Бронирование не найдено"}), 404

    logger.info(f"Найдено бронирование: {booking['passenger']}, рейс: {booking.get('flight_id')}")

    try:
        flight_id = ObjectId(booking['flight_id'])
        logger.info(f"Преобразован flight_id: {flight_id}")
    except Exception as e:
        logger.error(f"Ошибка преобразования flight_id: {e}")
        return jsonify({"error": "Некорректный ID рейса"}), 500

    # Получаем текущий статус рейса перед обновлением
    flight = db.flights.find_one({'_id': flight_id})
    if flight:
        logger.info(f"Рейс перед обновлением: {flight['flight_number']}, мест доступно: {flight['seats_available']}")

    # Обновляем количество мест на рейсе
    result = db.flights.update_one(
        {'_id': flight_id},
        {'$inc': {'seats_available': 1}}
    )

    if result.modified_count == 0:
        logger.error(f"Не удалось обновить рейс с ID: {flight_id}")
        return jsonify({
            "error": "Не удалось обновить количество мест на рейсе"
        }), 500
    else:
        logger.info(f"Количество мест на рейсе обновлено (увеличилось на 1)")

    # Удаляем бронирование
    db.bookings.delete_one({'booking_ref': ref})
    logger.info(f"Бронирование {ref} успешно удалено из базы данных")

    # Формируем ответ
    response_data = {
        "success": True,
        "message": "Бронирование успешно отменено",
        "booking_ref": ref,
        "passenger_name": booking['passenger'],
        "refund_info": {
            "amount": booking['total_price'],
            "currency": "RUB",
            "status": "pending"
        },
        "timestamp": datetime.utcnow().isoformat(),
        "action": "cancellation"
    }

    logger.info(f"Возврат ответа клиенту: {response_data}")
    return jsonify(response_data), 200


# --- КОЛЛЕКЦИЯ AIRLINES (АВИАКОМПАНИИ) ---

@app.route('/api/airlines', methods=['GET'])
def get_airlines():
    airlines = list(db.airlines.find({}, {'_id': 0}))
    return jsonify(airlines), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

@app.route('/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'route': str(rule)
        })
    return jsonify(routes)


