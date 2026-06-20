import streamlit as st
import sqlite3

st.set_page_config(page_title="Legacy Archive", layout="centered")

try:
    conn = sqlite3.connect('dad_media_vault.db')
    cursor = conn.cursor()
    
    # Get all tables, excluding internal ones
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    if not tables:
        st.error("Database empty or no user tables found.")
    else:
        # Use the first user-created table found
        table_name = tables[0][0]
        st.sidebar.write(f"Connected to table: {table_name}")
        
        # --- SHOW US YOUR COLUMN NAMES ---
        # This will print the column names so we can see what they are actually called
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in cursor.fetchall()]
        st.write(f"Columns found in {table_name}: {columns}")
        
        # Fetch data using the columns we now know exist
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        st.write("First row of data:", rows[0] if rows else "No data")

    conn.close()
except Exception as e:
    st.error(f"Error: {e}")
