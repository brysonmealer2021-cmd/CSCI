import streamlit as st
import pandas as pd
from supabase import create_client
import random
from datetime import datetime, timedelta

# 1. THE TOOLS
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 2. THE MEMORY
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steward_name' not in st.session_state:
    st.session_state.steward_name = ""
if 'steward_role' not in st.session_state:
    st.session_state.steward_role = ""
if 'blessing_received' not in st.session_state:
    st.session_state.blessing_received = False
if 'daily_blessing' not in st.session_state:
    st.session_state.daily_blessing = ""

# --- THE PRAYER RINGS ---
blessings_map = {
    "gay": [
        "O Lord Almighty, the Healer of our souls and bodies, visit Thy servant in her physical trial. Grant her patience and restore her to health.",
        "O Christ, who alone art our Defender, visit and heal Thy suffering servant. Deliver her from sickness and bitter pain.",
        "Holy Father, Physician of our souls and bodies, send down Thy healing power. Comfort her in her weakness and grant her quiet strength.",
        "O Lord, look down with mercy upon Thy servant. Ease her bodily distress and wrap her in the grace of Thy healing.",
        "Most Holy Theotokos, cover Thy servant with thy protecting veil. Grant her bodily endurance and deep, abiding peace."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her the physical strength to run the race and the spiritual patience.",
        "Establish the work of her hands, O Lord. Give her endurance in her body and stillness in her heart as she tends to her family.",
        "O Christ, who blessed the children, grant this mother the wisdom of the saints and unwavering energy.",
        "Lord, bless her efforts to build a strong vessel. Grant her health of body and clarity of mind.",
        "Most Holy Theotokos, guide this mother's daily labor. Multiply her strength and surround her house with grace."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family. Give her broad shoulders.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom and rest from her heavy burdens.",
        "O Christ, support Thy servant under the weight of her responsibilities. Let her not grow weary in well-doing.",
        "Establish her steps, O Lord, as she navigates the heavy trails for her family.",
        "O Master, look upon the one who bears the yoke of leadership in this house. Grant her rest and steady hands."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts and still the storms within.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind. Grant her a deep and abiding stillness.",
        "Cast all your anxieties on Him, because He cares for you. O Lord, wrap her in Thy calm.",
        "O Lord, grant her to meet this day in peace. In all unforeseen events, let her not forget that all are sent by Thee.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant. Bring her the gentle quiet of the Skete."
    ],
    "bryce": [
        "O Lord and Master of my life, grant the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch. Drive away all weariness.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner. Grant me a quiet spirit to tend the elder today.",
        "Having risen from sleep, I offer Thee, O Savior, the midnight song. Grant me to walk this shift pleasing in Thy sight.",
        "The Lord shall preserve thy going out and thy coming in. May He preserve this Cell and the heavy work of thy hands."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    return random.choice(blessings_map.get(name_key, ["Peace be with you."]))

# 3. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    entrance_quotes = [
        "“Come to me, all who labor and are heavy laden, and I will give you rest.” — Matthew 11:28",
        "*O God, come to my assistance; O Lord, make haste to help me.*",
        "“Let not your heart be troubled, neither let it be afraid.” — John 14:27",
        "*Direct my steps according to Your word, and let no iniquity have dominion over me.*",
        "“Cast all your anxieties on Him, because He cares for you.” — 1 Peter 5:7"
    ]
    st.info(random.choice(entrance_quotes))
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
        else:
            st.error("Credential error.")

# 4. THE BLESSING GATE
elif not st.session_state.blessing_received:
    with st.container(border=True):
        st.subheader("☦️ A Blessing for the Watch")
        st.write(f"*{st.session_state.daily_blessing}*")
        if st.button("Amen", type="primary", use_container_width=True):
            st.session_state.blessing_received = True
            st.rerun()

# 5. THE SACRED VIGIL
else:
    # --- SIDEBAR ---
    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    st.sidebar.divider()
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        watch_title = "🌅 Morning Light"
        time_quotes = ["“Grant me to greet the coming day in peace.”", "“Having risen from sleep, we fall down before Thee.”"]
    elif 12 <= current_hour < 18:
        watch_title = "☀️ Midday Labor"
        time_quotes = ["“Establish the work of our hands upon us.”", "“A humble man is never rushed.”"]
    elif 18 <= current_hour < 21:
        watch_title = "🕯️ Evening Watch"
        time_quotes = ["“Let my prayer arise as incense.”", "“Gladsome Light of the holy glory.”"]
    else:
        watch_title = "🌌 Night Vigil"
        time_quotes = ["“Behold, the Bridegroom comes at midnight.”", "“I remember Thee upon my bed.”"]
    
    st.sidebar.subheader(watch_title)
    st.sidebar.caption(f"*{random.choice(time_quotes)}*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Jesus Prayer")
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me.*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Trisagion")
    st.sidebar.caption("*Holy God, Holy Mighty, Holy Immortal, have mercy on us.*")
    
    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("The Day's Labor")
    
    ephrem = [
        "“O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk.”",
        "“But give rather the spirit of chastity, humility, patience, and love to Thy servant.”",
        "“Yea, O Lord and King, grant me to see my own transgressions, and not to judge my brother.”"
    ]
    st.info(random.choice(ephrem))

    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady and your father is in good hands. The daily labor here is focused entirely on his comfort and honor, kept with deep respect under watchful eyes. You carry no burden of the work today—the steward's tools are set aside for you. The complete ledger is laid open below so you can trace the quiet history of his days and know he is well loved.")
    else:
        shift = st.radio("Select your active vigil:", ["Day", "Night", "Overnight"], horizontal=True)

        # --- VITALS ---
        with st.expander("🩺 Vitals", expanded=False):
            st.caption(random.choice(["“A man ought to take heed to his own measure.”", "“The work of your hands is a vigil.”"]))
            v1, v2, v3, v4 = st.columns(4)
            bp, hr, sp, gl = v1.text_input("BP"), v2.text_input("HR"), v3.text_input("SpO2"), v4.text_input("Glucose")
            if st.button("Seal Vitals"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"bp":bp,"hr":hr,"spo2":sp,"glucose":gl}).execute()
                st.success("Vitals sealed.")

        # --- CONTINENCE ---
        with st.expander("🕒 Continence Round", expanded=False):
            st.caption(random.choice(["“In serving the least of these, we serve Christ.”", "“Cleanse the vessel, tend the spirit.”"]))
            bm_ur = st.radio("Output:", ["None", "Urine", "Bowel Movement", "Both"], horizontal=True)
            det = st.text_input("Details/Amount:")
            if st.button("Seal Continence"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"output_type":bm_ur,"output_details":det}).execute()
                st.success("Continence recorded.")

        # --- NUTRITION & HYDRATION ---
        with st.expander("🍲 Nutrition & Hydration", expanded=False):
            st.caption(random.choice(["“Whether you eat or drink, do all to the glory of God.”", "“Eat your bread in silence.”"]))
            m_type = st.selectbox("Intake Type", ["Water/Fluid", "Small Snack", "Breakfast", "Lunch", "Dinner"])
            amt = st.slider("% Consumed / mL", 0, 500, 0, 50)
            if st.button("Seal Intake"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"meal_info":f"{m_type}: {amt}"}).execute()
                st.success("Intake recorded.")

        # --- GENERAL LEDGER (MEDS & HYGIENE) ---
        st.header("💊 General Care & Medications")
        with st.container(border=True):
            if shift == "Day":
                st.markdown("**Morning/Noon Meds**")
                st.checkbox("Potassium / Citalopram / Furosemide")
                st.checkbox("Lantus (20 units) / Aspirin / Metoprolol")
