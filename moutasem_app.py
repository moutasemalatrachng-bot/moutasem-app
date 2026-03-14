import streamlit as st
from datetime import datetime
import os
import base64

# --- 1. إعدادات الصفحة والخصوصية ---
st.set_page_config(page_title="Organize Your Time", page_icon="🌟")

# استخدام Session State بدلاً من قاعدة البيانات لضمان الخصوصية
if 'my_tasks' not in st.session_state:
    st.session_state.my_tasks = []

# --- 2. إعداد الخلفية (background.jpg.jpeg) ---
bg_image_path = "background.jpg.jpeg"

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

# --- 3. واجهة التطبيق بالإنجليزية ---
st.title("Organize Your Time with Moutasem 🌟")

with st.container():
    t_text = st.text_input("What is the new task?", key="task_input")
    t_time = st.time_input("Set completion time:", value=datetime.now().time(), key="time_input")
    
    if st.button("Save Task 🌟"):
        if t_text:
            formatted_time = t_time.strftime("%I:%M %p")
            # إضافة المهمة لذاكرة الجلسة الحالية فقط
            st.session_state.my_tasks.append({
                "task": t_text,
                "time": formatted_time
            })
            st.rerun()

# --- 4. عرض المهام الخاصة بكل مستخدم ---
st.markdown("---")
st.subheader("My Private Tasks")

if not st.session_state.my_tasks:
    st.info("Your private list is empty. No one else can see your tasks!")
else:
    for index, item in enumerate(st.session_state.my_tasks):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"✅ **{item['task']}** | ⏰ {item['time']}")
        with col2:
            if st.button("🗑️", key=f"del_{index}"):
                st.session_state.my_tasks.pop(index)
                st.rerun()
