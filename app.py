import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="ক্লিনিক্যাল ডিসিশন সাপোর্ট সিস্টেম", page_icon="🩺", layout="wide")

# App Header
st.title("🩺 ডিজিটাল ডায়াগনসিস ও ট্রিটমেন্ট সাপোর্ট সিস্টেম (CDSS)")
st.subheader("প্রাথমিক রোগ নির্ণয়, ল্যাব টেস্ট অ্যানালাইসিস এবং চিকিৎসা গাইডলাইন")
st.write("---")

# 1. Database Creation (Based on Excel Logic)
disease_data = {
    "ডেঙ্গু (Dengue)": {
        "symptoms": "তীব্র জ্বর, চোখের পেছনে ব্যথা, শরীরে লাল র‍্যাশ, তীব্র জয়েন্ট পেইন।",
        "test": "Dengue NS1 Antigen / CBC (Platelet Count)",
        "criteria": "NS1 Positive অথবা Platelet < 100,000",
        "treatment": "১. সম্পূর্ণ বেড রেস্ট।\n২. প্রচুর তরল খাবার ও খাবার স্যালাইন (ORSaline) পান করা।\n৩. জ্বর ও ব্যথার জন্য শুধু Paracetamol (500mg-1g) সর্বোচ্চ দিনে ৪ বার। (🚨 কোনোভাবেই NSAID বা ব্যথানাশক যেমন Ibuprofen/Diclofenac দেওয়া যাবে না)।"
    },
    "টাইফয়েড (Typhoid)": {
        "symptoms": "ধাপ-ধাপ জ্বর বৃদ্ধি, কোষ্ঠকাঠিন্য বা ডায়রিয়া, লিভার ও প্লীহা বড় হওয়া।",
        "test": "Typhidot (IgM/IgG) / Blood Culture",
        "criteria": "Typhidot IgM Positive",
        "treatment": "১. পর্যাপ্ত পানি ও পুষ্টিকর তরল খাবার।\n২. রেজিস্টার্ড ডাক্তারের পরামর্শে অ্যান্টিবায়োটিক (যেমন: Azithromycin বা Cefixime) কোর্স সম্পন্ন করা।\n৩. জ্বরের জন্য Paracetamol।"
    },
    "রক্তস্বল্পতা (Anemia)": {
        "symptoms": "দুর্বলতা, ফ্যাকাশে চামড়া, অল্প পরিশ্রমে হাঁপিয়ে যাওয়া, মাথা ঘোরা।",
        "test": "Hemoglobin (Hb) Level (CBC)",
        "criteria": "Hb < 12 g/dL (নারী) অথবা < 13.5 g/dL (পুরুষ)",
        "treatment": "১. আয়রন ও ফলিক অ্যাসিড সমৃদ্ধ খাবার (কলা, কচুশাক, কলিজা, ডিম) খাওয়া।\n২. চিকিৎসকের পরামর্শে Iron Supplement বা সিরাপ সেবন করা।\n৩. ভিটামিন সি যুক্ত খাবার খাওয়া (যা আয়রন শোষণ বাড়ায়)।"
    },
    "ইউটিআই (UTI - Urinary Tract Infection)": {
        "symptoms": "প্রস্রাবে তীব্র জ্বালাপোড়া, ঘন ঘন প্রস্রাবের বেগ, তলপেটে ব্যথা, হালকা জ্বর।",
        "test": "Urine RE (Routine Examination) / Culture",
        "criteria": "Pus Cells > 5-10 / HPF",
        "treatment": "১. প্রতিদিন ৩-৪ লিটার পানি পান করা।\n২. ক্র্যানবেরি জুস খাওয়া উপকারী।\n৩. চিকিৎসকের পরামর্শে নির্দিষ্ট অ্যান্টিবায়োটিক (যেমন: Nitrofurantoin বা Ciprofloxacin) সঠিক ডোজে খাওয়া।"
    },
    "উচ্চ রক্তচাপ (Hypertension)": {
        "symptoms": "ঘাড়ের পেছনে ব্যথা, মাথা ঘোরা, বুক ধড়ফড় করা, অনিদ্রা।",
        "test": "BP Measurement (Sphygmomanometer)",
        "criteria": "Systolic ≥ 140 mmHg অথবা Diastolic ≥ 90 mmHg",
        "treatment": "১. খাবারে কাঁচা লবণ সম্পূর্ণ বন্ধ করা।\n২. চর্বিযুক্ত খাবার এড়িয়ে চলা এবং প্রতিদিন ৩০ মিনিট হাঁটা।\n৩. চিকিৎসকের পরামর্শ অনুযায়ী নিয়মিত প্রেশারের ওষুধ (যেমন: Amlodipine বা Losartan) নির্দিষ্ট সময়ে সেবন।"
    },
    "গ্যাস্ট্রিক (Peptic Ulcer)": {
        "symptoms": "বুক জ্বালাপোড়া করা, খালি পেটে বা ভরা পেটে পেটের উপরিভাগে তীব্র ব্যথা, টক ঢেকুর।",
        "test": "Endoscopy of UGI / H. Pylori Stool Antigen",
        "criteria": "H. Pylori Positive বা Endoscopy তে Ulcer ধরা পড়া",
        "treatment": "১. ভাজা পোড়া, ঝাল এবং তৈলাক্ত খাবার সম্পূর্ণ বর্জন করা।\n২. সময়মতো খাবার খাওয়া এবং খালি পেটে না থাকা।\n৩. চিকিৎসকের পরামর্শে Antacid এবং PPI (যেমন: Esomeprazole বা Omeprazole) খাবারের ২০ মিনিট আগে সেবন।"
    }
}

