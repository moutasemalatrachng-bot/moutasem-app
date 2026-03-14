import streamlit as st
import sqlite3
from datetime import datetime

# --- 1. إعداد قاعدة البيانات الدائمة ---
def init_db():
    conn = sqlite3.connect('moutasem_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  time TEXT, 
                  is_done BOOLEAN)''')
    conn.commit()
    conn.close()

def add_task(content, time):
    conn = sqlite3.connect('moutasem_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (content, time, is_done) VALUES (?, ?, ?)", (content, time, False))
    conn.commit()
    conn.close()

def delete_task(t_id):
    conn = sqlite3.connect('moutasem_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (t_id,))
    conn.commit()
    conn.close()

# --- 2. إعدادات الواجهة الاحترافية ---
st.set_page_config(page_title="Moutasem App", page_icon="⭐", layout="centered")
init_db()

# امسح الجزء القديم وضع هذا مكانه
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #00d1b2; color: white; font-weight: bold; }
    .task-box { background-color: #1d2129; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 5px solid #00d1b2; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌟 تطبيق Moutasem المطور")
st.write(f"اليوم: {datetime.now().strftime('%Y-%m-%d')}")

# --- 3. إضافة مهمة جديدة ---
with st.expander("➕ أضف مهمة جديدة الآن", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        task_text = st.text_input("", placeholder="ماذا تريد أن تنجز اليوم؟")
    with col2:
        task_time = st.time_input("التوقيت", datetime.now().time())
    
    if st.button("حفظ في القائمة"):
        if task_text:
            add_task(task_text, task_time.strftime("%I:%M %p"))
            st.rerun()

# --- 4. رفع الملفات ---
st.divider()
st.subheader("📁 مركز الملفات")
uploaded_file = st.file_uploader("ارفع ملفاتك هنا للوصول السريع", type=["pdf", "txt", "jpg", "png"])
if uploaded_file:
    st.success(f"تم استقبال الملف: {uploaded_file.name}")

# --- 5. عرض المهام من قاعدة البيانات ---
st.divider()
st.subheader("📋 مهامي اليومية")

conn = sqlite3.connect('moutasem_data.db')
c = conn.cursor()
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()
conn.close()

if not tasks:
    st.info("لا توجد مهام محفوظة حالياً. ابدأ بإضافة واحدة!")
else:
    for task in tasks:
        t_id, t_content, t_time, t_status = task
        with st.container():
            col_text, col_time, col_del = st.columns([4, 2, 1])
            with col_text:
                st.markdown(f"**{t_content}**")
            with col_time:
                st.caption(f"⏰ {t_time}")
            with col_del:
                if st.button("🗑️", key=f"del_{t_id}"):
                    delete_task(t_id)
                    st.rerun()