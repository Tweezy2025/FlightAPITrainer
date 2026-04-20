# app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"

# Создаём директорию для логов, если её нет
os.makedirs(LOG_DIR, exist_ok=True)

# Формат логов
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(funcName)s:%(lineno)d | %(message)s"
)

# Настройка логгера
logger = logging.getLogger("flight_app")
logger.setLevel(logging.INFO)

# Консольный вывод
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Ротация логов (5 MB, 5 файлов)
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, LOG_FILE),
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Подключаем хендлеры
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name: str):
    """
    Возвращает именованный логгер для модулей.
    """
    return logger.getChild(name)
