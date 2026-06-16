import streamlit as st
import pandas as pd
import sqlite3
from db_connection import get_connection

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("local_food_wastage.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS receivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT,
    quantity INTEGER,
    expiry_date TEXT,
    provider_id INTEGER,
    location TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER,
    receiver_id INTEGER,
    status TEXT,
    claim_date TEXT
)
""")

conn.commit()

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(page_title="Food Wastage Management", layout="wide")

conn = get_connection()

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Providers", "Receivers", "Claims", "Manage Food", "SQL Analysis"]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("🍲 Local Food Wastage Management System")

    providers = pd.read_sql("SELECT COUNT(*) as total FROM providers", conn)
    receivers = pd.read_sql("SELECT COUNT(*) as total FROM receivers", conn)
    food = pd.read_sql("SELECT COUNT(*) as total FROM food", conn)
    claims = pd.read_sql("SELECT COUNT(*) as total FROM claims", conn)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Providers", providers.iloc[0, 0])
    c2.metric("Receivers", receivers.iloc[0, 0])
    c3.metric("Food Listings", food.iloc[0, 0])
    c4.metric("Claims", claims.iloc[0, 0])

# ---------------- PROVIDERS ----------------
elif page == "Providers":

    st.title("Providers")

    df = pd.read_sql("SELECT * FROM providers", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- RECEIVERS ----------------
elif page == "Receivers":

    st.title("Receivers")

    df = pd.read_sql("SELECT * FROM receivers", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- CLAIMS ----------------
elif page == "Claims":

    st.title("Claims")

    df = pd.read_sql("SELECT * FROM claims", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- MANAGE FOOD ----------------
elif page == "Manage Food":

    st.title("Manage Food")

    action = st.selectbox("Action", ["View", "Add"])

    if action == "View":
        df = pd.read_sql("SELECT * FROM food", conn)
        st.dataframe(df, use_container_width=True)

    elif action == "Add":

        provider = st.number_input("Provider ID", step=1)
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", step=1)

        if st.button("Add Food"):

            cur = conn.cursor()
            cur.execute("""
            INSERT INTO food (provider_id, food_name, quantity)
            VALUES (?, ?, ?)
            """, (provider, food_name, quantity))

            conn.commit()
            st.success("Food Added Successfully")

# ---------------- SQL ANALYSIS ----------------
elif page == "SQL Analysis":

    st.title("SQL Analysis")

    query = st.selectbox("Choose Query", [
        "Total Food Available",
        "Top Provider",
        "Claim Status"
    ])

    if query == "Total Food Available":
        sql = "SELECT SUM(quantity) AS total FROM food"

    elif query == "Top Provider":
        sql = """
        SELECT provider_id, SUM(quantity) AS total
        FROM food
        GROUP BY provider_id
        ORDER BY total DESC
        """

    elif query == "Claim Status":
        sql = """
        SELECT status, COUNT(*) AS total
        FROM claims
        GROUP BY status
        """

    df = pd.read_sql(sql, conn)
    st.dataframe(df, use_container_width=True)
