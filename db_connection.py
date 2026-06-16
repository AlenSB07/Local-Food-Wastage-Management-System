import sqlite3

def get_connection():
    conn = sqlite3.connect("local_food_wastage.db")
    return conn
