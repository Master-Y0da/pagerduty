from peewee_async import AsyncMySQLDatabase, Manager
import os


DB_CONFIG = {
    'database': os.environ.get('MYSQL_DATABASE'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'host': os.environ.get('MYSQL_HOST'),
    'port': int(os.environ.get('MYSQL_PORT')),
}


database = AsyncMySQLDatabase(**DB_CONFIG)
db_session = Manager(database)


async def create_service_table():
    async with database:
        await database.create_tables([Service])