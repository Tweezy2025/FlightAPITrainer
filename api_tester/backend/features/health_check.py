from api_tester.backend.app.config import mongo
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def health_check():
    logger.info("🔎 Запуск проверки работоспособности системы...")

    # 1. Проверка подключения к БД
    try:
        mongo.db.command("ping")
        logger.info("✅ Подключение к MongoDB: ОК")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к MongoDB: {e}")
        return False

    # 2. Проверка базы данных
    db_name = mongo.db.name
    logger.info(f"🛰️ Используемая база данных: {db_name}")

    # 3. Проверка коллекции
    collections = mongo.db.list_collection_names()
    if "users" in collections:
        logger.info("✅ Коллекция 'users' существует")
    else:
        logger.warning("⚠️ Коллекция 'users' не найдена")

    # 4. Проверка количества документов
    count = mongo.db.users.count_documents({})
    logger.info(f"📊 Всего пользователей в БД: {count}")

    if count == 0:
        logger.warning("⚠️ База данных пуста. Рекомендуется запустить миграцию.")

    # 5. Тестовый запрос
    try:
        test_user = {"id": 999, "name": "HealthCheck", "email": "health@check.com"}
        result = mongo.db.users.insert_one(test_user)
        logger.info(f"✅ Тестовый пользователь создан с ID: {result.inserted_id}")

        # Удаляем тестовый документ
        mongo.db.users.delete_one({"id": 999})
        logger.info("🗑️ Тестовый пользователь удалён")
    except Exception as e:
        logger.error(f"❌ Ошибка при тестовой операции: {e}")
        return False

    logger.info("🎉 Все проверки пройдены успешно!")
    return True

if __name__ == '__main__':
    health_check()
