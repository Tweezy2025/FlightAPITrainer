# app/services/discount_service.py

def calculate_discount(promo_code: str, total_amount: float) -> float:
    """
    Расчёт скидки по промокоду.
    """
    if promo_code == "SUMMER2024":
        return min(500, total_amount * 0.1)
    return 0.0
