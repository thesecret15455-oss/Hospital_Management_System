import os
import mysql.connector
from mysql.connector import pooling

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql-304b94a4-hospital-management-system-1545.a.aivencloud.com"),
    "port": int(os.getenv("DB_PORT", 16621)),
    "user": os.getenv("DB_USER", "avnadmin"),
    "password": os.getenv("DB_PASSWORD", "AVNS_aNBqmcF2-ZY3M837-pW"),
    "database": os.getenv("DB_NAME", "defaultdb"),
    "ssl_disabled": False
}

_pool = pooling.MySQLConnectionPool(
    pool_name="hms_pool",
    pool_size=5,
    **DB_CONFIG
)

def get_connection():
    return _pool.get_connection()

def query(sql, params=None, fetchone=False):
    """Helper function to execute SELECT queries and return dictionary records."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params or ())
        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def execute(sql, params=None):
    """Helper function to execute INSERT/UPDATE/DELETE queries."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or ())
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()