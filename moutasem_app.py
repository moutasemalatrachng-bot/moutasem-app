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
    st.session_state.habits = {"Water/ماء 💧": False, "Reading/قراءة 📖": False, "Exercise/رياضة 🏃‍♂️": False, "Prayer/صلاة ✨": False}

# --- 2. التحية الذكية باللغتين ---
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Good Morning! ☀️ Ready to win today? | صباح الخير! هل أنت مستعد للنجاح اليوم؟"
    elif 12 <= hour < 17: return "Good Afternoon! 🚀 Keep up the energy! | طاب يومك! حافظ على طاقتك!"
    elif 17 <= hour < 21: return "Good Evening! 🌆 Time to wrap up your wins. | مساء الخير! حان وقت حصد إنجازاتك."
    else: return "Late Night Productivity? 🌙 Don't forget to rest! | إنتاجية متأخرة؟ لا تنسَ أن ترتاح!"

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
        h1, h2, h3, label, p, span, .stMarkdown {{ color: white !important; text-shadow: 2px 2px 5px #000; text-align: center; }}
        .stProgress > div > div > div > div {{ background-color: #FFD700 !important; }}
        </style>
        """, unsafe_allow_html=True)

# --- 4. العنوان والتحية ---
st.title("Organize Your Time | تنظيم وقتك 🌟")
st.write(f"### {get_greeting()}")

# --- 5. شريط الإنجاز ---
done_habits = sum(st.session_state.habits.values())
progress = (done_habits / len(st.session_state.habits))
st.write(f"**Daily Progress | مستوى الإنجاز اليومي:** {int(progress * 100)}%")
st.progress(progress)

st.markdown("---")

# --- 6. ميزة تعلم اللغات الجديدة (Language Learning) ---
with st.expander("🌍 Language Learning | تعلم اللغات", expanded=False):
    st.write("Keep expanding your horizons! | استمر في توسيع آفاقك!")
    
    col_lang, col_duration = st.columns(2)
    
    with col_lang:
        lang_choice = st.selectbox(
            "Which language are you learning? | ما اللغة التي تتعلمها؟",
            ["English / الإنجليزية", "Chinese / الصينية", "Spanish / الإسبانية", "German / الألمانية"]
        )
    
    with col_duration:
        # وقت حر حسب رغبة المستخدم
        learn_time = st.number_input("Study duration (minutes) | مدة الدراسة (بالدقائق):", min_value=1, max_value=480, value=30)

    if st.button("Start Learning Session | ابدأ جلسة التعلم 📚"):
        st.write(f"Focusing on **{lang_choice}** for **{learn_time}** minutes... 🔥")
        ph_lang = st.empty()
        for t in range(learn_time * 60, 0, -1):
            m, s = divmod(t, 60)
            ph_lang.metric("Study Time Remaining | الوقت المتبقي للدراسة", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.success(f"Great job learning {lang_choice}! | عمل رائع في تعلم {lang_choice}! 🎉")
        st.balloons()

st.markdown("---")

# --- 7. تنظيم النوم (Sleep Planner) ---
with st.expander("🌙 Sleep Planner & Health | مخطط النوم والصحة", expanded=False):
    st.markdown("### 😴 Why Sleep Matters | لماذا النوم مهم؟")
    st.write("Your brain needs **8 hours** of quality sleep. | يحتاج عقلك إلى **8 ساعات** من النوم العميق.")
    
    wake_time = st.time_input("Wake-up goal | وقت الاستيقاظ:", value=datetime.strptime("07:00", "%H:%M").time(), key="wake_p")
    
    if st.button("Calculate Bedtime | احسب وقت النوم 🛌"):
        wake_datetime = datetime.combine(datetime.today(), wake_time)
        perfect_bedtime = (wake_datetime - timedelta(hours=8)).strftime("%I:%M %p")
        st.success(f"To get 8 hours, go to bed at: **{perfect_bedtime}** | للحصول على 8 ساعات، نم في تمام الساعة")

st.markdown("---")

# --- 8. العادات اليومية ---
st.subheader("✅ Daily Habits | العادات اليومية")
cols = st.columns(len(st.session_state.habits))
for i, (habit, done) in enumerate(st.session_state.habits.items()):
    with cols[i]:
        if st.checkbox(habit, value=done, key=f"hb_{habit}"):
            st.session_state.habits[habit] = True
        else:
            st.session_state.habits[habit] = False

# --- 9. مؤقت التركيز العام ---
with st.expander("🕒 General Focus Timer | مؤقت التركيز العام", expanded=False):
    f_min = st.slider("Minutes | الدقائق:", 1, 120, 25, key="gen_timer")
    if st.button("Start Timer | ابدأ المؤقت", key="gen_btn"):
        ph = st.empty()
        for t in range(f_min * 60, 0, -1):
            m, s = divmod(t, 60)
            ph.metric("Remaining | المتبقي", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.balloons()

# --- 10. المهمات الجديدة ---
st.subheader("📝 New Task | مهمة جديدة")
c_t, c_p = st.columns([3, 1])
t_txt = c_t.text_input("Task name | اسم المهمة:", key="t_in")
t_prio = c_p.selectbox("Priority | الأولوية", ["Normal/عادي", "Urgent/عاجل", "Low/بسيط"])
t_tm = st.time_input("At | في وقت:", value=datetime.now().time(), key="t_tm_input")

if st.button("Save Task | حفظ المهمة 🚀"):
    if t_txt:
        p_em = "🔴" if "Urgent" in t_prio else "⚪" if "Normal" in t_prio else "🔵"
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
# --- 11. الإنجازات ---
st.subheader("🏆 Achievements | الإنجازات اليومية")
ach = st.text_input("I am proud of | أنا فخور بـ:", key="ach_in")
if st.button("Record | تسجيل"):
    if ach:
        st.session_state.achievements.append(f"⭐ {ach} ({datetime.now().strftime('%H:%M')})")
        st.rerun()
for a in reversed(st.session_state.achievements): st.write(a)
