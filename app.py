import streamlit as st
import sqlite3

# Page setup
st.set_page_config(page_title="Legacy Archive", layout="centered")

# CSS
st.markdown("""
    <style>
        .stApp { background-color: #050505; color: #fff; font-family: sans-serif; }
        .card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .year { color: #d4af37; font-size: 0.6rem; font-weight: 700; text-transform: uppercase; }
        .title { font-size: 1.1rem; margin: 8px 0; color: #f0f0f0; }
        .desc { color: #aaa; font-size: 0.9rem; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Connect to your DB
conn = sqlite3.connect('dad_media_vault.db')
cursor = conn.cursor()

# Get your data (Adjust 'events' table name if yours is different)
cursor.execute("SELECT year, title, filename, description, metric_label, metric_value FROM events")
rows = cursor.fetchall()

st.markdown("<h1 style='text-align:center;'>The Legacy Archive</h1>", unsafe_allow_html=True)

# Loop through your real database rows
for row in rows:
    year, title, filename, desc, m_lbl, m_val = row
    
    st.markdown(f"""
        <div class="card">
            <span class="year">{year}</span>
            <div class="title">{title}</div>
    """, unsafe_allow_html=True)
    
    # This uses your actual filename from the DB
    st.image(f"static/photos/{filename}", use_container_width=True)
    
    st.markdown(f"""
            <p class="desc">{desc}</p>
            <div style="font-size:0.6rem; color:#666;">{m_lbl}: {m_val}</div>
        </div>
    """, unsafe_allow_html=True)

conn.close()