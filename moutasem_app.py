import streamlit as st
import sqlite3
from datetime import datetime
import os
import base64

# --- 1. حل مشكلة الوقت (قاعدة بيانات جديدة لضمان الدقة) ---
conn = sqlite3.connect('moutasem_v12.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, time TEXT)')
conn.commit()

# --- 2. إعداد الخلفية (الاسم مطابق لـ GitHub) ---
bg_image_path = "background.jpg.jpeg"

st.set_page_config(page_title="Organize Your Time", page_icon="🌟")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

if os.path.exists(bg_image_path):
    bin_str = get_base64(bg_image_path)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .main {{
            background-color: rgba(0, 0, 0, 0.5);
            padding: 25px;
            border-radius: 15px;
        }}
        h1, label, p, .stMarkdown {{
            color: white !important;
            text-shadow: 2px 2px 5px #000;
        }}
        </style>
        """, unsafe_allow_html=True)

# --- 3. الاسم الجديد بالإنجليزية ---
st.title("Organize Your Time with Moutasem 🌟")

with st.container():
    t_text = st.text_input("What is the new task?", key="input_task")
    
    # اختيار الوقت مع مفتاح ثابت لضمان حفظ القيمة المختارة
    t_time = st.time_input("Set completion time:", value=datetime.now().time(), key="input_time")
    
    if st.button("Save Task 🌟"):
        if t_text:
            # تحويل الوقت المختار (مهما كان) إلى نص AM/PM
            formatted_time = t_time.strftime("%I:%M %p")
            c.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (t_text, formatted_time))
            conn.commit()
            st.rerun()

# --- 4. عرض المهام ---
st.markdown("---")
c.execute("SELECT * FROM tasks")
rows = c.fetchall()

if not rows:
    st.info("Your list is empty. Add a task and set its time!")
else:
    for row in rows:
        col1, col2 = st.columns([5, 1])
        with col1:
            # عرض الوقت المخزن في قاعدة البيانات
            st.markdown(f"✅ **{row[1]}** | ⏰ {row[2]}")
        with col2:
            if st.button("🗑️", key=f"del_{row[0]}"):
                c.execute("DELETE FROM tasks WHERE id=?", (row[0],))
                conn.commit()
                st.rerun()
