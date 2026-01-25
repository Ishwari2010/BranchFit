import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/system.db")

with open("database/schema.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully")
