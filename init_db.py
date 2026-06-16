import sqlite3

conn = sqlite3.connect("local_food_wastage.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

conn.commit()
conn.close()