# 2. Sidebar - Patient Info
st.sidebar.header("👤 রোগীর তথ্য (Patient Profile)")
patient_name = st.sidebar.text_input("রোগীর নাম", placeholder="উদা: আব্দুল করিম")
patient_age = st.sidebar.number_input("বয়স", min_value=1, max_value=120, value=30)
patient_gender = st.sidebar.selectbox("লিঙ্গ", ["পুরুষ", "নারী", "অন্যান্য"])

# 3. Step 1: Preliminary Screening
st.header("📋 ধাপ ১: প্রাথমিক স্ক্রিনিং ও টেস্ট সিলেকশন")
selected_disease = st.selectbox("সম্ভাব্য রোগটি নির্বাচন করুন:", list(disease_data.keys()))

if selected_disease:
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**🚨 প্রধান প্রধান লক্ষণসমূহ:**\n\n{disease_data[selected_disease]['symptoms']}")
    with col2:
        st.warning(f"**🔬 প্রয়োজনীয় ল্যাব টেস্ট:**\n\n**{disease_data[selected_disease]['test']}**\n\n*(পজিটিভ মানদণ্ড: {disease_data[selected_disease]['criteria']})*")

st.write("---")

# 4. Step 2: Lab Report Input
st.header("🧪 ধাপ ২: ল্যাব রিপোর্টের ফলাফল ইনপুট")
st.write(f"অনুগ্রহ করে **{disease_data[selected_disease]['test']}** এর রিপোর্ট চেক করুন।")

report_status = st.radio(
    "রিপোর্টের ফলাফল কি পজিটিভ / নির্ধারিত মানদণ্ডের বাইরে এসেছে?",
    ("নির্বাচন করুন...", "হ্যাঁ (Positive / Out of Range)", "না (Negative / Normal)"),
    index=0
)

st.write("---")

# 5. Step 3: Final Diagnosis & Medical Guidelines
st.header("💊 ধাপ ৩: চূড়ান্ত ডায়াগনসিস ও চিকিৎসাপত্র গাইডলাইন")

if report_status == "হ্যাঁ (Positive / Out of Range)":
    st.success(f"### 🎯 চূড়ান্ত রোগ: {selected_disease} নিশ্চিত (CONFIRMED)")
    
    st.markdown("### 📝 প্রাথমিক চিকিৎসা নির্দেশিকা (First-line Treatment Guidelines):")
    st.code(disease_data[selected_disease]['treatment'], language="markdown")
    
    # Medical Disclaimer Footer inside app
    st.error("**⚠️ সতর্কতা ও ডিসক্লেইমার:** এই অ্যাপ্লিকেশনটি শুধুমাত্র প্রাথমিক ধারণা এবং লজিক টেস্টের জন্য তৈরি। রোগীর সুনির্দিষ্ট অ্যান্টিবায়োটিক ও অন্যান্য ওষুধের সঠিক ডোজ নির্ধারণের জন্য অবশ্যই একজন রেজিস্টার্ড এমবিবিএস (MBBS) চিকিৎসকের সরাসরি পরামর্শ ও প্রেসক্রিপশন নিতে হবে।")

elif report_status == "না (Negative / Normal)":
    st.info("### ℹ️ ডায়াগনসিস: ল্যাব রিপোর্ট নরমাল এসেছে।")
    st.write("লক্ষণ থাকা সত্ত্বেও ল্যাব রিপোর্ট নেগেটিভ আসলে অন্য কোনো রোগের উপস্থিতি থাকতে পারে। অনুগ্রহ করে চিকিৎসকের শরণাপন্ন হোন।")
else:
    st.write("*ল্যাপ রিপোর্টের ফলাফল ইনপুট দিলে এখানে স্বয়ংক্রিয়ভাবে চিকিৎসার বিবরণ চলে আসবে।*")
