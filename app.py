import streamlit as st
import sqlite3

st.set_page_config(page_title="Legacy Archive", layout="centered")

try:
    conn = sqlite3.connect('dad_media_vault.db')
    cursor = conn.cursor()
    # Find the table name automatically
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if not tables:
        st.error("Database is empty. No tables found.")
    else:
        table_name = tables[0][0]
        st.sidebar.write(f"Connected to table: {table_name}")
        
        # Query using the detected table name
        cursor.execute(f"SELECT year, title, filename, description, metric_label, metric_value FROM {table_name}")
        rows = cursor.fetchall()
        
        st.markdown("<h1 style='text-align:center;'>The Legacy Archive</h1>", unsafe_allow_html=True)
        for row in rows:
            st.write(row) # This will display your data
            
    conn.close()
except Exception as e:
    st.error(f"Error: {e}")
