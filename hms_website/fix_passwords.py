import os
import mysql.connector
from werkzeug.security import generate_password_hash

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "mysql-304b94a4-hospital-management-system-1545.a.aivencloud.com"),
    port=int(os.getenv("DB_PORT", 16621)),
    user=os.getenv("DB_USER", "avnadmin"),
    password=os.getenv("DB_PASSWORD", "AVNS_aNBqmcF2-ZY3M837-pW"),
    database=os.getenv("DB_NAME", "defaultdb"),
    ssl_disabled=False
)

cursor = conn.cursor()

# Set password for all demo accounts to 'password123'
new_hash = generate_password_hash("password123")

try:
    cursor.execute("UPDATE Users SET password_hash = %s", (new_hash,))
    conn.commit()
    print("All user passwords updated successfully to 'password123'!")
finally:
    cursor.close()
    conn.close()