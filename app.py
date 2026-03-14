import streamlit as st
import pandas as pd
import random
from datetime import date
from supabase import create_client

# 1. CONNECTION
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.set_page_config(page_title="Charles Smith Care Initiative", layout="wide")

# 2. LITURGICAL DATE & WISDOM
today = date.today()
today_display = today.strftime("%B %d, %Y")

def get_steward_wisdom():
    # 2026 Lenten Calendar
    clean_monday = date(2026, 2, 23)
    delta = (today - clean_monday).days + 1
    
    # Sayings of the Saints and Desert Fathers
    wisdom_well = [
        "“He who carries a lantern at night stumbling is more to be pitied than he who has no lantern.” — St. Isaac the Syrian",
        "“Prayer is the wing of the soul.” — St. John Climacus",
        "“Acquire a peaceful spirit, and around you thousands will be saved.” — St. Seraphim of Sarov",
        "“The beginning of prayer is the expulsion of distractions.” — St. John of the Ladder",
        "“Do not be surprised if you fall every day; do not give up, but stand your ground.” — St. John Climacus",
        "“Love is the reason for every good thing.” — St. Maximus the Confessor",
        "“As a man who is thirsty, seek the prayer of the heart.” — The Desert Fathers",
        "“Be like a watchman at the gates of your heart.” — St. Hesychios the Priest"
    ]
    
    lit = {
        "saint": "Translation of the Relics of St. Nicephorus, Patriarch of Constantinople",
        "word": wisdom_well[today.day % len(wisdom_well)]
    }
    
    # Lent Tracker logic
    if 1 <= delta <= 40:
        period = f"Day {delta} of Great Lent"
    elif 40 < delta <= 48:
        period = "Holy and Great Week"
    else:
        period = "The Cycle of the Year"
        
    return lit, period

# 3. BLESSINGS
gate_blessings = ["Peace be to this Skete.", "Welcome, fellow steward.", "Glory to Jesus Christ!", "Enter the vigil in peace."]
report_blessings = ["The shift is secured. Go in peace.", "The flock is tended. May your rest be holy.", "Record sealed. Strength to your heart."]

# 4. LOGIN (Case-Insensitive)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("Steward Login")
    st.info(random.choice(gate_blessings))
    
    user_input_raw = st.text_input("Steward Name")
    user_input = user_input_raw.lower().strip() 
    pin_input = st.text_input("4-Digit PIN", type="password")
    
    if st.button("Open the Ledger"):
        res = supabase.table("users").select("*").eq("username", user_input).eq("pin", pin_input).execute()
        if user_input == "Bryce" and pin_input == "1580":
            st.session_state["authenticated"] = True
            st.session_state["username"] = "Bryce"
            st.session_state["role"] = "manager"
            st.rerun()

        if res.data:
            st.session_state["authenticated"] = True
            st.session_state["username"] = res.data[0].get('username').capitalize()
            st.session_state["role"] = res.data[0].get('role', 'steward')
            st.rerun()
        else:
            st.error("The gate is barred. Check name or PIN.")
