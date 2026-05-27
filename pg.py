from dotenv import load_dotenv
import psycopg2 as pg
import os

load_dotenv()

def connect():
    return pg.connect(
        database=os.getenv("PG_NAME"),
        user=os.getenv("PG_USER"),
        host=os.getenv("PG_HOST"),
        password=os.getenv("PG_PASS")
    )