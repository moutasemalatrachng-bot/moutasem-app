import streamlit as st
import sqlite3
from datetime import datetime
import os
import base64

# --- 1. حل مشكلة الوقت (استخدام قاعدة بيانات جديدة تماماً) ---
# تغيير الاسم لـ final_v11 يضمن تحديث النظام وتثبيت الوقت كنص
conn = sqlite3.connect('final_v11.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, time TEXT)')
conn.commit()

# --- 2. إعداد الخلفية (الاسم مطابق تماماً لـ GitHub) ---
# الاسم حسب الصورة التي أرفقتها هو: background.jpg.jpeg
bg_image_path = "background.jpg.jpeg"

st.set_page_config(page_title="Moutasem App", page_icon="🌟")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# كود حقن الخلفية CSS
if os.path.exists(bg_image_path):
    try:
        bin_str = get_base64(bg_image_path)
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* طبقة تعتيم لتوضيح الكلام الأبيض */
            .main {{
                background-color: rgba(0, 0, 0, 0.5);
                padding: 25px;
                border-radius: 15px;
                margin-top: 30px;
            }}
            h1, label, p, .stMarkdown {{
                color: white !important;
                text-shadow: 2px 2px 5px #000;
            }}
            </style>
            """, unsafe_allow_html=True)
    except:
        st.error("حدث خطأ أثناء تحميل الصورة.")
else:
    st.error(f"تنبيه: لم أجد ملف {bg_image_path} في GitHub.")

# --- 3. العنوان والنجمة 🌟 ---
st.title("تطبيق معتصم المطور 🌟")

with st.container():
    t_text = st.text_input("ما هي مهمتك الجديدة؟")
    t_time = st.time_input("حدد وقت التذكير:", datetime.now().time())
    
    if st.button("حفظ المهمة 🌟"):
        if t_text:
            # تخزين الوقت بصيغة نصية ثابتة (AM/PM)
            formatted_time = t_time.strftime("%I:%M %p")
            c.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (t_text, formatted_time))
            conn.commit()
            st.rerun()

# --- 4. عرض المهام المضافة ---
st.markdown("---")
c.execute("SELECT * FROM tasks")
rows = c.fetchall()

if not rows:
    st.info("لا توجد مهام حالياً.")
else:
    for row in rows:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                # عرض المهمة والوقت الثابت
                st.markdown(f"✅ **{row[1]}** | ⏰ {row[2]}")
            with col2:
                if st.button("🗑️", key=f"del_{row[0]}"):
                    c.execute("DELETE FROM tasks WHERE id=?", (row[0],))
                    conn.commit()
                    st.rerun()
