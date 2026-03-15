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
        "Holy Father, Physician of our souls and bodies, send down Thy healing power. Comfort her in her weakness and grant her quiet strength."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her the physical strength to run the race.",
        "Establish the work of her hands, O Lord. Give her endurance in her body as she tends to her family.",
        "Most Holy Theotokos, guide this mother's daily labor. Multiply her strength and surround her house with grace."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family. Give her broad shoulders.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom and rest from her heavy burdens.",
        "O Master, look upon the one who bears the yoke of leadership in this house. Grant her rest and steady hands."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant. Bring her the gentle quiet of the Skete."
    ],
    "bryce": [
        "O Lord and Master of my life, grant the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner. Grant me a quiet spirit to tend the elder today."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    return random.choice(blessings_map.get(name_key, ["Peace be to this house."]))

# 3. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    entrance_quotes = [
        "“Come to me, all who labor and are heavy laden...”",
        "*O God, come to my assistance; O Lord, make haste to help me.*",
        "“Let not your heart be troubled, neither let it be afraid.”"
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
        watch_title, watch_quote = "🌅 Morning Light", "“Grant me to greet the coming day in peace.”"
    elif 12 <= current_hour < 18:
        watch_title, watch_quote = "☀️ Midday Labor", "“Establish the work of our hands.”"
    elif 18 <= current_hour < 21:
        watch_title, watch_quote = "🕯️ Evening Watch", "“Let my prayer arise as incense.”"
    else:
        watch_title, watch_quote = "🌌 Night Vigil", "“Behold, the Bridegroom comes at midnight.”"
    
    st.sidebar.subheader(watch_title)
    st.sidebar.caption(f"*{watch_quote}*")
    st.sidebar.divider()
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me.*")
    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("The Day's Labor")
    
    st.info(random.choice([
        "“O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk.”",
        "“But give rather the spirit of chastity, humility, patience, and love to Thy servant.”",
        "“Yea, O Lord and King, grant me to see my own transgressions, and not to judge my brother.”"
    ]))

    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady and your father is in good hands. The complete ledger is laid open below.")
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

        # --- SPLIT NUTRITION & HYDRATION ---
        with st.expander("🍲 Nutrition & Hydration", expanded=False):
            col_food, col_water = st.columns(2)
            
            with col_food:
                st.markdown("### 🍞 Food")
                st.caption("“Eat your bread in silence.”")
                food_desc = st.text_input("What was eaten?")
                food_pct = st.slider("% Consumed", 0, 100, 0, 25)
                if st.button("Seal Food"):
                    supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"meal_info":f"Food: {food_desc} ({food_pct}%)"}).execute()
                    st.success("Food recorded.")
            
            with col_water:
                st.markdown("### 💧 Hydration")
                st.caption("“The fountain of life.”")
                drink_desc = st.text_input("What was drunk?")
                drink_ml = st.slider("Amount (mL)", 0, 500, 0, 50)
                if st.button("Seal Drink"):
                    supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"meal_info":f"Drink: {drink_desc} ({drink_ml}mL)"}).execute()
                    st.success("Hydration recorded.")

        # --- GENERAL LEDGER ---
        st.header("💊 General Care & Medications")
        with st.container(border=True):
            if shift == "Day":
                st.markdown("**Morning/Noon Meds**")
                st.checkbox("Potassium / Citalopram / Furosemide")
                st.checkbox("Lantus (20 units) / Aspirin / Metoprolol")
                st.checkbox("Zinc / Elderberry / Rosuvastatin / Timolol Drops")
            elif shift == "Night":
                st.markdown("**Evening/Bedtime Meds**")
                st.checkbox("Magnesium / Oxybutynin / Potassium")
                st.checkbox("Finasteride / Donepezil / Melatonin / Advil PM / Latanoprost")
            
            st.markdown("**➕ PRN (As Needed)**")
            st.checkbox("Phenazopyridine / Acetaminophen / Guaifenesin / Novolog / Diclofenac / Ondansetron / Pantoprazole")

            st.divider()
            st.markdown("**🧹 Daily Hygiene**")
            st.caption("“To instruct your neighbor is like building a church.”")
            h1, h2 = st.columns(2)
            with h1: 
                st.checkbox("Oral Care / Dentures"); st.checkbox("Bathing / Grooming")
            with h2: 
                st.checkbox("Laundry / Surfaces"); st.checkbox("Room Tidied")

            care_notes = st.text_area("Detailed Care Notes:")
            if st.button("Seal the General Ledger", type="primary"):
                supabase.table("care_logs").insert({"steward":st.session_state.steward_name,"shift":shift,"medications":"Routine/PRN Recorded","notes":care_notes}).execute()
                st.success("Ledger sealed.")

    # --- HISTORY ---
    st.divider()
    st.header("📜 Vigil History")
    recent = supabase.table("care_logs").select("*").order("created_at", desc=True).limit(50).execute()
    if recent.data:
        df = pd.DataFrame(recent.data)
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%m/%d/%Y %H:%M')
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("🖨️ Bind Records to CSV", data=csv, file_name=f"Care_Logs_{datetime.now().strftime('%m_%d_%Y')}.csv", mime="text/csv")
