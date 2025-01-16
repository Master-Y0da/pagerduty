import asyncio, logging
from app import create_app
from flask import g
import threading

from app.config.db import manage_db_connection
from .utils.service_populate import get_services
from .utils.incident_populate import get_incidents
from .utils.teams_populate import get_teams
from .utils.escalation_policies_populate import get_ep

app = create_app()
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)


def db_setup():
    sesionss = manage_db_connection()
    app.db_session = sesionss

async def initial_load():
    with app.app_context():
        await get_services()
        await get_incidents()
        await get_teams()
        await get_ep()

def run_initial_load():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(initial_load())


db_setup()
threading.Thread(target=run_initial_load, daemon=True).start()
