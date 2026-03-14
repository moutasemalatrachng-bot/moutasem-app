import streamlit as st
import sqlite3
from datetime import datetime

# --- 1. إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('moutasem_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  time TEXT, 
                  is_done BOOLEAN)''')
    conn.commit()
    conn.close()

def add_task(content, task_time):
    conn = sqlite3.connect('moutasem_data.db', check_same_thread=False)
    c = conn.cursor()
    time_str = task_time.strftime("%I:%M %p")
    c.execute("INSERT INTO tasks (content, time, is_done) VALUES (?, ?, ?)", (content, time_str, False))
    conn.commit()
    conn.close()

def delete_task(t_id):
    conn = sqlite3.connect('moutasem_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (t_id,))
    conn.commit()
    conn.close()

# --- 2. إعدادات الواجهة ---
st.set_page_config(page_title="Moutasem App", page_icon="🌹", layout="centered")
init_db()

# --- 3. تصميم الواجهة بالصورة الجديدة ---
# ملاحظة: استخدمت رابطاً لصورة تشبه صورتك لضمان الظهور على الإنترنت
img_url = "https://images.unsplash.com/photo-1550005817-06830d1d61ce?q=80&w=1000&auto=format&fit=crop"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{img_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* جعل النصوص والبطاقات واضحة فوق الصورة */
    .main {{
        background-color: rgba(0, 0, 0, 0.4); /* طبقة تعتيم خفيفة */
        padding: 20px;
        border-radius: 15px;
    }}
    
    h1, p, label, .stMarkdown {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7); /* ظل للنصوص */
    }}

    .stButton>button {{
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }}

    /* تصميم البطاقات للمهام */
    .task-card {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px); /* تأثير الزجاج الضبابي */
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🌹 تطبيق Moutasem الذكي")
st.write(f"اليوم: {datetime.now().strftime('%Y-%m-%d')}")

# --- 4. إضافة مهمة جديدة ---
with st.expander("✨ أضف مهمة جديدة الآن", expanded=True):
    task_text = st.text_input("ما هي مهمتك القادمة؟", placeholder="اكتب هنا...")
    task_time = st.time_input("التوقيت المفترض:", datetime.now().time())
    
    if st.button("إضافة للقائمة"):
        if task_text:
            add_task(task_text, task_time)
            st.rerun()

# --- 5. عرض المهام ---
st.divider()
conn = sqlite3.connect('moutasem_data.db', check_same_thread=False)
c = conn.cursor()
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()
conn.close()

if not tasks:
    st.info("القائمة فارغة، ابدأ بإضافة مهامك!")
else:
    for task in tasks:
        t_id, t_content, t_time, t_status = task
        st.markdown(f"""
        <div class="task-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 18px; font-weight: bold; color: white;">{t_content}</span><br>
                    <span style="font-size: 14px; color: #ddd;">⏰ {t_time}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # زر الحذف نضعه خارج الـ Markdown ليعمل برمجياً
        if st.button(f"إلغاء المهمة 🗑️", key=f"del_{t_id}"):
            delete_task(t_id)
            st.rerun()
