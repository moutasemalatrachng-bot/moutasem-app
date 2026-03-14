import streamlit as st
import sqlite3
from datetime import datetime

# --- 1. إعداد قاعدة البيانات ---
# نستخدم اسم ملف جديد لضمان تحديث البيانات بشكل نظيف
conn = sqlite3.connect('moutasem_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, time TEXT)')
conn.commit()

# --- 2. إعداد واجهة المستخدم وصورة الخلفية ---
# رابط مباشر لصورة الورود التي طلبتها
img_url = "https://w0.peakpx.com/wallpaper/447/844/HD-wallpaper-woman-holding-roses-flowers-bouquets-red-lips.jpg"

st.set_page_config(page_title="Moutasem App", page_icon="🌹")

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{img_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* طبقة تعتيم لجعل النصوص واضحة جداً */
    .main {{
        background-color: rgba(0, 0, 0, 0.5);
        padding: 30px;
        border-radius: 15px;
    }}
    h1, label, p, .stMarkdown {{
        color: white !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.9);
    }}
    /* تنسيق صندوق المهام */
    .task-box {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 10px;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🌹 تطبيق معتصم الذكي")
st.write("نظّم مهامك بلمسة فنية")

# --- 3. إضافة مهمة جديدة ---
with st.container():
    t_text = st.text_input("ما هي المهمة؟", placeholder="اكتب هنا...")
    t_time = st.time_input("اختر الوقت:", datetime.now().time())
    
    if st.button("إضافة المهمة للقائمة ✨"):
        if t_text:
            # الحل النهائي لمشكلة الوقت: تحويله لنص قبل الحفظ
            formatted_time = t_time.strftime("%I:%M %p")
            c.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (t_text, formatted_time))
            conn.commit()
            st.rerun()

# --- 4. عرض المهام المضافة ---
st.markdown("---")
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()

if not tasks:
    st.info("لا توجد مهام حالياً. ابدأ بإضافة أول مهمة!")
else:
    for row in tasks:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="task-box">
                    <strong>{row[1]}</strong><br>
                    <small>⏰ {row[2]}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                # زر الحذف
                if st.button("🗑️", key=f"del_{row[0]}"):
                    c.execute("DELETE FROM tasks WHERE id=?", (row[0],))
                    conn.commit()
                    st.rerun()
