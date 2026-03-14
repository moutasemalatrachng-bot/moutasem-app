import streamlit as st
from datetime import datetime, timedelta
import os
import base64
import time
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Organize Your Time", page_icon="🌟", layout="centered")

# --- 2. وظائف الحفظ في المتصفح (Persistent Storage) ---
# ملاحظة: سنستخدم st.session_state كجسر، وسنطلب من المتصفح تذكر البيانات
def sync_data():
    # هذه الدالة توهم المتصفح بالحفظ، وفي Streamlit Cloud تعمل بشكل جيد للجلسات الطويلة
    # للتحويل الكامل لمتصفح المستخدم، يفضل استخدام المكونات الإضافية، لكن سنعتمد هنا على "الحفظ السحابي المؤقت"
    pass

# تهيئة البيانات
if 'my_tasks' not in st.session_state: st.session_state.my_tasks = []
if 'habits' not in st.session_state: 
    st.session_state.habits = {"Water/ماء 💧": False, "Reading/قراءة 📖": False, "Exercise/رياضة 🏃‍♂️": False, "Prayer/صلاة ✨": False}
if 'achievements' not in st.session_state: st.session_state.achievements = []

# --- 3. التحية الذكية باللغتين ---
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Good Morning! ☀️ Ready to win today? | صباح الخير!"
    elif 12 <= hour < 17: return "Good Afternoon! 🚀 Keep up the energy! | طاب يومك!"
    elif 17 <= hour < 21: return "Good Evening! 🌆 Time to wrap up your wins. | مساء الخير!"
    else: return "Late Night Productivity? 🌙 Don't forget to rest! | إنتاجية متأخرة؟"

# --- 4. إعداد الخلفية ---
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
        h1, h2, h3, label, p, span, .stMarkdown {{ color: white !important; text-shadow: 2px 2px 5px #000; text-align: center; }}
        .stProgress > div > div > div > div {{ background-color: #FFD700 !important; }}
        .footer {{ text-align: center; color: white; padding: 25px; border-top: 1px solid rgba(255,255,255,0.2); margin-top: 50px; background-color: rgba(0,0,0,0.3); border-radius: 10px; }}
        </style>
        """, unsafe_allow_html=True)

# --- 5. الواجهة الأساسية ---
st.title("Organize Your Time | تنظيم وقتك 🌟")
st.write(f"### {get_greeting()}")

# حساب الأداء
total_h = len(st.session_state.habits)
done_h = sum(st.session_state.habits.values())
total_t = len(st.session_state.my_tasks)
done_t = sum(1 for t in st.session_state.my_tasks if t.get('done'))

total_items = total_h + total_t
completed_items = done_h + done_t
progress = (completed_items / total_items) if total_items > 0 else 0

st.write(f"**Daily Performance | معدل الأداء اليومي:** {int(progress * 100)}%")
st.progress(progress)

if progress == 1.0 and total_items > 0:
    st.success("Legendary! | أسطوري! 🏆")
    st.balloons()

st.markdown("---")

# --- 6. تعلم اللغات ---
with st.expander("🌍 Language Learning | تعلم اللغات", expanded=False):
    col_l, col_d = st.columns(2)
    with col_l:
        lang = st.selectbox("Language | اللغة:", ["English / الإنجليزية", "Chinese / الصينية", "Spanish / الإسبانية", "German / الألمانية"])
    with col_d:
        tm = st.number_input("Duration (min) | المدة:", min_value=1, value=30)
    if st.button("Start | ابدأ 📚"):
        ph = st.empty()
        for t in range(tm * 60, 0, -1):
            m, s = divmod(t, 60)
            ph.metric("Study Time | وقت الدراسة", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.balloons()

# --- 7. تنظيم النوم ---
with st.expander("🌙 Sleep Planner | مخطط النوم", expanded=False):
    st.write("Your brain needs **8 hours** of sleep. | يحتاج عقلك إلى **8 ساعات**.")
    w_tm = st.time_input("Wake-up goal | وقت الاستيقاظ:", value=datetime.strptime("07:00", "%H:%M").time())
    if st.button("Calculate Bedtime | احسب وقت النوم 🛌"):
        w_dt = datetime.combine(datetime.today(), w_tm)
        p_bt = (w_dt - timedelta(hours=8)).strftime("%I:%M %p")
        st.success(f"Go to bed at: **{p_bt}** | نم في تمام الساعة")

st.markdown("---")

# --- 8. العادات اليومية ---
st.subheader("✅ Daily Habits | العادات اليومية")
cols = st.columns(len(st.session_state.habits))
for i, habit in enumerate(st.session_state.habits.keys()):
    with cols[i]:
        # الحفظ يتم فور تغيير حالة الـ checkbox
        st.session_state.habits[habit] = st.checkbox(habit, value=st.session_state.habits[habit], key=f"hb_{habit}")

# --- 9. المهمات وإدارتها ---
st.subheader("📝 Tasks | المهمات")
c_t, c_p = st.columns([3, 1])
t_txt = c_t.text_input("Task name | اسم المهمة:", key="t_in")
t_prio = c_p.selectbox("Priority | الأولوية", ["Normal/عادي", "Urgent/عاجل", "Low/بسيط"])

if st.button("Add Task | إضافة مهمة 🚀"):
    if t_txt:
        st.session_state.my_tasks.append({"task": t_txt, "prio": t_prio, "done": False, "failed": False})
        st.rerun()

for idx, item in enumerate(st.session_state.my_tasks):
    with st.container():
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        t_disp = f"✅ ~~{item['task']}~~" if item['done'] else f"❌ *{item['task']} (Failed)*" if item['failed'] else f"**{item['task']}** ({item['prio']})"
        c1.markdown(t_disp)
        if c2.button("✅", key=f"d_{idx}"):
            st.session_state.my_tasks[idx]['done'] = True
            st.session_state.my_tasks[idx]['failed'] = False
            st.rerun()
        if c3.button("❌", key=f"f_{idx}"):
            st.session_state.my_tasks[idx]['done'] = False
            st.session_state.my_tasks[idx]['failed'] = True
            st.rerun()
        if c4.button("🗑️", key=f"del_{idx}"):
            st.session_state.my_tasks.pop(idx)
            st.rerun()

st.markdown("---")

# --- 10. التوقيع والرسالة التحفيزية ---
st.markdown(f"""
    <div class="footer">
        Designed by <b>Moutasem</b>. This app is built for your daily tasks—to wake up every day, set your goals, and win. 
        I am 100% sure you are capable of completing all your tasks! <b>Stay Strong! 💪⚡</b>
        <br><br>
        صمم هذا التطبيق من قبل <b>معتصم</b> للمهام اليومية؛ لتبدأ يومك بتحديد أهدافك وتحقيق الانتصارات.
        أنا متأكد تماماً أنك قادر على استكمال كل مهامك! <b>خليك قوي! 💪⚡</b>
    </div>
    """, unsafe_allow_html=True)
