import streamlit as st
from datetime import datetime
import os
import base64
import time
import random

# --- 1. الإعدادات والخصوصية ---
st.set_page_config(page_title="Organize Your Time", page_icon="🌟", layout="centered")

# تهيئة الذاكرة للميزات الجديدة
if 'my_tasks' not in st.session_state: st.session_state.my_tasks = []
if 'achievements' not in st.session_state: st.session_state.achievements = []
if 'habits' not in st.session_state: 
    st.session_state.habits = {"Water 💧": False, "Reading 📖": False, "Exercise 🏃‍♂️": False, "Prayer/Meditation ✨": False}

# قائمة اقتباسات تحفيزية
quotes = [
    "Small steps lead to big results. ✨",
    "Do something today that your future self will thank you for. 🚀",
    "Believe you can and you're halfway there. 🌟",
    "إنجاز صغير كل يوم يولد نجاحاً كبيراً. 💪",
    "ركز على الإنجاز وليس على الانشغال. 🧐",
    "Start where you are. Use what you have. Do what you can. 🔥"
]

# --- 2. إعداد الخلفية ---
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
        h1, h2, h3, label, p, span, .stMarkdown {{ color: white !important; text-shadow: 2px 2px 5px #000; }}
        .stButton>button {{ width: 100%; border-radius: 10px; background-color: rgba(255, 255, 255, 0.1); color: white; border: 1px solid white; }}
        .habit-box {{ background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; margin-bottom: 5px; }}
        </style>
        """, unsafe_allow_html=True)

# --- 3. العنوان والاقتباس اليومي ---
st.title("Organize Your Time with Moutasem 🌟")
st.info(f"💡 {random.choice(quotes)}")

# --- 4. قسم العادات اليومية (Habit Tracker) ---
st.subheader("✅ Daily Habits")
cols = st.columns(len(st.session_state.habits))
for i, (habit, done) in enumerate(st.session_state.habits.items()):
    with cols[i]:
        if st.checkbox(habit, value=done, key=f"habit_{habit}"):
            st.session_state.habits[habit] = True
        else:
            st.session_state.habits[habit] = False

st.markdown("---")

# --- 5. مؤقت التركيز المرن ---
with st.expander("🕒 Focus Timer", expanded=False):
    focus_minutes = st.slider("Minutes:", 1, 120, 25)
    if st.button(f"Start Session"):
        ph = st.empty()
        for t in range(focus_minutes * 60, 0, -1):
            m, s = divmod(t, 60)
            ph.metric("Remaining", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.success("Done! 🎉")
        st.balloons()

# --- 6. إضافة المهمة مع الأولوية والوقت ---
st.subheader("📝 New Task")
col_t, col_p = st.columns([3, 1])
with col_t:
    t_text = st.text_input("Task name:", key="t_in")
with col_p:
    t_prio = st.selectbox("Priority", ["Normal", "Urgent", "Low"])

t_time = st.time_input("At:", value=datetime.now().time())

if st.button("Save Task 🚀"):
    if t_text:
        p_emoji = "🔴" if t_prio == "Urgent" else "⚪" if t_prio == "Normal" else "🔵"
        st.session_state.my_tasks.append({
            "task": t_text,
            "time": t_time.strftime("%I:%M %p"),
            "prio": f"{p_emoji} {t_prio}"
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

# --- 7. مفكرة الإنجازات ---
st.subheader("🏆 Daily Achievements")
ach_in = st.text_input("Something you're proud of:", key="ach_in")
if st.button("Record"):
    if ach_in:
        st.session_state.achievements.append(f"⭐ {ach_in} ({datetime.now().strftime('%H:%M')})")
        st.rerun()

for a in reversed(st.session_state.achievements):
    st.write(a)
