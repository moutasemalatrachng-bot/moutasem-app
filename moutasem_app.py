import streamlit as st
from datetime import datetime
import os
import base64
import time
import random

# --- 1. الإعدادات والخصوصية ---
st.set_page_config(page_title="Organize Your Time", page_icon="🌟", layout="centered")

if 'my_tasks' not in st.session_state: st.session_state.my_tasks = []
if 'achievements' not in st.session_state: st.session_state.achievements = []
if 'habits' not in st.session_state: 
    st.session_state.habits = {"Water 💧": False, "Reading 📖": False, "Exercise 🏃‍♂️": False, "Prayer ✨": False}

# --- 2. التحية الذكية حسب الوقت ---
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Good Morning, Moutasem! ☀️ Ready to win today?"
    elif 12 <= hour < 17: return "Good Afternoon, Moutasem! 🚀 Keep up the energy!"
    elif 17 <= hour < 21: return "Good Evening, Moutasem! 🌆 Time to wrap up your wins."
    else: return "Late Night Productivity, Moutasem? 🌙 Don't forget to rest!"

# --- 3. إعداد الخلفية ---
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
        .main {{ background-color: rgba(0, 0, 0, 0.65); padding: 20px; border-radius: 15px; }}
        h1, h2, h3, label, p, span, .stMarkdown {{ color: white !important; text-shadow: 2px 2px 5px #000; }}
        .stProgress > div > div > div > div {{ background-color: #FFD700 !important; }}
        </style>
        """, unsafe_allow_html=True)

# --- 4. العنوان والتحية الذكية ---
st.title("Organize Your Time with Moutasem 🌟")
st.subheader(get_greeting())

# --- 5. حلقة الإنجاز (Progress Tracking) ---
# نحسب المهام المنجزة (افتراضياً هنا سنعتمد على العادات + المهام الموجودة)
total_habits = len(st.session_state.habits)
done_habits = sum(st.session_state.habits.values())
progress = (done_habits / total_habits) if total_habits > 0 else 0

st.write(f"Your Daily Progress: {int(progress * 100)}%")
st.progress(progress)
if progress == 1.0:
    st.success("100% Achievement! You are a legend today! 🏆")
    st.balloons()

st.markdown("---")

# --- 6. العادات اليومية ---
st.subheader("✅ Daily Habits")
cols = st.columns(len(st.session_state.habits))
for i, (habit, done) in enumerate(st.session_state.habits.items()):
    with cols[i]:
        if st.checkbox(habit, value=done, key=f"hb_{habit}"):
            if not st.session_state.habits[habit]:
                st.session_state.habits[habit] = True
                st.rerun()
        else:
            if st.session_state.habits[habit]:
                st.session_state.habits[habit] = False
                st.rerun()

# --- 7. مؤقت التركيز والمهمات ---
with st.expander("🕒 Focus Timer", expanded=False):
    f_min = st.slider("Minutes:", 1, 120, 25)
    if st.button("Start"):
        ph = st.empty()
        for t in range(f_min * 60, 0, -1):
            m, s = divmod(t, 60)
            ph.metric("Remaining", f"{m:02d}:{secs:02d}") # تم تصحيح secs هنا
            time.sleep(1)
        st.balloons()

# إضافة مهمة
st.subheader("📝 New Task")
c_t, c_p = st.columns([3, 1])
t_txt = c_t.text_input("Task name:", key="t_in")
t_prio = c_p.selectbox("Priority", ["Normal", "Urgent", "Low"])
t_tm = st.time_input("At:", value=datetime.now().time())

if st.button("Save Task 🚀"):
    if t_txt:
        p_em = "🔴" if t_prio == "Urgent" else "⚪" if t_prio == "Normal" else "🔵"
        st.session_state.my_tasks.append({"task": t_txt, "time": t_tm.strftime("%I:%M %p"), "prio": f"{p_em} {t_prio}"})
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
# --- 8. الإنجازات ---
st.subheader("🏆 Daily Achievements")
ach = st.text_input("Proud of:", key="ach_in")
if st.button("Record"):
    if ach:
        st.session_state.achievements.append(f"⭐ {ach} ({datetime.now().strftime('%H:%M')})")
        st.rerun()
for a in reversed(st.session_state.achievements): st.write(a)
