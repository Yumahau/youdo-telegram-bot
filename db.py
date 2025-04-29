import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS executors (user_id INTEGER PRIMARY KEY)""")
        await db.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, description TEXT)""")
        await db.commit()

async def add_executor(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO executors (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def get_executors():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT user_id FROM executors")
        return [row[0] for row in await cursor.fetchall()]

async def add_task(user_id: int, username: str, title: str, description: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO tasks (user_id, username, title, description) VALUES (?, ?, ?, ?)", 
                         (user_id, username, title, description))
        await db.commit()
