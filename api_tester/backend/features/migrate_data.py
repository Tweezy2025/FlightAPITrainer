from api_tester.backend.app.config import mongo
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrate_data():
    # Данные для миграции
    initial_users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]

    try:
        # Получаем коллекцию
        users_collection = mongo.db.users

        # Очищаем коллекцию перед миграцией (опционально)
        delete_result = users_collection.delete_many({})
        logger.info(f"Удалено документов перед миграцией: {delete_result.deleted_count}")

        # Вставляем данные
        result = users_collection.insert_many(initial_users)
        logger.info(f"Успешно вставлено документов: {len(result.inserted_ids)}")
        logger.info(f"ID вставленных документов: {result.inserted_ids}")

        # Дополнительная проверка: считаем документы в коллекции
        count_after = users_collection.count_documents({})
        logger.info(f"Всего документов в коллекции после миграции: {count_after}")

        # Проверка: читаем все документы
        all_users = list(users_collection.find({}, {"_id": 0}))
        logger.info(f"Текущие данные в коллекции: {all_users}")

        if count_after == len(initial_users):
            logger.info("✅ Миграция данных завершена успешно!")
            return True
        else:
            logger.error("❌ Количество документов не соответствует ожидаемому!")
            return False

    except Exception as e:
        logger.error(f"❌ Ошибка во время миграции: {e}")
        return False

if __name__ == '__main__':
    success = migrate_data()
    if success:
        print("\n🎉 Миграция данных прошла успешно!")
    else:
        print("\n💥 Миграция данных не удалась. Проверьте логи выше.")
