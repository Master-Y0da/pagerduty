import asyncio
from app import create_app
from flask import g
from .utils.service_populate import get_services
from .utils.incident_populate import get_incidents
from .utils.teams_populate import get_teams
from app.config.db import manage_db_connection
import threading

app = create_app()

def db_setup():
    sesionss = manage_db_connection()
    app.db_session = sesionss

async def initial_load():
    with app.app_context():
        await get_services()
        await get_incidents()
        await get_teams()

def run_initial_load():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(initial_load())


db_setup()
threading.Thread(target=run_initial_load, daemon=True).start()
