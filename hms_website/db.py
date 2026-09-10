"""
Database connection helper for the Hospital Management System.
Fill in your actual MySQL credentials below.
"""
import mysql.connector
from mysql.connector import pooling

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Ayush@123",          # <-- change this
    "database": "hospital_management_system"  # <-- change this if different
}

# A small connection pool so we don't open/close a raw connection on every request
_pool = pooling.MySQLConnectionPool(
    pool_name="hms_pool",
    pool_size=5,
    **DB_CONFIG
)


def get_connection():
    """Get a connection from the pool. Always close() it when done (or use `with`)."""
    return _pool.get_connection()


def query(sql, params=None, fetchone=False):
    """Run a SELECT and return rows as list of dicts (or a single dict if fetchone=True)."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        result = cursor.fetchone() if fetchone else cursor.fetchall()
        cursor.close()
        return result
    finally:
        conn.close()


def execute(sql, params=None):
    """Run an INSERT/UPDATE/DELETE and commit. Returns lastrowid."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    finally:
        conn.close()
