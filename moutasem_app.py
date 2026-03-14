import streamlit as st
from datetime import datetime
import os
import base64
import time

# --- 1. الإعدادات والخصوصية ---
st.set_page_config(page_title="Organize Your Time", page_icon="🌟", layout="centered")

if 'my_tasks' not in st.session_state: st.session_state.my_tasks = []
if 'achievements' not in st.session_state: st.session_state.achievements = []

# --- 2. الخلفية ---
bg_image_path = "background.jpg.jpeg"
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bin_str = get_base64(bg_image_path)
if bin_str:
    st.markdown(f"""
        <style>
        .stApp {{ background-image: url("data:image/jpeg;base64,{bin_str}"); background-size: cover; background-attachment: fixed; }}
        .main {{ background-color: rgba(0, 0, 0, 0.6); padding: 20px; border-radius: 15px; }}
        h1, h2, h3, label, p, .stMarkdown {{ color: white !important; text-shadow: 2px 2px 5px #000; }}
        .stButton>button {{ width: 100%; border-radius: 10px; }}
        </style>
        """, unsafe_allow_html=True)

st.title("Organize Your Time with Moutasem 🌟")

# --- 3. قسم مؤقت التركيز (Focus Timer) ---
with st.expander("🕒 Focus Timer (Pomodoro)", expanded=False):
    st.write("Concentrate for 25 minutes")
    if st.button("Start 25 min Focus Session"):
        ph = st.empty()
        for t in range(25 * 60, 0, -1):
            mins, secs = divmod(t, 60)
            ph.metric("Remaining Time", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        st.success("Time's up! Take a break. ☕")

st.markdown("---")

# --- 4. إضافة مهمة مع تحديد الأولوية (Priority Matrix) ---
col_t, col_p = st.columns([3, 1])
with col_t:
    t_text = st.text_input("What's the task?", key="t_in")
with col_p:
    t_prio = st.selectbox("Priority", ["Normal", "Urgent", "Low"])

t_time = st.time_input("Set time:", value=datetime.now().time())

if st.button("Add Task to My List 🚀"):
    if t_text:
        p_color = "🔴" if t_prio == "Urgent" else "⚪" if t_prio == "Normal" else "🔵"
        st.session_state.my_tasks.append({
            "task": t_text,
            "time": t_time.strftime("%I:%M %p"),
            "prio": f"{p_color} {t_prio}"
        })
        st.rerun()

# عرض المهام
for idx, item in enumerate(st.session_state.my_tasks):
    with st.container():
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"{item['prio']} **{item['task']}** | ⏰ {item['time']}")
        if c2.button("🗑️", key=f"del_{idx}"):
            st.session_state.my_tasks.pop(idx)
            st.rerun()

st.markdown("---")

# --- 5. مفكرة الإنجازات (Achievement Diary) ---
st.subheader("🏆 Daily Achievements")
ach_in = st.text_input("Write something you're proud of today:", key="ach_in")
if st.button("Record Achievement"):
    if ach_in:
        st.session_state.achievements.append(f"⭐ {ach_in} ({datetime.now().strftime('%H:%M')})")
        st.rerun()

for a in reversed(st.session_state.achievements):
    st.write(a)
