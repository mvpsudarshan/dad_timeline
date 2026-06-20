import streamlit as st
import sqlite3
import os
from PIL import Image, ImageOps

# Page setup
st.set_page_config(page_title="Legacy Archive", layout="centered")

# --- ROYAL UI STYLING (Updated Sizes) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=Montserrat:wght@300&display=swap');
    .stApp { background-color: #050505; }
    .block-container { max-width: 500px !important; }
    
    .royal-title { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; color: #d4af37; text-align: center; margin-bottom: 5px; }
    .sub-heading { font-family: 'Montserrat', sans-serif; font-size: 0.9rem; color: #888; text-align: center; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 30px; }
    
    .card { background: #0a0a0a; border-bottom: 1px solid #1a1a1a; padding: 10px 0; margin-bottom: 40px; }
    
    /* Bigger Year */
    .year { color: #d4af37; font-size: 1.1rem; font-weight: bold; letter-spacing: 1px; font-family: 'Cormorant Garamond'; margin-bottom: 5px; }
    
    .title { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; color: #fff; margin: 5px 0; }
    
    /* Smaller Images */
    .img-container { display: flex; justify-content: center; margin: 15px 0; }
    .img-container img { max-width: 80% !important; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='royal-title'>The Legacy Archive</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-heading'>Happy Father's Day</p>", unsafe_allow_html=True)

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
        
        if filename.lower() in available_files:
            actual_filename = available_files[filename.lower()]
            full_path = os.path.join(folder_path, actual_filename)
            
            img = Image.open(full_path)
            img = ImageOps.exif_transpose(img)
            
            # Display inside our centered container
            st.markdown("<div class='img-container'>", unsafe_allow_html=True)
            st.image(img) # use_container_width=False lets CSS control the size
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown(f"<p style='color:#ccc; font-family:Montserrat; font-size: 0.9rem; line-height: 1.5;'>{desc}</p>", unsafe_allow_html=True)
        st.caption(f"{m_lbl}: {m_val}")
            
    conn.close()
except Exception as e:
    st.error(f"Error: {e}")
