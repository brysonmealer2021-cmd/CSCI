import streamlit as st
import pandas as pd
from supabase import create_client
import random
from datetime import datetime, timedelta

# 1. THE TOOLS
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 2. CUSTOM THEME (TEAL INJECTION)
st.markdown("""
    <style>
    :root {
        --teal-primary: #008080;
        --teal-light: #20b2aa;
        --teal-dark: #006666;
    }
    .stApp {
        color: #004d4d;
    }
    div.stButton > button {
        background-color: var(--teal-primary) !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: var(--teal-light) !important;
        color: white !important;
    }
    h1, h2, h3, .stSubheader {
        color: var(--teal-dark) !important;
        font-family: 'serif';
    }
    .stExpander {
        border: 1px solid var(--teal-primary) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. THE MEMORY
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steward_name' not in st.session_state:
    st.session_state.steward_name = ""
if 'steward_role' not in st.session_state:
    st.session_state.steward_role = ""
if 'blessing_received' not in st.session_state:
    st.session_state.blessing_received = False

# --- THE PRAYER RINGS ---
blessings_map = {
    "gay": [
        "O Lord Almighty, the Healer of our souls and bodies, who put down and raise up, visit Thy servant in her physical trial. Grant her patience and restore her to health.",
        "O Christ, who alone art our Defender, visit and heal Thy suffering servant. Deliver her from sickness and bitter pain, that she may sing to Thee.",
        "Holy Father, Physician of our souls and bodies, send down Thy healing power. Comfort her in her weakness and grant her the quiet strength to endure."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her the physical strength to run the race and the spiritual patience to guide her children.",
        "Establish the work of her hands, O Lord. Give her endurance in her body and stillness in her heart as she tends to her family.",
        "Most Holy Theotokos, thou who didst raise the Savior, guide this mother's daily labor. Multiply her strength and surround her house with grace."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family. Give her broad shoulders and a quiet mind.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom, unending patience, and rest from her heavy burdens.",
        "O Master, look upon the one who bears the yoke of leadership in this house. Grant her rest when she is tired, and steady hands when the decisions are heavy."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts and still the storms within.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind. Grant her a deep and abiding stillness today.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant. Bring her the gentle quiet of the Skete, that she may rest securely in God's care."
    ],
    "bryce": [
        "O Lord and Master of my life, grant the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch. Drive away all weariness of the flesh.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner. Grant me a quiet spirit to tend the elder today."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    return random.choice(blessings_map.get(name_key, ["Peace be to this house, and to all who dwell herein."]))

# 4. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    st.info(random.choice([
        "“Come to me, all who labor and are heavy laden, and I will give you rest.” — Matthew 11:28",
        "“Let not your heart be troubled, neither let it be afraid.” — John 14:27",
        "“Cast all your anxieties on Him, because He cares for you.” — 1 Peter 5:7"
    ]))
    name_input = st.text_input("Identify yourself:")
    pin_input = st.text_input("PIN:", type="password")
    if st.button("Cross the Threshold"):
        user_query = supabase.table("users").select("*").eq("username", name_input).eq("pin", pin_input).execute()
        if len(user_query.data) > 0:
            st.session_state.logged_in = True
            st.session_state.steward_name = user_query.data[0]['username']
            st.session_state.steward_role = user_query.data[0]['role']
            st.session_state.blessing_received = False
            st.session_state.daily_blessing = get_blessing(st.session_state.steward_name)
            st.rerun()

# 5. THE BLESSING GATE
elif not st.session_state.blessing_received:
    with st.container(border=True):
        st.subheader("☦️ A Blessing for the Watch")
        st.write(f"*{st.session_state.daily_blessing}*")
        if st.button("Amen", type="primary"):
            st.session_state.blessing_received = True
            st.rerun()

# 6. THE SACRED VIGIL
else:
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        dynamic_title, wt, wq = "🌅 The Morning Offering", "🌅 Morning Light", "“O Lord, grant me to greet the coming day in peace.”"
    elif 12 <= current_hour < 18:
        dynamic_title, wt, wq = "☀️ The Midday Labor", "☀️ Midday Labor", "“Establish the work of our hands upon us, O Lord.”"
    elif 18 <= current_hour < 21:
        dynamic_title, wt, wq = "🕯️ The Evening Sacrifice", "🕯️ Evening Watch", "“Let my prayer arise in Thy sight as incense.”"
    else:
        dynamic_title, wt, wq = "🌌 The Night Vigil", "🌌 Night Vigil", "“Behold, the Bridegroom comes at midnight; blessed is the servant whom He finds watching.”"

    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    st.sidebar.divider()
    st.sidebar.subheader(wt)
    st.sidebar.caption(f"*{wq}*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Jesus Prayer")
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me, a sinner.*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Trisagion")
    st.sidebar.caption("*Holy God, Holy Mighty, Holy Immortal, have mercy on us.*")
    
    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.rerun()

    st.title(f"☦️ {dynamic_title}")

    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady and your father is in good hands. The daily labor here is focused entirely on his comfort and honor, kept with deep respect under watchful eyes. You carry no burden of the work today—the steward's tools are set aside for you. The complete ledger is laid open below so you can trace the quiet history of his days and know he is well loved.")
    else:
        shift = st.radio("Select vigil:", ["Day", "Night", "Overnight"], horizontal=True)

        # --- NUTRITION & HYDRATION ---
        with st.expander("🍲 Nutrition & Hydration", expanded=True):
            forty_eight_ago = (datetime.now() - timedelta(hours=48)).isoformat()
            logs = supabase.table("care_logs").select("meal_info").gt("created_at", forty_eight_ago).execute()
            
            total_oz = 0
            food_entries = []
            for entry in logs.data:
                info = entry.get('meal_info', '')
                if info and "Drink:" in info:
                    try: total_oz += int(info.split('(')[1].split('oz')[0])
                    except: pass
                elif info and "Food:" in info:
                    try: food_entries.append(int(info.split('(')[1].split('%')[0]))
                    except: pass
            
            avg_food = int(sum(food_entries)/len(food_entries)) if food_entries else 0

            col_nut, col_hyd = st.columns(2)
            with col_nut:
                st.markdown(f"### 🍞 Nutrition ({avg_food}% 48h avg)")
                st.caption("“He satisfieth the longing soul, and filleth the hungry soul with goodness.” — Psalm 107:9")
                food_item = st.text_input("What was eaten?", key="food_input")
                food_p = st.slider("% Eaten", 0, 100, 0, 10)
                if st.button("Seal Nutrition"):
                    supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"meal_info":f"Food: {food_item} ({food_p}%)"}).execute()
                    st.rerun()

            with col_hyd:
                st.markdown(f"### 💧 Hydration ({total_oz}oz 48h total)")
                st.caption("“As the deer pants for the water brooks, so pants my soul for Thee, O God.”")
                drink_item = st.text_input("What was drunk?", key="drink_input")
                drink_oz = st.number_input("Amount (oz)", min_value=0, max_value=64, value=0, step=1)
                if st.button("Seal Hydration", type="primary"):
                    supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"meal_info":f"Drink: {drink_item} ({drink_oz}oz)"}).execute()
                    st.rerun()

        # --- VITALS & CONTINENCE ---
        with st.expander("🩺 Vitals", expanded=False):
            v1, v2, v3, v4 = st.columns(4)
            bp, hr, sp, gl = v1.text_input("Blood Pressure"), v2.text_input("Heart Rate"), v3.text_input("SpO2"), v4.text_input("Glucose")
            if st.button("Seal Vitals"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"bp":bp,"hr":hr,"spo2":sp,"glucose":gl}).execute()

        with st.expander("🕒 Continence Round", expanded=False):
            bm_ur = st.radio("Output:", ["None", "Urine", "Bowel Movement", "Both"], horizontal=True)
            det = st.text_input("Details of Output:")
            if st.button("Seal Continence"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"output_type":bm_ur,"output_details":det}).execute()

        # --- GENERAL CARE & MEDS ---
        st.header("💊 General Care & Medications")
        with st.container(border=True):
            if shift == "Day":
                st.markdown("**Scheduled Meds**")
                st.checkbox("Potassium Chloride (10 MEQ)"); st.checkbox("Citalopram (20 mg)"); st.checkbox("Furosemide (20 mg)")
                st.checkbox("Lantus (20 units)"); st.checkbox("Aspirin/Metoprolol (Aspirin 81mg/Metoprolol 25mg)"); st.checkbox("Dorzolamide/Timolol Drops")
            elif shift == "Night":
                st.markdown("**Scheduled Meds**")
                st.checkbox("Magnesium Oxide (400 mg)"); st.checkbox("Oxybutynin (5 mg)"); st.checkbox("Donepezil (10 mg)")
                st.checkbox("Finasteride (5 mg) / Melatonin (5 mg)"); st.checkbox("Latanoprost Drops")

            st.markdown("**➕ PRN (As Needed)**")
            p1, p2, p3 = st.columns(3)
            with p1: 
                st.checkbox("Phenazopyridine"); st.checkbox("Acetaminophen (500 mg)"); st.checkbox("Guaifenesin")
            with p2: 
                st.checkbox("Novolog Insulin"); st.checkbox("Diclofenac Sodium Gel")
            with p3: 
                st.checkbox("Ondansetron (4 mg)"); st.checkbox("Pantoprazole (40 mg)")

            st.divider()
            st.markdown("**🧹 Daily Hygiene**")
            st.checkbox("Oral Care / Dentures Checked"); st.checkbox("Bathing / Grooming / Dressing")
            st.checkbox("Laundry Gathered / Surfaces Wiped"); st.checkbox("Room Tidied / Trash Emptied")

            care_notes = st.text_area("Detailed Care Notes for the Daughters:")
            if st.button("Seal the General Ledger"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"medications":"Daily Routine/PRN Administered","notes":care_notes}).execute()
                st.success("The ledger has been sealed.")

    # --- HISTORY ---
    st.divider()
    st.header("📜 Vigil History")
    recent = supabase.table("care_logs").select("*").order("created_at", desc=True).limit(50).execute()
    if recent.data:
        df = pd.DataFrame(recent.data)
        if 'created_at' in df.columns:
            df['created_at
