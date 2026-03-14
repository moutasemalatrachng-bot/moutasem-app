import streamlit as st
from datetime import datetime, timedelta
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

# --- 2. التحية الذكية العامة ---
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Good Morning! ☀️ Ready to win today?"
    elif 12 <= hour < 17: return "Good Afternoon! 🚀 Keep up the energy!"
    elif 17 <= hour < 21: return "Good Evening! 🌆 Time to wrap up your wins."
    else: return "Late Night Productivity? 🌙 Don't forget to rest!"

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

# --- 4. العنوان والتحية ---
st.title("Organize Your Time 🌟")
st.subheader(get_greeting())

# --- 5. شريط الإنجاز ---
done_habits = sum(st.session_state.habits.values())
progress = (done_habits / len(st.session_state.habits))
st.write(f"Daily Progress: {int(progress * 100)}%")
st.progress(progress)

st.markdown("---")

# --- 6. ميزة تنظيم النوم والمنبه (Sleep Planner & Alarm) ---
with st.expander("🌙 Sleep Planner & Reminders", expanded=False):
    st.write("Waking up refreshed depends on sleep cycles (90 mins each).")
    wake_time = st.time_input("Set your wake-up goal:", value=datetime.strptime("07:00", "%H:%M").time())
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("Calculate Bedtime 🛌"):
            wake_datetime = datetime.combine(datetime.today(), wake_time)
            bed_6 = (wake_datetime - timedelta(hours=9)).strftime("%I:%M %p")
            bed_5 = (wake_datetime - timedelta(hours=7, minutes=30)).strftime("%I:%M %p")
            st.info(f"Sleep at **{bed_6}** or **{bed_5}**")
    
    with col_s2:
        if st.button("Activate Wake-up Check ⏰"):
            st.write("Keep this tab open...")
            while True:
                now = datetime.now().time().strftime("%H:%M")
                target = wake_time.strftime("%H:%M")
                if now == target:
                    st.warning("⏰ TIME TO WAKE UP!")
                    st.balloons()
                    break
                time.sleep(30)

st.markdown("---")

# --- 7. العادات اليومية ---
st.subheader("✅ Daily Habits")
cols = st.columns(len(st.session_state.habits))
for i, (habit, done) in enumerate(st.session_state.habits.items()):
    with cols[i]:
        if st.checkbox(habit, value=done, key=f"hb_{habit}"):
            st.session_state.habits[habit] = True
        else:
            st.session_state.habits[habit] = False

# --- 8. مؤقت التركيز والمهمات ---
with st.expander("🕒 Focus Timer", expanded=False):
    f_min = st.slider("Minutes:", 1, 120, 25)
    if st.button("Start Timer"):
        ph = st.empty()
        for t in range(f_min * 60, 0, -1):
            m, s = divmod(t, 60)
            ph.metric("Remaining", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.success("Focus session complete! ☕")
        st.balloons()

st.subheader("📝 New Task")
c_t, c_p = st.columns([3, 1])
t_txt = c_t.text_input("Task name:", key="t_in")
t_prio = c_p.selectbox("Priority", ["Normal", "Urgent", "Low"])
t_tm = st.time_input("At:", value=datetime.now().time(), key="task_time")

if st.button("Save Task 🚀"):
    if t_txt:
        p_em = "🔴" if t_prio == "Urgent" else "⚪" if t_prio == "Normal" else "🔵"
        st.session_state.my_tasks.append({"task": t_txt, "time": t_tm.strftime("%I:%M %p"), "prio": f"{p_em} {t_prio}"})
        st.rerun()

for idx, item in enumerate(st.session_state.my_tasks):
    with st.container():
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"{item['prio']} **{item['task']}** | ⏰ {item['time']}")
        if c2.button("🗑️", key=f"del_{idx}"):
            st.session_state.my_tasks.pop(idx)
            st.rerun()

st.markdown("---")
st.subheader("🏆 Daily Achievements")
ach = st.text_input("Proud of:", key="ach_in")
if st.button("Record"):
    if ach:
        st.session_state.achievements.append(f"⭐ {ach} ({datetime.now().strftime('%H:%M')})")
        st.rerun()
for a in reversed(st.session_state.achievements): st.write(a)
