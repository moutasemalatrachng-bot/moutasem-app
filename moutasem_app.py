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

# --- 2. التحية الذكية العامة ---
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Good Morning! ☀️ Ready to win today? | صباح الخير! هل أنت مستعد للنجاح اليوم؟"
    elif 12 <= hour < 17: return "Good Afternoon! 🚀 Keep up the energy! | طاب يومك! حافظ على طاقتك!"
    elif 17 <= hour < 21: return "Good Evening! 🌆 Time to wrap up your wins. | مساء الخير! حان وقت حصد إنجازاتك."
    else: return "Late Night Productivity? 🌙 Don't forget to rest! | إنتاجية متأخرة؟ لا تنسَ أن ترتاح!"

# --- 3. إعداد الخلفية والتنسيق ---
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
        .footer {{ position: relative; width: 100%; text-align: center; color: white; padding: 25px; font-size: 15px; text-shadow: 1px 1px 3px #000; border-top: 1px solid rgba(255,255,255,0.2); margin-top: 50px; background-color: rgba(0,0,0,0.3); border-radius: 10px; }}
        </style>
        """, unsafe_allow_html=True)

# --- 4. العنوان والتحية ---
st.title("Organize Your Time | تنظيم وقتك 🌟")
st.write(f"### {get_greeting()}")

# --- 5. شريط الإنجاز المتطور ---
done_habits = sum(st.session_state.habits.values())
total_habits = len(st.session_state.habits)
done_tasks = sum(1 for task in st.session_state.my_tasks if task.get('done', False))
total_tasks = len(st.session_state.my_tasks)

total_items = total_habits + total_tasks
completed_items = done_habits + done_tasks
progress = (completed_items / total_items) if total_items > 0 else 0

st.write(f"**Daily Performance | معدل الأداء اليومي:** {int(progress * 100)}%")
st.progress(progress)

if progress == 1.0 and total_items > 0:
    st.success("Legendary Performance! | أداء أسطوري! اكتملت كل المهام 🏆")
    st.balloons()

st.markdown("---")

# --- 6. تعلم اللغات ---
with st.expander("🌍 Language Learning | تعلم اللغات", expanded=False):
    col_lang, col_duration = st.columns(2)
    with col_lang:
        lang_choice = st.selectbox("Language | اللغة:", ["English / الإنجليزية", "Chinese / الصينية", "Spanish / الإسبانية", "German / الألمانية"])
    with col_duration:
        learn_time = st.number_input("Duration (min) | المدة (دقيقة):", min_value=1, value=30)
    if st.button("Start Learning | ابدأ التعلم 📚"):
        ph_lang = st.empty()
        for t in range(learn_time * 60, 0, -1):
            m, s = divmod(t, 60)
            ph_lang.metric("Study Time | وقت الدراسة", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.balloons()

# --- 7. تنظيم النوم ---
with st.expander("🌙 Sleep Planner | مخطط النوم", expanded=False):
    st.write("Your brain needs **8 hours** of sleep. | يحتاج عقلك إلى **8 ساعات** من النوم.")
    wake_time = st.time_input("Wake-up goal | وقت الاستيقاظ:", value=datetime.strptime("07:00", "%H:%M").time(), key="sleep_p")
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

# --- 9. المهمات وإدارتها ---
st.subheader("📝 Tasks | المهمات")
c_t, c_p = st.columns([3, 1])
t_txt = c_t.text_input("Task name | اسم المهمة:", key="t_in")
t_prio = c_p.selectbox("Priority | الأولوية", ["Normal/عادي", "Urgent/عاجل", "Low/بسيط"])
t_tm = st.time_input("At | في وقت:", value=datetime.now().time(), key="t_tm_input")

if st.button("Add Task | إضافة مهمة 🚀"):
    if t_txt:
        p_em = "🔴" if "Urgent" in t_prio else "⚪" if "Normal" in t_prio else "🔵"
        st.session_state.my_tasks.append({"task": t_txt, "time": t_tm.strftime("%I:%M %p"), "prio": f"{p_em} {t_prio}", "done": False, "failed": False})
        st.rerun()

for idx, item in enumerate(st.session_state.my_tasks):
    with st.container():
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        task_display = f"✅ ~~{item['task']}~~" if item.get('done') else f"❌ *{item['task']} (Failed)*" if item.get('failed') else f"{item['prio']} **{item['task']}** | ⏰ {item['time']}"
        c1.markdown(task_display)
        if c2.button("✅", key=f"done_{idx}"):
            st.session_state.my_tasks[idx]['done'] = True
            st.session_state.my_tasks[idx]['failed'] = False
            st.rerun()
        if c3.button("❌", key=f"fail_{idx}"):
            st.session_state.my_tasks[idx]['done'] = False
            st.session_state.my_tasks[idx]['failed'] = True
            st.rerun()
        if c4.button("🗑️", key=f"del_{idx}"):
            st.session_state.my_tasks.pop(idx)
            st.rerun()

st.markdown("---")
# --- 10. الإنجازات ---
st.subheader("🏆 Achievements | الإنجازات")
ach = st.text_input("I am proud of | أنا فخور بـ:", key="ach_in")
if st.button("Record | تسجيل"):
    if ach:
        st.session_state.achievements.append(f"⭐ {ach} ({datetime.now().strftime('%H:%M')})")
        st.rerun()
for a in reversed(st.session_state.achievements): st.write(a)

# --- 11. التوقيع والرسالة التحفيزية (The Footer) ---
st.markdown(f"""
    <div class="footer">
        Designed by <b>Moutasem</b>. This app is built for your daily tasks—to wake up every day, set your goals, and win. 
        I am 100% sure you are capable of completing all your tasks! <b>Stay Strong! 💪⚡</b>
        <br><br>
        صمم هذا التطبيق من قبل <b>معتصم</b> للمهام اليومية؛ لتبدأ يومك بتحديد أهدافك وتحقيق الانتصارات.
        أنا متأكد تماماً أنك قادر على استكمال كل مهامك! <b>خليك قوي! 💪⚡</b>
    </div>
    """, unsafe_allow_html=True)
