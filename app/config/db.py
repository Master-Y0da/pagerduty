from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DB_SCHEMAS={
    "services": "services",
    "incidents": "incidents",
    "teams": "teams"
}

Bases = { key : declarative_base() for key in DB_SCHEMAS.keys() }

def manage_db_connection():

    def get_db_url():
        return f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('MYSQL_ROOT_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
    
    def generate_engine(DATABASE_URL):
         return {
            schema_name: create_engine(f"{DATABASE_URL}", echo=True)
            for key, schema_name in DB_SCHEMAS.items() }
    
    def generate_sessions(engines):
        return {
            key: sessionmaker(bind=engine, expire_on_commit=False)
            for key, engine in engines.items() }
    
    def generate_schemas(engine, schema,base):
        with engine.begin() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        base.metadata.create_all(bind=engine)

    DATABASE_URL = get_db_url()
    engines = generate_engine(DATABASE_URL)


    for key,engine in engines.items():
        try:
            generate_schemas(engine, key, Bases[key])
            print(f"Schema {key} created")
        except Exception as e:
            print(f"Error creating schema {key}")
            print(e)
            raise e

    current_session = generate_sessions(engines)
    return current_session
        