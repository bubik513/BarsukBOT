import asyncio
from app.utils.database import init_db, engine
from app.config import Config


async def test_database():
    print("Тестирование подключения к базе данных...")
    print(f"DB_HOST: {Config.DB_HOST}")
    print(f"DB_NAME: {Config.DB_NAME}")
    print(f"DB_USER: {Config.DB_USER}")

    try:
        # Пробуем создать таблицы
        await init_db()
        print("✅ Таблицы успешно созданы!")

        # Проверяем подключение
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            print("✅ Подключение к базе данных работает!")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\nПроверьте:")
        print("1. PostgreSQL запущен?")
        print("2. Правильный ли пароль в .env?")
        print("3. Существует ли база данных barsuk_db?")


if __name__ == "__main__":
    asyncio.run(test_database())