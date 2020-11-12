import os
from databases import Database


async def connect_pg():
    database = Database(os.environ.get("POSTGRESQL_URL"))
    await database.connect()

    return database
