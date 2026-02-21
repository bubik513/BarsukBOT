import asyncio
from app.utils.database import init_db

async def recreate():
    print("Пересоздание базы данных с новыми типами...")
    await init_db()
    print("✅ Готово!")

if __name__ == "__main__":
    asyncio.run(recreate())