import streamlit as st
import sqlite3
from datetime import datetime
import os
import base64

# --- 1. إعداد قاعدة البيانات و ميزة الوقت ---
# نستخدم اسم قاعدة بيانات جديدة لضمان مسح أي أخطاء سابقة في الوقت
conn = sqlite3.connect('moutasem_stars.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, time TEXT)')
conn.commit()

# --- 2. إعداد الخلفية باستخدام الصورة التي رفعتها ---
bg_image_path = "background.jpg"

st.set_page_config(page_title="Moutasem App", page_icon="🌟")

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

if os.path.exists(bg_image_path):
    try:
        bin_str = get_base64_image(bg_image_path)
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* طبقة تعتيم لتوضيح النصوص */
            .main {{
                background-color: rgba(0, 0, 0, 0.5);
                padding: 25px;
                border-radius: 15px;
            }}
            h1, label, p, .stMarkdown {{
                color: white !important;
                text-shadow: 2px 2px 5px rgba(0,0,0,0.8);
            }}
            </style>
            """, unsafe_allow_html=True)
    except Exception:
        st.warning("هناك مشكلة في قراءة الصورة، تأكد من رفعها باسم background.jpg")

# --- 3. العنوان الجديد مع النجمة ---
st.title("🌟 تطبيق معتصم المطور")

# --- 4. إضافة مهمة (حل مشكلة الوقت) ---
with st.container():
    t_text = st.text_input("ما هي مهمتك الجديدة؟", placeholder="اكتب هنا...")
    t_time = st.time_input("حدد وقت التذكير:", datetime.now().time())
    
    if st.button("حفظ المهمة 🌟"):
        if t_text:
            # تحويل الوقت لنص يضمن بقاءه ثابتاً في القائمة
            formatted_time = t_time.strftime("%I:%M %p")
            c.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (t_text, formatted_time))
            conn.commit()
            st.rerun()

# --- 5. عرض المهام ---
st.markdown("---")
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()

if not tasks:
    st.info("لا توجد مهام حالياً.")
else:
    for row in tasks:
        col1, col2 = st.columns([5, 1])
        with col1:
            # عرض المهمة والوقت بشكل واضح
            st.markdown(f"✅ **{row[1]}** | ⏰ {row[2]}")
        with col2:
            if st.button("🗑️", key=f"del_{row[0]}"):
                c.execute("DELETE FROM tasks WHERE id=?", (row[0],))
                conn.commit()
                st.rerun()
