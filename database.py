import psycopg2

from dotenv import load_dotenv
import os
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")
db_table = os.getenv("DB_TABLE")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

def get_db_connection():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port
    )
    return conn

def execute_query(query, params=None, fetch=False):
    """Execute a query and optionally return results"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    
    if fetch:
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    
    conn.commit()
    cur.close()
    conn.close()

