import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(os.getenv("DATABASE_URL"))

conn.execute("""
CREATE TABLE IF NOT EXISTS urls (
    short_code TEXT PRIMARY KEY,
    long_url TEXT NOT NULL
);
""")
conn.commit()

def insert_url(short_code: str, long_url: str):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO urls (short_code, long_url) VALUES (%s, %s)", (short_code, long_url))
        conn.commit()

def get_url(short_code: str):
    with conn.cursor() as cur:
        cur.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))
        result = cur.fetchone()
        return result[0] if result else None
