"""
Your sample CSV data has fake placeholder text in the password_hash column
(e.g. 'hashed_pwd_11'), which won't work for real login since it isn't an
actual password hash.

Run this ONCE after loading your CSVs to set a real, working password for
every user. Every account will then log in with the same password below.
"""
import mysql.connector
from werkzeug.security import generate_password_hash

DEMO_PASSWORD = "password123"   # <-- the password every demo account will use

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ayush@123",              # <-- change this
    database="hospital_management_system"  # <-- change this if different
)
cursor = conn.cursor()

hashed = generate_password_hash(DEMO_PASSWORD)

cursor.execute("UPDATE Users SET password_hash = %s", (hashed,))
conn.commit()

print(f"Done. All users can now log in with the password: {DEMO_PASSWORD}")
print("Example usernames: admin_john (Admin), dr_ravi (Doctor), pat_rahul (Patient)")

cursor.close()
conn.close()
