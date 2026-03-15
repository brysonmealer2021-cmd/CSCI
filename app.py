import streamlit as st
import pandas as pd
from supabase import create_client
import random
from datetime import datetime, timedelta

# 1. THE TOOLS
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 2. THE TEAL BUTTONS (ONLY)
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #008080 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #20b2aa !important;
        color: white !important;
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
        "O Lord Almighty, the Healer of our souls and bodies, visit Thy servant in her physical trial. Grant her patience and restore her to health.",
        "O Christ, who alone art our Defender, visit and heal Thy suffering servant. Deliver her from sickness and bitter pain.",
        "Holy Father, Physician of our souls and bodies, send down Thy healing power. Comfort her in her weakness."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her the physical strength to run the race.",
        "Establish the work of her hands, O Lord. Give her endurance in her body and stillness in her heart.",
        "Most Holy Theotokos, guide this mother's daily labor. Multiply her strength and surround her house with grace."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom and unending patience.",
        "O Master, look upon the one who bears the yoke of leadership. Grant her rest when she is tired."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind. Grant her deep stillness.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant. Bring her the gentle quiet of the Skete."
    ],
    "bryce": [
        "O Lord and Master of my life, grant the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner. Grant me a quiet spirit to tend the elder."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    return random.choice(blessings_map.get(name_key, ["Peace be to this house."]))

# 4. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    name_input = st.text_input("Identify yourself:")
    pin_input = st.text_input("PIN:", type="password")
    if st.button("Cross the Threshold"):
        try:
            user_query = supabase.table("users").select("*").eq("username", name_input).eq("pin", pin_input).execute()
            if user_query.data:
                st.session_state.logged_in = True
                st.session_state.steward_name = user_query.data[0]['username']
                st.session_state.steward_role = user_query.data[0]['role']
                st.session_state.blessing_received = False
                st.session_state.daily_blessing = get_blessing(st.session_state.steward_name)
                st.rerun()
            else:
                st.error("The threshold remains barred.")
        except Exception as e:
            st.error(f"Connection error: {e}")

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
        dynamic_title, wt, wq = "🌌 The Night Vigil", "🌌 Night Vigil", "“Behold, the Bridegroom comes at midnight.”"

    # --- SIDEBAR PRAYERS ---
    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Jesus Prayer")
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me, a sinner.*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Trisagion")
    st.sidebar.caption("*Holy God, Holy Mighty, Holy Immortal, have mercy on us.*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ St. Ephrem")
    st.sidebar.caption("*O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk. But give rather the spirit of chastity, humility, patience, and love to Thy servant.*")
    
    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.rerun()

    st.title(f"☦️ {dynamic_title}")

    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady. You carry no burden of the work today.")
    else:
        shift = st.radio("Select vigil:", ["Day", "Night", "Overnight"], horizontal=True)

        # --- NUTRITION & HYDRATION ---
        with st.expander("🍲 Nutrition & Hydration", expanded=True):
            st.caption(random.choice([
                "“He satisfieth the longing soul, and filleth the hungry soul with goodness.” — Ps 107:9",
                "“Whether you eat or drink, do all to the glory of God.”",
                "“The eyes of all look to Thee with hope, and Thou givest them their food in due season.”"
            ]))
            forty_eight_ago = (datetime.now() - timedelta(hours=48)).isoformat()
            try:
                logs = supabase.table("care_logs").select("meal_info").gt("created_at", forty_eight_ago).execute()
                data_list = logs.data if logs.data else []
            except:
                data_list = []
            
            total_oz = 0
            for entry in data_list:
                info = entry.get('meal_info', '')
                if info and "Drink:" in info:
                    try: total_oz += int(info.split('(')[1].split('oz')[0])
                    except: pass
            
            col_nut, col_hyd = st.columns(2)
            with col_nut:
                st.markdown("### 🍞 Nutrition")
                food_item = st.text_input("What was eaten?", key="f_in")
                food_p = st.slider("% Eaten", 0, 100, 0, 10)
                if st.button("Seal Nutrition"):
                    supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"meal_info":f"Food: {food_item} ({food_p}%)"}).execute()
                    st.rerun()

            with col_hyd:
                st.markdown(f"### 💧 Hydration ({total_oz}oz total)")
                drink_item = st.text_input("What was drunk?", key="d_in")
                drink_oz = st.number_input("Amount (oz)", min_value=0, max_value=64, value=0, step=1)
                if st.button("Seal Hydration"):
                    supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"meal_info":f"Drink: {drink_item} ({drink_oz}oz)"}).execute()
                    st.rerun()

        # --- VITALS & CONTINENCE ---
        with st.expander("🩺 Vitals", expanded=False):
            st.caption("“A man ought to take heed to his own measure.”")
            v1, v2, v3, v4 = st.columns(4)
            bp, hr, sp, gl = v1.text_input("BP"), v2.text_input("HR"), v3.text_input("SpO2"), v4.text_input("Gluc")
            if st.button("Seal Vitals"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"bp":bp,"hr":hr,"spo2":sp,"glucose":gl}).execute()

        with st.expander("🕒 Continence Round", expanded=False):
            st.caption("“In serving the least of these, we serve Christ.”")
            bm_ur = st.radio("Output:", ["None", "Urine", "BM", "Both"], horizontal=True)
            det = st.text_input("Details:")
            if st.button("Seal Continence"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"output_type":bm_ur,"output_details":det}).execute()

        #
