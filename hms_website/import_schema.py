import os
import mysql.connector

# Aiven Connection Credentials
DB_HOST = os.getenv("DB_HOST", "mysql-304b94a4-hospital-management-system-1545.a.aivencloud.com")
DB_PORT = int(os.getenv("DB_PORT", 16621))
DB_USER = os.getenv("DB_USER", "avnadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "AVNS_aNBqmcF2-ZY3M837-pW")
DB_NAME = os.getenv("DB_NAME", "defaultdb")

try:
    # Connect to Aiven MySQL
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl_disabled=False  # Required for Aiven SSL
    )

    cursor = conn.cursor()

    # Read and execute your local schema.sql file
    schema_file = 'schema.sql'  # Replace with your actual .sql file name
    with open(schema_file, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            command = command.strip()
            if command:
                cursor.execute(command)

    conn.commit()
    print("Database schema imported successfully to Aiven!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")