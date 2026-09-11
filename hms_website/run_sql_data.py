import os
import mysql.connector

# Fetch database credentials
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql-304b94a4-hospital-management-system-1545.a.aivencloud.com"),
    "port": int(os.getenv("DB_PORT", 16621)),
    "user": os.getenv("DB_USER", "avnadmin"),
    "password": os.getenv("DB_PASSWORD", "AVNS_aNBqmcF2-ZY3M837-pW"),
    "database": os.getenv("DB_NAME", "defaultdb"),
    "ssl_disabled": False
}

def execute_sql_file(filename):
    print("Connecting to Aiven MySQL database...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    with open(filename, 'r', encoding='utf-8') as sql_file:
        content = sql_file.read()

    # Split SQL script into individual statements
    statements = [stmt.strip() for stmt in content.split(';') if stmt.strip()]

    print(f"Executing {len(statements)} statements...")
    for statement in statements:
        # Ignore USE statement as database name is already set in connection
        if statement.upper().startswith("USE "):
            continue
        try:
            cursor.execute(statement)
        except mysql.connector.Error as err:
            print(f"Error executing statement:\n{statement[:100]}...\nDetails: {err}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Data insertion completed successfully!")

if __name__ == "__main__":
    execute_sql_file("Data_insertion_query.sql")