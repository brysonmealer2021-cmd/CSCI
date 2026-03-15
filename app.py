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
        dynamic_title
