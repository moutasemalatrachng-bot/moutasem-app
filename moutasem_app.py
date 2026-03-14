import streamlit as st
from datetime import datetime
import os
import base64

# --- 1. إعدادات تجعل الموقع يتصرف كتطبيق موبايل ---
st.set_page_config(
    page_title="Organize Your Time",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ميزة الخصوصية (Session State)
if 'my_tasks' not in st.session_state:
    st.session_state.my_tasks = []

# --- 2. إعداد الخلفية ---
bg_image_path = "background.jpg.jpeg"

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

if os.path.exists(bg_image_path):
    bin_str = get_base64(bg_image_path)
    st.markdown(f"""
        <style>
        /* إخفاء شريط Streamlit العلوي ليعطي شعور التطبيق الحقيقي */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .main {{
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 15px;
        }}
        /* تحسين مظهر الخطوط في الموبايل */
        h1 {{
            font-size: 24px !important;
            text-align: center;
            color: white !important;
            text-shadow: 2px 2px 5px #000;
        }}
        label, p, .stMarkdown {{
            color: white !important;
            text-shadow: 1px 1px 3px #000;
        }}
        </style>
        """, unsafe_allow_html=True)

# --- 3. واجهة التطبيق ---
st.title("Organize Your Time with Moutasem 🌟")

# نستخدم columns لجعل الشكل متناسق في شاشة الموبايل
t_text = st.text_input("What is the new task?", placeholder="Enter task name...")
t_time = st.time_input("Set time:", value=datetime.now().time())

if st.button("Save Task 🌟", use_container_width=True):
    if t_text:
        formatted_time = t_time.strftime("%I:%M %p")
        st.session_state.my_tasks.append({
            "task": t_text,
            "time": formatted_time
        })
        st.rerun()

# --- 4. عرض المهام ---
st.markdown("---")
if not st.session_state.my_tasks:
    st.info("Your private list is empty.")
else:
    for index, item in enumerate(st.session_state.my_tasks):
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"✅ **{item['task']}**\n\n⏰ {item['time']}")
            with col2:
                if st.button("🗑️", key=f"del_{index}"):
                    st.session_state.my_tasks.pop(index)
                    st.rerun()
