import streamlit as st

# Page Configuration
st.set_page_config(page_title="ডিজিটাল ডায়াগনসিস ও ট্রিটমেন্ট সাপোর্ট", page_icon="🩺", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main-title { font-size:28px !important; font-weight: bold; color: #1E3A8A; text-align: center; }
    .section-header { font-size:20px !important; font-weight: bold; color: #0F766E; margin-top: 20px; }
    .report-card { padding: 15px; border-radius: 10px; background-color: #F3F4F6; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# ----------------- MULTI-USER DATABASE -----------------
# 🚨 এখানে আপনি যত খুশি নতুন ইউজার আইডি এবং পাসওয়ার্ড যোগ করতে পারবেন
USERS_DATABASE = {
    "admin": {"name": "অ্যাডমিন (প্রধান ডাক্তার)", "password": "doctor123"},
    "razu": {"name": "Razu", "password": "razu556"},
    "assistant_1": {"name": "অ্যাসিস্ট্যান্ট ১", "password": "pass789"}
}

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user_name" not in st.session_state:
    st.session_state.current_user_name = ""

# Login Form Function
def login_page():
    st.markdown('<p class="main-title">🔐 মাল্টি-ইউজার লগইন সিস্টেম</p>', unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns()
    with col2:
        with st.form("login_form"):
            st.subheader("আপনার নিজস্ব আইডি দিয়ে লগইন করুন")
            user_id = st.text_input("ইউজার আইডি (User ID)", placeholder="আপনার আইডি লিখুন")
            password = st.text_input("পাসওয়ার্ড (Password)", type="password", placeholder="******")
            submit_button = st.form_submit_button("লগইন করুন")
            
            if submit_button:
                # Check if user exists and password matches
                if user_id in USERS_DATABASE and USERS_DATABASE[user_id]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user_name = USERS_DATABASE[user_id]["name"]
                    st.rerun()
                else:
                    st.error("❌ ভুল ইউজার আইডি অথবা পাসওয়ার্ড! আবার চেষ্টা করুন।")

# Logout Handler
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user_name = ""
    st.rerun()

# ----------------- MAIN APP ARCHITECTURE -----------------
if not st.session_state.logged_in:
    login_page()
else:
    # Top Bar with Logged-in User Info & Logout Button
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.markdown('<p class="main-title">🩺 ডিজিটাল ডায়াগনসিস ও ট্রিটমেন্ট সিস্টেম (Advanced CDSS)</p>', unsafe_allow_html=True)
        st.write(f"👋 স্বাগতম, **{st.session_state.current_user_name}**")
    with col_logout:
        if st.button("🚪 লগআউট"):
            logout()
            
    st.write("---")

    # 1. Sidebar - Patient Profile
    st.sidebar.header("👤 রোগীর তথ্য (Patient Profile)")
    patient_name = st.sidebar.text_input("রোগীর নাম", value="আব্দুল করিম")
    patient_age = st.sidebar.number_input("বয়স", min_value=1, max_value=120, value=35)
    patient_gender = st.sidebar.selectbox("লিঙ্গ", ["পুরুষ", "নারী", "অন্যান্য"])

    # 2. Disease Selector
    st.markdown('<p class="section-header">📋 ধাপ ১: প্রাথমিক স্ক্রিনিং ও টেস্ট সিলেকশন</p>', unsafe_allow_html=True)
    diseases = [
        "ডেঙ্গু (Dengue Fever)", 
        "রক্তস্বল্পতা (Anemia)", 
        "ইউটিআই (UTI)", 
        "উচ্চ রক্তচাপ (Hypertension)",
        "জন্ডিস (Acute Jaundice / Hepatitis)",
        "হার্ট অ্যাটাক (Acute Myocardial Infarction - Emergency)"
    ]
    selected_disease = st.selectbox("সম্ভাব্য রোগটি নির্বাচন করুন:", diseases)

    # 3. Dynamic Logic Based on Selection
    if selected_disease == "ডেঙ্গু (Dengue Fever)":
        st.info("**🚨 প্রধান লক্ষণ:** তীব্র জ্বর, চোখের পেছনে ব্যথা, শরীরে লাল র‍্যাশ, জয়েন্ট পেইন।")
        st.warning("**🔬 প্রয়োজনীয় ল্যাব টেস্ট:** CBC (Platelet Count) এবং Dengue NS1 Antigen")
        
        st.markdown('<p class="section-header">🧪 ধাপ ২: ল্যাব রিপোর্টের সঠিক মান ইনপুট দিন</p>', unsafe_allow_html=True)
        ns1 = st.selectbox("Dengue NS1 Antigen এর ফলাফল কী?", ["Select...", "Positive", "Negative"])
        platelet = st.number_input("Platelet Count (প্লেটলেট সংখ্যা) লিখুন:", min_value=1000, max_value=600000, value=150000, step=1000)
        
        is_positive = (ns1 == "Positive") or (platelet < 100000)
        criteria_msg = f"NS1: {ns1}, Platelet: {platelet:,}"
        treatment = """১. সম্পূর্ণ বেড রেস্ট এবং প্রতি ২ ঘণ্টা পর পর তরল খাবার (ডাবের পানি, জুস, খাবার স্যালাইন) পান করা।
২. শুধু Paracetamol (500mg বা 665mg) সর্বোচ্চ দিনে ৪ বার। (🚨 কোনো অবস্থাতেই ব্যথানাশক যেমন Ibuprofen/Diclofenac বা Aspirin দেওয়া যাবে না)।
৩. প্লেটলেট ৫০ হাজারের নিচে নামলে বা মাড়ি/নাক দিয়ে রক্তপাত হলে দ্রুত হাসপাতালে ভর্তি করুন।"""

    elif selected_disease == "রক্তস্বল্পতা (Anemia)":
        st.info("**🚨 প্রধান লক্ষণ:** শরীর ফ্যাকাশে হওয়া, প্রচণ্ড দুর্বলতা, অল্পতে হাঁপিয়ে যাওয়া, মাথা ঘোরা।")
        st.warning("**🔬 প্রয়োজনীয় ল্যাব টেস্ট:** Hemoglobin (Hb) Level (CBC রিপোর্ট থেকে)")
        
        st.markdown('<p class="section-header">🧪 ধাপ ২: ল্যাব রিপোর্টের সঠিক মান ইনপুট দিন</p>', unsafe_allow_html=True)
        hb_level = st.number_input("হিমোগ্লোবিন (Hb) এর মান লিখুন (g/dL):", min_value=1.0, max_value=20.0, value=13.0, step=0.1)
        
        if patient_gender == "নারী":
            is_positive = hb_level < 12.0
        else:
            is_positive = hb_level < 13.5
        criteria_msg = f"হিমোগ্লোবিনের মান: {hb_level} g/dL"
        treatment = """১. আয়রন সমৃদ্ধ খাবার (কলিজা, ডিমের কুসুম, কচুশাক, ডালিম, আপেল) বেশি খেতে হবে।
২. চিকিৎসকের পরামর্শ অনুযায়ী Iron Supplement (ক্যাপসুল বা সিরাপ) এবং সাথে Vitamin C খেতে হবে (যা আয়রন শোষণ বাড়ায়)।
৩. কৃমির সংক্রমণ থাকলে চিকিৎসকের পরামর্শে এন্টেলমিন্টিক (কৃমির ওষুধ) সেবন করতে হবে।"""

    elif selected_disease == "ইউটিআই (UTI)":
        st.info("**🚨 প্রধান লক্ষণ:** প্রস্রাবে তীব্র জ্বালাপোড়া, তলপেটে ব্যথা, ঘন ঘন প্রস্রাবের বেগ, হালকা জ্বর।")
        st.warning("**🔬 প্রয়োজনীয় ল্যাব টেস্ট:** Urine RE (Routine Examination)")
        
        st.markdown('<p class="section-header">🧪 ধাপ ২: ল্যাব রিপোর্টের সঠিক মান ইনপুট দিন</p>', unsafe_allow_html=True)
        pus_cells = st.number_input("Urine RE রিপোর্টে Pus Cells এর সংখ্যা কত? (per HPF):", min_value=0, max_value=100, value=3)
        
        is_positive = pus_cells > 5
        criteria_msg = f"Pus Cells: {pus_cells}/HPF"
        treatment = """১. দৈনিক ৩ থেকে ৪ লিটার নিরাপদ পানি পান নিশ্চিত করতে হবে।
২. প্রস্রাব দীর্ঘক্ষণ চেপে রাখা যাবে না এবং ব্যক্তিগত পরিচ্ছন্নতা বজায় রাখতে হবে।
৩. চিকিৎসকের পরামর্শ অনুযায়ী একটি নির্দিষ্ট অ্যান্টিবায়োটিক (যেমন: Nitrofurantoin) এর পূর্ণ কোর্স সম্পন্ন করতে হবে।"""

    elif selected_disease == "উচ্চ রক্তচাপ (Hypertension)":
        st.info("**🚨 প্রধান লক্ষণ:** ঘাড়ের পেছনে ব্যথা, মাথা ঘোরানো, বুক ধড়фড় করা, রাতে ঘুম না হওয়া।")
        st.warning("**🔬 প্রয়োজনীয় টেস্ট:** প্রেশার মাপার মেশিন (Sphygmomanometer) দিয়ে ৩ বার রিডিং নিন।")
        
        st.markdown('<p class="section-header">🧪 ধাপ ২: টেস্টের সঠিক মান ইনপুট দিন</p>', unsafe_allow_html=True)
        systolic = st.number_input("Systolic (উপরের প্রেশার) mmHg:", min_value=70, max_value=250, value=120)
        diastolic = st.number_input("Diastolic (নিচের প্রেশার) mmHg:", min_value=40, max_value=150, value=80)
        
        is_positive = (systolic >= 140) or (diastolic >= 90)
        criteria_msg = f"BP: {systolic}/{diastolic} mmHg"
        treatment = """১. তরকারিতে বা ভাতে বাড়তি কাঁচা লবণ খাওয়া সম্পূর্ণ বন্ধ করতে হবে।
২. চর্বিযুক্ত ও তৈলাক্ত খাবার (খাসি/গরুর মাংস, ডালডা) পরিহার করতে হবে এবং দৈনিক ৩০ মিনিট দ্রুত হাঁটতে হবে।
৩. প্রেশার নিয়ন্ত্রণে না এলে ডাক্তারের পরামর্শে নিয়মিত Antihypertensive ওষুধ (যেমন: Amlodipine) শুরু করতে হবে এবং কখনোই ওষুধ নিজে থেকে বন্ধ করা যাবে না।"""

    elif selected_disease == "জন্ডিস (Acute Jaundice / Hepatitis)":
        st.info("**🚨 প্রধান লক্ষণ:** চোখ ও প্রস্রাব হলুদ হওয়া, খাবারে তীব্র অরুচি, বমি বমি ভাব, ডান পেটের উপরিভাগে ব্যথা।")
        st.warning("**🔬 প্রয়োজনীয় ল্যাব টেস্ট:** Serum Bilirubin এবং SGPT (ALT)")
        
        st.markdown('<p class="section-header">🧪 ধাপ ২: ল্যাব রিপোর্টের সঠিক মান ইনপুট দিন</p>', unsafe_allow_html=True)
        bilirubin = st.number_input("Serum Bilirubin এর মান লিখুন (mg/dL):", min_value=0.1, max_value=30.0, value=1.0, step=0.1)
        
        is_positive = bilirubin > 1.2
        criteria_msg = f"Bilirubin: {bilirubin} mg/dL"
        treatment = """১. সম্পূর্ণ শারীরিক ও মানসিক বিশ্রামে থাকতে হবে (Bed Rest)।
২. তেল-মসলা ছাড়া সহজপাচ্য শর্বরা জাতীয় খাবার খেতে হবে। (🚨 কবিরাজি ওষুধ বা অতিরিক্ত ডাবের পানি/আখের রস খাওয়া থেকে বিরত থাকুন)।
৩. বমি বা তীব্র পেট ব্যথা থাকলে অবিলম্বে হাসপাতালে নিয়ে সিরাম মার্কার টেস্ট (HBsAg, Anti-HAV) করাতে হবে।"""

    elif selected_disease == "হার্ট অ্যাটাক (Acute Myocardial Infarction - Emergency)":
        st.info("**🚨 প্রধান লক্ষণ:** বুকের মাঝখানে প্রচণ্ড ভারী বা মোচড়ানো ব্যথা, যা বাম হাত, ঘাড় বা চোয়ালে ছড়ায়; সাথে ঠাণ্ডা ঘাম ও শ্বাসকষ্ট।")
        st.warning("**🔬 প্রয়োজনীয় টেস্ট:** ইমার্জেন্সি ECG এবং Troponin-I টেস্ট।")
        
        st.markdown('<p class="section-header">🧪 ধাপ ২: ল্যাব ও ক্লিনিক্যাল লক্ষণ ইনপুট দিন</p>', unsafe_allow_html=True)
        ecg_change = st.selectbox("ECG রিপোর্টে কি ST-Elevation বা কোনো পরিবর্তন আছে?", ["Select...", "Yes - Ischemia/Infarction", "No Change"])
        troponin = st.number_input("Troponin-I এর মান লিখুন (ng/mL):", min_value=0.0, max_value=50.0, value=0.01, step=0.01)
        
        is_positive = (ecg_change == "Yes - Ischemia/Infarction") or (troponin > 0.04)
        criteria_msg = f"ECG: {ecg_change}, Troponin: {troponin} ng/mL"
        treatment = """🚨 এটি একটি মেডিকেল ইমার্জেন্সি! অবিলম্বে রোগীকে সিসিইউ (CCU) সুবিধাযুক্ত কার্ডিয়াক হাসপাতালে স্থানান্তর করুন।
প্রাথমিক ফার্স্ট-এইড (ডাক্তারের পরামর্শ সাপেক্ষে):
১. Tab. Aspirin 300mg + Tab. Clopidogrel 300mg একসাথে চিবিয়ে খাইয়ে দিন।
