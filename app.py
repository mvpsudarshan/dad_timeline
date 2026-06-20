import streamlit as st
import sqlite3
import os

# Page setup
st.set_page_config(page_title="Legacy Archive", layout="centered")

# --- ROYAL UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=Montserrat:wght@300&display=swap');
    
    .stApp { background-color: #050505; }
    
    .royal-title { 
        font-family: 'Cormorant Garamond', serif; 
        font-size: 3.5rem; 
        color: #d4af37; 
        text-align: center; 
        margin-bottom: 0;
    }
    .sub-heading { 
        font-family: 'Montserrat', sans-serif; 
        font-size: 1.2rem; 
        color: #e0e0e0; 
        text-align: center; 
        letter-spacing: 2px; 
        margin-bottom: 40px;
    }
    .card { 
        background: #0a0a0a; 
        border: 1px solid #222; 
        padding: 20px; 
        border-radius: 2px; 
        margin-bottom: 30px; 
    }
    .year { color: #d4af37; font-size: 0.8rem; letter-spacing: 3px; }
    .title { font-family: 'Cormorant Garamond', serif; font-size: 1.8rem; color: #fff; margin: 10px 0; }
    
    /* Mobile Optimization */
    @media (max-width: 600px) {
        .royal-title { font-size: 2.5rem; }
        .card { padding: 15px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<h1 class='royal-title'>The Legacy Archive</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-heading'>HAPPY FATHER'S DAY</p>", unsafe_allow_html=True)

try:
    conn = sqlite3.connect('dad_media_vault.db')
    cursor = conn.cursor()
    cursor.execute("SELECT year, title, media_filename, description, metric_label, metric_value FROM timeline_media ORDER BY display_order ASC")
    rows = cursor.fetchall()

    folder_path = os.path.join("static", "photos")
    available_files = {f.lower(): f for f in os.listdir(folder_path)}

    for row in rows:
        year, title, filename, desc, m_lbl, m_val = row
        
        st.markdown(f"""
            <div class='card'>
                <div class='year'>{year}</div>
                <div class='title'>{title}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Image handling
        if filename.lower() in available_files:
            actual_filename = available_files[filename.lower()]
            st.image(os.path.join(folder_path, actual_filename), use_container_width=True)
            
        st.markdown(f"<p style='color:#bbb; font-family:Montserrat;'>{desc}</p>", unsafe_allow_html=True)
        st.caption(f"{m_lbl}: {m_val}")
        st.markdown("</div>", unsafe_allow_html=True)
            
    conn.close()
except Exception as e:
    st.error(f"Error loading archive: {e}")