else:
    role = st.session_state["role"]
    username = st.session_state["username"]
    lit, period = get_steward_wisdom()

    # SIDEBAR: Date, Lent Tracker, and Wisdom
    st.sidebar.title("☦️ Vigil Compass")
    st.sidebar.subheader(today_display)
    st.sidebar.markdown(f"**{period}**")
    st.sidebar.divider()
    st.sidebar.info(f"**Commemoration:**\n{lit['saint']}")
    st.sidebar.write("**A Word from the Elders:**")
    st.sidebar.caption(f"_{lit['word']}_")
    st.sidebar.divider()
    if st.sidebar.button("Leave the Vigil"):
        st.session_state.clear()
        st.rerun()

    if role in ["steward", "manager"]:
        st.title(f"Care Ledger — {username}")
        
        # I. TOILETING ROUND
        with st.expander("🕒 2-Hour Toileting Round", expanded=True):
            st.caption("“Lord Jesus Christ, Son of God, have mercy on us.”")
            with st.form("quick_toilet"):
                t_time = st.selectbox("Round Time", ["8 AM", "10 AM", "12 PM", "2 PM", "4 PM", "6 PM", "8 PM", "10 PM", "12 AM", "2 AM", "4 AM", "6 AM"])
                t_status = st.radio("Status", ["Dry/Clean", "BM", "Both", "Changed"], horizontal=True)
                cath_ml = st.number_input("Catheter Amount (mL)", 0, 2000, 0, step=50)
                t_obs = st.text_input("Observations")
                if st.form_submit_button("Log Round"):
                    supabase.table("care_logs").insert({"steward": username, "entry_type": "toileting_round", "toileting": f"{t_time}: {t_status} | Cath: {cath_ml}mL", "notes": t_obs}).execute()
                    st.toast("Round secured.")

        # II. FULL SHIFT REPORT
        st.divider()
        st.header("Full Shift Report")
        active_shift = st.selectbox("Current Shift", ["Night Shift", "Overnight Shift (Vigil)", "Day Shift"])
        
        with st.form("main_report_form"):
            st.subheader("Medication Administration")
            selected_scheduled = []
            
            if active_shift == "Night Shift":
                st.caption("“The Lord is my Shepherd; I shall not want.”")
                st.write("**Evening & Night Medications (PM/NIGHT):**")
                night_meds = [
                    "Evening: Mag Oxide (400mg x2)", "Evening: Oxybutynin (10mg)", 
                    "Evening: Potassium (10 MEQ x2)", "Night: Finasteride (5mg)", 
                    "Night: Donepezil (5mg)", "Night: Melatonin (10mg)", 
                    "Night: Advil PM", "Night: Latanoprost Drops"
                ]
                for m in night_meds:
                    if st.checkbox(m): selected_scheduled.append(m)
            
            elif active_shift == "Day Shift":
                st.caption("“The Lord is my Shepherd; I shall not want.”")
                st.write("**Morning & Noon Medications:**")
                day_meds = [
                    "Morning: Potassium (x2)", "Morning: Citalopram", "Morning: Furosemide", 
                    "Morning: Lantus (20u)", "Morning: Aspirin", "Morning: Metoprolol", 
                    "Morning: Lactobacillus", "Morning: Dorzolamide Drops", "Noon: Zinc", 
                    "Noon: Elderberry", "Noon: Rosuvastatin"
                ]
                for m in day_meds:
                    if st.checkbox(m): selected_scheduled.append(m)
            else:
                st.info("Overnight Vigil: Log PRN usage below.")

            st.write("**As Needed (PRN):**")
            prn_options = ["PRN: Phenazopyridine", "PRN: Acetaminophen", "PRN: Guaifenesin", "PRN: Novolog Sliding Scale", "PRN: Diclofenac Gel"]
            selected_prns = [p for p in prn_options if st.checkbox(p)]
            
            st.divider()
            st.subheader("Vitals & Intake")
            st.caption("“A heart at peace gives life to the body.”")
            v1, v2, v3, v4 = st.columns(4)
            with v1: sugar = st.number_input("Blood Sugar", 0, 500, 100)
            with v2: food = st.slider("Food Intake %", 0, 100, 100)
            with v3: fluids = st.number_input("Oral Fluids (oz)", 0, 120, 8)
            with v4: Blood_Pressure = st.text_input("Blood Pressure", placeholder="120/80")
            
            st.caption("“Keep thy heart with all diligence...”")
            final_notes = st.text_area("Shift Observations")

            if st.form_submit_button("Secure Full Ledger Entry"):
                supabase.table("care_logs").insert({
                    "steward": username, "shift": active_shift, "blood_pressure": blood_pressure, "blood_sugar": sugar,
                    "meds_given": ", ".join(selected_scheduled + selected_prns), "notes": final_notes
                }).execute()
                st.success(random.choice(report_blessings))

    # III. HISTORY
    st.divider()
    st.subheader("📜 Recent Vigil History")
    history = supabase.table("care_logs").select("*").order("created_at", desc=True).limit(25).execute()
    if history.data:
        st.dataframe(pd.DataFrame(history.data)[['created_at', 'steward', 'blood_sugar', 'toileting', 'notes']], use_container_width=True)

