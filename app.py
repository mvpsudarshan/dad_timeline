import streamlit as st
import sqlite3
import os

# Page setup
st.set_page_config(page_title="Legacy Archive", layout="centered")

# --- UI STYLING ---
st.markdown("""
    <style>
    .card { background:#0a0a0a; border:1px solid #333; padding:20px; border-radius:10px; margin-bottom:20px; }
    .year { color:#d4af37; font-weight:bold; font-size:1.2rem; }
    .title { font-size:1.5rem; color:#fff; margin:10px 0; }
    </style>
""", unsafe_allow_html=True)

try:
    conn = sqlite3.connect('dad_media_vault.db')
    cursor = conn.cursor()
    
    # Query all data from your confirmed table 'timeline_media'
    cursor.execute("SELECT year, title, media_filename, description, metric_label, metric_value FROM timeline_media ORDER BY display_order ASC")
    rows = cursor.fetchall()
    
    st.markdown("<h1 style='text-align:center;'>The Legacy Archive</h1>", unsafe_allow_html=True)

    folder_path = os.path.join("static", "photos")
    # Create a lowercase map of available files for case-insensitive matching
    available_files = {f.lower(): f for f in os.listdir(folder_path)}

    for row in rows:
        year, title, filename, desc, m_lbl, m_val = row
        
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='year'>{year}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
        
        # Case-insensitive image lookup
        if filename.lower() in available_files:
            actual_filename = available_files[filename.lower()]
            st.image(os.path.join(folder_path, actual_filename), use_container_width=True)
        else:
            st.warning(f"Could not find image: {filename}")
            
        st.write(desc)
        st.caption(f"{m_lbl}: {m_val}")
        st.markdown("</div>", unsafe_allow_html=True)
            
    conn.close()
except Exception as e:
    st.error(f"Error: {e}")
